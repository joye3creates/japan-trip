#!/usr/bin/env python3
"""Assemble site/ from the templates. Only what this script writes gets deployed.

Run order for a full rebuild:
    python3 extract.py && python3 build_dataset.py && python3 synth_times.py
    python3 build_site.py
"""
import html as H, json, re, shutil, sys
from pathlib import Path

import privacy_gate

ROOT = Path(__file__).resolve().parent
DATA, SITE, ASSETS = ROOT / "data", ROOT / "site", ROOT / "assets"
EXPLORE = ROOT / "explorations"

# template, dataset, output. The route map keeps the unfiltered dataset on
# purpose: it is the day-one artefact and later exclusions must not rewrite it.
PAGES = [
    ("app.template.html",   "trip_full.json", "route-map.html",  "Route map",
     "The first build. A geographic route diagram, day rail, and the full ledger."),
    ("ukiyo.template.html", "trip.json",      "woodblock.html",  "Woodblock sheet",
     "The same trip drawn as an aged survey map, on real prefecture coastlines."),
    ("scroll.template.html","trip.json",      "scroll.html",     "Scroll draft",
     "First scroll-driven version, where the map dissolves into a price ledger."),
    ("clock.template.html", "trip.json",      "clock.html",      "A day at a time",
     "The current build. Sixteen days by the hour, with a switch to the ledger."),
]

def photos():
    """What the page needs to show a photograph on a mark.

    `photo_meta.json` is written by scrub_photos.py and holds only what the
    original file knew: a capture time, sometimes coordinates. `photo_attach.json`
    is hand-edited and supplies what the file could not, which for a photograph
    sent through a messaging app is everything. A record ends up attached either
    to one named mark, or to a place on a day.
    """
    meta = json.loads((DATA / "photo_meta.json").read_text()) if (DATA / "photo_meta.json").is_file() else {}
    attach = json.loads((ROOT / "data/photo_attach.json").read_text()) if (ROOT / "data/photo_attach.json").is_file() else {}
    out = []
    for name in sorted(meta):
        a = attach.get(name) or {}
        rec = {"file": name, "caption": a.get("caption", "")}
        if a.get("mark"):
            rec["mark"] = a["mark"]
        else:
            # The file's own day wins where it has one. Where the two disagree
            # the hand-edit is wrong about a file that knew better, and that is
            # worth stopping for rather than quietly preferring one.
            fday, hday = meta[name].get("day_index"), a.get("day_index")
            if fday is not None and hday is not None and fday != hday:
                sys.exit(f"\nPHOTOS: {name} was taken on day {fday} but is attached to day {hday}")
            day = fday if fday is not None else hday
            if day is None or not a.get("place_id"):
                continue                      # nowhere to put it; say nothing
            rec["day"], rec["place"] = day, a["place_id"]
        if meta[name].get("taken"):
            rec["taken"] = meta[name]["taken"]
        out.append(rec)

    # Stand-ins, one per category, so every mark has a picture while the real
    # photographs are still being chosen. They carry no caption and the page
    # labels them, because a real photograph shown against a purchase it has
    # nothing to do with is the one thing this project must not do quietly.
    for cat, entries in sorted((attach.get("_placeholder_by_category") or {}).items()):
        if cat.startswith("_"):
            continue
        for e in ([entries] if isinstance(entries, (str, dict)) else entries):
            e = {"file": e} if isinstance(e, str) else e
            if e["file"] not in meta:
                sys.exit(f"\nPHOTOS: placeholder for {cat} names {e['file']}, "
                         f"which is not in assets/photos/")
            rec = {"file": e["file"], "category": cat, "placeholder": True}
            if e.get("rotate"):
                rec["rotate"] = e["rotate"]
            out.append(rec)

    # A mistyped place or mark attaches a photograph to nothing at all, and the
    # page has no way to say so: the picture simply never appears.
    trip = json.loads((DATA / "trip.json").read_text())
    places = {p["id"] for p in trip["places"]}
    marks = {m["id"] for m in trip["marks"]}
    day_places = [set(d.get("places") or []) for d in trip["days"]]
    cats = {m.get("category") for m in trip["marks"]}
    for r in out:
        if r.get("placeholder") and r["category"] not in cats:
            sys.exit(f"\nPHOTOS: placeholder names category {r['category']}, which nothing is in")
        if "mark" in r and r["mark"] not in marks:
            sys.exit(f"\nPHOTOS: {r['file']} names mark {r['mark']}, which is not in the dataset")
        if "place" in r:
            if r["place"] not in places:
                sys.exit(f"\nPHOTOS: {r['file']} names place {r['place']}, which is not in the registry")
            if r["place"] not in day_places[r["day"]]:
                sys.exit(f"\nPHOTOS: {r['file']} puts {r['place']} on day {r['day']}, "
                         f"which did not go there")
    return out


