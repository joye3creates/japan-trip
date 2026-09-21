# Original inputs

The two files the whole project derives from.

| File | What it is |
|---|---|
| `J_Cube_Trip.xlsx` | The expense workbook. 18 sheets, 16 of them day sheets, one per day from Day 0 to Day 15. Each has an itemised ledger in columns F–L and a summary block in B–C. |
| `Japan_Stays.pdf` | Named as a stays list, actually the full itinerary: region, rail pass, planned route and place names per day. It solved most of the within-day ordering problem. |

Both are committed, so the pipeline is reproducible with no setup:

```bash
pip install openpyxl
python3 extract.py
python3 build_dataset.py
```

## Two notes

**The PDF carries an "Oracle Restricted" classification banner** on every page,
applied automatically because the sheet was authored in a managed work account.
The content is a personal travel itinerary, but if your employer treats
banner-marked exports as controlled material, storing it here is worth a second
thought. The repo is private, which helps.

**This repo is private and holds sixteen days of personal financial data.**
Remove this folder before making it public.
