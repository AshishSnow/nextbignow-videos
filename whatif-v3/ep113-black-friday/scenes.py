import sys, os, json, math
sys.path.insert(0, '/home/claude/bf'); sys.path.insert(0, '/home/claude/samples')
from kit import *
import world as Wd
from world import surface, to_np, grad, stars, glow, earth_np, satellite, flash, aurora, palm, roof_people2, human, street, post
import essay as ES
D = '/home/claude/bf'
L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]
END = E[-1] + 0.3; TOTAL = END + 2.6
def wt(i, frac): return S[i] + L[i]['dur'] * frac
def wfind(i, word):
    tx = L[i]['text'].lower(); k = tx.find(word.lower()); assert k >= 0, (i, word); return wt(i, k / max(1, len(tx)))
exec(open(D + '/common_part.py').read())
def chip(fr, txt, cx, cy, t, col=CYAN, size=40, rot=0): tape(fr, txt, cx, cy, t, col=col, size=size, font=INTER, rot=rot)
def pop(T, t0, d=.35): return back(clamp((T - t0) / d))
def stamp(fr, txt, cx, cy, t, rot=-12, size=70, col=RED):
    if t <= 0: return
    s = 1.8 - .8 * eout(clamp(t / .18)); tape(fr, txt, cx, cy, 1.0, col=col, size=int(size * s), font=LUCKY, rot=rot, tcol='FFFFFF')
def quiet(T, t0, a, b, col='main', size=100):
    fr = ES.base(True); ES.headline(fr, [(a, 'grey'), (b, col)], T, [t0, t0 + .35], y=400, dark=True, size=size); return fr
ICE = '9FE7FF'; PINK = 'FF8AC8'

# ---------- world layers (float images, lit) ----------
def space_bg(T, n=260):
    s, c = surface(); Wd.grad(c, [(0, '02030C'), (1, '07102A')]); stars(c, T, n); return to_np(s)
def add_layer(img, fn):
    s, c = surface(); fn(c); img += to_np(s); return img
def bf_ring(c, T, cx, cy, rx, ry, n, dead=(), s=.7, spd=.05, tilt=0.0):
    for k in range(n):
        a = k * 6.283 / n + T * spd
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        if math.sin(a) < -.2 and abs(x - cx) < rx * .55: continue      # behind the planet
        satellite(c, x, y, s, T, dead=1.0 if k in dead else 0.0, rot=a)
def swarm(c, T, cx, cy, r, n, a=1.0, seed=2):
    rs = np.random.RandomState(seed)
    for k in range(n):
        inc = rs.uniform(-1.2, 1.2); ph = rs.uniform(0, 6.28) + T * rs.uniform(.15, .3); rr = r * rs.uniform(1.06, 1.3)
        x = cx + rr * math.cos(ph); y = cy + rr * math.sin(ph) * math.sin(inc) * .9
        if math.sin(ph) * math.cos(inc) < 0 and (x - cx) ** 2 + (y - cy) ** 2 < r * r: continue
        c.arc(x, y, 2.2, 0, 6.29); c.set_source_rgba(.75, .95, 1, a); c.fill()
def city(c, T, y=1560, lit=1.0, seed=4, col=(.02, .02, .05)):
    rs = np.random.RandomState(seed); x = -20
    while x < W:
        w = rs.uniform(70, 150); h = rs.uniform(180, 620)
        c.set_source_rgba(*col, 1); c.rectangle(x, y - h, w, h + 400); c.fill()
        for wy in np.arange(y - h + 24, y - 10, 34):
            for wx in np.arange(x + 12, x + w - 16, 26):
                if rs.rand() < .45 * lit: c.rectangle(wx, wy, 12, 18); c.set_source_rgba(1, .8, .45, .85); c.fill()
        x += w + rs.uniform(4, 18)
