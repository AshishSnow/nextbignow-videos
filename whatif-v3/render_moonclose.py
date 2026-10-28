"""What if the Moon came 10x closer? — episode 33, first v3-look episode (painted 3D hero in varsity jacket)."""
import sys, os, math, re
import skia
from mcprops import *
from engine3 import Episode3, load_words, HERE
from cine import grade_matrix

D = os.path.join(HERE, os.environ.get('MC_DIR', 'moonclose'))
WT = load_words(D)
TOK = [(w.lower().strip("'"), a, b) for w, a, b in WT]


def ph(text, after=0.0, end=False):
    q = [x.strip("'") for x in re.findall(r"[a-zA-Z']+", text.lower())]
    for i in range(len(TOK) - len(q) + 1):
        if TOK[i][1] + 1e-6 < after: continue
        if all(TOK[i + j][0] == q[j] for j in range(len(q))):
            return TOK[i + len(q) - 1][2] if end else TOK[i][1]
    raise KeyError(text)


END = WT[-1][2] + 0.45
DURATION = END + 2.3
WHITE = (255, 255, 255)
TY1, TY2 = 400, 560          # caption rows (top)
BY1, BY2 = 1290, 1450        # caption rows (bottom)


def cap(c, t, t0, small, big, top=True, t1=None, size=170):
    y1, y2 = (TY1, TY2) if top else (BY1, BY2)
    if small: caption(c, t, t0, [(small, WHITE)], y1, size=92, t1=t1)
    if big: caption(c, t, t0 + (0.25 if small else 0), big, y2, size=size, t1=t1)


def K(t, t0, d=0.4):
    return cl((t - t0) / d)


def bg_blur(c, sigma, fn):
    blurred(c, sigma, fn)


# ================================================================== chapter 0: hook
def sc_hook(c, t, S):
    t_c = ph('came ten'); t_e = ph('to earth', end=True)
    k = eio(cl((t - t_c) / max(0.3, t_e - t_c)))
    mr = lerp(60, 300, k); my = lerp(640, 880, k)
    cam = (1.0 + 0.05 * k, 0, -20 * k)
    meadow(c, t, cam, moon_r=mr, moon_c=(540, my), mood='dusk')
    look = cl((t - 0.5) / 0.4)
    shock = k > 0.6
    pose = POSES['shock'] if shock else lerp_pose(POSES['stand'], (0, -10, 205, 15, 155, -15, 186, 0, 174, 0), look)
    face = Face('wide', 'o', 'up', look=(0, -1)) if shock else Face('open', 'smile', look=(0, -look))
    sq = 1 - 0.06 * math.exp(-max(0, t - t_c - 0.6) / 0.1) if t > t_c + 0.6 else 1.0
    layer(c, 1.0, cam, lambda: hero(c, 540, 1660, 1.32, pose, face, t, L_DUSK, squash=sq, blink=(1.2 < t < 1.3)))
    meadow_near(c, t, cam, 'dusk')


def ov_hook(c, t, S):
    caption(c, t, -0.12, [('WHAT IF THE MOON', WHITE)], TY1, size=92)
    caption(c, t, ph('came ten') - 0.05, [('CAME ', WHITE), ('10X ', YEL), ('CLOSER?', WHITE)], TY2, size=170)


def sc_beautiful(c, t, S):
    u = t - S['t0']
    bg_blur(c, 11, lambda: meadow(c, t, (1, 0, 0), moon_r=430, moon_c=(540, 760), horizon=1240, mood='dusk', blur_far=0, blur_mid=0, fire=False))
    bokeh_(c, t, 14, 21, (60, 1150, 1020, 1750), a=0.5)
    z = 1.0 + 0.04 * u
    c.save(); c.translate(540, 1000); c.scale(z, z); c.translate(-540, -1000)
    hero(c, 540, 2050, 3.5, (0, -6, 205, 15, 155, -15, 186, 0, 174, 0), Face('happy', 'smile', 'up'), t, L_CU, shadow=0)
    c.restore()


def bokeh_(c, t, n, seed, box, col=(255, 214, 150), a=0.5, rmin=18, rmax=46):
    x0, y0, x1, y1 = box
    for i in range(n):
        ph_ = hsh(i, seed) * 6.283
        x = lerp(x0, x1, hsh(i, seed + 1)) + math.sin(t * 0.4 + ph_) * 20
        y = lerp(y0, y1, hsh(i, seed + 2)) + math.cos(t * 0.3 + ph_) * 14
        r = lerp(rmin, rmax, hsh(i, seed + 3))
        k = 0.55 + 0.45 * math.sin(t * (0.8 + hsh(i, seed + 4)) + ph_)
        c.drawCircle(x, y, r, paint(shader=rad(x, y, r, [argb(col, a * k * 0.55), argb(col, a * k * 0.7), argb(col, 0)], [0, 0.85, 1]), blend=SCREEN))