def main():
    # Everything is staged in memory first. The privacy gate reads all of it,
    # and only a clean pass lets a single byte reach site/.
    staged = {}
    geo = (DATA / "japan_geo.json").read_text()
    built = []
    for tpl, ds, out, title, blurb in PAGES:
        html = (ROOT / tpl).read_text()
        html = html.replace("/*__TRIP_DATA__*/", (DATA / ds).read_text())
        html = html.replace("/*__GEO__*/", geo)
        html = html.replace("/*__PHOTOS__*/", json.dumps(photos(), separators=(",", ":")))
        # Netlify sends a charset header, so a missing declaration never shows
        # up on the deployed page. Every review copy is opened as a local file,
        # where the browser guesses instead, and yen signs and em dashes come
        # out as mojibake. Declared here so no template can forget.
        if "charset" not in html[:2048]:
            html = '<meta charset="utf-8">\n' + html
        staged[out] = html
        built.append((out, title, blurb, len(html) // 1024))
        print(f"  {out:<18} {len(html)//1024:>4} KB   from {tpl} + {ds}")

    # The interaction studies, served as they were made. They are dead ends and
    # chosen designs both, and the log entries point at them, so they go up
    # beside the pages rather than living only in a chat.
    for f in sorted(EXPLORE.glob("*.html")) if EXPLORE.is_dir() else []:
        staged[f"explore/{f.name}"] = f.read_text()
        print(f"  {'explore/'+f.name:<18} {len(staged['explore/'+f.name])//1024:>4} KB")

    # robots.txt is written by hand into site/ and must survive a rebuild
    staged["robots.txt"] = ROBOTS
    print(f"  {'robots.txt':<18} {len(ROBOTS)//1024:>4} KB")

    cards = "\n".join(
        f'      <a class="card" href="{o}"><h2>{t}</h2><p>{b}</p>'
        f'<span class="sz">{k} KB</span></a>' for o, t, b, k in built)
    # The four-card index of earlier builds lives at /builds.html. The build log
    # is the front page, and stays at /log.html too so shared links keep working.
    staged["builds.html"] = INDEX.replace("<!--CARDS-->", cards)
    print(f"  {'builds.html':<18} {len(INDEX)//1024:>4} KB")

    log_html, status = build_log(set(staged))
    staged["index.html"] = staged["log.html"] = log_html
    # A tiny public fact sheet, so the card on the portfolio can read the day
    # number instead of being edited by hand. Sorted keys and no timestamp, so
    # it only changes when the log does.
    staged["status.json"] = json.dumps(status, sort_keys=True, indent=2) + "\n"
    print(f"  {'status.json':<18} {len(staged['status.json'])//1024:>4} KB   day {status['day']} of {status['total']}")
    print(f"  {'index.html':<18} {len(staged['index.html'])//1024:>4} KB   from log.template.html + BUILDING_IN_PUBLIC.md, also as log.html")

    # Only the media a page actually links. Anything else in assets/ would get
    # a public URL without having been reviewed for this context.
    refs = {r for v in staged.values() if isinstance(v, str)
            for r in re.findall(r'(?:src|href|poster)="(assets/[^"#?]+)"', v)}
    # Photographs are named by the data, not by a tag in the template. Adding
    # one to photo_attach.json used to need a matching <link> hand-written into
    # the page or the file silently never reached site/.
    refs |= {"assets/photos/" + p["file"] for p in photos()}
    refs = sorted(refs)
    missing = [r for r in refs if not (ROOT / r).is_file()]
    if missing:
        sys.exit("\nASSETS: linked from a page but not in assets/: " + ", ".join(missing))
    for r in refs:
        staged[r] = (ROOT / r).read_bytes()
    print(f"  {'assets/':<18} {sum(len(staged[r]) for r in refs)//1024:>4} KB   {len(refs)} linked files from assets/")

    privacy_gate.enforce(staged)

    # site/assets/ is wholly generated, so clear it: a file dropped from the
    # page must not linger at its old public URL.
    shutil.rmtree(SITE / "assets", ignore_errors=True)
    for rel, content in staged.items():
        dest = SITE / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        (dest.write_bytes if isinstance(content, bytes) else dest.write_text)(content)
    n = sum(1 for p in SITE.rglob("*") if p.is_file())
    print(f"\nsite/ holds {n} files and nothing else. Only this directory deploys.")


# ---------------------------------------------------------------- build log
# log.html is generated from BUILDING_IN_PUBLIC.md. Only what follows the
# "# Entries" heading is read: everything above it is the internal context
# pack for drafting posts and is never published.
LOG_SRC = ROOT / "BUILDING_IN_PUBLIC.md"

# Field labels are matched by prefix, because they drift: Day 3 has "The
# honest failure, and it is a good one:". Order matters where one prefix
# could swallow another.
FIELDS = [("shipped", "Shipped"), ("number", "The number"),
          ("interesting", "The interesting thing"), ("failure", "The honest failure"),
          ("angle", "Angle worth taking"), ("second", "A second number"),
          ("headline", "Headline"), ("media", "Media"),
          # One markdown link per line, to a page on this site. The studies are
          # the day's real argument on an interaction day, and until now the
          # page had nowhere to put them.
          ("explore", "Explorations"),
          # The recording that plays at the top of the page. The latest day's
          # is the one that plays, so the hero follows the log without a code
          # change, the way each day's still already does.
          ("watch", "Watch")]
REQUIRED = ("shipped", "number", "interesting", "failure", "angle")

# One still per day, found by convention so a new day needs no code change:
# assets/day-NN.png, unless the entry names another file in assets/ with
#     **Media:** <file> — <caption>
# Stills only. The screen recordings run 21s and 25s, too long to loop.
IMAGE_TYPES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
VIDEO_TYPES = {".mp4", ".webm"}

# The trip is sixteen days, so the build is sixteen working days: "Day N of 16".
TOTAL_DAYS = 16

WORDNUM = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve".split())}
FIGURE = re.compile(r"[¥₹$€£]?\d[\d,]*(?:\.\d+)?%?|\b(?:" + "|".join(WORDNUM) + r")\b", re.I)


# [name](page.html) — an optional note, running to the next link or the end.
EXPLORE_LINK = re.compile(r"\[([^\]]+)\]\((?!\w+:)([A-Za-z0-9._\-/#?=]+)\)"
                          r"(?:\s*[—–-]\s*([^\[]+))?")


class LogError(Exception):
    pass


def parse_log(text):
    """Return [{day, title, fields}] in file order. Raises LogError on any gap."""
    lines = text.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == "# Entries")
    except StopIteration:
        raise LogError('no "# Entries" marker; refusing to guess where public text starts')
    days, cur, field = [], None, None
    for no, line in enumerate(lines[start + 1:], start + 2):
        m = re.match(r"##\s+Day\s+(\d+)\s*[—–-]\s*(.+)$", line)
        if m:
            cur = {"day": int(m.group(1)), "title": m.group(2).strip(), "fields": {}, "line": no}
            days.append(cur); field = None
            continue
        if line.startswith("#"):
            raise LogError(f"line {no}: heading is not in the form '## Day N — title'")
        if cur is None:
            if line.strip():
                raise LogError(f"line {no}: text before the first day heading")
            continue
        m = re.match(r"\*\*([^*]+?):\*\*\s*(.*)$", line)
        if m:
            label = m.group(1).strip().lower()
            key = next((k for k, pre in FIELDS if label.startswith(pre.lower())), None)
            if key is None:
                raise LogError(f"line {no}: unrecognised field label on Day {cur['day']}")
            if key in cur["fields"]:
                raise LogError(f"line {no}: Day {cur['day']} has two '{key}' fields")
            field = key
            cur["fields"][key] = [m.group(2)]
        elif field:
            cur["fields"][field].append(line)
        elif line.strip():
            raise LogError(f"line {no}: Day {cur['day']} has text before its first field")
    if not days:
        raise LogError("no days found after the Entries marker")
    for d in days:
        # paragraphs, with the single line breaks inside each one folded away
        d["fields"] = {k: [" ".join(p.split()) for p in "\n".join(v).strip().split("\n\n") if p.strip()]
                       for k, v in d["fields"].items()}
        missing = [k for k in REQUIRED if not d["fields"].get(k)]
        if missing:
            raise LogError(f"Day {d['day']} (line {d['line']}) is missing: {', '.join(missing)}")
        d["media"] = media_for(d)
        d["watch"] = watch_for(d)
    seen = [d["day"] for d in days]
    if sorted(seen) != list(range(1, len(seen) + 1)):
        raise LogError(f"days are not a clean run from 1: {seen}")
    return days


def media_for(d):
    """(filename, caption) for a day. Fails naming the exact file it wanted."""
    caption = f"Day {d['day']}: {plain(d['title'])}"
    if d["fields"].get("media"):
        m = re.fullmatch(r"(\S+)(?:\s+[—–]\s+(.+))?", plain(" ".join(d["fields"]["media"])).strip())
        name = m.group(1) if m else ""
        if not m or "/" in name or "\\" in name or name.startswith("."):
            raise LogError(f"Day {d['day']}: Media must read '<file in assets/> — <caption>'")
        caption = (m.group(2) or caption).strip()
        how = f"named by its **Media:** field"
    else:
        name = f"day-{d['day']:02d}.png"
        how = "by convention, since the entry has no **Media:** field"
    if Path(name).suffix.lower() not in IMAGE_TYPES:
        raise LogError(f"Day {d['day']}: assets/{name} is not a still image")
    if not (ASSETS / name).is_file():
        raise LogError(f"Day {d['day']} wants assets/{name} ({how}); add that file")
    return name, caption


def watch_for(d):
    """(filename, hint) for the day's recording, or None. The hint is what the
    page says under the video, so it is written per day rather than generic."""
    if not d["fields"].get("watch"):
        return None
    m = re.fullmatch(r"(\S+)\s+[—–]\s+(.+)", plain(" ".join(d["fields"]["watch"])).strip())
    name = m.group(1) if m else ""
    if not m or "/" in name or "\\" in name or name.startswith("."):
        raise LogError(f"Day {d['day']}: Watch must read '<file in assets/> — <what it shows>'")
    if Path(name).suffix.lower() not in VIDEO_TYPES:
        raise LogError(f"Day {d['day']}: assets/{name} is not a video")
    if not (ASSETS / name).is_file():
        raise LogError(f"Day {d['day']} wants assets/{name} for its Watch field; add that file")
    return name, m.group(2).strip()


def inline(s):
    """The little markdown these entries use: bold, italic, code."""
    s = H.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    # [text](target), relative targets only. A log entry has no business
    # sending a reader off this site, and a scheme here would be a way to.
    s = re.sub(r"\[([^\]]+)\]\((?!\w+:)([A-Za-z0-9._\-/#?=]+)\)",
               r'<a href="\2">\1</a>', s)
    return re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)


