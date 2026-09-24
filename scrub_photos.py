#!/usr/bin/env python3
"""Turn original photographs into publishable ones, keeping what they know.

    python3 scrub_photos.py            # pics/ -> assets/photos/ + data/photo_meta.json

An original carries a capture time, a device fingerprint and often coordinates.
The first is the most useful data this project has been missing; the other two
must never reach a public URL. So this reads the metadata into a data file and
then writes a copy of the picture with none of it left.

`pics/` is gitignored. Originals stay on the machine that took them. Only the
scrubbed copies and the harvested facts are committed.

Needs Pillow. It is not imported anywhere in the build, so Netlify never
installs it: `privacy_gate.py` verifies the result using the standard library
alone, and refuses anything this script has not been run over.
"""
import json, re, struct, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC, OUT, META = ROOT / "pics", ROOT / "assets/photos", ROOT / "data/photo_meta.json"
MAX_EDGE, QUALITY = 1600, 82

EXIF_DATE = 36867          # DateTimeOriginal
EXIF_DATE_FALLBACK = 306   # DateTime
GPS_IFD = 34853


def _dms(v):
    try:
        d, m, s = [float(x) for x in v]
        return d + m / 60 + s / 3600
    except Exception:
        return None


def harvest(im):
    """What the original knows, before it is thrown away."""
    out = {}
    exif = im.getexif()
    if not exif:
        return out
    taken = exif.get(EXIF_DATE) or exif.get(EXIF_DATE_FALLBACK)
    if not taken:
        taken = exif.get_ifd(0x8769).get(EXIF_DATE)
    if taken:
        try:
            out["taken"] = datetime.strptime(str(taken), "%Y:%m:%d %H:%M:%S").isoformat()
        except ValueError:
            pass
    gps = exif.get_ifd(GPS_IFD)
    if gps:
        lat, lng = _dms(gps.get(2, ())), _dms(gps.get(4, ()))
        if lat is not None and lng is not None:
            if str(gps.get(1, "N")).upper().startswith("S"): lat = -lat
            if str(gps.get(3, "E")).upper().startswith("W"): lng = -lng
            out["lat"], out["lng"] = round(lat, 6), round(lng, 6)
    return out


def strip_app_segments(data):
    """Pillow still writes a JFIF APP0. Remove every APPn and COM outright, so
    what lands in assets/ is pixels and nothing else."""
    out, i = bytearray(data[:2]), 2
    while i + 4 <= len(data) and data[i] == 0xFF:
        m = data[i + 1]
        if m == 0xDA:
            out += data[i:]
            break
        n = struct.unpack(">H", data[i + 2:i + 4])[0]
        if not (0xE0 <= m <= 0xEF or m == 0xFE):
            out += data[i:i + 2 + n]
        i += 2 + n
    return bytes(out)


def day_for(iso, days):
    d = iso.split("T")[0]
    for row in days:
        if str(row.get("date")) == d:
            return row.get("day_index"), row.get("label")
    return None, None


def main():
    try:
        from PIL import Image, ImageOps
    except ImportError:
        sys.exit("scrub_photos.py needs Pillow:  pip install pillow")

    if not SRC.is_dir():
        sys.exit(f"No {SRC.name}/ directory. Put the original photographs there.")

    # trip.json carries the day labels ("Beppu & Mt. Aso"); days.json is the
    # raw sheet dump and has only the sheet name, so prefer the assembled one.
    days = []
    for candidate in ("data/trip.json", "data/days.json"):
        f = ROOT / candidate
        if not f.is_file():
            continue
        loaded = json.loads(f.read_text())
        days = loaded.get("days", []) if isinstance(loaded, dict) else loaded
        if days and any(r.get("label") for r in days):
            break

    OUT.mkdir(parents=True, exist_ok=True)
    meta, seen = {}, 0
    for src in sorted(SRC.iterdir()):
        if src.suffix.lower() not in (".jpg", ".jpeg", ".png", ".heic", ".webp"):
            continue
        seen += 1
        with Image.open(src) as im:
            facts = harvest(im)
            im = ImageOps.exif_transpose(im)      # bake rotation in, then lose the tag
            im = im.convert("RGB")
            im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
            name = re.sub(r"[^a-z0-9]+", "-", src.stem.lower()).strip("-") + ".jpg"
            dest = OUT / name
            im.save(dest, "JPEG", quality=QUALITY, optimize=True, exif=b"")
        dest.write_bytes(strip_app_segments(dest.read_bytes()))

        if facts.get("taken"):
            idx, label = day_for(facts["taken"], days)
            if idx is not None:
                facts["day_index"], facts["day_label"] = idx, label
        meta[name] = facts

        had = [k for k in ("taken", "lat", "lng") if k in facts]
        kb = dest.stat().st_size // 1024
        where = f" -> day {facts['day_index']}" if "day_index" in facts else ""
        print(f"  {name:36} {kb:>5} KB   kept: {', '.join(had) or 'nothing, the original had none'}{where}")

    META.parent.mkdir(exist_ok=True)
    META.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n")
    dated = sum(1 for v in meta.values() if "taken" in v)
    located = sum(1 for v in meta.values() if "lat" in v)
    print(f"\n  {seen} photographs. {dated} carried a capture time, {located} carried coordinates.")
    print(f"  Scrubbed copies in {OUT.relative_to(ROOT)}/, what they knew in {META.relative_to(ROOT)}.")


if __name__ == "__main__":
    main()
