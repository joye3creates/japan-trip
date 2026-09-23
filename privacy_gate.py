#!/usr/bin/env python3
"""Refuse to publish anything that looks personally identifying.

build_site.py hands every file it is about to write into site/ to check()
first. One hit and the build fails before site/ is touched. Findings name
the file and line (or byte offset, for binaries) and never the matched text,
so a build log on Netlify cannot itself become the leak.

Run by hand against what is already there:
    python3 privacy_gate.py            # scans site/

Why the names are hashed. names.local.txt is gitignored and absent on
Netlify's build machine, so the patterns have to travel with this script.
Writing them out in plain text would commit exactly what the gate exists to
keep out. Each name is stored as its length and a salted SHA-256, and every
run of letters of that length in the output is hashed and compared. That
keeps names out of `git grep` and casual reading. It is not secrecy: a
dictionary of first names reverses a hash like this in seconds, so this file
still belongs in a private repository.

To add a name: append (len(name), sha256(SALT + name.lower())) to NAME_HASHES.
    python3 -c "import hashlib;n='x';print(len(n),hashlib.sha256(('japan-trip/privacy-gate/v1:'+n).encode()).hexdigest())"
"""
import hashlib, re, struct, sys, zlib
from pathlib import Path

SALT = "japan-trip/privacy-gate/v1:"

# Both travellers, the family name, and the owner's public handle. The handle
# is why the allowlist exists: it may appear in the two links below and
# nowhere else.
NAME_HASHES = {
    (5, "5d8f3f1edafd3eb9b8e377f6ac931327ac9dcf5661d7762f2dba034b31e4d064"),
    (6, "bb634634710e1f525990b87a3dc5ec84cd3f933913b6745014e1813ce5a8f932"),
    (6, "dcd66416a1a1e00d660995c1588c1e24fab94a0302cdee184daffb614ec5f1ab"),
    (7, "f7b688cf28dd22c0a0223be81335eee9ed5348fe0e1b90e50e8884191c9c5079"),
}

# Exactly these two, matched case-insensitively and blanked before scanning.
ALLOWLIST = ("shirshabiswas.framer.website", "shirshacreates.bsky.social")

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")

PHONE = [
    # international: +81 3 1234 5678, +91-98765-43210
    re.compile(r"(?<![\w.])\+\d{1,3}[\s.-]?\(?\d{1,5}\)?(?:[\s.-]?\d{2,5}){2,3}(?![\w.])"),
    # Japanese domestic: 03-1234-5678, 090-1234-5678
    re.compile(r"(?<![\w.])0\d{1,4}-\d{1,4}-\d{3,4}(?![\w.])"),
    # Indian mobile, bare ten digits starting 6-9
    re.compile(r"(?<![\w.])[6-9]\d{9}(?![\w.])"),
]

REFERENCE = [
    # a labelled reference: "Booking no. HX42..", "order #1234567", "PNR: ABC123"
    re.compile(r"(?i)\b(?:booking|confirmation|reservation|order|itinerary|"
               r"reference|ref|pnr|pin|voucher)\s*(?:no\.?|number|num|id|code|#)?\s*"
               r"[:#]?\s*(?=[A-Z0-9-]*\d)[A-Z0-9][A-Z0-9-]{4,}\b"),
    # a bare code: eight or more capitals and digits, at least two of each
    re.compile(r"\b(?=(?:[A-Z0-9]*\d){2})(?=(?:[A-Z0-9]*[A-Z]){2})[A-Z0-9]{8,}\b"),
    # a long digit run that is not part of a decimal: order numbers, cards
    re.compile(r"(?<![\w.])\d(?:[ -]?\d){8,18}(?![\w.])"),
]

TEXT_SUFFIXES = {".html", ".htm", ".txt", ".json", ".js", ".css", ".svg",
                 ".xml", ".md", ".csv", ".webmanifest", ".toml"}


def _blank_allowlist(text):
    for ok in ALLOWLIST:
        text = re.sub(re.escape(ok), lambda m: " " * len(m.group()), text, flags=re.I)
    return text


def _has_name(text, _seen={}):
    """True if any run of letters, or any slice of one, hashes to a name."""
    lengths = {n for n, _ in NAME_HASHES}
    for run in re.findall(r"[A-Za-z]+", text):
        run = run.lower()
        for n in lengths:
            for i in range(len(run) - n + 1):
                w = run[i:i + n]
                if w not in _seen:
                    h = hashlib.sha256((SALT + w).encode()).hexdigest()
                    _seen[w] = (n, h) in NAME_HASHES
                if _seen[w]:
                    return True
    return False


def _scan_text(text):
    """Yield (line number, kind) for each finding. Never the match itself."""
    text = _blank_allowlist(text)
    for no, line in enumerate(text.splitlines(), 1):
        if _has_name(line):
            yield no, "name"
        if EMAIL.search(line):
            yield no, "email"
        if any(p.search(line) for p in PHONE):
            yield no, "phone number"
        if any(p.search(line) for p in REFERENCE):
            yield no, "booking/order reference shape"


def _binary_strings(data):
    """Printable runs from a binary, plus PNG text chunks inflated."""
    out = [(m.start(), m.group().decode("ascii"))
           for m in re.finditer(rb"[\x20-\x7e]{4,}", data)]
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        i = 8
        while i + 8 <= len(data):
            n, kind = struct.unpack(">I4s", data[i:i + 8])
            body = data[i + 8:i + 8 + n]
            if kind == b"zTXt" and b"\0" in body:
                try:
                    out.append((i, zlib.decompress(body.split(b"\0", 1)[1][1:]).decode("latin-1")))
                except zlib.error:
                    out.append((i, "unreadable compressed text chunk"))
            elif kind in (b"tEXt", b"iTXt"):
                out.append((i, body.decode("latin-1")))
            i += 12 + n
    return out


def _scan_binary(data):
    """Random bytes make phone and reference shapes meaningless, so binaries
    are checked for names and emails only, in their embedded strings."""
    for offset, s in _binary_strings(data):
        s = _blank_allowlist(s)
        if _has_name(s):
            yield f"byte {offset}", "name"
        if EMAIL.search(s):
            yield f"byte {offset}", "email"


def check(files):
    """files: {published path: str | bytes}. Returns a list of finding lines."""
    findings = []
    for path, content in sorted(files.items()):
        if isinstance(content, str):
            hits = [(f"line {n}", k) for n, k in _scan_text(content)]
        elif Path(path).suffix.lower() in TEXT_SUFFIXES:
            hits = [(f"line {n}", k) for n, k in _scan_text(content.decode("utf-8", "replace"))]
        else:
            hits = list(_scan_binary(content))
        findings += [f"  site/{path}  {where}  {kind}" for where, kind in hits]
    return findings


def enforce(files):
    """Exit the build if anything is found. Called before site/ is written."""
    findings = check(files)
    if findings:
        print(f"\nPRIVACY GATE: {len(findings)} finding(s). Nothing was written to site/.",
              file=sys.stderr)
        print("\n".join(findings), file=sys.stderr)
        print("Matched text is withheld on purpose. Open the file at that line.",
              file=sys.stderr)
        sys.exit(1)
    print(f"  privacy gate: {len(files)} files clean")


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent / "site")
    enforce({str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()})
