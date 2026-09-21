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

The decisions section carries the most weight. Split it into the user's decisions
and the assistant's, give each one its reasoning and the alternative that was
rejected, and focus on design and build decisions rather than admin. These logs
are raw material for a case study, so specificity beats tidiness.

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

The repo is private and holds sixteen days of personal financial data. `source/`
is for the original workbook and itinerary. Remove it before the repo is ever
made public.
