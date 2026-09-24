# Building in public — context pack

**How to use this.** Upload this one file to a Claude Project on claude.ai and
leave it there. Start a new chat inside that project each day, paste the newest
entry, and draft the post there. When this file grows, replace it in the
project's knowledge rather than pasting it again.

Everything above the line is stable. Everything below it grows by one entry a
working day.

---

## The project, in one paragraph

An interactive record of a sixteen-day trip through Japan, November 2025, two
travellers. It started as a travel memory map like the ones people make from
geotagged photos, and turned into something stranger: a page where a map of
Japan dissolves and every purchase, meal, journey and night flies to its place
on a twenty-four hour clock, one lane per day. A switch turns the clock into a
price ledger, and the marks rearrange. It is built from a real expense workbook,
real booking confirmations and a real rail pass order.

## Why it might interest people

- It is a **travel record organised by time rather than by money**, which almost
  nothing is. Every expense app answers what a trip cost. This one is trying to
  answer what a day felt like.
- The build keeps **hitting honest-data problems** rather than technical ones,
  and solving them changes the design. That is the good material.
- It is being built **with an AI assistant in a working loop**, and the process
  is being logged in detail, which is a second story running alongside the first.

## The constraints that keep producing interesting decisions

- **Placeholders are marked, never filled.** A night with no recorded price shows
  no price, not an estimate. This rule has forced several design choices.
- **Absence must not read as idleness.** On a clock, an empty morning looks like
  nothing happened. Usually it means nothing was *bought*. That distinction is
  the hardest thing in the project.
- **Nothing personally identifying is published.** No names, no emails, no
  booking references. The two travellers are A and B.
- **Shopping and gifts are excluded** at build time, not hidden in the page.

## Tone notes for drafting

Specific beats clever. The numbers are the hook, not the adjectives. The
failures are more interesting than the successes and should not be smoothed
over. No hashtags-as-decoration, no "excited to share".

## What is safe to post

| Fine | Careful | Never |
|---|---|---|
| Design decisions and reasoning | Total trip cost, if framed as the point | Traveller names |
| Screenshots of the page | Hotel names, which are businesses | Email, phone, address |
| Roadblocks and mistakes | Daily spend figures | Booking or order references |
| Method, data shapes, code | | Links to the private artifacts |

**The published pages are private links.** They will not open for anyone else.
To show the work, post screenshots, or use the Share menu on an artifact to make
one public first, having checked what is on it.

---

# Entries

## Day 1 — a first draft in one evening

**Shipped:** an interactive map with day-by-day spending, published and working,
built from an expense workbook and an itinerary.

**The number:** two working blocks of ten and twenty-three minutes inside a
seven-hour window. Most of that window was waiting.

**Headline:** ~₹50,000 — shopping never totalled on the summary

**Media:** route_map.png — The route map: day rail, route and a detail panel

**The interesting thing:** the source files contained a **reconciliation error of
about ₹50,000**. An entire spending category, shopping, had never been totalled
on the summary tab. It was the largest category of the trip. Nobody had noticed
because the daily sheets were internally consistent and only the roll-up was
wrong.

**The honest failure:** a map projection bug shipped into the first render.
Latitude was computed in radians while longitude stayed in degrees, so the whole
country flattened into a horizontal band. It was caught by screenshotting the
page, not by reading the code.

**Angle worth taking:** sending real files beat describing them. A careful
workflow had been designed for handwritten paper notes; the actual records were a
spreadsheet, and most of that planning was wasted. The artefact contained a
finding no amount of specification would have surfaced.

## Day 2 — the constraint that turned out not to exist

**Shipped:** the repository went live and the whole pipeline became reproducible
from committed sources. A second visual treatment, an aged Japanese survey sheet,
on real prefecture coastlines.

**The number:** Japan's prefecture geometry simplified from **80,370 points to
6,830**, about a tenth, small enough to sit inside a single HTML file at 115 KB.

**Headline:** 6,830 — map points, down from 80,370

**Media:** woodblock_full.png — The same trip as an aged survey sheet, on real coastlines

**The interesting thing:** day one had concluded that real map geography was
unavailable, because geocoding services were blocked by the network policy, and
settled for an abstract diagram of points and lines. Day two re-tested and found
that `git clone` worked perfectly well even though geocoding did not. **Real
coastlines had been reachable the whole time.** The environment had not changed;
the picture of it had simply never been finished.

