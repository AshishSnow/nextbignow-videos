#!/usr/bin/env python3
"""गैस की बदबू — v2 design (frame / fonts / animation).
Frame : cinematic 3:2 band (1080x720) inside the vertical canvas, black surround with a faint grid,
        series header, red '//' chapter tags above the band, doc metadata below it.
Type  : Noto Sans Devanagari 600/800/900 (merged with its Latin subset, so digits and punctuation work).
Motion: giant translucent words over the band, red per-word caption boxes, split-screen push,
        strike-through, blur/push transitions, RGB split + halftone on archive shots, white-flash blast.
usage: gas2.py stills t.. | seg a b"""
import os, sys
os.environ['CINE_H'] = '720'
sys.path.insert(0, '/home/claude/studio/tools'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, math, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cine as C
import gas as G
from cine import ease, eio
BW, BH = C.W, C.H                   # band 1080 x 720
CW, CH = 1080, 1920                 # canvas
BY = 540                            # band top -> band spans 540..1260
P = G.P; K = G.K; TOTAL = K['total']; FPS = 30
clamp, lerp = G.clamp, G.lerp
FD = '/home/claude/studio/fonts/doc/'
FW = {600: FD + 'nsd-600.ttf', 800: FD + 'nsd-800.ttf', 900: FD + 'nsd-900.ttf'}
RED = (226, 36, 36); WHITE = (255, 255, 255); GREY = (150, 150, 150)

# ---------------- text primitives (canvas space)
_TC = {}
def tl(txt, size, w=800, col=WHITE, track=0):
    k = (txt, size, w, col, track)
    if k in _TC: return _TC[k]
    f = ImageFont.truetype(FW[w], size, layout_engine=ImageFont.Layout.RAQM); bb = f.getbbox(txt)
    im = Image.new('RGBA', (bb[2] - bb[0] + 40, bb[3] - bb[1] + 40), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((20 - bb[0], 20 - bb[1]), txt, font=f, fill=col + (255,))
    _TC[k] = im; return im
def comp(cv, src, ox, oy, am, col=None):
    h, w = src.shape[:2]; Hh, Ww = cv.shape[:2]
    xa, ya = max(0, ox), max(0, oy); xb, yb = min(Ww, ox + w), min(Hh, oy + h)
    if xb <= xa or yb <= ya or am <= 0: return
    s = src[ya - oy:yb - oy, xa - ox:xb - ox]; al = s[..., 3:4] / 255 * am
    rgb = s[..., :3] if col is None else np.array(col, np.float32)
    cv[ya:yb, xa:xb] = cv[ya:yb, xa:xb] * (1 - al) + rgb * al
def cput(cv, im, x, y, a=1.0, anchor='c', shadow=.7, blur=0.0, scale=1.0):
    if a <= 0.01: return
    if scale != 1.0: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BICUBIC)
    if blur > .3: im = im.filter(ImageFilter.GaussianBlur(blur))
    x0 = int(x - im.width / 2) if anchor == 'c' else int(x - 20) if anchor == 'l' else int(x - im.width + 20)
    y0 = int(y - im.height / 2)
    if shadow: comp(cv, np.asarray(im.filter(ImageFilter.GaussianBlur(14))).astype(np.float32), x0, y0 + 6, a * shadow, (0, 0, 0))
    comp(cv, np.asarray(im).astype(np.float32), x0, y0, a)

def giant(cv, txt, y, t, size=300, w=900, alpha=.93, col=WHITE, dur=.4):
    """big word over the band: scales down 1.12->1 with a focus-pull in"""
    if t <= 0: return
    k = eio(t / dur)
    cput(cv, tl(txt, size, w, col), CW / 2, y, alpha * k, 'c', .55, 18 * (1 - k), 1.12 - .12 * k)
def tag(cv, txt, t, y=BY - 46, col=RED):
    """chapter tag above the band, typed on: 'TXT //'"""
    if t <= 0: return
    s = txt + '  //'; n = int(clamp(t * 30, 0, len(s)))
    if n: cput(cv, tl(s[:n], 44, 800, col), 56, y, 1.0, 'l', .0)
def meta(cv, txt, t, col=GREY):
    if t <= 0: return
    cput(cv, tl(txt, 30, 600, col), CW - 56, BY + BH + 34, eio(t / .4), 'r', 0)
def boxline(cv, txt, x, y, t, size=62, bg=RED, fg=WHITE, dur=.32, anchor='l'):
    """red box with white text, wipes in from the left"""
    if t <= 0: return
    k = eio(t / dur); im = tl(txt, size, 800, fg); w, h = im.width - 8, im.height - 4
    x0 = int(x if anchor == 'l' else x - w / 2); y0 = int(y - h / 2)
    ww = int(w * k); cv[y0:y0 + h, x0:x0 + ww] = np.array(bg, np.float32)
    if k > .55: cput(cv, im, x0 + w / 2, y, clamp((k - .55) / .3), 'c', 0)
def handles(cv, cx, cy, w, h, t, col=(235, 235, 235)):
    if t <= 0: return
    G.handles.__globals__['W']; k = eio(t / .3); w, h = w * (0.9 + .1 * k), h * (0.9 + .1 * k)
    x0, y0, x1, y1 = int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2); c = tuple(float(v * k) for v in col)
    for x in range(x0, x1, 18): cv2.line(cv, (x, y0), (min(x + 9, x1), y0), c, 2); cv2.line(cv, (x, y1), (min(x + 9, x1), y1), c, 2)
    for y in range(y0, y1, 18): cv2.line(cv, (x0, y), (x0, min(y + 9, y1)), c, 2); cv2.line(cv, (x1, y), (x1, min(y + 9, y1)), c, 2)
    for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)): cv2.rectangle(cv, (x - 9, y - 9), (x + 9, y + 9), c, -1)