def plain(s):
    return re.sub(r"[*`]", "", s)


def stated_headline(paras):
    """**Headline:** <figure> — <label, six words max>. Stated, not inferred."""
    m = re.fullmatch(r"(\S+)\s+[—–]\s+(.+)", plain(" ".join(paras)).strip())
    if not m:
        raise LogError("Headline must read '<figure> — <label>'")
    fig, label = m.group(1), m.group(2).strip().rstrip(".")
    if len(label.split()) > 6:
        raise LogError(f"Headline label is {len(label.split())} words; six at most")
    return fig, label


def headline(paras):
    """Fallback only. The big number and its label, from 'The number:'. The author's bold
    phrase is the source when there is one, else the first sentence. The first
    figure in it becomes the number; the words after it become the label."""
    first = paras[0]
    bold = re.search(r"\*\*(.+?)\*\*", first)
    phrase = bold.group(1) if bold else re.split(r"(?<=[.!?])\s", first)[0]
    phrase = plain(phrase).rstrip(".")
    m = FIGURE.search(phrase)
    if not m:
        raise LogError(f"no figure in the number field: cannot make a headline")
    fig = m.group()
    fig = str(WORDNUM[fig.lower()]) if fig.lower() in WORDNUM else fig
    label = (phrase[:m.start()] + phrase[m.end():]).strip(" ,:;")
    return fig, label


