import sys, os, json, math
sys.path.insert(0, '/home/claude/rodent')
from kit import *
D = '/home/claude/rodent'
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








def rodent(c, x, y, s, T, col='8B6A4A', walk=1.0, flip=False):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    for k, lx in enumerate((-110, -50, 60, 120)):
        sw = 18 * math.sin(T * 7 + k * 1.6) * walk
        c.move_to(lx, 60); c.line_to(lx + sw, 150); c.set_source_rgba(*hx('5E4630')); c.set_line_width(28); c.set_line_cap(1); c.stroke()
    c.move_to(190, 20); c.curve_to(280, 40, 320, -10, 360, 20); c.set_source_rgba(*hx('C98A8A')); c.set_line_width(14); c.stroke()
    c.save(); c.scale(1.6, 1); c.arc(0, 0, 120, 0, 6.29); c.restore(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 8); c.stroke()
    c.save(); c.translate(-200, -40); c.scale(1.3, 1); c.arc(0, 0, 70, 0, 6.29); c.restore(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 8); c.stroke()
    c.arc(-180, -110, 30, 0, 6.29); c.set_source_rgba(*hx('C98A8A')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.arc(-230, -60, 12, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(-290, -30, 14, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(-285, -5, 18, 30); c.set_source_rgba(*hx('F2C94C')); c.fill_preserve(); ink(c, 4); c.stroke()
    c.restore()

def dog(c, x, y, s, T):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    for k, lx in enumerate((-90, -40, 50, 100)): c.move_to(lx, 40); c.line_to(lx + 8 * math.sin(T * 6 + k), 170); c.set_source_rgba(*hx('C98A4B')); c.set_line_width(24); c.set_line_cap(1); c.stroke()
    c.move_to(140, -10); c.line_to(200, -70 + 15 * math.sin(T * 10)); ink(c, 14); c.stroke()
    c.save(); c.scale(1.7, 1); c.arc(0, 0, 80, 0, 6.29); c.restore(); c.set_source_rgba(*hx('C98A4B')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.arc(-150, -80, 62, 0, 6.29); c.set_source_rgba(*hx('C98A4B')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.move_to(-180, -130); c.curve_to(-230, -100, -220, -40, -190, -40); c.set_source_rgba(*hx('7A4E2A')); c.fill_preserve(); ink(c, 5); c.stroke()
    c.arc(-165, -95, 9, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill(); c.arc(-210, -70, 11, 0, 6.29); c.fill()
    c.restore()

def tooth(c, x, y, s, T, col='E8DCC4'):
    if s < .01: return
    c.save(); c.translate(x, y); c.rotate(.05 * math.sin(T * 2)); c.scale(s, s)
    c.move_to(-120, -60); c.curve_to(-130, -140, -40, -150, 0, -110); c.curve_to(40, -150, 130, -140, 120, -60)
    c.curve_to(120, 20, 90, 60, 70, 60); c.line_to(60, 150); c.curve_to(40, 170, 20, 170, 10, 120); c.line_to(-10, 120); c.curve_to(-20, 170, -40, 170, -60, 150); c.line_to(-70, 60); c.curve_to(-90, 60, -120, 20, -120, -60)
    c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 8); c.stroke()
    for k in range(3): c.move_to(-80 + k * 50, -90); c.curve_to(-70 + k * 50, -40, -60 + k * 50, -40, -50 + k * 50, -80); c.set_source_rgba(*hx('8E8270', .6)); c.set_line_width(5); c.stroke()
    c.restore()

def scale_(c, x, y, s, tilt):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, 0); c.line_to(0, 300); ink(c, 12); c.stroke()
    c.rectangle(-120, 300, 240, 40); c.set_source_rgba(*hx('8E949C')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.save(); c.rotate(tilt); c.move_to(-320, 0); c.line_to(320, 0); ink(c, 12); c.stroke(); c.restore()
    c.restore()

def mine(c, T):
    c.rectangle(0, 700, W, 1000); c.set_source_rgba(*hx('3A3530')); c.fill()
    for k, (y, col) in enumerate(((820, '2B2622'), (980, '6E6A63'), (1140, '2B2622'))):
        c.rectangle(0, y, W, 130); c.set_source_rgba(*hx(col)); c.fill()
    c.move_to(0, 700); c.line_to(W, 700); ink(c, 8); c.stroke()

def L_(fn): return cairo_layer(fn)

def s_hook(fr, T):
    bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .16)
    u = eout(clamp((T + .9) / 1.6))
    overlay(fr, L_(lambda c: (dog(c, lerp(1200, 780, u), 1130, .75, T), rodent(c, lerp(-200, 330, u), 1130, .8, T))))
    if T > wfind(0, 'real'): burst(fr, 'REAL!', 820, 860, T - wfind(0, 'real'), r=110, col=YEL, size=48, rot=10)
    tape(fr, 'A DOG-SIZED RODENT', CX, 470, T + .4, col=RED, size=58, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'FROM JUST', 600, T + .4, size=124, fill='FFFFFF', rot=-2); title(fr, 'ONE TOOTH', 730, T + .3, size=140, fill=YEL, rot=-2)

def s_weight(fr, T):
    lt = T - S[1]; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'HOW HEAVY?', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    tilt = .12 * math.sin(T * 2) * math.exp(-lt * .8)
    overlay(fr, L_(lambda c: (scale_(c, CX, 1000, 1.1, tilt), rodent(c, 260, 1000 + 290 * math.sin(tilt) - 150, .55, T, walk=0), dog(c, 830, 1000 - 290 * math.sin(tilt) - 160, .55, T))))
    title(fr, '~66 LBS', 620, lt, size=140, fill=YEL)
    if T > wfind(1, 'thailand'): chip(fr, 'THAILAND, 35 MILLION YEARS AGO', CX, 1360, T - wfind(1, 'thailand'), 'FFFFFF', 32, -2)

def s_mine(fr, T):
    lt = T - S[2]; bg(fr, T, 'C9DDF0')
    overlay(fr, L_(lambda c: (mine(c, T), tooth(c, CX, 1050, .5 * back(clamp((lt - .5) / .35)), T))))
    tape(fr, 'COAL MINE', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    if T > wfind(2, 'swamp'): chip(fr, 'OLD SWAMP CLAY', CX, 1300, T - wfind(2, 'swamp'), YEL, 38, -2)

def s_one(fr, T):
    fr[:] = essay_slide(T, [('ALL THEY FOUND:', 'grey'), ('ONE TOOTH.', 'hl')], [S[3], wfind(3, 'tooth')], size=128)
    overlay(fr, L_(lambda c: tooth(c, CX, 1160, .7 * back(clamp((T - wfind(3, 'tooth')) / .35)) if T > wfind(3, 'tooth') else 0, T)))

def s_chip(fr, T):
    lt = T - S[4]; bg(fr, T, 'F7E3C8'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, "THAT'S IT", CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    overlay(fr, L_(lambda c: (tooth(c, 380, 1050, .9, T), tooth(c, 790, 1120, .35 * back(clamp(lt / .3)), T + 1, 'D9CFC0'))))
    chip(fr, '+ A CHIP OF ANOTHER', 760, 1260, lt - .2, YEL, 34, 3)

def s_huge(fr, T):
    lt = T - S[5]; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'BIG TOOTH', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    g = eout(clamp((T - wfind(5, 'huge')) / .6)) if T > wfind(5, 'huge') else 0
    overlay(fr, L_(lambda c: (tooth(c, 380, 1060, .5 + .5 * g, T), tooth(c, 820, 1150, .4, T + 1, 'D9CFC0'))))
    chip(fr, 'THIS ONE', 380, 1350, lt - .2, YEL, 36, -3); chip(fr, 'ASIAN COUSINS', 820, 1350, lt - .4, 'FFFFFF', 32, 3)
    if T > wfind(5, 'twice'): title(fr, '2X BIGGER', 620, T - wfind(5, 'twice'), size=130, fill=YEL)

def s_back(fr, T):
    lt = T - S[6]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'WORK BACKWARD', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    u = eout(clamp((lt - .3) / 1.8))
    def dr(c):
        tooth(c, 240, 1000, .45, T)
        c.move_to(360, 1000); c.line_to(360 + 160 * u, 1000); c.set_source_rgba(*hx(RED)); c.set_line_width(14); c.stroke()
        if u > .3: rodent(c, 760, 1060, .7 * clamp((u - .3) / .7), T, walk=.3)
    overlay(fr, L_(dr))
    title(fr, 'TOOTH TO BODY', 620, lt, size=120, fill=YEL)

def s_guess(fr, T):
    fr[:] = essay_slide(T, [('A BALLPARK.', 'hl'), ('LOTS OF GUESSWORK.', 'main')], [S[7] + .2, wfind(7, 'guesswork')], size=112)
    overlay(fr, L_(lambda c: rodent(c, CX + 40, 1220, .55, T, walk=.2)))
    burst(fr, '?', 820, 1050, T - S[7] - .4, r=100, col=YEL, size=90, rot=8)

def s_early(fr, T):
    lt = T - S[8]; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, 'WHY IT MATTERS', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    def dr(c):
        x0, x1, y = 120, 960, 1080
        c.move_to(x0, y); c.line_to(x1, y); ink(c, 10); c.stroke()
        for v, lab, col in ((35, '', RED), (4, '', '1C1614')):
            x = x1 - (x1 - x0) * v / 40; c.arc(x, y, 26, 0, 6.29); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 5); c.stroke()
        rodent(c, x0 + 120, y - 160, .35, T)
    overlay(fr, L_(dr))
    chip(fr, 'THIS RODENT: 35M YRS', 300, 1200, lt - .2, YEL, 30, -3); chip(fr, 'S. AMERICA GIANTS: ~4M', 760, 1200, lt - .5, 'FFFFFF', 30, 3)
    if T > wfind(8, 'earlier'): title(fr, 'WAY EARLIER', 640, T - wfind(8, 'earlier'), size=130, fill=YEL)

def s_end(fr, T):
    lt = T - S[9]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .16)
    tape(fr, 'BE GLAD', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    u = eout(clamp(lt / 1.5))
    overlay(fr, L_(lambda c: (dog(c, 780, 1130, .75, T), rodent(c, lerp(-200, 330, u), 1130, .8, T))))
    if T > wfind(9, 'glad'): title(fr, "IT'S NOT THIS SIZE", 640, T - wfind(9, 'glad'), size=104, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_weight), (S[3], s_mine), (S[4], s_one), (S[5], s_chip), (S[6], s_huge), (S[7], s_back), (S[8], s_guess), (S[9], s_early), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'real'), wfind(3, 'tooth'), wfind(5, 'huge')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Study: Chaimanee et al., Scientific Reports (2026)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
