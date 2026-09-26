# Roadmap to day 16

Written on building day 6 of 16, and narrowed the same day. A checklist, not a
contract: tick things off, cross things out, move them. **(you)** marks what only
you can do.

## The aim

**A finished data visualisation piece about the trip**: real times, a look of its
own, and a data story worth reading. Good enough to pitch to The Pudding.

The product is **written down, not built**: what it would be, what it wouldn't
do, and why, so people can see the thinking. That lives in
[`docs/product-idea.md`](docs/product-idea.md).

## Done on day 16

1. **Must:** the Japan piece, finished: real times, final look, one data story
2. **Must:** one round of feedback from people, and the changes it asked for
3. **Must:** a record of every gap in the data and how it was found or worked
   around, in [`GAPS.md`](GAPS.md). Started today
4. **Must:** the product idea written down. Drafted today
5. **On the day:** a reusable prompt for turning trip objects into a visual
   language, written from how the exercise actually went
6. **Try:** the case study
7. **Maybe:** a pitch to The Pudding

---

## 1. Data in

- [ ] **(you)** Photo times and places: run ExifTool over the trip folders
- [ ] **(you)** Google Timeline: export it from the phone
- [ ] **(you)** Run both through `tools/trim-before-sending.html` before sending. It keeps only 14 Nov – 1 Dec 2025 and only Japan
- [ ] **(you)** Step counts from your phone's health or fitness app, if it was counting
- [ ] **(you)** Train and attraction bookings, the same way as the hotel PDFs
- [ ] **(you)** Pre-trip spending: SIM, anything bought before leaving
- [ ] **(you)** Photos of the surviving handwritten pages
- [ ] **(you)** Pick ~200 photos to show
- [x] A way to cut location files down on your laptop before they're sent
- [ ] Importer for the photo spreadsheet
- [ ] Importer for the Timeline file
- [ ] Replace invented times with real ones, and mark which source each time came from
- [ ] Coverage map: which days and places have no photos yet, to guide the 200

## 2. Gaps

- [x] Start the gaps record
- [ ] Add every new gap as the data comes in, with what was used instead
- [ ] Decide how the page shows a gap, so an empty morning never reads as "nothing happened"
- [ ] Use the surviving pages for what the data can't give: what mattered, what cost nothing

## 3. Patterns and the story

- [ ] Find two or three findings. Candidates:
  - what you photographed versus what you paid for
  - steps against spending: did walking days cost less
  - the rail passes: ¥116,884 paid before the trip, invisible in the daily spending. Did they pay off?
  - when in the day money went, and when photos were taken
- [ ] For a Pudding pitch, frame it as a question strangers care about, not only "our trip". "Did the rail passes pay off?" and "Where does the money actually go, hour by hour?" are both questions people planning Japan ask
- [ ] Pick one or two
- [ ] Design the scroll piece: dragging along a bar changes what the chart shows
- [ ] Build it

## 4. Visual identity

- [ ] **(you)** Photograph what you brought back or noticed: snack packets, souvenirs, tickets, manhole covers, signs, packaging
- [ ] Pull colours, textures and motifs out of them
- [ ] Three distinct directions: palette, type, icons, texture
- [ ] **(you)** Pick one
- [ ] **On the day: note how we worked** — what you sent, what worked, what didn't, what you'd skip next time. End with a prompt you can run again on your next trip
- [ ] Restyle the clock page
- [ ] Redraw the icons in the chosen language
- [ ] Fonts: check each one is licensed for the web
- [ ] Carry it into the log page, the portfolio card and the case study

## 5. Interaction and animation

- [ ] Refine the map-to-clock move and the camera
- [ ] Refine the micro-interactions: card, spread, stepping bar
- [ ] **Phones.** There is no hover on a phone, and most people will open a shared link on one
- [ ] Reduced-motion version

## 6. Feedback round

One round, once the piece is in a good place. Showing it to people, not asking
them for their data.

- [ ] **(you)** Pick three to five people
- [ ] Decide what to watch for: do they understand the clock, find the hover, follow the story, like the look
- [ ] Run it
- [ ] Write down what they said and what we changed because of it

## 7. The product, written down

- [x] Draft [`docs/product-idea.md`](docs/product-idea.md)
- [ ] **(you)** Read it and change what's wrong
- [ ] Add what the gaps record teaches about the product as it grows

## 8. Hosting and privacy

- [ ] Decide what's public before the feedback round. The Netlify site is Private right now
- [ ] Before the repo is ever public: early commits carry a real name and need a history rewrite
- [ ] Photo weight: 200 photos need to load quickly on a phone

## 9. Daily log

- [ ] Keep the daily entry and session log going

## 10. Case study (try)

- [ ] Outline the story, so each day's log feeds it
- [ ] Write it

---

## Suggested order

| Day | Focus |
|---|---|
| 6 | Plan. Product idea and gaps record drafted. Trimming page built. **(you)** exports |
| 7 | Data in: real times replace invented, new gaps recorded |
| 8 | Visual identity: three directions from your objects, and the reusable prompt |
| 9 | Apply the chosen look: page, icons, fonts |
| 10 | Patterns: find the story |
| 11 | Build the scroll piece |
| 12 | Feedback round |
| 13 | Changes from feedback, interaction and animation, phones |
| 14 | More of 13: this is where feedback usually lands |
| 15 | Polish. Pudding pitch if it's ready |
| 16 | Case study, if there's time |

If the object photos aren't ready by day 8, swap days 8–9 with 10–11.

## Parking lot: after day 16

- Building the product for real: logging during a trip, importing, accounts
- The style tool as a finished, automatic tool
- Links out to booking sites, and affiliate links
- Trips with more than one traveller's photos
