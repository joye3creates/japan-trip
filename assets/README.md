# Posting assets

All regenerated from the live pages, all swept for personal data before export.
Stills are 2x.

| File | What it shows |
|---|---|
| `clock_hero.png` | The clock view: sixteen days laid out hour by hour |
| `route_map.png` | The route map with the day rail and a detail panel |
| `numbers_tab.png` | The analytics tab: spend by day, by category, transport mix |
| `woodblock_full.png` | The full aged survey sheet, whole page |
| `site_index.png` | The index of the four builds |
| `day-04.png` | The build-log page: a generated day card, header and day nav |
| `interaction.mp4` | 21s. Map dissolving into the clock, then toggling to the ledger and back |
| `day-03-toggle.mp4` | 8.5s, cut from `interaction.mp4`: map dissolving into the clock, one toggle to the ledger and back |
| `tabs-route-numbers-ledger.mp4` | 25s. Route, day isolation, Numbers, Ledger with filters |
| `interaction.gif` | The first video at 600px, for places that will not take video |

**For Bluesky use the mp4 files.** Both are about a megabyte.

Only the files a page actually links are copied into `site/assets/`. The rest
live here and are posted by hand.

The build log looks for `day-NN.png` for day N unless that day's entry names
another file with a `**Media:**` line, so a new day needs a file here and no
code change. Days 1-3 are mapped to their existing stills rather than renamed,
so the names in this table stay true.

## How the stills are captured

Headless Chromium at 2x, driven by Playwright. Two things are easy to get wrong
and neither one announces itself.

**Fonts.** Chromium here does not trust the agent proxy's certificate
authority, so `fonts.googleapis.com` fails with `ERR_CERT_AUTHORITY_INVALID`
and every page quietly falls back to Georgia. `curl` does trust it, so fetch
the stylesheet and its woff2 files with curl and serve them back into the page
through `page.route()`. Then read `document.fonts` and confirm the families
actually loaded. A render that looks plausible is not evidence the type is
right.

**Framing.** The clock view's stage letterboxes inside its sticky pane unless
the viewport height is chosen to match the stage's own aspect ratio, which is
how an earlier still ended up two-thirds empty paper. The woodblock sheet is
taller than any sensible viewport, so screenshot the `.sheet` element rather
than the page, or the day strip gets sliced mid-row.

## Checked before export

- No traveller names, emails, phone numbers, addresses or booking references in
  any rendered page
- Hotel and landmark names are businesses and are left in deliberately
- Japanese script is kept on the two pages that were designed with it, the route
  map and the woodblock sheet
- Shopping and gifts excluded from the data, and no longer offered as filters

The privacy gate in `privacy_gate.py` cannot read text drawn into a screenshot
or a video frame. Every file here needs a human to look at it.
