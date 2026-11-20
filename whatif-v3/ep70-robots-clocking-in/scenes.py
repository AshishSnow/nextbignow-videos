import sys, os, json, math
sys.path.insert(0, '/home/claude/robots')
from kit import *
D = '/home/claude/robots'
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

ROB = st('robot', h=900); ROBS = st('robot', h=300); DIG = st('digit', h=820); WRK = st('worker', h=820)
BOX = st('box', w=260)

def conveyor(c, y, T, x0=60, x1=1020, speed=120):
    c.rectangle(x0 + 10, y + 12, x1 - x0, 60); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(x0, y, x1 - x0, 60); c.set_source_rgba(*hx('4A5568')); c.fill_preserve(); ink(c, 7); c.stroke()
    off = (T * speed) % 60
    for x in np.arange(x0 - 60 + off, x1, 60):
        if x0 < x < x1: c.move_to(x, y + 6); c.line_to(x - 20, y + 54); ink(c, 4, .6); c.stroke()
    for x in np.arange(x0 + 40, x1, 120):
        c.arc(x, y + 30, 18, 0, 2 * math.pi); c.set_source_rgba(*hx('A0AEC0')); c.fill_preserve(); ink(c, 4); c.stroke()

def timeclock(c, x, y, s, stamp=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-170 + 12, -230 + 14, 340, 460); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(-170, -230, 340, 460); c.set_source_rgba(*hx('E2E8F0')); c.fill_preserve(); ink(c, 9); c.stroke()
    c.arc(0, -90, 100, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
    c.move_to(0, -90); c.line_to(0, -160); ink(c, 9); c.stroke(); c.move_to(0, -90); c.line_to(55, -90); ink(c, 9); c.stroke()
    c.rectangle(-110, 60, 220, 40); c.set_source_rgba(*hx('1C1614')); c.fill()
    cy = lerp(-10, 70, eout(stamp)); c.rectangle(-80, cy + 60, 160, 210); c.set_source_rgba(*hx('FFF8E1')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.restore()

def clock24(c, x, y, r, T, spin=1.0):
    c.arc(x + 12, y + 14, r, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 10); c.stroke()
    for k in range(12):
        a = k * math.pi / 6; c.move_to(x + math.cos(a) * r * .82, y + math.sin(a) * r * .82); c.line_to(x + math.cos(a) * r * .93, y + math.sin(a) * r * .93); ink(c, 7); c.stroke()
    a1 = T * 6 * spin - math.pi / 2; a2 = T * .5 * spin - math.pi / 2
    c.move_to(x, y); c.line_to(x + math.cos(a1) * r * .78, y + math.sin(a1) * r * .78); ink(c, 9); c.stroke()
    c.move_to(x, y); c.line_to(x + math.cos(a2) * r * .5, y + math.sin(a2) * r * .5); c.set_source_rgba(*hx(RED)); c.set_line_width(14); c.stroke()

def tag(c, x, y, s, rot):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.move_to(-60, -300); c.line_to(0, -170); ink(c, 6); c.stroke()
    for dx, dy, col in ((14, 16, '1C1614'), (0, 0, YEL)):
        c.move_to(-170 + dx, -110 + dy); c.line_to(60 + dx, -170 + dy); c.line_to(170 + dx, -40 + dy); c.line_to(170 + dx, 150 + dy); c.line_to(-170 + dx, 150 + dy); c.close_path()
        c.set_source_rgba(*hx(col)); c.fill()
    c.move_to(-170, -110); c.line_to(60, -170); c.line_to(170, -40); c.line_to(170, 150); c.line_to(-170, 150); c.close_path(); ink(c, 8); c.stroke()
    c.arc(60, -120, 18, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 5); c.stroke(); c.restore()

def box_d(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-60 + 8, -50 + 10, 120, 100); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(-60, -50, 120, 100); c.set_source_rgba(*hx('C8A27A')); c.fill_preserve(); ink(c, 5); c.stroke()
    c.rectangle(-12, -50, 24, 100); c.set_source_rgba(*hx('E7D3B5')); c.fill(); c.restore()

def badge(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    for dx, dy, col in ((12, 14, '1C1614'), (0, 0, GREEN)):
        c.new_path()
        for k in range(12):
            a = k * math.pi / 6; r = 190 if k % 2 == 0 else 170
            c.line_to(dx + math.cos(a) * r, dy + math.sin(a) * r)
        c.close_path(); c.set_source_rgba(*hx(col)); c.fill()
    c.arc(0, 0, 140, 0, 2 * math.pi); ink(c, 7); c.stroke(); c.restore()

# ---------------------------------------------------------- scenes
def s_hook(fr, T):
    fr[:] = paper('FF8C1A', .72); rays(fr, T, 'FFFFFF', .12, cy=1060)
    ts = 2.3
    overlay(fr, cairo_layer(lambda c: (timeclock(c, 300, 1050, .95, clamp((T - ts) / .3)), conveyor(c, 1320, T))))
    x = lerp(1250, 760, eout(T / 1.6))
    sk(fr, ROB, x, 1000, T, 0, .78, -2 + 4 * math.sin(T * 6))
    if T > ts: burst(fr, 'CLOCKED IN!', 330, 760, T - ts, r=150, col=RED, size=40, rot=-8)
    tape(fr, 'ROBOTS ARE', CX, 470, 1.0, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    title(fr, 'CLOCKING IN', 600, 1.0, size=130, fill=YEL, rot=-3)

def s_question(fr, T):
    lt = T - S[1]; fr[:] = paper(BLUE, .68); rays(fr, T, 'FFFFFF', .1)
    overlay(fr, cairo_layer(lambda c: conveyor(c, 1330, T)))
    sk(fr, WRK, 320, 1060, T, 1, .55, -3, lt)
    sk(fr, ROB, 790, 1000, T, 2, .7, 3, lt - .3)
    burst(fr, 'VS', CX, 960, lt - .6, r=90, col=YEL, size=60)
    tape(fr, 'WHAT IF A ROBOT', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    title(fr, 'WORKED NEXT TO YOU?', 590, lt - .15, size=88, fill=YEL)

def s_thousand(fr, T):
    lt = T - S[2]; fr[:] = paper(None); rays(fr, T, YEL, .16)
    if T < S[3]:
        n = int(1000 * eout(lt / 2.2)); stat(fr, f'#{n:,}', 'HUMANOID BUILT', CX, 520, lt, RED, -3, 140)
        if ROBS is not None:
            for k in range(7):
                put_rgba(fr, ROBS, 150 + k * 130, 1100 + 15 * math.sin(T * 5 + k), clamp((lt - k * .2) / .3) * (1.0 if k == 3 else .8), 1.0, 0)
    else:
        l3 = T - S[3]; ph = photo('factory', 860, 560)
        if ph is not None: put_rgba(fr, ph, CX, 1010, back(clamp(l3 / .35)), 1.0, -2)
        sk(fr, ROB, 830, 1100, T, 3, .55, 4, l3 - .3)
        tape(fr, 'ALREADY AT WORK', CX, 470, l3, col=RED, size=56, font=LUCKY, rot=-2, tcol='FFFFFF')
        chip(fr, 'MOVING CAR PARTS', CX, 600, l3 - .3, YEL, 46, -2)

def s_boxes(fr, T):
    lt = T - S[4]; fr[:] = paper(GREEN, .55); rays(fr, T, 'FFFFFF', .12)
    th = wfind(4, 'hundred thousand')
    def dr(c):
        conveyor(c, 1330, T, speed=260)
        n = int(clamp((T - S[4]) / 4.0) * 14)
        for k in range(n):
            col, row = k % 5, k // 5; box_d(c, 200 + col * 120 + (row % 2) * 60, 1250 - row * 95, .9)
    overlay(fr, cairo_layer(dr))
    sk(fr, DIG, 820, 1000, T, 4, .62, -3, lt)
    tape(fr, 'IN A REAL WAREHOUSE', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    if T > th: stat(fr, '100,000+', 'BOXES MOVED', CX, 620, T - th, RED, -3, 120)

def s_china(fr, T):
    lt = T - S[5]; fr[:] = paper(RED, .74); rays(fr, T, 'FFFFFF', .1)
    t9 = wfind(5, 'nine'); t5 = wfind(6, 'five')
    base = 1260
    def dr(c):
        ink(c, 8); c.move_to(200, base); c.line_to(880, base); c.stroke()
        for j, (v, tg, col) in enumerate(((900, t9, 'FFFFFF'), (5000, t5, YEL))):
            p = eout((T - tg + .1) / .7); h = 560 * v / 5000 * p; x = 370 + j * 340
            c.rectangle(x - 100 + 12, base - h + 14, 200, h); c.set_source_rgba(*hx('1C1614')); c.fill()
            c.rectangle(x - 100, base - h, 200, h); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    overlay(fr, cairo_layer(dr))
    for j, (v, lab, tg) in enumerate((('900', 'IN 6 MONTHS', t9), ('5,000', 'THIS YEAR (GOAL)', t5))):
        p = eout((T - tg + .1) / .7); h = 560 * (900 if j == 0 else 5000) / 5000 * p; x = 370 + j * 340
        if T > tg - .1:
            title(fr, v, base - h - 60, T - tg + .1, size=84, fill='FFFFFF' if j else YEL, rot=0, cx=x)
            tape(fr, lab, x, base + 60, T - tg + .1, col=YEL, size=32, font=ELITE, rot=-2)
    tape(fr, 'ONE COMPANY IN CHINA', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)

def s_million(fr, T):
    lt = T - S[7]; fr[:] = paper('2A2F5A', .82); rays(fr, T, CYAN, .12)
    if ROBS is not None:
        for row in range(3):
            for k in range(9):
                x = (k * 130 + lt * 140 + row * 65) % 1300 - 110
                put_rgba(fr, ROBS, x, 860 + row * 200, .62 - row * .06, 1.0, 0)
    tape(fr, 'A FACTORY LINE FOR', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    tm = wfind(7, 'million')
    if T > tm: stat(fr, '1,000,000', 'ROBOTS A YEAR', CX, 600, T - tm, YEL, -3, 120)

def s_why(fr, T):
    lt = T - S[8]; fr[:] = paper(RED, .8); rays(fr, T, 'FFFFFF', .14)
    title(fr, 'SO WHY', 860, lt, size=180, fill='FFFFFF'); title(fr, 'NOW?', 1060, lt - .12, size=200, fill=YEL)

def s_tired(fr, T):
    lt = T - S[9]; fr[:] = paper(CYAN, .55); rays(fr, T, 'FFFFFF', .12)
    sp = 1.0 + 6 * clamp((T - S[11]) / .5)
    overlay(fr, cairo_layer(lambda c: clock24(c, 760, 1050, 210, T, sp)))
    sk(fr, ROB, 320, 1040, T, 5, .62, -3)
    tape(fr, "ROBOTS DON'T GET TIRED", CX, 470, lt, col='FFFFFF', size=52, font=LUCKY, rot=-2)
    chip(fr, 'NO BREAKS', 760, 760, T - wfind(10, 'breaks'), YEL, 44, -3)
    chip(fr, 'NO SICK DAYS', 760, 1330, T - wfind(10, 'sick'), 'FFFFFF', 44, 2)
    if T > S[11]: stat(fr, '3 SHIFTS', 'EVERY SINGLE DAY', CX, 600, T - S[11], RED, -3, 110)

def s_price(fr, T):
    lt = T - S[12]; fr[:] = paper(YEL, .55); rays(fr, T, 'FFFFFF', .14)
    sk(fr, ROB, 340, 1030, T, 6, .7, -3, lt)
    tp = wfind(12, 'thirty')
    overlay(fr, cairo_layer(lambda c: tag(c, 770, 1020, back(clamp((T - tp + .2) / .4)), .12 * math.sin(T * 3))))
    if T > tp: put_rgba(fr, ttext('$30K', 110, LUCKY, '1C1614', 'FFFFFF', shadow=False), 770, 1050, back(clamp((T - tp) / .3)), 1.0, 7 * math.sin(T * 3))
    tape(fr, 'PRICE TAG?', CX, 470, lt, col=RED, size=60, font=LUCKY, rot=-2, tcol='FFFFFF')
    chip(fr, "TESLA BOSS'S ESTIMATE", CX, 580, lt - .3, 'FFFFFF', 38, 2)

def s_next(fr, T):
    lt = T - S[13]; fr[:] = paper(RED, .8); rays(fr, T, 'FFFFFF', .14)
    title(fr, 'SO WHAT', 860, lt, size=170, fill='FFFFFF'); title(fr, 'HAPPENS NEXT?', 1060, lt - .15, size=130, fill=YEL)

def s_jobs(fr, T):
    lt = T - S[14]; fr[:] = paper(PINK, .55); rays(fr, T, 'FFFFFF', .1)
    sk(fr, WRK, CX, 1090, T, 7, .5, 0, lt)
    tape(fr, 'BORING JOBS GO FIRST', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    for k, (w, x, y) in enumerate((('lifting', 290, 700), ('sorting', 790, 780), ('carrying', 790, 1250))):
        tw = wfind(14, w); tape(fr, w.upper(), x, y, T - tw, col=YEL, size=46, font=LUCKY, rot=(-1) ** k * 4); xstamp(fr, x, y, T - tw - .35, .32)

def s_mech(fr, T):
    lt = T - S[15]; fr[:] = paper(GREEN, .55); rays(fr, T, 'FFFFFF', .14)
    ph = photo('tech', 760, 600, (.5, .4))
    if ph is not None: put_rgba(fr, ph, CX, 1020, back(clamp(lt / .35)), 1.0, -2)
    for k, w in enumerate(('fix', 'train', 'run')):
        chip(fr, w.upper() + ' THEM', 230 + k * 310, 640, T - wfind(15, w), (YEL, 'FFFFFF', CYAN)[k], 38, (-2, 2, -2)[k])
    tape(fr, 'SOMEONE HAS TO', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    if T > S[16]:
        l6 = T - S[16]; overlay(fr, cairo_layer(lambda c: badge(c, 810, 1240, back(clamp(l6 / .35)))))
        put_rgba(fr, ttext('NEXT BIG', 44, LUCKY, 'FFFFFF', shadow=False), 810, 1210, back(clamp(l6 / .35)), 1.0, -6)
        put_rgba(fr, ttext('JOB?', 60, LUCKY, YEL, shadow=False), 810, 1270, back(clamp(l6 / .35)), 1.0, -6)

def s_end(fr, T):
    lt = T - S[17]; fr[:] = paper(BLUE, .7); rays(fr, T, 'FFFFFF', .1)
    overlay(fr, cairo_layer(lambda c: conveyor(c, 1330, T)))
    sk(fr, WRK, 320, 1060, T, 8, .55, -3); sk(fr, ROB, 790, 1010, T, 9, .64, 3)
    tape(fr, 'WOULD YOU WORK', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    title(fr, 'NEXT TO A ROBOT?', 590, lt - .15, size=96, fill=YEL)
    if T > S[18]:
        burst(fr, 'YES', 230, 800, T - S[18], r=100, col=GREEN, size=56, rot=-8)
        burst(fr, 'NO', 860, 800, T - S[18] - .15, r=100, col=RED, size=56, rot=8)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_question), (S[4], s_thousand), (S[5], s_boxes), (S[7], s_china), (S[8], s_million), (S[9], s_why),
           (S[12], s_tired), (S[13], s_price), (S[14], s_next), (S[15], s_jobs), (S[17], s_mech), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (2.3, wfind(4, 'hundred thousand'), wfind(7, 'million'), S[11], wfind(12, 'thirty')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Photos: Wikimedia Commons (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
