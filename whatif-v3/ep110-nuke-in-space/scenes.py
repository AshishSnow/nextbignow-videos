import sys, os, json, math
sys.path.insert(0, '/home/claude/nuke'); sys.path.insert(0, '/home/claude/samples')
from kit import *
import world as Wd
from world import surface, to_np, grad, stars, glow, earth_np, satellite, flash, aurora, palm, roof_people2, human, street, post
import essay as ES
D = '/home/claude/nuke'
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
def nuke_sat(c, x, y, s, T):
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
def b_hook(T, t0):
    img = space_bg(T); earth_np(img, CX, 1560, 640, T)
    ft = wfind(0, 'in space')
    add_layer(img, lambda c: (sat_ring(c, T, CX, 1560, 800, 260, 9), flash(c, CX + 150, 990, T, ft, 1.3)))
    fr = post(img, T); ui_title(fr, 'WHAT IF A NUKE WENT OFF', 'IN SPACE?', 1.0); return fr
def b_notcity(T, t0):
    s, c = surface(); grad(c, [(0, '0A1030'), (1, '2A1F5A')]); stars(c, T, 160, a=.7); city(c, T)
    fr = post(to_np(s), T); stamp(fr, 'NOT ON A CITY', CX, 640, T - t0, -6, 76); return fr
def b_altitude(T, t0):
    img = space_bg(T, 200); earth_np(img, CX, 2900, 1500, T, light=(0, -1, .4))
    u = eout(clamp((T - t0) / 1.0))
    def dr(c):
        c.set_source_rgba(1, .85, .3, .9); c.set_line_width(6); c.set_dash([18, 14]); c.move_to(CX, 1420); c.line_to(CX, 1420 - 820 * u); c.stroke(); c.set_dash([])
        if u > .9: glow(c, CX, 600, 120, 'FFF0B0', .9)
        c.set_source_rgba(1, 1, 1, 1); human(c, CX, 1430, .25, T, 'point')
    add_layer(img, dr); fr = post(img, T)
    if u > .6: title(fr, '250 MILES UP', 470, T - t0 - .6, size=120, fill=YEL); chip(fr, '(400 KM) - OVER YOUR HEAD', CX, 1000, T - t0 - .9, 'FFFFFF', 38, -2)
    return fr
def b_russia(T, t0):
    img = space_bg(T); earth_np(img, CX - 250, 1750, 700, T, light=(.4, -.7, .5))
    add_layer(img, lambda c: nuke_sat(c, CX + 80, 1050 + 20 * math.sin(T), .95 * pop(T, t0), T))
    fr = post(img, T); chip(fr, 'US INTELLIGENCE: RUSSIA IS BUILDING ONE', CX, 470, T - t0 - .2, 'FFFFFF', 32, -2); return fr
def b_nextmonth(T, t0):
    s, c = surface(); grad(c, [(0, '1A0B10'), (1, '3A0E18')]); glow(c, CX, 1100, 700, 'FF3B3B', .35)
    calendar(c, CX, 1120, 1.4 * pop(T, t0), T, clamp((T - wfind(2, 'next month')) / .4))
    fr = post(to_np(s), T); chip(fr, 'GERMANY WARNS:', CX, 470, T - t0, 'FFFFFF', 40, -2)
    t = wfind(2, 'next month')
    if T > t: stamp(fr, 'AS SOON AS NEXT MONTH', CX, 600, T - t, -5, 64)
    return fr
def b_thesis(T, t0):
    ts = wfind(3, 'and that')
    if T < ts: return quiet(T, t0, "IT WOULDN'T HURT", 'A SINGLE PERSON...', 'main', 104)
    return quiet(T, ts, "...AND THAT'S WHY IT'S", 'SO DANGEROUS.', 'hl', 104)
def film(fr, T):   # 1962 archive look: warm sepia, flicker, scratches
    f = fr.astype(np.float32) / 255; g = f.mean(2, keepdims=True); f = g * np.array([1.08, .95, .72]) * (.92 + .08 * math.sin(T * 37)) * .7 + f * .3
    rs = np.random.RandomState(int(T * 24))
    for k in range(3): x = rs.randint(0, W); f[:, x:x + 2] = np.clip(f[:, x:x + 2] + .25, 0, 1)
    return (np.clip(f, 0, 1) * 255).astype(np.uint8)
