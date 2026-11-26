#!/usr/bin/env python3
"""गैस की बदबू — v3: built from the 4 reference doc edits.
 - 16:9-ish frame (1080x720) on black, no series header
 - one word at a time ON the picture (small white), key words as big condensed Teko
 - mixed media: photo wall, paper documents with marker highlight, torn newspaper headlines,
   flip-counter year, red spaced-number card, white page with taped photo, black label boxes
 - glitch / push / blur transitions
usage: gas3.py stills t.. | seg a b"""
import os, sys
os.environ['CINE_H'] = '720'
sys.path.insert(0, '/home/claude/studio/tools'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, math, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cine as C
import gas as G
from cine import ease, eio
BW, BH = C.W, C.H; CW, CH = 1080, 1920; BY = 560
P = G.P; K = G.K; TOTAL = K['total']; FPS = 30; A = G.A
clamp, lerp = G.clamp, G.lerp
FD = '/home/claude/studio/fonts/doc/'
FONT = {'s6': FD + 'nsd-600.ttf', 's8': FD + 'nsd-800.ttf', 's9': FD + 'nsd-900.ttf',
        't6': FD + 'teko-600.ttf', 't7': FD + 'teko-700.ttf', 'r4': FD + 'nserif-400.ttf', 'r7': FD + 'nserif-700.ttf',
        'it': FD + 'pkg_instrument-serif/package/files/instrument-serif-latin-400-italic.woff',
        'os': FD + 'pkg_oswald/package/files/oswald-latin-700-normal.woff'}
RED = (226, 36, 36); WHITE = (255, 255, 255); INK = (24, 22, 20)

_TC = {}
def tx(txt, f, size, col=WHITE):
    k = (txt, f, size, col)
    if k in _TC: return _TC[k]
    fo = ImageFont.truetype(FONT[f], size, layout_engine=ImageFont.Layout.RAQM); bb = fo.getbbox(txt)
    im = Image.new('RGBA', (bb[2] - bb[0] + 40, bb[3] - bb[1] + 40), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((20 - bb[0], 20 - bb[1]), txt, font=fo, fill=col + (255,)); _TC[k] = im; return im
def comp(cv, src, ox, oy, am, col=None):
    h, w = src.shape[:2]; Hh, Ww = cv.shape[:2]
    xa, ya = max(0, ox), max(0, oy); xb, yb = min(Ww, ox + w), min(Hh, oy + h)
    if xb <= xa or yb <= ya or am <= 0: return
    s = src[ya - oy:yb - oy, xa - ox:xb - ox]; al = s[..., 3:4] / 255 * am
    rgb = s[..., :3] if col is None else np.array(col, np.float32)
    cv[ya:yb, xa:xb] = cv[ya:yb, xa:xb] * (1 - al) + rgb * al
def put(cv, im, x, y, a=1.0, anchor='c', shadow=.7, blur=0.0, scale=1.0):
    if a <= 0.01: return
    if scale != 1.0: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BICUBIC)
    if blur > .3: im = im.filter(ImageFilter.GaussianBlur(blur))
    x0 = int(x - im.width / 2) if anchor == 'c' else int(x - 20) if anchor == 'l' else int(x - im.width + 20)
    y0 = int(y - im.height / 2)
    if shadow: comp(cv, np.asarray(im.filter(ImageFilter.GaussianBlur(10))).astype(np.float32), x0, y0 + 4, a * shadow, (0, 0, 0))
    comp(cv, np.asarray(im).astype(np.float32), x0, y0, a)
def pop(cv, txt, f, size, x, y, t, col=WHITE, dur=.3, shadow=.7, s0=1.15):
    if t <= 0: return
    k = eio(t / dur); put(cv, tx(txt, f, size, col), x, y, k, 'c', shadow, 14 * (1 - k), s0 - (s0 - 1) * k)
def labelbox(cv, txt, x, y, t, f='s8', size=60, bg=(10, 10, 10), fg=WHITE, dur=.25, anchor='l'):
    if t <= 0: return
    k = eio(t / dur); im = tx(txt, f, size, fg); w, h = im.width - 6, im.height - 6
    x0 = int(x if anchor == 'l' else x - w / 2); y0 = int(y - h / 2); ww = int(w * k)
    cv[max(0, y0):y0 + h, max(0, x0):x0 + ww] = np.array(bg, np.float32)
    if k > .5: put(cv, im, x0 + w / 2, y - 1, clamp((k - .5) / .3), 'c', 0)
def handles(cv, cx, cy, w, h, t, col=(235, 235, 235)):
    if t <= 0: return
    k = eio(t / .3); w, h = w * (0.9 + .1 * k), h * (0.9 + .1 * k)
    x0, y0, x1, y1 = int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2); c = tuple(float(v * k) for v in col)
    for x in range(x0, x1, 18): cv2.line(cv, (x, y0), (min(x + 9, x1), y0), c, 2); cv2.line(cv, (x, y1), (min(x + 9, x1), y1), c, 2)
    for y in range(y0, y1, 18): cv2.line(cv, (x0, y), (x0, min(y + 9, y1)), c, 2); cv2.line(cv, (x1, y), (x1, min(y + 9, y1)), c, 2)
    for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)): cv2.rectangle(cv, (x - 8, y - 8), (x + 8, y + 8), c, -1)