def rooftop_hero(c, t, pose, face, x=230, y=1600, s=1.05, L=L_DUSK):
    roof = rrect(-60, y - 6, 620, 420, 10)
    shade(c, roof, (120, 96, 110), L, sz=200, ow=4, depth=0.3)
    c.drawRect(R.MakeXYWH(-60, y - 22, 620, 22), paint((150, 120, 130))); c.drawRect(R.MakeXYWH(-60, y - 22, 620, 22), stroke(dark((150, 120, 130)), 3))
    hero(c, x, y - 10, s, pose, face, t, L)


def floaters(c, t, wl, k):
    if k <= 0: return
    items = [(180, 'duck'), (520, 'chair'), (850, 'ball')]
    for i, (x0, kind) in enumerate(items):
        x = x0 + 40 * math.sin(t * 0.7 + i); y = wl + 8 + 8 * math.sin(t * 2 + i)
        rot = 8 * math.sin(t * 1.5 + i)
        c.save(); c.translate(x, y); c.rotate(rot)
        if kind == 'duck':
            shade(c, union(oval(0, -10, 90, 56), circ(30, -46, 26)), (255, 214, 40), L_DUSK, sz=60, ow=3)
            c.drawPath(smooth_closed([(52, -50), (76, -44), (52, -38)]), paint((255, 140, 30)))
            c.drawCircle(36, -52, 4, paint((20, 20, 20)))
        elif kind == 'chair':
            shade(c, rrect(-60, -20, 120, 18, 6), (40, 160, 220), L_DUSK, sz=18, ow=3)
            for xx in (-60, -20, 20, 60): c.drawLine(xx, -10, xx - 8, -22, stroke((240, 240, 250), 5))
        else:
            shade(c, circ(0, -26, 34), (240, 70, 70), L_DUSK, sz=68, ow=3)
            c.drawArc(R.MakeXYWH(-34, -60, 68, 68), -60, 120, False, stroke((255, 255, 255), 10))
        c.restore()


def sc_ocean(c, t, S):
    u = t - S['t0']
    wl = lerp(1420, 1050, eio(cl(u / 1.4)))
    coast(c, t, wl=wl)
    floaters(c, t, wl, 1.0)
    rooftop_hero(c, t, POSES['shock'], Face('wide', 'teeth', 'worried', look=(1, 0)))


def ov_ocean(c, t, S):
    cap(c, t, S['t0'] + 0.15, 'UNTIL YOU SEE', [('THE ', WHITE), ('OCEAN', YEL)])


def sc_happened(c, t, S):
    u = t - S['t0']
    volcano_land(c, t, erupt=1.0, early=True, moon_r=int(420 + 20 * u))


def ov_happened(c, t, S):
    cap(c, t, ph('it already'), 'IT ALREADY', [('HAPPENED', YEL)])


# ================================================================== chapter 1: the mirror
def sc_apollo(c, t, S):
    u = t - S['t0']
    cam = (1.0 + 0.04 * u, 0, 0)
    lunar_surface(c, t, cam=cam, earth_pos=(830, 780), earth_r=110)
    layer(c, 1.0, cam, lambda: mirror_panel(c, 560, 1560, 1.5, t))


def ov_apollo(c, t, S):
    pill(c, t, S['t0'] + 0.2, 'JULY 1969', 540, 345, col=(40, 44, 60), size=46)
    caption(c, t, ph('apollo'), [('APOLLO ', WHITE), ('11', YEL)], 500, size=150)
    cap(c, t, ph('a panel of'), None, [('A PANEL OF ', WHITE), ('MIRRORS', YEL)], top=False)


def sc_lasers(c, t, S):
    tb = ph('fire lasers') + 0.15
    observatory(c, t, beam=cl((t - tb) / 0.35), moon_pos=(820, 520), moon_r=80)


def ov_lasers(c, t, S):
    cap(c, t, ph('fire lasers'), 'SCIENTISTS FIRE', [('LASERS ', GRN), ('AT IT', WHITE)])


def space_pair(c, t, ex=250, mx=860, y=1050, er=170, mr=48, laser=0.0, rewind=0.0):
    space_bg(c, t, seed=6)
    earth(c, ex, y, er, rot=t * 0.06)
    if laser > 0:
        f = 0.6 + 0.4 * math.sin(t * 30)
        c.drawLine(ex + er * 0.9, y, mx - mr, y, paint(GRN, 0.3 * laser * f, stroke=18, blur=8, blend=PLUS))
        c.drawLine(ex + er * 0.9, y, mx - mr, y, paint((210, 255, 220), 0.9 * laser * f, stroke=3, blend=PLUS))
    moon_ball(c, mx, y, mr, light=(-0.75, -0.2, 0.62), glow=0.25)


