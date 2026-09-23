#!/usr/bin/env python3
"""Check and publish one Bluesky post from a draft file.

    python3 social/bsky.py check social/drafts/day-02.md
    python3 social/bsky.py post  social/drafts/day-02.md

`check` never touches the network. `post` runs every check again, asks
Bluesky whether this day is already on the account, and only then uploads
and posts. Nothing here runs on a schedule: a post happens only when a
person has said "post it" and someone runs `post` by hand.

Credentials come from the environment and nowhere else:
    BLUESKY_HANDLE          shirshacreates.bsky.social
    BLUESKY_APP_PASSWORD    an app password, never the account password

Draft format: header lines, a line of three dashes, then the post text.
    day: 2
    media: assets/route_map.png
    media: assets/woodblock_full.png | optional alt text override
    ---
    Day 2/16 · Japan trip, visualized 🇯🇵
    ...

Alt text defaults to the file's row in assets/README.md.
"""
import json, os, re, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import privacy_gate  # noqa: E402

RECORD = ROOT / "social" / "posted.json"
SERVICE = "https://bsky.social"
LIMIT = 300                       # graphemes, as Bluesky counts them
HEADER = "Day {n}/16 · Japan trip, visualized 🇯🇵"
FOOTER = "#buildinpublic #dataviz"
IMAGE_MAX = 1_000_000             # Bluesky rejects images over ~976 KB
VIDEO_MAX = 100_000_000
IMAGES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
VIDEOS = {".mp4": "video/mp4"}

# Shopping and gifts are never posted. Words, not substrings, so "shop"
# does not trip on "workshop".
BANNED = re.compile(r"(?i)\b(shop|shops|shopping|shopped|gift|gifts|gifted|souvenirs?|"
                    r"purchases? for|bought for)\b")


# --- counting ---------------------------------------------------------------

def graphemes(text):
    """Count user-perceived characters the way Bluesky does.

    Covers what these posts contain: a flag is two regional indicators and
    counts once; combining marks, variation selectors, skin tones and
    zero-width-joined emoji attach to the character before them.
    """
    count, prev, ri_open = 0, "", False
    for ch in text:
        cp = ord(ch)
        is_ri = 0x1F1E6 <= cp <= 0x1F1FF
        attaches = (unicodedata.combining(ch) or 0xFE00 <= cp <= 0xFE0F
                    or 0x1F3FB <= cp <= 0x1F3FF or cp == 0x200D or prev == "‍"
                    or 0xE0020 <= cp <= 0xE007F)
        if is_ri and ri_open:
            ri_open = False
        elif attaches:
            pass
        elif ch == "\n" and prev == "\r":
            pass
        else:
            count += 1
            ri_open = is_ri
        prev = ch
    return count


# --- draft ------------------------------------------------------------------

def alt_from_readme(name):
    for line in (ROOT / "assets" / "README.md").read_text().splitlines():
        m = re.match(r"\|\s*`([^`]+)`\s*\|\s*(.+?)\s*\|", line)
        if m and m.group(1) == name:
            return m.group(2)
    return ""


def load(path):
    head, _, text = Path(path).read_text().partition("\n---\n")
    day, media = None, []
    for line in head.splitlines():
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if key == "day":
            day = int(val)
        elif key == "media":
            file, _, alt = (s.strip() for s in val.partition("|"))
            media.append({"path": ROOT / file, "alt": alt or alt_from_readme(Path(file).name)})
    return day, text.strip("\n"), media


def check(day, text, media):
    """Return a list of problems. Empty means the draft may be shown."""
    problems = []
    if day is None:
        problems.append("no `day:` line")
    elif text.splitlines()[0] != HEADER.format(n=day):
        problems.append(f"first line is not exactly: {HEADER.format(n=day)}")
    if not text.rstrip().endswith(FOOTER):
        problems.append(f"does not end with: {FOOTER}")
    if graphemes(text) > LIMIT:
        problems.append(f"{graphemes(text)} characters, limit {LIMIT}")
    if len(text.encode()) > 3000:
        problems.append("over 3000 bytes")
    for no, kind in privacy_gate._scan_text(text):
        problems.append(f"privacy: {kind} on line {no}")
    for no, line in enumerate(text.splitlines(), 1):
        if BANNED.search(line):
            problems.append(f"shopping/gifts wording on line {no}")

    kinds = set()
    for m in media:
        p, suffix = m["path"], m["path"].suffix.lower()
        if not p.is_file():
            problems.append(f"missing file: {p.relative_to(ROOT)}")
            continue
        kind = "image" if suffix in IMAGES else "video" if suffix in VIDEOS else None
        if not kind:
            problems.append(f"not an image or mp4: {p.name}")
            continue
        kinds.add(kind)
        if p.stat().st_size > (IMAGE_MAX if kind == "image" else VIDEO_MAX):
            problems.append(f"too large for Bluesky: {p.name}")
        if not m["alt"]:
            problems.append(f"no alt text for {p.name}")
        for where, k in privacy_gate._scan_binary(p.read_bytes()):
            problems.append(f"privacy: {k} in {p.name} metadata at {where}")
        if m["alt"] and list(privacy_gate._scan_text(m["alt"])):
            problems.append(f"privacy: alt text for {p.name}")
    if len(kinds) > 1:
        problems.append("images and a video together; Bluesky takes one or the other")
    if "image" in kinds and len(media) > 4:
        problems.append("more than 4 images")
    if "video" in kinds and len(media) > 1:
        problems.append("more than 1 video")
    if day is not None and any(r["day"] == day for r in record()):
        problems.append(f"day {day} is already in social/posted.json")
    return problems


