import sys, os, json, math
sys.path.insert(0, '/home/claude/sat'); sys.path.insert(0, '/home/claude/samples')
from kit import *
import world as Wd
from world import surface, to_np, grad, stars, glow, earth_np, satellite, flash, aurora, palm, roof_people2, human, street, post
import essay as ES
D = '/home/claude/sat'
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
def sat_ring(c, T, cx, cy, rx, ry, n, dead=(), s=.7, spd=.05, tilt=0.0):
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
def sat_sat(c, x, y, s, T):
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

# ---------- satellite-crash props ----------
def iridium(c, x, y, s, T, rot=0.0, glow_=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for k, a in enumerate((-.5, .5, 1.57)):
        c.save(); c.rotate(a + 1.57); c.rectangle(40, -38, 200, 76); c.set_source_rgba(*hx('2E6FD8')); c.fill_preserve(); c.set_source_rgba(.75, .85, 1, 1); c.set_line_width(4); c.stroke()
        for j in range(1, 4): c.move_to(40 + j * 50, -38); c.rel_line_to(0, 76); c.stroke()
        c.restore()
    c.move_to(-50, -90); c.line_to(50, -90); c.line_to(70, 90); c.line_to(-70, 90); c.close_path(); c.set_source_rgba(*hx('D9B45A')); c.fill()
    c.restore()
    if glow_: glow(c, x, y, 160 * s, '7FC8FF', .35 * glow_)
def cosmos(c, x, y, s, T, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.rectangle(-60, -170, 120, 340); g = cairo.LinearGradient(-60, 0, 60, 0); g.add_color_stop_rgb(0, .25, .26, .28); g.add_color_stop_rgb(.5, .62, .63, .64); g.add_color_stop_rgb(1, .2, .2, .22); c.set_source(g); c.fill()
    c.arc(0, -170, 60, 3.14, 6.28); c.set_source_rgba(.45, .46, .48, 1); c.fill()
    for yy in (-100, 0, 100): c.rectangle(-60, yy, 120, 8); c.set_source_rgba(.15, .15, .16, 1); c.fill()
    c.move_to(0, 170); c.line_to(0, 300); c.set_source_rgba(.6, .6, .6, 1); c.set_line_width(6); c.stroke()
    c.restore()
def debris(c, T, t0, cx, cy, n=420, spread=900, seed=7, col=(1, .8, .5), life=99, size=3.0, a=1.0):
    u = T - t0
    if u < 0: return
    rs = np.random.RandomState(seed)
    for k in range(n):
        ang = rs.uniform(0, 6.283); sp = rs.uniform(.15, 1) ** 1.5 * spread; e = rs.uniform(.5, 1.6)
        d = sp * (1 - math.exp(-u * 1.8 * e)) + sp * .04 * u
        x = cx + d * math.cos(ang); y = cy + d * math.sin(ang) * rs.uniform(.5, 1)
        hot = math.exp(-u * 1.5)
        c.arc(x, y, size * rs.uniform(.5, 1.6), 0, 6.29)
        c.set_source_rgba(col[0], col[1] * (1 - .5 * hot) + .5 * hot, col[2] * (1 - hot) + hot * .9, a * rs.uniform(.5, 1)); c.fill()
def iss(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-420, -14, 840, 28); c.set_source_rgba(.75, .75, .78, 1); c.fill()
    for px in (-400, -260, 180, 320):
        for py in (-1, 1):
            c.rectangle(px, py * 30 + (0 if py > 0 else -170), 90, 170); c.set_source_rgba(*hx('C9A04A')); c.fill_preserve(); c.set_source_rgba(.4, .3, .1, 1); c.set_line_width(3); c.stroke()
    for mx, mw in ((-120, 90), (-20, 150), (140, 70)): c.rectangle(mx, -40, mw, 80); c.set_source_rgba(.88, .88, .9, 1); c.fill_preserve(); c.set_source_rgba(.4, .4, .45, 1); c.stroke()
    c.restore()
def highway(c, T, dark_ratio=.5):
    grad(c, [(0, '05060F'), (.45, '0B1030'), (1, '141428')]); stars(c, T, 140, ymax=700)
    vx, vy = CX, 760
    c.move_to(vx - 10, vy); c.line_to(vx + 10, vy); c.line_to(W + 300, H); c.line_to(-300, H); c.close_path(); c.set_source_rgba(.07, .07, .1, 1); c.fill()
    for k in (-1, 0, 1):
        for j in range(14):
            u0 = ((j / 14 + T * .25) % 1); u1 = u0 + .025
            x0, y0 = vx + k * (600 * u0 ** 2), vy + (H - vy) * u0 ** 2; x1, y1 = vx + k * (600 * u1 ** 2), vy + (H - vy) * u1 ** 2
            c.move_to(x0, y0); c.line_to(x1, y1); c.set_source_rgba(1, .85, .3, .8); c.set_line_width(3 + 10 * u0); c.stroke()
    rs = np.random.RandomState(3)
    for j in range(16):
        lane = rs.choice([-1.5, -.5, .5, 1.5]); u = (rs.uniform(0, 1) + T * .12) % 1
        x = vx + lane * 300 * u ** 2; y = vy + (H - vy) * u ** 2; sc = .08 + 1.1 * u ** 2
        dead = rs.rand() < dark_ratio
        c.save(); c.translate(x, y); c.scale(sc, sc)
        c.rectangle(-90, -60, 180, 70); c.set_source_rgba(.02, .02, .04, 1); c.fill()
        c.rectangle(-60, -100, 120, 45); c.fill(); c.restore()
        if not dead:
            for d in (-1, 1): glow(c, x + d * 60 * sc, y - 30 * sc, 60 * sc + 4, 'FF3030', .9)
def sun_storm(c, T, t0, cx=W + 120, cy=520):
    glow(c, cx, cy, 900, 'FF9A2A', .55); glow(c, cx, cy, 420, 'FFE08A', 1)
    c.arc(cx, cy, 300, 0, 6.29); c.set_source_rgba(1, .85, .45, 1); c.fill()
    u = clamp((T - t0) / 1.6)
    for k in range(24):
        a = 3.14 + (k - 12) * .045; r0 = 300; r1 = 300 + 1300 * u * (.6 + .4 * math.sin(k * 7))
        c.move_to(cx + r0 * math.cos(a), cy + r0 * math.sin(a)); c.line_to(cx + r1 * math.cos(a), cy + r1 * math.sin(a))
        c.set_source_rgba(1, .7, .3, .25); c.set_line_width(14); c.stroke()
def dial(c, x, y, r, T, frac, col='FF3B3B'):
    c.arc(x, y, r, 0, 6.29); c.set_source_rgba(.06, .06, .1, .9); c.fill()
    c.arc(x, y, r, 0, 6.29); c.set_source_rgba(1, 1, 1, .9); c.set_line_width(10); c.stroke()
    c.move_to(x, y); c.arc(x, y, r - 14, -1.57, -1.57 + 6.283 * frac); c.close_path(); c.set_source_rgba(*hx(col, .85)); c.fill()
    for k in range(12): a = k * .5236; c.move_to(x + (r - 30) * math.cos(a), y + (r - 30) * math.sin(a)); c.line_to(x + (r - 10) * math.cos(a), y + (r - 10) * math.sin(a)); c.set_source_rgba(1, 1, 1, .8); c.set_line_width(5); c.stroke()
def dodge_sat(c, x, y, s, T, k=0):
    off = 40 * math.sin(T * 3 + k) ** 3
    iridium(c, x + off, y, s, T, rot=.3, glow_=.6)

def crash_pos(T, t0, tc):
    u = clamp((T - t0) / max(.3, tc - t0)); return u
def b_hook(T, t0):
    img = space_bg(T); earth_np(img, CX, 1700, 820, T, light=(.3, -.8, .5))
    tc = wfind(0, 'right over')
    u = crash_pos(T, 0, tc)
    def dr(c):
        if T < tc:
            c.set_source_rgba(.5, .8, 1, .35); c.set_dash([16, 12]); c.set_line_width(4)
            c.move_to(-100, 1250); c.line_to(W + 100, 650); c.stroke(); c.move_to(-100, 650); c.line_to(W + 100, 1250); c.stroke(); c.set_dash([])
            iridium(c, -100 + (CX + 100) * u, 1250 - 300 * u, .5, T, rot=.4)
            cosmos(c, W + 100 - (W + 100 - CX) * u, 1250 - 300 * u, .45, T, rot=T * 1.5)
        flash(c, CX, 950, T, tc, 1.1); debris(c, T, tc, CX, 950, n=300, spread=700)
    add_layer(img, dr); fr = post(img, T)
    ui_title(fr, 'WHAT IF TWO SATELLITES', 'CRASHED?', 1.0, ya=420, yb=560); return fr
def b_bullet(T, t0):
    tb = wfind(1, 'ten times')
    s, c = surface(); grad(c, [(0, '0A0A18'), (1, '1A1030')]); stars(c, T, 120)
    if T < tb:
        u = clamp((T - t0) / .8)
        for d in (-1, 1):
            c.save(); c.translate(CX + d * (300 - 230 * u), 1250); c.scale(-d, 1)
            c.rectangle(-140, -60, 280, 90); c.set_source_rgba(*hx('E63946' if d < 0 else '2D6CDF')); c.fill()
            c.rectangle(-80, -120, 160, 65); c.fill()
            for wx in (-90, 90): c.arc(wx, 35, 36, 0, 6.29); c.set_source_rgba(.05, .05, .05, 1); c.fill()
            c.restore()
        fr = post(to_np(s), T); stamp(fr, 'NOT A FENDER BENDER', CX, 620, T - t0 - .2, -5, 64); return fr
    u = (T - tb) * 2.2 % 1.2
    for k in range(10):
        x = -200 + (W + 400) * u - k * 60
        c.move_to(x, 1150); c.line_to(x - 260, 1150); c.set_source_rgba(1, .8, .4, .12 * (10 - k) / 10); c.set_line_width(26 - k * 2); c.stroke()
    c.save(); c.translate(-200 + (W + 400) * u, 1150); c.move_to(-70, -22); c.line_to(30, -22); c.curve_to(80, -22, 90, 0, 90, 0); c.curve_to(90, 0, 80, 22, 30, 22); c.line_to(-70, 22); c.close_path(); c.set_source_rgba(*hx('D9A441')); c.fill(); c.restore()
    fr = post(to_np(s), T); title(fr, '10X FASTER', 560, T - tb, size=170, fill=YEL); chip(fr, 'THAN A BULLET (26,000 MPH)', CX, 720, T - tb - .3, 'FFFFFF', 40, -2); return fr
def b_siberia(T, t0):
    img = space_bg(T); earth_np(img, CX, 1250, 520, T, light=(-.3, -.6, .75), spin=.01)
    add_layer(img, lambda c: (glow(c, CX - 40, 860, 70, 'FF3B3B', .8 + .2 * math.sin(T * 6)), c.arc(CX - 40, 860, 14, 0, 6.29), c.set_source_rgba(1, .2, .2, 1), c.fill()))
    fr = post(img, T); tape(fr, 'FEB 10, 2009', CX, 450, T - t0, col=RED, size=70, font=LUCKY, rot=-3, tcol='FFFFFF')
    t = wfind(2, 'siberia')
    if T > t: chip(fr, '490 MILES OVER SIBERIA', CX, 620, T - t, 'FFFFFF', 42, 2)
    return fr
def b_two(T, t0):
    img = space_bg(T)
    td = wfind(3, 'and a dead')
    def dr(c):
        iridium(c, 330, 1000, .9 * pop(T, t0), T, rot=.2 + .05 * math.sin(T))
        if T > td: cosmos(c, 790, 1080, .85 * pop(T, td), T, rot=T * .9)
    add_layer(img, dr); fr = post(img, T)
    chip(fr, 'WORKING  -  USA', 330, 700, T - t0 - .1, CYAN, 40, -3)
    if T > td: chip(fr, 'DEAD SINCE 1995  -  RUSSIA', 790, 760, T - td - .1, 'BBBBBB', 34, 3)
    return fr
def b_boom(T, t0):
    img = space_bg(T); tc = t0 + .15
    def dr(c):
        u = clamp((T - t0) / .15)
        if T < tc: iridium(c, 300 + 240 * u, 1000, .7, T); cosmos(c, 780 - 240 * u, 1000, .65, T, rot=1.2)
        flash(c, CX, 1000, T, tc, 1.4); debris(c, T, tc, CX, 1000, n=520, spread=1100, seed=3)
    add_layer(img, dr); fr = post(img, T, bloom=1.3)
    t = wfind(4, 'over two')
    if T > t: title(fr, '2,000+ PIECES', 560, T - t, size=150, fill='FFFFFF'); tape(fr, 'OF SHRAPNEL', CX, 710, T - t - .3, col=RED, size=60, font=LUCKY, rot=-2, tcol='FFFFFF')
    return fr
def b_still(T, t0):
    img = space_bg(T); earth_np(img, CX, 1150, 380, T)
    def dr(c):
        rs = np.random.RandomState(9)
        for k in range(260):
            a = rs.uniform(0, 6.28) + T * .12; rr = rs.uniform(470, 560)
            x, y = CX + rr * math.cos(a), 1150 + rr * math.sin(a) * .45 - (rr - 470) * .1
            if math.sin(a) < 0 and abs(x - CX) < 380: continue
            c.arc(x, y, 2.6, 0, 6.29); c.set_source_rgba(1, .55, .35, .9); c.fill()
    add_layer(img, dr); fr = post(img, T)
    tape(fr, '15 YEARS LATER', CX, 450, T - t0, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    t = wfind(5, 'over a thousand')
    if T > t: title(fr, '1,000+ STILL UP THERE', 600, T - t, size=100, fill='FF8A5A')
    return fr
def b_iss(T, t0):
    img = space_bg(T); earth_np(img, CX, 2500, 1300, T, light=(0, -1, .5))
    ts = wfind(6, 'had to hide')
    def dr(c):
        iss(c, CX, 1050, .95 * pop(T, t0), T)
        if T > ts:
            u = clamp((T - ts) / 1.2); x = -200 + (W + 400) * u
            c.move_to(x, 820); c.line_to(x - 300, 760); c.set_source_rgba(1, .6, .3, .7); c.set_line_width(6); c.stroke(); glow(c, x, 820, 40, 'FFB070', 1)
    add_layer(img, dr); fr = post(img, T)
    tape(fr, '2012', CX, 450, T - t0, col=RED, size=70, font=LUCKY, rot=-3, tcol='FFFFFF')
    if T > ts: chip(fr, 'CREW HID IN ESCAPE CAPSULES', CX, 620, T - ts, YEL, 40, 2)
    return fr
def b_one(T, t0): return quiet(T, t0, 'BUT THAT WAS', 'ONE CRASH.', 'hl', 130)
def b_today(T, t0):
    img = space_bg(T); earth_np(img, CX, 1150, 360, T)
    tj = wfind(8, 'and half')
    def dr(c):
        swarm(c, T, CX, 1150, 360, 1400)
        if T > tj:
            rs = np.random.RandomState(5)
            for k in range(1200):
                ph = rs.uniform(0, 6.28) + T * .18; rr = 360 * rs.uniform(1.06, 1.35); inc = rs.uniform(-1.2, 1.2)
                x = CX + rr * math.cos(ph); y = 1150 + rr * math.sin(ph) * math.sin(inc) * .9
                if math.sin(ph) * math.cos(inc) < 0 and (x - CX) ** 2 + (y - 1150) ** 2 < 360 ** 2: continue
                c.arc(x, y, 2.2, 0, 6.29); c.set_source_rgba(1, .3, .3, .9 * clamp((T - tj) / .8)); c.fill()
    add_layer(img, dr); fr = post(img, T)
    title(fr, '16,000+', 520, T - t0, size=170, fill=ICE); chip(fr, 'WORKING SATELLITES', CX, 660, T - t0 - .3, 'FFFFFF', 40, -2)
    if T > tj: chip(fr, '+ ~15,000 PIECES OF DEAD JUNK', CX, 750, T - tj, 'FF6B6B', 38, 2)
    return fr
def b_highway(T, t0):
    s, c = surface(); highway(c, T); fr = post(to_np(s), T)
    title(fr, 'HALF THE CARS', 470, T - t0, size=120, fill='FFFFFF'); tape(fr, 'HAVE NO DRIVER', CX, 610, T - t0 - .3, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF'); return fr
def b_dodge(T, t0):
    img = space_bg(T); earth_np(img, CX, 2400, 1250, T, light=(0, -1, .5))
    def dr(c):
        for k, (x, y) in enumerate(((260, 900), (760, 1000), (480, 1250), (880, 1350))):
            dodge_sat(c, x, y, .45, T * 1.3, k)
            u = ((T * .9 + k * .3) % 1); c.move_to(x - 400 + 800 * u, y - 140); c.line_to(x - 520 + 800 * u, y - 160); c.set_source_rgba(1, .5, .3, .7); c.set_line_width(4); c.stroke()
    add_layer(img, dr); fr = post(img, T)
    title(fr, '~1,000 DODGES', 520, T - t0, size=130, fill=YEL); chip(fr, 'EVERY DAY - STARLINK ALONE', CX, 660, T - t0 - .3, 'FFFFFF', 40, -2); return fr
def b_clock(T, t0):
    ts, t18 = wfind(10, 'if every'), wfind(10, 'in twenty eighteen')
    s, c = surface(); grad(c, [(0, '1A0A06'), (1, '2A0E20')]); stars(c, T, 100)
    if T > ts: sun_storm(c, T, ts)
    dial(c, CX, 1150, 300 * pop(T, t0), T, clamp((T - t0) / 3) * (2.8 / 7) if T < t18 else 1.0, 'FF3B3B' if T < t18 else '3FAE5A')
    fr = post(to_np(s), T); chip(fr, 'THE "CRASH CLOCK"', CX, 450, T - t0, 'FFFFFF', 44, -2)
    t = wfind(10, 'under three')
    if T > t and T < t18: title(fr, 'UNDER 3 DAYS', 620, T - t, size=130, fill='FF5A5A')
    if T > t18: title(fr, '2018: 4 MONTHS', 620, T - t18, size=120, fill='9BFFB0')
    return fr
def b_chain(T, t0):
    img = space_bg(T); earth_np(img, CX, 1250, 330, T)
    def dr(c):
        for k, (x, y, at) in enumerate(((300, 800, .2), (760, 760, 1.0), (520, 1650, 1.7), (900, 1450, 2.3), (180, 1400, 2.8))):
            tt = t0 + at
            if T < tt: iridium(c, x, y, .35, T, rot=k)
            flash(c, x, y, T, tt, .35); debris(c, T, tt, x, y, n=120, spread=380, seed=k + 20)
    add_layer(img, dr); fr = post(img, T)
    title(fr, 'MORE JUNK = MORE CRASHES', 480, T - t0, size=86, fill='FFFFFF')
    if T > wfind(11, 'causes'): chip(fr, 'SCIENTISTS CALL IT KESSLER SYNDROME', CX, 600, T - wfind(11, 'causes'), YEL, 34, 2)
    return fr
def b_90(T, t0):
    img = space_bg(T); earth_np(img, CX, 1200, 400, T)
    add_layer(img, lambda c: (swarm(c, T, CX, 1200, 400, 1600), dodge_sat(c, CX + 260, 820, .4, T * 2)))
    fr = post(img, T); title(fr, 'A DODGE EVERY', 470, T - t0, size=96, fill='FFFFFF'); title(fr, '90 SECONDS', 610, T - t0 - .3, size=150, fill=YEL); return fr
def b_end(T, t0):
    tw = wfind(13, 'every single')
    if T < tw: return quiet(T, t0, 'AND THEY HAVE TO', 'WIN...', 'main', 130)
    img = space_bg(T); add_layer(img, lambda c: (flash(c, CX, 1150, T, tw + .6, 1.0), debris(c, T, tw + .6, CX, 1150, n=350, spread=900, seed=12)))
    fr = post(img, T); title(fr, 'EVERY. SINGLE. TIME.', 560, T - tw, size=104, fill=YEL); return fr

def beats():
    return [(0, b_hook), (S[1], b_bullet), (S[2], b_siberia), (S[3], b_two), (S[4], b_boom), (S[5], b_still), (S[6], b_iss),
        (S[7], b_one), (S[8], b_today), (wfind(8, 'like a highway'), b_highway), (S[9], b_dodge), (S[10], b_clock), (S[11], b_chain),
        (S[12], b_90), (S[13], b_end), (END, None)]
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
    for at in (wfind(0, 'right over'), S[4] + .15, wfind(6, 'had to hide'), wfind(10, 'under three'), wfind(13, 'every single') + .6):
        a, b = shake(T, at); dx += a; dy += b
    fr = cv2.warpAffine(fr, np.float32([[z, 0, (1 - z) * CX + dx], [0, z, (1 - z) * H / 2 + dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    credit(fr, 'Illustrations. Sources: NASA/Wikipedia (2009 collision), Orbital Radar (Nov 2026), SpaceX FCC reports via Space.com, Thiele et al. CRASH Clock (2025).')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
