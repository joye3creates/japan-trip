# Session logs

One document per working session, written at the end of it. These are the raw
material for a case study later — keep them specific rather than tidy.

Naming: `YYYY-MM-DD-session-NN.md`

Each one covers, in this order:

1. **At a glance** — date, active working time, what shipped
2. **Timeline** — wall-clock, reconstructed from file timestamps and commits
3. **What got built** — the concrete output
4. **Decisions** — split into *yours* and *the assistant's*, each with the
   reasoning and the alternative that was rejected. This is the section a case
   study actually needs, so it gets the most detail.
5. **Roadblocks** — what broke, why, how it resolved, what it cost
6. **Prompts and briefs** — the session's actual instructions, quoted as written,
   each paired with what it produced and what it left open. Quote verbatim,
   including the typos and the thinking-aloud; a cleaned-up paraphrase destroys
   exactly what makes this useful. This section feeds a separate write-up about
   how to brief these tools, so err towards keeping too much.
7. **Artefacts** — files produced or changed, so attachments can be reassembled
8. **Open at end of session**

After writing the log, add a matching entry to `BUILDING_IN_PUBLIC.md` in the
repo root. That file is a different job: short, written for someone drafting a
social post rather than for an engineer, and it goes to a Claude Project on
claude.ai. One entry a working day, in the established shape — shipped, the
number, the interesting thing, the honest failure, the angle worth taking.
Add a `**Headline:** <figure> — <label, six words max>` line: it is the big
number on the public log page, and the build warns when it is missing.
Each day's still is `assets/day-NN.png` (Day 4 is `day-04.png`). To use another
file in `assets/`, add `**Media:** <file> — <caption>`. A missing still fails the
build with the filename it wanted. Adding a day never needs a code change. Keep
it under about 300 words. Never put anything in it that the safe-to-post table
at the top of that file rules out.

`PROCESS.md` in the repo root is the running cumulative account. These session
files are the per-day detail underneath it.
