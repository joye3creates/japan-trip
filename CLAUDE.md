# Working conventions for this project

## Session logs

At the end of each working day, write `sessions/YYYY-MM-DD-session-NN.md` in the
format described in `sessions/README.md`.

**Do not reproduce the log in chat.** Send it as a file and write at most two
lines summarising what the day covered. The user reads it as a document, not as
a wall of terminal text.

A scheduled routine fires this at 23:59 IST daily. If no work happened that day,
write no log and say so in one line.

Timings must be reconstructed from real file timestamps and commit times. Never
estimate or invent them. Report active working time and elapsed time separately;
the gap between them is meaningful.

Quote the session's instructions verbatim in the prompts section, typos and all.
They are raw material for a write-up about how to brief these tools, and a tidied
paraphrase throws away the thing being studied. `STYLE_BRIEF.md` and the doc
"Briefing Design to AI" are the current state of that thinking.

The decisions section carries the most weight. Split it into the user's decisions
and the assistant's, give each one its reasoning and the alternative that was
rejected, and focus on design and build decisions rather than admin. These logs
are raw material for a case study, so specificity beats tidiness.

## Building in public

`BUILDING_IN_PUBLIC.md` is the context pack for drafting social posts elsewhere.
It gets one short entry per working day, added at the same time as the session
log, in the shape already established there. It is written for a reader drafting
a post, not for an engineer: the number and the honest failure carry it.

Its safe-to-post table governs what may appear in it. The published artifact
links are private and must never be posted as if they were shareable.

## Data integrity

Placeholders are marked, never filled. Steps, photos and untranscribed notes
appear as explicit pending states throughout the interface. Inventing plausible
figures would make the page look finished and the analytics worthless.

Every derived number traces to a source. The page footer states where figures
come from. When a figure is inferred rather than recorded, say so in the
interface, not just in a comment.

Place records carry a `confidence` field: `itinerary`, `ledger` or `inferred`.
Surface it rather than hiding it.

## Building

`extract.py` then `build_dataset.py` then inject into `app.template.html`. The
rebuild command is in `README.md`. `japan-map.html` is generated — edit the
template, never the built file.

Render the page and look at it before publishing anything visual. The one bug
that shipped into a first draft was a projection error that code review would not
have caught.

Chart palettes get validated, not eyeballed.

## Privacy

**Nothing personally identifying leaves this repository or reaches any published
page.** This is a standing rule, not a per-task instruction, and it is checked
before every publish rather than remembered afterwards.

Never committed, never rendered, never sent anywhere:

- Names of either traveller, or of anyone else
- Email addresses, phone numbers, postal addresses
- Card numbers, payment identifiers, booking reference or confirmation numbers
- Order numbers, loyalty identifiers, anything that indexes back to an account

The two travellers are **A** and **B** throughout. The mapping from names to
labels lives in `names.local.txt`, which is gitignored, and `extract.py` applies
it at read time so the dataset is anonymous from the first write. If that file
is absent the names simply pass through, so its absence is a bug, not a silent
success. Check the dataset after any extraction change.

Trip expenses, property names, dates, durations and prices are fine. A hotel's
own address is a business address and is fine. The guest name on the same
confirmation is not.

When a source document carries identifying material, say so in the reply rather
than silently dropping it, so the person knows what was in the file they sent.

To audit: `git grep -ilE '<names>' -- .` plus a scan for email, phone and
confirmation-number shapes. Note that **commits before ffd3a2d carry a real name
and address in their authorship**, which rewriting history would be needed to
remove.

`source/` holds the original workbook and itinerary and must be removed before
the repo is ever made public. The repo is private and holds sixteen days of
personal financial data.
