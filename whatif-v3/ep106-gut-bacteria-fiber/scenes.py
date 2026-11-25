import sys, os, json, math
sys.path.insert(0, '/home/claude/gut')
from kit import *
D = '/home/claude/gut'
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






GUTW = 'F08A9A'; MUC = 'C8E07A'; LUM = 'FFE9D6'; PURP = '9B5DE5'

def gut(c, x, y, s, T, mucus=1.0):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.arc(12, 16, 300, 0, 6.29); c.set_source_rgba(0, 0, 0, .22); c.fill()
    c.arc(0, 0, 300, 0, 6.29); c.set_source_rgba(*hx(GUTW)); c.fill_preserve(); ink(c, 9); c.stroke()
    c.arc(0, 0, 255, 0, 6.29); c.set_source_rgba(*hx('E06C80')); c.set_line_width(6); c.stroke()
    m = 70 * clamp(mucus)
    c.arc(0, 0, 215, 0, 6.29); c.set_source_rgba(*hx(MUC, .95)); c.fill()
    c.arc(0, 0, 215 - m, 0, 6.29); c.set_source_rgba(*hx(LUM)); c.fill()
    for k in range(18):
        a = k / 18 * 6.283 + .05 * math.sin(T * 3 + k)
        c.arc(215 * math.cos(a), 215 * math.sin(a), 22, 0, 6.29); c.set_source_rgba(*hx(GUTW)); c.fill()
    c.arc(0, 0, 215 - m, 0, 6.29); ink(c, 3, .35); c.stroke()
    c.arc(0, 0, 300, 0, 6.29); ink(c, 9); c.stroke()
    c.restore()

