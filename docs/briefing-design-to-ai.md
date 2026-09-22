# Briefing Design to AI

> **Snapshot.** The living version is a Claude doc at
> https://claude.ai/code/artifact/7fd68c77-8280-4dc7-890f-c4fa3798add3 — edit and
> comment there. This copy exists so the repo is a complete archive and so the
> content survives independently. Re-export it when the doc changes materially.
>
> `STYLE_BRIEF.md` in the repo root is the earlier working draft this grew from.
> Where they differ, the doc is newer.

A working guide to getting the visual and interactive result you want, written
from what actually happened while building an interactive map of a sixteen-day
trip through Japan.

## What to send, ranked by value per minute

Most advice about briefing design to an AI assumes the answer is to be more
thorough. That is the wrong axis. The question is which kinds of thoroughness
pay, and the returns are wildly uneven.

| Your effort | What it buys | What to send |
| --- | --- | --- |
| 5 minutes | **Highest** | Three to six reference images, each with one line naming what to take from it |
| 10 minutes | High | A short written note: palette, type, materials, and a list of what to avoid |
| Hours | Medium | A Figma file, but only if you already work in Figma |
| Hours | **Lowest** | A finished, pixel-perfect mockup |

### Why a finished mockup scores worst

Hand over a finished mockup and it gets reproduced literally, including its
accidents. The slightly-off padding you never got round to fixing becomes a rule.
The one component drawn at a different scale becomes a deliberate variation.

Hand over tokens and references instead and what comes back is a system, one that
extends to screens nobody has drawn yet. That second outcome is almost always the
one actually wanted, because any real project has far more screens than anyone
will ever mock up.

The mockup answers one question perfectly. The system answers every question
approximately. Approximately is worth more.

## Briefing visual style

### The one habit that matters most

Say what to take from each reference, not just that you like it.

> I like this map.

> Take the palette and the paper texture from this. Take the double-rule frame
> and the boxed title. Ignore the density, mine should breathe more.

The second is roughly ten times more useful and cost fifteen extra seconds. A
reference without instructions is a Rorschach test: it contains a dozen qualities
and no signal about which three you actually want.

### The negative list is underrated

Saying what to avoid is often more decisive than saying what to aim for, because
it rules out the defaults that get reached for otherwise.

- No gradients, no drop shadows, no rounded corners
- Not the cream-and-serif look that nearly every AI design lands on
- No emoji standing in for icons
- Do not centre everything
- Avoid pure black and pure white

A single line of this kind eliminates more wrong outcomes than a paragraph of
aspiration.

### The template

Blanks are fine. Guessing is worse than blank, because a wrong specific reads as
a decision and gets built on.

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
  (Names if you know them, otherwise a description: "a Mincho serif",
   "a grotesque with personality, not Inter".)

MATERIAL
  Texture, grain, paper, glass, none:
  Light source, depth, flatness:

REFERENCES
  1. <image>  - take: ______  ignore: ______
  2. <image>  - take: ______  ignore: ______

DENSITY
  Sparse and roomy, or dense and information-rich:

NEGATIVE LIST
  -
```

## Briefing interactions

This needs a completely different format, and that is the part people get wrong.
Interactions are behaviour over time. A static frame cannot hold them, so prose
beats any visual tool here. A clickable prototype shows the happy path and hides
every state that actually causes trouble.

### Trigger, response, feel

```
WHEN <the thing I do>  ->  <what happens>  (feel: <how fast, how heavy>)
```

Real examples from the trip map:

```
WHEN I scroll on the map        -> it zooms toward the cursor      (feel: immediate)
WHEN zoom passes "region"       -> place marks fade in             (feel: gentle, ~200ms)
WHEN zoom passes "city"         -> names appear beside the marks   (feel: gentle)
WHEN I hover a route line       -> a card appears near the cursor  (feel: instant, no delay)
WHEN I click a day in the strip -> the map flies to that day only  (feel: eased, ~400ms)
WHEN I click the same day again -> it releases back to the whole trip
```

Six lines. That is a complete interaction spec for a map, and it took under two
minutes to write.

### The states everyone forgets

- **At rest** — what it looks like before anyone touches it
- **Hover** — and whether touch devices get an equivalent
- **Active or pressed**
- **Selected** — and whether selection is exclusive or additive
- **Empty** — no data yet
- **Loading**
- **Error**

The empty state repays attention most and is specified least often. On this
project, steps, photographs and handwritten notes were all still pending, so how
*pending* should look was a genuine design decision affecting most of the
interface.

### Motion vocabulary

- **Snap** — no animation, instant
- **Ease** — soft start and stop, roughly 200 to 400 milliseconds
- **Drift** — slow, ambient, in the background
- **Stagger** — items arriving one after another

One rule applies whether or not it is asked for: anything that animates gets
disabled for people who have reduced motion turned on.

### Screen recordings are the cheat code

Fifteen seconds of screen capture showing an app doing something you like, plus
"the bit at eight seconds", is the highest-signal thing you can send about
behaviour. Timing and weight survive the transfer intact. Words have to
reconstruct those; video just carries them.

## On Figma specifically

Figma files can be read directly through a connector, so this is a real option
rather than a dead end. But it pays off in exactly one situation: **you already
work in Figma and want exact tokens locked down.**

The useful file is not a mockup. It is one page containing:

- A colour token frame, named swatches with hex values
- A type scale, named styles with size, weight and line height
- A spacing scale
- Two or three real components, each shown in its several states

That converts to code faithfully, because every decision has a name attached. A
beautiful mockup with no named styles can only be copied, not understood.

### The recommendation while a design is still unsettled

Skip it. The reason is about sequencing rather than about Figma. Early on the
design is still a question, and the fastest way to answer a question is to see
several answers quickly. Building a Figma file commits hours to one answer before
you know whether it is the right one.

## The worked example

### What was asked for

An existing interactive map of a sixteen-day trip through Japan, already built in
a clean modern style, was to be redone in a different visual language. The brief
was one reference image, a scan of an early twentieth-century Japanese survey map,
plus six specifications:

1. Minimal lines
2. Ukiyo-e woodcut feeling
3. Very neutral colour
4. A paper feel, with light texture
5. Interactive
6. Zoomable, so you can dig deeper into an area

Six specifications and one image. Under a minute to write.

### What those six settled

A great deal. They determined the palette direction, the linework weight, the
material treatment, the frame, and the fact that detail should be revealed
progressively rather than sitting on the surface. The result needed two correction
passes, both minor: the first attempt was too saturated for "very neutral" and too
busy for "minimal lines".

### What the brief did not settle

| Decision | What was chosen | Why it mattered |
| --- | --- | --- |
| Typefaces | Shippori Mincho for display, Spectral for body | Sets the period feel more than any colour choice does |
| How the route reads against land | Oxidised vermillion, the only saturated colour on the page | Determines whether the map is about the country or about the journey |
| What "dig deeper" concretely means | Progressive disclosure by zoom level, not click-through drilling | Two completely different interaction models |
| Whether to keep prefecture borders | Kept, but faded, with coastline weight only on visited prefectures | The difference between a map and a diagram |

**This is the useful lesson.** Those four are exactly the level of detail where
one line of input changes the outcome most. Not the high-level vibe, which six
words already captured well. Not the fine implementation, which does not need
direction. The layer in between: the handful of structural choices that a style
reference cannot encode.

## Beyond visual style

The rest of what this project taught, about working with these tools rather than
about design, now lives in its own document: `docs/what-moved-the-needle.md`,
whose living version is at
https://claude.ai/code/artifact/61ebb4fc-280d-4643-8d2b-952318c78284