def bf_sat(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(.15 * math.sin(T * .6))
    for d in (-1, 1):
        c.rectangle(d * 70 + (0 if d > 0 else -220), -45, 220, 90); c.set_source_rgba(*hx('1E2A44')); c.fill_preserve(); c.set_source_rgba(.5, .6, .8, 1); c.set_line_width(4); c.stroke()
        for k in range(1, 4): c.move_to(d * 70 + (0 if d > 0 else -220) + k * 55, -45); c.rel_line_to(0, 90); c.stroke()
    c.rectangle(-70, -110, 140, 220); c.set_source_rgba(*hx('2B2B30')); c.fill_preserve(); c.set_source_rgba(.6, .6, .65, 1); c.stroke()
    c.arc(0, 0, 48, 0, 6.29); c.set_source_rgba(*hx('FFD21F')); c.fill()
    for k in range(3):
        a0 = -1.57 + k * 2.094 - .5; c.move_to(0, 0); c.arc(0, 0, 44, a0, a0 + 1.0); c.close_path(); c.set_source_rgba(.05, .05, .05, 1); c.fill()
    c.arc(0, 0, 12, 0, 6.29); c.set_source_rgba(*hx('FFD21F')); c.fill(); c.arc(0, 0, 8, 0, 6.29); c.set_source_rgba(.05, .05, .05, 1); c.fill()
    c.restore()
    glow(c, x, y + 120 * s, 60 * s, 'FF2A2A', .5 + .5 * math.sin(T * 6))
def calendar(c, x, y, s, T, flip):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-200, -230, 400, 460); c.set_source_rgba(.96, .95, .92, 1); c.fill()
    c.rectangle(-200, -230, 400, 110); c.set_source_rgba(*hx('E63946')); c.fill()
    c.select_font_face('Luckiest Guy'); c.set_font_size(76); c.set_source_rgba(1, 1, 1, 1)
    m = 'DEC' if flip > .5 else 'NOV'; e = c.text_extents(m); c.move_to(-e.width / 2, -145); c.show_text(m)
    c.set_source_rgba(.1, .1, .1, 1)
    for r in range(4):
        for k in range(5): c.rectangle(-170 + k * 70, -90 + r * 75, 50, 50); c.fill()
    if flip > 0 and flip < 1:
        c.rectangle(-200, -230 + 460 * flip, 400, 460 * (1 - flip) * .3); c.set_source_rgba(.85, .84, .8, 1); c.fill()
    c.restore()
def house_alarm(c, x, y, s, T, on):
    c.save(); c.translate(x, y); c.scale(s, s); c.set_source_rgba(.02, .02, .05, 1)
    c.rectangle(-260, -240, 520, 240); c.fill(); c.move_to(-300, -240); c.line_to(0, -420); c.line_to(300, -240); c.close_path(); c.fill()
    for wx in (-170, 90): c.rectangle(wx, -180, 80, 80); c.set_source_rgba(1, .75, .4, .7); c.fill()
    c.restore()
    if on: glow(c, x + 200 * s, y - 300 * s, 260 * s, 'FF2020' if int(T * 6) % 2 else '2050FF', .8)
def phone_old(c, x, y, s, T, dead):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-220, 120); c.line_to(-160, -60); c.line_to(160, -60); c.line_to(220, 120); c.close_path(); c.set_source_rgba(*hx('B3122E')); c.fill()
    c.arc(0, 30, 70, 0, 6.29); c.set_source_rgba(.95, .9, .8, 1); c.fill()
    for k in range(10): a = k * .55 - 1.4; c.arc(46 * math.cos(a), 30 + 46 * math.sin(a), 10, 0, 6.29); c.set_source_rgba(.2, .05, .05, 1); c.fill()
    lift = 0 if dead else 20 * abs(math.sin(T * 10))
    c.save(); c.translate(0, -100 - lift); c.move_to(-240, 0); c.curve_to(-200, -60, 200, -60, 240, 0); c.line_to(200, 30); c.curve_to(100, 0, -100, 0, -200, 30); c.close_path()
    c.set_source_rgba(*hx('C8173A')); c.fill(); c.restore()
    c.restore()