# ---------------- materials
_PAPER = {}
def paper(w, h, seed=0, base=(238, 234, 224)):
    k = (w, h, seed, base)
    if k in _PAPER: return _PAPER[k].copy()
    r = np.random.default_rng(seed)
    lo = cv2.resize(r.normal(0, 1, (h // 40 + 2, w // 40 + 2)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)
    fib = cv2.GaussianBlur(r.normal(0, 1, (h, w)).astype(np.float32), (0, 0), .8)
    p = np.array(base, np.float32)[None, None] + (lo * 5 + fib * 4)[..., None]
    _PAPER[k] = p; return p.copy()
def torn_mask(w, h, seed=0, jag=10):
    r = np.random.default_rng(seed); pts = []
    for x in np.linspace(0, w, 40): pts.append((x, r.uniform(0, jag)))
    for y in np.linspace(0, h, 12): pts.append((w - r.uniform(0, jag * .6), y))
    for x in np.linspace(w, 0, 40): pts.append((x, h - r.uniform(0, jag)))
    for y in np.linspace(h, 0, 12): pts.append((r.uniform(0, jag * .6), y))
    m = np.zeros((h, w), np.uint8); cv2.fillPoly(m, [np.array(pts, np.int32)], 255); return m
def strip(txt, f, size, seed, pad=(34, 18), base=(236, 231, 218)):
    """torn newspaper strip with black serif text -> RGBA PIL"""
    t = tx(txt, f, size, INK); w, h = t.width + pad[0] * 2 - 40, t.height + pad[1] * 2 - 40
    p = paper(w, h, seed, base); im = Image.fromarray(np.clip(p, 0, 255).astype(np.uint8)).convert('RGBA')
    im.alpha_composite(t, (pad[0] - 20, pad[1] - 20)); im.putalpha(Image.fromarray(torn_mask(w, h, seed))); return im
def place(cv, im, x, y, rot, t, dur=.18, a=1.0, shadow=.6):
    """slam an RGBA card onto cv: scale 1.25->1 + rotate, drop shadow"""
    if t <= 0: return
    k = eio(t / dur); s = 1.25 - .25 * k
    r = im.rotate(rot, Image.BICUBIC, expand=True)
    put(cv, r, x, y, a * k, 'c', shadow, 0, s)

_TILE = {}
def tile(name, fx=.5, fy=.5, gray=False, size=(BW, BH)):
    k = (name, fx, fy, gray, size)
    if k not in _TILE:
        im = Image.open(A + name).convert('RGB'); w, h = im.size; tw, th = size; s = max(tw / w, th / h)
        im = im.resize((int(w * s) + 1, int(h * s) + 1), Image.LANCZOS); x0 = int((im.width - tw) * fx); y0 = int((im.height - th) * fy)
        a = np.asarray(im).astype(np.float32)[y0:y0 + th, x0:x0 + tw]
        a = C.grade(a, sat=0 if gray else .95)
        if gray: a = a * np.array([1.04, 1.0, .9], np.float32)
        _TILE[k] = a
    return _TILE[k]
def wall(tiles, z, gap=10, bg=8, pops=None, t=0, center_live=None):
    """3x3 photo wall; z=1 whole wall in frame, z=3 centre tile fills the frame"""
    o = np.full((BH, BW, 3), bg, np.float32); tw, th = BW / 3, BH / 3
    for i, tl_ in enumerate(tiles):
        cx, cy = i % 3 - 1, i // 3 - 1
        if pops is not None and t < pops[i]: continue
        sc = 1.0 if pops is None else .85 + .15 * eio((t - pops[i]) / .15)
        w, h = (tw - gap) * z * sc, (th - gap) * z * sc
        x = BW / 2 + cx * tw * z - w / 2; y = BH / 2 + cy * th * z - h / 2
        x0, y0, x1, y1 = int(x), int(y), int(x + w), int(y + h)
        if x1 <= 0 or y1 <= 0 or x0 >= BW or y0 >= BH or w < 2: continue
        src = center_live if (i == 4 and center_live is not None) else tl_
        r = cv2.resize(src, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA if z < 2 else cv2.INTER_LINEAR)
        xa, ya, xb, yb = max(0, x0), max(0, y0), min(BW, x1), min(BH, y1)
        o[ya:yb, xa:xb] = r[ya - y0:yb - y0, xa - x0:xb - x0]
    return o

def page(lines, w=1500, h=1000, seed=3, hl=None, hk=0.0, f='r7', size=70, top=120, lead=128):
    """paper document. lines = [(txt, font, size, color)], hl = index of the line to highlight, hk = 0..1 sweep"""
    p = paper(w, h, seed)
    for i, (t_, f_, s_, c_) in enumerate(lines):
        im = tx(t_, f_, s_, c_); y = top + i * lead
        if hl is not None and i in (hl if isinstance(hl, tuple) else (hl,)) and hk > 0:
            ww = int((im.width - 30) * clamp(hk)); y0 = int(y + 12); p[y0:y0 + im.height - 34, 110:110 + ww] = p[y0:y0 + im.height - 34, 110:110 + ww] * .25 + np.array([255, 222, 60], np.float32) * .75
        comp(p, np.asarray(im).astype(np.float32), 100, y, 1.0)
    return p
def warp_page(bg, pg, T, t, tilt=(.06, .0), push=(1.0, 1.12), cy_shift=0, blur_far=True):
    """lay the page into the band with a perspective tilt + slow push; soft shadow"""
    h, w = pg.shape[:2]; s = lerp(*push, eio(clamp(t / 4))) * min(BW / w, BH / h) * 1.02
    cx, cy = BW / 2, BH / 2 + cy_shift; tl_ = tilt[0]
    dw, dh = w * s / 2, h * s / 2
    dst = np.float32([[cx - dw * (1 - tl_), cy - dh], [cx + dw * (1 + tl_ * .2), cy - dh * (1 - tl_)],
                      [cx + dw, cy + dh * (1 + tl_ * .3)], [cx - dw * (1 + tl_ * .4), cy + dh]])
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]), dst)
    img = cv2.warpPerspective(pg, M, (BW, BH), flags=cv2.INTER_LINEAR)
    m = cv2.warpPerspective(np.ones((h, w), np.float32), M, (BW, BH))[..., None]
    sh = cv2.GaussianBlur(np.roll(m, 14, 0), (0, 0), 18)[..., None]
    o = bg * (1 - .6 * sh) ; o = o * (1 - m) + img * m
    if blur_far:   # shallow focus toward the far (right/top) side
        b = cv2.GaussianBlur(o, (0, 0), 6); g = np.clip((np.linspace(0, 1, BW)[None, :, None] - .55) * 2.2, 0, 1).astype(np.float32)
        o = o * (1 - g) + b * g
    return o