def sc_drift(c, t, S):
    td = ph('drifting away')
    k = eio(cl((t - td) / 1.6))
    mx = lerp(840, 900, k)
    space_pair(c, t, mx=mx, laser=1.0 if t < td else 0.0)
    if t > td:
        for i in range(4):
            x = mx - 70 - i * 26
            c.drawCircle(x, 1050, 44 - i * 6, stroke((255, 255, 255), 2, 0.25 * (1 - i / 4) * k))
        arrow_x = mx + 70
        c.drawLine(arrow_x, 1050, arrow_x + 80, 1050, stroke(YEL, 8, k)); c.drawPath(poly([(arrow_x + 100, 1050), (arrow_x + 74, 1034), (arrow_x + 74, 1066)], True), paint(YEL, k))
    dashed_line(c, 430, 1150, mx - 20, 1150, (255, 255, 255), 3, 0.5, phase=-t * 20)


def ov_drift(c, t, S):
    dist_pill(c, 640, 1230, '384,400 KM', a=K(t, S['t0'] + 0.3))
    cap(c, t, ph('drifting away'), None, [('DRIFTING ', WHITE), ('AWAY', YEL)])
    caption(c, t, ph('about four'), [('~4 CM ', YEL), ('EVERY YEAR', WHITE)], TY1 + 330, size=96)


def sc_rewind(c, t, S):
    u = t - S['t0']
    tk = ph('bring the moon', after=S['t0'])
    k = eio(cl((t - tk) / 1.6))
    mx = lerp(900, 520, k)
    space_pair(c, t, mx=mx, mr=lerp(48, 70, k))
    if t < tk + 0.2:
        # VHS rewind look
        for i in range(14):
            y = (i * 140 + t * 900) % H
            c.drawRect(R.MakeXYWH(0, y, W, 6), paint((255, 255, 255), 0.12))
        c.drawRect(FULLR, paint((40, 80, 160), 0.12, blend=SCREEN))


def ov_rewind(c, t, S):
    u = t - S['t0']
    tk = ph('bring the moon', after=S['t0'])
    if t < tk + 0.2:
        a = 0.6 + 0.4 * math.sin(t * 12)
        for i, x in enumerate((470, 540)):
            c.drawPath(poly([(x + 40, 330), (x - 20, 370), (x + 40, 410)], True), paint(WHITE, a))
        f = font('ant', 60); c.drawString('REWIND', 620, 395, f, paint(WHITE, a))
    k = eio(cl((t - tk) / 1.6))
    km = int(lerp(384400, 38440, k) / 10) * 10
    dist_pill(c, 540, 1230, '{:,} KM'.format(km), a=K(t, tk - 0.2))
    cap(c, t, ph('ten times closer', after=S['t0']), None, [('10X ', YEL), ('CLOSER', WHITE)])


# ================================================================== chapter 2: the view
def sc_wider(c, t, S):
    tw = ph('ten times wider')
    k = eio(cl((t - tw) / 0.9))
    meadow(c, t, (1, 0, 0), moon_r=lerp(38, 380, k), moon_c=(540, lerp(560, 760, k)), mood='night', shine=0.2 * k)
    hero(c, 540, 1680, 1.25, (0, -12, 205, 15, 155, -15, 186, 0, 174, 0), Face('wide' if k > 0.5 else 'open', 'o' if k > 0.5 else 'smile', 'up', look=(0, -1)), t, L_NIGHT)
    meadow_near(c, t, (1, 0, 0), 'night')


def ov_wider(c, t, S):
    cap(c, t, ph('ten times wider'), None, [('10X ', YEL), ('WIDER', WHITE)])


def sc_bright(c, t, S):
    tb = ph('a hundred')
    k = eio(cl((t - tb) / 0.8))
    meadow(c, t, (1, 0, 0), moon_r=380, moon_c=(540, 820), mood='night', shine=0.2 + 0.8 * k, moon_a=1.0)
    # the 10 x 10 grid of 'small moons' that fit across the big one
    g = cl((t - S['t0'] - 0.3) / 0.6) * (1 - k * 0.6)
    if g > 0:
        cx, cy, r = 540, 820, 380
        c.save(); p = skia.Path(); p.addCircle(cx, cy, r); c.clipPath(p, doAntiAlias=True)
        for i in range(10):
            for j in range(10):
                x = cx - r + (i + 0.5) * r * 0.2; y = cy - r + (j + 0.5) * r * 0.2
                c.drawCircle(x, y, r * 0.09, stroke((40, 60, 120), 3, 0.7 * g))
        c.restore()
    c.drawRect(FULLR, paint((200, 220, 255), 0.18 * k, blend=SCREEN))