def tv_old(c, x, y, s, T, static):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-260, -200, 520, 400); c.set_source_rgba(*hx('6B4A2E')); c.fill()
    c.rectangle(-220, -165, 380, 330); c.set_source_rgba(.75, .8, .8, 1) if not static else c.set_source_rgba(.4, .4, .45, 1); c.fill()
    if static:
        rs = np.random.RandomState(int(T * 24))
        for k in range(220): c.rectangle(-220 + rs.uniform(0, 370), -165 + rs.uniform(0, 320), rs.uniform(4, 20), 3); c.set_source_rgba(1, 1, 1, rs.uniform(.3, 1)); c.fill()
    else:
        c.select_font_face('Luckiest Guy'); c.set_font_size(90); c.set_source_rgba(.9, .1, .15, 1); e = c.text_extents('LIVE'); c.move_to(-30 - e.width / 2, 30); c.show_text('LIVE')
    for k in range(2): c.arc(200, -80 + k * 90, 22, 0, 6.29); c.set_source_rgba(.2, .15, .1, 1); c.fill()
    c.restore()
def telstar(c, x, y, s, T, dead):
    c.save(); c.translate(x, y); c.rotate(T * (2.5 if dead else .3)); c.scale(s, s)
    c.arc(0, 0, 90, 0, 6.29); c.set_source_rgba(*hx('C9A24A' if not dead else '6E6555')); c.fill()
    for k in range(12): a = k * .5236; c.move_to(0, 0); c.line_to(90 * math.cos(a), 90 * math.sin(a)); c.set_source_rgba(.1, .1, .2, .6); c.set_line_width(5); c.stroke()
    c.arc(0, 0, 90, 0, 6.29); c.set_source_rgba(.2, .3, .6, .35); c.fill()
    c.move_to(0, -90); c.line_to(0, -150); c.set_source_rgba(.85, .85, .85, 1); c.set_line_width(6); c.stroke()
    c.restore()
def mphone(c, x, y, s, T, on=1.0, map_=True):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-150, -300, 300, 600); c.set_source_rgba(.04, .04, .06, 1); c.fill()
    if on > 0:
        g = cairo.LinearGradient(0, -280, 0, 280); g.add_color_stop_rgb(0, .55, .8, .65); g.add_color_stop_rgb(1, .75, .88, .7)
        c.rectangle(-135, -280, 270, 560); c.set_source(g); c.paint_with_alpha(0) if False else c.fill()
        for k in range(6): c.move_to(-135, -240 + k * 95); c.line_to(135, -200 + k * 80); c.set_source_rgba(1, 1, 1, .8); c.set_line_width(10); c.stroke()
        c.arc(10, -20, 34, 3.14, 6.28); c.line_to(10, 40); c.close_path(); c.set_source_rgba(.9, .15, .2, 1); c.fill()
        c.rectangle(-135, -280, 270, 560); c.set_source_rgba(0, 0, 0, 1 - on); c.fill()
    c.restore()
    if on > 0: glow(c, x, y, 380 * s, 'BFFFE0', .25 * on)

def ui_title(fr, a, b, t, ca='FFFFFF', cb=YEL, ya=430, yb=570, sa=92, sb=160):
    title(fr, a, ya, t + .3, size=sa, fill=ca); title(fr, b, yb, t, size=sb, fill=cb)

# ---------- beats ----------



# ---------- Black Friday sale world: black + electric yellow + hot red ----------
YEL2 = 'FFE14A'; HOT = 'FF2D55'; GRN = '3DFF8A'
def sale_bg(c, T, spot=(CX, 900), col='FFE14A'):
    grad(c, [(0, '07060A'), (1, '120D14')])
    rs = np.random.RandomState(8)
    for k in range(26):
        x = rs.uniform(0, W); y = rs.uniform(0, H); r = rs.uniform(40, 140)
        glow(c, x + 20 * math.sin(T * .5 + k), y, r, (YEL2, HOT, 'FFFFFF')[k % 3], .08)
    glow(c, spot[0], spot[1], 760, col, .22)