def record():
    return json.loads(RECORD.read_text()) if RECORD.exists() else []


# --- Bluesky ----------------------------------------------------------------

def xrpc(method, token=None, body=None, raw=None, mime=None, params=None, base=SERVICE):
    url = f"{base}/xrpc/{method}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = None
    if body is not None:
        data, headers["Content-Type"] = json.dumps(body).encode(), "application/json"
    elif raw is not None:
        data, headers["Content-Type"] = raw, mime
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        # The response body can echo the request; say only what failed.
        sys.exit(f"Bluesky refused {method}: HTTP {e.code}")


def hashtag_facets(text):
    """Bluesky does not link hashtags by itself; the client must say where."""
    facets = []
    for m in re.finditer(r"(?<!\S)#(\w+)", text):
        start = len(text[:m.start()].encode())
        facets.append({"index": {"byteStart": start, "byteEnd": start + len(m.group().encode())},
                       "features": [{"$type": "app.bsky.richtext.facet#tag", "tag": m.group(1)}]})
    return facets


def already_posted(did, token, day):
    marker = f"Day {day}/16"
    cursor = None
    for _ in range(10):
        params = {"actor": did, "limit": 100, "filter": "posts_no_replies"}
        if cursor:
            params["cursor"] = cursor
        feed = xrpc("app.bsky.feed.getAuthorFeed", token, params=params)
        for item in feed.get("feed", []):
            if item["post"]["record"].get("text", "").startswith(marker):
                return item["post"]["uri"]
        cursor = feed.get("cursor")
        if not cursor:
            return None
    return None


def video_embed(session, m):
    """Upload through Bluesky's video service, which transcodes and returns a blob."""
    did, token, pds = session["did"], session["accessJwt"], session["pds"]
    host = pds.split("//", 1)[1]
    auth = xrpc("com.atproto.server.getServiceAuth", token,
                params={"aud": f"did:web:{host}", "lxm": "com.atproto.repo.uploadBlob",
                        "exp": int(datetime.now().timestamp()) + 1800})["token"]
    job = xrpc("app.bsky.video.uploadVideo", auth, raw=m["path"].read_bytes(), mime="video/mp4",
               params={"did": did, "name": m["path"].name}, base="https://video.bsky.app")
    for _ in range(120):
        status = xrpc("app.bsky.video.getJobStatus", auth, params={"jobId": job["jobId"]},
                      base="https://video.bsky.app")["jobStatus"]
        if status.get("blob"):
            return {"$type": "app.bsky.embed.video", "video": status["blob"], "alt": m["alt"]}
        if status.get("state") == "JOB_STATE_FAILED":
            sys.exit("Bluesky could not process the video")
        time.sleep(2)
    sys.exit("video processing did not finish in four minutes")


def post(day, text, media, draft):
    handle = os.environ.get("BLUESKY_HANDLE")
    password = os.environ.get("BLUESKY_APP_PASSWORD")
    if not handle or not password:
        sys.exit("BLUESKY_HANDLE and BLUESKY_APP_PASSWORD must be set in the environment")

    s = xrpc("com.atproto.server.createSession", body={"identifier": handle, "password": password})
    did, token = s["did"], s["accessJwt"]
    s["pds"] = next((svc["serviceEndpoint"] for svc in s.get("didDoc", {}).get("service", [])
                     if svc.get("id") == "#atproto_pds"), SERVICE)

    existing = already_posted(did, token, day)
    if existing:
        sys.exit(f"Day {day} is already on the account: {existing}. Nothing posted.")

    rec = {"$type": "app.bsky.feed.post", "text": text, "langs": ["en"],
           "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")}
    facets = hashtag_facets(text)
    if facets:
        rec["facets"] = facets
    if media and media[0]["path"].suffix.lower() in VIDEOS:
        rec["embed"] = video_embed(s, media[0])
    elif media:
        images = []
        for m in media:
            blob = xrpc("com.atproto.repo.uploadBlob", token, raw=m["path"].read_bytes(),
                        mime=IMAGES[m["path"].suffix.lower()])["blob"]
            images.append({"image": blob, "alt": m["alt"]})
        rec["embed"] = {"$type": "app.bsky.embed.images", "images": images}

    out = xrpc("com.atproto.repo.createRecord", token,
               body={"repo": did, "collection": "app.bsky.feed.post", "record": rec})
    rkey = out["uri"].rsplit("/", 1)[1]
    url = f"https://bsky.app/profile/{handle}/post/{rkey}"

    entries = record() + [{"day": day, "posted_at": rec["createdAt"], "url": url,
                           "uri": out["uri"], "draft": str(Path(draft).relative_to(ROOT)),
                           "text": text,
                           "media": [str(m["path"].relative_to(ROOT)) for m in media]}]
    RECORD.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n")
    print(f"Posted: {url}")


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("check", "post"):
        sys.exit(__doc__)
    day, text, media = load(sys.argv[2])
    problems = check(day, text, media)

    print(text)
    print("\n" + "-" * 40)
    print(f"{graphemes(text)} / {LIMIT} characters, as Bluesky counts them")
    for m in media:
        print(f"  {m['path'].relative_to(ROOT)}  ({m['path'].stat().st_size // 1000} KB)"
              if m["path"].is_file() else f"  {m['path']}")
        print(f"    alt: {m['alt']}")
    if problems:
        print("\nNOT READY:\n" + "\n".join(f"  - {p}" for p in problems))
        sys.exit(1)
    print("\nAll checks pass. Images and video still need a human look: "
          "the privacy gate cannot read pixels.")
    if sys.argv[1] == "post":
        post(day, text, media, sys.argv[2])


if __name__ == "__main__":
    main()