def ov_bright(c, t, S):
    caption(c, t, S['t0'] + 0.3, [('10 X 10 = ', WHITE), ('100', YEL)], TY1 + 20, size=110, t1=ph('a hundred') - 0.1)
    cap(c, t, ph('a hundred'), None, [('100X ', YEL), ('BRIGHTER', WHITE)], top=False)


def sc_never(c, t, S):
    u = t - S['t0']
    on = cl((t - ph('never really') - 0.2) / 0.3)
    meadow(c, t, (1, 0, 0), moon_r=360, moon_c=(540, 640), mood='bright', shine=1.0, fire=False)
    pose = lerp_pose(POSES['stand'], (0, -2, 200, 10, 140, -150, 186, 0, 174, 0), cl(on * 3) * (1 - cl((on - 0.5) * 3)))
    hero(c, 540, 1680, 1.3, pose, Face('open', 'smile' if on < 0.6 else 'grin', 'none'), t, L_BRIGHT, acc='shades' if on > 0.5 else None)
    meadow_near(c, t, (1, 0, 0), 'night')


def ov_never(c, t, S):
    pill(c, t, S['t0'] + 0.15, '12:00 AM', 540, 345, col=(40, 44, 60), size=50)
    cap(c, t, ph('never really'), None, [('NEVER ', WHITE), ('DARK', YEL)])


def sc_sleep(c, t, S):
    tc = ph('trying to sleep')
    bedroom(c, t, shine=1.0, cover=cl((t - tc) / 0.5), face=Face('open', 'flat', 'angry'))


def ov_sleep(c, t, S):
    cap(c, t, ph('a free nightlight'), 'A FREE', [('NIGHTLIGHT', YEL)], t1=ph('and terrible') - 0.1)
    cap(c, t, ph('and terrible'), 'GOOD LUCK', [('SLEEPING', YEL)])


# ================================================================== chapter 3: tides
def sc_tides(c, t, S):
    u = t - S['t0']
    space_bg(c, t, seed=11)
    bul = 0.10 + 0.04 * math.sin(t * 2)
    moon_ball(c, 540, 330, 70, light=(-0.6, 0.3, 0.75), glow=0.3)
    earth(c, 540, 1180, 300, rot=t * 0.05, bulge=bul * cl((t - ph('makes tides')) / 0.5) + 0.0001, bulge_dir=90)
    for i in range(3):
        y = 760 - i * 60 - (t * 80 % 60)
        c.drawPath(poly([(540, y - 30), (510, y + 10), (570, y + 10)], True), paint(YEL, 0.7 - i * 0.2))


def ov_tides(c, t, S):
    cap(c, t, ph("the moon's pull"), "THE MOON'S PULL", [('= ', WHITE), ('TIDES', CYAN)], top=False)


def sc_thousand(c, t, S):
    space_bg(c, t, seed=12, neb=((200, 60, 80), (60, 40, 160)), na=0.3)
    moon_ball(c, 540, 420, 120, light=(-0.5, 0.2, 0.84), glow=0.5)
    earth(c, 540, 1500, 360, rot=t * 0.05, bulge=0.06 + 0.4 * eio(cl((t - ph('a thousand times')) / 0.6)), bulge_dir=90)


def ov_thousand(c, t, S):
    t1 = ph("doesn't get ten")
    t2 = ph('a thousand times')
    def card(cc):
        f = font('ant', 110)
        s1 = '10 X 10 X 10'
        cc.drawString(s1, -f.measureText(s1) / 2, -10, f, paint(WHITE))
        f2 = font('ant', 70); s2 = 'NOT 10X...'
        cc.drawString(s2, -f2.measureText(s2) / 2, 90, f2, paint((255, 120, 110), K(t, t1, 0.2)))
    glass_card(c, 540, 900, 760, 270, card, k=K(t, S['t0'] + 0.3, 0.4) * (1 - K(t, t2 - 0.1, 0.15)))
    caption(c, t, ph('ten times closer', after=S['t0']), [('10X ', YEL), ('CLOSER', WHITE)], TY2 - 120, size=120, t1=t2 - 0.1)
    if t > t2 - 0.05:
        caption(c, t, t2 - 0.05, [('1000X', YEL)], 820, size=300)
        caption(c, t, t2 + 0.3, [('STRONGER', WHITE)], 960, size=150)


def sc_flood(c, t, S):
    tr = ph('the sea would'); tc = ph('coastal cities', end=True); tp = ph('pull back out')
    up = eio(cl((t - tr) / max(0.5, tc - tr)))
    down = eio(cl((t - tp) / 1.2))
    wl = lerp(1420, 820, up * (1 - down))
    coast(c, t, wl=wl)
    floaters(c, t, wl, up)
    rooftop_hero(c, t, POSES['shock'] if up > 0.3 else POSES['stand'],
                 Face('wide', 'teeth', 'worried', look=(1, -0.3)) if up > 0.3 else Face('open', 'smile', look=(1, 0)))