def glitch(o, T, amt=1.0):
    r = np.random.default_rng(int(T * 60)); o = o.copy()
    for _ in range(int(10 * amt)):
        y = int(r.integers(0, BH - 40)); hh = int(r.integers(8, 60)); dx = int(r.normal(0, 70 * amt))
        o[y:y + hh] = np.roll(o[y:y + hh], dx, 1)
    o[..., 0] = np.roll(o[..., 0], int(14 * amt), 1); o[..., 2] = np.roll(o[..., 2], -int(14 * amt), 1)
    return o

# ---------------- captions: one word at a time, on the picture
WORDS = json.load(open(P + '/work/words.json'))
BIG = {'ज़रूरी', 'भयानक', 'चुपचाप', 'भनक', 'टीचर', 'स्विच', 'चिंगारी', 'उड़', 'नाक', 'अलार्म', 'केमिकल', 'बंद', 'खोलो', 'दीवारों', 'पाइपलाइन'}
REDW = {'भयानक', 'अलार्म', 'चिंगारी'}
CAP_OFF = []  # filled after shots
def caption(cv, T, dark=False):
    if any(a <= T < b for a, b in CAP_OFF): return
    cur = [w for w in WORDS if w[0] - .02 <= T < w[1] + .12]
    if not cur: return
    st, en, wd = cur[-1]; wd = wd.strip(',.।'); t = T - st; cy = BY + BH / 2 + 10
    col = INK if dark else WHITE
    if wd in BIG and not dark:
        pop(cv, wd, 't7', 150, CW / 2, cy, t, RED if wd in REDW else WHITE, .16, .65, 1.1)
    else:
        pop(cv, wd, 's8', 50, CW / 2, cy, t, col, .1, 0 if dark else .85, 1.08)

