import sys, os, json, math
sys.path.insert(0, '/home/claude/barreleye')
from kit import *
D = '/home/claude/barreleye'
L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]
END = E[-1] + 0.3; TOTAL = END + 1.6
def wt(i, frac): return S[i] + L[i]['dur'] * frac
def wfind(i, word):
    tx = L[i]['text'].lower(); k = tx.find(word.lower()); return wt(i, k / max(1, len(tx)))
def st(name, **kw):
    return load_st(name, **kw) if os.path.exists(f'{D}/st/{name}.png') else None
PHOTO = {}
def photo(name, w, h, focus=(.5, .5)):
    k = (name, w, h, focus)
    if k not in PHOTO:
        p = f'{D}/ph/{name}.jpg'
        PHOTO[k] = panel_img(comic_photo(p, w, h, focus)) if os.path.exists(p) else None
    return PHOTO[k]
exec(open(D + '/common_part.py').read())
def chip(fr, txt, cx, cy, t, col=CYAN, size=40, rot=0): tape(fr, txt, cx, cy, t, col=col, size=size, font=INTER, rot=rot)
def sk(fr, im, x, y, T, k, sc, rot=0, t=1.0):
    if im is not None: sticker(fr, im, x, y, T, k, sc, rot, t)
def stat(fr, big, small, cx, cy, t, col=RED, rot=-3, size=130):
    if t <= 0: return
    title(fr, big, cy, t, size=size, fill='FFFFFF' if col == RED else YEL, rot=rot, cx=cx)
    tape(fr, small, cx, cy + size * .8, t - .1, col=col, size=40, font=LUCKY, rot=rot + 1, tcol='FFFFFF' if col == RED else '1C1614')

sys.path.insert(0, '/home/claude/samples')
import essay as ES

def bg(fr, T, tint='F3E3B3', m=.55): fr[:] = paper(tint, m)
def essay_slide(T, lines, t0s, size=128):
    fr = ES.base(True); ES.headline(fr, lines, T, t0s, y=400, dark=True, size=size); return fr






