import sys, os, json, math
sys.path.insert(0, '/home/claude/birds')
from kit import *
D = '/home/claude/birds'
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

def tree(c, x, y, s):
    c.rectangle(x - 18 * s, y, 36 * s, 160 * s); c.set_source_rgba(*hx('8B5A3C')); c.fill_preserve(); ink(c, 6); c.stroke()
    for dx, dy, r in ((0, -40, 110), (-80, 10, 80), (80, 10, 80)):
        c.arc(x + dx * s, y + dy * s, r * s, 0, 6.29); c.set_source_rgba(*hx(GREEN)); c.fill_preserve(); ink(c, 6); c.stroke()

def ground(fr, T, tint='DCE8C2'):
    bg(fr, T, tint); rays(fr, T, 'FFFFFF', .1)
    overlay(fr, cairo_layer(lambda c: (c.rectangle(0, 1290, W, 400), c.set_source_rgba(*hx('9CCB7A', .6)), c.fill())))

def L_(fn): return cairo_layer(fn)

def s_hook(fr, T):
    ground(fr, T)
    t1 = wfind(0, 'run'); fly = clamp((T - t1) / .3) if T > t1 else 0
    bx, by = CX + 40 + 500 * eout(clamp((T - t1) / 2.5)) * (T > t1), 1180 - 420 * eout(clamp((T - t1) / 2.5)) * (T > t1)
    def dr(c):
        tree(c, 900, 820, .9)
        person(c, 230, 1060, 1.05, T, 1.0 if T < t1 else 0, True, RED)
        bird(c, bx, by, .9, T, fly, True)
    overlay(fr, L_(dr))
    if T > t1: burst(fr, 'FLAP!', 760, 820, T - t1, r=110, col=YEL, size=50, rot=10)
    tape(fr, 'NOBODY KNOWS WHY', CX, 470, T + .3, col=RED, size=58, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'BIRDS FLEE WOMEN FIRST', 600, T + .3, size=94, fill=YEL, rot=-2)

def s_one(fr, T):
    fr[:] = essay_slide(T, [("NOT ONE", 'grey'), ('JUMPY PIGEON.', 'hl')], [S[1], wfind(1, 'jumpy')], size=124)
    lt = T - S[1]
    overlay(fr, L_(lambda c: [bird(c, 240 + k * 300, 1130 + 30 * math.sin(T * 3 + k), .6 * back(clamp((lt - k * .12) / .3)), T, 0, k % 2 == 0, ['8A93A6', 'B5895F', '4A4A55'][k]) for k in range(3)]))

def s_countries(fr, T):
    lt = T - S[2]; ground(fr, T, 'C9DDF0')
    tape(fr, '5 COUNTRIES', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: (tree(c, 200, 1120, .8), tree(c, 880, 1120, .8))))
    for k, (n, col) in enumerate((('CZECHIA', 'FFFFFF'), ('FRANCE', CYAN), ('GERMANY', YEL), ('POLAND', 'FFFFFF'), ('SPAIN', RED))):
        chip(fr, n, CX + (-150 if k % 2 else 150), 760 + k * 105, lt - .4 - k * .25, col, 44, -4 if k % 2 else 4)
    if T > wfind(2, 'parks'): title(fr, 'CITY PARKS', 600, T - wfind(2, 'parks'), size=104, fill=YEL)

