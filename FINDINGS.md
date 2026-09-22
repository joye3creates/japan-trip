# What came out of the two files

## The trip

**15 to 30 November 2025, 16 days (Day 0 to Day 15), two travellers: the two travellers.**

Route from the itinerary PDF:

| Days | Where |
|---|---|
| 0 | Delhi, fly out |
| 1 | Tokyo |
| 2 | Mt. Fuji / Kawaguchiko |
| 3 | Fuji to Kyoto |
| 4 | Kyoto and Uji |
| 5 | Hiroshima, Miyajima, on to Beppu |
| 6 | Beppu and Mt. Aso |
| 7 | Beppu to Osaka |
| 8 | Osaka, Himeji, Nara |
| 9–11 | Kanazawa, Shirakawa-go, Matsumoto |
| 12–14 | Tokyo |
| 15 | Fly home to Delhi |

## What was extracted

**158 line items**, of which 154 carry an amount. Every day's itemised total was
checked against that day's own summary block and they agree, which means the
spreadsheet is internally consistent and can be trusted.

| | count |
|---|---|
| Food entries | 82 |
| Shopping entries | 25 |
| Transport legs | 26 |
| Experiences, utilities, gifts | 25 |

## Five things worth knowing

### 1. Your totals tab undercounts the trip by about ₹50,000

The day sheets are in **yen**. The totals tab is in **rupees**, converted at roughly
0.58, which is visible in the data: food divides out at 0.5858 and in-Japan travel at
0.6135. That is a real rate with forex markup baked in, so it looks right.

Two categories do not fit that rate, for different reasons:

- **Shopping was never rolled up.** The totals tab has ₹2,000 against it. The day
  sheets contain ¥119,093, about ₹69,000. This is the single largest category of the
  whole trip and it is missing from your summary.
- **Experiences divides out at 1.13**, which is not an exchange rate. The totals figure
  must include experiences booked and paid from India before you left.

Reconciled, at 0.58:

| | ₹ |
|---|---|
| In-country spend, 16 day sheets | 166,254 |
| Flights | 80,000 |
| Accommodation | 100,000 |
| JR passes | 67,700 |
| Pre-booked train and bus | 29,017 |
| **Total, two people** | **442,971** |
| Per person | 221,485 |
| Per person per day | 13,843 |

Treat this as provisional until you confirm the rate you actually got.

### 2. Four tab names are wrong

Days 6, 7 and 8 are all labelled 19th Nov. The real dates are 21, 22 and 23 November.
Confirmed two ways: Day 9 is correctly labelled 24 Nov, and the itinerary PDF puts
Beppu on Friday 21st and Osaka on the 22nd and 23rd. Day N is simply 15 Nov plus N.

### 3. Google Sheets silently ate one of your entries

On Day 1 an item reading **7/11** was auto-converted into the date 11 July 2025, so the
item name was destroyed. The ¥3,278 amount survived. Recovered as a convenience store
purchase. Worth checking your other sheets for the same trap.

### 4. Steps were never actually recorded

Every one of the 16 sheets has a **Step count** row. All 16 are empty. Nothing was
ever entered. So step data has to come from your phone's health app export, and that
is now the one genuinely time-sensitive item, because retention windows are the risk.

### 5. Four amounts are missing

Fillable from your paper notes:

| Day | Date | Item |
|---|---|---|
| 1 | 16 Nov | suica card top up |
| 5 | 20 Nov | breakfast at Hiroshima station |
| 14 | 29 Nov | hotwheels |
| 13 | 28 Nov | ¥360 water is double counted, as both food and utilities |

## Note on transfers

Suica top-ups and ATM withdrawals sit in columns A and C, outside the ledger, so they
were correctly left out. They move money rather than spend it, and counting them
alongside the suica purchases they fund would double count. The one exception is Day
15, where a ¥500 suica recharge is logged in the ledger as a utility.
