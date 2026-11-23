import sys, os, json, math
sys.path.insert(0, '/home/claude/hera')
from kit import *
D = '/home/claude/hera'
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


def stars(c, T, n=70, seed=3):
    rng = np.random.default_rng(seed)
    for k in range(n):
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(2, 6)
        a = .5 + .5 * math.sin(T * 3 + k)
        c.arc(x, y, r, 0, 6.29); c.set_source_rgba(1, 1, .9, .35 + .5 * a); c.fill()

def probe(c, x, y, s=1.0, rot=0, col='D9A43A', panels=True):
    c.save(); c.translate(x, y); c.rotate(math.radians(rot)); c.scale(s, s)
    if panels:
        for sx in (-1, 1):
            c.rectangle(sx * 70 - (150 if sx < 0 else 0), -28, 150, 56); c.set_source_rgba(*hx('2B4C8C')); c.fill_preserve(); ink(c, 6); c.stroke()
            for k in range(1, 5):
                xx = sx * 70 - (150 if sx < 0 else 0) + k * 30; c.move_to(xx, -28); c.line_to(xx, 28); c.set_source_rgba(1, 1, 1, .35); c.set_line_width(2); c.stroke()
    c.rectangle(-70, -60, 140, 120); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    c.move_to(-40, -60); c.line_to(-20, -95); c.line_to(20, -95); c.line_to(40, -60); c.set_source_rgba(*hx('BBBBBB')); c.fill_preserve(); ink(c, 5); c.stroke()
    c.restore()

def earth(c, x, y, r):
    c.arc(x + 10, y + 12, r, 0, 6.29); c.set_source_rgba(0, 0, 0, .3); c.fill()
    c.arc(x, y, r, 0, 6.29); c.set_source_rgba(*hx('2D6CDF')); c.fill()
    for dx, dy, rr in ((-.3, -.2, .38), (.35, .25, .3), (.1, -.45, .2)):
        c.arc(x + dx * r, y + dy * r, rr * r, 0, 6.29); c.set_source_rgba(*hx('3FAE5A')); c.fill()
    c.arc(x, y, r, 0, 6.29); ink(c, 8); c.stroke()

def rock(fr, T, x, y, w, t=1.0, rot=0, bob=6):
    s_ = st('rock', w=w)
    if s_ is not None and t > 0: put_rgba(fr, s_, x, y + bob * math.sin(T * 1.7), back(clamp(t / .35)), 1.0, rot + 4 * math.sin(T * .6))

def space(fr, T, tint='1E2450', m=.88):
    bg(fr, T, tint, m); overlay(fr, cairo_layer(lambda c: stars(c, T)))

def s_hook(fr, T):
    space(fr, T)
    hit = wfind(0, 'purpose') - .15
    rock(fr, T, 700, 1080, 560 if T < hit else int(560 + 30 * math.exp(-(T - hit) * 6)), 1.0)
    if T < hit:
        u = clamp(T / hit); px, py = lerp(120, 560, eout(u * .9)), lerp(700, 980, eout(u * .9))
        def tr(c):
            c.move_to(-50, 560); c.line_to(px, py); c.set_source_rgba(*hx(YEL, .7)); c.set_line_width(10); c.set_dash([30, 20]); c.stroke(); c.set_dash([])
            probe(c, px, py, .9, 25)
        overlay(fr, cairo_layer(tr))
    else:
        k = T - hit
        def fl(c):
            for i in range(14):
                a = i / 14 * 6.283; r0 = 40 + 400 * eout(k / .6)
                c.move_to(560, 990); c.line_to(560 + math.cos(a) * r0, 990 + math.sin(a) * r0)
                c.set_source_rgba(*hx('FFFFFF', max(0, 1 - k / .8))); c.set_line_width(14); c.stroke()
        overlay(fr, cairo_layer(fl)); burst(fr, 'BOOM', 560, 990, k, r=150, col=YEL, size=72, rot=-8)
    tape(fr, 'ON PURPOSE', CX, 470, T + .3, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'NASA HIT AN ASTEROID', 600, T + .3, size=100, fill=YEL, rot=-2)

