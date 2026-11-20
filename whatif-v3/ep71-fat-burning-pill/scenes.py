import sys, os, json, math
sys.path.insert(0, '/home/claude/tofa')
from kit import *
D = '/home/claude/tofa'
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

MOUSE = st('mouse', w=560); CAP = st('capsule', w=520); SCALE = st('scale', w=460); BURG = st('burger', w=420)
PEN = st('pen', w=560); BICEP = st('bicep', w=480); PLATE = st('plate', w=480)

def flames(c, x, y, s, T, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for k, (col, sc) in enumerate((('FF3B1F', 1.0), ('FF9A1F', .72), ('FFE14D', .45))):
        c.new_path(); w = 150 * sc; h = 300 * sc
        wob = [math.sin(T * 9 + j * 1.7 + k) * 16 * sc for j in range(5)]
        c.move_to(-w, 0); c.curve_to(-w * 1.1, -h * .4 + wob[0], -w * .3, -h * .6, -w * .45, -h + wob[1])
        c.curve_to(-w * .1, -h * .7, w * .15, -h * .9 + wob[2], w * .3, -h * 1.1 + wob[3])
        c.curve_to(w * .5, -h * .7, w * 1.15, -h * .45 + wob[4], w, 0); c.curve_to(w * .6, h * .35, -w * .6, h * .35, -w, 0); c.close_path()
        c.set_source_rgba(*hx(col, a)); c.fill_preserve()
        if k == 0: ink(c, 8, a); c.stroke()
        else: c.new_path()
    c.restore()

def body(c, x, y, s, fire=0.0, T=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    def shape(dx, dy):
        c.new_path(); c.arc(dx, -360 + dy, 95, 0, 2 * math.pi)
        c.move_to(-170 + dx, -220 + dy); c.line_to(170 + dx, -220 + dy); c.line_to(150 + dx, 120 + dy); c.line_to(100 + dx, 420 + dy); c.line_to(-100 + dx, 420 + dy); c.line_to(-150 + dx, 120 + dy); c.close_path()
    shape(14, 16); c.set_source_rgba(*hx('1C1614')); c.fill()
    shape(0, 0); c.set_source_rgba(*hx('FFFFFF')); c.fill_preserve(); ink(c, 9); c.stroke()
    c.restore()
    if fire > 0: flames(c, x, y + 60 * s, s * .9 * fire, T)

def chart(c, T, t0, x0=170, y0=1300, w=740, h=520):
    ink(c, 7); c.move_to(x0, y0 - h); c.line_to(x0, y0); c.line_to(x0 + w, y0); c.stroke()
    p = clamp((T - t0) / 1.8); stop = x0 + w * .4
    c.move_to(stop, y0 - h); c.line_to(stop, y0); c.set_source_rgba(*hx('1C1614', .5)); c.set_line_width(4); c.set_dash([14, 10]); c.stroke(); c.set_dash([])
    for col, fn in ((RED, lambda u: .35 if u < .4 else .35 + (u - .4) * 1.0), (GREEN, lambda u: .35 if u < .4 else .35 + (u - .4) * .1)):
        c.new_path(); n = int(60 * p)
        for j in range(n + 1):
            u = j / 60; c.line_to(x0 + w * u, y0 - h * fn(u))
        c.set_source_rgba(*hx(col)); c.set_line_width(14); c.stroke()

def arm(c, x, y, s, flex=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    def sh(dx, dy):
        c.new_path(); c.move_to(-260 + dx, 160 + dy); c.curve_to(-200 + dx, 60 + dy, -60 + dx, 40 + dy, 40 + dx, 70 + dy)
        c.curve_to(60 + dx, -40 - 60 * flex + dy, -40 + dx, -120 + dy, -10 + dx, -230 + dy); c.curve_to(30 + dx, -300 + dy, 150 + dx, -290 + dy, 150 + dx, -200 + dy)
        c.curve_to(150 + dx, -130 + dy, 110 + dx, -90 + dy, 140 + dx, 0 + dy); c.curve_to(170 + dx, 120 + dy, 120 + dx, 230 + dy, -40 + dx, 240 + dy)
        c.curve_to(-140 + dx, 245 + dy, -230 + dx, 230 + dy, -260 + dx, 160 + dy); c.close_path()
    sh(14, 16); c.set_source_rgba(*hx('1C1614')); c.fill()
    sh(0, 0); c.set_source_rgba(*hx('F2B48C')); c.fill_preserve(); ink(c, 9); c.stroke()
    c.arc(-70, -10 - 30 * flex, 70 + 40 * flex, math.pi * 1.1, math.pi * 1.9); ink(c, 7); c.stroke()
    c.restore()

def s_hook(fr, T):
    fr[:] = paper('FF8C1A', .72); rays(fr, T, 'FFFFFF', .14, cy=1080)
    overlay(fr, cairo_layer(lambda c: flames(c, CX, 1320, 1.5, T, .95)))
    sk(fr, CAP, CX, 1050, T, 0, 1.0, -18)
    sk(fr, BURG, 250, 1260, T, 1, .7, -8)
    tape(fr, 'A PILL THAT BURNS FAT', CX, 470, 1.0, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    title(fr, 'WITHOUT EATING LESS?', 600, 1.0, size=88, fill=YEL, rot=-3)

def s_question(fr, T):
    lt = T - S[1]; fr[:] = paper(BLUE, .68); rays(fr, T, 'FFFFFF', .1)
    overlay(fr, cairo_layer(lambda c: body(c, CX, 1060, .95, clamp((lt - .6) / .8), T)))
    tape(fr, 'WHAT IF YOUR BODY', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    title(fr, 'JUST BURNED MORE?', 590, lt - .15, size=96, fill=YEL)

def s_glp(fr, T):
    lt = T - S[2]; fr[:] = paper(CYAN, .55); rays(fr, T, 'FFFFFF', .12)
    sk(fr, PEN, 330, 960, T, 2, .8, -25, lt)
    sh = 1 - .5 * eout((T - wfind(2, 'less hungry')) / .8)
    sk(fr, PLATE, 770, 1080, T, 3, .85 * sh, 4, lt - .2)
    tape(fr, 'OZEMPIC-STYLE DRUGS', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    chip(fr, 'MAKE YOU LESS HUNGRY', CX, 600, T - wfind(2, 'less hungry') + .2, YEL, 44, -2)

def s_catch1(fr, T):
    lt = T - S[3]; fr[:] = paper(RED, .74); rays(fr, T, 'FFFFFF', .1)
    tw = wfind(3, 'weight')
    sh = 1 - .35 * eout((T - wfind(3, 'muscle')) / 1.0)
    if T < tw - .2:
        overlay(fr, cairo_layer(lambda c: arm(c, CX, 1060, 1.3 * sh, sh)))
        chip(fr, 'MUSCLE LOSS', CX, 1340, T - wfind(3, 'muscle'), YEL, 50, -3)
        tape(fr, 'BUT SOME PEOPLE...', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    else:
        l2 = T - tw + .2; sk(fr, SCALE, CX, 1060, T, 5, .95, 3, l2)
        def arr(c):
            p = eout(l2 / .6); c.move_to(860, 1250); c.line_to(860, 1250 - 360 * p); ink(c, 26); c.stroke()
            c.move_to(860, 1250); c.line_to(860, 1250 - 360 * p); c.set_source_rgba(*hx(YEL)); c.set_line_width(14); c.stroke()
            if p > .9: c.move_to(800, 920); c.line_to(860, 860); c.line_to(920, 920); ink(c, 16); c.stroke()
        overlay(fr, cairo_layer(arr))
        tape(fr, 'THE WEIGHT COMES BACK', CX, 470, l2, col='FFFFFF', size=54, font=LUCKY, rot=-2)

def s_lab(fr, T):
    lt = T - S[4]; fr[:] = paper(None); rays(fr, T, YEL, .16)
    ph = photo('lab', 820, 560, (.5, .4))
    if ph is not None: put_rgba(fr, ph, CX, 960, back(clamp(lt / .35)), 1.0, -2)
    tt = wfind(4, 'tofa')
    if T > tt - .2: sk(fr, CAP, 790, 1250, T, 6, .62, -15, T - tt + .2); tape(fr, 'TOFA', 790, 1250, T - tt, col=RED, size=60, font=LUCKY, rot=-6, tcol='FFFFFF')
    tape(fr, 'UC BERKELEY SCIENTISTS', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    chip(fr, 'AN OLD COMPOUND', CX, 590, T - wfind(4, 'old'), YEL, 44, 2)

def s_mice(fr, T):
    lt = T - S[5]; fr[:] = paper(GREEN, .55); rays(fr, T, 'FFFFFF', .12)
    t18 = wfind(6, 'eighteen')
    sh = 1 - .18 * eout((T - t18) / 1.0)
    sk(fr, MOUSE, 400, 1050, T, 7, .95 * sh, -4)
    sk(fr, PLATE, 820, 1180, T, 8, .55, 6)
    chip(fr, 'SAME FOOD', 820, 960, lt - .3, 'FFFFFF', 44, 3)
    tape(fr, 'OBESE MICE', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    if T > t18: stat(fr, '-18%', 'BODY WEIGHT', CX, 610, T - t18, RED, -3, 150)

def s_energy(fr, T):
    lt = T - S[7]; fr[:] = paper('FF8C1A', .7); rays(fr, T, 'FFFFFF', .12)
    overlay(fr, cairo_layer(lambda c: flames(c, 380, 1300, 1.0 + .5 * eout(lt / 1.5), T)))
    sk(fr, MOUSE, 380, 1060, T, 9, .7, 3)
    def meter(c):
        p = eout((lt - .3) / 1.2); x, y0, h = 820, 1320, 600
        c.rectangle(x - 60 + 12, y0 - h + 14, 120, h); c.set_source_rgba(*hx('1C1614')); c.fill()
        c.rectangle(x - 60, y0 - h, 120, h); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
        c.rectangle(x - 48, y0 - h * .82 * p, 96, h * .82 * p - 12); c.set_source_rgba(*hx(RED)); c.fill()
    overlay(fr, cairo_layer(meter))
    tape(fr, 'BURNED MORE ENERGY', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    stat(fr, '+18%', 'UP TO', 520, 640, lt - wfind(7, 'eighteen') + S[7], YEL, 3, 120)

def s_muscle(fr, T):
    lt = T - S[8]; fr[:] = paper(PINK, .55); rays(fr, T, 'FFFFFF', .14)
    overlay(fr, cairo_layer(lambda c: arm(c, CX, 1060, 1.4 * back(clamp(lt / .35)), 1.0)))
    tape(fr, 'AND THE MUSCLE?', CX, 470, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    if T > S[9]: burst(fr, 'IT STAYED!', 800, 760, T - S[9], r=160, col=GREEN, size=48, rot=8)

def s_combo(fr, T):
    lt = T - S[10]; fr[:] = paper(YEL, .55); rays(fr, T, 'FFFFFF', .14)
    sk(fr, CAP, 300, 1000, T, 11, .6, -20, lt); sk(fr, PEN, 780, 1000, T, 12, .6, -25, lt - .3)
    burst(fr, '+', CX, 1000, lt - .5, r=80, col=RED, size=90)
    tape(fr, 'MIX IT WITH OZEMPIC-STYLE DRUGS', CX, 470, lt, col='FFFFFF', size=40, font=LUCKY, rot=-2)
    if T > wfind(10, 'even better'): title(fr, 'EVEN BETTER', 600, T - wfind(10, 'even better'), size=110, fill=RED)

def s_regain(fr, T):
    lt = T - S[11]; fr[:] = paper(None); rays(fr, T, CYAN, .14)
    overlay(fr, cairo_layer(lambda c: chart(c, T, S[11] + .2)))
    tape(fr, 'AFTER TREATMENT STOPPED', CX, 470, lt, col='FFFFFF', size=52, font=LUCKY, rot=-2)
    chip(fr, 'STOP', 466, 760, lt - .3, 'FFFFFF', 34, 0)
    if lt > 1.4:
        chip(fr, 'OZEMPIC-STYLE: WEIGHT BACK', 690, 820, lt - 1.4, RED, 32, -2)
        chip(fr, 'TOFA: STAYED DOWN', 720, 1080, lt - 1.6, GREEN, 34, 2)
    credit(fr, 'Chart: simplified illustration of mouse results')

def s_next(fr, T):
    lt = T - S[12]; fr[:] = paper(RED, .8); rays(fr, T, 'FFFFFF', .14)
    title(fr, 'SO WHAT', 860, lt, size=170, fill='FFFFFF'); title(fr, 'HAPPENS NEXT?', 1060, lt - .15, size=130, fill=YEL)

def s_catch(fr, T):
    lt = T - S[13]; fr[:] = paper('2A2F5A', .82); rays(fr, T, 'FFFFFF', .08)
    sk(fr, MOUSE, CX, 1030, T, 13, .85, 0)
    tape(fr, "HERE'S THE CATCH", CX, 470, lt, col=YEL, size=60, font=LUCKY, rot=-2)
    chip(fr, 'ONLY MALE MICE', CX, 600, T - wfind(13, 'only'), 'FFFFFF', 46, 2)
    if T > S[14]:
        for k, (w, txt, x, y) in enumerate((('human', 'NO HUMAN TRIALS', 300, 760), ('dose', 'RIGHT DOSE?', 800, 820), ('safe', 'LONG-TERM SAFE?', 330, 1300))):
            chip(fr, txt, x, y, T - wfind(14, w), (RED, YEL, CYAN)[k], 40, (-3, 3, -2)[k])

def s_future(fr, T):
    lt = T - S[15]; fr[:] = paper('FF8C1A', .72); rays(fr, T, 'FFFFFF', .14)
    overlay(fr, cairo_layer(lambda c: flames(c, CX, 1330, 1.3, T)))
    sk(fr, CAP, CX, 1060, T, 14, .9, -15)
    tape(fr, 'IF IT WORKS IN PEOPLE...', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    te = wfind(16, 'eat less'); tb = wfind(16, 'burn more')
    if T > te: tape(fr, 'EAT LESS', 300, 640, T - te, col='FFFFFF', size=56, font=LUCKY, rot=-4); xstamp(fr, 300, 640, T - te - .3, .45)
    if T > tb: title(fr, 'BURN MORE', 640, T - tb, size=88, fill=YEL, rot=3, maxw=440, cx=760)

def s_end(fr, T):
    lt = T - S[17]; fr[:] = paper(BLUE, .7); rays(fr, T, 'FFFFFF', .1)
    sk(fr, CAP, CX, 1050, T, 15, .95, -15)
    title(fr, 'WOULD YOU TRY IT?', 560, lt, size=100, fill=YEL)
    if T > S[18]:
        burst(fr, 'YES', 260, 1250, T - S[18], r=110, col=GREEN, size=60, rot=-8)
        burst(fr, 'NO', 820, 1250, T - S[18] - .15, r=110, col=RED, size=60, rot=8)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_question), (S[3], s_glp), (S[4], s_catch1), (S[5], s_lab), (S[7], s_mice), (S[8], s_energy), (S[10], s_muscle),
           (S[11], s_combo), (S[12], s_regain), (S[13], s_next), (S[15], s_catch), (S[17], s_future), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(6, 'eighteen'), S[9], wfind(10, 'even better'), wfind(16, 'burn more')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END and not (S[11] <= T < S[12]): credit(fr, 'Photos: Wikimedia Commons (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
