#!/usr/bin/env python3
"""Generate PWA icons (PNG) for the RPGT Calculator: a house on a jade gradient,
gold roof, white body. Pure Python — no Pillow. Produces icon-180/192/512.png."""
import zlib, struct, math, os

OUT = os.path.dirname(os.path.abspath(__file__))
TOP = (17, 138, 118)     # jade #128a76
BOT = (10, 80, 68)       # deep jade #0a5044
ROOF = (216, 174, 92)    # gold #d8ae5c
BODY = (255, 255, 255)   # white

# normalized polygons (y down)
ROOF_TRI = [(0.50, 0.150), (0.850, 0.455), (0.150, 0.455)]
HOUSE_BODY = [(0.205, 0.455), (0.795, 0.455), (0.795, 0.850), (0.205, 0.850)]
# a doorway punched out of the body
DOOR = [(0.435, 0.850), (0.435, 0.640), (0.565, 0.640), (0.565, 0.850)]

def inside(poly, x, y):
    n = len(poly); ins = False; j = n - 1
    for i in range(n):
        xi, yi = poly[i]; xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            ins = not ins
        j = i
    return ins

def color_at(fx, fy):
    if inside(DOOR, fx, fy):
        return None
    if inside(ROOF_TRI, fx, fy):
        return ROOF
    if inside(HOUSE_BODY, fx, fy):
        return BODY
    return None

def make_icon(size, path):
    W = H = size; ss = 3
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        t = y / (H - 1)
        bg = (int(TOP[0]+(BOT[0]-TOP[0])*t), int(TOP[1]+(BOT[1]-TOP[1])*t), int(TOP[2]+(BOT[2]-TOP[2])*t))
        for x in range(W):
            acc = [0.0, 0.0, 0.0]; hits = 0
            for sy in range(ss):
                for sx in range(ss):
                    fx = (x + (sx+0.5)/ss) / size
                    fy = (y + (sy+0.5)/ss) / size
                    c = color_at(fx, fy)
                    if c is not None:
                        acc[0]+=c[0]; acc[1]+=c[1]; acc[2]+=c[2]; hits += 1
            if hits == 0:
                raw += bytes((bg[0], bg[1], bg[2], 255))
            else:
                a = hits / (ss*ss)
                fg = (acc[0]/hits, acc[1]/hits, acc[2]/hits)
                raw += bytes((int(bg[0]+(fg[0]-bg[0])*a), int(bg[1]+(fg[1]-bg[1])*a), int(bg[2]+(fg[2]-bg[2])*a), 255))

    def chunk(typ, data):
        return struct.pack(">I", len(data)) + typ + data + struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff)
    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack(">IIBBBBB", W, H, 8, 6, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
           + chunk(b'IEND', b''))
    with open(os.path.join(OUT, path), 'wb') as f:
        f.write(png)
    print(path, len(png), "bytes")

for s, p in [(180, 'icon-180.png'), (192, 'icon-192.png'), (512, 'icon-512.png')]:
    make_icon(s, p)
print("done")