def bird(c, x, y, s, T, fly=0.0, flip=False, col='8A93A6'):
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    flap = math.sin(T * 22) if fly > 0 else 0
    c.save(); c.scale(1.4, 1); c.arc(0, 0, 80, 0, 6.29); c.restore(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    c.move_to(100, -10); c.line_to(170, -40); c.line_to(160, 30); c.close_path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 6); c.stroke()
    c.arc(-95, -60, 50, 0, 6.29); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(-80, -30, 34, .5, 2.6); c.set_source_rgba(*hx('6FB39A', .8)); c.set_line_width(10); c.stroke()
    c.move_to(-140, -65); c.line_to(-175, -55); c.line_to(-140, -48); c.close_path(); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 4); c.stroke()
    c.arc(-108, -70, 9, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    wy = -60 * fly * (1 + flap)
    c.move_to(-20, -20); c.curve_to(10, -60 + wy, 70, -60 + wy, 90, -30 + wy * .6); c.curve_to(60, 0, 20, 10, -20, -20); c.set_source_rgba(*hx('6D7587')); c.fill_preserve(); ink(c, 6); c.stroke()
    if fly < .5:
        for lx in (-20, 20): c.move_to(lx, 75); c.line_to(lx, 120); c.set_source_rgba(*hx('E07A5F')); c.set_line_width(8); c.stroke()
    c.restore()

def person(c, x, y, s, T, walk=0.0, hair=False, col=BLUE, flip=False):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    sw = 25 * math.sin(T * 8) * walk
    for d in (-1, 1):
        c.move_to(-15 * d, 120); c.line_to(-15 * d + sw * d, 300); c.set_source_rgba(*hx('2B2B33')); c.set_line_width(30); c.set_line_cap(1); c.stroke()
    c.move_to(-70, -60); c.curve_to(-80, 60, -60, 130, 0, 130); c.curve_to(60, 130, 80, 60, 70, -60); c.curve_to(40, -80, -40, -80, -70, -60)
    c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    if hair:
        c.move_to(-62, -150); c.curve_to(-90, -60, -70, -20, -40, -30); c.line_to(40, -30); c.curve_to(70, -20, 90, -60, 62, -150); c.close_path(); c.set_source_rgba(*hx('6B3E26')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.arc(0, -135, 58, 0, 6.29); c.set_source_rgba(*hx('F2C9A0')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(0, -168, 58, 3.3, 6.1); c.set_source_rgba(*hx('6B3E26' if hair else '3A2A20')); c.fill()
    for ex in (-20, 20): c.arc(ex, -130, 7, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.restore()






def fish(c, x, y, s, T, eye=0.0, dots=0.0, glow=1.0):
    if s < .01: return
    c.save(); c.translate(x, y + 10 * math.sin(T * 1.5)); c.scale(s, s)
    # fins
    for sy in (-1, 1):
        c.move_to(60, sy * 40); c.curve_to(160, sy * (140 + 20 * math.sin(T * 3)), 260, sy * 120, 230, sy * 30); c.close_path()
        c.set_source_rgba(*hx('3A3F55', .85)); c.fill_preserve(); ink(c, 6); c.stroke()
    c.move_to(260, 0); c.line_to(360, -70 + 10 * math.sin(T * 4)); c.line_to(360, 70 + 10 * math.sin(T * 4)); c.close_path(); c.set_source_rgba(*hx('2B2F45')); c.fill_preserve(); ink(c, 6); c.stroke()
    # body
    c.save(); c.scale(1.7, 1); c.arc(40, 30, 140, 0, 6.29); c.restore(); c.set_source_rgba(*hx('2B2F45')); c.fill_preserve(); ink(c, 8); c.stroke()
    for k in range(5): c.arc(40 + k * 40, 80, 8, 0, 6.29); c.set_source_rgba(*hx('5A6188')); c.fill()
    # mouth + nostril dots
    c.arc(-185, 70, 14, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    for k, dy in enumerate((-10, 25)):
        c.arc(-175, dy, 20, 0, 6.29); c.set_source_rgba(*hx('111318')); c.fill_preserve(); ink(c, 4); c.stroke()
        c.arc(-181, dy - 6, 6, 0, 6.29); c.set_source_rgba(1, 1, 1, .7); c.fill()
        if dots > 0:
            c.arc(-175, dy, 34 + 6 * math.sin(T * 6), 0, 6.29); c.set_source_rgba(*hx(RED, dots)); c.set_line_width(7); c.stroke()
    # dome
    c.save(); c.scale(1.5, 1); c.arc(-20, -110, 150, math.pi, 0); c.restore()
    c.set_source_rgba(.75, .95, 1, .18); c.fill_preserve(); c.set_source_rgba(1, 1, 1, .85); c.set_line_width(6); c.stroke()
    c.move_to(-170, -170); c.curve_to(-140, -230, -60, -250, 0, -245); c.set_source_rgba(1, 1, 1, .6); c.set_line_width(10); c.set_line_cap(1); c.stroke()
    # eyes: tubes, rotate from up (0) to forward (1)
    for k, ex in enumerate((-60, 30)):
        c.save(); c.translate(ex, -80); c.rotate(-math.pi / 2 * eye * .9)
        if glow > 0:
            c.arc(0, -95, 48, 0, 6.29); c.set_source_rgba(*hx('7CFF6B', .25 * glow)); c.fill()
        c.rectangle(-28, -90, 56, 100); c.set_source_rgba(*hx('2E6B3A')); c.fill_preserve(); ink(c, 5); c.stroke()
        c.arc(0, -90, 30, 0, 6.29); c.set_source_rgba(*hx('6BFF5A')); c.fill_preserve(); ink(c, 5); c.stroke()
        c.arc(-8, -98, 9, 0, 6.29); c.set_source_rgba(1, 1, 1, .9); c.fill()
        c.restore()
    c.restore()

def deep(fr, T, tint='101836', m=.9):
    bg(fr, T, tint, m)
    def sn(c):
        rng = np.random.default_rng(5)
        for k in range(70):
            x = (rng.uniform(0, W) + T * 8 * rng.uniform(.3, 1)) % W; y = (rng.uniform(0, H) + T * 20 * rng.uniform(.3, 1)) % H
            c.arc(x, y, rng.uniform(2, 5), 0, 6.29); c.set_source_rgba(1, 1, 1, .35); c.fill()
    overlay(fr, cairo_layer(sn))

def jelly(c, x, y, s, T):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    for k in range(6):
        c.move_to(-50 + k * 20, 0)
        for j in range(1, 12): c.line_to(-50 + k * 20 + 14 * math.sin(T * 2 + j * .6 + k), j * 30)
        c.set_source_rgba(*hx('F28CB1', .8)); c.set_line_width(5); c.stroke()
    for k in range(5): c.arc(0, -20 - k * 40, 34 - k * 3, 0, 6.29); c.set_source_rgba(*hx('F7B7D2', .85)); c.fill_preserve(); ink(c, 4); c.stroke()
    c.restore()

def shrimp(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.scale(1.6, 1); c.arc(0, 0, 18, 0, 6.29); c.restore(); c.set_source_rgba(*hx('F28C28')); c.fill_preserve(); ink(c, 3); c.stroke()
    c.restore()

def gauge(c, x, y, h, u):
    c.rectangle(x - 30, y, 60, h); c.set_source_rgba(1, 1, 1, .15); c.fill_preserve(); c.set_source_rgba(1, 1, 1, .8); c.set_line_width(5); c.stroke()
    c.rectangle(x - 30, y, 60, h * u); c.set_source_rgba(*hx(CYAN, .7)); c.fill()

def L_(fn): return cairo_layer(fn)

def s_hook(fr, T):
    deep(fr, T)
    overlay(fr, L_(lambda c: fish(c, CX + 40, 1110, 1.25 * back(clamp((T + .5) / .5)), T, 0, clamp((T - 1.2) / .3) if T > 1.2 else 0)))
    tape(fr, 'SEE-THROUGH HEAD', CX, 470, T + .4, col=RED, size=60, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, "THOSE AREN'T", 600, T + .4, size=120, fill='FFFFFF', rot=-2); title(fr, 'ITS EYES', 730, T + .3, size=140, fill=YEL, rot=-2)

def s_nose(fr, T):
    fr[:] = essay_slide(T, [('THOSE DOTS?', 'grey'), ('ITS NOSE.', 'hl')], [S[1], wfind(1, 'nose')], size=128)
    overlay(fr, L_(lambda c: fish(c, CX + 60, 1180, .8, T, 0, 1.0)))

def s_real(fr, T):
    lt = T - S[2]; deep(fr, T, '0E2A36')
    tape(fr, 'THE REAL EYES', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    overlay(fr, L_(lambda c: fish(c, CX + 20, 1150, 1.5, T, 0, 0, 1.0 + .5 * math.sin(T * 4))))
    if T > wfind(2, 'green'): title(fr, 'GLOWING GREEN TUBES', 620, T - wfind(2, 'green'), size=92, fill=YEL)
    if T > wfind(2, 'up'): chip(fr, 'POINTING UP', 300, 1380 - 40, T - wfind(2, 'up'), CYAN, 38, -3)

def s_depth(fr, T):
    lt = T - S[3]; deep(fr, T, '0A1028')
    tape(fr, 'WAY DOWN', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    u = eout(clamp(lt / 3))
    overlay(fr, L_(lambda c: (gauge(c, 150, 700, 700, u), fish(c, 620, 700 + 560 * u, .6, T))))
    if T > wfind(3, 'thousand'): title(fr, '~2,000 FEET DOWN', 620, T - wfind(3, 'thousand'), size=100, fill=YEL)
    if T > wfind(3, 'sunlight'): chip(fr, 'ALMOST NO SUNLIGHT', 640, 1360 - 40, T - wfind(3, 'sunlight'), 'FFFFFF', 34, 3)

def s_watch(fr, T):
    lt = T - S[4]; deep(fr, T, '101836')
    tape(fr, 'WATCHING UP', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    def dr(c):
        u = (lt * .35) % 1.4 - .2
        c.save(); c.translate(lerp(-200, W + 200, u), 760); c.scale(2.2, .7); c.arc(0, 0, 70, 0, 6.29); c.restore(); c.set_source_rgba(0, 0, 0, .55); c.fill()
        fish(c, CX + 40, 1180, 1.0, T, 0, 0, 1.0)
        c.move_to(CX - 30, 1000); c.line_to(CX - 30, 840); c.set_source_rgba(*hx('7CFF6B', .5)); c.set_line_width(8); c.set_dash([18, 14]); c.stroke(); c.set_dash([])
    overlay(fr, L_(dr))
    if T > wfind(4, 'shadows'): title(fr, 'SHADOW = FOOD', 620, T - wfind(4, 'shadows'), size=110, fill=YEL)

def s_swivel(fr, T):
    lt = T - S[5]; deep(fr, T, '0E2A36')
    tape(fr, 'DINNER SPOTTED', CX, 470, lt, col=RED, size=60, font=LUCKY, rot=-2, tcol='FFFFFF')
    t1 = wfind(5, 'swivel'); e = eout(clamp((T - t1) / .8)) if T > t1 else 0
    overlay(fr, L_(lambda c: fish(c, CX + 20, 1150, 1.45, T, e, 0, 1.0)))
    if T > t1: title(fr, 'EYES SWIVEL FORWARD', 620, T - t1, size=92, fill=YEL); burst(fr, 'INSIDE ITS HEAD', 300, 1320, T - t1, r=130, col=YEL, size=28, rot=-8)

def s_food(fr, T):
    lt = T - S[6]; deep(fr, T, '1A1236')
    tape(fr, 'THE THIEF', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    def dr(c):
        jelly(c, 300, 760, 1.2, T)
        for k in range(3): shrimp(c, 260 + k * 50, 1000 + k * 40, 1.2)
        fish(c, 740, 1180, .85, T, .8, 0, 1.0)
    overlay(fr, L_(dr))
    if T > wfind(6, 'shrimp'): chip(fr, 'TINY SHRIMP', 300, 1180, T - wfind(6, 'shrimp'), YEL, 36, -3)
    if T > wfind(6, 'stinging'): chip(fr, 'STINGING JELLY COUSINS', CX, 1360 - 40, T - wfind(6, 'stinging'), 'FFFFFF', 32, 2)

def s_rare(fr, T):
    fr[:] = essay_slide(T, [('11 SIGHTINGS', 'hl'), ('IN ~40 YEARS.', 'main')], [wfind(7, 'eleven'), wfind(7, 'forty')], size=124)
    lt = T - S[7]
    def dr(c):
        for k in range(11):
            on = lt > .4 + k * .2
            c.arc(150 + k * 78, 1150, 28, 0, 6.29); c.set_source_rgba(*hx(YEL if on else '444444')); c.fill_preserve(); ink(c, 4); c.stroke()
    overlay(fr, L_(dr))
    chip(fr, '~7,000 DIVES BY ONE OCEAN LAB', CX, 1300, lt - .6, 'FFFFFF', 30, -2)

def s_4k(fr, T):
    lt = T - S[8]; deep(fr, T)
    tape(fr, 'FINALLY', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    def dr(c):
        c.rectangle(110, 760, 860, 600); c.set_source_rgba(1, 1, 1, .9); c.set_line_width(12); c.stroke()
        for (x, y) in ((130, 780), (950, 780), (130, 1340), (950, 1340)): c.arc(x, y, 10, 0, 6.29); c.set_source_rgba(*hx(RED)); c.fill()
        fish(c, CX + 40, 1080, .9, T, 0, 0, 1.0)
    overlay(fr, L_(dr))
    title(fr, 'FILMED IN 4K', 620, lt, size=130, fill=YEL)

def s_end(fr, T):
    lt = T - S[9]; deep(fr, T)
    tape(fr, 'LOOK CLOSER', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    overlay(fr, L_(lambda c: fish(c, CX + 40, 1110, 1.25, T, 0, clamp((T - wfind(9, 'nose')) / .3) if T > wfind(9, 'nose') else 0)))
    if T > wfind(9, 'nose') - .2: title(fr, "IT'S A NOSE", 620, T - wfind(9, 'nose') + .2, size=130, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_nose), (S[3], s_real), (S[4], s_depth), (S[5], s_watch), (S[6], s_swivel), (S[7], s_food), (S[8], s_rare), (S[9], s_4k), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(1, 'nose'), wfind(5, 'swivel'), wfind(8, '4k')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Source: MBARI (Nov 2026)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
