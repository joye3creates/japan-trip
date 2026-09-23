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
        staged[out] = html
        built.append((out, title, blurb, len(html) // 1024))
        print(f"  {out:<18} {len(html)//1024:>4} KB   from {tpl} + {ds}")

    # robots.txt is written by hand into site/ and must survive a rebuild
    staged["robots.txt"] = ROBOTS
    print(f"  {'robots.txt':<18} {len(ROBOTS)//1024:>4} KB")

    cards = "\n".join(
        f'      <a class="card" href="{o}"><h2>{t}</h2><p>{b}</p>'
        f'<span class="sz">{k} KB</span></a>' for o, t, b, k in built)
    staged["index.html"] = INDEX.replace("<!--CARDS-->", cards)
    print(f"  {'index.html':<18} {len(INDEX)//1024:>4} KB")

    staged["log.html"] = build_log()
    print(f"  {'log.html':<18} {len(staged['log.html'])//1024:>4} KB   from log.template.html + BUILDING_IN_PUBLIC.md")

    # Only the media a page actually links. Anything else in assets/ would get
    # a public URL without having been reviewed for this context.
    refs = sorted({r for v in staged.values() if isinstance(v, str)
                   for r in re.findall(r'(?:src|href)="(assets/[^"#?]+)"', v)})
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
          ("headline", "Headline")]
REQUIRED = ("shipped", "number", "interesting", "failure", "angle")

# One still per day. The two screen recordings run 21s and 25s, too long to
# loop as decoration, so the log uses stills and the videos stay for posting.
MEDIA = {1: ("route_map.png", "The route map: day rail, route and a detail panel"),
         2: ("woodblock_full.png", "The same trip as an aged survey sheet, on real coastlines"),
         3: ("clock_hero.png", "The clock view: sixteen days laid out hour by hour")}

WORDNUM = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve".split())}
FIGURE = re.compile(r"[¥₹$€£]?\d[\d,]*(?:\.\d+)?%?|\b(?:" + "|".join(WORDNUM) + r")\b", re.I)


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
        if d["day"] not in MEDIA:
            raise LogError(f"Day {d['day']} has no image in MEDIA")
    seen = [d["day"] for d in days]
    if sorted(seen) != list(range(1, len(seen) + 1)):
        raise LogError(f"days are not a clean run from 1: {seen}")
    return days


def inline(s):
    """The little markdown these entries use: bold, italic, code."""
    s = H.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
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


def build_log():
    try:
        days = parse_log(LOG_SRC.read_text())
    except LogError as e:
        sys.exit(f"\nBUILD LOG: {LOG_SRC.name}: {e}")
    latest = max(d["day"] for d in days)
    nav = "\n".join(f'    <li><a href="#day-{d["day"]}">{d["day"]:02d}</a></li>'
                    for d in sorted(days, key=lambda d: d["day"]))
    entries = []
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
        img, alt = MEDIA[d["day"]]
        failure = "".join(f"<p>{inline(p[:1].upper() + p[1:])}</p>" for p in f["failure"])
        entries.append(f"""  <article class="day" id="day-{d['day']}">
    <figure class="media"><img src="assets/{img}" alt="{H.escape(alt)}" loading="lazy"><figcaption>{H.escape(alt)}</figcaption></figure>
    <div>
      <span class="num-label">Day {d['day']:02d}</span>
      <h3>{inline(d['title'][:1].upper() + d['title'][1:])}</h3>
      <div class="big">{H.escape(fig)}</div>
      <p class="big-label">{H.escape(label)}</p>
      <p class="takeaway">{H.escape(first_sentence(f['angle']))}</p>
      <div class="failure"><span class="k">The honest failure</span>{failure}</div>
    </div>
  </article>""")
    return ((ROOT / "log.template.html").read_text()
            .replace("<!--NAV-->", nav).replace("<!--DAY-->", str(latest))
            .replace("<!--ENTRIES-->", "\n".join(entries)))

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