def ov_flood(c, t, S):
    pill(c, t, S['t0'] + 0.15, 'TWICE A DAY', 540, 345, col=RED, size=52)
    cap(c, t, ph('coastal cities') - 0.2, None, [('OVER ', WHITE), ('COASTAL CITIES', YEL)], t1=ph('pull back out') + 0.4)


def sc_sub(c, t, S):
    def h(): hero(c, 540, 1560, 1.25, POSES['sit'], Face('open', 'flat', 'none', look=(-1, 0)), t, L_WATER, acc='snorkel', blink=(abs((t % 3) - 1.5) < 0.06))
    house_under(c, t, hero_fn=h)


def ov_sub(c, t, S):
    cap(c, t, S['t0'] + 0.1, None, [('BEACH HOUSE?', WHITE)], t1=ph('submarine') - 0.15)
    cap(c, t, ph('submarine') - 0.1, 'MORE LIKE A', [('SUBMARINE', YEL)])


# ================================================================== chapter 4: the ground
def sc_ground(c, t, S):
    tf = ph("you just can't")
    def h(gy):
        pose = POSES['shrug'] if t > tf else POSES['stand']
        hero(c, 540, gy + 12, 1.2, pose, Face('happy' if t > tf else 'open', 'smile', 'up' if t > tf else 'none'), t, L_DUSK)
    ground_section(c, t, k=0.0, hero_fn=h)


def ov_ground(c, t, S):
    tc = ph('twenty centimeters')
    gy = 1180 - 9 * math.sin(t * 1.2)
    ruler(c, 930, gy - 150, gy + 50, '20 CM', a=K(t, tc - 0.1, 0.25))
    cap(c, t, ph('rises and falls'), 'THE GROUND', [('RISES ', YEL), ('& FALLS', WHITE)], t1=ph("you just can't") - 0.1)
    cap(c, t, ph("you just can't"), "YOU JUST CAN'T", [('FEEL IT', YEL)])


def sc_squeeze(c, t, S):
    ts = ph('squeezed like')
    sq = eio(cl((t - ts) / 0.5)) * (0.85 + 0.15 * math.sin(t * 6))
    earth_squeeze(c, t, sq=sq, crack=cl((t - ts - 0.4) / 0.5))


def ov_squeeze(c, t, S):
    caption(c, t, S['t0'] + 0.15, [('1000X ', YEL), ('STRONGER', WHITE)], TY2 - 120, size=110, t1=ph('squeezed like') - 0.1)
    cap(c, t, ph('squeezed like'), 'SQUEEZED LIKE A', [('STRESS BALL', YEL)], top=False)


def sc_quake(c, t, S):
    tv = ph('more volcanoes')
    er = cl((t - tv) / 0.4)
    def h():
        wob = math.sin(t * 14) * 10
        hero(c, 300, 1500, 1.15, (wob, -4, 240, 60, 120, -60, 196, 6, 164, -6), Face('wide', 'teeth', 'worried'), t, L_LAVA, sweat=1.0)
    volcano_land(c, t, erupt=er, quake=1.0, early=False, hero_fn=h)


def ov_quake(c, t, S):
    cap(c, t, ph('more earthquakes'), 'MORE', [('EARTHQUAKES', YEL)], t1=ph('more volcanoes') - 0.1)
    cap(c, t, ph('more volcanoes'), 'MORE', [('VOLCANOES', (255, 120, 60))])


def sc_io(c, t, S):
    u = t - S['t0']
    z = 1 + 0.05 * u
    c.save(); c.translate(470, 1160); c.scale(z, z); c.translate(-470, -1160)
    jupiter_io(c, t, plume=1.0)
    c.restore()


def ov_io(c, t, S):
    pill(c, t, ph('moon io') + 0.1, "JUPITER'S MOON IO", 540, 345, col=(40, 44, 60), size=46)
    cap(c, t, ph('most volcanic'), 'THE MOST', [('VOLCANIC ', (255, 140, 60)), ('WORLD', WHITE)], top=False)


# ================================================================== chapter 5: the Roche limit
def sc_roche(c, t, S):
    u = t - S['t0']
    tr = ph('rip the moon'); tp = ph('the pieces would'); tl = ph('twenty thousand')
    space_bg(c, t, seed=17)
    d = lerp(780, 450, eio(cl(u / max(0.5, tr - S['t0']))))
    stretch = cl((t - tr + 0.5) / 0.5)
    shatter = cl((t - tr) / 0.25)
    ring = eio(cl((t - tp) / 2.4))
    roche(c, t, moon_d=d, stretch=stretch, shatter=shatter, ring=ring, moon_ang=-0.95, show_limit=K(t, tl - 0.1, 0.4) * (1 - ring))


