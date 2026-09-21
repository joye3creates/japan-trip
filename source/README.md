# Original inputs

Drop the two original files here to make the archive fully reproducible:

- `J_Cube_Trip.xlsx` — the expense workbook, 18 sheets, 16 of them day sheets
- `Japan_Stays.pdf` — the planning document, which turned out to be the itinerary

`extract.py` reads the workbook path from its `SRC` constant. Point it here:

```python
SRC = "source/J_Cube_Trip.xlsx"
```

These were deliberately not committed by the assistant that built this repo:
copying uploaded source files into version control was blocked by a provenance
check. Adding them is your call.
