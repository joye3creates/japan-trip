# Japan trip — how to hand over your paper notes

## The short version

**Do not transcribe anything by hand.** Photograph the pages and upload them.
Transcription is the slowest possible use of your time and I can read handwriting
from photos. Your job is the verification pass at the end, not the typing.

---

## Part 1 — The workflow

### Step 1: photograph the pages

- One photo per page. Do not fit two pages in one frame.
- Flat page, daylight or bright indoor light, phone directly above (not at an angle).
- Do not crop tight. Margins often have scribbles that turn out to matter.
- If a page has a date written on it, make sure the date is in frame.
- If a day spans two pages, shoot both and upload them next to each other.

### Step 2: upload in batches of 3 to 5 days

Not all 15 days at once. Reasons:

- A bad transcription convention caught on day 3 is cheap to fix. Caught on day 15 it is not.
- After each batch I produce a table of that batch's days for you to eyeball.
- You confirm or correct, and we move on.

### Step 3: verify the money column only

This is the one thing you must actually check, line by line, against the page.

Everything else has a sanity check available. Place names can be geocoded and a wrong
one lands in the sea. A misread transport mode contradicts the travel time. But a `7`
read as a `1` in a cost is silently plausible, and it poisons every number in the
analytics. So: costs get eyeballed by you, once, per batch.

### Step 4: photos and Google Timeline

Separate from the notes, and they can come later:

- Export Google Timeline for the trip dates if you still have it.
- The trip photos themselves. I need their timestamps and GPS, not the images at full size.
  A script can pull just the metadata into a small file so you are not uploading gigabytes.

---

## Part 2 — What your notes probably do not have

Four things that are cheap to recall now and painful to reconstruct later. Write them
in a message or on a fresh page and photograph it:

1. **Trip dates.** Exact start and end date. Everything joins on date.

2. **Currency, and whether you wrote yen or rupees.** If costs are in yen I need the
   rate you actually got, not today's rate. Bank statement or the exchange counter
   receipt is ideal. One rate for the whole trip is fine.

3. **Per person or combined.** When a note says a meal cost 2,400, was that the table
   or your half? This single ambiguity breaks every per-person analytic and cannot be
   recovered from the page later. If it varies, tell me the default and I will flag
   the exceptions as I go.

4. **Where you slept each night.** Hotel or area, per night. This anchors the start
   and end of each day's route and is usually the missing piece that makes ordering work.

---

## Part 2b — What the time axis needs

This supersedes the older guidance below, which assumed a spend-only chart. The
default view is now a 24-hour clock per day, in two-hour bands, with a toggle to
the price axis. That changes what the notes have to carry.

### Per entry, in order of value

| Field | Why |
|---|---|
| **Time, even rough** | "late morning", "around 3", "after dinner" all work. This is the axis. |
| **Free or paid** | A free temple is a mark on the clock with no price. Without these the chart invents idle mornings. |
| **What it was** | Chooses the icon. Meal, temple, shop, train, lodging. |
| **Cost, if any** | Already have most of this from the workbook. |
| **Duration, if it was long** | A three-hour museum reads differently from a ten-minute shrine. Only worth noting when it was substantial. |

**The single most valuable thing you can add is the things that cost nothing.**
The workbook has 155 priced entries and no free ones. On a price axis that is
complete; on a clock it is a trip where you apparently did nothing between meals.

### Per transport leg

- Departure time, and arrival time if you noted it
- Mode: walk, bus, train, shinkansen, ferry, cycle
- Whether a rail pass covered it

A train at 09:00 followed by an afternoon of marks in a new city is the clearest
single thing a time axis can show. Worth being precise here even if you are rough
elsewhere.

### Per day, for lodging

Two marks a day: **when you left the lodging** and **when you got back**. Not
check-in and check-out, which only happen at the ends of a multi-night stay and
would leave the middle nights of your Kyoto, Beppu, Osaka and Kanazawa stays with
no lodging marks at all.

On the price toggle those two converge into the one night's cost, which is what
the data already holds.

### A rule for after midnight

If a dinner ran to 00:30, it stays on that day's lane, sitting past the 24:00
mark, rather than jumping to the next day. The lane is the journal day, not the
clock day. Note it as "day 8, 00:30" and it will land correctly.

## Part 3 — Two things I will infer, and how

You flagged both of these yourself. Here is the actual method, so you can judge whether
you trust it.

### Ordering within a day

Your notes are per day, not timestamped. Order comes from, in priority order:

1. **Google Timeline**, if you have it. This is ground truth with real timestamps and
   it settles the question completely.
2. **Meal anchors.** Lunch and dinner split the day into segments and are usually
   obvious from the note.
3. **Geography.** Given the hotel as start and end, and the places visited, there is
   usually one route that is not absurd. Tokyo sprawls, so a sequence that crosses the
   city three times is almost certainly wrong.
4. **Opening hours.** A temple that shuts at 17:00 cannot be the evening stop.

Every entry carries `seq_confidence` set to `known` or `inferred`. Inferred ordering is
marked in the app rather than presented as fact. You can correct any of it later.

### Steps per leg

You have a daily total. Splitting it across the day is a two-bucket model, not a
flat proportional split, because a lot of walking happens *inside* places rather than
between them. A temple complex or a department store can be a couple of thousand steps
without moving you on the map at all.

    daily_total = transit_steps + onsite_steps

    transit_steps = sum over walking legs of (distance_km × STEPS_PER_KM)
                    STEPS_PER_KM starts at 1300 and gets tuned to you

    onsite_steps  = daily_total − transit_steps
                    distributed across that day's places by dwell time,
                    or evenly if no times are known

**This estimator checks itself.** If `transit_steps` comes out larger than your recorded
daily total, the walking classification is wrong, and something labelled a walk was
actually a train or a bus. That contradiction surfaces as a flag rather than a wrong
number, which is why it is worth doing this way.

Tuning `STEPS_PER_KM`: if any day was mostly walking between known points, that day
gives a personal calibration figure better than the 1300 default.
