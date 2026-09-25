#!/usr/bin/env python3
"""Strip metadata from images inlined into a page as data: URIs.

The interaction studies were built with their photographs pasted straight into
the HTML, which walks past the gate's image check: a data: URI is text. It no
longer does, and these files were the first thing it caught. Same rule as
scrub_photos.py applies to a file on disk — what ships is pixels and nothing
else — so the same stripper runs over the blobs.

Idempotent. Run it over explorations/ whenever a study is added.
"""
import base64, re, sys
from pathlib import Path
from scrub_photos import strip_app_segments

URI = re.compile(r"data:image/([\w.+-]+);base64,([A-Za-z0-9+/=]+)")


def clean(text):
    n = [0]

    def one(m):
        raw = base64.b64decode(m.group(2))
        out = strip_app_segments(raw)
        if out != raw:
            n[0] += 1
        return f"data:image/{m.group(1)};base64," + base64.b64encode(out).decode()

    return URI.sub(one, text), n[0]


def main(paths):
    for p in paths:
        text = p.read_text()
        out, n = clean(text)
        if n:
            p.write_text(out)
        print(f"  {p.name:<34} {n} image(s) stripped, "
              f"{(len(text) - len(out)) // 1024} KB smaller")


if __name__ == "__main__":
    args = [Path(a) for a in sys.argv[1:]] or sorted(Path("explorations").glob("*.html"))
    main(args)