def s_det(fr, T):
    fr[:] = essay_slide(T, [('A DETECTIVE', 'main'), ('AT THE CRASH SITE.', 'hl')], [S[1], wfind(1, 'crash')], size=118)
    lt = T - S[1]
    overlay(fr, cairo_layer(lambda c: probe(c, CX + 30 * math.sin(T), 1080 + 10 * math.sin(T * 2), 1.5 * back(clamp(lt / .4)), -8)))
    if T > wfind(1, 'detective'): burst(fr, '?', 830, 1270, T - wfind(1, 'detective'), r=100, col=YEL, size=100, rot=8)

def s_trip(fr, T):
    lt = T - S[2]; bg(fr, T, 'C9DDF0'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'MEET HERA', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    u = eout(clamp(lt / 5.5))
    def dr(c):
        earth(c, 230, 1230, 130)
        pts = [(230 + (850 - 230) * s_, 1230 + (820 - 1230) * s_ - 260 * math.sin(math.pi * s_)) for s_ in np.linspace(0, 1, 60)]
        c.move_to(*pts[0])
        for p in pts[1:]: c.line_to(*p)
        c.set_source_rgba(*hx('1C1614', .6)); c.set_line_width(8); c.set_dash([22, 16]); c.stroke(); c.set_dash([])
        p = pts[int(u * 59)]; probe(c, p[0], p[1], .6, -20)
    rock(fr, T, 860, 810, 260, lt)
    overlay(fr, cairo_layer(dr))
    if T > wfind(2, 'two years'): chip(fr, '2 YEARS IN SPACE', 640, 1290, T - wfind(2, 'two years'), YEL, 38, -3)
    if T > wfind(2, 'hundred'): stat(fr, '120 MILLION MI', 'FROM EARTH', CX, 620, T - wfind(2, 'hundred'), RED, -3, 96)

def field(c, x, y, w, h):
    c.rectangle(x + 12, y + 14, w, h); c.set_source_rgba(0, 0, 0, .3); c.fill()
    c.rectangle(x, y, w, h); c.set_source_rgba(*hx('3FAE5A')); c.fill_preserve(); ink(c, 7); c.stroke()
    for k in range(1, 10):
        c.move_to(x + w * k / 10, y + 8); c.line_to(x + w * k / 10, y + h - 8); c.set_source_rgba(1, 1, 1, .8); c.set_line_width(4); c.stroke()

def s_size(fr, T):
    lt = T - S[3]; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .08)
    tape(fr, 'THE TARGET', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    t1 = wfind(3, 'football')
    rock(fr, T, CX, 940, 600, lt)
    if T > t1:
        u = eout(clamp((T - t1) / .6))
        def dr(c):
            field(c, 110, 1230, 560 * u, 110)
            if u > .5: field(c, 110 + 570, 1230, 280 * clamp((u - .5) * 2), 110)
        overlay(fr, cairo_layer(dr))
        title(fr, '1.5 FOOTBALL FIELDS', 620, T - t1, size=96, fill=YEL)

def s_hit(fr, T):
    lt = T - S[4]; bg(fr, T, 'F7D9C4'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'THE HIT', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    ph = photo('dart', 760, 520, (.45, .4))
    if ph is not None: put_rgba(fr, ph, CX, 900, back(clamp(lt / .35)), 1.0, -3)
    if T > wfind(4, 'vending'): chip(fr, 'VENDING-MACHINE SIZE', 600, 1180, T - wfind(4, 'vending'), YEL, 40, 3)
    t2 = wfind(4, 'fourteen')
    if T > t2:
        n = int(14000 * eout(clamp((T - t2) / 1.2)) // 100 * 100)
        stat(fr, f'{n:,} MPH', 'ABOUT 6 KM PER SECOND', CX, 620, T - t2, RED, -3, 110)

def s_33(fr, T):
    fr[:] = essay_slide(T, [('IT WORKED.', 'grey'), ('33 MINUTES', 'hl'), ('SHORTER ORBIT.', 'main')], [S[5], wfind(5, 'thirty'), wfind(5, 'shorter')], size=112)
    def orb(c):
        x, y = CX, 1130; c.save(); c.translate(x, y); c.scale(1, .45)
        rr = 330 - 50 * eout(clamp((T - wfind(5, 'shorter')) / 1)); c.arc(0, 0, rr, 0, 6.29); c.restore()
        c.set_source_rgba(1, 1, 1, .6); c.set_line_width(5); c.set_dash([16, 12]); c.stroke(); c.set_dash([])
        c.arc(x, y, 70, 0, 6.29); c.set_source_rgba(*hx('888888')); c.fill_preserve(); ink(c, 6); c.stroke()
        a = T * 1.6; c.arc(x + math.cos(a) * rr, y + math.sin(a) * rr * .45, 26, 0, 6.29); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 5); c.stroke()
    overlay(fr, cairo_layer(orb))
    if T > wfind(5, 'way more'): burst(fr, 'MORE THAN PREDICTED', 800, 1330, T - wfind(5, 'way more'), r=140, col=YEL, size=30, rot=8)

def s_why(fr, T):
    lt = T - S[6]; bg(fr, T, 'F2E6CF'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'BUT WHY?', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    rock(fr, T, CX, 1000, 520, lt)
    if T > wfind(6, 'crater'): chip(fr, 'A CRATER?', 270, 760, T - wfind(6, 'crater'), YEL, 44, -6)
    if T > wfind(6, 'reshape'): chip(fr, 'RESHAPED?', 810, 1230, T - wfind(6, 'reshape'), CYAN, 44, 5)
    if T > wfind(6, "that's"): title(fr, "HERA'S JOB", 620, T - wfind(6, "that's"), size=110, fill=YEL)

def s_plan(fr, T):
    fr[:] = essay_slide(T, [('IF ONE HEADS FOR EARTH,', 'grey'), ('THIS IS THE PLAN.', 'hl')], [S[7], wfind(7, 'this is')], size=100)
    lt = T - S[7]
    def dr(c):
        earth(c, 330, 1130, 170)
        u = clamp(lt / 3.5); rx, ry = lerp(920, 700, u), lerp(800, 960, u)
        c.arc(rx, ry, 55, 0, 6.29); c.set_source_rgba(*hx('888888')); c.fill_preserve(); ink(c, 6); c.stroke()
        if T > wfind(7, 'this is'):
            k = clamp((T - wfind(7, 'this is')) / .5); probe(c, lerp(980, rx + 60, k), lerp(1250, ry + 40, k), .5, -40)
    overlay(fr, cairo_layer(dr))

def calendar(c, x, y, T, t):
    s = back(clamp(t / .35)); c.save(); c.translate(x, y); c.scale(s, s); c.rotate(math.radians(-4))
    c.rectangle(-230 + 14, -200 + 16, 460, 420); c.set_source_rgba(0, 0, 0, .3); c.fill()
    c.rectangle(-230, -200, 460, 420); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
    c.rectangle(-230, -200, 460, 110); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 8); c.stroke()
    c.restore()

def s_end(fr, T):
    lt = T - S[8]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    tape(fr, 'FIRST CLOSE-UPS', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    rock(fr, T, 780, 1180, 380, lt - .2)
    overlay(fr, cairo_layer(lambda c: calendar(c, 380, 1000, T, lt)))
    if lt > .2:
        title(fr, 'NOV', 860, lt - .2, size=64, fill='FFFFFF', rot=-4, cx=380)
        title(fr, '25', 1050, lt - .25, size=190, fill=RED, rot=-4, cx=380)
    if T > wfind(8, 'crash'): chip(fr, 'OF THE CRASH SITE', 700, 640, T - wfind(8, 'crash'), YEL, 40, 3)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_det), (S[3], s_trip), (S[4], s_size), (S[5], s_hit), (S[6], s_33), (S[7], s_why), (S[8], s_plan), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'purpose') - .15, wfind(5, 'thirty'), wfind(4, 'fourteen')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Images: NASA/JHU APL via Wikimedia Commons')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