def tagshape(c, x, y, s, T, price, sub='', col=YEL2, cross=None, swing=1.0, sale=False):
    c.save(); c.translate(x, y); c.rotate(.06 * swing * math.sin(T * 2.2)); c.scale(s, s)
    c.move_to(0, -330); c.line_to(0, -250); c.set_source_rgba(.85, .85, .85, 1); c.set_line_width(5); c.stroke()
    c.move_to(-230, -250); c.line_to(230, -250); c.line_to(230, 180); c.line_to(-230, 180); c.close_path()
    c.move_to(-60, -250); c.line_to(0, -320); c.line_to(60, -250); c.close_path()
    c.set_source_rgba(*hx(col)); c.fill()
    c.arc(0, -270, 14, 0, 6.29); c.set_source_rgba(.05, .05, .05, 1); c.fill()
    c.select_font_face('Luckiest Guy')
    if cross:
        c.set_font_size(60); e = c.text_extents(cross); c.move_to(-e.width / 2, -120); c.set_source_rgba(.2, .2, .2, .8); c.show_text(cross)
        c.move_to(-e.width / 2 - 10, -140); c.line_to(e.width / 2 + 10, -140); c.set_source_rgba(*hx(HOT)); c.set_line_width(9); c.stroke()
    c.set_font_size(120 if len(price) < 6 else 96); e = c.text_extents(price); c.move_to(-e.width / 2, 40); c.set_source_rgba(.05, .05, .05, 1); c.show_text(price)
    if sub: c.set_font_size(40); e = c.text_extents(sub); c.move_to(-e.width / 2, 130); c.show_text(sub)
    if sale:
        c.save(); c.translate(170, -220); c.rotate(.35); c.arc(0, 0, 95, 0, 6.29); c.set_source_rgba(*hx(HOT)); c.fill()
        c.set_font_size(54); c.set_source_rgba(1, 1, 1, 1); e = c.text_extents('SALE'); c.move_to(-e.width / 2, 18); c.show_text('SALE'); c.restore()
    c.restore()
