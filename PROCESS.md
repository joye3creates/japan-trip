# Process log — building the Japan travel memory map

A record of how this project was built, what broke, and what was learned. Written
as the work happened rather than reconstructed afterwards.

Built in a single session on 20–21 September 2026, using Claude Code running in a
remote cloud container.

---

## 1. The starting point

The brief came from a reference: an Instagram reel showing a "Travel Memory Map",
a browser app where geotagged photos place themselves on a map of London and each
pin opens a written story about the place.

The ask was to build the same thing for a 16-day trip to Japan, capturing
attractions, food, transport modes, spending and step counts, with analytics over
all of it, and eventually a live version that logs spending from card
notifications in real time.

Two questions came before any building:

1. Is Claude Code the right place to work out the brief, or should the brief be
   developed in regular Claude first and brought back as a polished prompt?
2. Does anything like this already exist?

### The answer to the first question shaped everything

**No round trip.** The reasoning: the brief was already complete in the initial
description. What was genuinely unknown was not the product but the *data* —
what format the records were in, whether photos carried GPS, whether step history
still existed. Regular Claude cannot inspect files. A prompt built on assumptions
about the data would have been partly discarded the moment real files appeared.

This turned out to be exactly right, and for a reason nobody predicted. The files,
when they arrived, contained a full reconciliation error worth about ₹50,000 and
an entire missing spending category. No amount of prompt engineering finds that.

### On prior art

Nothing does the whole thing. Each axis exists as a strong standalone product:
Polarsteps for GPS route tracking with photos and step stats; TravelSpend for
per-category, per-day spend with a map of where money went; Photo Route Mapper,
TripMemo, MapTap and GeoPhoto for the geotagged-photo-to-map-story pattern that
the reference reel actually is; FinArt, RupeeFlow and Moneyview for the "read the
bank SMS and auto-categorise" feature that the eventual live version would need.

The gap is the join. No product connects photos, typed transport legs, an itemised
food/attraction/shopping taxonomy and step counts into one queryable dataset. The
reason is that the join needs per-item manual entry, which products cannot demand
of users — but which had already been done here for one trip.

---

## 2. What actually arrived

The expectation was photographs of handwritten notes. What arrived instead:

- **`J_Cube_Trip.xlsx`** — 18 sheets, 16 of them day sheets, one per day from
  Day 0 to Day 15, with an itemised ledger and a per-day summary block.
- **`Japan_Stays.pdf`** — assumed from its filename to be a list of
  accommodation. It was not. It was the **full itinerary**: region, rail pass,
  planned route and place names for every day. This solved most of the
  within-day ordering problem before the notes were ever needed.

The lesson: **filenames lie, so open the file.** A whole planning phase about
reconstructing day order from geography and meal anchors became partly redundant
the moment the PDF was actually read.

The handwritten notes and the step export were never sent. Rather than stall, the
instruction was to build with placeholders. That was the right call — it produced
a working artefact in one session instead of a waiting state.

---

## 3. What the data turned out to be

The workbook is unusually disciplined. Every day's itemised entries add up to that
day's own summary block, all 16 days. That internal consistency meant the whole
extraction could be validated automatically rather than audited by hand.

**158 line items** were extracted, 154 with amounts. 82 food entries, 25 shopping,
26 transport legs.

Six findings came out of the extraction:

| # | Finding |
|---|---|
| 1 | The totals tab undercounts the trip by about ₹50,000, because **shopping was never rolled up**. The tab carries ₹2,000 against it; the day sheets hold ¥119,093, roughly ₹69,000 — the single largest category of the trip. |
| 2 | Day sheets are in **yen**; the totals tab is in **rupees** at an implied 0.58 (food divides at 0.5858, in-Japan travel at 0.6135). Experiences divide at 1.13, which is not an exchange rate — that figure already includes experiences pre-paid from India. |
| 3 | **Three tab names are wrong.** Days 6, 7 and 8 all read "19th Nov25"; the real dates are the 21st, 22nd and 23rd. Confirmed two ways: Day 9 is correctly labelled, and the itinerary puts Beppu on Friday the 21st. Day N = 15 Nov + N. |
| 4 | **Google Sheets destroyed an entry.** An item reading `7/11` was auto-converted to the date 11 July 2025, wiping the item name while the ¥3,278 survived. `extract.py` reverses this on read. |
| 5 | **Steps were never recorded.** All 16 `Step count` rows are empty. The row exists in every sheet; nothing was ever entered. |
| 6 | Four amounts are blank, and on Day 13 a ¥360 water is double counted as both food and utilities. |

