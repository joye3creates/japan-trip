# japan-trip

## What this is

An interactive record of a sixteen-day trip through Japan, 15–30 November 2025,
two travellers. Built from a real expense workbook, seven booking confirmations
and a rail pass order. Four views of the same data, kept in order rather than
replaced, so the progression stays visible.

The current build is the **clock view**: sixteen days laid out hour by hour, with
a switch to a price ledger. The model behind it is in `INTERACTION.md` and should
be read before changing how marks behave.

## Folders

```
*.template.html     page sources; the built files are generated, never edited
build_site.py       assembles site/ from templates + data
site/               THE ONLY DEPLOYED DIRECTORY
data/               generated datasets; not deployed
source/             original workbook and itinerary; never deployed, never public
notes/              raw dumps, render checks; working material
sessions/           one log per working day
docs/               archived copies of the living documents
assets/             screenshots and screen recordings for posting
names.local.txt     traveller names, gitignored, read at extraction time
```

## Pipeline

```bash
python3 extract.py          # workbook  -> data/raw_expenses.json, days.json
python3 build_dataset.py    # + places  -> data/trip.json and trip_full.json
python3 synth_times.py      # + times   -> marks; DELETE when real notes arrive
python3 build_site.py       # + templates -> site/
```

**Two datasets, deliberately.** `trip_full.json` keeps shopping and gifts and
feeds the route map alone, because that is the day-one artefact and a later
decision must not rewrite an earlier one. `trip.json` has them excluded and feeds
every page built since.

| Template | Dataset | Built as |
|---|---|---|
| `app.template.html` | `trip_full.json` | `site/route-map.html` |
| `ukiyo.template.html` | `trip.json` | `site/woodblock.html` |
| `scroll.template.html` | `trip.json` | `site/scroll.html` |
| `clock.template.html` | `trip.json` | `site/clock.html` |
| `log.template.html` | `BUILDING_IN_PUBLIC.md` (after `# Entries`) | `site/log.html` |

## Privacy

**Nothing personally identifying reaches the repository or a published page.**
Checked before every publish, not remembered afterwards.

Never committed, never rendered, never deployed:

- Names of either traveller or anyone else. They are **A** and **B** throughout.
- Emails, phone numbers, postal addresses
- Card numbers, payment identifiers, booking or confirmation references

The name mapping lives in `names.local.txt`, gitignored, applied by `extract.py`
at read time so the dataset is anonymous from its first write. If that file is
missing the names pass straight through, so its absence is a bug rather than a
silent success. Re-check the dataset after any extraction change.

A hotel's own address is a business address and is fine. The guest name on the
same confirmation is not. When a source document carries identifying material,
say so in the reply rather than dropping it silently.

**Shopping and gifts are excluded at build time**, not hidden in the page, for
every view except the route map.

**`privacy_gate.py` runs inside `build_site.py`** and scans every file bound for
`site/`, including embedded JSON and image metadata. One hit fails the build
before anything is written, reporting file and line but never the match. Names are
carried as salted hashes; run `python3 privacy_gate.py` to check `site/` by hand.
It reads images and video for metadata and embedded strings only. Text drawn
into a screenshot or a video frame is pixels it cannot see, so every binary it
lists needs a human look before it ships. Only assets a page links are copied.

Audit: `git grep -ilE '<names>' -- .` plus a scan for email, phone and
confirmation-number shapes across `site/`.

Commits before `ffd3a2d` carry a real name in their authorship. Removing that
needs a history rewrite, and must happen before this repo is ever public.

## Deploying

Netlify site **courageous-lolly-4dfc48**, linked to this repository, currently
set to Private. `main` publishes automatically; pull requests get a preview at
`deploy-preview-<n>--courageous-lolly-4dfc48.netlify.app`.

`site/robots.txt` disallows crawling. Relax it deliberately, not by accident.

Netlify publishes **`site/` and nothing else**, set in `netlify.toml`. Everything
private is outside that directory, so it is excluded by default rather than by
remembering to exclude it. Never move source material, datasets or notes into
`site/`, and never widen the publish directory.

Build command is `python3 build_site.py`.

## Daily routine

1. **Branch** off `main`, named for the day's work
2. **Write the entry**: a session log in `sessions/`, plus a matching short entry
   in `BUILDING_IN_PUBLIC.md`
3. **Open a PR**
4. **Wait for review.** The owner checks the Netlify deploy preview
5. **Merge** once approved

Do not push to `main` directly. A scheduled routine fires at 23:59 IST and should
follow the same path.

## Conventions that matter

**Placeholders are marked, never filled.** A night with no recorded price shows
no price, not an estimate from the nightly rate. Invented times are labelled in
three places on the page, including every tooltip. Inventing plausible figures
makes a page look finished and the analysis worthless.

**Absence must not read as idleness.** On a clock, an empty morning looks like
nothing happened when it usually means nothing was bought. This is why the notes
must record activities that cost nothing.

**Session logs** follow `sessions/README.md`: at a glance, timeline, what got
built, decisions split between the owner's and the assistant's with reasoning and
rejected alternatives, roadblocks with cost, prompts quoted verbatim, artefacts,
what remains open. Timings come from file timestamps and commit times, never
estimates. Do not reproduce a log in chat; send the file.

**Render before publishing.** Every visual bug this project has had was caught by
looking at the page, not by reading the code. A PDF that yields text is not
therefore fully read: check for pages with no text and non-zero images before
reporting anything as absent.

Chart palettes get validated, not eyeballed.

## Open

**The transcribed handwritten notes** are the one thing blocking a real version
rather than a demonstration. They bring times, activities that cost nothing, and
journey departures. `CAPTURE.md` says what they need to contain. When they
arrive, delete `synth_times.py` rather than editing it.

**Micro-interactions and story placement** on the clock view are wanted but not
yet specified. Ask rather than assume.

Also outstanding: which rides each pass actually covered, which fixes a per-ride
figure that is currently absurd for one of them; the pre-booked tickets that are
not yet shared out; a custom icon set the owner is drawing; and photographs and
step counts, pending since the first session.
