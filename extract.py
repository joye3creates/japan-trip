#!/usr/bin/env python3
"""Parse J_Cube_Trip_.xlsx day sheets into a structured trip dataset."""
import openpyxl, json, re, datetime, sys
from pathlib import Path

SRC = "/root/.claude/uploads/b3850738-abc6-5216-a1c1-a24a34cc94c0/e4fd231f-J_Cube_Trip_.xlsx"
OUT = Path("/home/user/japan-trip/data")
TRIP_START = datetime.date(2025, 11, 15)

# Ledger is grouped into category blocks; each block starts at a fixed row in col G.
BLOCKS = [(2,"utilities"),(16,"experiences"),(29,"food"),(44,"travel"),
          (61,"shopping"),(79,"gifts"),(94,"misc"),(110,None)]

# Summary-block labels -> canonical category
SUMMAP = {"utilities":"utilities","experiences":"experiences","entertainment":"experiences",
          "food + coffee + water":"food","outside food":"food","travel":"travel",
          "shopping":"shopping","gift":"gifts","gifts":"gifts","misc":"misc"}

def clean(v):
    """Item cells: Google Sheets silently turned '7/11' into a date. Undo that."""
    if v is None: return None
    if isinstance(v, datetime.datetime):
        return f"{v.month}/{v.day}"
    return str(v).strip()

def day_index(sheet_name):
    m = re.match(r"Day\s*(\d+)", sheet_name)
    return int(m.group(1)) if m else None

def parse_summary(ws):
    """Find the per-day summary table in cols B/C and return {category: total}."""
    out = {}
    for row in range(18, 45):
        if str(ws.cell(row, 2).value).strip().lower() == "category":
            for r in range(row+1, row+18):
                label = ws.cell(r, 2).value
                if label is None: continue
                key = str(label).strip().lower()
                if key in ("total", "wo shopping/gifts", "remaining",
                           "wo investment & trip", "step count"): continue
                if key in SUMMAP:
                    val = ws.cell(r, 3).value
                    out[SUMMAP[key]] = float(val) if isinstance(val,(int,float)) else 0.0
            break
    return out

def parse_day(ws, idx):
    date = TRIP_START + datetime.timedelta(days=idx)
    rows = []
    for (start, cat), (nxt, _) in zip(BLOCKS[:-1], BLOCKS[1:]):
        for r in range(start, nxt):
            item = clean(ws.cell(r, 8).value)          # H
            amt  = ws.cell(r, 9).value                 # I
            mode = clean(ws.cell(r, 10).value)         # J
            payer= clean(ws.cell(r, 11).value)         # K
            note = clean(ws.cell(r, 12).value)         # L
            if item is None and amt is None: continue
            if item is not None and str(item).strip().lower() == cat: continue
            rows.append({
                "date": date.isoformat(), "day_index": idx, "category": cat,
                "item": item, "amount": float(amt) if isinstance(amt,(int,float)) else None,
                "payment_mode": mode, "paid_by": payer, "note": note,
                "row": r,
            })
    return date, rows, parse_summary(ws)

def main():
    wb = openpyxl.load_workbook(SRC, data_only=True)
    all_rows, days, problems = [], [], []

    for name in wb.sheetnames:
        idx = day_index(name)
        if idx is None: continue
        ws = wb[name]
        date, rows, summary = parse_day(ws, idx)

        # currency: in-Japan days are JPY; travel days at each end are mixed
        currency = "JPY"
        if idx == 0: currency = "INR"
        for row in rows:
            row["currency"] = currency
            if idx == 15 and row["item"] and re.search(r"delhi|uber|home", row["item"], re.I):
                row["currency"] = "INR"
                row["_flag"] = "currency inferred INR (back in India)"
            if row["amount"] is None:
                problems.append(f"{name} row {row['row']}: '{row['item']}' has no amount")

        # validate itemised totals against the sheet's own summary block
        tot = {}
        for row in rows:
            if row["amount"]: tot[row["category"]] = tot.get(row["category"],0)+row["amount"]
        for cat, expected in summary.items():
            got = tot.get(cat, 0.0)
            if abs(got - expected) > 0.5:
                problems.append(f"{name}: {cat} itemised={got:.0f} but summary={expected:.0f} (diff {got-expected:+.0f})")

        days.append({"date": date.isoformat(), "day_index": idx, "sheet": name,
                     "currency": currency, "summary": summary,
                     "itemised": tot, "steps_total": None})
        all_rows.extend(rows)

    days.sort(key=lambda d: d["day_index"])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/"raw_expenses.json").write_text(json.dumps(all_rows, indent=2, ensure_ascii=False))
    (OUT/"days.json").write_text(json.dumps(days, indent=2, ensure_ascii=False))

    print(f"days parsed      : {len(days)}")
    print(f"expense rows     : {len(all_rows)}")
    print(f"rows with amount : {sum(1 for r in all_rows if r['amount'])}")
    jpy = sum(r["amount"] for r in all_rows if r["amount"] and r["currency"]=="JPY")
    inr = sum(r["amount"] for r in all_rows if r["amount"] and r["currency"]=="INR")
    print(f"total JPY        : {jpy:,.0f}")
    print(f"total INR        : {inr:,.0f}")
    print(f"\nby category (JPY):")
    bycat={}
    for r in all_rows:
        if r["amount"] and r["currency"]=="JPY":
            bycat[r["category"]]=bycat.get(r["category"],0)+r["amount"]
    for k,v in sorted(bycat.items(), key=lambda x:-x[1]):
        print(f"  {k:12s} {v:10,.0f}")
    print(f"\nVALIDATION ({len(problems)} issues):")
    for p in problems: print("  !", p)

main()
