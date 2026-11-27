import sys, os, json, math
sys.path.insert(0, '/home/claude/cash'); sys.path.insert(0, '/home/claude/samples')
from kit import *
import world as Wd
from world import surface, to_np, grad, stars, glow, earth_np, satellite, flash, aurora, palm, roof_people2, human, street, post
import essay as ES
D = '/home/claude/cash'
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
def cash_ring(c, T, cx, cy, rx, ry, n, dead=(), s=.7, spd=.05, tilt=0.0):
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
def cash_sat(c, x, y, s, T):
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


# ---------- free-money props (warm golden world) ----------
GOLD = 'FFC94A'; GREEN = '7CFFB2'
def warm_sky(c, T, top='1B0F3A', mid='7A2E5C', bot='FF9A4A'):
    grad(c, [(0, top), (.55, mid), (1, bot)])
def rocket(c, x, y, s, T, fire=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if fire > 0:
        for k in range(3):
            fl = 1 + .15 * math.sin(T * 30 + k)
            c.move_to(-40 + k * 10, 230); c.curve_to(-60, 380 * fl, 0, 520 * fl * fire, 0, 560 * fl * fire); c.curve_to(0, 520 * fl, 60, 380 * fl, 40 - k * 10, 230); c.close_path()
            c.set_source_rgba(1, (.9, .6, .3)[k], (.6, .2, .1)[k], .8); c.fill()
    c.move_to(0, -300); c.curve_to(90, -200, 90, 100, 70, 240); c.line_to(-70, 240); c.curve_to(-90, 100, -90, -200, 0, -300); c.close_path()
    g = cairo.LinearGradient(-90, 0, 90, 0); g.add_color_stop_rgb(0, .7, .72, .78); g.add_color_stop_rgb(.45, 1, 1, 1); g.add_color_stop_rgb(1, .55, .57, .62); c.set_source(g); c.fill()
    c.arc(0, -90, 34, 0, 6.29); c.set_source_rgba(*hx('2A4D69')); c.fill_preserve(); c.set_source_rgba(.9, .9, .95, 1); c.set_line_width(8); c.stroke()
    for d in (-1, 1): c.move_to(d * 70, 120); c.line_to(d * 150, 280); c.line_to(d * 70, 240); c.close_path(); c.set_source_rgba(*hx('E63946')); c.fill()
    c.restore()
    if fire > 0: glow(c, x, y + 330 * s, 260 * s, 'FFB040', .7 * fire)
def certificate(c, x, y, s, T):
    c.save(); c.translate(x, y); c.rotate(-.06 + .02 * math.sin(T)); c.scale(s, s)
    c.rectangle(-330, -210, 660, 420); c.set_source_rgba(.98, .95, .86, 1); c.fill()
    c.rectangle(-305, -185, 610, 370); c.set_source_rgba(*hx('2F6B4F')); c.set_line_width(10); c.stroke()
    c.rectangle(-290, -170, 580, 340); c.set_line_width(3); c.stroke()
    c.select_font_face('Luckiest Guy'); c.set_font_size(58); c.set_source_rgba(*hx('2F6B4F'))
    for txt, yy, sz in (('STOCK CERTIFICATE', -70, 50), ('1 SHARE', 30, 84)):
        c.set_font_size(sz); e = c.text_extents(txt); c.move_to(-e.width / 2, yy); c.show_text(txt)
    c.arc(220, 110, 46, 0, 6.29); c.set_source_rgba(*hx('C9A04A')); c.fill()
    c.restore()
def kids_grid(c, T, n_on, y0=900, rows=6, cols=9, col=(1, .85, .45)):
    k = 0
    for r in range(rows):
        for q in range(cols):
            x = 110 + q * 108; y = y0 + r * 120
            a = .9 if k < n_on else .15
            c.set_source_rgba(*col, a); human(c, x, y + 90, .28, T, 'stand', k % 3, k); k += 1
def mountains(c, T, gy=1350, aur=1.0):
    grad(c, [(0, '050B24'), (.6, '0E2A4A'), (1, '1E4D6B')]); stars(c, T, 180, ymax=900)
    if aur: aurora(c, T, aur, cols=('33FFAA', '44DDFF', 'AA66FF'), top=200, bot=1000)
    for (x0, h, colr) in ((-100, 520, '1B3550'), (300, 640, '23405E'), (700, 560, '1B3550')):
        c.move_to(x0, gy); c.line_to(x0 + 300, gy - h); c.line_to(x0 + 600, gy); c.close_path(); c.set_source_rgba(*hx(colr)); c.fill()
        c.move_to(x0 + 300, gy - h); c.line_to(x0 + 230, gy - h + 140); c.line_to(x0 + 260, gy - h + 120); c.line_to(x0 + 300, gy - h + 160); c.line_to(x0 + 340, gy - h + 120); c.line_to(x0 + 370, gy - h + 140); c.close_path(); c.set_source_rgba(.92, .96, 1, 1); c.fill()
    c.rectangle(0, gy, W, H - gy); c.set_source_rgba(.85, .92, 1, 1); c.fill()
def cabin(c, x, y, s, T, wood=True):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-220, -200, 440, 200); c.set_source_rgba(*hx('5A3420')); c.fill()
    for k in range(5): c.move_to(-220, -200 + k * 40); c.line_to(220, -200 + k * 40); c.set_source_rgba(.25, .13, .07, 1); c.set_line_width(4); c.stroke()
    c.move_to(-260, -200); c.line_to(0, -360); c.line_to(260, -200); c.close_path(); c.set_source_rgba(.95, .97, 1, 1); c.fill()
    c.rectangle(-150, -150, 90, 80); c.set_source_rgba(1, .8, .4, 1); c.fill(); c.restore()
    glow(c, x - 105 * s, y - 110 * s, 200 * s, 'FFB040', .6)
    if wood:
        c.save(); c.translate(x, y); c.scale(s, s)
        for r in range(3):
            for q in range(5 - r): c.arc(260 + q * 46 + r * 23, -26 - r * 42, 22, 0, 6.29); c.set_source_rgba(*hx('C08A57')); c.fill_preserve(); c.set_source_rgba(.4, .22, .1, 1); c.set_line_width(4); c.stroke()
        c.restore()