def ov_roche(c, t, S):
    tl = ph('twenty thousand')
    dist_pill(c, 540, 1660, 'ROCHE LIMIT: ~20,000 KM', a=K(t, tl - 0.1) * (1 - K(t, ph('the pieces would'), 0.3)), col=(120, 30, 40))
    cap(c, t, ph('rip the moon'), 'GRAVITY WOULD', [('RIP IT APART', (255, 120, 110))], t1=ph('the pieces would') - 0.1)
    cap(c, t, ph('a giant ring') - 0.1, 'A GIANT', [('RING', YEL)])


def sc_ringsky(c, t, S):
    u = t - S['t0']
    meadow(c, t, (1.0 + 0.03 * u, 0, 0), mood='dusk', ring=cl(u / 0.6), moon_a=0.0)
    hero(c, 540, 1660, 1.3, (0, -12, 230, 40, 130, -40, 186, 0, 174, 0), Face('wide', 'grin', 'up', look=(0, -1)), t, L_DUSK)
    meadow_near(c, t, (1, 0, 0), 'dusk')


def ov_ringsky(c, t, S):
    cap(c, t, S['t0'] + 0.1, 'LIKE', [("SATURN'S", YEL)])


def sc_phobos(c, t, S):
    u = t - S['t0']
    tr = ph('become a ring')
    space_bg(c, t, seed=19, neb=((180, 70, 50), (60, 40, 130)), na=0.3)
    ring = eio(cl((t - tr) / 1.6))
    if ring <= 0:
        draw_planet(c, 'mars', 540, 1150, 260, rot=t * 0.05, glow=(255, 160, 120), halo=(255, 140, 100), light=(-0.65, -0.3, 0.70))
        a = -0.9 + u * 0.35
        rr = lerp(560, 430, cl(u / 6))
        # spiral path hint
        p = skia.Path()
        for i in range(60):
            aa = a - i * 0.1; r_ = rr + i * 3
            (p.moveTo if i == 0 else p.lineTo)(540 + math.cos(aa) * r_, 1150 + math.sin(aa) * r_ * 0.45)
        pp = stroke((255, 255, 255), 3, 0.4); pp.setPathEffect(skia.DashPathEffect.Make([10, 10], -t * 20)); c.drawPath(p, pp)
        phobos(c, 540 + math.cos(a) * rr, 1150 + math.sin(a) * rr * 0.45, 1.0, t, rot=t * 20)
    else:
        roche(c, t, cx=540, cy=1150, er=260, moon_d=430, shatter=1.0, ring=ring, moon_ang=-0.9 + (tr - S['t0']) * 0.35, tilt=0.3, show_limit=0, planet='mars')


def ov_phobos(c, t, S):
    pill(c, t, ph('phobos') - 0.1, "MARS'S MOON PHOBOS", 540, 345, col=(120, 50, 40), size=46)
    caption(c, t, ph('creeping closer'), [('~2 M CLOSER ', YEL), ('EVERY CENTURY', WHITE)], TY1 + 160, size=90, t1=ph('become a ring') - 0.2)
    cap(c, t, ph('become a ring'), 'IN TENS OF MILLIONS OF YEARS', [('A RING', YEL)])


# ================================================================== chapter 6: it already happened
def sc_yes(c, t, S):
    ty = ph('yes')
    bg_blur(c, 11, lambda: meadow(c, t, (1, 0, 0), moon_r=300, moon_c=(540, 760), horizon=1240, mood='night', blur_far=0, blur_mid=0, fire=False))
    k = cl((t - ty) / 0.25)
    if k <= 0:
        pose = (0, 8, 205, 15, 165, -160, 186, 0, 174, 0); face = Face('open', 'flat', 'worried', look=(-1, -1))
        hands = ('relaxed', 'fist')
    else:
        pose = lerp_pose((0, 0, 200, 10, 160, -10, 186, 0, 174, 0), POSES['arms_up'], eback(k)); face = Face('happy', 'grin', 'up')
        hands = ('open', 'open')
    jump = -60 * math.sin(math.pi * cl((t - ty) / 0.45)) if k > 0 else 0
    hero(c, 540, 2030 + jump, 3.3, pose, face, t, L_CU, shadow=0, hands=hands)


def ov_yes(c, t, S):
    cap(c, t, S['t0'] + 0.1, 'DID IT EVER', [('HAPPEN?', WHITE)], t1=ph('yes') - 0.1)
    caption(c, t, ph('yes'), [('YES!', YEL)], TY2, size=260)


def sc_born(c, t, S):
    u = t - S['t0']
    volcano_land(c, t, erupt=1.0, early=True, moon_r=int(430 + 15 * u))


