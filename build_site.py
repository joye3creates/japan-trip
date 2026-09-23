#!/usr/bin/env python3
"""Assemble site/ from the templates. Only what this script writes gets deployed.

Run order for a full rebuild:
    python3 extract.py && python3 build_dataset.py && python3 synth_times.py
    python3 build_site.py
"""
import json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA, SITE = ROOT / "data", ROOT / "site"

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
    SITE.mkdir(exist_ok=True)
    geo = (DATA / "japan_geo.json").read_text()
    built = []
    for tpl, ds, out, title, blurb in PAGES:
        html = (ROOT / tpl).read_text()
        html = html.replace("/*__TRIP_DATA__*/", (DATA / ds).read_text())
        html = html.replace("/*__GEO__*/", geo)
        (SITE / out).write_text(html)
        built.append((out, title, blurb, len(html) // 1024))
        print(f"  {out:<18} {len(html)//1024:>4} KB   from {tpl} + {ds}")

    # robots.txt is written by hand into site/ and must survive a rebuild
    (SITE / "robots.txt").write_text(ROBOTS)
    print(f"  {'robots.txt':<18} {len(ROBOTS)//1024:>4} KB")

    cards = "\n".join(
        f'      <a class="card" href="{o}"><h2>{t}</h2><p>{b}</p>'
        f'<span class="sz">{k} KB</span></a>' for o, t, b, k in built)
    (SITE / "index.html").write_text(INDEX.replace("<!--CARDS-->", cards))
    print(f"  {'index.html':<18} {len(INDEX)//1024:>4} KB")
    n = len(list(SITE.iterdir()))
    print(f"\nsite/ holds {n} files and nothing else. Only this directory deploys.")

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