def microbe(c, x, y, s, T, col='5BC0BE', chomp=1.0, ph=0.0, happy=False, ang=0.0):
    if s < .01: return
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    w = math.sin(T * 6 + ph)
    c.move_to(-60, 0)
    for k in range(9): c.line_to(-60 - 14 * k, 14 * math.sin(T * 14 + k + ph))
    ink(c, 6); c.stroke()
    c.save(); c.scale(1.25 + .06 * w, 1 - .06 * w); c.arc(0, 0, 60, 0, 6.29); c.restore()
    c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    for ex in (8, 38): c.arc(ex, -18, 12, 0, 6.29); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 3); c.stroke(); c.arc(ex + 3, -18, 5, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    o = .5 + .5 * math.sin(T * 16 + ph) if chomp > 0 else 0
    if happy: c.arc(28, 14, 20, .2, 2.9); ink(c, 6); c.stroke()
    else:
        c.move_to(10, 18); c.line_to(60, 8 - 18 * o); c.line_to(60, 22 + 18 * o); c.close_path(); c.set_source_rgba(*hx('7A1C2C')); c.fill_preserve(); ink(c, 5); c.stroke()
        for tx in (30, 45): c.move_to(tx, 13 - 8 * o); c.line_to(tx + 5, 20 - 8 * o); c.line_to(tx + 10, 13 - 8 * o); c.set_source_rgba(1, 1, 1, 1); c.fill()
    c.restore()

def broccoli(c, x, y, s, T=0, bite=0.0):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(.06 * math.sin(T * 3))
    c.move_to(-35, 0); c.line_to(-25, 180); c.line_to(25, 180); c.line_to(35, 0); c.close_path(); c.set_source_rgba(*hx('9BCB6A')); c.fill_preserve(); ink(c, 7); c.stroke()
    for bx, by, r in ((-70, -20, 70), (0, -70, 85), (75, -15, 70), (-30, 20, 55), (40, 25, 55)):
        r *= (1 - .5 * bite); c.arc(bx, by, r, 0, 6.29); c.set_source_rgba(*hx('3FAE5A')); c.fill_preserve(); ink(c, 7); c.stroke()
        c.arc(bx - r * .3, by - r * .3, r * .25, 0, 6.29); c.set_source_rgba(*hx('6FD47E')); c.fill()
    c.restore()

def cloud(c, x, y, s, a=1.0, col=PURP):
    if s < .01 or a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    for bx, by, r in ((-40, 0, 40), (0, -25, 50), (45, 0, 40), (0, 15, 40)):
        c.arc(bx, by, r, 0, 6.29); c.set_source_rgba(*hx(col, .85 * a)); c.fill()
    c.restore()

def bean(c, x, y, s, rot=0, col='A0522D'):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.save(); c.scale(1.5, 1); c.arc(0, 0, 40, 0, 6.29); c.restore(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 6); c.stroke()
    c.arc(-10, -12, 10, 0, 6.29); c.set_source_rgba(1, 1, 1, .5); c.fill()
    c.restore()

def mouse(c, x, y, s, T):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(150, 40); c.curve_to(260, 60, 260, -60 + 30 * math.sin(T * 4), 330, -40); ink(c, 9); c.stroke()
    c.save(); c.scale(1.5, 1); c.arc(0, 0, 110, 0, 6.29); c.restore(); c.set_source_rgba(*hx('B8B8C4')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.arc(-150, -40, 75, 0, 6.29); c.set_source_rgba(*hx('B8B8C4')); c.fill_preserve(); ink(c, 8); c.stroke()
    for ex, ey in ((-170, -120), (-100, -115)): c.arc(ex, ey, 45, 0, 6.29); c.set_source_rgba(*hx('F4A6B8')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(-180, -50, 10, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(-222, -30, 14, 0, 6.29); c.set_source_rgba(*hx(PINK)); c.fill_preserve(); ink(c, 4); c.stroke()
    c.restore()

def phone(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    def rr(x0, y0, w, h, r):
        c.new_sub_path(); c.arc(x0 + w - r, y0 + r, r, -1.57, 0); c.arc(x0 + w - r, y0 + h - r, r, 0, 1.57); c.arc(x0 + r, y0 + h - r, r, 1.57, 3.14); c.arc(x0 + r, y0 + r, r, 3.14, 4.71); c.close_path()
    rr(-190 + 12, -330 + 16, 380, 660, 50); c.set_source_rgba(0, 0, 0, .25); c.fill()
    rr(-190, -330, 380, 660, 50); c.set_source_rgba(*hx('1C1614')); c.fill()
    rr(-165, -290, 330, 580, 24); c.set_source_rgba(1, 1, 1, 1); c.fill()
    c.restore()

MICS = [('5BC0BE', 0.0), ('F28C28', 1.3), ('9B7EDE', 2.6), ('3FAE5A', 3.9), ('FF7AA8', 5.1)]
def swarm(c, x, y, s, T, rad, n=5, chomp=1.0, happy=False, cols=None):
    for k in range(n):
        col, ph = MICS[k % 5]
        if cols: col = cols
        a = ph + T * .25; r = rad + 12 * math.sin(T * 2 + ph)
        microbe(c, x + r * math.cos(a) * s, y + r * math.sin(a) * s, .55 * s, T, col, chomp, ph, happy, a)

def L_(fn): return cairo_layer(fn)
def pop(T, t0, d=.35): return back(clamp((T - t0) / d))

def s_hook(fr, T):
    bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .16, CX, 1120)
    rad = 70 + 60 * eout(clamp(T / 3.5))
    overlay(fr, L_(lambda c: (gut(c, CX, 1120, .95 * pop(T, -.4), T, 1.0), swarm(c, CX, 1120, .95, T, rad))))
    tape(fr, 'SKIP YOUR VEGGIES?', CX, 430, T + .4, col=RED, size=54, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'YOUR GUT IS', 565, T + .4, size=118, fill='FFFFFF', rot=-2); title(fr, 'ON THE MENU', 700, T + .3, size=132, fill=YEL, rot=-2)
    t = wfind(0, 'you.'); 
    if T > t: burst(fr, 'YOU!', 850, 880, T - t, r=120, col=YEL, size=70, rot=8)

def s_lining(fr, T):
    fr[:] = essay_slide(T, [('NOT YOUR FOOD.', 'grey'), ('YOUR GUT LINING.', 'hl')], [S[1], wfind(1, 'gut')], size=104)
    overlay(fr, L_(lambda c: (gut(c, CX, 1130, .7, T, 1.0 + .15 * math.sin(T * 5)), swarm(c, CX, 1130, .7, T, 70, 3, 0))))
    t = wfind(1, 'slimy')
    if T > t: chip(fr, 'SLIMY MUCUS SHIELD', CX, 860, T - t, YEL, 36, -3)

def s_fiber(fr, T):
    lt = T - S[2]; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .12, CX, 1100)
    tape(fr, "HERE'S WHY", CX, 450, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    bite = .5 * clamp(lt / 3.5)
    def dr(c):
        broccoli(c, CX, 1060, .95 * pop(T, S[2]), T, bite)
        for k, (col, ph) in enumerate(MICS[:4]):
            a = ph + T * .6; microbe(c, CX + 260 * math.cos(a), 1080 + 200 * math.sin(a), .6 * pop(T, S[2] + .2 + k * .1), T, col, 1, ph, False, a + 3.14)
    overlay(fr, L_(dr))
    t = wfind(2, 'fiber')
    if T > t: title(fr, 'FIBER = THEIR FOOD', 620, T - t, size=100, fill=YEL)
    t = wfind(2, 'favorite')
    if T > t: chip(fr, 'FAVORITE MEAL', 800, 1380 - 60, T - t, 'FFFFFF', 36, 3)

def s_runout(fr, T):
    lt = T - S[3]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .12, CX, 1120)
    tape(fr, 'NO FIBER LEFT?', CX, 450, lt, col=RED, size=60, font=LUCKY, rot=-2, tcol='FFFFFF')
    tm = wfind(3, 'turn'); mu = 1 - .6 * eout(clamp((T - tm) / 2.5)); rad = 60 + 110 * eout(clamp((T - tm) / 1.2))
    overlay(fr, L_(lambda c: (gut(c, CX, 1120, .9, T, mu), swarm(c, CX, 1120, .9, T, rad))))
    t = wfind(3, 'mucus')
    if T > t: title(fr, 'THEY EAT THE SHIELD', 620, T - t, size=96, fill=YEL)
    t = wfind(3, 'fiber')
    if T > t and T < tm: chip(fr, 'PLATE: EMPTY', 780, 760, T - t, 'FFFFFF', 34, 4)

def s_harm(fr, T):
    lt = T - S[4]; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .1, CX, 1120)
    tape(fr, 'CHEW, CHEW...', CX, 450, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    def dr(c):
        gut(c, CX, 1120, .9, T, .4); swarm(c, CX, 1120, .9, T, 170)
        for k in range(6):
            u = (lt * .5 + k / 6) % 1; a = k * 1.05
            cloud(c, CX + 160 * math.cos(a) * (1 + u), 1120 + 160 * math.sin(a) * (1 + u) - 120 * u, .5 + .8 * u, clamp(lt * 2) * (1 - u))
    overlay(fr, L_(dr))
    t = wfind(4, 'chemicals')
    if T > t: title(fr, 'LINKED TO HARM', 620, T - t, size=110, fill='FFFFFF')

def s_tag(fr, T):
    lt = T - S[5]; bg(fr, T, 'FFE08A', .6); rays(fr, T, 'FFFFFF', .2, CX, 1080)
    tape(fr, 'TAG THAT FRIEND', CX, 450, lt, col=RED, size=64, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: (phone(c, CX, 1080, .85 * pop(T, S[5] - .1)), broccoli(c, CX, 1150, .45 * pop(T, S[5] + .3), T * 2))))
    chip(fr, '@YOUR_FRIEND', CX, 900, lt - .2, CYAN, 40, 0)
    t = wfind(5, 'vegetable')
    if T > t: burst(fr, '0 VEGGIES', 830, 700, T - t, r=140, col=YEL, size=44, rot=10)
    t = wfind(5, 'week')
    if T > t: chip(fr, 'ALL WEEK', 300, 1330 - 60, T - t, 'FFFFFF', 40, -4)

def s_twist(fr, T):
    tb = wfind(6, 'those')
    if T < tb:
        fr[:] = essay_slide(T, [('TWIST:', 'hl'), ('PLANT PROTEINS', 'main'), ("YOU CAN'T DIGEST.", 'grey')], [S[6], wfind(6, 'plants'), wfind(6, 'digest') - .3], size=104)
        def dr(c):
            for k in range(9): bean(c, 300 + (k % 5) * 120 + (k // 5) * 60, 1150 + (k // 5) * 80, .8 * pop(T, S[6] + .6 + k * .06), k * .7, ('A0522D', 'E9C46A', '3FAE5A')[k % 3])
        overlay(fr, L_(dr)); return
    lt = T - tb; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .14, CX, 1100)
    tape(fr, 'PROTEINS IMITATING FIBER', CX, 450, lt, col='FFFFFF', size=48, font=LUCKY, rot=-2)
    def dr2(c):
        for k in range(7): bean(c, CX - 240 + k * 80, 1200 + 20 * math.sin(k), .8, k * .6, ('A0522D', 'E9C46A', '3FAE5A')[k % 3])
        for k, (col, ph) in enumerate(MICS[:4]):
            x = 220 + k * 210; y = 1010 + 20 * math.sin(T * 3 + ph); microbe(c, x, y, .6 * pop(T, tb + k * .1), T, col, 0, ph, True)
            for j in range(3):
                u = (T * .7 + j / 3 + ph) % 1; c.arc(x + 30 * math.sin(j + ph), y - 90 - 140 * u, 12 * (1 - u) + 4, 0, 6.29); c.set_source_rgba(*hx('FFFFFF', 1 - u)); c.fill()
    overlay(fr, L_(dr2))
    t = wfind(6, 'helpful')
    if T > t: title(fr, 'HELPFUL CHEMICALS', 640, T - t, size=100, fill=YEL)

def s_mice(fr, T):
    fr[:] = essay_slide(T, [('MOSTLY IN MICE.', 'grey'), ('STILL EARLY.', 'hl')], [S[7], wfind(7, 'early') - .2], size=110)
    overlay(fr, L_(lambda c: mouse(c, CX + 40, 1150, .9 * pop(T, S[7] + .1), T)))

def s_end(fr, T):
    lt = T - S[8]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .16, CX, 1120)
    tf = wfind(8, 'feed on')
    def dr(c):
        gut(c, CX, 1120, .9, T, 1.0)
        if T < tf: broccoli(c, CX, 1110, .55, T, .3 * clamp(lt / 2)); swarm(c, CX, 1120, .9, T, 150, 4, 1)
        else: swarm(c, CX, 1120, .9, T, 60 + 120 * eout(clamp((T - tf) / .6)), 5, 1)
    overlay(fr, L_(dr))
    t = wfind(8, 'fiber')
    if T > t: title(fr, 'FEED THEM FIBER', 560, T - t, size=112, fill=YEL)
    if T > tf: tape(fr, '...OR THEY FEED ON YOU', CX, 700, T - tf, col=RED, size=54, font=LUCKY, rot=2, tcol='FFFFFF')

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_lining), (S[3], s_fiber), (S[4], s_runout), (S[5], s_harm), (S[6], s_tag), (S[7], s_twist), (S[8], s_mice), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'you.'), wfind(3, 'mucus'), wfind(8, 'feed on')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Research: Ludwig Cancer Research Princeton, PNAS (2026)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
