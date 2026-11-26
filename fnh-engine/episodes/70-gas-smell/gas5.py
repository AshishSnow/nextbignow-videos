#!/usr/bin/env python3
"""गैस की बदबू — v5.
 - unique Hindi type system: Rozha One poster words (grain fill + red echo), Sarpanch for danger/numbers,
   Khand for labels/captions, Kalam handwritten notes
 - no white paper: spec & law scenes rebuilt as dark posters with scrolling red ribbons + rubber stamp
 - 3 s beat-synced cold open on 'The Business' + song returns for the 'today' section and the brand card
usage: gas5.py stills t.. | seg a b"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['CINE_W'] = '1000'; os.environ['CINE_H'] = '750'
sys.path.insert(0, '/home/claude/studio/tools')
import cine
import math, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import gas3 as V
FD = '/home/claude/studio/fonts/doc/'
FF = {'roz': FD + 'd_rozha-one.ttf', 'sarp': FD + 'd_sarpanch.ttf', 'khand': FD + 'd_khand.ttf', 'kalam': FD + 'd_kalam.ttf', 'eczar': FD + 'd_eczar.ttf'}
_F = {}
def fnt(k, s):
    if (k, s) not in _F: _F[(k, s)] = ImageFont.truetype(FF[k], s, layout_engine=ImageFont.Layout.RAQM)
    return _F[(k, s)]
_GR = np.random.default_rng(5).normal(0, 1, (900, 2400)).astype(np.float32)
def styled(txt, key, size, style, col=(255, 255, 255), maxw=980):
    """RGBA type with treatment. style: poster | danger | label | note | plain"""
    f = fnt(key, size); bb = f.getbbox(txt, stroke_width=6)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    if w > maxw and size > 20: return styled(txt, key, int(size * maxw / w), style, col, maxw)
    pad = 20 if style in ('plain', 'note') else 50; W_, H_ = w + pad * 2, h + pad * 2
    def mask(stroke=0):
        m = Image.new('L', (W_, H_), 0); ImageDraw.Draw(m).text((pad - bb[0], pad - bb[1]), txt, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
        return np.asarray(m).astype(np.float32) / 255
    out = np.zeros((H_, W_, 4), np.float32)
    def lay(m, rgb, a=1.0, dx=0, dy=0):
        m = np.roll(np.roll(m, dy, 0), dx, 1) * a
        out[..., :3] = out[..., :3] * (1 - m[..., None]) + np.array(rgb, np.float32) * m[..., None]
        out[..., 3] = np.maximum(out[..., 3], m)
    if style == 'poster':                       # red echo trail + grain-textured white face
        m = mask(); e = max(2, size // 40)
        for i, a in ((4, .35), (3, .55), (2, .8), (1, 1.0)): lay(m, (200, 28, 30), a, e * i, e * i)
        lay(mask(max(1, size // 70)), (14, 10, 10), 1.0)
        g = _GR[:H_, :W_] if H_ <= 900 and W_ <= 2400 else 0
        face = np.clip(np.array(col, np.float32)[None, None] * (0.93 + 0.07 * np.tanh(g)[..., None] if np.ndim(g) else 1), 0, 255)
        out[..., :3] = out[..., :3] * (1 - m[..., None]) + face * m[..., None]; out[..., 3] = np.maximum(out[..., 3], m)
    elif style == 'danger':                      # red fill, white keyline, hard black drop
        st = max(3, size // 28); lay(mask(st), (0, 0, 0), .9, st, st); lay(mask(st), (255, 255, 255)); lay(mask(), col if col != (255, 255, 255) else (226, 36, 36))
    elif style == 'note':
        lay(mask(), (0, 0, 0), .6, 3, 4); lay(mask(), col)
    else:
        lay(mask(), col)
    out[..., 3] *= 255
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), 'RGBA')

# ---- route the old font keys through the new type system
_old_tx = V.tx; _TC = {}
def tx(txt, f, size, col=(255, 255, 255)):
    k = (txt, f, size, col)
    if k in _TC: return _TC[k]
    if f == 't7': im = styled(txt, 'khand' if col == V.RED else 'roz', int(size * (.8 if col == V.RED else .82)), 'danger' if col == V.RED else 'poster', col)
    elif f == 's9': im = styled(txt, 'khand', int(size * 1.05), 'plain', col)
    elif f == 'os': im = styled(txt, 'sarp', int(size * .8), 'plain', col)
    elif f in ('s8', 's6') and size <= 70: im = styled(txt, 'khand', int(size * 1.12), 'plain', col)
    elif f == 'r7': im = styled(txt, 'eczar', size, 'plain', col)
    else: im = _old_tx(txt, f, size, col)
    _TC[k] = im; return im
V.tx = tx
import gas4 as G4                                  # imports after the patch so it picks up the new tx
G4.tx = tx
import cine as C
from cine import eio, ease
import gas as G
BW, BH, BX, BY, CW, CH = G4.BW, G4.BH, G4.BX, G4.BY, G4.CW, G4.CH
K = G4.K; clamp, lerp, put, pop, labelbox = G.clamp, G.lerp, V.put, V.pop, V.labelbox
OFF = 3.0; TOTAL_NEW = 66.5; OLD_END = TOTAL_NEW - OFF
RED = V.RED

# ---------------- poster materials
def dark_photo(name, t, d, fy=.5, sat=0.0, k=.38, **kw):
    o = V.sh(name, t, d, fy=fy, **kw); o = C.grade(o, sat=sat, contrast=1.2) * k
    return G.screen_tex(o, .18)
_RIB = {}
def ribbon(o, txt, T, y, angle, speed=120, h=96, col=(206, 26, 28), tcol=(255, 255, 255), a=1.0, k_in=1.0):
    if a <= 0: return o
    key = (txt, h, col, tcol)
    if key not in _RIB:
        unit = styled(txt + '   ·   ', 'khand', int(h * .62), 'plain', tcol); uw = unit.width - 10
        strip = Image.new('RGBA', (uw * 8, h), col + (255,))
        for i in range(8): strip.alpha_composite(unit, (i * uw - 5, (h - unit.height) // 2))
        _RIB[key] = (np.asarray(strip).astype(np.float32), uw)
    S, uw = _RIB[key]; L = int(BW * 1.7)
    off = int((T * speed) % uw); crop = S[:, off:off + L].copy()
    crop[:, int(L * k_in):, 3] = 0                                   # wipe-in from the left
    im = Image.fromarray(crop.astype(np.uint8), 'RGBA').rotate(angle, Image.BICUBIC, expand=True)
    sh = np.asarray(im).astype(np.float32); x0 = int(BW / 2 - sh.shape[1] / 2); y0 = int(y - sh.shape[0] / 2)
    V.comp(o, sh, x0 + 6, y0 + 10, .5 * a, (0, 0, 0)); V.comp(o, sh, x0, y0, a); return o
def stamp(txt, size=110, col=(220, 30, 30), seed=4):
    t = styled(txt, 'khand', size, 'plain', col); w, h = t.width + 30, t.height + 10
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((8, 8, w - 9, h - 9), outline=col + (255,), width=10); d.rectangle((24, 24, w - 25, h - 25), outline=col + (255,), width=4)
    im.alpha_composite(t, (15, 5))
    a = np.asarray(im).astype(np.float32); r = np.random.default_rng(seed)
    n = cv2.GaussianBlur(r.random(a.shape[:2]).astype(np.float32), (0, 0), 1.6); a[..., 3] *= np.clip((n - .38) * 6, 0, 1) * .92   # ink grunge
    return Image.fromarray(a.astype(np.uint8), 'RGBA')
STAMP = None

# ---------------- replacement scenes (old-timeline time T)
def B_odor(T, t, d):
    o = dark_photo('cylinder.jpg', t, d, fy=.35, sat=.5, k=.45, z=(1.05, 1.15), dz=(0, .3), focus=(.85, .85), blur=6)
    o = ribbon(o, 'रंग : कोई नहीं', T, 140, 7, 140, k_in=eio(clamp(t / .5)))
    o = ribbon(o, 'गंध : कोई नहीं', -T, 610, -6, 160, col=(18, 18, 18), k_in=eio(clamp((t - .3) / .5)))
    return o, False
def O_odor(cv, T, t, d):
    V.pop(cv, 'कोई गंध नहीं', 't7', 170, CW / 2, BY + BH / 2 + 5, T - 6.45, (255, 255, 255), .25, .6)
    if T < 6.45: put(cv, styled('LPG = प्रोपेन + ब्यूटेन', 'kalam', 46, 'note', (255, 214, 70)), CW / 2, BY + BH / 2, eio(clamp((t - .4) / .3)), 'c', 0)
def B_law2(T, t, d):
    o = dark_photo('odorant.jpg', t, d, sat=0, k=.42, z=(1.1, 1.0), dz=(.25, 0), focus=(.6, .85), blur=8)
    o = ribbon(o, 'कानून · 1937', T, 120, -5, 130, k_in=eio(clamp(t / .5)))
    o = ribbon(o, 'टेक्सस रेलरोड कमीशन', -T, 640, 4, 110, col=(18, 18, 18), k_in=eio(clamp((t - .3) / .5)))
    ts = T - 45.15
    if 0 < ts < .3: r = np.random.default_rng(int(T * 60)); o = np.roll(o, int(r.normal(0, 14 * (1 - ts / .3))), 0)
    return o, False
def O_law2(cv, T, t, d):
    global STAMP
    V.pop(cv, 'नया कानून', 't7', 150, CW / 2, BY + BH / 2 - 90, T - 43.45, (255, 255, 255), .25, .6)
    ts = T - 45.15
    if ts > 0:
        if STAMP is None: STAMP = stamp('हर गैस में बदबू', 92)
        k = eio(clamp(ts / .16)); put(cv, STAMP.rotate(-8, Image.BICUBIC, expand=True), CW / 2, BY + BH / 2 + 110, k, 'c', .5, 0, 1.5 - .5 * k)
def B_human2(T, t, d):
    u = t / d; o = V.sh('kids.jpg', t, d, z=(1.05, 1.16), dz=(0, .2), focus=(.8, .8), blur=6, fx=.45)
    o = C.grade(C.archive(o, T, seed=21, sepia=False), sat=0, contrast=1.15) * lerp(.85, .62, u)
    o = o + C.leak(T, .22, (255, 150, 80), 2)[:BH, :BW] if C.H == BH else o
    return G.screen_tex(o, .1), False
def O_none(cv, T, t, d): pass
def B_end5(T, t, d):
    o, _ = V.B_end(T, t, d); kb = clamp((T - 61.3) / .3); return o * (1 - .78 * kb), False
def O_end5(cv, T, t, d):
    if T < 61.3:
        tm = K['w_main'] - .35
        pop(cv, 'आपको', 's8', 64, CW / 2, BY + BH / 2 - 160, T - 59.2, (255, 255, 255), .2, .6)
        pop(cv, 'बचाने के लिए', 't7', 210, CW / 2, BY + BH / 2 + 10, T - tm, (255, 255, 255), .3, .7)
    else:
        tb = T - 61.3; k = clamp(tb / .3); b = 1 + .14 * math.sin(min(1, tb / .45) * math.pi) * (1 - min(1, tb / .45))
        put(cv, G4.LOGO[230], CW / 2, BY + BH / 2 - 100, k, 'c', .6, 0, (.55 + .45 * eio(k)) * b)
        put(cv, styled('FreshNestHub', 'roz', 84, 'poster'), CW / 2, BY + BH / 2 + 95, eio(clamp((tb - .12) / .3)), 'c', 0)
        pop(cv, '@fnhtruths', 's8', 40, CW / 2, BY + BH / 2 + 190, tb - .3, (210, 210, 210), .25, .5)

REPL = {V.B_odorless: (B_odor, O_odor), V.B_law: (B_law2, O_law2), V.B_human: (B_human2, O_none)}
for i, (a, b, Bf, Of, tr) in enumerate(G4.S):
    if Bf in REPL: G4.S[i] = (a, b, REPL[Bf][0], REPL[Bf][1], tr)
a, b, Bf, Of, tr = G4.S[-1]; G4.S[-1] = (a, OLD_END, B_end5, O_end5, tr)
V.CAP_OFF[:] = [(lo, hi if hi < 62 else OLD_END) for lo, hi in V.CAP_OFF]
V.CAP_OFF += [(K['s_odorless'], K['s_added']), (K['s_human'], K['s_voice'])] if False else []
V.CAP_OFF[:] = [c for c in V.CAP_OFF if c != (K['s_human'], K['s_voice'])]

# ---------------- cold open (new-timeline 0..3), cut to 'The Business' build, hit at 2.6
HIT = 2.6
CUTS = [(0.0, 'flame'), (.34, 'globe'), (.68, 'flip'), (1.02, 'ruins'), (1.36, 'blue'), (1.70, 'clock'), (2.04, 'odorant'), (2.38, 'black'), (HIT, 'flame')]
def intro_band(T):
    cur = [c for c in CUTS if c[0] <= T][-1][1]; t = T - [c for c in CUTS if c[0] <= T][-1][0]
    if cur == 'flame': o = V.sh('flame.jpg', T, 3.0, z=(1.0, 1.12), dz=(0, .25), focus=(.9, .9), blur=6); o = C.bloom(o, 150, .8, 40, (.7, .9, 1.2)); o = C.grade(o, shadows=(.85, 1, 1.2), highs=(1.05, 1, .9))
    elif cur == 'globe': o = G4.maps.globe(BW, BH, lerp(60, 20, t / .34), 25, 330, {'India': ((255, 170, 60), .9)})
    elif cur == 'flip': o = np.zeros((BH, BW, 3), np.float32) + 30; V.flipcard(o, '1937', BW / 2, BH / 2, 1.0)
    elif cur == 'ruins': o = C.grade(V.arch(V.sh('ruins.jpg', t, .34, z=(1.1, 1.2), focus=(.5, .5), blur=0), T, 2), sat=0, contrast=1.2)
    elif cur == 'blue': o, _ = G4.B_blue(22.8, 3.0, 4.6)
    elif cur == 'clock': o, _ = G4.B_clock(29.4, 1.3, 2.6)
    elif cur == 'odorant': o = C.grade(V.sh('odorant.jpg', t, .34, z=(1.15, 1.25), focus=(.6, .6), blur=0))
    else: o = np.zeros((BH, BW, 3), np.float32) + 4
    if t < .06: o = V.glitch(o, T, .8)
    if T >= HIT: o = o * (1 - math.exp(-(T - HIT) * 9)) + 255 * math.exp(-(T - HIT) * 9)
    return o * (.55 if cur != 'black' and T < HIT else 1.0)
def intro(T):
    band = C.finish(np.clip(intro_band(T), 0, 255), T, grain=6).astype(np.float32)
    sc, sh = 1.0, (0, 0)
    if T >= HIT: r = np.random.default_rng(int(T * 90)); s = 22 * math.exp(-(T - HIT) * 7); sh = (r.normal(0, s), r.normal(0, s)); sc = 1 + .05 * math.exp(-(T - HIT) * 6)
    cv = G4.compose(band, T, sc, sh); G4.brand_bug(cv)
    put(cv, styled('आपकी गैस में', 'khand', 78, 'plain'), CW / 2, BY + BH / 2 - 150, 1, 'c', .8)
    k = 1 + (.25 * math.exp(-(T - HIT) * 8) if T >= HIT else 0)
    put(cv, styled('बदबू क्यों है?', 'roz', 170, 'poster'), CW / 2, BY + BH / 2 + 30, 1, 'c', .5, 0, k)
    return np.clip(cv, 0, 255).astype(np.uint8)

def frame(T):
    return intro(T) if T < OFF else G4.frame(T - OFF)

if __name__ == '__main__':
    P = G.P
    if sys.argv[1] == 'stills':
        for s in sys.argv[2:]: Image.fromarray(frame(float(s))).save(f'/tmp/g5_{s}.jpg', quality=88)
    else:
        a, b = float(sys.argv[2]), float(sys.argv[3]); os.makedirs(P + '/segs5', exist_ok=True); out = f'{P}/segs5/seg_{a:05.1f}.mp4'
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{CW}x{CH}', '-r', '30', '-i', '-',
                              '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', out + '.tmp.mp4'], stdin=subprocess.PIPE)
        for n in range(int(round(a * 30)), int(round(b * 30))): p.stdin.write(frame(n / 30).tobytes())
        p.stdin.close(); p.wait(); os.replace(out + '.tmp.mp4', out)
