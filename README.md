# Japan, Sixteen Days

An interactive route map and spending analysis of a 16-day trip through Japan,
15–30 November 2025, built from a logged expense workbook.

Open `japan-map.html` in any browser. It is self-contained: all 158 expense lines
and every coordinate are embedded in the file. The only external reference is a
Google Fonts stylesheet, which falls back to system fonts if unavailable. No build
step, no server, no network required.

## What's here

| Path | What it is |
|---|---|
| `japan-map.html` | The built page. This is the deliverable. |
| `app.template.html` | The page source, with a `/*__TRIP_DATA__*/` marker where data is injected. |
| `extract.py` | Reads the expense workbook, emits `data/raw_expenses.json` and `data/days.json`. |
| `build_dataset.py` | Joins expenses with the place registry, emits `data/trip.json`. |
| `data/trip.json` | The joined dataset the page consumes. |
| `CAPTURE.md` | How to hand over the handwritten notes, and the step-estimation method. |
| `SCHEMA.md` | The data model and why it is shaped this way. |
| `FINDINGS.md` | What the first extraction turned up, including the reconciliation. |
| `notes/` | Provenance: raw spreadsheet dump and the itinerary PDF text. |

## Rebuilding

```bash
pip install openpyxl
python3 extract.py          # workbook  -> raw_expenses.json + days.json
python3 build_dataset.py    # + places  -> trip.json
python3 -c "import pathlib; t=pathlib.Path('app.template.html').read_text(); \
  d=pathlib.Path('data/trip.json').read_text(); \
  pathlib.Path('japan-map.html').write_text(t.replace('/*__TRIP_DATA__*/', d))"
```

`extract.py` has the workbook path in the `SRC` constant at the top. Point it at
your own copy; the source file is deliberately not committed.

## Current state

Three things are placeholders, marked as pending in the interface rather than
filled with invented values:

- **Steps.** All 16 `Step count` rows in the workbook are empty. Needs a health
  app export. `CAPTURE.md` describes the two-bucket estimator that splits a daily
  total into transit steps and on-site steps.
- **Photos.** Each place and day card reserves a slot. Geotagged photos will pin
  themselves via EXIF coordinates.
- **Handwritten notes.** Attractions visited and within-day ordering come from
  paper notes not yet transcribed.

## Known data issues

Carried in `trip.json` under `open_questions` and shown on the Route tab:

1. **Day 4** — the itinerary planned Arashiyama and the Sagano railway, but every
   expense names Uji. The receipts were trusted over the plan.
2. **Day 10** — `matsumoto trip tix` ¥8,140 is either Matsumoto the city or
   Matsumoto Kiyoshi the drugstore. The itinerary says Shirakawa-go.
3. **Day 13** — a `kanazawa` travel line and a buddha temple entry on a Tokyo day,
   most likely Kamakura reached via Kanazawa-hakkei.
4. **Stays** — the PDF lists Airbnb shortlists, not final bookings, so nights are
   not yet mapped to addresses.

Also worth knowing: the workbook tab names for days 6, 7 and 8 all read
"19th Nov25" and are wrong; the real dates are the 21st, 22nd and 23rd. Day N is
15 Nov + N. And Google Sheets silently converted an item reading `7/11` into a
July date on day 1, destroying the item name while the ¥3,278 survived;
`extract.py` reverses that conversion.

## Reconciliation note

The day sheets are in yen. The totals tab is in rupees at roughly 0.58 implied.
Shopping was never rolled up into the totals tab, which undercounts the trip by
about ₹50,000 — it is the single largest category. At the 0.57 rate used here,
in-country spend is ¥286,644 (₹163,387), and the whole trip including pre-paid
flights, stays and rail passes comes to about ₹440,104 for two people.
