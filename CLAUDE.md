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
| `log.template.html` | `BUILDING_IN_PUBLIC.md` (after `# Entries`) | `site/index.html`, the front page, and `site/log.html` |
| `INDEX` in `build_site.py` | the four pages above | `site/builds.html` |

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

The log page takes each day's still from `assets/day-NN.png`, or from the file an
entry names with `**Media:**`. A new day is an entry plus an image, never code.

**Photographs go through `scrub_photos.py`, never straight into `assets/`.**
Originals live in `pics/`, which is gitignored, because they carry capture
times, a device fingerprint and often GPS. The script reads those into
`data/photo_meta.json`, matches each photo to a day, and writes a copy with
every APP segment removed. The gate then refuses **any** image carrying
metadata at all, rather than a list of known-bad tags: the phone that took
these wrote its model name into two private vendor tags, so an allowlist loses
by definition. `python3 privacy_gate.py --selftest` checks that protection is
still in place. The scrubber needs Pillow; nothing in the build does, so
Netlify installs nothing.

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
3. **Push the branch. Do not open a pull request.**
4. **Send the owner the built file** with `SendUserFile`, so it is reviewed
   locally rather than on a deploy preview
5. **Open the PR only when asked**, then merge once approved

Do not push to `main` directly.

**Netlify builds cost credits, and a pull request is what spends them.** Every
push to an *open* PR rebuilds its preview, so the old habit of opening a PR and
then pushing fixes to it spent one build per commit. A branch with no PR
normally builds nothing. Previews are worth it for a final look before merging;
they are not worth it for iteration. Send the file instead.

**A scheduled routine fires at 23:59 IST into the main build session** and writes
both files, then opens the PR. There is no separate logging session: one was
tried and retired, because it duplicated the routine and produced a second PR
against the same file. If a session is asked to write the day's entry, check the
routine has not already done it.

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