def ov_born(c, t, S):
    pill(c, t, S['t0'] + 0.15, '4.5 BILLION YEARS AGO', 540, 345, col=(120, 40, 30), size=46)
    cap(c, t, ph('way closer'), None, [('WAY ', WHITE), ('CLOSER', YEL)], top=False, t1=ph('enormous') - 0.1)
    cap(c, t, ph('enormous'), None, [('ENORMOUS', YEL)], top=False)


def sc_day18(c, t, S):
    space_bg(c, t, seed=23)
    earth(c, 540, 1500, 330, rot=t * 0.9)
    clock18(c, t, 540, 860, 270, spin=2.5)


def ov_day18(c, t, S):
    pill(c, t, S['t0'] + 0.15, '1.4 BILLION YEARS AGO', 540, 345, col=(40, 44, 60), size=46)
    cap(c, t, ph('eighteen hours'), '1 DAY =', [('18 HOURS', YEL)], top=False)


def sc_sneak(c, t, S):
    u = t - S['t0']
    space_bg(c, t, seed=29)
    earth(c, 220, 1100, 200, rot=t * 0.06)
    x = 640 + 70 * u; y = 1060 - 20 * abs(math.sin(u * 5))
    sneaky_moon(c, x, y, 110, t, look=-1.0)
    for i in range(3):
        fx = x - 140 - i * 60; c.drawOval(R.MakeXYWH(fx - 14, 1190, 28, 12), paint((255, 255, 255), 0.25 - i * 0.07))


def ov_sneak(c, t, S):
    cap(c, t, ph('sneaking away'), "IT'S BEEN", [('SNEAKING AWAY', YEL)])


def sc_nail(c, t, S):
    u = t - S['t0']
    fingernail(c, t, grow=cl(u / 2.5))


def ov_nail(c, t, S):
    u = t - S['t0']
    gy = 1900 - 880 - cl(u / 2.5) * 70
    ruler(c, 800, gy, 1900 - 880 + 40, '', a=K(t, S['t0'] + 0.2))
    cap(c, t, ph('fingernails') - 0.1, '~3.8 CM A YEAR', [('LIKE ', WHITE), ('FINGERNAILS', YEL)])


# ================================================================== ending
def sc_thanks(c, t, S):
    meadow(c, t, (1, 0, 0), moon_r=70, moon_c=(540, 560), mood='night', fire=True)
    hero(c, 540, 1660, 1.3, POSES['wave'], Face('happy', 'grin', 'up', look=(0, -1)), t, L_NIGHT, hands=('relaxed', 'open'))
    meadow_near(c, t, (1, 0, 0), 'night')


def ov_thanks(c, t, S):
    cap(c, t, ph('the perfect distance') - 0.1, 'AT THE', [('PERFECT DISTANCE', YEL)])


def sc_ask(c, t, S):
    u = t - S['t0']
    bg_blur(c, 10, lambda: meadow(c, t, (1, 0, 0), moon_r=300, moon_c=(540, 760), horizon=1240, mood='dusk', blur_far=0, blur_mid=0, fire=False))
    bokeh_(c, t, 12, 31, (60, 1150, 1020, 1750), a=0.5)
    wv = 12 * math.sin(t * 7)
    hero(c, 540, 2050, 3.4, (0, 4, 205, 15, 130 + wv, -70, 186, 0, 174, 0), Face('happy', 'grin', 'up'), t, L_CU, shadow=0, hands=('relaxed', 'open'))
    if t > END:
        k = eio(cl((t - END) / 1.2))
        c.drawRect(FULLR, paint((10, 6, 20), 0.85 * k))
        moon_ball(c, 540, 880, lerp(40, 300, k), light=(-0.2, -0.2, 0.95), glow=0.6 * k, a=k)


def ov_ask(c, t, S):
    cap(c, t, S['t0'] + 0.1, 'WHAT SHOULD I', [('BRING CLOSER', YEL), (' NEXT?', WHITE)], t1=END)


G_SPACE = grade_matrix(sat=1.18, contrast=1.12, gain=(0.98, 1.0, 1.04), lift=(-0.004, 0.0, 0.02))
G_LAVA = grade_matrix(sat=1.2, contrast=1.12, gain=(1.06, 0.98, 0.92), lift=(0.01, 0.0, -0.004))
G_WATER = grade_matrix(sat=1.15, contrast=1.1, gain=(0.95, 1.02, 1.04), lift=(-0.01, 0.01, 0.02))

