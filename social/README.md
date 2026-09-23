# Bluesky posts

One post a day to @shirshacreates.bsky.social, drafted from that day's entry in
`BUILDING_IN_PUBLIC.md`. Bluesky runs about a day behind the website.

## The loop

1. Asked for day N: read the Day N entry, write `drafts/day-NN.md`, run
   `python3 social/bsky.py check social/drafts/day-NN.md`.
2. Look at every image or video frame being attached. The privacy gate reads
   metadata, not pixels.
3. Show the owner the full text, the count the script printed, and the media.
   **Wait.**
4. The owner posts it by hand. When they say it is up, add the day to
   `posted.json` (link if given) and commit that to a branch with a PR, as
   with everything else here.

`bsky.py post` exists but is not in use: the owner posts. Run it only if the
owner explicitly says "post it" to you. Never auto-post. Never schedule.

## Credentials

Only needed if `bsky.py post` is ever used. `BLUESKY_HANDLE` and
`BLUESKY_APP_PASSWORD`, set as environment variables in
the cloud environment's settings. An app password, never the account password.
Never committed, never pasted into a chat. The network policy must allow
`bsky.social` and `bsky.network` (and `video.bsky.app` for video).

## Format

- First line exactly `Day N/16 · Japan Trip visualised 🇯🇵`
- Blank line between paragraphs; hashtags on the line directly under the last
  one, as on Day 1
- One main detail. At most 300 characters as Bluesky counts them, hashtags
  included. The script counts; do not estimate.
- Ends `#buildinpublic #dataviz`
- Up to 4 images or 1 video, never both. Alt text comes from `assets/README.md`.

## Voice

- Lead with the number, the failure, or a before/after. Never "excited to share".
- Never invent or round a number. If it is not in the entry, it is not in the post.
- Tell failures straight, not as lessons learned.
- Claude only when it is genuinely the story, never as a credit line.

## Never post

- Either traveller's name (they are A and B), emails, phone numbers, addresses,
  booking, order or payment references, or anything copied from `source/`.
- Shopping or gifts, in any form.