# ---------------- band scenes  (each returns (band, dark_caption))
def sh(name, t, d, **kw): return G.shot3d(name, clamp(t / d), **kw)[0]
def arch(o, T, seed=0): return G.chroma(C.archive(o, T, seed=seed) * .9 + 14, 2)

OPEN_T = [tile(n, *xy) for n, xy in (('kettle.jpg', (.5, .5)), ('kitchen.jpg', (.3, .5)), ('switch.jpg', (.5, .5)), ('pipeline.jpg', (.5, .5)),
                                     ('flame.jpg', (.5, .5)), ('odorant.jpg', (.5, .5)), ('cylinder.jpg', (.5, .35)), ('kitchen.jpg', (.8, .5)), ('kettle.jpg', (.2, .6)))]
def B_open(T, t, d):
    live, _ = G.shot3d('flame.jpg', clamp(t / d), z=(1.0, 1.1), dz=(0, .2), focus=(.85, .85), blur=0)
    z = lerp(1.0, 3.0, eio(clamp((t - .9) / 1.1)))
    o = wall(OPEN_T, z, center_live=C.grade(live, sat=1.0))
    return o * .82, False
def O_open(cv, T, t, d):
    pop(cv, 'बदबू', 's9', 290, CW / 2, BY + BH / 2 + 8, t + 1, WHITE, .01, .6)
    handles(cv, CW / 2, BY + BH / 2 + 4, 620, 300, t + 1)

def B_kitchen(T, t, d):
    o = sh('kitchen.jpg', t, d, z=(1.0, 1.12), dz=(0, .3), tx=(0, -30), focus=(.85, .95), blur=9)
    o = C.bloom(o, 180, .45); o = G.wisps(o, T, 560, 690, alpha=.5, spread=.62)
    return C.grade(o, shadows=(0.9, 1.0, 1.15), highs=(1.1, 1.0, .85)) * (1 - .3 * eio(clamp((T - 3.45) / .2))), False
def O_kitchen(cv, T, t, d):
    ta = T - 3.45; pop(cv, 'असली', 't7', 300, CW / 2, BY + BH / 2 + 20, ta, WHITE, .2)
    ts = T - 3.95
    if ts > 0:
        w = tx('असली', 't7', 300).width - 60; k = eio(ts / .22); x0 = int(CW / 2 - w / 2); y = int(BY + BH / 2 + 6)
        cv[y - 10:y + 10, x0:x0 + int(w * k)] = np.array(RED, np.float32)

DOC1 = [('LPG  (प्रोपेन + ब्यूटेन)', 's8', 58, INK), ('रंग :  कोई नहीं', 'r7', 74, INK), ('गंध :  कोई नहीं', 'r7', 74, INK), ('सुरक्षा :  ?', 'r7', 74, (150, 40, 36))]
def B_odorless(T, t, d):
    bg = sh('cylinder.jpg', t, d, z=(1.1, 1.15), focus=(.1, .1), blur=20, fy=.35) * .45
    hk = clamp((T - 6.6) / .5); pg = page(DOC1, 1300, 760, 3, hl=2, hk=hk, top=70, lead=160)
    if T > 7.4: pg = page(DOC1, 1300, 760, 3, hl=(2,), hk=1, top=70, lead=160)
    return warp_page(bg, pg, T, t, tilt=(.07, 0), push=(.8, .88)), False
def O_odorless(cv, T, t, d): pass

def B_added(T, t, d):
    o = sh('flame.jpg', t, d, z=(1.0, 1.15), dz=(0, .25), focus=(.9, .9), blur=10)
    o = C.bloom(o, 150, .8, 40, (.7, .9, 1.2)); o = C.grade(o, shadows=(0.85, 1.0, 1.2), highs=(1.05, 1.0, .9))
    return o * (1 - .35 * eio(clamp((T - 8.7) / .3))), False
def O_added(cv, T, t, d): pop(cv, 'जानबूझकर', 't7', 230, CW / 2, BY + BH / 2 + 14, T - 8.78, WHITE, .2)

