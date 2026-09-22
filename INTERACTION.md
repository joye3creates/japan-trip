# The interaction model

Settled across conversation, recorded here so it stops living in chat. Not yet
built. The scroll skeleton in `japan-scroll.html` implements an earlier version
of this and will be brought in line once the notes are transcribed.

---

## Two views, one set of marks

Every purchase, journey, meal and free activity is a single element that exists
from the first frame of the page to the last. It is never destroyed and
recreated. That is what makes the transitions read as transformation rather than
as a crossfade, and it is borrowed directly from the Pudding's EU regions piece.

| View | Horizontal axis | Default |
|---|---|---|
| **Clock** | 24 hours, in two-hour bands, one lane per day | yes |
| **Ledger** | price, logarithmic, one lane per day | toggle |

The vertical axis never changes: one lane per day, sixteen lanes.

## The grammar of the toggle

A mark does one of exactly two things when the view changes. Naming this keeps
the two behaviours below from feeling like unrelated special cases.

- **It moves.** Same mark, new horizontal position. Most things do this.
- **It merges into a parent.** Several marks converge on one and become it.

**Merging must be reversible.** A merged mark is stacked at its parent's
position, not deleted, so toggling back splits it out again. If that does not
reverse cleanly the whole toggle feels broken.

## Lodging

**One icon every time you arrive at the lodging.** No check-out concept.

- First day at a property: two icons, the initial check-in and the nightly return
- Every following night at the same property: one icon, the nightly return
- New property: the two-icon pattern begins again

On the ledger view, a day's lodging icons merge into that day's single night cost.
Day one's two icons become one; a later night's single icon simply moves.

This survives multi-night stays, which a check-in and check-out model does not.
Four of the seven bookings run two or three nights, and those middle nights would
otherwise show no lodging at all.

## The trip-level band

A separate band above the sixteen day lanes, on the same price axis, in the
overflow zone past the last gridline. It holds exactly two things.

- **The flights**, a round trip for two
- **The rail passes**, two of them

Nothing else goes there. Everything else pre-booked, including train and bus
tickets bought before departure, sits on the day it was used. The band is for
costs that genuinely cannot be attributed to one day, not a place to put anything
awkward.

## Rail-pass journeys

Sixteen train and bullet-train journeys were covered by the passes. They cost
nothing on the day, so on the ledger view they have no price and nowhere to sit.

**On toggling to the ledger, they travel up to the pass mark in the band and
merge into it.** Not a fade, and not a holding area off to one side. The
journeys visibly become the purchase that paid for them, which is the same
gesture as the lodging merge and should feel like the same idea.

Hovering the pass mark then reveals what it absorbed.

The flights behave identically: they appear on the clock at their departure
times on day 0 and day 15, then collapse into the flight mark on the ledger.

## Icons carry category, colour does not

Identity is shape: bowl, bag, train, torii, house. The palette stays the muted
woodblock set with one vermillion accent. This avoids a seven-hue categorical
scale, suits the aged-paper treatment, and matches how the original sketch was
drawn.

Transport branches further by mode, so a bus and a bullet train are
distinguishable at a glance.

## Rules that keep the chart honest

- **Placeholders are marked, never filled.** A night whose price is unknown
  carries no price rather than an estimate from the nightly rate.
- **Absence must not read as idleness.** This is why activities that cost nothing
  have to be in the notes. Without them the clock view shows empty mornings that
  were not empty.
- **A dinner running past midnight stays on its own day's lane**, sitting past
  the 24:00 mark. The lane is the journal day, not the clock day.
- **Shopping and gifts are excluded at build time**, not hidden in the page, and
  the exclusion is stated where the totals are.

## Still open

1. Which pass covers which dates, and how the ₹67,700 splits between the two.
2. Whether the scroll sequence lands on the clock or the ledger, with the toggle
   as a control afterwards. Landing on the clock is the stronger story.
3. Whether the day-0 flight and day-15 return flight appear on the clock at all,
   or whether those two lanes stay near-empty.
