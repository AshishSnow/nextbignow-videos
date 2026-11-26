#!/usr/bin/env python3
"""गैस की बदबू (v3) — premium doc short.
Look: every still is a real 3D camera move (AI depth) with rack focus, bloom, haze; archive film for 1937;
anchored-word montage + black text cards (Apple-style reference); red '//' labels + chromatic edges (founder-reel reference).
usage: gas.py stills t.. | seg a b"""
import sys, os, json, math, subprocess
sys.path.insert(0, '/home/claude/studio/tools')
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cine as C
from cine import W, H, ease, eio

P = os.path.dirname(os.path.abspath(__file__)); A = '/home/claude/studio/assets/70/'
K = json.load(open(P + '/work/keys.json')); TOTAL = K['total']
FPS = 30
FD = '/home/claude/studio/fonts/doc/'
F_SERIF = FD + 'pkg_fontsource-noto-serif-devanagari-5.3.0/files/noto-serif-devanagari-devanagari-700-normal.woff'
F_SERIF_R = FD + 'pkg_fontsource-tiro-devanagari-hindi-5.3.0/files/tiro-devanagari-hindi-devanagari-400-normal.woff'
F_LAT = FD + 'pkg_fontsource-playfair-display-5.3.0/files/playfair-display-latin-700-normal.woff'
F_CAP = '/home/claude/studio/fonts/hi/mukta-700.ttf'
F_TYPE = '/home/claude/studio/fonts/comic/SpecialElite-Regular.ttf'
F_SANS = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
_F = {}
def font(p, s):
    if (p, s) not in _F: _F[(p, s)] = ImageFont.truetype(p, s, layout_engine=ImageFont.Layout.RAQM)
    return _F[(p, s)]
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def lerp(a, b, u): return a + (b - a) * u

_IMG = {}
def plate(name, fx=.5, fy=.5, pad=1.2):
    k = (name, fx, fy, pad)
    if k not in _IMG: _IMG[k] = C.cover(A + name, fx=fx, fy=fy, pad=pad)
    return _IMG[k]
def shot3d(name, u, z=(1.0, 1.0), dz=(0, .2), tx=(0, 0), ty=(0, 0), focus=(.8, .8), blur=12, fx=.5, fy=.5, pad=1.2):
    img, d = plate(name, fx, fy, pad); e = eio(u)
    o, dd = C.cam3d(img, d, zoom=lerp(*z, e), dz=lerp(*dz, e), tx=lerp(*tx, e), ty=lerp(*ty, e))
    if blur: o = C.dof(o, dd, focus=lerp(*focus, e), strength=blur)
    return o, dd

