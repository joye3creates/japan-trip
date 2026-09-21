# Data model

One flat event log, not a nested tree. Every analytic you described is then a
group-by over one table, and the future live-capture app writes new rows into the
same shape instead of needing a second model.

Five files in `data/`.

---

## `trip.json`

Trip-level facts. Travellers, dates, currency, exchange rate, step calibration.

## `places.json`

The canonical place registry. Everything else refers to a place by `id`, so a place
is named and geocoded exactly once.

| field | notes |
|---|---|
| `id` | slug, e.g. `senso-ji` |
| `name` | as you wrote it |
| `name_ja` | Japanese name where known; materially improves geocoding accuracy |
| `lat`, `lng` | filled by geocoding, then spot-checked |
| `city` | Tokyo, Kyoto, Osaka … |
| `category` | `attraction` · `food` · `shopping` · `accommodation` · `transit_hub` · `other` |

## `days.json`

One row per day. Date, base city, where you slept, the recorded step total, raw note text.

## `entries.json`

The event log. Things you did that were not movement.

| field | notes |
|---|---|
| `date`, `seq` | `seq` orders the day |
| `seq_confidence` | `known` or `inferred` |
| `place_id` | |
| `kind` | `attraction` · `food` · `shopping` · `other` |
| `title`, `detail` | `detail` holds your raw note text verbatim |
| `cost` | `{ amount, currency, paid_for }` where `paid_for` is `both` · `self` · `mom` |
| `items[]` | dishes for a meal, purchases for a shop |
| `time_start`, `time_end` | only if Timeline supplies them |
| `photo_ids[]` | |

`items[]` is what answers "how many food items across the whole trip". Worth being
slightly obsessive about while transcribing, because it cannot be recovered later.

## `legs.json`

Movement between places. This is what draws the routes.

| field | notes |
|---|---|
| `date`, `seq` | |
| `from_place_id`, `to_place_id` | |
| `mode` | `walk` · `subway` · `train` · `shinkansen` · `bus` · `taxi` · `ferry` · `bike` · `flight` |
| `line_name` | e.g. Yamanote Line. Optional but makes the map far more evocative |
| `cost` | same shape as entries |
| `duration_min` | |
| `distance_km` | computed |
| `steps_estimated` | computed, walking legs only |
| `source` | `notes` · `timeline` · `inferred` — drives how confidently the app draws it |

---

## Why separate `entries` and `legs`

A leg has an origin and a destination; an entry has one location. Forcing both into one
table means half the columns are null on every row and every query needs a filter.
Two tables, one union view when something needs both.

## What the analytics become

- Spend by category, by day, by city → group `entries` and `legs` by `kind` / `mode`.
- Total food items → flatten `items[]` where `kind` is `food`.
- Steps per day and per leg → `days.steps_total` and the computed `legs.steps_estimated`.
- Transport mix → group `legs` by `mode`, summing `duration_min` and `distance_km`.
- Cost per attraction, cost per km, cost per day → joins across the two.