def check(c, x, y, s, T, amt='$1,000', rot=-.08):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.rectangle(-300, -130, 600, 260); c.set_source_rgba(.88, .97, .9, 1); c.fill()
    c.rectangle(-300, -130, 600, 40); c.set_source_rgba(*hx('2F6B4F')); c.fill()
    c.select_font_face('Luckiest Guy'); c.set_font_size(90); c.set_source_rgba(*hx('1C1614')); e = c.text_extents(amt); c.move_to(-e.width / 2, 60); c.show_text(amt)
    c.move_to(-260, 105); c.line_to(260, 105); c.set_source_rgba(.3, .3, .3, 1); c.set_line_width(3); c.stroke()
    c.restore()
def bars(c, T, t0, vals, labels_x, maxv, cols, y=1450, h=620, w=200):
    for k, (v, x, col) in enumerate(zip(vals, labels_x, cols)):
        u = eout(clamp((T - t0 - k * .5) / .8)); hh = h * v / maxv * u
        c.rectangle(x - w / 2, y - hh, w, hh); c.set_source_rgba(*hx(col)); c.fill()
        glow(c, x, y - hh, 120, col, .35 * u)
def pipeline(c, T, y=1250):
    for k in range(9):
        x = k * 135; c.rectangle(x, y - 20, 130, 40); c.set_source_rgba(.62, .64, .68, 1); c.fill(); c.rectangle(x + 120, y - 30, 14, 60); c.set_source_rgba(.4, .42, .46, 1); c.fill()
        c.rectangle(x + 50, y + 20, 18, 90); c.fill()
def b_hook(T, t0):
    s, c = surface(); warm_sky(c, T); stars(c, T, 120, ymax=900, a=.7)
    u = clamp(T / 4)
    rocket(c, CX, 1000 - 250 * u, .9, T)
    rs = np.random.RandomState(4)
    for k in range(40):
        x = rs.uniform(60, W - 60); y = ((rs.uniform(0, 1) + T * .25) % 1) * 1500 + 200
        c.save(); c.translate(x, y); c.scale(1, abs(math.sin(T * 3 + k)) + .2); c.arc(0, 0, 20, 0, 6.29); c.restore(); c.set_source_rgba(*hx(GOLD)); c.fill()
    c.set_source_rgba(.03, .02, .05, 1); c.rectangle(0, 1560, W, 400); c.fill()
    for k, x in enumerate((180, 380, 600, 820)): c.set_source_rgba(.03, .02, .05, 1); human(c, x, 1580, .55, T, 'point' if k % 2 else 'stand', k % 3, k)
    fr = post(to_np(s), T); ui_title(fr, 'FREE MONEY MADE PEOPLE', 'WORK MORE.', 1.0, ya=420, yb=560); return fr
def b_share(T, t0):
    tk = wfind(2, "that's seventy")
    s, c = surface(); warm_sky(c, T, '120A2A', '3A1F55', '7A3E6A'); stars(c, T, 120)
    if T < tk:
        rocket(c, 850, 880, .45, T, .6); certificate(c, CX, 1180, 1.25 * pop(T, t0), T)
        fr = post(to_np(s), T); chip(fr, 'ELON MUSK: 1 SPACEX SHARE PER KID', CX, 470, T - t0, 'FFFFFF', 34, -2); chip(fr, '1 SHARE = ~$146', CX, 860, T - t0 - .6, GOLD, 44, 2); return fr
    kids_grid(c, T, int(54 * clamp((T - tk) / 1.5)))
    fr = post(to_np(s), T); title(fr, '72 MILLION KIDS', 520, T - tk, size=120, fill='FFFFFF')
    return fr