# ---------- text
def text_layer(txt, fp, size, fill=(255, 255, 255, 255)):
    if fp.endswith('.woff') and 'devanagari-' in fp and any(c.isascii() and not c.isspace() for c in txt): fp = F_CAP   # subset font lacks digits/?
    f = font(fp, size); bb = f.getbbox(txt)
    im = Image.new('RGBA', (bb[2] - bb[0] + 40, bb[3] - bb[1] + 40), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((20 - bb[0], 20 - bb[1]), txt, font=f, fill=fill); return im
def put(arr, im, cx, cy, a=1.0, shadow=True, blur_in=0.0):
    if a <= 0: return
    if blur_in > .01: im = im.filter(ImageFilter.GaussianBlur(blur_in))
    x0, y0 = int(cx - im.width / 2), int(cy - im.height / 2)
    def comp(src, ox, oy, am, col=None):
        h, w = src.shape[:2]; xa, ya = max(0, ox), max(0, oy); xb, yb = min(W, ox + w), min(H, oy + h)
        if xb <= xa or yb <= ya: return
        s = src[ya - oy:yb - oy, xa - ox:xb - ox]; al = s[..., 3:4] / 255 * am
        rgb = s[..., :3] if col is None else np.array(col, np.float32)
        arr[ya:yb, xa:xb] = arr[ya:yb, xa:xb] * (1 - al) + rgb * al
    if shadow: comp(np.asarray(im.filter(ImageFilter.GaussianBlur(12))).astype(np.float32), x0 + 2, y0 + 6, a * .8, (0, 0, 0))
    comp(np.asarray(im).astype(np.float32), x0, y0, a)
def reveal(arr, txt, fp, size, cx, cy, t, col=(255, 255, 255), dur=.5, rise=26):
    if t <= 0: return
    k = eio(t / dur); put(arr, text_layer(txt, fp, size, col + (255,)), cx, cy + rise * (1 - k), k, True, 16 * (1 - k))
def typewriter(arr, txt, cx, cy, t, size=54, col=(240, 230, 210), cps=20, fp=None):
    n = int(clamp(t * cps, 0, len(txt)))
    if n: put(arr, text_layer(txt[:n], fp or F_TYPE, size, col + (255,)), cx, cy, 1.0)
def label(arr, txt, x, y, t, col=(225, 35, 35)):
    """founder-reel style: small red text + '//' typed on"""
    if t <= 0: return
    s = txt + ' //'; n = int(clamp(t * 26, 0, len(s)))
    if n: put(arr, text_layer(s[:n], F_CAP, 54, col + (255,)), x + 60, y, 1.0, True)
def card(T, t, txt, d, size=58):
    """Apple-style: black frame, small centred white line, focus-in"""
    o = np.zeros((H, W, 3), np.float32) + 4
    reveal(o, txt, F_CAP, size, W / 2, 960, t, (240, 240, 240), .45, 0)
    return o

def handles(arr, cx, cy, w, h, t, col=(235, 235, 235)):
    if t <= 0: return
    k = eio(t / .3); w, h = w * (0.9 + .1 * k), h * (0.9 + .1 * k)
    x0, y0, x1, y1 = int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2)
    c = tuple(int(v * k) for v in col)
    for x in range(x0, x1, 18): cv2.line(arr, (x, y0), (min(x + 9, x1), y0), c, 2); cv2.line(arr, (x, y1), (min(x + 9, x1), y1), c, 2)
    for y in range(y0, y1, 18): cv2.line(arr, (x0, y), (x0, min(y + 9, y1)), c, 2); cv2.line(arr, (x1, y), (x1, min(y + 9, y1)), c, 2)
    for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)): cv2.rectangle(arr, (x - 9, y - 9), (x + 9, y + 9), c, -1)

# ---------- caption: tiny, centred, phrase-level (reference style)
WORDS = json.load(open(P + '/work/words.json'))   # [start, end, word]
def caption(arr, T):
    cur = [w for w in WORDS if w[0] <= T < w[1] + .3]
    if not cur: return
    i = WORDS.index(cur[-1]); grp = [g for g in WORDS[max(0, i - 2):i + 1] if T - g[0] < 1.3]
    put(arr, text_layer(' '.join(g[2] for g in grp), F_SERIF_R, 54, (255, 255, 255, 255)), W / 2, 1330, 1.0, True)

# ---------- looks
def chroma(o, amt=4):
    o = o.copy(); o[..., 0] = np.roll(o[..., 0], amt, 1); o[..., 2] = np.roll(o[..., 2], -amt, 1); return o
_HT = None
def screen_tex(o, a=.10):
    """fine halftone / screen texture (founder reel)"""
    global _HT
    if _HT is None:
        yy, xx = np.mgrid[0:H, 0:W]; _HT = ((np.sin(xx * .9) * np.sin(yy * .9)) * .5 + .5).astype(np.float32)[..., None]
    return o * (1 - a) + o * _HT * a * 2 * .5 + o * a * .5
