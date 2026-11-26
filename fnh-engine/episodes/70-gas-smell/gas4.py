#!/usr/bin/env python3
"""गैस की बदबू — v4.
Frame : floating 4:3 card (1000x750, rounded) on an ambient blur of itself (screen never dead black)
Brand : FreshNestHub logo bug above the frame + chapter tag; branded end card
New   : 3D globe India -> USA with a flight arc, Texas map zoom + pin, blueprint of the school with gas
        creeping through the crawlspace, frame-break on the explosion, 1937 newsreel (if available)
usage: gas4.py stills t.. | seg a b"""
import os, sys
os.environ['CINE_W'] = '1000'; os.environ['CINE_H'] = '750'
sys.path.insert(0, '/home/claude/studio/tools'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, math, subprocess
import numpy as np, cv2
from PIL import Image
import cine as C, gas as G, gas3 as V, maps
from cine import ease, eio
BW, BH = C.W, C.H; CW, CH = 1080, 1920; BX = (CW - BW) // 2; BY = 560
V.BY = BY
K = G.K; TOTAL = K['total']; FPS = 30; P = G.P
clamp, lerp, tx, put, pop, labelbox = G.clamp, G.lerp, V.tx, V.put, V.pop, V.labelbox
RED = V.RED; WHITE = V.WHITE

# ---------------- brand
_logo = Image.open('/home/claude/studio/fnh_logoB_2048.png').convert('RGBA')
LOGO = {s: _logo.resize((s, s), Image.LANCZOS) for s in (64, 230)}
def brand_bug(cv, a=1.0):
    put(cv, LOGO[64], BX + 30, BY - 58, a, 'l', .5)
    put(cv, tx('FreshNestHub', 's8', 34, WHITE), BX + 100, BY - 56, a, 'l', .5)
CHAP = [(0, 10.46, 'LPG'), (10.46, 15.0, 'अमेरिका'), (15.0, 28.1, 'टेक्सस · 1937'), (28.1, 36.28, '18 मार्च 1937'),
        (36.28, 42.5, 'न्यू लंदन स्कूल'), (42.5, 48.9, 'कानून'), (48.9, 58.1, 'आज · आपकी रसोई')]
def chapter(cv, T):
    for a, b, s in CHAP:
        if a <= T < b:
            t = T - a; n = int(clamp(t * 30, 0, len(s)))
            if n:
                im = tx(s[:n], 's8', 30, WHITE); w = im.width - 20
                x1 = BX + BW - 10; x0 = x1 - w - 34; y = BY - 56
                cv[y - 22:y + 22, x0:x1] = np.array(RED, np.float32)
                put(cv, im, x0 + 17 + w / 2 - 10, y - 1, 1, 'c', 0)
            return

# ---------------- frame material
_yy, _xx = np.mgrid[0:BH, 0:BW]
def _round_mask(r=26):
    m = np.ones((BH, BW), np.float32)
    for (cx, cy) in ((r, r), (BW - r - 1, r), (r, BH - r - 1), (BW - r - 1, BH - r - 1)):
        q = ((_xx < r) if cx == r else (_xx > BW - r - 1)) & ((_yy < r) if cy == r else (_yy > BH - r - 1))
        d = np.sqrt((_xx - cx) ** 2 + (_yy - cy) ** 2); m[q] = np.clip(r + .5 - d[q], 0, 1)
    return m[..., None]
MASK = _round_mask()
SHADOW = np.zeros((CH, CW), np.float32); SHADOW[BY + 18:BY + BH + 18, BX:BX + BW] = 1; SHADOW = cv2.GaussianBlur(SHADOW, (0, 0), 30)[..., None]
_cy = np.linspace(0, 1, CH, dtype=np.float32)[:, None, None]
AMB_V = (.5 - .25 * np.abs(_cy - .48) * 2).clip(.12, 1)
def ambient(band):
    s = cv2.resize(band, (BW // 12, BH // 12), interpolation=cv2.INTER_AREA); s = cv2.GaussianBlur(s, (0, 0), 2.5)
    a = cv2.resize(s, (CW // 6, CH // 6), interpolation=cv2.INTER_LINEAR); a = cv2.resize(cv2.GaussianBlur(a, (0, 0), 8), (CW, CH), interpolation=cv2.INTER_LINEAR)
    g = a.mean(2, keepdims=True); a = g + (a - g) * 1.35        # keep colour rich
    return a * AMB_V
def compose(band, T, scale=1.0, shake=(0, 0)):
    cv = ambient(band); cv = cv * (1 - .55 * SHADOW)
    if scale == 1.0 and shake == (0, 0):
        reg = cv[BY:BY + BH, BX:BX + BW]; reg[:] = reg * (1 - MASK) + band * MASK
        cv2.rectangle(cv, (BX, BY), (BX + BW - 1, BY + BH - 1), (0, 0, 0), 0)
    else:
        w, h = int(BW * scale), int(BH * scale); b = cv2.resize(band, (w, h)); m = cv2.resize(MASK, (w, h))[..., None]
        x0 = int(CW / 2 - w / 2 + shake[0]); y0 = int(BY + BH / 2 - h / 2 + shake[1])
        xa, ya, xb, yb = max(0, x0), max(0, y0), min(CW, x0 + w), min(CH, y0 + h)
        reg = cv[ya:yb, xa:xb]; bb = b[ya - y0:yb - y0, xa - x0:xb - x0]; mm = m[ya - y0:yb - y0, xa - x0:xb - x0]
        reg[:] = reg * (1 - mm) + bb * mm
    return cv

# ---------------- new scenes
def B_globe(T, t, d):
    k = eio(clamp((t - .35) / 1.65))
    lon = lerp(78, -95, k); lat = lerp(20, 33, k); R = lerp(300, 330, eio(clamp(t / d)))
    hl = {'India': ((255, 170, 60), .95 * (1 - .4 * k)), 'United States of America': ((226, 36, 36), .9 * eio(clamp((t - 1.6) / .4)))}
    o = maps.globe(BW, BH, lon, lat, R, hl, arc=((22.5, 78.5), (32.2, -94.9), max(.001, k)), T=T)
    return o, False
def O_globe(cv, T, t, d):
    k = eio(clamp((t - .35) / 1.65))
    if t < .5: pop(cv, 'भारत', 's8', 40, BX + BW / 2 + 40, BY + BH / 2 - 70, t - .05, WHITE, .2, .8)
    if t > 1.75: pop(cv, 'अमेरिका', 's8', 44, BX + BW / 2 + 60, BY + BH / 2 - 120, t - 1.75, WHITE, .2, .8)
def B_texmap(T, t, d):
    z = eio(clamp(t / 1.1)); sc = math.exp(lerp(math.log(14), math.log(62), z))
    o = maps.statemap(BW, BH, lerp(38, 31.8, z), lerp(-97, -96.2, z), sc, 'Texas', (32.235, -94.92), t - .9, T)
    return o, False
def O_texmap(cv, T, t, d):
    if t > 1.15:
        s = 'न्यू लंदन'; n = int(clamp((t - 1.15) * 20, 0, len(s)))
        k = math.cos(math.radians(31.8)); x = BX + BW / 2 + (-94.92 + 96.2) * k * 62; y = BY + BH / 2 - (32.235 - 31.8) * 62
        if n: labelbox(cv, s[:n], int(x - 250), int(y - 4), 1, 's8', 46, WHITE, (20, 20, 20))
    if t > 1.6: labelbox(cv, 'पैसे बचाने के लिए', BX + 40, BY + BH - 70, t - 1.6, 's8', 40, (10, 10, 10), WHITE)

BLUE = np.array([20, 54, 108], np.float32)
def _bp_base():
    o = np.zeros((BH, BW, 3), np.float32) + BLUE
    for x in range(0, BW, 25): o[:, x] += 10 if x % 125 else 22
    for y in range(0, BH, 25): o[y, :] += 10 if y % 125 else 22
    return o
BP = _bp_base()
PIPE = np.array([[0, 650], [250, 650], [330, 650], [330, 590], [420, 590]], np.float32)
def along(path, n_space=26, off=0.0):
    seg = np.diff(path, axis=0); L = np.hypot(seg[:, 0], seg[:, 1]); cum = np.concatenate([[0], np.cumsum(L)]); pts = []
    s = off % n_space
    while s < cum[-1]:
        i = np.searchsorted(cum, s) - 1; i = max(0, min(i, len(seg) - 1)); u = (s - cum[i]) / L[i]; pts.append(path[i] + seg[i] * u); s += n_space
    return pts
def B_blue(T, t, d):
    o = BP.copy(); lay = np.zeros((BH, BW), np.float32); draw = clamp(t / .7)
    def L(p, q, w=3): cv2.line(lay, tuple(map(int, p)), tuple(map(int, q)), 1.0, w, cv2.LINE_AA)
    # ground + school section
    L((0, 600), (BW, 600), 2)
    for (x0, y0, x1, y1) in ((420, 300, 940, 530), (420, 530, 940, 545)): cv2.rectangle(lay, (x0, y0), (x1, y1), 1.0, 3, cv2.LINE_AA)
    cv2.rectangle(lay, (420, 545), (940, 600), .55, 2, cv2.LINE_AA)                     # crawlspace
    for c in range(5):
        for r_ in range(2): cv2.rectangle(lay, (450 + c * 98, 330 + r_ * 95), (520 + c * 98, 395 + r_ * 95), .8, 2, cv2.LINE_AA)
    L((400, 300), (960, 300), 4)
    for i in range(len(PIPE) - 1): L(PIPE[i], PIPE[i + 1], 9)
    vx, vy = 200, 650; cv2.fillPoly(lay, [np.array([[vx - 22, vy - 18], [vx + 22, vy + 18], [vx + 22, vy - 18], [vx - 22, vy + 18]], np.int32)], 1.0)
    m = (np.arange(BW)[None, :] < draw * BW).astype(np.float32)
    o = o + (lay * m)[..., None] * np.array([215, 230, 255], np.float32) * .9
    # gas flow (from 'कच्ची')
    tg = T - K['w_kachi'] + .3
    if tg > 0:
        g = np.zeros((BH, BW), np.float32)
        for p in along(PIPE, 26, T * 160):
            if p[0] < 60 + tg * 600: cv2.circle(g, (int(p[0]), int(p[1])), 5, 1.0, -1, cv2.LINE_AA)
        fill = clamp((T - K['w_bina'] + .2) / 1.6)
        if fill > 0:
            cv2.rectangle(g, (422, int(598 - 52 * fill)), (938, 598), .55, -1)
            up = clamp((T - 22.6) / 1.0)
            if up > 0: cv2.rectangle(g, (422, int(545 - 240 * up)), (938, 545), .22, -1)
        g = cv2.GaussianBlur(g, (0, 0), 2.5); gl = cv2.GaussianBlur(g, (0, 0), 12)
        o = o * (1 - g[..., None] * .6) + (g[..., None] * .9 + gl[..., None] * .8) * np.array([170, 235, 90], np.float32)
        o = C.haze(o, T, np.clip(g * 1.5, 0, 1), amp=4)
    return o, False
def O_blue(cv, T, t, d):
    put(cv, tx('स्कूल', 's8', 36, (215, 230, 255)), BX + 680, BY + 270, clamp((t - .5) / .3), 'c', 0)
    put(cv, tx('पाइपलाइन', 's8', 32, (215, 230, 255)), BX + 130, BY + 700, clamp((t - .5) / .3), 'c', 0)
    labelbox(cv, 'कच्ची गैस', BX + 40, BY + 560, T - K['w_kachi'], 's8', 44, RED)
    labelbox(cv, 'बिना गंध', BX + 560, BY + 650, T - K['w_bina'], 's8', 44, (10, 10, 10))

def B_spark(T, t, d):
    o = np.zeros((BH, BW, 3), np.float32) + 3; ts = K['w_spark'] - K['spark0']; cx, cy = BW // 2, BH // 2
    if t > ts - .15:
        r = np.random.default_rng(int(T * 60)); k = clamp((t - ts + .15) / .5)
        for _ in range(50):
            a = r.uniform(0, 6.28); s = r.uniform(5, 170) * k
            cv2.line(o, (cx, cy), (int(cx + math.cos(a) * s), int(cy + math.sin(a) * s)), (255, 215, 150), 2, cv2.LINE_AA)
        o = C.bloom(o, 80, 2.2, 28)
    return o, False
def B_clock(T, t, d):
    o = np.zeros((BH, BW, 3), np.float32) + np.array([168, 22, 24], np.float32)
    o = o * (1 - .35 * np.clip(np.abs(np.linspace(-1, 1, BW))[None, :, None] ** 2, 0, 1))
    sil = np.zeros((BH, BW, 3), np.float32); G.clock(sil, T, t, cx=BW // 2, cy=BH // 2, r=320)
    m = (sil.mean(2, keepdims=True) > 1).astype(np.float32); return o * (1 - .14 * m), False
def B_end(T, t, d):
    o, _ = V.B_end(T, t, d)
    kb = clamp((T - 60.85) / .35)
    return o * (1 - .75 * kb), False
def O_end(cv, T, t, d):
    if T < 60.85:
        tm = K['w_main'] - .35
        pop(cv, 'आपको', 's8', 64, CW / 2, BY + BH / 2 - 150, T - 59.2, WHITE, .2, .6)
        pop(cv, 'बचाने के लिए', 't7', 210, CW / 2, BY + BH / 2 + 20, T - tm, WHITE, .3, .7)
    else:
        tb = T - 60.85; k = clamp(tb / .35); bounce = 1 + .12 * math.sin(min(1, tb / .5) * math.pi) * (1 - min(1, tb / .5))
        put(cv, LOGO[230], CW / 2, BY + BH / 2 - 90, k, 'c', .6, 0, (.6 + .4 * eio(k)) * bounce)
        pop(cv, 'FreshNestHub', 's8', 64, CW / 2, BY + BH / 2 + 90, tb - .15, WHITE, .25, .6)
        pop(cv, '@fnhtruths', 's6', 38, CW / 2, BY + BH / 2 + 165, tb - .3, (200, 200, 200), .25, .6)

# ---------------- timeline
S = []
def seg(a, b, B, O, tr): S.append((a, b, B, O, tr))
k = K
seg(0, k['s_kitchen'], V.B_open, V.O_open, None); seg(k['s_kitchen'], k['s_odorless'], V.B_kitchen, V.O_kitchen, 'cut')
seg(k['s_odorless'], k['s_added'], V.B_odorless, V.O_odorless, 'push'); seg(k['s_added'], k['s_ruins'], V.B_added, V.O_added, 'blur')
seg(k['s_ruins'], 12.9, B_globe, O_globe, 'glitch'); seg(12.9, k['s_texas'], V.B_ruins, V.O_ruins, 'cut')
seg(k['s_texas'], 16.0, V.B_texas, (lambda cv, T, t, d: None), 'cut'); seg(16.0, k['s_pipe'], B_texmap, O_texmap, 'cut')
seg(k['s_pipe'], k['s_walls'], B_blue, O_blue, 'push'); seg(k['s_walls'], k['s_clock'], V.B_walls, V.O_walls, 'blur')
seg(k['s_clock'], k['w_teacher'], B_clock, V.O_clock, 'glitch'); seg(k['w_teacher'], k['spark0'], V.B_teacher, V.O_teacher, 'push')
seg(k['spark0'], k['s_blast'], B_spark, V.O_spark, 'cut'); seg(k['s_blast'], k['s_cost'], V.B_blast, V.O_blast, 'cut')
seg(k['s_cost'], k['s_human'], V.B_cost, V.O_cost, 'glitch'); seg(k['s_human'], k['s_voice'], V.B_human, V.O_human, 'blur')
seg(k['s_voice'], 46.85, V.B_law, V.O_law, 'push'); seg(46.85, k['s_today'], V.B_voice, V.O_voice, 'blur')
seg(k['s_today'], k['s_rules'], V.B_today, V.O_today, 'push'); seg(k['s_rules'], k['s_end'], V.B_rules, V.O_rules, 'blur'); seg(k['s_end'], TOTAL, B_end, O_end, 'blur')
V.CAP_OFF[:] = [(0, 3.0), (3.4, 4.6), (4.6, 7.98), (8.7, 10.1), (12.9, 15.0), (15.0, 16.0), (17.1, 23.6), (28.9, K['w_teacher']), (K['s_cost'], K['s_human']),
                (K['s_voice'], 46.85), (K['w_ethyl'] - .1, K['s_rules']), (K['s_rules'], K['s_end']), (59.1, TOTAL)]
V.caption.__globals__['BY'] = BY

def band_at(i, T):
    a, b, fn, _, _ = S[i]; return fn(T, T - a, b - a)[0]
def frame(T):
    for i, (a, b, fn, ov, tr) in enumerate(S):
        if a <= T < b or i == len(S) - 1: break
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
        o = V.glitch(o if t > .07 else band_at(i - 1, T), T, 1.0)
    band = C.finish(np.clip(o, 0, 255), T, grain=5, vig=not dark).astype(np.float32)
    if fn is V.B_blast:                                   # frame break: card blows up to full screen, then snaps back
        fl = math.exp(-t * 7); r = np.random.default_rng(int(T * 90)); shk = 40 * math.exp(-t * 5)
        sc = lerp(2.6, 2.45, clamp(t / d))
        cv = compose(band, T, sc, (r.normal(0, shk), r.normal(0, shk))); cv = cv * (1 - fl) + 255 * fl
        return np.clip(cv, 0, 255).astype(np.uint8)
    cv = compose(band, T)
    brand_bug(cv); chapter(cv, T)
    ov(cv, T, t, d)
    V.caption(cv, T, dark)
    return np.clip(cv, 0, 255).astype(np.uint8)

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for s in sys.argv[2:]: Image.fromarray(frame(float(s))).save(f'/tmp/g4_{s}.jpg', quality=88)
    else:
        a, b = float(sys.argv[2]), float(sys.argv[3]); os.makedirs(P + '/segs4', exist_ok=True); out = f'{P}/segs4/seg_{a:05.1f}.mp4'
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{CW}x{CH}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', out + '.tmp.mp4'], stdin=subprocess.PIPE)
        for n in range(int(round(a * FPS)), int(round(b * FPS))): p.stdin.write(frame(n / FPS).tobytes())
        p.stdin.close(); p.wait(); os.replace(out + '.tmp.mp4', out)
