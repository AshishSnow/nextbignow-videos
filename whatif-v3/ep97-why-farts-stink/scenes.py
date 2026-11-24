import sys, os, json, math
sys.path.insert(0, '/home/claude/fart')
from kit import *
D = '/home/claude/fart'
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




STINK = '9BC94A'

def cloud(c, x, y, s, T, col=STINK, al=.9):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    P = ((-90, 10, 80), (0, -40, 100), (100, 0, 85), (40, 60, 70), (-40, 60, 70))
    for dx, dy, r in P:
        c.arc(dx + 6 * math.sin(T * 2 + dx), dy, r + 6, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    for dx, dy, r in P:
        c.arc(dx + 6 * math.sin(T * 2 + dx), dy, r, 0, 6.29); c.set_source_rgba(*hx(col)); c.fill()
    c.restore()

def wavy(c, x, y, s, T, n=3, col='5E8C2A'):
    for k in range(n):
        xx = x + (k - (n - 1) / 2) * 50 * s
        c.move_to(xx, y)
        for j in range(1, 8): c.line_to(xx + 14 * s * math.sin(T * 5 + j + k), y - j * 18 * s)
        c.set_source_rgba(*hx(col)); c.set_line_width(8 * s); c.set_line_cap(1); c.stroke()

def egg(c, x, y, s, rot=False):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.scale(.8, 1); c.arc(0, 0, 120, 0, 6.29); c.restore(); c.set_source_rgba(*hx('F7F1E3' if not rot else 'D9D2A0')); c.fill_preserve(); ink(c, 8); c.stroke()
    if rot:
        c.move_to(-60, -20); c.line_to(-20, 10); c.line_to(10, -15); c.line_to(50, 20); ink(c, 6); c.stroke()
    c.restore()

def skunk(c, x, y, s, T):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(100, 0); c.curve_to(260, -40, 260, -260, 140, -280); c.curve_to(200, -180, 160, -80, 60, -40); c.close_path(); c.set_source_rgba(*hx('1C1614')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.move_to(140, -40); c.curve_to(210, -100, 210, -200, 150, -250); c.set_source_rgba(1, 1, 1, 1); c.set_line_width(16); c.stroke()
    c.save(); c.scale(1.5, 1); c.arc(0, 0, 90, 0, 6.29); c.restore(); c.set_source_rgba(*hx('2B2B33')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.move_to(-120, -60); c.line_to(100, -70); c.set_source_rgba(1, 1, 1, 1); c.set_line_width(18); c.stroke()
    c.arc(-140, -20, 60, 0, 6.29); c.set_source_rgba(*hx('2B2B33')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.arc(-160, -35, 10, 0, 6.29); c.set_source_rgba(1, 1, 1, 1); c.fill()
    c.arc(-195, -10, 10, 0, 6.29); c.set_source_rgba(*hx(PINK)); c.fill()
    c.restore()

def pie(c, x, y, r, u):
    parts = (('N2', .55, 'C9CED6'), ('H2', .25, CYAN), ('CO2', .19, 'F7F1E3'), ('S', .01, STINK))
    a = -math.pi / 2
    for lab, f, col in parts:
        b = a + 6.283 * f * u
        c.move_to(x, y); c.arc(x, y, r, a, b); c.close_path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 6); c.stroke()
        a = b

def bug(c, x, y, s, T, col='E07A5F'):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(.2 * math.sin(T * 3 + x))
    c.save(); c.scale(1.6, 1); c.arc(0, 0, 40, 0, 6.29); c.restore(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 5); c.stroke()
    for ex in (-18, 18): c.arc(ex - 20, -8, 8, 0, 6.29); c.set_source_rgba(1, 1, 1, 1); c.fill(); c.arc(ex - 20, -8, 4, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    for k in range(4): c.move_to(-40 + k * 26, 38); c.line_to(-46 + k * 26, 58 + 6 * math.sin(T * 8 + k)); ink(c, 4); c.stroke()
    c.restore()

def food(c, kind, x, y, s, T):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    if kind == 'meat':
        c.save(); c.scale(1.3, 1); c.arc(0, 0, 80, 0, 6.29); c.restore(); c.set_source_rgba(*hx('B5523B')); c.fill_preserve(); ink(c, 6); c.stroke()
        c.save(); c.scale(1.3, 1); c.arc(-10, -5, 45, 0, 6.29); c.restore(); c.set_source_rgba(*hx('F2C9A0')); c.fill()
    elif kind == 'egg':
        c.restore(); egg(c, x, y, .6 * s); return
    elif kind == 'milk':
        c.rectangle(-55, -70, 110, 150); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 6); c.stroke()
        c.move_to(-55, -70); c.line_to(0, -120); c.line_to(55, -70); c.close_path(); c.set_source_rgba(*hx(CYAN)); c.fill_preserve(); ink(c, 6); c.stroke()
    elif kind == 'broc':
        c.rectangle(-18, 0, 36, 90); c.set_source_rgba(*hx('8BC34A')); c.fill_preserve(); ink(c, 5); c.stroke()
        for dx, dy in ((-45, -20), (0, -50), (45, -20), (-20, 10), (25, 10)):
            c.arc(dx, dy, 42, 0, 6.29); c.set_source_rgba(*hx('3FAE5A')); c.fill_preserve(); ink(c, 5); c.stroke()
    elif kind == 'beans':
        for k in range(5):
            c.save(); c.translate(-60 + k * 30, (k % 2) * 20); c.rotate(.4 * k); c.scale(1.5, 1); c.arc(0, 0, 22, 0, 6.29); c.restore()
            c.set_source_rgba(*hx('8B3A2E')); c.fill_preserve(); ink(c, 4); c.stroke()
    c.restore()

def nose(c, x, y, s):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, -200); c.curve_to(40, -80, 140, 40, 120, 90); c.curve_to(100, 130, 30, 130, 0, 110); c.curve_to(-30, 130, -100, 130, -120, 90); c.curve_to(-140, 40, -40, -80, 0, -200)
    c.set_source_rgba(*hx('F2C9A0')); c.fill_preserve(); ink(c, 8); c.stroke()
    for sx in (-1, 1): c.save(); c.translate(sx * 50, 95); c.scale(1.4, 1); c.arc(0, 0, 16, 0, 6.29); c.restore(); c.set_source_rgba(*hx('7A4E2A')); c.fill()
    c.restore()

def L_(fn): return cairo_layer(fn)

def s_hook(fr, T):
    bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    overlay(fr, L_(lambda c: (cloud(c, CX, 1060, 1.6 * back(clamp((T + .4) / .4)), T), wavy(c, CX, 860, 1.2, T, 4))))
    if T > wfind(0, 'twenty'): burst(fr, '~20 A DAY', 830, 1300, T - wfind(0, 'twenty'), r=120, col=YEL, size=36, rot=10)
    tape(fr, 'YOUR BODY', CX, 470, T + .3, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'WHY FARTS STINK', 600, T + .3, size=110, fill=YEL, rot=-2)

def s_most(fr, T):
    fr[:] = essay_slide(T, [('MOST OF IT', 'grey'), ("DOESN'T SMELL.", 'hl')], [S[1] - .1, S[1] + .6], size=124)
    overlay(fr, L_(lambda c: cloud(c, CX, 1180, .9, T, 'C9CED6')))

def s_pie(fr, T):
    lt = T - S[2]; bg(fr, T, 'C9DDF0'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, "WHAT'S INSIDE", CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    overlay(fr, L_(lambda c: pie(c, CX, 1020, 330, eout(clamp(lt / 2)))))
    for k, (w, lab, x, y, col) in enumerate((('nitrogen', 'NITROGEN', 300, 740, 'FFFFFF'), ('hydrogen', 'HYDROGEN', 820, 800, CYAN), ('carbon', 'CARBON DIOXIDE', 760, 1310, 'FFFFFF'))):
        if T > wfind(2, w): chip(fr, lab, x, y, T - wfind(2, w), col, 38, -4 + 4 * k)
    if T > wfind(2, 'none'): title(fr, 'NO SMELL', 600, T - wfind(2, 'none'), size=120, fill=YEL)

def s_bugs(fr, T):
    lt = T - S[3]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'THE STINK', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    def dr(c):
        for k, (x, y, col) in enumerate(((300, 1000, 'E07A5F'), (560, 1120, '9B7EDE'), (800, 980, 'F2A541'), (450, 1300, '6FB39A'), (760, 1260, 'E07A5F'))):
            bug(c, x, y, 1.1 * back(clamp((lt - k * .1) / .3)), T, col)
        if T > wfind(3, 'sulfur'): cloud(c, CX, 820, .7 * back(clamp((T - wfind(3, 'sulfur')) / .35)), T)
    overlay(fr, L_(dr))
    if T > wfind(3, 'sulfur'): title(fr, 'SULFUR GAS', 600, T - wfind(3, 'sulfur'), size=120, fill=YEL)
    if T > wfind(3, 'bacteria'): chip(fr, 'GUT BACTERIA', CX, 1420 - 60, T - wfind(3, 'bacteria'), YEL, 38, -2)

def s_smells(fr, T):
    lt = T - S[4]; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'SMELLS LIKE...', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    t2 = wfind(4, 'skunk')
    def dr(c):
        egg(c, 300, 1020, 1.3 * back(clamp(lt / .3)), True); wavy(c, 300, 860, 1, T)
        if T > t2 - .3: skunk(c, 760, 1100, .9 * back(clamp((T - t2 + .3) / .3)), T)
    overlay(fr, L_(dr))
    chip(fr, 'ROTTEN EGGS', 300, 1260, lt - .3, YEL, 38, -3)
    if T > t2: chip(fr, 'SKUNK', 760, 1290, T - t2, 'FFFFFF', 40, 3)

def s_nose(fr, T):
    fr[:] = essay_slide(T, [('1 MOLECULE', 'hl'), ('IN A MILLION.', 'main')], [wfind(5, 'one'), wfind(5, 'million')], size=124)
    lt = T - S[5]
    def dr(c):
        rng = np.random.default_rng(9)
        for k in range(160):
            c.arc(rng.uniform(80, 1000), rng.uniform(950, 1380), 7, 0, 6.29); c.set_source_rgba(1, 1, 1, .35); c.fill()
        c.arc(820, 1060, 18, 0, 6.29); c.set_source_rgba(*hx(STINK)); c.fill_preserve(); ink(c, 4); c.stroke()
        nose(c, 330, 1130, .9 * back(clamp((lt - .1) / .35)))
    overlay(fr, L_(dr))
    if T > wfind(5, 'sensitive'): chip(fr, 'YOUR NOSE: SUPER SENSITIVE', CX, 870, T - wfind(5, 'sensitive'), YEL, 32, -2)

def s_why(fr, T):
    lt = T - S[6]; bg(fr, T, 'F7E3C8'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'BUT WHY?', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    def dr(c):
        person(c, 300, 1000, 1.0 * back(clamp(lt / .3)), T, 0, False, '8B6A4A')
        food(c, 'meat', 760, 1150, 1.3, T); wavy(c, 760, 1040, 1, T)
        for k in range(3):
            a = T * 3 + k * 2; c.arc(760 + 90 * math.cos(a), 980 + 40 * math.sin(a), 10, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    overlay(fr, L_(dr))
    if T > wfind(6, 'ancestors'): title(fr, 'A DANGER ALARM', 600, T - wfind(6, 'ancestors'), size=104, fill=YEL)
    if T > wfind(6, 'rotting'): chip(fr, 'ROTTING FOOD = DANGER', 700, 1330, T - wfind(6, 'rotting'), YEL, 34, 3)

def s_food(fr, T):
    lt = T - S[7]; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'MAKES IT WORSE', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    def dr(c):
        for k, (w, kind, x, y) in enumerate((('meat', 'meat', 280, 900), ('eggs', 'egg', 780, 900), ('dairy', 'milk', 280, 1220), ('broccoli', 'broc', 780, 1220))):
            if T > wfind(7, w) - .2: food(c, kind, x, y, 1.3 * back(clamp((T - wfind(7, w) + .2) / .3)), T)
    overlay(fr, L_(dr))
    if T > wfind(7, 'sulfur'): title(fr, 'SULFUR-RICH FOOD', 600, T - wfind(7, 'sulfur'), size=100, fill=YEL)
    if T > wfind(7, 'broccoli'): burst(fr, 'YES, REALLY', CX, 1060, T - wfind(7, 'broccoli'), r=110, col=YEL, size=30, rot=8)

def s_loud(fr, T):
    fr[:] = essay_slide(T, [('LOUDER', 'grey'), ("ISN'T SMELLIER.", 'hl')], [S[8], wfind(8, 'smellier')], size=124)
    def dr(c):
        food(c, 'beans', 300, 1150, 1.4, T)
        if T > wfind(8, 'sulfur'): cloud(c, 780, 1150, .6, T); wavy(c, 780, 1040, .8, T)
    overlay(fr, L_(dr))
    chip(fr, 'BEANS: MORE GAS', 300, 1290, T - S[8] - .4, 'FFFFFF', 32, -3)
    if T > wfind(8, 'sulfur'): chip(fr, 'SULFUR: THE STINK', 780, 1290, T - wfind(8, 'sulfur'), YEL, 32, 3)

def s_end(fr, T):
    lt = T - S[9]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    tape(fr, 'ALWAYS FOUL? SEE A DOCTOR', CX, 470, lt, col=RED, size=50, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: [bug(c, 260 + k * 190, 1100 + 30 * math.sin(T * 3 + k), .9, T, ['E07A5F', '9B7EDE', 'F2A541', '6FB39A', 'E07A5F'][k]) for k in range(5)]))
    if T > wfind(9, 'otherwise'): title(fr, 'YOUR GUT AT WORK', 600, T - wfind(9, 'otherwise'), size=100, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_most), (S[3], s_pie), (S[4], s_bugs), (S[5], s_smells), (S[6], s_nose), (S[7], s_why), (S[8], s_food), (S[9], s_loud), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'stink'), wfind(3, 'sulfur'), wfind(7, 'broccoli')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Source: B. Wilson, Univ. of Illinois (The Conversation)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
