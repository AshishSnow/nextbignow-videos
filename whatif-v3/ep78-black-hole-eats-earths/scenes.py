import sys, os, json, math
sys.path.insert(0, '/home/claude/bh')
from kit import *
D = '/home/claude/bh'
L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]
END = E[-1] + 0.3; TOTAL = END + 2.6
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

def space(fr, T, tint='0B1026'):
    fr[:] = paper(tint, .9)
    def st_(c):
        rng = np.random.default_rng(1)
        for k in range(120):
            x, y = rng.uniform(0, W), rng.uniform(0, H); r = rng.uniform(1, 4); tw = .5 + .5 * math.sin(T * 3 + k)
            c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(1, 1, .9, .4 + .5 * tw); c.fill()
    overlay(fr, cairo_layer(st_))

def blackhole(c, x, y, r, T, eat=0.0):
    for k in range(10, 0, -1):
        rr = r * (1 + k * .18); a = .05 * (11 - k)
        c.save(); c.translate(x, y); c.scale(1, .45); c.arc(0, 0, rr, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(1, .55 + .03 * k, .15, a); c.fill()
    c.save(); c.translate(x, y); c.rotate(T * .4)
    for k in range(3):
        c.save(); c.scale(1, .4); c.arc(0, 0, r * (1.3 + k * .25), 0, 2 * math.pi); c.restore(); c.set_source_rgba(1, .8, .3, .5 - k * .12); c.set_line_width(14 - k * 3); c.stroke()
    c.restore()
    c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(0, 0, 0, 1); c.fill()
    c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(1, .7, .3, .9); c.set_line_width(5); c.stroke()

def clumps(c, x, y, T, n=5, r0=420, speed=.12, col='7FDBFF'):
    for k in range(n):
        u = ((T * speed + k / n) % 1); rr = r0 * (1 - u); ang = u * 7 + k * 1.3
        px, py = x + math.cos(ang) * rr, y + math.sin(ang) * rr * .5
        c.arc(px + 4, py + 5, 18 * (1 - u * .6), 0, 2 * math.pi); c.set_source_rgba(0, 0, 0, .5); c.fill()
        c.arc(px, py, 18 * (1 - u * .6), 0, 2 * math.pi); c.set_source_rgba(*hx(col, 1 - u * .5)); c.fill()

def binary(c, x, y, s, T, wind=1.0):
    a = T * 1.5
    for k, col in ((0, 'FFF1A8'), (1, '9FD3FF')):
        ang = a + k * math.pi; px, py = x + math.cos(ang) * 60 * s, y + math.sin(ang) * 25 * s
        for g in range(6, 0, -1):
            c.arc(px, py, (40 + g * 10) * s, 0, 2 * math.pi); c.set_source_rgba(*hx(col, .06)); c.fill()
        c.arc(px, py, 45 * s, 0, 2 * math.pi); c.set_source_rgba(*hx(col)); c.fill()
    if wind > 0:
        for k in range(16):
            ang = k / 16 * 2 * math.pi + T * .3; ph = (T * .8 + k * .13) % 1
            r1 = (80 + ph * 260) * s
            c.move_to(x + math.cos(ang) * r1, y + math.sin(ang) * r1); c.line_to(x + math.cos(ang) * (r1 + 40 * s), y + math.sin(ang) * (r1 + 40 * s))
            c.set_source_rgba(1, 1, 1, wind * (1 - ph)); c.set_line_width(6); c.stroke()

def s_hook(fr, T):
    space(fr, T)
    ph = load_st('earth', w=300)
    def dr(c): blackhole(c, CX, 1080, 150, T); clumps(c, CX, 1080, T, 4)
    overlay(fr, cairo_layer(dr))
    if ph is not None:
        u = clamp(T / 4.5); put_rgba(fr, ph, lerp(860, CX + 40, eout(u)), lerp(820, 1060, eout(u)), lerp(.7, .15, u), 1.0 - .8 * u, T * 40)
    tape(fr, 'AN EARTH OF GAS', CX, 470, 1.0, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    title(fr, 'EVERY 10 YEARS', 600, 1.0, size=118, fill=YEL, rot=-3)

def s_question(fr, T):
    lt = T - S[1]; space(fr, T, '1B1040')
    ph = photo('center', 760, 520, (.5, .5))
    if ph is not None: put_rgba(fr, ph, CX, 1010, back(clamp(lt / .35)), 1.0, -2)
    tape(fr, "WHO'S FEEDING THE MONSTER", CX, 470, lt, col='FFFFFF', size=52, font=LUCKY, rot=-2)
    title(fr, 'IN THE MILKY WAY?', 590, lt - .15, size=100, fill=YEL)

def s_sgra(fr, T):
    lt = T - S[2]; space(fr, T)
    ph = photo('sgra', 600, 600)
    if ph is not None: put_rgba(fr, ph, CX, 1030, back(clamp(lt / .35)), 1.0, 0)
    else: overlay(fr, cairo_layer(lambda c: blackhole(c, CX, 1030, 200, T)))
    tape(fr, 'SAGITTARIUS A*', CX, 470, lt, col='FFFFFF', size=64, font=LUCKY, rot=-2)
    tm = wfind(2, 'four million')
    if T > tm: stat(fr, '4,000,000x', 'HEAVIER THAN THE SUN', CX, 610, T - tm, YEL, -3, 110)

def s_mystery(fr, T):
    lt = T - S[3]; space(fr, T, '102040')
    def dr(c): blackhole(c, CX, 1050, 120, T); clumps(c, CX, 1050, T, 6, col='C084FC')
    overlay(fr, cairo_layer(dr))
    tape(fr, 'STRANGE GLOWING GAS CLOUDS', CX, 470, lt, col='FFFFFF', size=50, font=LUCKY, rot=-2)
    tn = wfind(3, 'nobody')
    if T > tn: burst(fr, '???', 830, 780, T - tn, r=110, col=RED, size=70)
    chip(fr, 'G1   G2   G2t', CX, 600, lt - 1.5, CYAN, 44, 2)

def s_culprit(fr, T):
    lt = T - S[4]; space(fr, T, '2A1040')
    overlay(fr, cairo_layer(lambda c: binary(c, CX, 1040, 2.0, T, 0)))
    tape(fr, 'THE CULPRIT', CX, 470, lt, col=RED, size=66, font=LUCKY, rot=-2, tcol='FFFFFF')
    tt = wfind(4, 'two giant')
    if T > tt: title(fr, 'TWO GIANT STARS', 600, T - tt, size=110, fill=YEL)
    if T > wfind(4, 'touching'): chip(fr, 'SO CLOSE THEY TOUCH', CX, 1330, T - wfind(4, 'touching'), 'FFFFFF', 44, -2)

def s_winds(fr, T):
    lt = T - S[5]; space(fr, T, '1B1040')
    overlay(fr, cairo_layer(lambda c: binary(c, CX, 1040, 1.6, T, 1.0)))
    tape(fr, 'THEIR WINDS COLLIDE', CX, 470, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    tk = wfind(5, 'thousands')
    if T > tk: stat(fr, 'THOUSANDS OF KM/S', 'WIND SPEED', CX, 610, T - tk, RED, -3, 84)
    if T > wfind(5, 'smash'): burst(fr, 'SMASH!', 820, 1320 - 60, T - wfind(5, 'smash'), r=110, col=YEL, size=46)

def s_clump(fr, T):
    lt = T - S[6]; space(fr, T)
    overlay(fr, cairo_layer(lambda c: (binary(c, 330, 1000, .9, T, .6), clumps(c, 760, 1020, T * .3, 3, 200))))
    ph = load_st('earth', w=260)
    te = wfind(6, 'earth')
    if ph is not None and T > te - .2: put_rgba(fr, ph, 780, 1300 - 60, back(clamp((T - te + .2) / .3)) * .8, 1.0, 0)
    tape(fr, 'GAS GETS SQUEEZED INTO CLUMPS', CX, 470, lt, col='FFFFFF', size=48, font=LUCKY, rot=-2)
    if T > te: chip(fr, 'EACH = ABOUT 1 EARTH', CX, 600, T - te, YEL, 44, 2)

def s_fall(fr, T):
    lt = T - S[7]; space(fr, T, '0B1026')
    def dr(c): blackhole(c, CX, 1060, 170, T); clumps(c, CX, 1060, T * 2, 3, 520, .25)
    overlay(fr, cairo_layer(dr))
    tape(fr, 'AND THEN THEY FALL', CX, 470, lt, col=RED, size=64, font=LUCKY, rot=-2, tcol='FFFFFF')

def s_fed(fr, T):
    lt = T - S[8]; space(fr, T, '1B2A6B')
    def dr(c):
        blackhole(c, CX, 1080, 150, T)
        for k in range(10):
            x = 170 + k * 82; on = clamp((lt - .3 - k * .2) / .2)
            c.arc(x, 820, 22, 0, 2 * math.pi); c.set_source_rgba(*hx(CYAN if k == 9 else '4A5568', .3 + .7 * on)); c.fill()
    overlay(fr, cairo_layer(dr))
    tape(fr, 'ONE CLUMP EVERY 10 YEARS', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    if T > wfind(8, 'fed'): title(fr, 'KEEPS IT FED', 620, T - wfind(8, 'fed'), size=110, fill=YEL)

def s_next(fr, T):
    lt = T - S[9]; fr[:] = paper(RED, .8); rays(fr, T, 'FFFFFF', .14)
    title(fr, 'SO WHAT', 860, lt, size=170, fill='FFFFFF'); title(fr, 'HAPPENS NEXT?', 1060, lt - .15, size=130, fill=YEL)

def s_scopes(fr, T):
    lt = T - S[10]; space(fr, T, '102040')
    ph = photo('vlt', 780, 520, (.5, .5))
    if ph is not None: put_rgba(fr, ph, CX, 1010, back(clamp(lt / .35)), 1.0, -2)
    tape(fr, 'BIGGER TELESCOPES ARE COMING', CX, 470, lt, col='FFFFFF', size=50, font=LUCKY, rot=-2)
    if T > wfind(10, 'more'): chip(fr, 'MORE GAS STREAMS TO FIND', CX, 600, T - wfind(10, 'more'), YEL, 42, 2)

def s_dinner(fr, T):
    lt = T - S[11]; space(fr, T)
    def dr(c):
        blackhole(c, CX, 1060, 180, T); clumps(c, CX, 1060, T, 5)
        c.rectangle(CX - 330, 1300, 660, 22); c.set_source_rgba(*hx('C8A27A')); c.fill()
    overlay(fr, cairo_layer(dr))
    tape(fr, "A BLACK HOLE'S DINNER", CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    if T > wfind(11, 'real time'): title(fr, 'ALMOST LIVE', 600, T - wfind(11, 'real time'), size=110, fill=YEL)

def s_end(fr, T):
    lt = T - S[12]; space(fr, T, '1B1040')
    overlay(fr, cairo_layer(lambda c: blackhole(c, CX, 1060, 180, T)))
    title(fr, 'WANT A CLOSER LOOK?', 560, lt, size=96, fill=YEL)
    if T > S[13]:
        burst(fr, 'YES', 230, 1280, T - S[13], r=100, col=GREEN, size=54, rot=-8)
        burst(fr, 'NO', 850, 1280, T - S[13] - .15, r=100, col=RED, size=54, rot=8)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_question), (S[3], s_sgra), (S[4], s_mystery), (S[5], s_culprit), (S[6], s_winds), (S[7], s_clump), (S[8], s_fall),
           (S[9], s_fed), (S[10], s_next), (S[11], s_scopes), (S[12], s_dinner), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(4, 'culprit'), wfind(5, 'smash'), S[7] + 1.5):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Images: Wikimedia Commons / ESO / NASA (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