# ---------------- captions: word chunks under the band, active word in a red box
WORDS = [w for w in json.load(open(P + '/work/words.json'))]
CH_ = []; cur = []
for i, w in enumerate(WORDS):
    if cur and (len(cur) >= 3 or w[0] - cur[-1][1] > .28 or sum(len(x[2]) for x in cur) + len(w[2]) > 20): CH_.append(cur); cur = []
    cur.append(w)
CH_.append(cur)
CAP_Y = BY + BH + 150
def captions(cv, T, off=()):
    for ci, ch in enumerate(CH_):
        nxt = CH_[ci + 1][0][0] if ci + 1 < len(CH_) else TOTAL
        if ch[0][0] - .05 <= T < min(nxt, ch[-1][1] + .6): break
    else: return
    if any(a <= T < b for a, b in off): return
    ims = [tl(w[2].strip(',.'), 64, 800) for w in ch]; gap = 10
    tot = sum(im.width - 40 + 28 for im in ims) + gap * (len(ims) - 1); x = CW / 2 - tot / 2
    for w, im in zip(ch, ims):
        bw = im.width - 40 + 28; act = w[0] <= T < (w[1] + .05)
        if T >= w[0] - .05:
            if act:
                k = eio((T - w[0]) / .12); h = 92
                cv[int(CAP_Y - h / 2):int(CAP_Y + h / 2), int(x + bw / 2 - bw * k / 2):int(x + bw / 2 + bw * k / 2)] = np.array(RED, np.float32)
            cput(cv, im, x + bw / 2, CAP_Y - 4, 1.0, 'c', 0 if act else .8)
        x += bw + gap

