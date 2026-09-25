# Framer code component

`JapanBuildLogCard.tsx` is the card in the Playground section of the portfolio
site. It is pasted into Framer as a code component, so this copy is the record,
not the thing that runs.

**It reads `status.json` off the live site** and shows that day number, so the
card follows the build log without being edited. Everything it needs is a
property in Framer's panel:

| Panel field | Value |
|---|---|
| Status URL | `https://japantripon24hrclock.netlify.app/status.json` |
| Link | `https://japantripon24hrclock.netlify.app/` |
| Day | the fallback, used only when the fetch fails |

A failed fetch degrades to the hand-set Day rather than to a blank, which is
why a wrong Status URL shows a stale number instead of an error. The site was
renamed from `courageous-lolly-4dfc48` at some point, and that is exactly how
it went unnoticed.

**The fetch needs the site to be readable without a password.** Netlify's site
protection applies to `status.json` too, so while the site is Private the card
falls back to the hand-set Day. `netlify.toml` already sends
`Access-Control-Allow-Origin: *` for that one path, and nothing else.

Check it by opening the Status URL in a browser tab. JSON on screen means the
card will work; a password prompt means it will not.
