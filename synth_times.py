#!/usr/bin/env python3
"""Attach times to every entry so the clock view can be built before the notes exist.

DELETE THIS FILE once the transcribed notes arrive. Nothing here is evidence.
Every time it produces is flagged, and the page says so on its face.

It also derives the three kinds of mark the interaction needs:

  both   a time and a price      a meal, a ticket, a coffee
  event  a time, no price        arriving at lodging, a pass-covered ride, a flight
  cost   a price, no time        a night's lodging, the pass purchase, the flights

An event names the cost it belongs to. On the clock the events show and the
costs hide; on the ledger the events fly into their cost and merge with it.
That one rule covers lodging and rail passes and flights identically.
"""
import json, re, random
from pathlib import Path

D = Path(__file__).resolve().parent / "data"
RATE = 0.57
FLIGHTS_INR = 80000

# Text already in the workbook that names a time. These are inferred, not invented.
SIGNAL = [
    (r"breakfast|morning|brunch",            (7.5, 9.5)),
    (r"\blunch\b|noon",                      (12.0, 14.0)),
    (r"dinner|evening|night(?!life)",        (18.5, 21.0)),
    (r"nightlife",                           (21.0, 23.0)),
]
# Fallback windows by category when the text says nothing.
WINDOW = {
    "food":        (8.0, 21.5),
    "experiences": (9.5, 17.0),
    "travel":      (8.0, 19.0),
    "utilities":   (8.0, 21.0),
    "stays":       (16.0, 16.0),
}

def main():
    d = json.loads((D / "trip.json").read_text())
    rng = random.Random(20251115)          # fixed, so the page is stable between builds
    entries, costs, events = [], [], []

    # ---- 1. the ordinary entries: a time and a price
    for i, r in enumerate(d["entries"]):
        if not r.get("amount"):
            continue
        if r["category"] == "stays":
            continue                        # handled below, as cost + events
        txt = str(r.get("item") or "").lower()
        lo = hi = None
        src = "synthetic"
        for pat, win in SIGNAL:
            if re.search(pat, txt):
                lo, hi = win; src = "inferred from the item text"; break
        if lo is None:
            lo, hi = WINDOW.get(r["category"], (9.0, 20.0))
        t = round(lo + rng.random() * (hi - lo), 2)
        r = dict(r, id=f"e{i}", hour=t, time_source=src,
                 kind="event" if r.get("pass_allocated") else "both")
        if r["kind"] == "event":
            r["merge_to"] = "pass-" + r.get("pass_id", "ss")
            r["amount_display"] = None
        entries.append(r)

    # ---- 2. lodging: one cost per night, arrival events on the clock
    seen_property = set()
    for st in d.get("stays", []):
        if st["status"] != "stayed":
            continue
        start = int(st["check_in"][-2:]) - 15
        per = (st["jpy"] / st["nights"]) if st.get("jpy") else (
              (st["inr"] / st["nights"] / RATE) if st.get("inr") else None)
        for n in range(st["nights"]):
            day = start + n
            cid = f"stay-{day}"
            costs.append({"id": cid, "day_index": day, "category": "stays",
                          "item": st["name"], "amount": round(per) if per else None,
                          "kind": "cost", "lane": day,
                          "note": "one night" + ("" if per else ", price not recorded")})
            first = st["place"] not in seen_property
            seen_property.add(st["place"])
            times = [16.2, 21.7] if first and n == 0 else [21.7]
            for j, t in enumerate(times):
                events.append({"id": f"{cid}-a{j}", "day_index": day, "category": "stays",
                               "item": ("arrived at " if j == 0 and first else "back to ") + st["name"],
                               "hour": t, "kind": "event", "merge_to": cid,
                               "time_source": "synthetic", "place_id": st["place"]})

    # ---- 3. the trip-level band: passes and flights, with their events
    for p in d["trip"]["jr_passes"]:
        costs.append({"id": "pass-" + p["id"], "day_index": None, "category": "travel",
                      "item": p["name"], "amount": p["jpy"], "kind": "cost", "lane": "band",
                      "note": f"{p['days_valid']}-day pass for two, covering {p['covers']}"})
    fl = round(FLIGHTS_INR / RATE)
    costs.append({"id": "flights", "day_index": None, "category": "travel",
                  "item": "Return flights, Delhi and Tokyo", "amount": fl,
                  "kind": "cost", "lane": "band", "note": "round trip for two"})
    for day, hour, label in [(0, 22.5, "flew out of Delhi"), (15, 11.0, "flew home from Tokyo")]:
        events.append({"id": f"flight-{day}", "day_index": day, "category": "travel",
                       "item": label, "hour": hour, "kind": "event", "merge_to": "flights",
                       "mode_hint": "flight", "time_source": "synthetic"})

    marks = entries + events + costs
    d["marks"] = marks
    d["trip"]["times_are_synthetic"] = True
    syn = sum(1 for m in marks if m.get("time_source") == "synthetic")
    inf = sum(1 for m in marks if m.get("time_source", "").startswith("inferred"))
    (D / "trip.json").write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")))

    print(f"marks            : {len(marks)}")
    for k in ("both", "event", "cost"):
        print(f"  {k:<6}         : {sum(1 for m in marks if m['kind']==k)}")
    print(f"times inferred   : {inf}  (from words already in the workbook)")
    print(f"times invented   : {syn}")
    print(f"band items       : {sum(1 for m in marks if m.get('lane')=='band')}")
    print(f"merging events   : {sum(1 for m in marks if m.get('merge_to'))}")

main()