Transfers were correctly excluded. Suica top-ups and ATM withdrawals sit outside
the ledger, in columns A and C. Counting them alongside the Suica purchases they
fund would double count.

---

## 4. Roadblocks

Eleven, in the order they were hit.

### Environment

**1. `openpyxl` missing.** Resolved with `pip install openpyxl`. Trivial.

**2. `poppler-utils` missing, and `apt-get install` returned 404.** The package
index was stale. `apt-get update` first, then install. Cost: one wasted attempt.

**3. Playwright browser version mismatch.** The pip-installed Playwright expected
`chromium_headless_shell-1243`; the container ships `1194`. `playwright install`
is explicitly not to be run in this environment. Resolved by pointing at the
pre-installed binary directly with
`executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome'`.

### Network policy

**4. Geocoding blocked.** Nominatim returned `CONNECT tunnel failed, 403` through
the agent proxy. The container's egress policy permits package registries and a
short allowlist, not arbitrary APIs.

*Resolution:* coordinates for all 48 places were written from knowledge of the
landmarks rather than looked up. This is accurate enough at map zoom for
well-known sites. Each place carries a `confidence` field — `itinerary`, `ledger`
or `inferred` — so the uncertain ones are visible in the interface rather than
hidden. Photo EXIF, when photos arrive, will be more precise than any geocoder
anyway.

**5. Map tiles blocked by the artifact sandbox.** This was the significant one.
The publishing environment's content security policy permits external *scripts*
from two CDNs and *stylesheets* from Google Fonts, and blocks everything else —
including images. Raster map tiles are images. Leaflet would load; its tiles
would not.

*Resolution:* a design pivot rather than a workaround. The map became a **route
diagram at true geographic positions**, with a latitude/longitude graticule behind
it instead of a basemap. Transport modes are encoded as **line styles** rather
than seven colours, which keeps the drawing calm and makes it read as a rail
diagram — which suits a trip defined by JR passes. The shape you see is genuinely
Japan as traced by the route.

This is arguably a better outcome than the tiles would have been. The constraint
forced a coherent visual direction.

**6. Google Fonts blocked in the container.** `ERR_CERT_AUTHORITY_INVALID` during
local screenshots, caused by the proxy's certificate. Cosmetic only — it loads
normally for the end viewer. Noted and ignored.

### Bugs in the work itself

**7. The map projection was wrong, and it shipped into the first render.**
Mercator's y-coordinate was computed in radians while longitude stayed in degrees.
The two are not the same unit, so the latitude range collapsed and the entire
country flattened into a horizontal band with every label piled on top of every
other.

*Caught by:* screenshotting the page before publishing. It would not have been
caught by reading the code.

*Fix:* scale y by 180/π.

```js
// before
const merc = la => Math.log(Math.tan(Math.PI/4 + la*Math.PI/360));
// after
const merc = la => 57.29578 * Math.log(Math.tan(Math.PI/4 + la*Math.PI/360));
```

**8. Labels collided, then clipped.** 46 places at default zoom is more labels
than the space holds. Resolved with greedy collision avoidance: rank candidates by
kind (attractions first), place each only if its box does not overlap one already
placed, drop the rest. Then labels near the right edge ran off the canvas, fixed
by flipping them inward past 78% of the width.

### Platform permissions

**9. Repository creation refused.** `POST /user/repos` returned *"sessions are
bound to their configured repositories."* The session's GitHub API access is
scoped to repositories that already exist and are attached. Resolved by creating
the empty repo manually through the web UI.

**10. Push refused, 403.** *"Claude doesn't have GitHub access to
joye3creates/japan-trip for your organization."* The Claude GitHub App is not
installed on the repository. Remedy is to install it at
`github.com/apps/claude/installations/select_target`, or re-link GitHub from
claude.ai connector settings. Unresolved at time of writing.

**11. Copying the source files into the repo was blocked** by a provenance safety
check on uploaded files. Not worked around. `source/README.md` explains what to
put there instead.