SCENES = [
    dict(k='hook', t0=0.0, fn=sc_hook, ov=ov_hook),
    dict(k='beautiful', t0=ph('it sounds beautiful') - 0.2, fn=sc_beautiful, tin='punch'),
    dict(k='ocean', t0=ph('until you see') - 0.15, fn=sc_ocean, ov=ov_ocean, tin='whip'),
    dict(k='happened', t0=ph('and the craziest') - 0.2, fn=sc_happened, ov=ov_happened, tin='flash', grade=G_LAVA),
    dict(k='apollo', t0=ph('in nineteen') - 0.2, fn=sc_apollo, ov=ov_apollo, tin='dip', grade=G_SPACE),
    dict(k='lasers', t0=ph('scientists still') - 0.2, fn=sc_lasers, ov=ov_lasers, tin='whip', grade=G_SPACE),
    dict(k='drift', t0=ph('and it showed') - 0.2, fn=sc_drift, ov=ov_drift, tin='punch', grade=G_SPACE),
    dict(k='rewind', t0=ph("so let's run") - 0.2, fn=sc_rewind, ov=ov_rewind, tin='flash', grade=G_SPACE),
    dict(k='wider', t0=ph('first the view') - 0.2, fn=sc_wider, ov=ov_wider, tin='dip'),
    dict(k='bright', t0=ph('and a full moon') - 0.2, fn=sc_bright, ov=ov_bright, tin='punch'),
    dict(k='never', t0=ph('nights would never') - 0.2, fn=sc_never, ov=ov_never, tin='whip'),
    dict(k='sleep', t0=ph('a free nightlight') - 0.2, fn=sc_sleep, ov=ov_sleep, tin='whip'),
    dict(k='tides', t0=ph("but here's the problem") - 0.2, fn=sc_tides, ov=ov_tides, tin='punch', grade=G_SPACE),
    dict(k='thousand', t0=ph('bring the moon ten', after=ph("but here's the problem")) - 0.2, fn=sc_thousand, ov=ov_thousand, tin='punch', grade=G_SPACE),
    dict(k='flood', t0=ph('twice a day') - 0.2, fn=sc_flood, ov=ov_flood, tin='whip'),
    dict(k='sub', t0=ph('beach house') - 0.2, fn=sc_sub, ov=ov_sub, tin='punch', grade=G_WATER),
    dict(k='ground', t0=ph("and it's not just") - 0.2, fn=sc_ground, ov=ov_ground, tin='dip'),
    dict(k='squeeze', t0=ph('make that a thousand') - 0.2, fn=sc_squeeze, ov=ov_squeeze, tin='punch', grade=G_SPACE),
    dict(k='quake', t0=ph('more earthquakes') - 0.2, fn=sc_quake, ov=ov_quake, tin='flash', grade=G_LAVA),
    dict(k='io', t0=ph("that's exactly what") - 0.2, fn=sc_io, ov=ov_io, tin='whip', grade=G_SPACE),
    dict(k='roche', t0=ph('now bring the moon') - 0.2, fn=sc_roche, ov=ov_roche, tin='dip', grade=G_SPACE),
    dict(k='ringsky', t0=ph("like saturn's") - 0.25, fn=sc_ringsky, ov=ov_ringsky, tin='punch'),
    dict(k='phobos', t0=ph("and that's not science") - 0.2, fn=sc_phobos, ov=ov_phobos, tin='whip', grade=G_SPACE),
    dict(k='yes', t0=ph('so did a close') - 0.2, fn=sc_yes, ov=ov_yes, tin='dip'),
    dict(k='born', t0=ph('when the moon was born') - 0.2, fn=sc_born, ov=ov_born, tin='flash', grade=G_LAVA),
    dict(k='day18', t0=ph('and one point four') - 0.2, fn=sc_day18, ov=ov_day18, tin='whip', grade=G_SPACE),
    dict(k='sneak', t0=ph('since then') - 0.2, fn=sc_sneak, ov=ov_sneak, tin='punch', grade=G_SPACE),
    dict(k='nail', t0=ph('about as fast') - 0.2, fn=sc_nail, ov=ov_nail, tin='punch'),
    dict(k='thanks', t0=ph('so next time') - 0.2, fn=sc_thanks, ov=ov_thanks, tin='dip'),
    dict(k='ask', t0=ph('what should i') - 0.2, fn=sc_ask, ov=ov_ask, tin='punch'),
]
EP = Episode3(D, SCENES, DURATION, END)
EP.shk(ph('came ten') + 0.5, 12, 0.35)
EP.shk(ph('a thousand times'), 16, 0.3)
EP.shk(ph('rip the moon'), 22, 0.35); EP.flash(ph('rip the moon') + 0.05, 0.6, 0.2)
EP.shk(ph('squeezed like') + 0.3, 10, 0.3)
EP.shk(ph('more earthquakes'), 14, 0.6)
EP.shk(ph('more volcanoes'), 18, 0.4); EP.flash(ph('more volcanoes'), 0.4, 0.15, (255, 160, 80))
EP.shk(ph('yes') + 0.05, 10, 0.25)

if __name__ == '__main__':
    EP.main(sys.argv)