def s_match(fr, T):
    lt = T - S[3]; ground(fr, T, 'F6D5DA')
    tape(fr, 'FAIR TEST', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    def dr(c):
        person(c, 330, 1000, 1.1 * back(clamp(lt / .3)), T, 0, True, BLUE)
        person(c, 750, 1000, 1.1 * back(clamp((lt - .15) / .3)), T, 0, False, BLUE)
        c.move_to(120, 795); c.line_to(960, 795); c.set_source_rgba(*hx(RED)); c.set_line_width(8); c.set_dash([24, 14]); c.stroke(); c.set_dash([])
    overlay(fr, L_(dr))
    chip(fr, 'WOMAN', 330, 1340, lt - .3, 'FFFFFF', 40, -3); chip(fr, 'MAN', 750, 1340, lt - .4, 'FFFFFF', 40, 3)
    if T > wfind(3, 'height'): chip(fr, 'SAME HEIGHT', CX, 720, T - wfind(3, 'height'), YEL, 40, -2)
    if T > wfind(3, 'dressed'): title(fr, 'SAME CLOTHES', 600, T - wfind(3, 'dressed'), size=104, fill=YEL)

def s_test(fr, T):
    lt = T - S[4]; ground(fr, T, 'F7E3C8')
    tape(fr, 'THE TEST', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    u = eout(clamp(lt / 2.5)); px = 200 + 330 * u
    t1 = wfind(4, 'takes off'); fly = clamp((T - t1) / .3) if T > t1 else 0
    def dr(c):
        person(c, px, 1040, 1.0, T, 1 - fly, False, BLUE)
        bird(c, 880 + 200 * fly, 1200 - 300 * fly, .7, T, fly, True)
        c.move_to(px + 70, 1380); c.line_to(830, 1380); c.set_source_rgba(*hx(RED)); c.set_line_width(10); c.stroke()
        for xx in (px + 70, 830): c.move_to(xx, 1355); c.line_to(xx, 1405); c.stroke()
    overlay(fr, L_(dr))
    if T > wfind(4, 'close'): title(fr, 'HOW CLOSE?', 600, T - wfind(4, 'close'), size=120, fill=YEL)

def s_result(fr, T):
    lt = T - S[5]; ground(fr, T, 'E4DCEF')
    tape(fr, 'THE RESULT', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    def dr(c):
        bird(c, 930, 860, .55, T, 0, True); bird(c, 930, 1200, .55, T, 0, True)
        uw = eout(clamp(lt / 1)); um = eout(clamp((lt - .3) / 1.2))
        person(c, 150 + 220 * uw, 860, .6, T, 0, True, BLUE)
        person(c, 150 + 420 * um, 1180, .6, T, 0, False, BLUE)
    overlay(fr, L_(dr))
    chip(fr, 'WOMAN', 640, 860, lt, 'FFFFFF', 34, -3); chip(fr, 'MAN', 760, 1260, lt, 'FFFFFF', 34, -3)
    t1 = wfind(5, 'meter')
    if T > t1: burst(fr, '~1 M CLOSER', 840, 1040, T - t1, r=120, col=YEL, size=30, rot=8)
    if T > wfind(5, 'thirty'): title(fr, '37 SPECIES', 600, T - wfind(5, 'thirty'), size=120, fill=YEL)

def s_noidea(fr, T):
    fr[:] = essay_slide(T, [('THE SCIENTISTS:', 'grey'), ("NO IDEA WHY.", 'hl')], [S[6], wfind(6, 'explain')], size=124)
    overlay(fr, L_(lambda c: bird(c, CX, 1150, .8 * back(clamp((T - S[6] - .2) / .3)), T, 0)))
    burst(fr, '???', 780, 1000, T - S[6] - .4, r=100, col=YEL, size=60, rot=8)

def s_why(fr, T):
    lt = T - S[7]; ground(fr, T, 'F3E3B3')
    tape(fr, 'THREE GUESSES', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: bird(c, CX, 1030, 1.0, T, 0)))
    for k, (w, lab, col, x, y) in enumerate((('smell', 'SMELL?', CYAN, 280, 720), ('shape', 'BODY SHAPE?', YEL, 800, 780), ('walk', 'THE WALK?', 'FFFFFF', CX, 1300))):
        if T > wfind(7, w): chip(fr, lab, x, y, T - wfind(7, w), col, 50, -4 + 4 * k)

def s_untested(fr, T):
    fr[:] = essay_slide(T, [('NOBODY HAS TESTED', 'grey'), ('WHICH ONE.', 'hl')], [S[8], wfind(8, 'which')], size=110)
    lt = T - S[8]
    for k, (lab, col) in enumerate((('SMELL', CYAN), ('SHAPE', YEL), ('WALK', 'FFFFFF'))):
        chip(fr, lab + '?', 230 + k * 310, 1120, lt - .2 - k * .15, col, 44, -3 + 3 * k)

def s_end(fr, T):
    lt = T - S[9]; ground(fr, T)
    tape(fr, 'EARLY STUDY', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    t1 = wfind(9, 'bolts'); fly = clamp((T - t1) / .3) if T > t1 else 0
    def dr(c):
        tree(c, 900, 820, .9)
        person(c, 260, 1060, 1.05, T, 0, True, RED)
        bird(c, 620 + 400 * eout(clamp((T - t1) / 2)) * (T > t1), 1180 - 400 * eout(clamp((T - t1) / 2)) * (T > t1), .9, T, fly, True)
    overlay(fr, L_(dr))
    if T > wfind(9, 'personal'): title(fr, "IT'S NOT PERSONAL", 600, T - wfind(9, 'personal'), size=100, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_one), (S[3], s_countries), (S[4], s_match), (S[5], s_test), (S[6], s_result), (S[7], s_noidea), (S[8], s_why), (S[9], s_untested), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'run'), wfind(5, 'meter'), wfind(6, 'explain')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Study: Morelli et al., People and Nature')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
