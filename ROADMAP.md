# Roadmap to day 16

Written on building day 6 of 16. A checklist, not a contract: tick things off,
cross things out, move them. **(you)** marks the things only you can do. The rest
I can start as soon as what it depends on arrives.

## Where we are

Days 1–5 are built and logged. The clock view works: the map dissolves into
sixteen days by the hour, it switches to what things cost, every point has a
photo card, crowded points open under the cursor, and the build log is live.

The two biggest weaknesses: **the times are invented**, and **the photos are
placeholders**.

## What we're making (proposed, not agreed)

**One line:** drop in your trip's photos and spending, and see the trip laid out
hour by hour. Nothing leaves your laptop unless you choose to publish it.

**Done on day 16 could mean:**

1. The Japan piece, finished: real times, final look, one data story
2. One working slice of the product: someone drops in their own photo list and a
   spending sheet and sees their own trip on the clock, in their browser, with
   nothing uploaded
3. Mocks of the rest: logging during a trip, the souvenir style tool, privacy
   controls
4. Tested with at least three people, findings written down
5. The case study

Everything past that goes in the parking lot at the bottom.

---

## 1. Data in

- [ ] **(you)** Photo times and places: run ExifTool over the trip folders, send the spreadsheet
- [ ] **(you)** Google Timeline: export from the phone, then cut to 15–30 Nov before sending
- [ ] **(you)** Step counts from your phone's health or fitness app, if it was counting
- [ ] **(you)** Train and attraction bookings, the same way as the hotel PDFs
- [ ] **(you)** Pre-trip spending: SIM, passes, anything bought before leaving
- [ ] **(you)** Photos of the surviving handwritten pages
- [ ] **(you)** Pick ~200 photos to show
- [ ] Importer for the photo spreadsheet
- [ ] Importer for the Timeline file
- [ ] Replace invented times with real ones, and mark which source each time came from
- [ ] Coverage map: which days and places have no photos yet, to guide the 200

## 2. Gaps

- [ ] List what's still missing after everything is in
- [ ] Decide how the page shows a gap, so an empty morning never reads as "nothing happened"
- [ ] Use the surviving pages for what the data can't give: what mattered, what cost nothing

## 3. Patterns and the story

- [ ] Look for two or three findings worth telling. Candidates:
  - what you photographed versus what you paid for
  - steps against spending: did walking days cost less
  - the rail pass: the biggest cost of the trip, invisible day to day
  - when in the day money went, and when photos were taken
- [ ] Pick one or two
- [ ] Design the scroll piece: dragging along a bar changes what the chart shows
- [ ] Build it

## 4. Visual identity

- [ ] **(you)** Photograph what you brought back or noticed: snack packets, souvenirs, tickets, manhole covers, signs, packaging
- [ ] Pull colours, textures and motifs out of them
- [ ] Three distinct directions: palette, type, icons, texture
- [ ] **(you)** Pick one
- [ ] Restyle the clock page
- [ ] Redraw the icons in the chosen language (the manhole covers could be the place icons)
- [ ] Fonts: check every one is licensed for the web, and for a product if this becomes one
- [ ] Carry it into the log page, the portfolio card and the case study

## 5. Interaction and animation

- [ ] Refine the map-to-clock move and the camera
- [ ] Refine the micro-interactions: card, spread, stepping bar
- [ ] **Design for phones.** There is no hover on a phone, and most people will open a shared link on one
- [ ] Reduced-motion version

## 6. Product: the working slice

- [ ] A page where you drop in a photo spreadsheet and a spending sheet and get your own clock
- [ ] Runs in the browser; nothing is uploaded
- [ ] Works on a trip that isn't Japan

## 7. Product: concept and mocks

- [ ] Write the one-line product properly **(you)**
- [ ] Look at what exists: Polarsteps, TripIt, Google Photos and Apple Photos memories. Be ready to say how this is different
- [ ] Logging during a trip: spending and a note, nothing more (the phone already records where and when)
- [ ] The souvenir style tool: upload what you liked the look of, get a palette, motifs and suggested fonts, then choose
- [ ] Privacy controls: what to show, what to hide, per photo and per day
- [ ] Links out: where each hotel and ticket was booked, the place's own page, and any trick it needed

## 8. Testing

- [ ] **(you)** Ask three people who travelled recently. They need their own photo data for the second round, so ask early
- [ ] Round 1: watch three people use the Japan piece. Can they read the clock? Do they find the hover?
- [ ] Fix what they trip on
- [ ] Round 2: three people try the working slice with their own trip
- [ ] Write the findings down

## 9. Hosting and privacy

- [ ] Decide what's public and what stays private. The Netlify site is Private right now
- [ ] Before the repo is ever public: early commits carry a real name and need a history rewrite
- [ ] Photo weight: 200 photos need to load quickly on a phone
- [ ] People in photos: fine for this trip by your decision; a product for others needs a rule

## 10. Daily log

- [ ] Keep the daily entry and session log going
- [ ] Record every annoyance in getting the data in. That is the research for the product

## 11. Case study

- [ ] Outline the story now, so each day's log feeds it
- [ ] Write it
- [ ] Carry the visual language into it

---

## Suggested order

| Day | Focus |
|---|---|
| 6 | **(you)** exports, souvenir photos, ask testers. Me: importers, this roadmap |
| 7 | Data in: real times replace invented, gap list |
| 8 | Test round 1 on the Japan piece |
| 9 | Visual identity: three directions |
| 10 | Apply the chosen one: page, icons, fonts |
| 11 | Interaction and animation, including phones |
| 12 | Patterns and the scroll story |
| 13 | The working slice: drop in your own trip |
| 14 | Product mocks: logging, style tool, privacy |
| 15 | Test round 2 with testers' own trips |
| 16 | Case study |

## Risks

- **Too much for eleven days.** Build the Japan piece and one working slice properly; design the rest as mocks.
- **Everything waits on the data.** Exports first.
- **Phones.** The interaction is built on hover.
- **Google Timeline is fragile.** Google already pulled it off the web; it only exists if it was switched on. Photo data is what every phone has, so it should be the backbone.
- **Testing needs other people's data.** Ask early.

## Parking lot: after day 16

- A real mobile app for logging during a trip
- Accounts, login, sync
- The style tool as a finished, automatic tool
- Affiliate links for bookings
- Trips with more than one traveller's photos
