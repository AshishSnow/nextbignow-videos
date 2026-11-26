import sys, os, json, math
sys.path.insert(0, '/home/claude/nose')
from kit import *
D = '/home/claude/nose'
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

SKIN = 'F2B48C'; SKD = 'D98A62'; BRAIN = 'F7A8C4'; BRD = 'D9709A'

def face(c, x, y, s, T, door=0.0):
    """side profile head facing right with a big nose; a glowing door in the nose."""
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-260, -330); c.curve_to(-40, -420, 140, -330, 150, -170); c.line_to(170, -60)
    c.curve_to(310, 10, 330, 90, 250, 110); c.line_to(170, 120); c.curve_to(190, 180, 150, 230, 120, 250)
    c.curve_to(140, 300, 60, 380, -40, 380); c.line_to(-60, 520); c.line_to(-300, 520); c.line_to(-300, -200); c.close_path()
    c.set_source_rgba(*hx(SKIN)); c.fill_preserve(); ink(c, 9); c.stroke()
    c.move_to(-280, -320); c.curve_to(-120, -470, 120, -420, 150, -230); c.curve_to(40, -300, -100, -260, -300, -120); c.close_path()
    c.set_source_rgba(*hx('3A2A20')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(60, -120, 18, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(205, 92, 16, 0, 6.29); c.set_source_rgba(*hx(SKD)); c.fill()
    if door > 0:
        c.save(); c.translate(225, 40); c.scale(door, door)
        c.rectangle(-30, -60, 60, 90); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 5); c.stroke()
        c.arc(-15, -12, 5, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
        c.restore()
    c.restore()

def brain(c, x, y, s, T, glow=0.0, door=0.0):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    if glow > 0:
        for r in (260, 220): c.arc(0, 0, r * (1 + .05 * math.sin(T * 6)), 0, 6.29); c.set_source_rgba(*hx(YEL, .18 * glow)); c.fill()
    for bx, by, r in ((-90, -40, 110), (0, -80, 120), (95, -40, 110), (-60, 50, 100), (60, 50, 100)):
        c.arc(bx, by, r, 0, 6.29); c.set_source_rgba(*hx(BRAIN)); c.fill()
    c.save(); c.scale(1.45, 1); c.arc(0, -10, 140, 0, 6.29); c.restore(); ink(c, 9); c.stroke()
    for k in range(7):
        a = -2.6 + k * .55; c.move_to(60 * math.cos(a), 40 * math.sin(a) - 20)
        c.curve_to(120 * math.cos(a) + 20, 90 * math.sin(a), 150 * math.cos(a), 110 * math.sin(a) - 10, 170 * math.cos(a), 120 * math.sin(a))
        c.set_source_rgba(*hx(BRD)); c.set_line_width(8); c.stroke()
    c.move_to(0, -150); c.line_to(0, 120); c.set_source_rgba(*hx(BRD)); c.set_line_width(7); c.stroke()
    c.move_to(-40, 120); c.curve_to(-30, 180, 30, 180, 20, 230); ink(c, 18); c.stroke()
    if glow > 0:
        for k in range(6):
            a = k * 1.05 + T; r = 190 + 20 * math.sin(T * 5 + k)
            c.move_to(r * math.cos(a), r * math.sin(a)); c.line_to((r + 40) * math.cos(a), (r + 40) * math.sin(a)); c.set_source_rgba(*hx(YEL, glow)); c.set_line_width(10); c.stroke()
    if door > 0:
        c.save(); c.translate(-180, 60); c.scale(door, door)
        c.rectangle(-30, -50, 60, 90); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 5); c.stroke(); c.restore()
    c.restore()

def dropper(c, x, y, s, T, drip=True):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(.15)
    c.move_to(-40, -260); c.curve_to(-40, -340, 40, -340, 40, -260); c.line_to(40, -200); c.line_to(-40, -200); c.close_path()
    c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 7); c.stroke()
    c.move_to(-30, -200); c.line_to(30, -200); c.line_to(12, 0); c.line_to(-12, 0); c.close_path(); c.set_source_rgba(.85, .95, 1, .9); c.fill_preserve(); ink(c, 7); c.stroke()
    c.move_to(-24, -120); c.line_to(24, -120); c.line_to(12, 0); c.line_to(-12, 0); c.close_path(); c.set_source_rgba(*hx(CYAN)); c.fill()
    if drip:
        for k in range(2):
            u = (T * 1.3 + k * .5) % 1; dy = 30 + 260 * u * u
            c.move_to(0, dy - 22); c.curve_to(16, dy, 16, dy + 22, 0, dy + 22); c.curve_to(-16, dy + 22, -16, dy, 0, dy - 22)
            c.set_source_rgba(*hx(CYAN, 1 - u * .6)); c.fill_preserve(); ink(c, 4, 1 - u * .6); c.stroke()
    c.restore()