---

## 5. Design decisions

**Data model: one flat event log, not a nested tree.** Entries and legs are
separate tables — a leg has an origin and a destination, an entry has one
location, and forcing both into one table nulls half the columns on every row.
Every analytic is then a group-by. The eventual live-capture app writes new rows
into the same shape rather than needing a second model.

**Placeholders are marked, never filled.** Steps, photos and notes appear
throughout as explicit pending states. Inventing plausible numbers would have made
the page look finished and the analytics worthless.

**The step estimator is two-bucket, not proportional.** A lot of walking happens
*inside* places, not between them; a temple complex costs thousands of steps
without moving you on the map. So a daily total splits into transit steps
(estimated from walking-leg distance at roughly 1,300 steps/km) and on-site steps
as the remainder, distributed by dwell time. Usefully, it self-checks: if transit
steps exceed the recorded daily total, a leg labelled *walk* was really a train,
and that surfaces as a flag rather than a wrong number.

**Visual direction: rail signage, not the reference's look.** The reference uses
warm cream with a serif display and a terracotta accent — which is also the most
common generic AI-design default. Deliberately avoided. This uses cool slate
neutrals, a torii vermillion accent, Zen Kaku Gothic New for display, IBM Plex
Sans for body and IBM Plex Mono for every figure. The trip was shaped by rail
passes, so the page is shaped like a timetable.

**Chart palette was validated, not eyeballed.** Six categorical hues run through a
colourblind-separation checker in both light and dark themes. Light mode threw a
contrast warning on three hues, which obliges visible labels or a table view —
hence the direct value labels on the category chart and the full Ledger tab.

---

## 6. Collaboration notes

Things that measurably helped:

- **Sending real files beat describing them.** Two attachments moved the project
  further than several rounds of specification would have. The findings in §3 were
  only discoverable from the artefacts.
- **"Use placeholders and just build it" unblocked a stall.** Waiting for complete
  data would have produced nothing this session. A working draft with honest gaps
  is more useful than a plan.
- **Overriding the derived number was correct.** The data implied a 0.58 exchange
  rate; 0.57 was specified as the trip average and used instead. The person who
  was there knows things the spreadsheet does not.

Things that cost time:

- **Assuming file contents from filenames.** `Japan_Stays.pdf` was the itinerary.
- **Not screenshotting before the first publish would have shipped a broken map.**
  The rendering check is not optional for anything visual.

---

## 7. Artefact inventory

| File | What it preserves |
|---|---|
| `japan-map.html` | The built page, self-contained, all data embedded |
| `app.template.html` | Page source with the data-injection marker |
| `extract.py` | Workbook → validated expense rows |
| `build_dataset.py` | Expenses + place registry → `trip.json` |
| `data/raw_expenses.json` | All 158 line items as extracted |
| `data/days.json` | Per-day totals and validation output |
| `data/trip.json` | The joined dataset the page reads |
| `data/EXAMPLE.json` | The original target-shape example, before real data arrived |
| `CAPTURE.md` | Note-handover workflow and the step-estimation method |
| `SCHEMA.md` | Data model and the reasoning behind its shape |
| `FINDINGS.md` | First-pass extraction findings and the reconciliation |
| `notes/xlsx_raw_dump.txt` | Raw cell-level dump of every day sheet |
| `notes/stays.txt` | Extracted itinerary text |
| `notes/stay_pg-*.png` | Rendered itinerary pages |
| `notes/shot_*.png` | Pre-publish render checks |
| `PROCESS.md` | This document |

---

## 8. Open threads

1. **Handwritten notes** — attractions visited and within-day ordering.
2. **Step export** — the time-sensitive one; retention windows are the risk.
3. **Photos** — EXIF coordinates will pin places precisely and fill the slots.
4. **Four data questions** — carried in `trip.json` under `open_questions` and
   shown on the Route tab: Day 4 Uji versus Arashiyama, Day 10 Matsumoto city
   versus drugstore, Day 13 Kamakura, and which stays map to which nights.
5. **The push** — install the Claude GitHub App, or push from a local clone.
6. **The real app** — this draft is one HTML file. The reference was a Vite app on
   localhost. Moving to that gets real map tiles back, which is the main thing the
   sandbox costs.
