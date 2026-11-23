import sys, os, json, math
sys.path.insert(0, '/home/claude/coffee')
from kit import *
D = '/home/claude/coffee'
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




def cup(c, x, y, s, T, steam=True):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.scale(1, .3); c.arc(12, 220 / .3 + 40, 260, 0, 6.29); c.restore(); c.set_source_rgba(0, 0, 0, .25); c.fill()
    c.save(); c.scale(1, .3); c.arc(0, 200 / .3, 250, 0, 6.29); c.restore(); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
    c.arc(170, 20, 70, -1.4, 1.4); c.set_line_width(34); c.set_source_rgba(*hx('1C1614')); c.stroke()
    c.arc(170, 20, 70, -1.4, 1.4); c.set_line_width(20); c.set_source_rgba(*hx(RED)); c.stroke()
    c.move_to(-170, -90); c.line_to(-140, 170); c.curve_to(-60, 210, 60, 210, 140, 170); c.line_to(170, -90); c.close_path()
    c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 9); c.stroke()
    c.save(); c.scale(1, .28); c.arc(0, -90 / .28, 170, 0, 6.29); c.restore(); c.set_source_rgba(*hx('4A2A17')); c.fill_preserve(); ink(c, 7); c.stroke()
    if steam:
        for k in (-1, 0, 1):
            ph = T * 2 + k
            c.move_to(k * 70, -140)
            for j in range(1, 7): c.line_to(k * 70 + 22 * math.sin(ph + j), -140 - j * 32)
            c.set_source_rgba(*hx('1C1614', .55)); c.set_line_width(9); c.stroke()
    c.restore()