# ---------------- canvas background: near-black with faint grid
BG = np.full((CH, CW, 3), 7, np.float32)
for g in range(0, CW, 54): BG[:, g] += 5
for g in range(0, CH, 54): BG[g, :] += 5
_yy, _xx = np.mgrid[0:CH, 0:CW]; BG *= (1 - .55 * np.clip(np.sqrt(((_xx - 540) / 900) ** 2 + ((_yy - 900) / 1300) ** 2) - .2, 0, 1))[..., None]
def header(cv, T):
    a = .9
    cput(cv, tl('छुपी कहानियाँ', 34, 800, (235, 235, 235)), 56, 360, a, 'l', 0)
    im = tl('EP 01', 26, 800, WHITE); x = 56 + tl('छुपी कहानियाँ', 34, 800).width - 10
    cv[343:377, x:x + im.width - 22] = np.array(RED, np.float32); cput(cv, im, x + (im.width - 22) / 2, 360, a, 'c', 0)
    cput(cv, tl('FreshNestHub', 28, 600, (170, 170, 170)), CW - 56, 360, a, 'r', 0)

# ---------------- band shots (1080x720)
shot3d = G.shot3d
def arch(o, T, seed=0, fade=True):
    o = C.archive(o, T, seed=seed)
    if fade: o = o * .86 + 22
    return G.screen_tex(G.chroma(o, 3), .10)
def look(o, **kw): return C.grade(o, **kw)

def B_open(T, t, d):
    nm = 'flame.jpg' if t < .62 else 'cylinder.jpg' if t < 1.3 else 'kettle.jpg'
    o, _ = shot3d(nm, clamp(t / d), z=(1.06, 1.16), dz=(0, .25), focus=(.85, .85), blur=10)
    return G.screen_tex(G.chroma(look(o, sat=.8) * .78, 3), .08)
def O_open(cv, T, t, d):
    giant(cv, 'बदबू', BY + BH / 2 + 10, t + .4, 330, dur=.01)
    handles(cv, CW / 2, BY + BH / 2 + 2, 640, 320, t - .1)
def B_kitchen(T, t, d):
    tn = K['w_nahi'] - K['s_kitchen'] - .5
    o, _ = shot3d('kitchen.jpg', t / d, z=(1.0, 1.12), dz=(0, .3), tx=(0, -30), focus=(.85, .95), blur=9)
    o = C.bloom(o, 180, .45); o = G.wisps(o, T, 560, 690, alpha=.5, spread=.62)
    if t > tn: o = G.chroma(o, int(12 * math.exp(-(t - tn) * 7)))
    return look(o, shadows=(0.9, 1.0, 1.15), highs=(1.1, 1.0, .85))
def O_kitchen(cv, T, t, d):
    ta = 3.5 - K['s_kitchen']; tag(cv, 'LPG', t)
    giant(cv, 'असली', BY + BH / 2, t - ta + .15, 260)
    ts = t - (4.0 - K['s_kitchen'])
    if ts > 0:
        im = tl('असली', 260, 900); w = im.width - 60; k = eio(ts / .25); x0 = int(CW / 2 - w / 2); y = int(BY + BH / 2 + 12)
        cv[y - 9:y + 9, x0:x0 + int(w * k)] = np.array(RED, np.float32)
def B_odorless(T, t, d):
    o, dd = shot3d('cylinder.jpg', t / d, z=(1.0, 1.1), dz=(0, .3), tx=(20, -20), focus=(.85, .85), blur=12, fy=.35)
    m = np.clip((dd - .2) * 1.5, 0, 1).astype(np.float32); o = C.haze(o, T, m, amp=9)
    return look(o, shadows=(0.9, 1.0, 1.12), highs=(1.05, 1.0, .9))
def O_odorless(cv, T, t, d):
    tag(cv, 'गंध: शून्य', T - 6.6); meta(cv, 'प्राकृतिक LPG · गंधहीन', t - .3)
def B_added(T, t, d):
    o, _ = shot3d('flame.jpg', t / d, z=(1.0, 1.15), dz=(0, .25), focus=(.9, .9), blur=10)
    o = C.bloom(o, 150, .8, 40, (.7, .9, 1.2)); o = look(o, shadows=(0.85, 1.0, 1.2), highs=(1.05, 1.0, .9))
    return o * (1 - .35 * eio(clamp((T - 8.7) / .3)))
