# How to brief visual style and interactions

Written after the woodblock experiment, where the brief was a reference image plus
about six sentences and that turned out to be close to optimal. This is what to
send, ranked by how much it buys per minute you spend on it.

---

## Part 1 — Visual style

### The ranking

| Effort | Value | What |
|---|---|---|
| 5 min | **Highest** | 3–6 reference images, each with one line naming *what to take from it* |
| 10 min | High | A short written note: palette, type, materials, and a **negative list** |
| Hours | Medium | A Figma file — only worth it if you already live in Figma |
| Hours | **Low** | A full pixel-perfect mockup |

### Why a full mockup scores badly

If you hand me a finished mockup I will reproduce *that screen*, literally,
including its accidents. If you hand me tokens and references I will build a
*system* that extends to screens you never drew. The second is what you actually
want, because the app has more screens than you will ever mock up.

### The single highest-value habit

**Say what to take from each reference, not just that you like it.** Compare:

> "I like this map."

> "Take the palette and the paper texture from this. Take the double-rule frame
> and the boxed title. Ignore the density — mine should breathe more."

The second one is roughly ten times more useful and took fifteen extra seconds.
Your woodblock brief already did this well: minimal lines, neutral colour, paper
feel, ukiyo-e. That was enough to work from.

### The negative list is underrated

Telling me what to avoid is often more decisive than what to aim for, because it
rules out the defaults I would otherwise reach for. Things worth saying out loud:

- no gradients / no drop shadows / no rounded corners
- not the cream-and-serif look that every AI design lands on
- no emoji as icons
- don't centre everything
- avoid pure black and pure white

### Template

Copy this, fill what you know, leave the rest blank. Blanks are fine. Guessing is
worse than blank, because a wrong specific reads as a decision.

```
FEELING
  Three adjectives:
  It should feel like:
  It should NOT feel like:

COLOUR
  Ground / background:
  Ink / text:
  One accent, used sparingly:
  Anything forbidden:
  (Hex if you have it. "Sampled from reference 2" is equally fine.)

TYPE
  Display / headings:
  Body:
  Numbers:
  (Font names if you know them, otherwise a description: "a Mincho serif",
   "a grotesque with personality, not Inter".)

MATERIAL
  Texture, grain, paper, glass, none:
  Light source, depth, flatness:

REFERENCES
  1. <image>  — take: ______  ignore: ______
  2. <image>  — take: ______  ignore: ______

DENSITY
  Sparse and roomy, or dense and information-rich:

NEGATIVE LIST
  -
```

---

## Part 2 — Interactions

**Do not use a visual tool for this.** Interactions are behaviour over time, and
prose beats a static frame every time. A Figma prototype shows me the happy path
and hides the states that actually matter.

### The format that works: trigger, response, feel

```
WHEN <the thing I do>  →  <what happens>  (feel: <how fast, how heavy>)
```

Real examples from the map:

```
WHEN I scroll on the map        → it zooms toward the cursor      (feel: immediate)
WHEN zoom passes "region"       → place marks fade in             (feel: gentle, ~200ms)
WHEN zoom passes "city"         → names appear beside the marks   (feel: gentle)
WHEN I hover a route line       → a card appears near the cursor  (feel: instant, no delay)
WHEN I click a day in the strip → the map flies to that day only  (feel: eased, ~400ms)
WHEN I click the same day again → it releases back to the whole trip
```

### Also worth listing: the states

Every interactive thing has more states than people brief. Name them:

- **at rest** — what it looks like before anyone touches it
- **hover** — and whether touch devices get an equivalent
- **active / pressed**
- **selected** — and whether selection is exclusive or additive
- **empty** — no data yet, which is most of your app right now
- **loading**
- **error**

The empty state matters most for this project, because steps, photos and notes
are all still pending. Saying how "pending" should *look* is a real design
decision.

### Motion vocabulary

You do not need easing curves. These words are enough:

- **snap** — no animation, instant
- **ease** — soft start and stop, ~200–400ms
- **drift** — slow, ambient, background
- **stagger** — items arrive one after another

One rule I will apply whether or not you ask: anything that animates gets
disabled for people who have reduced motion turned on.

### Screen recordings are gold

A 15-second screen capture of an app doing an interaction you like, plus "the bit
at 0:08", is the single highest-signal thing you can send about behaviour. Better
than any written spec, because timing and weight survive the transfer.

---

## Part 3 — On Figma specifically

I can read Figma files directly through a connector, so it is a real option, not
a dead end. But it pays off only in one situation: **you already work in Figma and
want exact tokens locked down.**

If you go that route, the useful file is not a mockup. It is one page containing:

- a colour token frame, named swatches with hex
- a type scale, named styles with size, weight and line height
- a spacing scale
- two or three real components in their several states

That I can turn into code faithfully. A beautiful mockup with no named styles, I
can only copy.

**My honest recommendation for this project:** skip Figma. Reference images plus
the filled template above will get you 90% of the way in a tenth of the time. Come
back to Figma when the design is settled and you want it pinned down.

---

## Part 4 — What actually happened this time

For the record, since this is case-study material. The woodblock brief was:

> reference image + "minimal lines" + "ukiyo-e woodcut" + "neutral colour" +
> "paper feel, play with light texture" + "make it interactive, zoom in and dig deeper"

Six specifications and one image. That was enough to produce something close on
the first attempt. What the brief did **not** settle, and what I had to decide
alone:

- which typefaces (chose Shippori Mincho with Spectral)
- how the route should read against the land
- what "dig deeper" means concretely (chose progressive disclosure by zoom level)
- whether to keep prefecture borders at all (kept them, but faded)

Any of those four would have been worth one line from you. That is the level of
detail where your input changes the outcome most.
