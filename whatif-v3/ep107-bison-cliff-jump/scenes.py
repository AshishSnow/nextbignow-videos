import sys, os, json, math
sys.path.insert(0, '/home/claude/bison')
from kit import *
D = '/home/claude/bison'
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









def phone(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    def rr(x0, y0, w, h, r):
        c.new_sub_path(); c.arc(x0 + w - r, y0 + r, r, -1.57, 0); c.arc(x0 + w - r, y0 + h - r, r, 0, 1.57); c.arc(x0 + r, y0 + h - r, r, 1.57, 3.14); c.arc(x0 + r, y0 + r, r, 3.14, 4.71); c.close_path()
    rr(-190 + 12, -330 + 16, 380, 660, 50); c.set_source_rgba(0, 0, 0, .25); c.fill()
    rr(-190, -330, 380, 660, 50); c.set_source_rgba(*hx('1C1614')); c.fill()
    rr(-165, -290, 330, 580, 24); c.set_source_rgba(1, 1, 1, 1); c.fill()
    c.restore()

BR = '6B4226'; BRD = '4A2E1A'; SKY = 'BFE3F2'; DIRT = 'D9A066'; ROCK = 'B5763C'

def bison(c, x, y, s, T, run=1.0, flip=False, scared=False):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    bob = 8 * math.sin(T * 16) * run; c.translate(0, bob)
    for k, (lx, ph) in enumerate(((-110, 0), (-70, 3.1), (70, 1.6), (110, 4.7))):
        sw = 30 * math.sin(T * 16 + ph) * run
        c.move_to(lx, 40); c.line_to(lx + sw, 150); c.set_source_rgba(*hx(BRD)); c.set_line_width(26); c.set_line_cap(1); c.stroke()
    c.move_to(-160, -10); c.curve_to(-200, -30, -210, 20, -190, 30 + 10 * math.sin(T * 10)); ink(c, 7); c.stroke()
    c.save(); c.scale(1.7, 1); c.arc(-20, 0, 95, 0, 6.29); c.restore(); c.set_source_rgba(*hx(BR)); c.fill_preserve(); ink(c, 8); c.stroke()
    c.arc(80, -50, 95, 0, 6.29); c.set_source_rgba(*hx(BRD)); c.fill_preserve(); ink(c, 8); c.stroke()
    c.save(); c.translate(170, 10)
    c.move_to(-20, 40); c.line_to(10, 110); c.line_to(40, 40); c.set_source_rgba(*hx(BRD)); c.fill()
    c.arc(0, 0, 62, 0, 6.29); c.set_source_rgba(*hx(BRD)); c.fill_preserve(); ink(c, 7); c.stroke()
    for hxp in (-30, 30):
        c.move_to(hxp * .6, -50); c.curve_to(hxp * 1.4, -70, hxp * 1.6, -100, hxp * 1.1, -115); c.set_source_rgba(*hx('F2E8D5')); c.set_line_width(14); c.stroke()
    r = 12 if scared else 9
    c.arc(26, -10, r, 0, 6.29); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 3); c.stroke(); c.arc(30, -10, 5, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(52, 28, 7, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.restore(); c.restore()

def hill(c, edge_x, edge_y, T, base=1500):
    c.rectangle(0, 0, W, H); c.set_source_rgba(*hx(SKY)); c.fill()
    for k in range(3):
        x = (180 + k * 330 - T * 20) % (W + 200) - 100; cl(c, x, 330 + k * 60)
    c.move_to(-20, base); c.curve_to(edge_x * .4, base - 60, edge_x * .7, edge_y + 40, edge_x, edge_y); c.line_to(edge_x, H); c.line_to(-20, H); c.close_path()
    c.set_source_rgba(*hx(DIRT)); c.fill_preserve(); ink(c, 8); c.stroke()
    c.move_to(-20, base + 30); c.curve_to(edge_x * .4, base - 30, edge_x * .7, edge_y + 70, edge_x - 10, edge_y + 30); c.set_source_rgba(*hx('C48A50')); c.set_line_width(14); c.stroke()

def cl(c, x, y):
    for bx, by, r in ((0, 0, 40), (40, -20, 50), (85, 0, 40)):
        c.arc(x + bx, y + by, r, 0, 6.29); c.set_source_rgba(1, 1, 1, .9); c.fill()

def cliff(c, T, bones=True, crumble=0.0, top=700, x0=260, x1=820):
    c.rectangle(0, 0, W, H); c.set_source_rgba(*hx(SKY)); c.fill()
    c.move_to(x0, top); c.line_to(x1, top)
    for k in range(9): c.line_to(x1 + 20 * math.sin(k * 1.7) - 60 * crumble * (k % 3) / 2, top + (k + 1) * 90)
    c.line_to(x0, top + 900); c.close_path(); c.set_source_rgba(*hx(ROCK)); c.fill_preserve(); ink(c, 9); c.stroke()
    for k in range(5):
        c.move_to(x0, top + 120 + k * 130); c.line_to(x1 - 10, top + 140 + k * 130); c.set_source_rgba(*hx('8E5A2B')); c.set_line_width(8); c.stroke()
    if bones:
        for k in range(14):
            bx = x0 + 50 + (k * 97) % (x1 - x0 - 100); by = top + 430 + (k * 37) % 120; a = k * .9
            c.save(); c.translate(bx, by); c.rotate(a)
            c.rectangle(-30, -6, 60, 12); c.set_source_rgba(*hx('FAF3E3')); c.fill_preserve(); ink(c, 3); c.stroke()
            for ex in (-30, 30):
                for ey in (-7, 7): c.arc(ex, ey, 9, 0, 6.29); c.set_source_rgba(*hx('FAF3E3')); c.fill_preserve(); ink(c, 3); c.stroke()
            c.restore()
    c.rectangle(0, top + 900, W, H); c.set_source_rgba(*hx('C9A27A')); c.fill()
    for k in range(int(crumble * 12)):
        u = (T * .8 + k / 12) % 1; c.arc(x1 + 30 + (k * 23) % 80, top + 100 + u * 800, 14 + k % 3 * 6, 0, 6.29); c.set_source_rgba(*hx(ROCK)); c.fill_preserve(); ink(c, 3); c.stroke()

def L_(fn): return cairo_layer(fn)
def pop(T, t0, d=.35): return back(clamp((T - t0) / d))

def s_hook(fr, T):
    edge = 900; bx = 330 + 120 * eout(clamp(T / 3.4)); by = 1500 - (bx / edge) ** 1.6 * 430
    overlay(fr, L_(lambda c: (hill(c, edge, 1070, T), bison(c, bx, by - 150, .62, T, 1.0))))
    tape(fr, "YOU'RE A BISON", CX, 430, T + .4, col=RED, size=58, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'THE GROUND', 565, T + .4, size=128, fill='FFFFFF', rot=-2); title(fr, 'JUST ENDS', 700, T + .3, size=140, fill=YEL, rot=-2)
    chip(fr, '?', 930, 960, T - 1.0, 'FFFFFF', 70, 6)

def s_drop(fr, T):
    lt = T - S[1]
    overlay(fr, L_(lambda c: (cliff(c, T, False), bison(c, 560, 610 + 30 * math.sin(T * 20), .55, T, 2.0, False, True))))
    def arr(c):
        c.move_to(900, 720); c.line_to(900, 1580); c.set_source_rgba(*hx(RED)); c.set_line_width(14); c.stroke()
        for yy, d in ((720, 1), (1580, -1)): c.move_to(870, yy + 40 * d); c.line_to(900, yy); c.line_to(930, yy + 40 * d); c.stroke()
    overlay(fr, L_(arr))
    title(fr, '6-STORY DROP', 470, lt + .1, size=130, fill=YEL, rot=-3)
    chip(fr, '~20 M', 900, 1150, lt - .2, 'FFFFFF', 40, 0)

def s_bones(fr, T):
    lt = T - S[2]; overlay(fr, L_(lambda c: cliff(c, T, True)))
    tape(fr, 'TEXAS PANHANDLE', CX, 450, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    t = wfind(2, 'bones')
    if T > t: title(fr, 'FULL OF BONES', 590, T - t, size=120, fill=YEL)
    if T > t + .3: chip(fr, 'BISON BONES', 380, 1250, T - t - .3, YEL, 38, -4)

def s_trick(fr, T):
    fr[:] = essay_slide(T, [('THE TRICK:', 'hl'), ('A SLOPE THAT', 'main'), ('HIDES THE EDGE.', 'grey')], [S[3], wfind(3, 'smooth'), wfind(3, 'hides')], size=110)
    def dr(c):
        c.move_to(150, 1350); c.curve_to(400, 1330, 650, 1200, 860, 1100); c.line_to(860, 1350); c.close_path(); c.set_source_rgba(*hx(DIRT)); c.fill_preserve(); ink(c, 6); c.stroke()
        bison(c, 420 + 60 * math.sin(T), 1230, .32, T, 1.0)
    overlay(fr, L_(dr))
    t = wfind(3, 'late')
    if T > t: chip(fr, 'TOO LATE', 860, 1020, T - t, RED, 40, 6)

def s_teams(fr, T):
    lt = T - S[4]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, 'TEAMWORK', CX, 450, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    ts = [wfind(4, 'found'), wfind(4, 'steered'), wfind(4, 'waited')]
    def dr(c):
        if T > ts[0] - .2: person(c, 230, 1000, .9 * pop(T, ts[0] - .2), T, 1.0, False, BLUE); bison(c, 300, 1330, .42 * pop(T, ts[0]), T, .6)
        if T > ts[1] - .2: person(c, 540, 1000, .9 * pop(T, ts[1] - .2), T, 1.0, True, GREEN, True)
        if T > ts[2] - .2: person(c, 850, 1000, .9 * pop(T, ts[2] - .2), T, 0.0, False, 'F28C28')
    overlay(fr, L_(dr))
    for k, (lab, col) in enumerate((('FIND', 'FFFFFF'), ('STEER', YEL), ('WAIT BELOW', 'FFFFFF'))):
        if T > ts[k]: chip(fr, lab, 230 + k * 310, 720, T - ts[k], col, 36, (-3, 0, 3)[k])
    chip(fr, 'PROBABLY', CX, 570, lt - .3, 'FFFFFF', 26, 5)

def s_share(fr, T):
    lt = T - S[5]; bg(fr, T, 'FFE08A', .6); rays(fr, T, 'FFFFFF', .2, CX, 1080)
    tape(fr, 'SEND THIS TO...', CX, 450, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: (phone(c, CX, 1080, .85 * pop(T, S[5] - .1)), bison(c, CX, 1110, .38 * pop(T, S[5] + .2), T, 1.0))))
    chip(fr, '@SHORTCUT_KING', CX, 900, lt - .2, CYAN, 38, 0)
    t = wfind(5, 'shortcut')
    if T > t: burst(fr, 'TRUST ME', 830, 700, T - t, r=140, col=YEL, size=44, rot=10)

def s_seven(fr, T):
    lt = T - S[6]; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'THE WILD PART', CX, 450, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    t7 = wfind(6, 'seven'); t3 = wfind(6, 'three')
    def dr(c):
        c.move_to(120, 1150); c.line_to(960, 1150); ink(c, 10); c.stroke()
        for k in range(7):
            x = 160 + k * 125; tk = t7 + k * .12
            if T > tk - .1: bison(c, x, 1050, .2 * pop(T, tk - .1), T, .3)
            c.arc(x, 1150, 14, 0, 6.29); c.set_source_rgba(*hx(RED)); c.fill()
    overlay(fr, L_(dr))
    if T > t7: title(fr, '7+ HUNTS', 620, T - t7, size=140, fill=YEL)
    if T > t3: chip(fr, 'OVER ~3,000 YEARS', CX, 1290, T - t3, 'FFFFFF', 42, -2)

def s_crumble(fr, T):
    fr[:] = essay_slide(T, [('MOST OF IT', 'main'), ('HAS CRUMBLED.', 'hl')], [S[7], wfind(7, 'crumbled') - .2], size=120)
    def dr(c):
        c.move_to(300, 1000); c.line_to(700, 1000); c.line_to(660, 1400); c.line_to(300, 1400); c.close_path(); c.set_source_rgba(*hx(ROCK)); c.fill_preserve(); ink(c, 6); c.stroke()
        for k in range(10):
            u = ((T - S[7]) * .7 + k / 10) % 1; c.arc(700 + (k * 31) % 120, 1000 + u * 420, 12 + k % 3 * 5, 0, 6.29); c.set_source_rgba(*hx(ROCK, 1 - u * .5)); c.fill()
    overlay(fr, L_(dr))

def s_end(fr, T):
    lt = T - S[8]; edge = 900; bx = 520 + 260 * eout(clamp(lt / 2.6)); by = 1500 - (bx / edge) ** 1.6 * 430
    overlay(fr, L_(lambda c: (hill(c, edge, 1070, T), bison(c, bx, by - 150, .62, T, 1 - clamp((lt - 2.4) / .4), False, lt > 2.4))))
    tape(fr, 'RUNNING UPHILL?', CX, 450, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    t = wfind(8, 'check')
    if T > t: title(fr, 'CHECK THE TOP', 620, T - t, size=124, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_drop), (S[3], s_bones), (S[4], s_trick), (S[5], s_teams), (S[6], s_share), (S[7], s_seven), (S[8], s_crumble), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (S[1], wfind(6, 'seven'), wfind(8, 'check')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Research: Rice University, American Antiquity (2026)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
