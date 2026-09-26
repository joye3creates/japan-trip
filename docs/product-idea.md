# The trip clock as a product

An idea written down, not built. The Japan piece is what's being made in these
sixteen days. This is what it could become, what it wouldn't try to do, and why.

## In one line

Drop in what your phone already knows about your trip, add what it doesn't, and
see the whole trip laid out hour by hour. Nothing leaves your device unless you
choose to publish it.

## Who it's for

People who come back from a trip with a camera roll, a pile of booking emails
and a rough idea of what they spent, and no good way to answer "how was it?" or
"what did it cost?"

## The main idea: don't build a capture app

The obvious version of this product is an app you carry on the trip that records
everything. That's the wrong starting point.

**Your phone already records where you were and when.** Every photo carries its
time and place. Booking emails carry the times of trains, flights and tickets.
None of that needs a new app.

**What nothing records well is money and meaning.** What something cost, and why
it mattered. Those are the only two things worth asking someone to do during a
trip, and both should take seconds:

- log a spend: amount, and a tap for what kind
- add a note: a line of text or a voice memo, when something was worth
  remembering

Everything else gets pulled in afterwards. That turns the hardest part of the
product, capture, into the smallest.

## What it would pull in

| From | Gives |
|---|---|
| Photo metadata | when and where, for most of the trip |
| Booking emails and PDFs | times of trains, flights, tickets and check-ins |
| The spending log, or a bank export | what things cost |
| Notes | what mattered, and what cost nothing |

Google Timeline is deliberately **not** on that list as a requirement. Google
moved it off the web and onto the phone in 2024–25, it only exists if it was
switched on, and many people have it off. Useful when it's there; not something
to build on.

## What it would make

- The clock: every day as a row, every moment placed at its hour, switchable to
  what it cost
- A photo on every point, stepping through a day
- A visual language made from your own trip: photograph the snack packets,
  tickets and manhole covers you liked the look of, and get a palette, motifs and
  suggested fonts to choose from. The tool suggests; you decide
- A page you can keep private, share with a link, or publish

## Privacy as a feature

Everything runs on your device. Photos are stripped of their hidden location and
device details before anything is published. You choose what to show per photo
and per day. "Nothing leaves your device unless you publish it" is a reason to
pick this over apps that upload everything by default.

The Japan piece already works this way: it builds on a laptop, checks every file
for names, emails and booking numbers, and only then publishes.

## Links out

For each hotel, ticket and pass: where it was booked, a link to the place's own
page (never your booking, which carries your name and reference), and any trick
it needed — like waking up at a set time to get tickets. For anyone who wants to
ask more, a contact form rather than an email address on the page.

## What's out there already

| | Does | Doesn't |
|---|---|---|
| Polarsteps | Tracks your route automatically, makes a travel book | Money, or the hour-by-hour shape of a day |
| TripIt | Builds an itinerary from forwarded booking emails | Photos, spending, anything after the trip |
| Google Photos, Apple Photos | Make "memories" from your photos | Money, bookings, or a view you can read at a glance |

None of them put time, money and photos on one view.

## The hard parts

- **Phones have no hover.** The Japan piece is built around hovering a point.
  A product has to work by tapping first
- **Time zones.** Photos store local time, often without saying which zone.
  Crossing zones mid-trip needs care
- **People forget to log spending.** The whole product leans on one habit.
  A bank export as a fallback matters
- **Several travellers, several phones.** Two people's photos of the same day
  need merging
- **People in photos.** Fine for your own trip by your own choice. A product for
  others needs a rule about who appears
- **Photo weight.** Hundreds of photos have to load quickly on a phone
- **Fonts.** Anything suggested has to be licensed for the web

## What doing it by hand taught us

Getting the Japan data in by hand is the research for this product. Every gap
and every workaround is in [`../GAPS.md`](../GAPS.md). The short version so far:

- the most useful record of the trip turned out to be the photos, not the notes
- a large cost, ¥116,884 of rail passes, was invisible in the daily spending
- a photo belongs to a place, not to the nearest minute

## Status

Idea only. Not being built in these sixteen days.