**The honest failure:** Japanese day labels printed on top of one another.
Inspecting the page structure said the layout was *correct*, a box of exactly the
right size holding exactly two characters. Only a screenshot at three times scale
showed both characters drawn at the same position. Vertical writing mode depends
on font metrics that a fallback face does not carry.

**Angle worth taking:** a constraint accepted once tends to stay accepted,
because nothing prompts a re-examination. Pushing on it is cheap.

## Day 3 — the axis changed

**Shipped:** the clock view. The page now lands on a twenty-four hour timeline,
one lane per day, with a switch to a price ledger.

**The number:** individual purchases run from ¥100 to ¥36,000. On a linear axis
**89% of marks land in the leftmost tenth of the width**; on a logarithmic axis,
5%. The log scale was not a preference, it was the difference between a chart and
an unreadable smear.

**Headline:** 89% — marks squeezed left on linear axis

**Media:** clock_hero.png — The clock view: sixteen days laid out hour by hour

**The interesting thing:** the whole project pivoted. Price is an accounting
question; time is the travel question, and almost no travel tool answers it. The
data argued against it at first, since only 15% of entries carried any time
signal, and a third of them have no moment *in principle*. A night in a hotel is
not a point in time.

That objection produced the best piece of design so far. Every mark is one of
three kinds: **both** a time and a price, an **event** with a time and no price,
or a **cost** with a price and no time. An event names the cost it belongs to. On
the clock the events show and the costs hide; on the ledger the events fly into
their cost and merge with it. One rule covers hotel arrivals, rail-pass journeys
and flights identically, and it reverses.

**The honest failure, and it is a good one:** five accommodation bookings were
reported as missing when they were sitting in the PDF all along. The pages
holding them were **images**, so text extraction returned nothing and that was
taken as proof of absence. The same file was re-sent twice before the question
came back as "aren't you able to see this within the PDF?" — and only then did
anyone check page by page.

Text extraction returning something is not evidence it returned everything.

**A second number worth using:** the rail passes cost ¥116,884 and covered
journeys that appeared nowhere in the daily book, because they cost nothing on
the day. Once shared across the rides they paid for, they turn out to be the
**single largest expense of the trip**, and they had been invisible.

**Angle worth taking:** the most useful thing said all day was six words from the
person who could see what the tool could not.

## Day 4 — a photograph does not know where it belongs

**Shipped:** photographs on the clock view. Hover any mark and a card comes up
with the picture, the place, the hour and the price; click to pin it and the bar
at the foot becomes a way to walk that day in order.

**The number:** the Mt Aso photograph was taken at 12:50. The nearest marks are
an ice cream at 11:52 and a lunch at 13:50 — **58 minutes one way, 60 the other**.
Matching a photograph to its nearest timestamp would have been a coin flip
between two wrong answers. So photographs attach to a place on a day, or to one
named mark, and never to a moment.

**Headline:** 58/60 — minutes to the two wrong marks

**Media:** day-04-photographs.png — A photograph on the mark it belongs to, and the bar that walks the day

**The interesting thing:** four of the day's five hours went on interaction,
not on pipeline. Five models were built as a throwaway study and three were
rejected in a single message, each with a reason — two because they hid the
photographs behind a click, one because hovering it made the row expand, which
moved the mark out from under the cursor, which unhovered it. All four studies are published below as they were made; three are dead ends.

**The honest failure:** everything worked and almost nothing was attached. Two
of six photographs reached the page, on 7 of 182 marks, and it took "I can't see
any image on these right now" to find out. Three separate faults, each of which
failed by showing nothing at all rather than by complaining. The build now
refuses an unknown place, and a place on a day that did not go there.

**Explorations:** [Five ways a photograph can live on the clock](explore/01-five-ways.html) — the first pass, at two-day density
[The card at real density](explore/02-hover-card-at-density.html) — the same idea against all 165 marks
[Stepping through a day](explore/03-stepping-card.html) — sizing the card, and what the arrows do
[Reaching a cluster](explore/04-reaching-a-cluster.html) — three ways to open a crowded line, still open

**Angle worth taking:** the questions that changed the most were three words
long. "Or any identifiers" rewrote the privacy gate from a list of known-bad
tags into a refusal of anything that is not pixel data — the phone had written
its model name into two private vendor tags, so any list would have lost.
