# Gaps in the data, and what we did about each

A running record. Every time something turns out to be missing, it goes here:
what's missing, why, what we used instead, and how the page shows it.

**The rule:** never fill a gap with a guess that looks real. Either find a real
source, or mark the gap on the page so nobody mistakes it for data.

This is also the research for the product idea. Every workaround here is
something a person doing this for their own trip would hit too.

---

## Open

### Times for most of the trip

- **Missing:** when things happened. The spending sheet has what and how much,
  almost never when. Of 165 things that should have a time, 24 have one worked
  out from words already in the sheet (breakfast, dinner). The other 141 are
  invented so the clock could be designed at all.
- **Why:** the times were in handwritten notes, and some pages are lost.
- **For now:** invented times, labelled "invented" on every card that has one.
- **Next:** photo times (ExifTool), Google Timeline if it exists, and the times
  on train and attraction bookings. Each real time will say where it came from.

### Things that cost nothing

- **Missing:** walks, views, temples with no entry fee, hours on a train with a
  pass. None of it is in a spending sheet.
- **Why:** the sheet records purchases, not the day.
- **Problem it causes:** an empty morning on the clock looks like nothing
  happened, when it usually means nothing was bought.
- **Next:** photos fill most of these. The surviving handwritten pages are best
  used for the ones that mattered.

### Step counts

- **Missing:** how far you walked each day.
- **Next:** your phone's health or fitness app, if it was counting.

### Which rides each rail pass covered

- **Missing:** the two regional passes were paid before the trip, ¥116,884
  together, and every ride on them cost nothing on the day. So the passes were
  invisible in the daily spending, and nothing says which rides they paid for.
- **For now:** the cost is shared across the rides it most likely covered. For one
  pass that gives a per-ride figure that is plainly wrong.
- **Next:** the train bookings should settle it.

### Pre-booked tickets and pre-trip costs

- **Missing:** tickets booked before the trip, a SIM, anything bought before
  leaving.
- **Next:** you're sending these. They go in the "Before leaving" row at the top
  of the clock.

### Photos to show

- **Missing:** the photos themselves. Every point shows a picture now, but 167 of
  182 are stand-ins, one per kind of thing, labelled "placeholder" on the picture.
- **Next:** the ~200 you pick.

### Two photos with no place

- **Missing:** where the koi pond photo was taken, and which day Osaka Castle was.
- **Why:** both files had lost all their hidden details, and neither has a
  landmark that pins it down. Osaka Castle is obvious, but it isn't on the
  itinerary for any day.
- **Next:** the photo spreadsheet, if the originals kept their details.

---

## Worked around

### Hotel bookings reported missing

- **What happened:** five hotel bookings were reported as not being in the PDF.
  They were there all along, on pages that were pictures rather than text, so
  reading the text returned nothing.
- **Found by:** being asked "aren't you able to see this within the PDF?", then
  checking every page.
- **Lesson:** reading a document's text is not proof it has no more in it.

### A photo belongs to a place, not a minute

- **What happened:** the Mt Aso photo was taken at 12:50. The nearest points are
  an ice cream at 11:52 and lunch at 13:50. Matching by nearest time would have
  put a photo of a volcano on an ice cream.
- **Worked around:** photos attach to a place on a day, or to one named point.

### Photos that knew nothing about themselves

- **What happened:** of the first six photos, five came with no time, place or
  device details at all, stripped somewhere along the way. One still had them.
- **Worked around:** the one that knew placed itself. The others were placed by
  hand, or left unplaced rather than guessed.

### Google Timeline moved

- **What happened:** Google moved Timeline off its servers and onto the phone in
  2024–25. It's no longer in Google Takeout.
- **Worked around:** export it from the phone. If the phone was changed without
  Timeline backup on, it may be gone.
- **Found out:** before trying Takeout, which saves a wasted hour.

### The photos live in Google Photos, not on a drive

- **What happened:** the plan assumed photos on a hard drive, read with ExifTool.
  They're in Google Photos.
- **Worked around:** Google Takeout exports an album with a small `.json` file
  next to every photo. It carries the time and place Google shows, even for
  photos whose own files lost them. The trimming page reads only those files and
  never opens the photos, so ExifTool isn't needed.
- **Watch for:** those files also carry the names of people Google recognised,
  links into the account and any captions. The page keeps none of that.

### Location files include home

- **What happened:** the photo spreadsheet and the Timeline file both carry
  locations. The Timeline file holds every place you've been, including home,
  and the photo list could include home on the first and last days.
- **Worked around:** `tools/trim-before-sending.html` cuts both down on your
  laptop to 14 Nov – 1 Dec 2025 and to places inside Japan, before anything is
  sent.

---

## Left out on purpose

These aren't gaps. They're choices.

- **Shopping and gifts.** Personal, and no use to anyone reading this as a record
  of travelling in Japan. Excluded everywhere except the first map.
- **One night with no recorded price** shows no price, not an estimate from the
  nightly rate.