def car(c, x, y, s, T, q=False):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-220, 40); c.line_to(-220, -20); c.curve_to(-200, -60, -140, -70, -110, -70); c.line_to(-60, -140); c.line_to(90, -140); c.line_to(150, -70)
    c.curve_to(200, -66, 230, -40, 230, 0); c.line_to(230, 40); c.close_path(); c.set_source_rgba(*hx(BLUE)); c.fill_preserve(); ink(c, 8); c.stroke()
    c.move_to(-45, -122); c.line_to(20, -122); c.line_to(20, -78); c.line_to(-85, -78); c.close_path(); c.set_source_rgba(*hx('BFE3F2')); c.fill_preserve(); ink(c, 5); c.stroke()
    c.move_to(40, -122); c.line_to(80, -122); c.line_to(118, -78); c.line_to(40, -78); c.close_path(); c.set_source_rgba(*hx('BFE3F2')); c.fill_preserve(); ink(c, 5); c.stroke()
    for wx in (-130, 140): c.arc(wx, 40, 48, 0, 6.29); c.set_source_rgba(*hx('2A2A2A')); c.fill_preserve(); ink(c, 6); c.stroke(); c.arc(wx, 40, 18, 0, 6.29); c.set_source_rgba(.8, .8, .8, 1); c.fill()
    c.restore()

def calendar(c, x, y, s, T, flips=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-170, -150, 340, 320); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
    c.rectangle(-170, -150, 340, 80); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 8); c.stroke()
    for k in range(4):
        for j in range(5):
            c.rectangle(-140 + j * 58, -50 + k * 52, 40, 36); c.set_source_rgba(*hx('E8E2D4')); c.fill()
    for rx in (-90, 90): c.arc(rx, -150, 16, 0, 6.29); ink(c, 7); c.stroke()
    c.restore()

def L_(fn): return cairo_layer(fn)
def pop(T, t0, d=.35): return back(clamp((T - t0) / d))

def s_hook(fr, T):
    bg(fr, T, 'FFE08A', .55); rays(fr, T, 'FFFFFF', .18, 620, 1150)
    def dr(c):
        face(c, 470, 1180, .95 * pop(T, -.4), T, .9 * eout(clamp((T - .8) / .4)))
        dropper(c, 770, 1010 + 10 * math.sin(T * 3), .7 * pop(T, -.3), T)
    overlay(fr, L_(dr))
    tape(fr, 'BACK DOOR?', CX, 440, T + .4, col=RED, size=58, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'OLD MICE.', 570, T + .4, size=130, fill='FFFFFF', rot=-2); title(fr, 'YOUNG BRAINS.', 705, T + .3, size=124, fill=YEL, rot=-2)
    t = wfind(0, 'brain')
    if T > t: chip(fr, 'BRAIN', 330, 900, T - t, CYAN, 38, -5)

