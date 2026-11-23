import sys, os, json, math
sys.path.insert(0, '/home/claude/b12')
from kit import *
D = '/home/claude/b12'
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



def battery(c, x, y, s=1.0, fill=1.0, rot=0, col=GREEN):
    c.save(); c.translate(x, y); c.rotate(math.radians(rot)); c.scale(s, s)
    c.rectangle(-110 + 12, -190 + 14, 220, 380); c.set_source_rgba(0, 0, 0, .3); c.fill()
    c.rectangle(-45, -225, 90, 40); c.set_source_rgba(*hx('BBBBBB')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.rectangle(-110, -190, 220, 380); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 9); c.stroke()
    hh = 340 * clamp(fill); c.rectangle(-90, 170 - hh, 180, hh); c.set_source_rgba(*hx(col)); c.fill()
    c.move_to(15, -110); c.line_to(-40, 10); c.line_to(5, 10); c.line_to(-15, 110); c.line_to(45, -20); c.line_to(0, -20); c.close_path()
    c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 6); c.stroke()
    c.restore()

def coin(c, x, y, r=110, holes=True, label='Zn'):
    c.arc(x + 10, y + 12, r, 0, 6.29); c.set_source_rgba(0, 0, 0, .3); c.fill()
    c.arc(x, y, r, 0, 6.29); c.set_source_rgba(*hx('C9CED6')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.arc(x, y, r * .72, 0, 6.29); c.set_source_rgba(*hx('E6E9EE')); c.fill_preserve(); ink(c, 4); c.stroke()
    if holes:
        for k in range(4):
            a = k * 1.57 + .6; c.arc(x + math.cos(a) * r * .38, y + math.sin(a) * r * .38, r * .08, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()

def puffs(c, T, x, y, n=5, col='FFFFFF'):
    for k in range(n):
        u = ((T * .7 + k / n) % 1.0); px = x - 300 + 300 * u; py = y + 60 * math.sin(k * 2 + T * 2)
        c.arc(px, py, 30 + 20 * u, 0, 6.29); c.set_source_rgba(*hx(col, .8 * (1 - u) + .1)); c.fill_preserve(); ink(c, 4, .6 * (1 - u)); c.stroke()

def egg(fr, T, x, y, w, t=1.0, rot=0):
    s_ = st('egg', w=w)
    if s_ is not None and t > 0: put_rgba(fr, s_, x, y + 6 * math.sin(T * 2), back(clamp(t / .35)), 1.0, rot)

def molecule(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(.1 * math.sin(T))
    pts = [(math.cos(a * 1.2566 + .3) * 200, math.sin(a * 1.2566 + .3) * 200) for a in range(5)]
    for px, py in pts:
        c.move_to(0, 0); c.line_to(px, py); c.set_source_rgba(1, 1, 1, .9); c.set_line_width(10); c.stroke()
        c.save(); c.translate(px, py); c.move_to(55, 0)
        for a in range(1, 7): c.line_to(55 * math.cos(a * 1.047), 55 * math.sin(a * 1.047))
        c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 7); c.stroke(); c.restore()
    c.arc(0, 0, 80, 0, 6.29); c.set_source_rgba(*hx(PINK)); c.fill_preserve(); ink(c, 8); c.stroke()
    c.restore()

def nugget(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    pts = [(-120, -40), (-60, -110), (40, -100), (130, -30), (110, 70), (20, 110), (-90, 90)]
    c.move_to(pts[0][0] + 12, pts[0][1] + 14)
    for px, py in pts[1:]: c.line_to(px + 12, py + 14)
    c.close_path(); c.set_source_rgba(0, 0, 0, .3); c.fill()
    c.move_to(*pts[0])
    for px, py in pts[1:]: c.line_to(px, py)
    c.close_path(); c.set_source_rgba(*hx('D8DCE2')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.move_to(-50, -60); c.line_to(10, -70); c.set_source_rgba(1, 1, 1, .9); c.set_line_width(10); c.stroke()
    c.restore()

def s_hook(fr, T):
    bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    egg(fr, T, 330, 1080, 620, T + .4, -6)
    overlay(fr, cairo_layer(lambda c: battery(c, 800, 1060, 1.0, clamp(T / 2.2), 6)))
    def arc_(c):
        c.move_to(500, 860); c.curve_to(560, 760, 680, 760, 720, 840); c.set_source_rgba(*hx(RED)); c.set_line_width(14); c.set_dash([24, 14]); c.stroke(); c.set_dash([])
    overlay(fr, cairo_layer(arc_))
    tape(fr, 'NEW BATTERY', CX, 470, T + .3, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'THE EGG VITAMIN BATTERY', 600, T + .3, size=96, fill=YEL, rot=-2)

def s_air(fr, T):
    fr[:] = essay_slide(T, [('NOT LITHIUM.', 'grey'), ('IT BREATHES AIR.', 'hl')], [S[1], wfind(1, 'this one')])
    overlay(fr, cairo_layer(lambda c: (puffs(c, T, 560, 1080), battery(c, 740, 1100, .9, .7, 4))))

def s_zinc(fr, T):
    lt = T - S[2]; bg(fr, T, 'C9DDF0'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'ZINC + AIR', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    def dr(c):
        for k, (x, y) in enumerate(((300, 980), (560, 1090), (820, 960))):
            if lt > .15 * k: coin(c, x, y + 8 * math.sin(T * 2 + k), 120 * back(clamp((lt - .15 * k) / .35)))
    overlay(fr, cairo_layer(dr))
    if T > wfind(2, 'hearing'): chip(fr, 'ALREADY IN HEARING AIDS', CX, 1290, T - wfind(2, 'hearing'), YEL, 40, -2); title(fr, 'HEARING-AID BATTERIES', 620, T - wfind(2, 'hearing'), size=90, fill=YEL)

def s_once(fr, T):
    lt = T - S[3]; bg(fr, T, 'F7D9C4'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'BUT...', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, cairo_layer(lambda c: coin(c, CX, 1000, 200)))
    t1 = wfind(3, 'one use'); xstamp(fr, CX, 1000, T - t1, 1.3)
    if T > t1: chip(fr, 'ONE USE, THEN TRASH', CX, 1290, T - t1, 'FFFFFF', 40, 2)
    if T > wfind(3, 'recharging'): title(fr, 'RECHARGING = HARD', 620, T - wfind(3, 'recharging'), size=100, fill=YEL)

def s_plat(fr, T):
    lt = T - S[4]; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'THE HELPER', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    def cyc(c):
        x, y, r = CX, 1010, 260
        for k, col in enumerate((GREEN, RED)):
            a0 = math.pi * k + .25; a1 = a0 + math.pi - .5
            c.arc(x, y, r, a0, a1); c.set_source_rgba(*hx(col)); c.set_line_width(26); c.stroke()
            ex, ey = x + math.cos(a1) * r, y + math.sin(a1) * r; d = a1 + math.pi / 2
            c.move_to(ex + math.cos(d) * 40, ey + math.sin(d) * 40); c.line_to(ex + math.cos(d - 2.3) * 40, ey + math.sin(d - 2.3) * 40); c.line_to(ex + math.cos(d + 2.3) * 40, ey + math.sin(d + 2.3) * 40); c.close_path(); c.set_source_rgba(*hx(col)); c.fill()
    overlay(fr, cairo_layer(cyc))
    chip(fr, 'CHARGE', 250, 760, lt - .4, GREEN, 38, -4); chip(fr, 'USE', 830, 1280, lt - .6, RED, 38, 4)
    t1 = wfind(4, 'platinum')
    if T > t1 - .3: overlay(fr, cairo_layer(lambda c: nugget(c, CX, 1010, 1.2 * back(clamp((T - t1 + .3) / .35)))))
    if T > t1: chip(fr, 'Pt', CX, 1010, T - t1, 'FFFFFF', 50, 0)
    if T > t1: burst(fr, '$$$', 800, 820, T - t1, r=110, col=YEL, size=60, rot=8); title(fr, 'PRICEY PLATINUM', 620, T - t1, size=100, fill=YEL)

def s_b12(fr, T):
    fr[:] = essay_slide(T, [('VITAMIN B12.', 'hl'), ('THE ONE IN YOUR EGGS.', 'main')], [S[5], wfind(5, 'the one')], size=110)
    lt = T - S[5]
    overlay(fr, cairo_layer(lambda c: molecule(c, 640, 1040, back(clamp((lt - .2) / .35)), T)))
    if lt > .4: chip(fr, 'COBALT CORE', 640, 1040, lt - .4, 'FFFFFF', 30, 0)
    if T > wfind(5, 'the one'):
        e_ = st('egg', w=300)
        if e_ is not None: put_rgba(fr, glow_outline(e_, 12, (255, 255, 255)), 250, 1180, back(clamp((T - wfind(5, 'the one')) / .35)), 1.0, -8)
    if T > wfind(5, 'spain'): chip(fr, 'UNIVERSITY OF CORDOBA, SPAIN', CX, 1320, T - wfind(5, 'spain'), YEL, 34, -2)

def s_wash(fr, T):
    lt = T - S[6]; bg(fr, T, 'D6EEF0'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'PROBLEM', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    t1 = wfind(6, 'washing')
    def dr(c):
        x, y, w, h = CX, 1020, 460, 520
        c.move_to(x - w / 2, y - h / 2); c.line_to(x - w / 2 + 30, y + h / 2); c.line_to(x + w / 2 - 30, y + h / 2); c.line_to(x + w / 2, y - h / 2)
        c.set_source_rgba(1, 1, 1, .5); c.fill_preserve(); ink(c, 9); c.stroke()
        wy = y - h / 2 + 110 + 10 * math.sin(T * 3)
        c.move_to(x - w / 2 + 20, wy); c.line_to(x + w / 2 - 20, wy); c.line_to(x + w / 2 - 34, y + h / 2 - 6); c.line_to(x - w / 2 + 34, y + h / 2 - 6); c.close_path(); c.set_source_rgba(*hx('6FB7E8', .8)); c.fill()
        rng = np.random.default_rng(4)
        for k in range(16):
            px, py = x + rng.uniform(-170, 170), wy + rng.uniform(30, 360)
            if T > t1: d = (T - t1) * 260; px += d * (1 if k % 2 else -1) * rng.uniform(.5, 1.5); py += 30 * math.sin(T * 4 + k)
            c.arc(px, py, 16, 0, 6.29); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 3); c.stroke()
    overlay(fr, cairo_layer(dr))
    chip(fr, 'B12 DISSOLVES IN WATER', CX, 1310, T - wfind(6, 'dissolves'), YEL, 38, 2)
    if T > t1: title(fr, 'IT WASHED AWAY', 620, T - t1, size=104, fill=YEL)

def tubes(c, T, t0, n=0):
    x0, y0 = 120, 820
    for r in range(4):
        y = y0 + r * 120
        c.rectangle(x0 + 10, y + 12, 840, 80); c.set_source_rgba(0, 0, 0, .25); c.fill()
        c.rectangle(x0, y, 840, 80); c.set_source_rgba(*hx('3A3A40')); c.fill_preserve(); ink(c, 6); c.stroke()
        for k in range(14):
            hx_ = x0 + 30 + k * 60 + (30 if r % 2 else 0)
            if hx_ > x0 + 820: continue
            c.save(); c.translate(hx_, y + 40); c.move_to(22, 0)
            for a in range(1, 7): c.line_to(22 * math.cos(a * 1.047), 22 * math.sin(a * 1.047))
            c.set_source_rgba(1, 1, 1, .35); c.set_line_width(2); c.stroke(); c.restore()
            if T > t0 + (r * 14 + k) * .02 and (k + r) % 3 == 0:
                c.arc(hx_, y + 40, 14, 0, 6.29); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 3); c.stroke()

def s_glue(fr, T):
    lt = T - S[7]; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'THE FIX', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    overlay(fr, cairo_layer(lambda c: tubes(c, T, S[7] + .4)))
    if T > wfind(7, 'tiny'): chip(fr, 'TINY CARBON TUBES', 330, 740, T - wfind(7, 'tiny'), YEL, 38, -3)
    t2 = wfind(7, 'two hundred')
    if T > wfind(7, 'worked'): title(fr, 'IT WORKED', 620, T - wfind(7, 'worked'), size=110, fill=YEL)
    if T > t2:
        n = int(250 * eout(clamp((T - t2) / 1.0)))
        burst(fr, f'{n} CHARGES', 760, 1330, T - t2, r=160, col=YEL, size=40, rot=8)

def s_vit(fr, T):
    fr[:] = essay_slide(T, [('NO FIRE-PRONE LITHIUM.', 'grey'), ('ZINC. AIR. A VITAMIN.', 'hl')], [S[8], wfind(8, 'just')], size=100)
    lt = T - S[8]
    def dr(c):
        coin(c, 250, 1120, 100 * back(clamp((T - wfind(8, 'zinc')) / .3))) if T > wfind(8, 'zinc') else None
        if T > wfind(8, 'air.'): puffs(c, T, 640, 1120, 4)
    overlay(fr, cairo_layer(dr))
    if T > wfind(8, 'vitamin'):
        e_ = st('egg', w=260)
        if e_ is not None: put_rgba(fr, glow_outline(e_, 12, (255, 255, 255)), 840, 1110, back(clamp((T - wfind(8, 'vitamin')) / .35)), 1.0, 6)

def s_end(fr, T):
    lt = T - S[9]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    tape(fr, 'STILL A LAB PROTOTYPE', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    egg(fr, T, 380, 1080, 480, lt, -6)
    overlay(fr, cairo_layer(lambda c: battery(c, 800, 1080, .9, .5 + .5 * clamp(lt / 3), 6)))
    if T > wfind(9, 'one day') - .2: title(fr, 'POWER FROM BREAKFAST?', 620, T - wfind(9, 'one day') + .2, size=96, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_air), (S[3], s_zinc), (S[4], s_once), (S[5], s_plat), (S[6], s_b12), (S[7], s_wash), (S[8], s_glue), (S[9], s_vit), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(3, 'one use'), wfind(7, 'worked'), wfind(7, 'two hundred')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Images: Wikimedia Commons (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