def watch(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    for d in (-1, 1): c.rectangle(-70, d * 150 - (90 if d < 0 else 0), 140, 90 + 60); c.set_source_rgba(.15, .15, .18, 1); c.fill()
    c.rectangle(-130, -160, 260, 320); c.set_source_rgba(.1, .1, .12, 1); c.fill()
    c.rectangle(-112, -142, 224, 284); c.set_source_rgba(.02, .02, .03, 1); c.fill()
    for k, (r, col) in enumerate(((80, HOT), (60, GRN), (40, '4FC3FF'))):
        c.arc(0, -10, r, -1.57, -1.57 + 6.28 * (.6 + .3 * math.sin(T + k))); c.set_source_rgba(*hx(col)); c.set_line_width(14); c.stroke()
    c.rectangle(130, -40, 18, 60); c.set_source_rgba(.3, .3, .32, 1); c.fill()
    c.restore(); glow(c, x, y, 300 * s, '4FC3FF', .25)
def boots(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    for d, dx in ((0, -130), (1, 120)):
        c.save(); c.translate(dx, 0)
        c.move_to(-80, -260); c.line_to(60, -260); c.line_to(70, -40); c.curve_to(200, -30, 230, 40, 220, 80); c.line_to(-90, 80); c.close_path()
        c.set_source_rgba(*hx('B07A45')); c.fill()
        c.rectangle(-95, 60, 320, 30); c.set_source_rgba(.25, .15, .08, 1); c.fill()
        c.rectangle(-85, -270, 150, 40); c.set_source_rgba(.92, .85, .7, 1); c.fill()
        c.restore()
    c.restore()
def card_grid(c, T, t0, n_grey, n_red, cols=5, rows=5, y0=830):
    rs = np.random.RandomState(2); order = rs.permutation(cols * rows)
    for k in range(cols * rows):
        q, r = k % cols, k // cols; x = 120 + q * 190; y = y0 + r * 150
        idx = int(np.where(order == k)[0][0])
        col = (1, 1, 1) if idx >= n_grey else ((.45, .45, .5) if idx >= n_red else hx(HOT)[:3])
        p = pop(T, t0 + k * .02)
        c.rectangle(x - 75 * p, y - 55 * p, 150 * p, 110 * p); c.set_source_rgba(*col, .95); c.fill()
        c.rectangle(x - 60 * p, y - 40 * p, 50 * p, 50 * p); c.set_source_rgba(.1, .1, .12, .8); c.fill()
def magnifier(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.arc(0, 0, 150, 0, 6.29); c.set_source_rgba(.6, .85, 1, .18); c.fill_preserve(); c.set_source_rgba(1, 1, 1, 1); c.set_line_width(22); c.stroke()
    c.move_to(105, 105); c.line_to(260, 260); c.set_line_width(44); c.set_line_cap(1); c.set_source_rgba(*hx(YEL2)); c.stroke(); c.restore()
def chart(c, x0, y0, w, h, T, pts, upto=1.0, col=GRN, window=None):
    c.rectangle(x0, y0, w, h); c.set_source_rgba(1, 1, 1, .06); c.fill()
    for k in range(5): c.move_to(x0, y0 + k * h / 4); c.line_to(x0 + w, y0 + k * h / 4); c.set_source_rgba(1, 1, 1, .12); c.set_line_width(2); c.stroke()
    if window: c.rectangle(x0 + w * window[0], y0, w * (window[1] - window[0]), h); c.set_source_rgba(*hx(YEL2, .16)); c.fill()
    n = len(pts); m = max(1, int((n - 1) * upto))
    for i in range(m + 1):
        px = x0 + w * i / (n - 1); py = y0 + h * (1 - pts[i])
        (c.move_to if i == 0 else c.line_to)(px, py)
    c.set_source_rgba(*hx(col)); c.set_line_width(9); c.stroke()
    px = x0 + w * m / (n - 1); py = y0 + h * (1 - pts[m]); glow(c, px, py, 50, col, .9)
def bookmark(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-120, -170); c.line_to(120, -170); c.line_to(120, 190); c.line_to(0, 90); c.line_to(-120, 190); c.close_path(); c.set_source_rgba(*hx(YEL2)); c.fill(); c.restore()
    glow(c, x, y, 300 * s, YEL2, .3)

def b_hook(T, t0):
    s, c = surface(); sale_bg(c, T)
    t78 = wfind(0, 'seventy')
    tagshape(c, CX, 1200, 1.15 * pop(T, -.3), T, '$679.99', 'BLACK FRIDAY', sale=True)
    fr = post(to_np(s), T); ui_title(fr, "THIS 'DEAL' COST", '$78 MORE', 1.0, ya=420, yb=570, cb=HOT)
    if T > t78: stamp(fr, '+$78', 850, 860, T - t78, 12, 90)
    return fr
def b_watch(T, t0):
    tb = wfind(1, 'then six')
    s, c = surface(); sale_bg(c, T, col='4FC3FF')
    watch(c, CX, 800, 1.15 * pop(T, t0), T)
    if T < tb: tagshape(c, CX, 1220, .55 * pop(T, t0 + .3), T, '$602', 'OCTOBER', col=GRN)
    else: tagshape(c, CX, 1220, .55 * pop(T, tb), T, '$679', 'BLACK FRIDAY', sale=True)
    fr = post(to_np(s), T); chip(fr, 'A SMARTWATCH', CX, 450, T - t0, 'FFFFFF', 44, -2)
    if T > tb: chip(fr, 'SAME WATCH. HIGHER PRICE. SALE BADGE.', CX, 560, T - tb - .3, YEL2, 32, 2)
    return fr
def b_check(T, t0):
    t3, t10 = wfind(2, 'almost one'), wfind(2, 'nearly one')
    s, c = surface(); sale_bg(c, T)
    ng = int(25 * .29 * clamp((T - t3) / .8)) if T > t3 else 0; nr = int(25 * .09 * clamp((T - t10) / .6)) if T > t10 else 0
    card_grid(c, T, t0, max(ng, nr), nr)
    magnifier(c, 300 + 400 * clamp((T - t0) / 3), 1150 - 200 * math.sin(T), .7)
    fr = post(to_np(s), T); chip(fr, 'WATCHDOG CHECKED 350 AMAZON DEALS', CX, 450, T - t0, 'FFFFFF', 34, -2)
    if T > t3: title(fr, '1 IN 3: NO CHEAPER', 600, T - t3, size=96, fill='C8C8D0')
    if T > t10: chip(fr, '~1 IN 10 COST MORE', CX, 710, T - t10, HOT, 44, 2)
    return fr
def b_boots(T, t0):
    tb = wfind(3, 'to a hundred')
    s, c = surface(); sale_bg(c, T, col='B07A45'); boots(c, CX, 820, .95 * pop(T, t0), T)
    tagshape(c, CX, 1230, .55 * pop(T, t0 + .2 if T < tb else tb), T, '$98' if T < tb else '$180', 'A FEW WEEKS EARLIER' if T < tb else 'CYBER MONDAY "DEAL"', col=GRN if T < tb else YEL2, sale=T >= tb)
    fr = post(to_np(s), T)
    if T > tb: stamp(fr, '+$82', 840, 640, T - tb - .2, 10, 84)
    return fr
def b_amazon(T, t0):
    s, c = surface(); sale_bg(c, T, col='FFFFFF')
    for k, (x, txt) in enumerate(((300, 'STUDY'), (780, "AMAZON'S CHECK"))):
        p = pop(T, t0 + k * .5); c.rectangle(x - 200 * p, 900 - 260 * p, 400 * p, 520 * p); c.set_source_rgba(1, 1, 1, .1); c.fill()
    fr = post(to_np(s), T); chip(fr, 'AMAZON: THE STUDY IS "FLAWED"', CX, 460, T - t0, 'FFFFFF', 38, -2)
    title(fr, '1 IN 3', 900, T - t0 - .2, size=110, fill='C8C8D0', cx=300)
    if T > t0 + .5: title(fr, '98% REAL', 900, T - t0 - .6, size=96, fill=GRN, cx=780)
    chip(fr, 'WATCHDOG', 300, 1060, T - t0 - .3, 'C8C8D0', 34, -2); chip(fr, 'AMAZON', 780, 1060, T - t0 - .7, GRN, 34, 2)
    return fr
def b_how(T, t0): return quiet(T, t0, 'SO HOW', 'DO YOU KNOW?', 'hl', 130)
def b_rule(T, t0):
    tu = wfind(6, 'in the us')
    s, c = surface(); grad(c, [(0, '0A1240'), (1, '0A0A14')])
    for k in range(12): a = k * .5236; c.arc(300 + 150 * math.cos(a), 950 + 150 * math.sin(a), 16, 0, 6.29); c.set_source_rgba(1, .85, .1, 1); c.fill()
    if T > tu:
        c.rectangle(560, 700, 520, 520); c.set_source_rgba(.3, .05, .1, .5); c.fill()
        u = clamp((T - tu) / .3); c.move_to(700, 820); c.line_to(700 + 240 * u, 820 + 240 * u); c.move_to(940, 820); c.line_to(940 - 240 * u, 820 + 240 * u); c.set_source_rgba(*hx(HOT)); c.set_line_width(30); c.stroke()
    fr = post(to_np(s), T); chip(fr, 'EUROPE: MUST SHOW 30-DAY LOW', 300, 1230, T - t0, YEL2, 30, -2)
    if T > tu: chip(fr, 'US: NO SUCH RULE', 820, 1230, T - tu, HOT, 36, 2)
    title(fr, 'THE CROSSED-OUT PRICE', 480, T - t0, size=86, fill='FFFFFF')
    return fr
def b_tip(T, t0):
    tk = wfind(7, 'keepa'); tl = wfind(7, 'look at')
    s, c = surface(); sale_bg(c, T, col=GRN)
    c.save(); c.translate(CX, 1080); c.rectangle(-300, -480, 600, 960); c.set_source_rgba(.04, .04, .06, 1); c.fill(); c.rectangle(-280, -460, 560, 920); c.set_source_rgba(.09, .1, .13, 1); c.fill(); c.restore()
    pts = [.55, .5, .52, .48, .3, .32, .31, .3, .3, .62, .64, .7, .7]
    chart(c, 300, 820, 480, 420, T, pts, upto=clamp((T - t0) / 2.5), window=(.62, 1.0) if T > tl else None)
    fr = post(to_np(s), T); title(fr, 'CHECK PRICE HISTORY', 470, T - t0, size=92, fill=GRN)
    if T > tk: chip(fr, 'FREE: KEEPA  /  CAMELCAMELCAMEL', CX, 610, T - tk, 'FFFFFF', 34, -2)
    if T > tl: chip(fr, 'LAST 30 DAYS', CX, 1310, T - tl, YEL2, 40, 2)
    return fr
def b_sticker(T, t0):
    ts = wfind(8, 'sticker')
    s, c = surface(); sale_bg(c, T)
    chart(c, 160, 900, 760, 360, T, [.5] * 12, upto=1.0, col='C8C8D0', window=(.6, 1.0))
    if T > ts:
        u = clamp((T - ts) / .4); c.save(); c.translate(CX + 200 * u, 800 - 300 * u); c.rotate(.4 + 1.5 * u); c.arc(0, 0, 130, 0, 6.29); c.set_source_rgba(*hx(HOT, 1 - u * .6)); c.fill(); c.restore()
    fr = post(to_np(s), T); title(fr, "LINE DIDN'T DROP?", 520, T - t0, size=110, fill='FFFFFF')
    if T > ts: title(fr, "IT'S JUST A STICKER.", 680, T - ts, size=100, fill=HOT)
    return fr
def b_save(T, t0):
    s, c = surface(); sale_bg(c, T); bookmark(c, CX, 1050, 1.2 * pop(T, t0))
    fr = post(to_np(s), T); title(fr, 'SAVE THIS.', 520, T - t0, size=150, fill=YEL2); chip(fr, 'CHECK BEFORE YOU TAP BUY', CX, 680, T - t0 - .3, 'FFFFFF', 40, 2); return fr

def beats():
    return [(0, b_hook), (S[1], b_watch), (S[2], b_check), (S[3], b_boots), (S[4], b_amazon), (S[5], b_how), (S[6], b_rule),
        (S[7], b_tip), (S[8], b_sticker), (S[9], b_save), (END, None)]
BEATS = None
def frame(T, plat='ig'):
    global BEATS
    if BEATS is None: BEATS = beats()
    if T >= END:
        fr = np.zeros((H, W, 3), np.uint8); s_cta(fr, T, plat); return fr
    k = max(i for i in range(len(BEATS) - 1) if BEATS[i][0] <= T)
    t0, fn = BEATS[k]; t1 = BEATS[k + 1][0]
    fr = fn(T, t0)
    z = 1 + .05 * clamp((T - t0) / max(.5, t1 - t0)) + .06 * math.exp(-(T - t0) * 10)
    dx = dy = 0
    for at in (wfind(0, 'seventy'), wfind(1, 'then six'), wfind(3, 'to a hundred'), wfind(8, 'sticker')):
        a, b = shake(T, at); dx += a; dy += b
    fr = cv2.warpAffine(fr, np.float32([[z, 0, (1 - z) * CX + dx], [0, z, (1 - z) * H / 2 + dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    credit(fr, 'Illustrations. Sources: Groundwork Collaborative report via MarketWatch, EMARKETER, Digital Trends (Nov 2026); Amazon response.')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