def s_sneak(fr, T):
    lt = T - S[1]; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .12)
    u = eout(clamp(lt / 1.8))
    def dr(c):
        brain(c, CX + 40, 1080, .95 * pop(T, S[1]), T, 0, 1.0)
        x = lerp(160, 360, u); y = lerp(1450, 1150, u)
        c.move_to(x, y - 26); c.curve_to(x + 20, y, x + 20, y + 26, x, y + 26); c.curve_to(x - 20, y + 26, x - 20, y, x, y - 26); c.set_source_rgba(*hx(CYAN)); c.fill_preserve(); ink(c, 5); c.stroke()
        c.arc(x - 6, y + 4, 4, 0, 6.29); c.arc(x + 8, y + 4, 4, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    overlay(fr, L_(dr))
    t = wfind(1, 'snuck')
    if T > t: title(fr, 'SNEAKING IN...', 600, T - t, size=110, fill=YEL)

def s_mice(fr, T):
    lt = T - S[2]; bg(fr, T, 'DCE8F2'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, 'SYDNEY, AUSTRALIA', CX, 450, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    def dr(c):
        mouse(c, CX - 40, 1180, .9 * pop(T, S[2] + .1), T)
        dropper(c, CX - 300, 860, .7 * pop(T, wfind(2, 'nose') - .2), T)
    overlay(fr, L_(dr))
    t = wfind(2, 'old')
    if T > t: chip(fr, 'OLD MOUSE', 760, 900, T - t, 'FFFFFF', 36, 4)
    t = wfind(2, 'mrna')
    if T > t: title(fr, 'mRNA DROPS', 620, T - t, size=120, fill=YEL)
    t = wfind(2, 'covid')
    if T > t: chip(fr, 'SAME TECH AS COVID VACCINES', CX, 1440 - 80, T - t, CYAN, 32, -2)

def s_bdnf(fr, T):
    lt = T - S[3]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .16, CX, 1100)
    g = eout(clamp((T - wfind(3, 'booster')) / .6))
    overlay(fr, L_(lambda c: brain(c, CX, 1100, 1.0 * pop(T, S[3]), T, g)))
    tape(fr, 'BUT THIS mRNA...', CX, 450, lt, col=RED, size=56, font=LUCKY, rot=-2, tcol='FFFFFF')
    t = wfind(3, 'booster')
    if T > t: title(fr, 'BRAIN BOOSTER', 620, T - t, size=120, fill=YEL)
    t = wfind(3, 'bdnf')
    if T > t: burst(fr, 'BDNF', 830, 820, T - t, r=120, col=YEL, size=56, rot=8)

def s_result(fr, T):
    lt = T - S[4]; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, 'THE RESULT?', CX, 450, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    tm = wfind(4, 'young')
    def dr(c):
        mouse(c, 300, 960, .55 * pop(T, S[4]), T); mouse(c, 790, 960, .55 * pop(T, S[4] + .15), T * 1.6)
        for k, (x, h) in enumerate(((300, 180 + 200 * eout(clamp((T - wfind(4, 'tests')) / 1.2))), (790, 380))):
            c.rectangle(x - 70, 1500 - h, 140, h); c.set_source_rgba(*hx((GREEN, YEL)[k])); c.fill_preserve(); ink(c, 7); c.stroke()
    overlay(fr, L_(dr))
    chip(fr, 'OLD + DROPS', 300, 1560 - 20, lt - .2, 'FFFFFF', 32, -3); chip(fr, 'YOUNG', 790, 1560 - 20, lt - .3, 'FFFFFF', 32, 3)
    t = wfind(4, 'memory')
    if T > t: title(fr, 'MEMORY TESTS', 610, T - t, size=110, fill=YEL)
    if T > tm: burst(fr, 'SAME!', CX, 880, T - tm, r=120, col=YEL, size=56, rot=-6)

def s_share(fr, T):
    lt = T - S[5]; bg(fr, T, 'FFE08A', .6); rays(fr, T, 'FFFFFF', .2, CX, 1080)
    tape(fr, 'SEND THIS TO...', CX, 450, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: (phone(c, CX, 1080, .85 * pop(T, S[5] - .1)), car(c, CX, 1130, .55 * pop(T, S[5] + .2), T))))
    chip(fr, '@LOST_MY_CAR_AGAIN', CX, 900, lt - .2, CYAN, 34, 0)
    t = wfind(5, 'parked')
    if T > t: burst(fr, 'WHERE?!', 830, 700, T - t, r=130, col=YEL, size=44, rot=10)

def s_catch(fr, T):
    fr[:] = essay_slide(T, [("HERE'S THE CATCH:", 'hl'), ('ONLY MICE.', 'main'), ('SO FAR.', 'grey')], [S[6], wfind(6, 'only'), wfind(6, 'so far')], size=110)
    overlay(fr, L_(lambda c: mouse(c, CX + 40, 1250, .7 * pop(T, wfind(6, 'only')), T)))

def s_trials(fr, T):
    lt = T - S[7]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, 'HUMAN TRIALS?', CX, 450, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: calendar(c, CX, 1120, 1.1 * pop(T, S[7]), T)))
    t = wfind(7, 'two')
    if T > t: title(fr, '~2 YEARS AWAY', 640, T - t, size=118, fill=YEL)

def s_end(fr, T):
    lt = T - S[8]; bg(fr, T, 'DCE8F2'); rays(fr, T, 'FFFFFF', .16, CX, 1150)
    overlay(fr, L_(lambda c: car(c, CX, 1180, 1.0 * pop(T, S[8]), T)))
    tape(fr, 'SO FOR NOW...', CX, 450, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    t = wfind(8, 'remember')
    if T > t: title(fr, 'REMEMBER WHERE', 600, T - t, size=110, fill='FFFFFF')
    t = wfind(8, 'parked')
    if T > t: title(fr, 'YOU PARKED', 730, T - t, size=124, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_sneak), (S[3], s_mice), (S[4], s_bdnf), (S[5], s_result), (S[6], s_share), (S[7], s_catch), (S[8], s_trials), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'door'), wfind(4, 'young'), wfind(8, 'parked')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Research: University of Sydney, Advanced Science (2026). Mouse study.')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