def wisps(arr, T, ox, oy, col=(190, 220, 90), alpha=.5, spread=1.0, n=7, seed=5):
    if alpha <= 0.01: return arr
    r = np.random.default_rng(seed); layer = np.zeros((H // 4, W // 4), np.float32)
    for i in range(n):
        ph = r.random() * 6.28; sp = .6 + r.random() * .6; pts = []
        for k in range(28):
            s = k / 27; pts.append(((ox + math.sin(s * 5 + T * sp * 2 + ph) * 130 * s * spread + (r.random() - .5) * 16) / 4, (oy - s * 900 * spread) / 4))
        for k in range(27):
            cv2.line(layer, (int(pts[k][0]), int(pts[k][1])), (int(pts[k + 1][0]), int(pts[k + 1][1])), float(1 - k / 28), max(1, int((1 - k / 28) * 6 + 2)), cv2.LINE_AA)
    layer = cv2.resize(cv2.GaussianBlur(layer, (0, 0), 3), (W, H), interpolation=cv2.INTER_CUBIC)[..., None]
    return arr * (1 - layer * alpha * .35) + layer * np.array(col, np.float32) * alpha
def clock(arr, T, t, cx=540, cy=860, r=300):
    im = Image.new('RGBA', (2 * r + 40, 2 * r + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = r + 20
    d.ellipse((20, 20, 2 * r + 20, 2 * r + 20), fill=(236, 228, 210, 255), outline=(40, 34, 28, 255), width=14)
    for k in range(60):
        a = k / 60 * 2 * math.pi; l = 30 if k % 5 == 0 else 12
        d.line((c + math.sin(a) * (r - 20), c - math.cos(a) * (r - 20), c + math.sin(a) * (r - 20 - l), c - math.cos(a) * (r - 20 - l)), fill=(40, 34, 28, 255), width=6 if k % 5 == 0 else 2)
    m = min(17.0, 14 + int(t / .35))                                   # minute hand ticks 14 -> 17
    ha = (3 + m / 60) / 12 * 2 * math.pi; ma = m / 60 * 2 * math.pi; sa = (int(t * 4) / 60) * 2 * math.pi * 4
    d.line((c, c, c + math.sin(ha) * r * .5, c - math.cos(ha) * r * .5), fill=(30, 26, 22, 255), width=16)
    d.line((c, c, c + math.sin(ma) * r * .78, c - math.cos(ma) * r * .78), fill=(30, 26, 22, 255), width=10)
    d.line((c, c, c + math.sin(sa) * r * .85, c - math.cos(sa) * r * .85), fill=(170, 30, 30, 255), width=4)
    d.ellipse((c - 16, c - 16, c + 16, c + 16), fill=(30, 26, 22, 255)); put(arr, im, cx, cy, 1.0, True)

def arch(o, T, seed=0): return chroma(C.archive(o, T, seed=seed), 3)

# ================== SHOTS (all times from keys.json) ==================
MONT = K.get('montage', ['milk.jpg', 'egg.jpg', 'smoke.jpg', 'kettle.jpg'])
def S_open(T, t, d):            # anchored word montage: बदबू stays, pictures change every ~0.4 s
    i = min(len(MONT) - 1, int(t / max(.35, d / len(MONT)))); nm = MONT[i]
    o, dd = shot3d(nm, clamp(t / d), z=(1.06, 1.14), dz=(0, .2), focus=(.85, .85), blur=10)
    o = C.grade(o, sat=.75) * .72; o = screen_tex(chroma(o, 3), .12)
    put(o, text_layer('बदबू', F_SERIF, 170, (255, 255, 255, 255)), W / 2, 900, 1.0, True)
    handles(o, W / 2, 905, 480, 260, t - .15)
    return o
def S_kitchen(T, t, d):          # पर रसोई गैस की ये बदबू — असली नहीं है
    u = t / d; tn = K['w_nahi'] - K['s_kitchen']
    o, dd = shot3d('kitchen.jpg', u, z=(1.0, 1.12), dz=(0, .3), tx=(0, -30), focus=(.85, .95), blur=9)
    o = C.bloom(o, 180, .45)
    o = wisps(o, T, 560, 1150, alpha=.55 if t < tn else .55 * clamp(1 - (t - tn) / .25))
    if t > tn: o = chroma(o, int(10 * math.exp(-(t - tn) * 8)))
    o = C.grade(o, (0.9, 1.0, 1.15), (1.1, 1.0, .85))
    reveal(o, 'असली नहीं।', F_SERIF, 92, W / 2, 560, t - tn)
    return o
def S_added(T, t, d):            # ये डाली जाती है
    u = t / d
    o, dd = shot3d('flame.jpg', u, z=(1.0, 1.15), dz=(0, .25), focus=(.9, .9), blur=10)
    o = C.bloom(o, 150, .8, 40, (.7, .9, 1.2)); o = C.grade(o, (0.85, 1.0, 1.2), (1.05, 1.0, .9))
    label(o, 'डाली जाती है', 150, 520, t - .1)
    return o
def S_silent(T, t, d): return card(T, t, 'क्योंकि एक दिन… गैस चुप थी।', d)
def S_blast(T, t, d):            # और एक पूरा स्कूल उड़ गया — white flash + shake into the ruins
    img, dd = plate('ruins.jpg'); tb = t; sh = 34 * math.exp(-tb * 4); r = np.random.default_rng(int(T * 90))
    o, _ = C.cam3d(img, dd, zoom=lerp(1.18, 1.04, eio(clamp(tb / d))), dz=.15, tx=r.normal(0, sh), ty=r.normal(0, sh))
    o = arch(o, T, 1); o = C.grade(o, sat=.0, contrast=1.15)
    fl = math.exp(-tb * 7); return o * (1 - fl) + 255 * fl
def S_texas(T, t, d):            # 1937, टेक्सस … कच्ची गैस जोड़ ली
    u = t / d
    o, dd = shot3d('pipeline.jpg', u, z=(1.05, 1.2), dz=(0, .35), tx=(-40, 30), focus=(.9, .6), blur=14)
    fb = 1 - eio(clamp((t - 1.0) / .5))                      # background blurred while the year is on screen
    if fb > .01: o = cv2.GaussianBlur(o, (0, 0), 1 + 22 * fb) * fb + o * (1 - fb)
    o = arch(o, T, 3); o = C.grade(o, sat=1.0)
    put(o, text_layer('1937', F_LAT, 260, (245, 238, 225, 255)), W / 2, 820, fb, True, 10 * (1 - eio(clamp(t / .3))))
    typewriter(o, 'न्यू लंदन, टेक्सस', W / 2, 520, t - 1.1, 54, fp=F_CAP)
    return o
def S_walls(T, t, d):            # वो दीवारों में भरती रही… किसी ने सूंघी नहीं। किसी ने देखी नहीं।
    u = t / d
    o, dd = shot3d('kids.jpg', u, z=(1.0, 1.14), dz=(0, .35), focus=(.75, .5), blur=12)
    o = C.archive(o, T, seed=7)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None].repeat(W, 1)
    m = (np.clip((yy - lerp(1.05, -.15, ease(u))) / .3, 0, 1) * np.clip(1.1 - dd * .4, 0, 1)).astype(np.float32)
    o = C.haze(o, T, m, amp=13); o = o * (1 - .14 * m[..., None]) + np.array([150, 165, 120], np.float32) * .14 * m[..., None]
    o = o * (1 - .07 * math.exp(-((t % .85) * 9)))     # heartbeat breathing
    return chroma(C.grade(o, sat=.85), 2)
def S_clock(T, t, d):            # तीन बजकर सत्रह मिनट
    o, dd = shot3d('kids.jpg', .5, z=(1.35, 1.35), focus=(.1, .1), blur=24, fx=.6)
    o = C.archive(o, T, seed=9) * .45; clock(o, T, t)
    reveal(o, '3:17', F_LAT, 96, W / 2, 1250, t - .9, (240, 230, 210)); return o
def S_teacher(T, t, d):          # एक टीचर। एक स्विच।
    u = t / d; ts = K['w_switch'] - K['w_teacher']
    o, dd = shot3d('switch.jpg', u, z=(1.05, 1.35), dz=(0, .35), focus=(.95, .95), blur=18)
    o = arch(o, T, 11); o = C.grade(o) * lerp(1, .8, u)
    label(o, 'एक टीचर', 150, 560, t - .05); label(o, 'एक स्विच', 150, 640, t - ts)
    return o
def S_spark(T, t, d):            # … एक चिंगारी — black, one spark, silence
    o = np.zeros((H, W, 3), np.float32) + 3
    ts = K['w_spark'] - K['spark0']
    if t > ts - .15:
        r = np.random.default_rng(int(T * 60)); k = clamp((t - ts + .15) / .5)
        for _ in range(46):
            a = r.uniform(0, 6.28); s = r.uniform(5, 160) * k
            cv2.line(o, (540, 960), (int(540 + math.cos(a) * s), int(960 + math.sin(a) * s)), (255, 215, 150), 2, cv2.LINE_AA)
        o = C.bloom(o, 80, 2.2, 28)
    return o
def S_cost(T, t, d):             # करीब तीन सौ लोग। ज़्यादातर बच्चे।
    u = t / d
    o, dd = shot3d('rescue.jpg', u, z=(1.02, 1.12), dz=(0, .25), tx=(30, -30), focus=(.55, .8), blur=10)
    o = C.archive(o, T, seed=15) * .78; o = C.dust(o, T, 60, alpha=.28); o = C.grade(o, sat=0)
    fb = clamp(1 - (T - K['w_kids']) / .6) if T > K['w_kids'] else 1.0
    o = cv2.GaussianBlur(o, (0, 0), 18) * fb + o * (1 - fb)
    reveal(o, '300', F_LAT, 300, W / 2, 760, t - .1, (245, 240, 230))
    reveal(o, 'लोग', F_CAP, 60, W / 2, 960, t - .35, (230, 225, 215))
    reveal(o, 'ज़्यादातर बच्चे', F_SERIF_R, 72, W / 2, 1100, T - K['w_kids'], (235, 90, 80))
    return o
def S_voice(T, t, d):            # गैस को आवाज़ दी गई — archive B&W blooms into colour
    u = t / d
    o, dd = shot3d('odorant.jpg', u, z=(1.12, 1.0), dz=(.25, 0), tx=(20, -20), focus=(.6, .85), blur=12)
    col = C.grade(C.bloom(o, 190, .4)); bw = C.archive(o, T, seed=17, sepia=False)
    k = eio(clamp((T - K['w_awaaz']) / 1.2)); o = bw * (1 - k) + col * k
    label(o, 'कानून: गैस में बदबू', 150, 520, T - K['w_awaaz'], (235, 60, 50))
    return o
def S_today(T, t, d):            # आज आपके सिलेंडर में भी वही है। एथिल मरकैप्टन।
    u = t / d
    o, dd = shot3d('cylinder.jpg', u, z=(1.0, 1.14), dz=(0, .3), tx=(-20, 20), focus=(.85, .85), blur=14)
    o = C.bloom(o, 190, .4); o = wisps(o, T, 540, 1100, alpha=.45, spread=.9); o = C.grade(o)
    label(o, 'एथिल मरकैप्टन', 150, 520, T - K['w_ethyl'], (60, 200, 110))
    return o
def S_rules(T, t, d):            # बदबू आए? स्विच — मत छूना। रेगुलेटर — बंद। खिड़कियाँ — खुली।
    o, dd = shot3d('kitchen.jpg', t / d, z=(1.1, 1.14), focus=(.05, .05), blur=26)
    o = C.grade(o) * .62
    reveal(o, 'बदबू आए?', F_SERIF, 84, W / 2, 520, t - .05)
    for i, (txt, key) in enumerate((('स्विच — मत छूना', 'r1'), ('रेगुलेटर — बंद', 'r2'), ('खिड़कियाँ — खुली', 'r3'))):
        tt = T - K[key]
        if tt <= 0: continue
        k = eio(tt / .35); y = 760 + i * 190
        x0, x1, y0, y1 = int(W / 2 - 400), int(W / 2 + 400), int(y - 70), int(y + 70)
        o[y0:y1, x0:x1] = cv2.GaussianBlur(o[y0:y1, x0:x1], (0, 0), 16) * k + o[y0:y1, x0:x1] * (1 - k) + 22 * k
        cd = Image.new('RGBA', (800, 140), (0, 0, 0, 0)); g = ImageDraw.Draw(cd)
        g.rounded_rectangle((0, 0, 799, 139), 34, outline=(255, 255, 255, 110), width=2)
        g.text((48, 30), txt, font=font(F_CAP, 60), fill=(255, 255, 255, 255))
        put(o, cd, W / 2 + 70 * (1 - k), y, k, False)
    return o
def S_end(T, t, d):              # हर बदबू कुछ कहती है। ये वाली कहती है… मैं यहाँ हूँ।
    u = t / d; tm = K['w_main'] - K['s_end']
    o, dd = shot3d('kettle.jpg', u, z=(1.0, 1.1), dz=(0, .25), focus=(.8, .8), blur=14)
    o = C.bloom(o, 170, .6); o = wisps(o, T, 540, 1250, (255, 200, 120), alpha=.4); o = C.grade(o, (0.9, 1.0, 1.15), (1.12, 1.0, .82))
    o = o * (1 - .55 * eio(clamp((t - tm) / .6)))
    reveal(o, 'आपको बचाने के लिए।', F_SERIF, 92, W / 2, 900, t - tm)
    return o

def S_odorless(T, t, d):         # आपके सिलेंडर की गैस में… कोई गंध होती ही नहीं (clear, invisible shimmer, no wisps)
    u = t / d
    o, dd = shot3d('cylinder.jpg', u, z=(1.0, 1.1), dz=(0, .3), tx=(20, -20), focus=(.85, .85), blur=12, fy=.3)
    m = np.clip((dd - .2) * 1.5, 0, 1).astype(np.float32); o = C.haze(o, T, m, amp=9)
    o = C.grade(o, (0.9, 1.0, 1.12), (1.05, 1.0, .9))
    label(o, 'गंध: शून्य', 150, 520, T - 6.1, (240, 240, 240))
    return o
def S_ruinsq(T, t, d):           # अमेरिका के इतिहास का सबसे भयानक स्कूल हादसा (quiet, archival)
    u = t / d
    o, dd = shot3d('ruins.jpg', u, z=(1.0, 1.12), dz=(0, .3), tx=(25, -25), focus=(.5, .8), blur=10)
    o = arch(o, T, 5); o = C.grade(o, sat=0, contrast=1.1) * .85
    reveal(o, 'सबसे भयानक', F_SERIF, 96, W / 2, 520, T - K['w_worst'], (245, 240, 230))
    reveal(o, 'स्कूल हादसा', F_SERIF_R, 70, W / 2, 640, T - K['w_worst'] - .35, (235, 90, 80))
    return o
def S_pipe2(T, t, d):            # पास की पाइपलाइन से कच्ची गैस … बिना किसी गंध वाली गैस
    u = t / d
    o, dd = shot3d('pipeline.jpg', u, z=(1.25, 1.42), dz=(.1, .4), tx=(-30, 30), focus=(.9, .9), blur=14, fx=.4)
    o = arch(o, T, 6); o = C.grade(o, sat=1.0)
    m = np.clip((dd - .35) * 3, 0, 1).astype(np.float32); o = C.haze(o, T, m, amp=8)
    label(o, 'कच्ची गैस', 150, 520, T - K['w_kachi']); label(o, 'बिना गंध', 150, 600, T - K['w_bina'])
    return o
def S_human(T, t, d):            # सच कहूँ… (honest beat: children's faces, slow, near-silent)
    u = t / d
    o, dd = shot3d('kids.jpg', u, z=(1.12, 1.2), dz=(0, .15), focus=(.8, .8), blur=10, fx=.45)
    o = C.archive(o, T, seed=21) * lerp(.75, .55, u); return C.grade(o, sat=0)
def build():
    k = K; S = []
    def seg(a, b, fn, tr): S.append((a, b, fn, tr))
    seg(0, k['s_kitchen'], S_open, None); seg(k['s_kitchen'], k['s_odorless'], S_kitchen, 'cut')
    seg(k['s_odorless'], k['s_added'], S_odorless, 'blur'); seg(k['s_added'], k['s_ruins'], S_added, 'blur')
    seg(k['s_ruins'], k['s_texas'], S_ruinsq, 'flash'); seg(k['s_texas'], k['s_pipe'], S_texas, 'blur'); seg(k['s_pipe'], k['s_walls'], S_pipe2, 'cut')
    seg(k['s_walls'], k['s_clock'], S_walls, 'blur'); seg(k['s_clock'], k['w_teacher'], S_clock, 'cut'); seg(k['w_teacher'], k['spark0'], S_teacher, 'cut')
    seg(k['spark0'], k['s_blast'], S_spark, 'cut'); seg(k['s_blast'], k['s_cost'], S_blast, 'cut'); seg(k['s_cost'], k['s_human'], S_cost, 'blur')
    seg(k['s_human'], k['s_voice'], S_human, 'blur'); seg(k['s_voice'], k['s_today'], S_voice, 'blur'); seg(k['s_today'], k['s_rules'], S_today, 'blur')
    seg(k['s_rules'], k['s_end'], S_rules, 'blur'); seg(k['s_end'], TOTAL, S_end, 'blur')
    return S
SHOTS = build()
NOCAP = {S_open, S_rules, S_spark}

def frame(T):
    for i, (a, b, fn, tr) in enumerate(SHOTS):
        if a <= T < b or i == len(SHOTS) - 1: break
    t, d = T - a, b - a
    o = fn(T, t, d)
    if tr == 'blur' and t < .35 and i > 0:
        pa, pb, pfn, _ = SHOTS[i - 1]; prev = pfn(T, T - pa, pb - pa); kk = eio(t / .35)
        o = cv2.GaussianBlur(prev, (0, 0), 1 + 30 * kk) * (1 - kk) + cv2.GaussianBlur(o, (0, 0), 1 + 30 * (1 - kk)) * kk
    elif tr == 'flash' and t < .1: o = o * (t / .1) + 255 * (1 - t / .1)
    if fn not in NOCAP: caption(o, T)
    return C.finish(o, T, grain=6, vig=fn not in (S_silent,))

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for s in sys.argv[2:]: Image.fromarray(frame(float(s))).save(f'/tmp/gs_{s}.png')
    else:
        a, b = float(sys.argv[2]), float(sys.argv[3]); os.makedirs(P + '/segs', exist_ok=True); out = f'{P}/segs/seg_{a:05.1f}.mp4'
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', out + '.tmp.mp4'], stdin=subprocess.PIPE)
        for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(frame(n / FPS).tobytes())
        p.stdin.close(); p.wait(); os.replace(out + '.tmp.mp4', out)
