#!/usr/bin/env python3
"""Reduce Japan prefecture geometry to something that can ship inside one HTML file.

Douglas-Peucker simplification plus coordinate rounding. The target style is an
old woodblock survey map, where a slightly generalised coastline reads as correct
rather than as a loss of fidelity.
"""
import json, math
from pathlib import Path

SRC = "/tmp/claude-0/-home-user/b3850738-abc6-5216-a1c1-a24a34cc94c0/scratchpad/geo/japan.geojson"
OUT = Path(__file__).resolve().parent / "data" / "japan_geo.json"

TOL      = 0.010   # degrees; coastline detail
MIN_AREA = 0.004   # drop islands smaller than this (deg^2), keeps the map uncluttered
PREC     = 3       # ~110 m

# Prefectures the trip actually touched, by the dataset's own English names.
VISITED = {
 "Tokyo To","Yamanashi Ken","Kyoto Fu","Hiroshima Ken","Oita Ken","Kumamoto Ken",
 "Osaka Fu","Nara Ken","Hyogo Ken","Ishikawa Ken","Gifu Ken","Nagano Ken","Kanagawa Ken",
}

def perp(p, a, b):
    if a == b: return math.dist(p, a)
    (x,y),(x1,y1),(x2,y2) = p,a,b
    dx,dy = x2-x1, y2-y1
    t = max(0, min(1, ((x-x1)*dx + (y-y1)*dy) / (dx*dx+dy*dy)))
    return math.dist(p, (x1+t*dx, y1+t*dy))

def dp(pts, tol):
    if len(pts) < 3: return pts
    dmax, idx = 0, 0
    for i in range(1, len(pts)-1):
        d = perp(pts[i], pts[0], pts[-1])
        if d > dmax: dmax, idx = d, i
    if dmax > tol:
        return dp(pts[:idx+1], tol)[:-1] + dp(pts[idx:], tol)
    return [pts[0], pts[-1]]

def area(ring):
    s = 0
    for i in range(len(ring)):
        x1,y1 = ring[i]; x2,y2 = ring[(i+1) % len(ring)]
        s += x1*y2 - x2*y1
    return abs(s)/2

def rings_of(geom):
    if geom["type"] == "Polygon":   return [geom["coordinates"][0]]
    return [poly[0] for poly in geom["coordinates"]]

def main():
    g = json.load(open(SRC))
    prefs, kept, dropped, pts_in, pts_out = [], 0, 0, 0, 0
    import sys; sys.setrecursionlimit(100000)

    for f in g["features"]:
        name = f["properties"]["nam"]; ja = f["properties"].get("nam_ja","")
        out = []
        for ring in rings_of(f["geometry"]):
            pts_in += len(ring)
            if area(ring) < MIN_AREA:
                dropped += 1; continue
            s = dp([tuple(c) for c in ring], TOL)
            if len(s) < 4: continue
            out.append([[round(x,PREC), round(y,PREC)] for x,y in s])
            pts_out += len(s); kept += 1
        if out:
            prefs.append({"n":name, "ja":ja, "v":1 if name in VISITED else 0, "r":out})

    OUT.write_text(json.dumps(prefs, separators=(",",":")))
    print(f"prefectures  : {len(prefs)}")
    print(f"rings kept   : {kept}  (dropped {dropped} small islands)")
    print(f"points       : {pts_in:,} -> {pts_out:,}  ({pts_out/pts_in*100:.1f}%)")
    print(f"visited      : {sum(p['v'] for p in prefs)} prefectures")
    print(f"output       : {OUT.stat().st_size/1024:.0f} KB")

main()