def O_added(cv, T, t, d):
    tag(cv, 'मिलाई जाती है', T - 9.4); giant(cv, 'जानबूझकर', BY + BH / 2, T - 8.75, 210)
def B_ruins(T, t, d):
    ts = T - K['w_worst']
    o, _ = shot3d('ruins.jpg', t / d, z=(1.0, 1.12), dz=(0, .3), tx=(25, -25), focus=(.5, .8), blur=10)
    o = look(arch(o, T, 5), sat=0, contrast=1.1) * .85
    if ts > 0:                                                    # split-screen push: rescue slides in from the right
        k = eio(ts / .45); r, _ = shot3d('rescue.jpg', clamp(ts / 2), z=(1.1, 1.18), focus=(.6, .6), blur=8)
        r = look(arch(r, T, 8), sat=0, contrast=1.1) * .8
        half = BW // 2; sh = int(half * k); out = o.copy()
        out[:, :BW - sh] = o[:, int(sh * .5):int(sh * .5) + BW - sh]          # left panel pushed aside
        out[:, BW - sh:] = r[:, half - sh // 2:half - sh // 2 + sh]            # right panel enters
        if 0 < sh < BW: out[:, BW - sh - 3:BW - sh + 3] = 8
        o = out
    return o
def O_ruins(cv, T, t, d):
    tag(cv, 'USA', t - .2); meta(cv, 'अमेरिका · स्कूल हादसा', t - .6)
    giant(cv, 'हादसा', BY + BH / 2, T - 14.35, 300, alpha=.95)
def B_texas(T, t, d):
    o, _ = shot3d('pipeline.jpg', t / d, z=(1.05, 1.2), dz=(0, .35), tx=(-40, 30), focus=(.9, .6), blur=14)
    fb = 1 - eio(clamp((t - 1.0) / .5))
    if fb > .01: o = cv2.GaussianBlur(o, (0, 0), 1 + 22 * fb) * fb + o * (1 - fb)
    return look(arch(o, T, 3), sat=1.0)
def O_texas(cv, T, t, d):
    fb = 1 - eio(clamp((t - 1.0) / .5))
    if fb > .01: giant(cv, '1937', BY + BH / 2, t + .01, 340, alpha=.95 * fb)
    tag(cv, 'न्यू लंदन, टेक्सस', t - .9); meta(cv, '18 मार्च 1937', t - 1.2)
def B_pipe(T, t, d):
    o, dd = shot3d('pipeline.jpg', t / d, z=(1.25, 1.42), dz=(.1, .4), tx=(-30, 30), focus=(.9, .9), blur=14, fx=.4)
    o = look(arch(o, T, 6), sat=1.0); m = np.clip((dd - .35) * 3, 0, 1).astype(np.float32)
    return C.haze(o, T, m, amp=8)
def O_pipe(cv, T, t, d):
    tag(cv, 'कच्ची गैस', T - K['w_kachi']) if T < K['w_bina'] else tag(cv, 'बिना गंध', T - K['w_bina'])
    meta(cv, 'पैसे बचाने के लिए', t - .3)
def B_walls(T, t, d):
    u = t / d; o, dd = shot3d('kids.jpg', u, z=(1.0, 1.14), dz=(0, .35), focus=(.75, .5), blur=12)
    o = C.archive(o, T, seed=7) * .86 + 22
    yy = np.linspace(0, 1, BH, dtype=np.float32)[:, None].repeat(BW, 1)
    m = (np.clip((yy - lerp(1.05, -.15, ease(u))) / .3, 0, 1) * np.clip(1.1 - dd * .4, 0, 1)).astype(np.float32)
    o = C.haze(o, T, m, amp=13); o = o * (1 - .14 * m[..., None]) + np.array([150, 165, 120], np.float32) * .14 * m[..., None]
    o = o * (1 - .07 * math.exp(-((t % .85) * 9)))
    return G.screen_tex(G.chroma(look(o, sat=.85), 2), .08)
def O_walls(cv, T, t, d): tag(cv, 'चुपचाप', t - .4); meta(cv, 'स्कूल की दीवारों के पीछे', t - .8)
def B_clock(T, t, d):
    o, _ = shot3d('kids.jpg', .5, z=(1.35, 1.35), focus=(.1, .1), blur=24, fx=.6)
    o = C.archive(o, T, seed=9) * .4; G.clock(o, T, t, cx=540, cy=360, r=250); return o
def O_clock(cv, T, t, d):
    tag(cv, 'दोपहर', t - .1); giant(cv, '3:17', BY + BH - 40, T - 29.0, 200, alpha=.9)
def B_teacher(T, t, d):
    u = t / d; o, _ = shot3d('switch.jpg', u, z=(1.05, 1.35), dz=(0, .35), focus=(.95, .95), blur=18)
    return look(arch(o, T, 11, fade=False)) * lerp(1, .8, u)
def O_teacher(cv, T, t, d):
    tag(cv, 'एक टीचर', t - .05) if T < K['w_switch'] else tag(cv, 'एक स्विच', T - K['w_switch'])
def B_spark(T, t, d):
    o = np.zeros((BH, BW, 3), np.float32) + 3; ts = K['w_spark'] - K['spark0']
    if t > ts - .15:
        r = np.random.default_rng(int(T * 60)); k = clamp((t - ts + .15) / .5)
        for _ in range(46):
            a = r.uniform(0, 6.28); s = r.uniform(5, 160) * k
            cv2.line(o, (540, 360), (int(540 + math.cos(a) * s), int(360 + math.sin(a) * s)), (255, 215, 150), 2, cv2.LINE_AA)
        o = C.bloom(o, 80, 2.2, 28)
    return o
def O_spark(cv, T, t, d): pass
def B_blast(T, t, d):
    img, dd = G.plate('ruins.jpg'); sh = 34 * math.exp(-t * 4); r = np.random.default_rng(int(T * 90))
    o, _ = C.cam3d(img, dd, zoom=lerp(1.18, 1.04, eio(clamp(t / d))), dz=.15, tx=r.normal(0, sh), ty=r.normal(0, sh))
    return look(arch(o, T, 1, fade=False), sat=.0, contrast=1.15)
def O_blast(cv, T, t, d): pass
def B_cost(T, t, d):
    o, _ = shot3d('rescue.jpg', t / d, z=(1.02, 1.12), dz=(0, .25), tx=(30, -30), focus=(.55, .8), blur=10)
    o = C.archive(o, T, seed=15) * .7; o = C.dust(o, T, 40, alpha=.25); o = look(o, sat=0)
    fb = clamp(1 - (T - K['w_kids']) / .6) if T > K['w_kids'] else 1.0
    return cv2.GaussianBlur(o, (0, 0), 16) * fb + o * (1 - fb)
def O_cost(cv, T, t, d):
    fb = clamp(1 - (T - K['w_kids']) / .5) if T > K['w_kids'] else 1.0
    giant(cv, '300', BY + BH / 2 - 30, t - .1, 400, alpha=.95 * fb)
    if fb > .01: cput(cv, tl('लोग', 60, 800), CW / 2, BY + BH / 2 + 190, fb * eio(clamp((t - .7) / .3)), 'c', .6)
    tag(cv, 'मौतें', t - .2); meta(cv, 'न्यू लंदन स्कूल, 1937', t - .5)
    boxline(cv, 'ज़्यादातर बच्चे', CW / 2, BY + BH / 2, T - K['w_kids'], 92, anchor='c')
def B_human(T, t, d):
    u = t / d; o, _ = shot3d('kids.jpg', u, z=(1.12, 1.2), dz=(0, .15), focus=(.8, .8), blur=10, fx=.45)
    return look(C.archive(o, T, seed=21) * lerp(.75, .55, u), sat=0)
def O_human(cv, T, t, d): pass
def B_voice(T, t, d):
    o, _ = shot3d('odorant.jpg', t / d, z=(1.12, 1.0), dz=(.25, 0), tx=(20, -20), focus=(.6, .85), blur=12)
    col = look(C.bloom(o, 190, .4)); bw = C.archive(o, T, seed=17, sepia=False)
    k = eio(clamp((T - K['w_awaaz']) / 1.2)); return bw * (1 - k) + col * k
def O_voice(cv, T, t, d):
    tag(cv, 'कानून', T - K['w_awaaz']); meta(cv, '1937 के बाद', T - K['w_awaaz'] - .3)
    if T > 46.9: tag(cv, 'नाक = अलार्म', T - 46.9, BY - 46 - 0, (255, 255, 255)) if False else None
def B_today(T, t, d):
    o, _ = shot3d('cylinder.jpg', t / d, z=(1.0, 1.14), dz=(0, .3), tx=(-20, 20), focus=(.85, .85), blur=14, fy=.35)
    o = C.bloom(o, 190, .4); o = G.wisps(o, T, 540, 690, alpha=.4, spread=.6); o = look(o)
    return o * (1 - .45 * eio(clamp((T - K['w_ethyl'] + .1) / .3)))
def O_today(cv, T, t, d):
    tag(cv, 'आज', t - .1); te = T - K['w_ethyl'] + .1
    giant(cv, 'एथिल मरकैप्टन', BY + BH / 2 - 20, te, 120, alpha=.97)
    if te > .3: cput(cv, tl('C₂H₅SH', 46, 600, (200, 200, 200)) if False else tl('ETHYL MERCAPTAN', 34, 600, (205, 205, 205)), CW / 2, BY + BH / 2 + 80, eio((te - .3) / .3), 'c', .5)
def B_rules(T, t, d):
    o, _ = shot3d('kitchen.jpg', t / d, z=(1.1, 1.14), focus=(.05, .05), blur=26)
    return look(o) * .5
def O_rules(cv, T, t, d):
    tag(cv, 'बदबू आए तो', t - .05)
    for i, (txt, key) in enumerate((('स्विच मत छूना', 'r1'), ('रेगुलेटर बंद करो', 'r2'), ('खिड़कियाँ खोलो', 'r3'))):
        tt = T - K[key] + .15; y = BY + 170 + i * 190
        if tt > 0: cput(cv, tl(f'0{i + 1}', 40, 800, (255, 255, 255)), 96, y, eio(tt / .3), 'l', 0)
        boxline(cv, txt, 170, y, tt, 72)
def B_end(T, t, d):
    u = t / d; tm = K['w_main'] - K['s_end']
    o, _ = shot3d('kettle.jpg', u, z=(1.0, 1.1), dz=(0, .25), focus=(.8, .8), blur=14)
    o = C.bloom(o, 170, .6); o = G.wisps(o, T, 540, 700, (255, 200, 120), alpha=.4, spread=.6)
    o = look(o, shadows=(0.9, 1.0, 1.15), highs=(1.12, 1.0, .82))
    return o * (1 - .6 * eio(clamp((t - tm + .4) / .6)))
def O_end(cv, T, t, d):
    tm = K['w_main'] - .4
    cput(cv, tl('आपको', 70, 800), CW / 2, BY + BH / 2 - 150, eio(clamp((T - K['s_end'] - 1.0) / .3)), 'c', .6)
    giant(cv, 'बचाने', BY + BH / 2, T - tm, 260)
    boxline(cv, 'के लिए।', CW / 2, BY + BH / 2 + 190, T - 60.2, 76, anchor='c')
    if T > 61.0: cput(cv, tl('FreshNestHub  //', 40, 800, RED), CW / 2, BY + BH + 150, eio((T - 61.0) / .4), 'c', 0)

def build():
    k = K; S = []
    def seg(a, b, nm, tr): S.append((a, b, globals()['B_' + nm], globals()['O_' + nm], tr))
    seg(0, k['s_kitchen'], 'open', None); seg(k['s_kitchen'], k['s_odorless'], 'kitchen', 'cut')
    seg(k['s_odorless'], k['s_added'], 'odorless', 'push'); seg(k['s_added'], k['s_ruins'], 'added', 'blur')
    seg(k['s_ruins'], k['s_texas'], 'ruins', 'flash'); seg(k['s_texas'], k['s_pipe'], 'texas', 'blur'); seg(k['s_pipe'], k['s_walls'], 'pipe', 'push')
    seg(k['s_walls'], k['s_clock'], 'walls', 'blur'); seg(k['s_clock'], k['w_teacher'], 'clock', 'cut'); seg(k['w_teacher'], k['spark0'], 'teacher', 'push')
    seg(k['spark0'], k['s_blast'], 'spark', 'cut'); seg(k['s_blast'], k['s_cost'], 'blast', 'cut'); seg(k['s_cost'], k['s_human'], 'cost', 'blur')
    seg(k['s_human'], k['s_voice'], 'human', 'blur'); seg(k['s_voice'], k['s_today'], 'voice', 'blur'); seg(k['s_today'], k['s_rules'], 'today', 'push')
    seg(k['s_rules'], k['s_end'], 'rules', 'blur'); seg(k['s_end'], TOTAL, 'end', 'blur')
    return S
SHOTS = build()
CAP_OFF = ((K['s_rules'], K['s_end']), (K['w_main'] - .4, TOTAL), (K['w_kids'] - .1, K['s_human']))

def band_at(i, T):
    a, b, fn, _, _ = SHOTS[i]; return fn(T, T - a, b - a)
def frame(T):
    for i, (a, b, fn, ov, tr) in enumerate(SHOTS):
        if a <= T < b or i == len(SHOTS) - 1: break
    t, d = T - a, b - a
    o = fn(T, t, d)
    if i > 0 and tr == 'blur' and t < .35:
        prev = band_at(i - 1, T); kk = eio(t / .35)
        o = cv2.GaussianBlur(prev, (0, 0), 1 + 30 * kk) * (1 - kk) + cv2.GaussianBlur(o, (0, 0), 1 + 30 * (1 - kk)) * kk
    elif i > 0 and tr == 'push' and t < .3:               # whip push: old slides out left, new in from right, motion blur
        prev = band_at(i - 1, T); kk = eio(t / .3); sh = int(BW * kk)
        mb = np.ones((1, 61), np.float32) / 61 * math.sin(math.pi * kk)
        both = np.concatenate([prev, o], 1)[:, sh:sh + BW]
        o = cv2.filter2D(both, -1, mb) + both * (1 - math.sin(math.pi * kk)) if kk < 1 else o
    elif tr == 'flash' and t < .1: o = o * (t / .1) + 255 * (1 - t / .1)
    if fn is B_blast: o = o * (1 - math.exp(-t * 7)) + 255 * math.exp(-t * 7)
    band = C.finish(o, T, grain=6).astype(np.float32)
    # band entrance punch on the very first frames (hook)
    cv = BG.copy(); cv[BY:BY + BH] = band
    header(cv, T)
    ov(cv, T, t, d)
    captions(cv, T, CAP_OFF)
    if fn is B_blast: fl = math.exp(-t * 6); cv = cv * (1 - fl) + 255 * fl
    return np.clip(cv, 0, 255).astype(np.uint8)

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for s in sys.argv[2:]: Image.fromarray(frame(float(s))).save(f'/tmp/g2_{s}.jpg', quality=88)
    else:
        a, b = float(sys.argv[2]), float(sys.argv[3]); os.makedirs(P + '/segs2', exist_ok=True); out = f'{P}/segs2/seg_{a:05.1f}.mp4'
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{CW}x{CH}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', out + '.tmp.mp4'], stdin=subprocess.PIPE)
        for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(frame(n / FPS).tobytes())
        p.stdin.close(); p.wait(); os.replace(out + '.tmp.mp4', out)
