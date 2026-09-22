# What Moved the Needle

> **Snapshot.** The living version is a Claude doc at
> https://claude.ai/code/artifact/61ebb4fc-280d-4643-8d2b-952318c78284
> Split out of *Briefing Design to AI* on 22 September 2026, because it is about
> working with these tools rather than about design.

Moments from building an interactive map of a sixteen-day trip through Japan
where a choice visibly changed the outcome.

## Sending files beat describing them

The project opened with a careful workflow designed for handwritten paper notes,
built on the assumption that the records were on paper. Two attachments later
that assumption was wrong, and most of the workflow was unnecessary.

More importantly, those two files contained a reconciliation error of roughly
fifty thousand rupees and an entire spending category that had never been
totalled. **No amount of prompt refinement surfaces that.** Only the artefact
does.

The general principle: when the question is about *your* material, stop
describing it and hand it over. Describing it can only ever transmit what you
already noticed.

## "Use placeholders and just build it" unblocked a stall

Three inputs were missing: photographs, step counts, and transcribed notes. The
choice was to wait for them or to ship with honest gaps. Shipping with gaps
produced a working artefact in one session. Waiting would have produced a plan.

The corollary matters as much as the decision. Gaps must be **marked, not
filled**. Inventing plausible numbers would have made the page look finished and
the analysis worthless. A visible *pending* is information; a fabricated value is
damage.

## Overriding a derived number was correct

The data implied an exchange rate of 0.58. The instruction was to use 0.57,
because the rate moved across the sixteen days.

That override was right. A figure derived from records is an average of averages
contaminated by forex markup. The person who was there knows things the
spreadsheet does not.

**The general form:** an assistant will defend a number it derived, because it
can show its working. It should still lose to lived knowledge, and saying so
plainly is enough. No justification is required beyond "I was there."

## Asking "is this even possible here?" reopened a closed door

An early session concluded that real map geography was unavailable, because
geocoding services were blocked by the network policy. The map became an abstract
diagram of points and lines, and that constraint was written down as settled.

A later request for something more realistic prompted a re-test. Geocoding was
still blocked. But `git clone` worked fine, so real prefecture coastlines had
been reachable the whole time. The environment had never changed. The picture of
it had simply never been completed.

**The lesson generalises:** a constraint accepted once tends to stay accepted,
because nothing prompts a re-examination. Pushing on it is cheap, and
occasionally the answer has been different all along. Worth doing whenever the
cost of the workaround starts to rise.

## Looking at the output caught what review could not

Two bugs shipped into first drafts. Both were caught by rendering the page and
looking at it, never by reading the code.

One was a map projection error that flattened an entire country into a horizontal
band, because latitude was being computed in radians while longitude stayed in
degrees.

The second was more instructive. Japanese day labels printed on top of one
another. Inspecting the page structure reported the layout as *correct*: a box of
exactly the right size, holding exactly two characters. That seemed to clear the
layout of suspicion. Only a screenshot at three times scale showed both
characters drawn at the same position.

**The box was right and the drawing was wrong.** Structural inspection can
confirm everything and still miss what is on screen. The pixels are the
authority, and a feature that works only once a webfont has loaded is fragile
even when the webfont usually loads.

## The shape of all five

Four of these five are the same move in different clothes: **prefer the artefact
to the description of it.** Hand over the file rather than summarise it. Look at
the render rather than review the code. Re-test the environment rather than trust
the note about it.

The fifth, on placeholders, is the counterweight. When the artefact does not
exist yet, say so visibly rather than approximate it.