def b_1962(T, t0):
    s, c = surface(); grad(c, [(0, '05070F'), (.7, '0E1A30'), (1, '102235')]); stars(c, T, 220)
    u = clamp((T - t0) / 2.5)
    c.set_source_rgba(1, .9, .6, .9); c.set_line_width(5); c.move_to(CX - 100, 1500); c.curve_to(CX - 80, 1200, CX, 900, CX + 40, 1500 - 1100 * u); c.stroke()
    glow(c, CX + 40, 1500 - 1100 * u, 60, 'FFE2A0', 1)
    c.set_source_rgba(.01, .01, .02, 1); c.rectangle(0, 1500, W, 500); c.fill(); palm(c, 160, 1510, .7, T); palm(c, 900, 1520, .6, T)
    fr = film(post(to_np(s), T, grain=.06), T)
    tape(fr, 'JULY 9, 1962', CX, 460, T - t0, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    t = wfind(4, 'america')
    if T > t: chip(fr, 'U.S. TEST: STARFISH PRIME', CX, 620, T - t, YEL, 40, 2)
    return fr
def roof_sky(T, mode):
    s, c = surface()
    if mode == 'calm': grad(c, [(0, '050A1E'), (.7, '0D1C44'), (1, '1E2E66')]); stars(c, T, 220)
    elif mode == 'white': grad(c, [(0, 'FFF6DA'), (.6, 'FFE9A8'), (1, 'FFD07A')])
    else: grad(c, [(0, '12041F'), (.45, '5B0C36'), (.8, 'C8303F'), (1, 'F06A3A')]); stars(c, T, 120, a=.5); aurora(c, T, 1.3, cols=('FF3355', 'FF8844', '33FFAA')); glow(c, 700, 520, 560, 'FFB060', .5)
    palm(c, 70, 1560, 1.05, T); palm(c, 1010, 1590, .9, T); roof_people2(c, 1560, T); return to_np(s)
def b_party(T, t0):
    fr = post(roof_sky(T, 'calm'), T); chip(fr, 'HAWAII: ROOFTOP PARTIES', CX, 470, T - t0 - .2, 'FFFFFF', 40, -2); return fr
def b_sun(T, t0):
    img = roof_sky(T, 'white'); fr = post(img, T, bloom=1.5)
    title(fr, 'A BRAND NEW SUN', 560, T - t0, size=124, fill='E63946', rot=-3); return fr
def b_red(T, t0):
    fr = post(roof_sky(T, 'red'), T); title(fr, 'BLOOD RED', 560, T - t0, size=160, fill='FF4D5E', rot=-3); return fr
def b_lights(T, t0):
    t = wfind(7, 'three hundred'); n = int(clamp((T - t) / 1.6) * 6)
    lit = tuple(0 if k < n else 1 for k in range(5))
    s, c = surface(); street(c, T, lit); glow(c, CX, 150, 700, 'FF3366', .25)
    fr = post(to_np(s), T); chip(fr, '900 MILES AWAY', CX, 470, T - t0, 'FFFFFF', 40, -2)
    if T > t: title(fr, '300 STREETLIGHTS', 620, T - t, size=110, fill='FFFFFF'); tape(fr, 'WENT DARK', CX, 760, T - t - .3, col=RED, size=60, font=LUCKY, rot=-2, tcol='FFFFFF')
    return fr
def b_alarm(T, t0):
    s, c = surface(); grad(c, [(0, '050A1E'), (1, '151A3A')]); stars(c, T, 150); house_alarm(c, CX, 1450, 1.4, T, True)
    c.set_source_rgba(.01, .01, .03, 1); c.rectangle(0, 1450, W, 500); c.fill()
    fr = post(to_np(s), T); stamp(fr, 'ALARMS WENT OFF', CX, 600, T - t0, -6, 70); return fr
def b_phone(T, t0):
    t = wfind(7, 'cut out'); dead = T > t
    s, c = surface(); grad(c, [(0, '1A1208'), (1, '3A2A14')]); glow(c, CX, 1100, 600, 'FFB060', .3); phone_old(c, CX, 1150, 1.5 * pop(T, t0), T, dead)
    fr = film(post(to_np(s), T), T); chip(fr, 'CALLS BETWEEN ISLANDS', CX, 470, T - t0, 'FFFFFF', 40, -2)
    if dead: stamp(fr, 'CUT OUT', CX, 640, T - t, -6, 84)
    return fr
def b_invisible(T, t0): return quiet(T, t0, 'BUT THE REAL DAMAGE', 'WAS INVISIBLE.', 'hl', 110)
def b_belt(T, t0):
    img = space_bg(T); earth_np(img, CX, 1150, 380, T)
    ub = eout(clamp((T - t0) / 1.2)); td = wfind(9, 'within months')
    def dr(c):
        for k, (sc, a) in enumerate(((1.55, .55), (1.78, .4), (2.0, .25))):
            c.save(); c.translate(CX, 1150); c.rotate(-.35); c.scale(sc * 380, .42 * sc * 380); c.arc(0, 0, 1, 0, 6.29); c.restore()
            c.set_source_rgba(1, .3, .7, a * ub); c.set_line_width(20 - k * 4 + 5 * math.sin(T * 3 + k)); c.stroke()
        nd = int(clamp((T - td) / 1.5) * 6) if T > td else 0
        sat_ring(c, T, CX, 1150, 650, 300, 10, dead=tuple(range(nd)), s=.8, spd=.08)
    add_layer(img, dr); fr = post(img, T)
    chip(fr, 'A RADIATION BELT FOR YEARS', CX, 470, T - t0 - .1, PINK, 40, -2)
    if T > td: title(fr, '6 SATELLITES DEAD', 600, T - td, size=112, fill='FFFFFF')
    return fr
def b_telstar(T, t0):
    t = wfind(9, 'live tv'); dead = T > t + .4
    img = space_bg(T, 180)
    add_layer(img, lambda c: (telstar(c, CX + 150, 820, 1.4 * pop(T, t0), T, dead), tv_old(c, CX - 120, 1300, 1.0 * pop(T, t0 + .2), T, dead)))
    fr = post(img, T); chip(fr, 'TELSTAR: FIRST LIVE TV SATELLITE', CX, 470, T - t0, YEL, 36, -2); return fr
def b_today(T, t0):
    img = space_bg(T); earth_np(img, CX, 1150, 360, T)
    tn = wfind(10, 'eleven thousand'); n = int(1500 * eout(clamp((T - tn + .6) / 1.5)))
    add_layer(img, lambda c: swarm(c, T, CX, 1150, 360, n))
    fr = post(img, T); tape(fr, 'TODAY', CX, 460, T - t0, col=RED, size=70, font=LUCKY, rot=-3, tcol='FFFFFF')
    if T > tn: title(fr, '11,000+', 620, T - tn, size=170, fill=ICE); chip(fr, 'STARLINK SATELLITES ALONE', CX, 760, T - tn - .3, 'FFFFFF', 38, 2)
    return fr
def b_gps(T, t0):
    s, c = surface(); grad(c, [(0, '061226'), (1, '0E2A3E')]); stars(c, T, 120); mphone(c, CX, 1150, 1.5 * pop(T, t0), T)
    fr = post(to_np(s), T); title(fr, '+ THE GPS IN YOUR PHONE', 520, T - t0, size=86, fill='FFFFFF'); return fr
def b_wouldnt(T, t0):
    s, c = surface(); grad(c, [(0, '0A1030'), (1, '2A1F5A')]); stars(c, T, 160, a=.7); city(c, T, 1300, seed=9)
    glow(c, CX, 1560, 700, 'FF9A5A', .55); c.set_source_rgba(.01, .01, .03, 1); c.rectangle(0, 1560, W, 400); c.fill()
    for k, x in enumerate((200, 420, 640, 880)):
        c.set_source_rgba(.01, .01, .03, 1); human(c, x, 1600, .9, T, 'stand', k % 3, k); glow(c, x + 30, 1300, 60, 'BFFFE0', .7)
    fr = post(to_np(s), T); chip(fr, 'NOBODY ON THE GROUND GETS HURT...', CX, 470, T - t0 - .2, 'FFFFFF', 36, -2); return fr
def b_off(T, t0):
    ft = wfind(12, 'turn off'); off = clamp((T - ft) / 1.4)
    s, c = surface(); grad(c, [(0, '0A1030'), (1, '1A1440')]); stars(c, T, 160, a=1 - off * .8)
    flash(c, CX, 300, T, ft - .1, .8)
    for k in range(3): mphone(c, 250 + k * 290, 1200 + (k % 2) * 70, .7, T, on=0 if off * 3 > k else 1)
    fr = post(to_np(s), T)
    if T > ft: title(fr, 'TURN OFF THE SKY', 520, T - ft, size=120, fill='FFFFFF'); tape(fr, 'YOUR PHONE TALKS TO', CX, 660, T - ft - .3, col=YEL, size=54, font=LUCKY, rot=-2)
    return fr

def beats():
    return [(0, b_hook), (S[1], b_notcity), (wfind(1, 'two hundred'), b_altitude), (S[2], b_russia), (wfind(2, 'and germany'), b_nextmonth),
        (S[3], b_thesis), (S[4], b_1962), (S[5], b_party), (S[6], b_sun), (wfind(6, 'then turned'), b_red),
        (S[7], b_lights), (wfind(7, 'burglar'), b_alarm), (wfind(7, 'phone calls'), b_phone), (S[8], b_invisible),
        (S[9], b_belt), (wfind(9, 'including'), b_telstar), (S[10], b_today), (wfind(10, 'plus the gps'), b_gps),
        (S[11], b_wouldnt), (S[12], b_off), (END, None)]
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
    for at in (wfind(0, 'in space'), S[6], wfind(7, 'cut out'), wfind(9, 'within months'), wfind(12, 'turn off')):
        a, b = shake(T, at); dx += a; dy += b
    fr = cv2.warpAffine(fr, np.float32([[z, 0, (1 - z) * CX + dx], [0, z, (1 - z) * H / 2 + dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    credit(fr, 'Illustrations. Sources: US DIA (2026), Euronews, 10 Things (Nov 2026), Nat Geo, Starfish Prime records (1962).')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