def first_sentence(paras):
    s = re.split(r"(?<=[.!?])\s", plain(paras[0]))[0].strip()
    return s[:1].upper() + s[1:]


def build_log(staged_names=()):
    try:
        days = parse_log(LOG_SRC.read_text())
    except LogError as e:
        sys.exit(f"\nBUILD LOG: {LOG_SRC.name}: {e}")
    latest = max(d["day"] for d in days)
    built = {d["day"] for d in days}
    if latest > TOTAL_DAYS:
        sys.exit(f"\nBUILD LOG: Day {latest} is past the {TOTAL_DAYS}-day plan")
    nav = "\n".join(
        f'    <li><a href="#day-{n}">{n:02d}</a></li>' if n in built else
        f'    <li><span aria-disabled="true" title="Not built yet">{n:02d}</span></li>'
        for n in range(1, TOTAL_DAYS + 1))
    segs = "".join(f'<i class="{"done" if n <= latest else ""}"></i>' for n in range(1, TOTAL_DAYS + 1))
    entries, cards, status = [], [], {}
    for d in sorted(days, key=lambda d: -d["day"]):
        f = d["fields"]
        try:
            if f.get("headline"):
                fig, label = stated_headline(f["headline"])
            else:
                fig, label = headline(f["number"])
                print(f"  WARNING: Day {d['day']} has no **Headline:** field; "
                      f"big number inferred from 'The number:'. State it.")
        except LogError as e:
            sys.exit(f"\nBUILD LOG: {LOG_SRC.name}: Day {d['day']}: {e}")
        img, alt = d["media"]
        title = inline(d['title'][:1].upper() + d['title'][1:])
        if d["day"] == latest:
            bare = plain(d["title"])
            status = {"day": latest, "total": TOTAL_DAYS,
                      "title": bare[:1].upper() + bare[1:],
                      "headline": fig, "label": label}
        failure = "".join(f"<p>{inline(p[:1].upper() + p[1:])}</p>" for p in f["failure"])
        links = ""
        if f.get("explore"):
            text = " ".join(f["explore"]).strip()
            items, rest = [], text
            for m in EXPLORE_LINK.finditer(text):
                if m.group(2) not in staged_names:
                    sys.exit(f"\nBUILD LOG: Day {d['day']}: Explorations points at "
                             f"{m.group(2)}, which this build does not publish")
                note = (m.group(3) or "").strip(" .")
                items.append(f'<li><a href="{m.group(2)}">{H.escape(m.group(1))}</a>'
                             + (f"<span>{H.escape(note)}</span>" if note else "") + "</li>")
                rest = rest.replace(m.group(0), "", 1)
            if not items or rest.strip():
                sys.exit(f"\nBUILD LOG: Day {d['day']}: Explorations takes only "
                         f"'[name](page.html) — note' entries; left over: {rest.strip()[:60]!r}")
            links = ('<div class="explore"><span class="k">Explorations</span>'
                     f'<ul>{"".join(items)}</ul></div>')
        watched = d["day"] == latest and d["watch"]
        figure = "" if watched else (
            f'\n    <figure class="media"><img src="assets/{img}" alt="{H.escape(alt)}" '
            f'loading="lazy"><figcaption>{H.escape(alt)}</figcaption></figure>')
        entries.append(f"""  <article class="day{' no-media' if watched else ''}" id="day-{d['day']}" data-day="{d['day']}">{figure}
    <div class="body">
      <div class="lede">
        <span class="num-label">Day {d['day']:02d} of {TOTAL_DAYS}</span>
        <h3>{title}</h3>
        <div class="big">{H.escape(fig)}</div>
        <p class="big-label">{H.escape(label)}</p>
        <p class="takeaway">{H.escape(first_sentence(f['angle']))}</p>
      </div>
      <div class="notes">
        <div class="failure"><span class="k">The honest failure</span>{failure}</div>{links}
      </div>
    </div>
  </article>""")
        cards.append(f"""    <a class="card" href="#day-{d['day']}" data-day="{d['day']}">
      <img src="assets/{img}" alt="" loading="lazy">
      <span class="card-t"><span class="num-label">Day {d['day']:02d}{' · latest' if d['day'] == latest else ''}</span>
      <b>{title}</b><span class="card-n">{H.escape(fig)}</span><small>{H.escape(label)}</small></span>
    </a>""")
    # the next two days, dashed, so progress reads at a glance
    upcoming = "".join(f"""    <div class="card future" aria-hidden="true">
      <span class="card-t"><span class="num-label">Day {n:02d} of {TOTAL_DAYS}</span></span><span class="ph">Not built yet</span></div>
""" for n in range(min(latest + 2, TOTAL_DAYS), latest, -1))
    # The recording at the top of the page is the latest day's, and falls back
    # to the first one made when a day has no Watch field of its own.
    top = next(d for d in days if d["day"] == latest)
    watch, hint = top["watch"] or ("interaction.mp4", "A screen recording of the clock view.")
    poster = top["media"][0]
    return (((ROOT / "log.template.html").read_text()
            .replace("<!--NAV-->", nav).replace("<!--SEGS-->", segs)
            .replace("<!--DAY-->", str(latest)).replace("<!--TOTAL-->", str(TOTAL_DAYS))
            .replace("<!--WATCH-->", H.escape(watch))
            .replace("<!--POSTER-->", H.escape(poster))
            .replace("<!--HINT-->", H.escape(hint))
            .replace("<!--HINT_JS-->", json.dumps(hint))
            .replace("<!--ENTRIES-->", "\n".join(entries))
            .replace("<!--CARDS-->", upcoming + "\n".join(cards))), status)