def brain(c, x, y, s, glow=0.0, fast=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.scale(1.3, 1); c.arc(10 / 1.3, 14, 160, 0, 6.29); c.restore(); c.set_source_rgba(0, 0, 0, .25); c.fill()
    c.save(); c.scale(1.3, 1); c.arc(0, 0, 160, 0, 6.29); c.restore(); c.set_source_rgba(*hx(PINK)); c.fill_preserve(); ink(c, 9); c.stroke()
    for a, b, d in ((-150, -40, 1), (-60, -110, -1), (40, -60, 1), (120, 10, -1), (-90, 60, 1), (20, 90, -1)):
        c.move_to(a, b); c.curve_to(a + 30, b - 40 * d, a + 70, b + 40 * d, a + 100, b); c.set_source_rgba(*hx('1C1614', .7)); c.set_line_width(7); c.stroke()
    if glow > 0:
        for r, al in ((90, .25), (60, .45), (36, .9)):
            c.arc(-40, 40, r * (.4 + .6 * glow), 0, 6.29); c.set_source_rgba(*hx(YEL, al * glow)); c.fill()
    if fast > 0:
        c.move_to(40, -150); c.line_to(-10, -40); c.line_to(30, -40); c.line_to(-20, 60); c.line_to(70, -70); c.line_to(30, -70); c.line_to(70, -150); c.close_path()
        c.set_source_rgba(*hx(YEL, fast)); c.fill_preserve(); ink(c, 6, fast); c.stroke()
    c.restore()

def gut(c, x, y, s, T, pulse=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    pts = [(-120, -140), (120, -140), (120, -60), (-110, -60), (-110, 20), (110, 20), (110, 100), (-100, 100), (-100, 170)]
    for w, col in ((70, '1C1614'), (52, 'F29C9C')):
        c.move_to(*pts[0])
        for p in pts[1:]: c.line_to(*p)
        c.set_line_join(1); c.set_line_cap(1); c.set_source_rgba(*hx(col)); c.set_line_width(w); c.stroke()
    if pulse > 0:
        n = len(pts) - 1; u = (T * .8) % 1.0; i = int(u * n); f = u * n - i
        px = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f; py = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f
        c.arc(px, py, 22, 0, 6.29); c.set_source_rgba(*hx(YEL, pulse)); c.fill_preserve(); ink(c, 4, pulse); c.stroke()
    c.restore()

def mouse(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(150, 40); c.curve_to(260, 60, 280, -40, 330, 10); c.set_source_rgba(*hx('1C1614')); c.set_line_width(10); c.stroke()
    c.save(); c.scale(1.5, 1); c.arc(0, 20, 110, 0, 6.29); c.restore(); c.set_source_rgba(*hx('B9B4AE')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.arc(-150, -60, 60, 0, 6.29); c.set_source_rgba(*hx('B9B4AE')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(-150, -60, 34, 0, 6.29); c.set_source_rgba(*hx(PINK)); c.fill()
    c.move_to(-130, -30); c.curve_to(-200, -30, -250, 0, -270, 40); c.line_to(-140, 60); c.close_path(); c.set_source_rgba(*hx('B9B4AE')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(-200, 0, 12 if (T % 3) > .15 else 3, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(-272, 40, 14, 0, 6.29); c.set_source_rgba(*hx(PINK)); c.fill_preserve(); ink(c, 4); c.stroke()
    c.restore()

def heart(c, x, y, s, col=RED):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, 30); c.curve_to(-60, -20, -30, -60, 0, -30); c.curve_to(30, -60, 60, -20, 0, 30); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 5); c.stroke()
    c.restore()

def L_(fn): return cairo_layer(fn)

def s_hook(fr, T):
    bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    overlay(fr, L_(lambda c: cup(c, CX, 1060, 1.15 * back(clamp((T + .4) / .4)), T)))
    t1 = wfind(0, 'awful')
    if T > t1: burst(fr, 'YUCK!', 830, 850, T - t1, r=130, col=YEL, size=56, rot=10)
    if T > wfind(0, 'love'): overlay(fr, L_(lambda c: heart(c, 260, 870, 1.4 * back(clamp((T - wfind(0, 'love')) / .3)))))
    tape(fr, 'YOUR FIRST SIP', CX, 470, T + .3, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'WHY YOU LOVE COFFEE', 600, T + .3, size=104, fill=YEL, rot=-2)

def s_gut(fr, T):
    fr[:] = essay_slide(T, [("NOT YOUR TONGUE.", 'grey'), ('YOUR GUT.', 'hl')], [S[1], wfind(1, 'your gut')], size=124)
    lt = T - S[1]
    overlay(fr, L_(lambda c: gut(c, CX, 1110, 1.5 * back(clamp((lt - .2) / .4)), T, 1.0)))

def s_fast(fr, T):
    lt = T - S[2]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'SIGNAL 1', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    t1 = wfind(2, 'fast')
    overlay(fr, L_(lambda c: brain(c, CX, 1000, 1.5 * back(clamp(lt / .35)), 0, clamp((T - t1) / .2) if T > t1 else 0)))
    if T > wfind(2, 'second'): chip(fr, 'FAST DOPAMINE: SECONDS', CX, 1290, T - wfind(2, 'second'), YEL, 40, -2); title(fr, 'TASTE = INSTANT HIT', 620, T - wfind(2, 'second'), size=92, fill=YEL)

def s_slow(fr, T):
    lt = T - S[3]; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'SIGNAL 2', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    t1 = wfind(3, 'gut')
    def dr(c):
        brain(c, 740, 900, .8)
        gut(c, 330, 1130, 1.1 * back(clamp(lt / .35)), T, 1.0 if T > t1 else 0)
        if T > t1:
            u = clamp((T - t1) / 1.5)
            c.move_to(420, 960); c.curve_to(500, 900, 560, 900, 420 + 200 * u, 960 - 100 * u); c.set_source_rgba(*hx(RED)); c.set_line_width(14); c.set_dash([24, 16]); c.stroke(); c.set_dash([])
    overlay(fr, L_(dr))
    if T > wfind(3, 'slow'): title(fr, 'A SLOW ONE TOO', 620, T - wfind(3, 'slow'), size=104, fill=YEL)

def s_build(fr, T):
    lt = T - S[4]; bg(fr, T, 'F7E3C8'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'GUT SENSORS', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    t1 = wfind(4, 'dopamine')
    g = clamp((T - t1) / 3) if T > t1 else 0
    overlay(fr, L_(lambda c: brain(c, CX, 1010, 1.5 * back(clamp(lt / .35)), g)))
    if T > wfind(4, 'sugar'): chip(fr, 'SUGAR', 250, 760, T - wfind(4, 'sugar'), YEL, 44, -6)
    if T > wfind(4, 'fat'): chip(fr, 'FAT', 830, 760, T - wfind(4, 'fat'), CYAN, 44, 6)
    if T > t1: chip(fr, 'AMYGDALA', 450, 1310, T - t1, 'FFFFFF', 38, -3); chip(fr, 'BUILDS FOR MINUTES', 760, 1240, T - t1 - .4, RED, 34, 3)
    if T > wfind(4, 'spot'): title(fr, 'DOPAMINE, SLOWLY', 620, T - wfind(4, 'spot'), size=100, fill=YEL)

def s_mice(fr, T):
    lt = T - S[5]; bg(fr, T, 'C9DDF0'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'THE MOUSE TEST', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    def dr(c):
        mouse(c, 620, 1030, 1.2 * back(clamp(lt / .35)), T)
        c.move_to(620, 1060); c.line_to(620, 1360); c.set_source_rgba(*hx('1C1614')); c.set_line_width(20); c.stroke()
        c.move_to(620, 1060); c.line_to(620, 1360); c.set_source_rgba(*hx('F4E8B8')); c.set_line_width(12); c.stroke()
    overlay(fr, L_(dr))
    if T > wfind(5, 'stomach'): chip(fr, 'STRAIGHT TO THE STOMACH', 420, 760, T - wfind(5, 'stomach'), YEL, 36, -3)
    t2 = wfind(5, 'no tasting')
    if T > t2: xstamp(fr, 300, 1000, T - t2, .8); chip(fr, 'NO TASTING', 300, 1180, T - t2, 'FFFFFF', 40, 4)

def s_block(fr, T):
    fr[:] = essay_slide(T, [('BLOCK THE SLOW SIGNAL...', 'grey'), ('NO FLAVOR LEARNING.', 'hl')], [S[6], wfind(6, 'mice')], size=88)
    lt = T - S[6]
    overlay(fr, L_(lambda c: mouse(c, 640, 1120, .9 * back(clamp((lt - .2) / .35)), T)))
    if T > wfind(6, 'block'): xstamp(fr, 300, 1100, T - wfind(6, 'block') - .3, .6)

def s_prefer(fr, T):
    lt = T - S[7]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, 'FLIP IT ON', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    def dr(c):
        mouse(c, 560, 1080, 1.1, T)
        c.move_to(860, 940); c.curve_to(940, 1040, 940, 1120, 860, 1140); c.curve_to(780, 1120, 780, 1040, 860, 940)
        c.set_source_rgba(*hx(CYAN)); c.fill_preserve(); ink(c, 7); c.stroke()
        if T > wfind(7, 'prefer'):
            k = T - wfind(7, 'prefer')
            for j, (hx_, hy) in enumerate(((380, 840), (520, 760), (680, 820))):
                if k > j * .15: heart(c, hx_, hy - 30 * ((k * .5 + j * .3) % 1), 1.2 * back(clamp((k - j * .15) / .3)))
    overlay(fr, L_(dr))
    if T > wfind(7, 'zero'): chip(fr, '0-CALORIE FLAVOR', 820, 1270, T - wfind(7, 'zero'), YEL, 36, 3)
    if T > wfind(7, 'prefer'): title(fr, 'NOW IT LOVES IT', 620, T - wfind(7, 'prefer'), size=104, fill=YEL)

def s_coffee(fr, T):
    lt = T - S[8]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    tape(fr, 'SO, COFFEE', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    t1 = wfind(8, 'linked')
    def dr(c):
        cup(c, 300, 1100, .75 * back(clamp(lt / .35)), T)
        brain(c, 780, 950, .8, clamp((T - t1) / 1) if T > t1 else 0)
        if T > t1:
            u = clamp((T - t1) / .6); c.move_to(420, 960); c.line_to(420 + 220 * u, 960 - 30 * u); c.set_source_rgba(*hx(RED)); c.set_line_width(16); c.stroke()
    overlay(fr, L_(dr))
    if T > wfind(8, 'bitter'): chip(fr, 'BITTER TASTE', 300, 1340, T - wfind(8, 'bitter'), 'FFFFFF', 38, -3)
    if T > wfind(8, 'caffeine'): chip(fr, '= CAFFEINE KICK', 780, 1240, T - wfind(8, 'caffeine'), YEL, 38, 3); title(fr, 'TASTE + KICK, LINKED', 620, T - wfind(8, 'caffeine'), size=90, fill=YEL)
    chip(fr, 'MOUSE STUDY + HUMAN BRAIN SCANS', CX, 770, lt - .6, CYAN, 28, -1)

def s_end(fr, T):
    fr[:] = essay_slide(T, [('YOUR GUT', 'main'), ('TRAINED YOUR BRAIN.', 'hl')], [S[9], wfind(9, 'trained')], size=116)
    lt = T - S[9]
    overlay(fr, L_(lambda c: (gut(c, 330, 1130, .9 * back(clamp(lt / .35)), T, 1.0), brain(c, 760, 1080, .8 * back(clamp((lt - .3) / .35)), .8))))

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_gut), (S[3], s_fast), (S[4], s_slow), (S[5], s_build), (S[6], s_mice), (S[7], s_block), (S[8], s_prefer), (S[9], s_coffee), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'awful'), wfind(6, 'block'), wfind(7, 'prefer')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Study: UCSF, Nature (2026)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
