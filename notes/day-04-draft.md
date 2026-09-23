# Day 4 — unused draft, kept for tonight's log run

Written by a separate session that was set up to turn session logs into
public entries, before we found that the 23:59 routine already does that
job. That session is retired and its PR (#3) was closed unmerged.

It is kept because the writing is good and because it only saw half of
the day: it covers the build-log page and the privacy gate, and knows
nothing about the stills, the fonts falling back to Georgia, or the
MEDIA convention. Tonight's entry should cover all of it. Take the
phrasing, not the framing, and reconsider which failure leads.

---

## Day 4 — the privacy rule became code

**Shipped:** a public build-log page, generated from this file, and a privacy
gate that every file bound for the site must pass before anything is written.

**The number:** the first version copied eight media files into the site. The
page linked three. **Five files, 4.6 MB, including two screen recordings, would
have had URLs** that nobody had reviewed for strangers to see. Now only what a
page links is copied, and three stills, 1.2 MB, remain.

**Headline:** 5 — unlinked files committed into the site

**The interesting thing:** the site gets its first page meant for strangers, so
"nothing identifying is published" stopped being a checklist and became a build
step. One hit fails the build, and it reports file and line but never the match,
so the build log cannot leak what it caught. The names it looks for are stored
as salted hashes rather than plain text, and the file says plainly what that is
worth: a list of first names reverses them. Obscurity, not secrecy.

**The honest failure:** all three problems in the first version were caught in
review, not by the build. The big number on each day was inferred from the text,
and for Day 1 it came out as "2 working blocks", burying a ₹50,000 reconciliation
error. The media was copied wholesale. And the gate printed "files clean" when it
reads images only for metadata. **Text drawn into a screenshot is pixels, and it
cannot see them.** It now says so on every run and lists each image for a human
look.

**Angle worth taking:** a check that reports "clean" is claiming more than it
checked. The fix was not a smarter gate but an honest one, that names its own
blind spot every time it runs.