def b_lazy(T, t0):
    return quiet(T, t0, 'SO... WILL THEY', 'GROW UP LAZY?', 'hl', 110)
def b_forty(T, t0):
    s, c = surface(); mountains(c, T); fr = post(to_np(s), T)
    title(fr, 'ONE STATE', 520, T - t0, size=150, fill='FFFFFF'); tape(fr, 'HAS DONE IT FOR 40+ YEARS', CX, 680, T - t0 - .4, col=GREEN, size=50, font=LUCKY, rot=-2); return fr
def b_alaska(T, t0):
    s, c = surface(); mountains(c, T, aur=.6); pipeline(c, T, 1300)
    tb = wfind(4, 'even babies')
    for k in range(4):
        u = ((T - t0) * .5 + k * .25) % 1
        check(c, 120 + u * 840, 1200 - 380 * math.sin(u * 3.14), .25, T, '$', rot=u * 6)
    cabin(c, 820, 1520, .6, T, wood=False)
    fr = post(to_np(s), T); tape(fr, 'ALASKA, SINCE 1982', CX, 450, T - t0, col=RED, size=62, font=LUCKY, rot=-3, tcol='FFFFFF')
    if T > tb: chip(fr, 'EVERYONE. EVEN BABIES.', CX, 620, T - tb, GOLD, 46, 2)
    return fr
def b_amounts(T, t0):
    s, c = surface(); warm_sky(c, T, '0E1A2A', '1E3A3A', '2F5E4A')
    t22, tf = wfind(5, 'in twenty'), 1e9
    if T < tf:
        bars(c, T, t0, (1000, 3284), (330, 750), 3600, ('8FD9A8', GOLD))
        fr = post(to_np(s), T); chip(fr, '1982: $1,000', 330, 1530, T - t0 - .3, 'FFFFFF', 40, -2)
        if T > t22: chip(fr, '2022: $3,284', 750, 1530, T - t22, GOLD, 40, 2); title(fr, 'RECORD YEAR', 520, T - t22, size=120, fill=GOLD)
        return fr
    check(c, CX, 1150, 1.4 * pop(T, tf), T, '$16,000+')
    for k in range(5): c.set_source_rgba(.03, .03, .05, 1); human(c, 220 + k * 160, 1620, .45 - (k % 2) * .12, T, 'stand', k % 3, k)
    fr = post(to_np(s), T); title(fr, 'FAMILY OF FIVE', 520, T - tf, size=120, fill='FFFFFF'); return fr
def b_buy(T, t0):
    tf = wfind(6, 'firewood')
    s, c = surface()
    if T < tf:
        warm_sky(c, T, '1A1040', '3C2A6A', '6A4A9A')
        c.rectangle(240, 760, 600, 360); c.set_source_rgba(.05, .05, .08, 1); c.fill(); c.rectangle(260, 780, 560, 320); g = cairo.LinearGradient(260, 780, 820, 1100); g.add_color_stop_rgb(0, .2, .6, 1); g.add_color_stop_rgb(1, .9, .3, .7); c.set_source(g); c.fill(); glow(c, 540, 940, 500, '66AAFF', .35)
        c.set_source_rgba(.03, .03, .05, 1); c.rectangle(300, 1420, 480, 120); c.fill(); c.rectangle(400, 1340, 220, 90); c.fill()
        for wx in (380, 700): c.arc(wx, 1545, 52, 0, 6.29); c.fill()
        fr = post(to_np(s), T); chip(fr, 'TVs. TRUCKS.', CX, 470, T - t0, 'FFFFFF', 50, -2); return fr
    mountains(c, T, aur=.8); cabin(c, CX - 120, 1500, 1.1, T, True)
    fr = post(to_np(s), T); title(fr, 'FIREWOOD', 520, T - tf, size=150, fill=GOLD); chip(fr, 'TO SURVIVE WINTER', CX, 670, T - tf - .3, 'FFFFFF', 40, 2); return fr