ROBOTS = """# This site is a personal record and is not intended for search indexing.
# Remove or relax this when the work is ready to be found.
User-agent: *
Disallow: /
"""

INDEX = """<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sixteen Days in Japan</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@600;800&family=Spectral:wght@300;400&display=swap">
<style>
:root{--paper:#E8DCC0;--paper-2:#DFD0AE;--ink:#3B2F23;--ink-2:#6B5B47;--ink-3:#92836C;--verm:#A83A2B}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);
  font-family:Spectral,Georgia,serif;font-size:15px;line-height:1.6}
.wrap{max-width:860px;margin:0 auto;padding:12vh 20px 10vh}
h1{font-family:"Shippori Mincho",serif;font-size:38px;font-weight:800;margin:0 0 6px;letter-spacing:.02em}
.sub{color:var(--ink-2);margin:0 0 6px}
.note{color:var(--ink-3);font-size:12.5px;max-width:62ch;margin:0 0 34px}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}
.card{display:block;text-decoration:none;color:inherit;background:var(--paper-2);
  border:1px solid var(--ink);padding:16px 18px 18px;box-shadow:4px 4px 0 rgba(59,47,35,.12);
  transition:transform .15s,box-shadow .15s}
.card:hover{transform:translate(-2px,-2px);box-shadow:6px 6px 0 rgba(59,47,35,.18)}
.card h2{font-family:"Shippori Mincho",serif;font-size:17px;font-weight:600;margin:0 0 6px}
.card p{margin:0;font-size:13px;color:var(--ink-2)}
.sz{display:block;margin-top:9px;font-size:11px;color:var(--ink-3)}
footer{margin-top:44px;padding-top:18px;border-top:1px solid var(--ink-3);
  font-size:11.5px;color:var(--ink-3)}
footer p{margin:0 0 6px;max-width:70ch}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
</style></head><body><div class="wrap">
<h1>Sixteen Days in Japan</h1>
<p class="sub">15&ndash;30 November 2025. Two travellers, thirteen prefectures.</p>
<p class="note">Four builds of the same trip, kept in order rather than replaced, so the
progression is visible. Each reads from a real expense book, real booking
confirmations and a real rail pass order.</p>
<div class="grid">
<!--CARDS-->
</div>
<footer>
<p><b>On the numbers.</b> Prices are as recorded. Where something was not recorded it
shows as pending rather than as an estimate.</p>
<p><b>On the times.</b> The clock view currently runs on invented times, clearly marked
throughout, until handwritten notes are transcribed.</p>
<p><b>On what is missing.</b> Shopping and gifts are excluded from every view except the
first, which is kept in its original form.</p>
</footer></div></body></html>"""

main()
