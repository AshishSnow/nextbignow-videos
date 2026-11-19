import sys, os, json, math
sys.path.insert(0, '/home/claude/freeze')
from kit import *
D = '/home/claude/freeze'
L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]
END = E[-1] + 0.3; TOTAL = END + 2.6
def wt(i, frac): return S[i] + L[i]['dur'] * frac
def wfind(i, word):
    tx = L[i]['text'].lower(); k = tx.find(word.lower()); return wt(i, k / max(1, len(tx)))
def st(name, **kw):
    p = f'{D}/st/{name}.png'
    return load_st(name, **kw) if os.path.exists(p) else None
PHOTO = {}
def photo(name, w, h, focus=(.5, .5)):
    k = (name, w, h, focus)
    if k not in PHOTO:
        p = f'{D}/ph/{name}.jpg'
        PHOTO[k] = panel_img(comic_photo(p, w, h, focus)) if os.path.exists(p) else None
    return PHOTO[k]
exec(open(D + '/common_part.py').read())
ICE = st('icecream', w=420); MEAT = st('meat', w=420); MILK = st('milk', h=420); LAP = st('laptop', w=560)
FIRE = None; PILLS = st('pills', w=380); TRUCK = None; THERMO = None

def milk_d(c, x, y, s, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.move_to(-90 + 12, -120 + 14); c.line_to(90 + 12, -120 + 14); c.line_to(90 + 12, 200 + 14); c.line_to(-90 + 12, 200 + 14); c.close_path(); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.move_to(-90, -120); c.line_to(0, -200); c.line_to(90, -120); c.line_to(90, 200); c.line_to(-90, 200); c.close_path(); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
    c.rectangle(-90, -40, 180, 110); c.set_source_rgba(*hx(BLUE)); c.fill_preserve(); ink(c, 6); c.stroke(); c.restore()

def steak_d(c, x, y, s, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.save(); c.translate(12, 14); c.scale(1.4, 1); c.arc(0, 0, 110, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.save(); c.scale(1.4, 1); c.arc(0, 0, 110, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('C8394B')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.save(); c.scale(1.4, 1); c.arc(-20, -10, 70, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('F2A7B0')); c.set_line_width(14); c.stroke()
    c.arc(60, 20, 26, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 6); c.stroke(); c.restore()

def truck_d(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    for dx, dy in ((12, 14), (0, 0)):
        c.rectangle(-300 + dx, -150 + dy, 400, 240); c.rectangle(110 + dx, -80 + dy, 170, 170)
        c.set_source_rgba(*hx('1C1614')) if dx else c.set_source_rgba(1, 1, 1, 1); c.fill()
    c.rectangle(-300, -150, 400, 240); ink(c, 8); c.stroke(); c.rectangle(110, -80, 170, 170); c.set_source_rgba(*hx(CYAN)); c.fill_preserve(); ink(c, 8); c.stroke()
    c.rectangle(180, -60, 80, 60); c.set_source_rgba(*hx('DFF4FF')); c.fill_preserve(); ink(c, 6); c.stroke()
    for wx in (-200, 0, 200):
        c.arc(wx, 110, 46, 0, 2 * math.pi); c.set_source_rgba(*hx('2A2F3A')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.restore()

def chip(fr, txt, cx, cy, t, col=CYAN, size=40, rot=0):
    tape(fr, txt, cx, cy, t, col=col, size=size, font=INTER, rot=rot)

def sk(fr, im, x, y, T, k, sc, rot=0, t=1.0):
    if im is not None: sticker(fr, im, x, y, T, k, sc, rot, t)

def freezer(c, x, y, s, heat=0.0, T=0.0):
    """drawn chest-freezer / upright cabinet, glows red with heat."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-210 + 14, -330 + 16, 420, 660); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(-210, -330, 420, 660); c.set_source_rgba(*hx('E9EEF3')); c.fill_preserve(); ink(c, 9); c.stroke()
    for k in range(2):
        y0 = -300 + k * 310; c.rectangle(-180, y0, 360, 280)
        col = (lerp(.62, 1.0, heat), lerp(.86, .35, heat), lerp(1.0, .2, heat), 1)
        c.set_source_rgba(*col); c.fill_preserve(); ink(c, 6); c.stroke()
        for j in range(3):
            c.rectangle(-150 + j * 105, y0 + 40, 80, 100 + 20 * (j % 2)); c.set_source_rgba(1, 1, 1, .55 * (1 - heat * .5)); c.fill()
        c.move_to(150, y0 + 60); c.line_to(150, y0 + 220); ink(c, 10); c.stroke()
    if heat > .3:
        for k in range(4):
            ph = (T * .7 + k / 4) % 1
            c.move_to(-120 + k * 80, -350 - ph * 160); c.curve_to(-150 + k * 80, -400 - ph * 160, -90 + k * 80, -430 - ph * 160, -120 + k * 80, -480 - ph * 160)
            c.set_source_rgba(1, .55, .2, (heat - .3) * (1 - ph)); c.set_line_width(12); c.stroke()
    c.restore()

def thermo(c, x, y, s, val):
    """drawn thermometer -30..60 C, val in C."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-46 + 12, -420 + 14, 92, 700); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(-46, -420, 92, 700); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 9); c.stroke()
    c.arc(0, 320, 90, 0, 2 * math.pi); c.set_source_rgba(*hx(RED if val > 0 else BLUE)); c.fill_preserve(); ink(c, 9); c.stroke()
    frac = clamp((val + 30) / 90); top = 280 - frac * 680
    c.rectangle(-24, top, 48, 300 - top); c.set_source_rgba(*hx(RED if val > 0 else BLUE)); c.fill()
    for k in range(10):
        yy = 280 - k * 68; c.move_to(46, yy); c.line_to(80, yy); ink(c, 6); c.stroke()
    c.restore()

def bin_(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-190 + 12, -150 + 14); c.line_to(190 + 12, -150 + 14); c.line_to(150 + 12, 250 + 14); c.line_to(-150 + 12, 250 + 14); c.close_path(); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.move_to(-190, -150); c.line_to(190, -150); c.line_to(150, 250); c.line_to(-150, 250); c.close_path(); c.set_source_rgba(*hx('6C7A89')); c.fill_preserve(); ink(c, 9); c.stroke()
    for k in range(4): c.move_to(-100 + k * 66, -100); c.line_to(-80 + k * 54, 210); ink(c, 6, .6); c.stroke()
    c.rectangle(-210, -190, 420, 46); c.set_source_rgba(*hx('8A97A6')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.restore()

def dial(c, x, y, r, ang):
    c.save(); c.translate(x, y)
    c.arc(12, 14, r, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    for k in range(24):
        a = math.pi * .75 + k / 23 * math.pi * 1.5; t = k / 23
        c.arc(0, 0, r, a, a + math.pi * 1.5 / 23); c.line_to(0, 0); c.close_path(); c.set_source_rgba(lerp(.25, 1, t), lerp(.6, .25, t), lerp(1, .2, t), 1); c.fill()
    c.arc(0, 0, r * .62, 0, 2 * math.pi); c.set_source_rgba(*hx('2A2F3A')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.arc(0, 0, r, 0, 2 * math.pi); ink(c, 9); c.stroke()
    a = math.pi * .75 + ang * math.pi * 1.5; c.move_to(0, 0); c.line_to(math.cos(a) * r * .9, math.sin(a) * r * .9); c.set_source_rgba(1, 1, 1, 1); c.set_line_width(16); c.stroke()
    c.restore()

def lock(c, x, y, s, open_=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.translate(0, -120 - 70 * open_); c.rotate(-.5 * open_)
    c.arc(0, 0, 90, math.pi, 0); c.line_to(90, 60); c.move_to(-90, 0); c.line_to(-90, 60); ink(c, 34); c.stroke(); c.restore()
    c.rectangle(-150 + 12, -100 + 14, 300, 240); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(-150, -100, 300, 240); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 9); c.stroke()
    c.arc(0, 0, 26, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill(); c.rectangle(-10, 0, 20, 70); c.fill()
    c.restore()

def map_pins(fr, T, t0, n, cx=CX, cy=980, w=820, h=640, col=RED, seed=1, dur=1.6):
    rng = np.random.default_rng(seed); pts = rng.uniform(-1, 1, (n, 2)); ts = np.sort(rng.uniform(0, dur, n))
    def dr(c):
        for (px, py), tt in zip(pts, ts):
            p = back(clamp((T - t0 - tt) / .25))
            if p <= 0: continue
            x, y = cx + px * w / 2, cy + py * h / 2
            c.save(); c.translate(x, y); c.scale(p, p)
            c.arc(3, 4, 13, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
            c.arc(0, 0, 13, 0, 2 * math.pi); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 4); c.stroke(); c.restore()
    overlay(fr, cairo_layer(dr))

def stat(fr, big, small, cx, cy, t, col=RED, rot=-3):
    if t <= 0: return
    title(fr, big, cy, t, size=130, fill='FFFFFF' if col == RED else YEL, rot=rot, cx=cx)
    tape(fr, small, cx, cy + 105, t - .1, col=col, size=40, font=LUCKY, rot=rot + 1, tcol='FFFFFF' if col == RED else '1C1614')

# ------------------------------------------------------------- scenes
def s_hook(fr, T):
    heat = clamp(.55 + .45 * math.sin(T * 2))
    fr[:] = paper('FF8C1A', .7); rays(fr, T, 'FFFFFF', .12, cy=1050)
    ph = photo('aisle', 760, 600, (.5, .5))
    if ph is not None:
        warm = ph.copy(); warm[..., 0] = np.clip(warm[..., 0] * 1.15 + 25, 0, 255); warm[..., 2] = (warm[..., 2] * .75).astype(np.uint8)
        put_rgba(fr, warm, CX, 1010, 1.0 + .02 * T, 1.0, -2)
    overlay(fr, cairo_layer(lambda c: thermo(c, 880, 1080, .55, lerp(20, 50, clamp(T / 2.4)))))
    sk(fr, ICE, 250, 1230, T, 0, .75, -10)
    tape(fr, 'HACKERS ARE COOKING', CX, 470, 1.0, col='FFFFFF', size=52, font=LUCKY, rot=-2)
    title(fr, 'SUPERMARKET FREEZERS', 600, 1.0, size=96, fill=YEL, rot=-3)

def s_question(fr, T):
    lt = T - S[1]; fr[:] = paper(BLUE, .7); rays(fr, T, 'FFFFFF', .1)
    def dr(c):
        freezer(c, 760, 1050, .9, 0.0, T)
        for k in range(4):
            ph = (lt * .9 + k / 4) % 1; c.arc(380, 980, 60 + ph * 260, -.5, .5); ink(c, 8, 1 - ph); c.stroke()
    overlay(fr, cairo_layer(dr))
    sk(fr, LAP, 300, 1080, T, 1, .8, 4, lt)
    tape(fr, 'WHAT IF SOMEONE HACKED', CX, 470, lt, col='FFFFFF', size=50, font=LUCKY, rot=-2)
    title(fr, "YOUR STORE'S FRIDGE?", 590, lt - .15, size=92, fill=YEL)

def s_temp(fr, T):
    lt = T - S[2]; t50 = S[3]
    hot = clamp((T - t50 + .2) / .6)
    fr[:] = paper(CYAN, .6) if hot < .5 else paper(RED, .78)
    rays(fr, T, 'FFFFFF', .12)
    val = -18 if T < t50 - .2 else lerp(-18, 50, eout(hot))
    def dr(c):
        thermo(c, CX + 220, 1040, .95, val); freezer(c, 330, 1060, .7, hot, T)
    overlay(fr, cairo_layer(dr))
    title(fr, f'{int(round(val))}°C', 560, 1.0, size=150, fill='FFFFFF' if hot < .5 else YEL, rot=-3)
    if hot < .5: tape(fr, 'NORMAL FREEZER', CX, 420, lt, col=BLUE, size=46, font=LUCKY, rot=-2, tcol='FFFFFF')
    else: tape(fr, 'HACKED FREEZER', CX, 420, T - t50, col=YEL, size=46, font=LUCKY, rot=-2)
    if T > S[4]: chip(fr, '= 122°F', CX + 220, 1340, T - S[4], 'FFFFFF', 48, -3)
    if T > t50 + .2: burst(fr, 'HOT!', 330, 1330, T - t50 - .2, r=110, col=YEL, size=60)

def s_nobreak(fr, T):
    lt = T - S[5]; fr[:] = paper(None); rays(fr, T, YEL, .16)
    a = wfind(5, 'broke'); b = wfind(5, 'cut')
    def dr(c):
        c.save(); c.translate(300, 1000)
        c.rectangle(-150 + 12, -250 + 14, 300, 500); c.set_source_rgba(*hx('1C1614')); c.fill()
        c.rectangle(-150, -250, 300, 500); c.set_source_rgba(*hx('9FD8FF')); c.fill_preserve(); ink(c, 9); c.stroke()
        c.rectangle(-150, -250, 300, 70); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 7); c.stroke(); c.restore()
        c.save(); c.translate(780, 1000)
        c.rectangle(-130 + 12, -170 + 14, 260, 340); c.set_source_rgba(*hx('1C1614')); c.fill()
        c.rectangle(-130, -170, 260, 340); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 9); c.stroke()
        for sx in (-40, 40): c.rectangle(sx - 12, -70, 24, 70); c.set_source_rgba(*hx('1C1614')); c.fill()
        c.arc(0, 60, 28, 0, 2 * math.pi); c.fill(); c.restore()
    overlay(fr, cairo_layer(dr))
    tape(fr, 'DOORS LOCKED', 300, 1310, T - a, col='FFFFFF', size=40, font=LUCKY, rot=-3)
    tape(fr, 'POWER ON', 780, 1240, T - b, col=GREEN, size=40, font=LUCKY, rot=3, tcol='FFFFFF')
    tape(fr, 'NOBODY BROKE IN', CX, 470, T - a, col=RED, size=58, font=LUCKY, rot=-2, tcol='FFFFFF')

def s_dial(fr, T):
    lt = T - S[6]; th = S[7]; fr[:] = paper(PINK, .6)
    ang = .1 if T < th else lerp(.1, .98, eout((T - th) / .8))
    def dr(c): dial(c, 640, 1040, 230, ang)
    overlay(fr, cairo_layer(dr))
    sk(fr, LAP, 300, 1240, T, 2, .7, -4, lt)
    tape(fr, 'LOGGED IN ONLINE', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    if T > th:
        title(fr, 'HEAT: MAX', 590, T - th, size=110, fill=YEL)
        f = photo('fire', 300, 300)
        if f is not None and T > th + .3: put_rgba(fr, f, 840, 920, back(clamp((T - th - .3) / .3)), 1.0, 6)

def s_france(fr, T):
    lt = T - S[8]; fr[:] = paper(BLUE, .55); rays(fr, T, 'FFFFFF', .1)
    ph = photo('map', 860, 760, (.45, .55))
    if ph is not None: put_rgba(fr, ph, CX, 1040, 1.0, 1.0, -1)
    map_pins(fr, T, wfind(8, 'seven') - .2, 60, cx=420, cy=1150, w=150, h=130, seed=3, dur=1.6)
    tape(fr, 'FRANCE', CX, 440, lt, col=RED, size=56, font=LUCKY, rot=-2, tcol='FFFFFF')
    stat(fr, '~700', 'FOOD SITES IN ONE WEEKEND', CX, 560, T - wfind(8, 'seven'), YEL)

def s_trash(fr, T):
    lt = T - S[9]; fr[:] = paper(GREEN, .55); rays(fr, T, 'FFFFFF', .1)
    overlay(fr, cairo_layer(lambda c: bin_(c, CX, 1220, .95)))
    def items(c):
        for k, (fn, w0, x) in enumerate(((steak_d, 'meat', 300), (None, 'ice', 540), (milk_d, 'milk', 780))):
            tw = wfind(9, w0); p = eout((T - tw) / .8)
            if fn and T > tw: fn(c, lerp(x, CX + (k - 1) * 60, p), lerp(700, 1100, p), .8 - .3 * p, (k - 1) * .5 * p)
    overlay(fr, cairo_layer(items))
    tw = wfind(9, 'ice'); p = eout((T - tw) / .8)
    if ICE is not None and T > tw: put_rgba(fr, ICE, lerp(540, CX, p), lerp(700, 1080, p), .55 - .2 * p, 1.0, 20 * p)
    overlay(fr, cairo_layer(lambda c: c.save() or (c.rectangle(CX - 190, 1070, 380, 60), c.set_source_rgba(*hx('8A97A6')), c.fill_preserve(), ink(c, 8), c.stroke(), c.restore())))
    tape(fr, 'ALL THROWN AWAY', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    tf = wfind(9, 'fifteen')
    if T > tf:
        f = photo('fire', 320, 320)
        if f is not None: put_rgba(fr, f, 820, 760, back(clamp((T - tf) / .3)), 1.0, 6)
        burst(fr, '15+ FIRES', 300, 760, T - tf - .2, r=150, col=RED, size=46)

def s_again(fr, T):
    lt = T - S[10]; fr[:] = paper('2A2F5A', .85)
    ph = photo('map', 860, 760, (.5, .45))
    if ph is not None and T > S[11]: put_rgba(fr, ph, CX, 1040, 1.0, 1.0, 1)
    if T < S[11]:
        def dr(c):
            c.arc(CX, 1000, 160, 0, 2 * math.pi); c.set_source_rgba(*hx('FFF1B8')); c.fill()
            c.arc(CX + 70, 960, 150, 0, 2 * math.pi); c.set_source_rgba(*hx('2A2F5A')); c.fill()
        overlay(fr, cairo_layer(dr))
        tape(fr, 'THREE WEEKS LATER...', CX, 560, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    else:
        map_pins(fr, T, S[11] + .2, 110, cx=CX - 40, cy=1000, w=480, h=380, seed=7, dur=2.6)
        stat(fr, '9', 'COUNTRIES', 230, 520, T - wfind(11, 'nine'), YEL, -4)
        stat(fr, '100+', 'STORES', CX + 40, 520, T - wfind(11, 'hundred'), RED, 2)
        tw = wfind(11, 'overnight')
        if T > tw: burst(fr, 'OVERNIGHT', 860, 560, T - tw, r=150, col=YEL, size=42)

def s_quote(fr, T):
    lt = T - S[12]; fr[:] = paper(None, .5); rays(fr, T, RED, .1)
    ph = photo('aisle', 760, 560, (.5, .6))
    if ph is not None:
        dark = ph.copy(); dark[..., :3] = (ph[..., :3].astype(np.float32) * np.array([1.0, .7, .6])).astype(np.uint8); put_rgba(fr, dark, CX, 1080, 1.0, 1.0, 2)
    def dr(c):
        p = back(clamp((lt - .5) / .3)); c.save(); c.translate(CX, 720); c.scale(p, p)
        c.move_to(-400 + 12, -110 + 14); c.line_to(400 + 12, -110 + 14); c.line_to(400 + 12, 110 + 14); c.line_to(-80 + 12, 110 + 14); c.line_to(-160 + 12, 200 + 14); c.line_to(-150 + 12, 110 + 14); c.line_to(-400 + 12, 110 + 14); c.close_path(); c.set_source_rgba(*hx('1C1614')); c.fill()
        c.move_to(-400, -110); c.line_to(400, -110); c.line_to(400, 110); c.line_to(-80, 110); c.line_to(-160, 200); c.line_to(-150, 110); c.line_to(-400, 110); c.close_path(); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 9); c.stroke(); c.restore()
    overlay(fr, cairo_layer(dr))
    if lt > .6: put_rgba(fr, ttext('"EVERYTHING IS', 64, LUCKY, RED, shadow=False), CX, 680, back(clamp((lt - .6) / .3)), 1.0, -2)
    if lt > .9: put_rgba(fr, ttext('DESTROYED."', 76, LUCKY, '1C1614', 'FFFFFF', shadow=False), CX, 765, back(clamp((lt - .9) / .3)), 1.0, -2)
    tape(fr, 'A STORE MANAGER', CX, 470, lt, col=YEL, size=50, font=ELITE, rot=-2)

def s_next(fr, T):
    lt = T - S[13]; fr[:] = paper(RED, .8); rays(fr, T, 'FFFFFF', .14)
    title(fr, 'SO WHAT', 860, lt, size=170, fill='FFFFFF')
    title(fr, 'HAPPENS NEXT?', 1060, lt - .15, size=130, fill=YEL)

def s_open(fr, T):
    lt = T - S[14]; fr[:] = paper(YEL, .55); rays(fr, T, 'FFFFFF', .12)
    to = wfind(14, 'wide open')
    def dr(c): lock(c, CX, 1060, 1.3, eout((T - to) / .5))
    overlay(fr, cairo_layer(dr))
    tape(fr, "GERMANY'S CYBER AGENCY:", CX, 470, lt, col='FFFFFF', size=50, font=LUCKY, rot=-2)
    if T > to - .3: title(fr, 'STILL WIDE OPEN', 600, T - to + .3, size=100, fill=RED)

def s_where(fr, T):
    lt = T - S[15]; fr[:] = paper(CYAN, .55); rays(fr, T, 'FFFFFF', .12)
    tw = wfind(15, 'warehouses'); tm = wfind(15, 'medicine'); td = wfind(15, 'delivery')
    a = photo('warehouse', 520, 400)
    if a is not None and T > tw - .1: put_rgba(fr, a, 330, 830, back(clamp((T - tw + .1) / .3)), 1.0, -4)
    tape(fr, 'WAREHOUSES', 330, 1060, T - tw, col='FFFFFF', size=40, font=LUCKY, rot=-3)
    sk(fr, PILLS, 800, 860, T, 5, .9, 8, T - tm + .1)
    tape(fr, 'MEDICINE', 800, 1060, T - tm, col=GREEN, size=40, font=LUCKY, rot=3, tcol='FFFFFF')
    if T > td - .1: overlay(fr, cairo_layer(lambda c: truck_d(c, CX - 30, 1230, .75 * back(clamp((T - td + .1) / .3)))))
    tape(fr, "IT'S NOT JUST SUPERMARKETS", CX, 470, lt, col=RED, size=48, font=LUCKY, rot=-2, tcol='FFFFFF')

def s_melt(fr, T):
    lt = T - S[16]; fr[:] = paper(PINK, .55); rays(fr, T, 'FFFFFF', .1)
    tm = S[17]
    def dr(c):
        p = eout(clamp(lt / .4)); c.save(); c.translate(CX, 800); c.scale(p, p)
        c.rectangle(-340 + 12, -60 + 14, 680, 120); c.set_source_rgba(*hx('1C1614')); c.fill()
        c.rectangle(-340, -60, 680, 120); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke(); c.restore()
    overlay(fr, cairo_layer(dr))
    if lt > .3: put_rgba(fr, ttext('PASSWORD: ••••••••', 52, INTER, '1C1614', 'FFFFFF', sw=0, shadow=False), CX, 800, 1.0, 1.0, 0)
    if T > tm:
        xstamp(fr, CX, 800, T - tm, .9)
        if ICE is not None:
            m = clamp((T - tm - .2) / 1.4); im = ICE.copy(); h = im.shape[0]
            put_rgba(fr, im, CX, 1120 + 30 * m, .8, 1.0, -6 - 20 * m)
            def drip(c):
                for k in range(6):
                    x = CX - 150 + k * 60; c.move_to(x, 1180); c.line_to(x, 1180 + (80 + 60 * (k % 3)) * m)
                    c.set_source_rgba(*hx('FFD1DC')); c.set_line_width(28); c.stroke()
        title(fr, 'MELTS YOUR GROCERIES', 560, T - tm, size=86, fill=YEL)
    else:
        tape(fr, 'THE NEXT BIG HACK', CX, 560, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)

def s_end(fr, T):
    lt = T - S[18]; fr[:] = paper(BLUE, .7); rays(fr, T, 'FFFFFF', .1)
    ph = photo('aisle', 700, 540, (.5, .5))
    if ph is not None: put_rgba(fr, ph, CX, 1050, 1.0, 1.0, -2)
    tape(fr, 'WOULD YOU STILL TRUST', CX, 470, lt, col='FFFFFF', size=52, font=LUCKY, rot=-2)
    title(fr, 'THE FROZEN AISLE?', 590, lt - .15, size=100, fill=YEL)
    if T > S[19]:
        burst(fr, 'YES', 280, 1260, T - S[19], r=110, col=GREEN, size=60, rot=-8)
        burst(fr, 'NO', 800, 1260, T - S[19] - .15, r=110, col=RED, size=60, rot=8)

def credit_on(fr, T):
    if T < END: credit(fr, 'Photos: Wikimedia Commons (credits in description)')

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_question), (S[5], s_temp), (S[6], s_nobreak), (S[8], s_dial), (S[9], s_france), (S[10], s_trash),
           (S[12], s_again), (S[13], s_quote), (S[14], s_next), (S[15], s_open), (S[16], s_where), (S[18], s_melt), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (S[3] + .2, S[7] + .3, wfind(9, 'fifteen'), S[11] + .2, S[17]):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    credit_on(fr, T); subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