def b_quit(T, t0): return quiet(T, t0, 'SO DID ALASKANS', 'QUIT THEIR JOBS?', 'hl', 110)
def b_nope(T, t0):
    s, c = surface(); warm_sky(c, T, '0E1A2A', '153A3A', '1F5A4A')
    tp = wfind(6, 'part-time')
    u = eout(clamp((T - t0 - .6) / 1.6))
    c.move_to(140, 1250); c.line_to(140 + 800 * u, 1250 - 6 * math.sin(u * 9)); c.set_source_rgba(*hx(GREEN)); c.set_line_width(12); c.stroke(); glow(c, 140 + 800 * u, 1250, 60, GREEN, .8)
    if T > tp:
        v = eout(clamp((T - tp) / 1.0)); c.move_to(140, 1450); c.line_to(140 + 800 * v, 1450 - 160 * v); c.set_source_rgba(*hx(GOLD)); c.stroke()
    fr = post(to_np(s), T); stamp(fr, "JOBS DIDN'T DROP", CX, 560, T - wfind(6, 'jobs'), -6, 84, '2F6B4F')
    chip(fr, 'UCHICAGO ECONOMISTS CHECKED', CX, 1130, T - t0 - .2, GREEN, 36, -2)
    if T > tp: chip(fr, 'PART-TIME WORK: +17%', CX, 1560, T - tp, GOLD, 40, 2)
    return fr
def b_stockton(T, t0):
    s, c = surface(); warm_sky(c, T, '3A1A4A', 'C8503F', 'FFB060'); glow(c, CX, 1250, 500, 'FFE08A', .7)
    city(c, T, 1300, seed=11, col=(.12, .05, .12))
    tf = wfind(1, 'full-time')
    if T > tf: bars(c, T, tf, (28, 40), (360, 720), 45, ('B8B8C4', GREEN), y=1250, h=520)
    fr = post(to_np(s), T); tape(fr, 'A CALIFORNIA CITY: $500 / MONTH', CX, 460, T - t0, col='FFFFFF', size=40, font=LUCKY, rot=-2)
    if T > tf:
        chip(fr, 'FULL-TIME JOBS', CX, 600, T - tf, GOLD, 44, 2)
        if T > tf + .8: title(fr, '28% -> 40%', 740, T - tf - .8, size=120, fill='FFFFFF')
    return fr
def b_cushion(T, t0):
    s, c = surface(); warm_sky(c, T, '2A2A6A', 'FF8A5A', 'FFE08A'); glow(c, CX, 1350, 700, 'FFF0B0', .8)
    u = clamp((T - t0) / 4)
    c.set_source_rgba(.05, .04, .08, 1); c.rectangle(0, 1450, W, 500); c.fill(); human(c, 200 + 500 * u, 1460, .9, T, 'stand', 0, 1)
    fr = post(to_np(s), T); chip(fr, "A CUSHION DOESN'T MAKE PEOPLE QUIT", CX, 470, T - t0, 'FFFFFF', 36, -2)
    t = wfind(7, 'room')
    if T > t: title(fr, 'ROOM TO FIND', 600, T - t, size=120, fill=GOLD); title(fr, 'SOMETHING BETTER', 730, T - t - .3, size=100, fill='FFFFFF')
    return fr
def b_rocketkids(T, t0):
    s, c = surface(); warm_sky(c, T); stars(c, T, 150, ymax=900)
    rocket(c, CX, 900, .7, T, .4); kids_grid(c, T, 999, y0=1150, rows=3)
    fr = post(to_np(s), T); title(fr, '72 MILLION KIDS', 470, T - t0, size=110, fill='FFFFFF'); chip(fr, '+ A PIECE OF A ROCKET COMPANY', CX, 610, T - t0 - .4, GOLD, 38, 2); return fr
def b_end(T, t0):
    tb = wfind(8, "it's what")
    if T < tb: return quiet(T, t0, "THE REAL QUESTION ISN'T", 'IF THEY GET LAZY...', 'main', 96)
    s, c = surface(); warm_sky(c, T); stars(c, T, 150, ymax=900)
    u = clamp((T - tb) / 2.5); rocket(c, CX, 1100 - 700 * u ** 2, .7, T); flash(c, CX, 1500, T, tb, .6)
    c.set_source_rgba(.03, .02, .05, 1); c.rectangle(0, 1560, W, 400); c.fill()
    for k, x in enumerate((180, 380, 600, 820)): human(c, x, 1580, .55, T, 'point', k % 3, k)
    fr = post(to_np(s), T); title(fr, "IT'S WHAT THEY'LL BUILD.", 560, T - tb, size=96, fill=GOLD); return fr

def beats():
    return [(0, b_hook), (S[1], b_stockton), (S[2], b_share), (S[3], b_lazy), (S[4], b_alaska), (S[5], b_amounts),
        (S[6], b_nope), (S[7], b_cushion), (S[8], b_end), (END, None)]
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
    for at in (wfind(1, 'to forty'), wfind(6, 'jobs'), wfind(8, "it's what")):
        a, b = shake(T, at); dx += a; dy += b
    fr = cv2.warpAffine(fr, np.float32([[z, 0, (1 - z) * CX + dx], [0, z, (1 - z) * H / 2 + dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    credit(fr, 'Illustrations. Sources: Newsweek (Oct 2026), Alaska PFD Division, AP (2022), Jones & Marinescu / UChicago, Stockton SEED via NPR.')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