NEWS = None
def B_ruins(T, t, d):
    o = sh('ruins.jpg', t, d, z=(1.0, 1.14), dz=(0, .3), tx=(25, -25), focus=(.5, .8), blur=8)
    o = C.grade(arch(o, T, 5), sat=0, contrast=1.15) * .8
    tc = T - 12.9
    if tc > 0:   # newspaper collage slams in
        o = G.screen_tex(o * .55, .25)
        place(o, strip('मार्च 1937  ·  टेक्सस', 's8', 34, 11, (26, 12)), 300, 150, 3, tc, .14)
        place(o, strip('अमेरिका का सबसे भयानक', 'r7', 70, 12), 520, 320, -2, T - 13.45, .16)
        place(o, strip('स्कूल हादसा', 'r7', 120, 13, (40, 14)), 560, 500, 1.5, T - 14.1, .16)
    if 0 < tc < .12: o = glitch(o, T, .8)
    return o, False
def O_ruins(cv, T, t, d): pass

def flipcard(o, txt, cx, cy, sc=1.0):
    w, h = int(560 * sc), int(300 * sc); x0, y0 = int(cx - w / 2), int(cy - h / 2)
    card = np.zeros((h, w, 3), np.float32) + np.linspace(228, 200, h, dtype=np.float32)[:, None, None]
    cv2.line(card, (0, h // 2), (w, h // 2), (120, 120, 120), 3)
    im = tx(txt, 'os', int(230 * sc), (36, 36, 38)); comp(card, np.asarray(im).astype(np.float32), int(w / 2 - im.width / 2), int(h / 2 - im.height / 2 - 6), 1)
    mask = np.zeros((h, w), np.float32); cv2.rectangle(mask, (14, 14), (w - 14, h - 14), 1, -1); mask = cv2.GaussianBlur(mask, (0, 0), 6)[..., None]
    sh_ = cv2.GaussianBlur(mask[..., 0], (0, 0), 20)[..., None]
    reg = o[y0:y0 + h, x0:x0 + w]; reg[:] = reg * (1 - .7 * sh_) ; reg[:] = reg * (1 - mask) + card * mask
def B_texas(T, t, d):
    if t < 1.55:
        bg = sh('pipeline.jpg', t, d, z=(1.2, 1.25), focus=(.1, .1), blur=22) * .35
        k = clamp(t / .7); yr = int(round(2026 - (2026 - 1937) * (1 - (1 - k) ** 3)))
        flipcard(bg, str(yr), BW / 2, BH / 2, 1.0 + .03 * t)
        return C.grade(bg, sat=.6), False
    o = sh('pipeline.jpg', t - 1.55, d - 1.55, z=(1.05, 1.2), dz=(0, .35), tx=(-40, 30), focus=(.5, .5), blur=5)
    o = C.grade(arch(o, T, 3), sat=1.0)
    if t < 1.67: o = glitch(o, T, .7)
    return o, False
def O_texas(cv, T, t, d):
    if t > 1.55:
        s = 'न्यू लंदन, टेक्सस'; n = int(clamp((t - 1.7) * 22, 0, len(s)))
        if n: labelbox(cv, s[:n], 70, BY + 70, 1, 's8', 44)

def B_pipe(T, t, d):
    o, dd = G.shot3d('pipeline.jpg', clamp(t / d), z=(1.25, 1.42), dz=(.1, .4), tx=(-30, 30), focus=(.6, .6), blur=6, fx=.4)
    o = C.grade(arch(o, T, 6), sat=1.0); m = np.clip((dd - .35) * 3, 0, 1).astype(np.float32)
    return C.haze(o, T, m, amp=8), False
def O_pipe(cv, T, t, d):
    labelbox(cv, 'कच्ची गैस', 70, BY + 70, T - K['w_kachi'], 's8', 44, RED)
    labelbox(cv, 'बिना गंध', 70, BY + 150, T - K['w_bina'], 's8', 44)

def B_walls(T, t, d):
    u = t / d; o, dd = G.shot3d('kids.jpg', u, z=(1.0, 1.14), dz=(0, .35), focus=(.75, .5), blur=10)
    o = C.archive(o, T, seed=7) * .9 + 14
    yy = np.linspace(0, 1, BH, dtype=np.float32)[:, None].repeat(BW, 1)
    m = (np.clip((yy - lerp(1.05, -.15, ease(u))) / .3, 0, 1) * np.clip(1.1 - dd * .4, 0, 1)).astype(np.float32)
    o = C.haze(o, T, m, amp=13); o = o * (1 - .14 * m[..., None]) + np.array([150, 165, 120], np.float32) * .14 * m[..., None]
    return G.chroma(C.grade(o, sat=.85), 2) * (1 - .07 * math.exp(-((t % .85) * 9))), False
def O_walls(cv, T, t, d): pass

def B_clock(T, t, d):
    o = np.zeros((BH, BW, 3), np.float32) + np.array([168, 22, 24], np.float32)
    o = o * (1 - .35 * np.clip(np.abs(np.linspace(-1, 1, BW))[None, :, None] ** 2, 0, 1))
    sil = np.zeros((BH, BW, 3), np.float32); G.clock(sil, T, t, cx=540, cy=360, r=300)
    m = (sil.mean(2, keepdims=True) > 1).astype(np.float32); o = o * (1 - .28 * m) + o * .5 * .28 * m   # dark-red clock silhouette
    return o, False
def O_clock(cv, T, t, d):
    pop(cv, 'दोपहर', 's8', 46, CW / 2, BY + 150, t - .05, WHITE, .2, .3)
    for i, ch in enumerate('3:17'):
        pop(cv, ch, 'os', 230, CW / 2 + (i - 1.5) * 170, BY + BH / 2 + 30, T - (29.0 + i * .28), WHITE, .12, .4, 1.3)

def B_teacher(T, t, d):
    u = t / d; o = sh('switch.jpg', t, d, z=(1.05, 1.35), dz=(0, .35), focus=(.9, .9), blur=7)
    return C.grade(arch(o, T, 11)) * lerp(1, .8, u), False
def O_teacher(cv, T, t, d): pass

def B_spark(T, t, d):
    o = np.zeros((BH, BW, 3), np.float32) + 3; ts = K['w_spark'] - K['spark0']
    if t > ts - .15:
        r = np.random.default_rng(int(T * 60)); k = clamp((t - ts + .15) / .5)
        for _ in range(46):
            a = r.uniform(0, 6.28); s = r.uniform(5, 160) * k
            cv2.line(o, (540, 360), (int(540 + math.cos(a) * s), int(360 + math.sin(a) * s)), (255, 215, 150), 2, cv2.LINE_AA)
        o = C.bloom(o, 80, 2.2, 28)
    return o, False
def O_spark(cv, T, t, d): pass
def B_blast(T, t, d):
    img, dd = G.plate('ruins.jpg'); s_ = 34 * math.exp(-t * 4); r = np.random.default_rng(int(T * 90))
    o, _ = C.cam3d(img, dd, zoom=lerp(1.18, 1.04, eio(clamp(t / d))), dz=.15, tx=r.normal(0, s_), ty=r.normal(0, s_))
    o = C.grade(arch(o, T, 1), sat=.0, contrast=1.15)
    return glitch(o, T, .6) if t < .25 else o, False
def O_blast(cv, T, t, d): pass

COST_T = [tile(n, fx, .5, True) for n, fx in (('rescue.jpg', .2), ('ruins.jpg', .1), ('kids.jpg', .2), ('ruins.jpg', .9), ('rescue.jpg', .6),
                                              ('kids.jpg', .8), ('ruins.jpg', .5), ('rescue.jpg', .95), ('kids.jpg', .5))]
def B_cost(T, t, d):
    z = lerp(1.6, 1.0, eio(clamp(t / 1.6)))
    o = wall(COST_T, z, 8, 6) * .62
    kb = T - K['w_kids']
    if kb > 0: o = o * (1 - .35 * eio(kb / .3))
    return o, False
def O_cost(cv, T, t, d):
    kb = T - K['w_kids']; fb = 1 - eio(clamp(kb / .25)) if kb > 0 else 1
    if fb > 0: pop(cv, '300', 'os', 330, CW / 2, BY + BH / 2 - 10, t - .1, WHITE, .25, .7);
    if fb < 1 and fb > 0: pass
    if kb > 0: pop(cv, 'ज़्यादातर बच्चे', 't7', 190, CW / 2, BY + BH / 2 + 10, kb, RED, .2, .8)

def B_human(T, t, d):
    o = paper(BW, BH, 21, (240, 238, 233))
    ph = tile('kids.jpg', .45, .5, True, (520, 350)); ph = C.archive(ph.copy(), 0, sepia=False, seed=4) if False else ph
    s = lerp(1.0, 1.08, eio(clamp(t / d))); w, h = int(560 * s), int(390 * s)
    card = np.full((h, w, 3), 246, np.float32); card[16:h - 16, 16:w - 16] = cv2.resize(ph, (w - 32, h - 32))
    x0, y0 = BW // 2 - w // 2, BH // 2 - h // 2 - 20
    m = np.zeros((BH, BW), np.float32); m[y0:y0 + h, x0:x0 + w] = 1; shd = cv2.GaussianBlur(np.roll(m, 12, 0), (0, 0), 16)[..., None]
    o = o * (1 - .35 * shd); o[y0:y0 + h, x0:x0 + w] = card
    for (tx_, ty_, rot) in ((x0 - 20, y0 - 10, -30), (x0 + w - 90, y0 - 12, 28)):    # tape
        tp = np.zeros((BH, BW), np.uint8); box = cv2.boxPoints(((tx_ + 55, ty_ + 14), (130, 34), rot)); cv2.fillPoly(tp, [box.astype(np.int32)], 255)
        a = (tp / 255 * .55)[..., None]; o = o * (1 - a) + np.array([232, 226, 200], np.float32) * a
    return o, True
def O_human(cv, T, t, d): pass

DOC2 = [('टेक्सस  ·  1937', 's8', 50, (120, 40, 36)), ('नया कानून :', 'r7', 70, INK), ('हर गैस में', 'r7', 70, INK), ('तेज़ गंध मिलाना', 'r7', 70, INK), ('ज़रूरी होगा।', 'r7', 70, INK)]
def B_law(T, t, d):
    bg = paper(BW, BH, 30, (60, 58, 56)) * .6
    hk = clamp((T - 45.15) / .7); pg = page(DOC2, 1100, 820, 9, hl=(3, 4), hk=hk, top=60, lead=140)
    return warp_page(bg, pg, T, t, tilt=(-.05, 0), push=(1.0, 1.1)), False
def O_law(cv, T, t, d): pass
def B_voice(T, t, d):
    o = sh('odorant.jpg', t, d, z=(1.12, 1.0), dz=(.25, 0), tx=(20, -20), focus=(.6, .85), blur=12)
    col = C.grade(C.bloom(o, 190, .4)); bw = C.archive(o, T, seed=17, sepia=False)
    k = eio(clamp(t / .9)); return bw * (1 - k) + col * k, False
def O_voice(cv, T, t, d): pass

def B_today(T, t, d):
    o = sh('cylinder.jpg', t, d, z=(1.0, 1.14), dz=(0, .3), tx=(-20, 20), focus=(.85, .85), blur=14, fy=.35)
    o = C.bloom(o, 190, .4); o = G.wisps(o, T, 540, 690, alpha=.4, spread=.6); o = C.grade(o)
    return o * (1 - .35 * eio(clamp((T - K['w_ethyl'] + .1) / .3))), False
def O_today(cv, T, t, d):
    te = T - K['w_ethyl'] + .05
    labelbox(cv, 'एथिल', 150, BY + BH / 2 - 50, te, 's9', 96)
    labelbox(cv, 'मरकैप्टन', 150, BY + BH / 2 + 70, te - .3, 's9', 96)
    if te > .7: put(cv, tx('ETHYL MERCAPTAN  ·  C₂H₅SH' if False else 'ETHYL MERCAPTAN', 's6', 30, (230, 230, 230)), 150, BY + BH / 2 + 165, eio((te - .7) / .3), 'l', .7)

def B_rules(T, t, d): return C.grade(sh('kitchen.jpg', t, d, z=(1.1, 1.14), focus=(.05, .05), blur=26)) * .5, False
def O_rules(cv, T, t, d):
    pop(cv, 'बदबू आए तो —', 's8', 48, 70 + 200, BY + 80, t - .1, WHITE, .2, .5)
    for i, (txt, key) in enumerate((('स्विच मत छूना', 'r1'), ('रेगुलेटर बंद करो', 'r2'), ('खिड़कियाँ खोलो', 'r3'))):
        tt = T - K[key] + .15; y = BY + 250 + i * 150
        if tt > 0: put(cv, tx(f'0{i + 1}', 'os', 46, WHITE), 80, y, eio(tt / .3), 'l', 0)
        labelbox(cv, txt, 175, y, tt, 's8', 54, RED)

def B_end(T, t, d):
    u = t / d; tm = K['w_main'] - K['s_end']
    o = sh('kettle.jpg', t, d, z=(1.0, 1.1), dz=(0, .25), focus=(.8, .8), blur=14)
    o = C.bloom(o, 170, .6); o = G.wisps(o, T, 540, 700, (255, 200, 120), alpha=.4, spread=.6)
    o = C.grade(o, shadows=(0.9, 1.0, 1.15), highs=(1.12, 1.0, .82))
    return o * (1 - .6 * eio(clamp((t - tm + .4) / .6))), False
def O_end(cv, T, t, d):
    tm = K['w_main'] - .35
    pop(cv, 'आपको', 's8', 64, CW / 2, BY + BH / 2 - 150, T - 59.2, WHITE, .2, .6)
    pop(cv, 'बचाने के लिए', 't7', 210, CW / 2, BY + BH / 2 + 20, T - tm, WHITE, .3, .7)
    if T > 60.9: put(cv, tx('FreshNestHub', 's8', 34, (200, 200, 200)), CW / 2, BY + BH + 70, eio((T - 60.9) / .4), 'c', 0)

def build():
    k = K; S = []
    def seg(a, b, nm, tr): S.append((a, b, globals()['B_' + nm], globals()['O_' + nm], tr))
    seg(0, k['s_kitchen'], 'open', None); seg(k['s_kitchen'], k['s_odorless'], 'kitchen', 'cut')
    seg(k['s_odorless'], k['s_added'], 'odorless', 'push'); seg(k['s_added'], k['s_ruins'], 'added', 'blur')
    seg(k['s_ruins'], k['s_texas'], 'ruins', 'glitch'); seg(k['s_texas'], k['s_pipe'], 'texas', 'cut'); seg(k['s_pipe'], k['s_walls'], 'pipe', 'push')
    seg(k['s_walls'], k['s_clock'], 'walls', 'blur'); seg(k['s_clock'], k['w_teacher'], 'clock', 'glitch'); seg(k['w_teacher'], k['spark0'], 'teacher', 'push')
    seg(k['spark0'], k['s_blast'], 'spark', 'cut'); seg(k['s_blast'], k['s_cost'], 'blast', 'cut'); seg(k['s_cost'], k['s_human'], 'cost', 'glitch')
    seg(k['s_human'], k['s_voice'], 'human', 'blur'); seg(k['s_voice'], 46.85, 'law', 'push'); seg(46.85, k['s_today'], 'voice', 'blur')
    seg(k['s_today'], k['s_rules'], 'today', 'push'); seg(k['s_rules'], k['s_end'], 'rules', 'blur'); seg(k['s_end'], TOTAL, 'end', 'blur')
    return S
SHOTS = build()
CAP_OFF += [(0, 3.0), (3.4, 4.6), (4.6, 7.98), (8.7, 10.1), (12.9, 15.0), (15.0, 16.55), (28.9, K['w_teacher']), (K['s_cost'], K['s_human']),
            (K['s_voice'], 46.85), (K['w_ethyl'] - .1, K['s_rules']), (K['s_rules'], K['s_end']), (59.1, TOTAL)]

BG = np.full((CH, CW, 3), 5, np.float32)
def band_at(i, T):
    a, b, fn, _, _ = SHOTS[i]; return fn(T, T - a, b - a)[0]
def frame(T):
    for i, (a, b, fn, ov, tr) in enumerate(SHOTS):
        if a <= T < b or i == len(SHOTS) - 1: break
    t, d = T - a, b - a
    o, dark = fn(T, t, d)
    if i > 0 and tr == 'blur' and t < .3:
        prev = band_at(i - 1, T); kk = eio(t / .3)
        o = cv2.GaussianBlur(prev, (0, 0), 1 + 28 * kk) * (1 - kk) + cv2.GaussianBlur(o, (0, 0), 1 + 28 * (1 - kk)) * kk
    elif i > 0 and tr == 'push' and t < .28:
        prev = band_at(i - 1, T); kk = eio(t / .28); s = math.sin(math.pi * kk); sh_ = int(BW * kk)
        both = np.concatenate([prev, o], 1)[:, sh_:sh_ + BW]
        o = cv2.blur(both, (int(1 + 70 * s), 1)) if s > .05 else both
    elif i > 0 and tr == 'glitch' and t < .14:
        o = glitch(o if t > .07 else band_at(i - 1, T), T, 1.0)
    if fn is B_blast: o = o * (1 - math.exp(-t * 7)) + 255 * math.exp(-t * 7)
    band = C.finish(o, T, grain=5, vig=not dark).astype(np.float32)
    cv = BG.copy(); cv[BY:BY + BH] = band
    ov(cv, T, t, d)
    caption(cv, T, dark)
    if fn is B_blast: fl = math.exp(-t * 6); cv = cv * (1 - fl) + 255 * fl
    return np.clip(cv, 0, 255).astype(np.uint8)

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for s in sys.argv[2:]: Image.fromarray(frame(float(s))).save(f'/tmp/g3_{s}.jpg', quality=88)
    else:
        a, b = float(sys.argv[2]), float(sys.argv[3]); os.makedirs(P + '/segs3', exist_ok=True); out = f'{P}/segs3/seg_{a:05.1f}.mp4'
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{CW}x{CH}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', out + '.tmp.mp4'], stdin=subprocess.PIPE)
        for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(frame(n / FPS).tobytes())
        p.stdin.close(); p.wait(); os.replace(out + '.tmp.mp4', out)
