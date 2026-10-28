"""Props + sets for episode 33, 'What if the Moon came 10x closer?' (first v3-look episode, varsity hero)."""
import math
import numpy as np
import skia
from hero import *
from cine import *
from gfx import SCREEN, PLUS, glow_disc

OUTFIT = 'varsity'
YEL = (255, 214, 10); RED = (226, 40, 52); CYAN = (90, 220, 255); GRN = (80, 255, 120)
_C = {}

# ------------------------------------------------------------------ lights
L_DUSK = Light(key=(-0.45, -0.9), key_col=(255, 226, 196), ka=0.24, tint=(168, 150, 206), sa=0.95,
               rim=(-0.6, -0.8), rim_col=(200, 220, 255), ra=0.9, ground=(14, 10, 24), ga=0.6, amb=(0.88, 0.86, 0.95))
L_CU = Light(key=(-0.55, -0.75), key_col=(255, 226, 200), ka=0.26, tint=(170, 148, 204), sa=0.95,
             rim=(0.35, -1.0), rim_col=(255, 232, 210), ra=1.0, ground=(14, 10, 24), ga=0.0, amb=(0.92, 0.9, 0.97))
L_NIGHT = Light(key=(-0.5, -0.85), key_col=(220, 232, 255), ka=0.22, tint=(140, 150, 210), sa=1.0,
                rim=(0.2, -1.0), rim_col=(210, 230, 255), ra=1.1, ground=(6, 8, 24), ga=0.6, amb=(0.80, 0.84, 0.98))
L_BRIGHT = Light(key=(-0.3, -0.95), key_col=(240, 246, 255), ka=0.3, tint=(176, 186, 226), sa=0.9,
                 rim=(0.2, -1.0), rim_col=(230, 240, 255), ra=1.0, ground=(10, 14, 34), ga=0.55, amb=(0.98, 0.99, 1.04))
L_DAY = Light(key=(-0.55, -0.8), key_col=(255, 246, 228), ka=0.26, tint=(190, 176, 210), sa=0.9,
              rim=(0.8, -0.5), rim_col=(255, 230, 190), ra=0.6, ground=(30, 30, 50), ga=0.5, amb=None)
L_LAVA = Light(key=(0.6, 0.4), key_col=(255, 150, 80), ka=0.35, tint=(150, 100, 120), sa=1.0,
               rim=(-0.8, -0.4), rim_col=(255, 120, 60), ra=1.2, ground=(20, 6, 6), ga=0.6, amb=(0.92, 0.8, 0.78))
L_WATER = Light(key=(0.6, -0.7), key_col=(170, 255, 240), ka=0.28, tint=(120, 170, 200), sa=1.0,
                rim=(0.9, -0.3), rim_col=(120, 230, 255), ra=0.9, ground=(0, 20, 30), ga=0.5, amb=(0.82, 0.95, 1.0))
L_ROOM = Light(key=(0.7, -0.6), key_col=(220, 232, 255), ka=0.3, tint=(130, 130, 200), sa=1.0,
               rim=(0.9, -0.4), rim_col=(200, 225, 255), ra=1.1, ground=(6, 8, 24), ga=0.6, amb=(0.75, 0.8, 0.98))


def hero(c, x, y, s, pose, face, t, L, **kw):
    return draw_hero(c, x, y, s, pose, face, outfit=OUTFIT, L=L, t=t, **kw)


def layer(c, d, cam, fn):
    z, px, py = cam
    zz = 1 + (z - 1) * d
    c.save(); c.translate(W / 2, H / 2); c.scale(zz, zz); c.translate(-W / 2 - px * d, -H / 2 - py * d)
    r = fn(); c.restore(); return r


# ------------------------------------------------------------------ meadow (dusk / night / bright night)
SKIES = {
    'dusk': [(0.0, (18, 28, 66)), (0.30, (52, 50, 104)), (0.52, (132, 82, 122)), (0.66, (226, 120, 96)), (0.74, (255, 170, 104)), (1.0, (255, 196, 128))],
    'night': [(0.0, (6, 10, 30)), (0.4, (16, 28, 70)), (0.75, (40, 62, 120)), (1.0, (70, 96, 150))],
    'bright': [(0.0, (30, 54, 120)), (0.4, (60, 98, 170)), (0.75, (110, 150, 210)), (1.0, (160, 190, 230))],
}
TREES = {
    'dusk': [((150, 112, 150), (196, 130, 140), (255, 200, 170), (255, 170, 136)), ((92, 84, 120), (104, 86, 116), (230, 220, 255), (226, 156, 156)),
             ((48, 58, 78), (34, 40, 54), (210, 222, 255), (190, 140, 160))],
    'night': [((40, 56, 100), (52, 66, 110), (180, 200, 255), (70, 96, 150)), ((24, 36, 70), (26, 38, 70), (190, 210, 255), (50, 70, 120)),
              ((12, 20, 42), (10, 16, 34), (200, 220, 255), (40, 56, 100))],
    'bright': [((80, 110, 160), (100, 128, 176), (230, 240, 255), (150, 180, 220)), ((48, 76, 120), (54, 80, 120), (230, 240, 255), (120, 150, 200)),
               ((24, 44, 70), (20, 36, 58), (230, 240, 255), (90, 120, 170))],
}
FIELD = {'dusk': ((98, 104, 86), (20, 34, 26)), 'night': ((40, 60, 70), (8, 18, 20)), 'bright': ((90, 120, 110), (22, 44, 38))}

GR_WIDE = Grass(1178, H + 60, n=2200, seed=5, h_near=210, h_far=10, cols=((26, 60, 40), (78, 132, 66)), tip=(255, 206, 150))
GR_NIGHT = Grass(1178, H + 60, n=2200, seed=5, h_near=210, h_far=10, cols=((16, 40, 40), (46, 90, 70)), tip=(190, 220, 255))
GR_LOW = Grass(1440, H + 160, n=3200, seed=9, h_near=480, h_far=24, cols=((22, 62, 38), (80, 136, 62)), tip=(255, 206, 150))


def meadow(c, t, cam=(1, 0, 0), moon_r=250, moon_c=(540, 880), horizon=1060, mood='dusk', blur_far=2.0, blur_mid=1.0,
           grass=None, wind=1.0, gust=0.0, moon_warm=0.12, ring=0.0, moon_a=1.0, shine=0.0, stars_a=0.7, fire=True):
    mx, my = moon_c
    grass = grass or (GR_WIDE if mood == 'dusk' else GR_NIGHT)
    def sky():
        vgrad(c, SKIES[mood], -200, horizon + 140)
        stars(c, 4, 760, 110, stars_a * (1 - 0.7 * shine), t)
        if mood == 'dusk':
            cloud_streaks(c, t, 2, 300, 760, (70, 58, 110), 0.5, n=6, drift=8, lit=(255, 150, 120))
        else:
            cloud_streaks(c, t, 2, 300, 760, (30, 44, 90), 0.5, n=5, drift=8, lit=(170, 200, 255))
    layer(c, 0.05, cam, sky)
    if ring > 0:
        layer(c, 0.08, cam, lambda: sky_ring(c, t, ring, mood))
    if moon_a > 0:
        def moon():
            if moon_a < 1: c.saveLayerAlpha(None, int(255 * moon_a))
            if mood == 'dusk':
                draw_moon(c, mx, my, moon_r, glow=(255, 226, 206), ga=0.75, warm=moon_warm, low_haze=(255, 168, 120), lha=0.55)
            else:
                draw_moon(c, mx, my, moon_r, glow=(210, 228, 255), ga=0.8 + 0.6 * shine, warm=0.0, low_haze=(150, 170, 220), lha=0.25)
                if shine > 0:
                    sun_glow(c, mx, my, moon_r * 4.5, (200, 220, 255), 0.35 * shine)
            cloud_streaks(c, t, 8, my - moon_r * 0.1, my + moon_r * 0.7, (96, 64, 112) if mood == 'dusk' else (40, 56, 100), 0.5, n=3, drift=14,
                          lit=(255, 170, 130) if mood == 'dusk' else (170, 200, 255))
            if moon_a < 1: c.restore()
        layer(c, 0.12, cam, moon)
    rim = ((mx - W / 2) / 1000, -1)
    T = TREES[mood]
    def row(i, key, y_off, seed, h, sp, con, tall=0.12, bl=1.0):
        top, bot, rc, hz = T[i]
        p = _C.setdefault((key, horizon), crown_row_path(horizon + y_off, seed, h=h, spacing=sp, conifer=con, tall=tall))
        rim_fill(c, p, top, bot, horizon - 70 + y_off - h, horizon + y_off + 10, rc, (0.18, 0.22, 0.3)[i] * (1 + shine), rim, 3 + i)
        haze(c, horizon + y_off + 2, 40 + i * 6, hz, (0.5, 0.42, 0.45)[i])
    layer(c, 0.25, cam, lambda: blurred(c, blur_far, lambda: row(0, 'r1', 20, 31, 70, 46, 0.25), bounds=R.MakeLTRB(-400, horizon - 260, W + 400, horizon + 200)))
    layer(c, 0.38, cam, lambda: blurred(c, blur_mid * 1.4, lambda: row(1, 'r2', 70, 17, 115, 60, 0.18), bounds=R.MakeLTRB(-400, horizon - 260, W + 400, horizon + 260)))
    layer(c, 0.5, cam, lambda: blurred(c, blur_mid, lambda: row(2, 'r3', 125, 23, 170, 78, 0.12, 0.2), bounds=R.MakeLTRB(-400, horizon - 300, W + 400, horizon + 320)))
    def field():
        f0, f1 = FIELD[mood]
        ground_tex(c, horizon + 118, H + 100, f0, f1, seed=4, blotch=(10, 20, 16), ba=0.35)
        grass.draw(c, t, wind=wind, light=(255, 196, 150) if mood == 'dusk' else (190, 215, 255), band_range=range(0, 4), gust=gust)
        haze(c, horizon + 150, 40, (200, 150, 170) if mood == 'dusk' else (90, 120, 180), 0.35)
    layer(c, 0.85, cam, field)
    if fire:
        layer(c, 0.9, cam, lambda: fireflies(c, t, 22, 3, (40, 1180, 1040, 1700), size=3.2, a=1 - shine))


def meadow_near(c, t, cam=(1, 0, 0), mood='dusk', wind=1.0, gust=0.0, grass=None):
    grass = grass or (GR_WIDE if mood == 'dusk' else GR_NIGHT)
    layer(c, 1.0, cam, lambda: grass.draw(c, t, wind=wind, light=(255, 196, 150) if mood == 'dusk' else (190, 215, 255), band_range=range(4, 6), gust=gust))


def sky_ring(c, t, k, mood='dusk'):
    """A planetary ring seen from the ground: many fine translucent bands arching across the sky."""
    if k <= 0: return
    cx, cy = 540, 2600
    col = (255, 238, 220) if mood == 'dusk' else (232, 238, 255)
    rng = np.random.default_rng(4)
    c.saveLayerAlpha(None, int(255 * cl(k)))
    base = 2050
    for i in range(46):
        rr = base + i * 9 + rng.normal(0, 2)
        a = (0.10 + 0.30 * rng.random()) * (0.25 if 20 < i < 24 else 1.0)    # a dark gap like Cassini's
        p = skia.Path(); p.addArc(R.MakeXYWH(cx - rr * 0.95, cy - rr, rr * 1.9, rr * 2), 200, 140)
        c.drawPath(p, paint(col, a, stroke=7 + 6 * rng.random(), blur=1.2))
    p = skia.Path(); p.addArc(R.MakeXYWH(cx - (base + 200) * 0.95, cy - base - 200, (base + 200) * 1.9, (base + 200) * 2), 200, 140)
    c.drawPath(p, paint(col, 0.18, stroke=440, blur=40, blend=SCREEN))
    # Earth's shadow falls across one side of the ring
    c.drawRect(R.MakeXYWH(760, 0, 400, 900), paint(shader=lin(760, 0, 1080, 0, [argb((8, 12, 34), 0), argb((8, 12, 34), 0.7)]), blend=skia.BlendMode.kSrcATop))
    c.restore()


# ------------------------------------------------------------------ space
def space_bg(c, t, seed=3, neb=((120, 50, 170), (30, 90, 190), (200, 80, 120)), na=0.35, top=(4, 6, 20), bot=(14, 12, 40)):
    vgrad(c, [(0, top), (1, bot)])
    for i, col in enumerate(neb):
        x = hsh(i, seed) * W; y = 200 + hsh(i, seed + 1) * (H - 400)
        r = 420 + 380 * hsh(i, seed + 2)
        c.drawOval(R.MakeXYWH(x - r, y - r * 0.6, 2 * r, 1.2 * r), paint(col, na * (0.6 + 0.4 * math.sin(t * 0.2 + i)), blur=r * 0.35, blend=SCREEN))
    for i in range(260):
        x = hsh(i, seed + 5) * W; y = hsh(i, seed + 6) * H
        s_ = 0.6 + 2.2 * hsh(i, seed + 7) ** 3
        tw_ = 0.6 + 0.4 * math.sin(t * (0.6 + 2 * hsh(i, seed + 8)) + i)
        col = mix((255, 255, 255), (170, 200, 255) if hsh(i, seed + 9) > 0.5 else (255, 220, 180), 0.4 * hsh(i, seed + 10))
        c.drawCircle(x, y, s_, paint(col, 0.85 * tw_))
        if s_ > 2.2: glow_disc(c, x, y, s_ * 5, col, 0.25 * tw_)


def earth(c, x, y, r, rot=0.0, light=(-0.65, -0.3, 0.70), glow=(120, 180, 255), bulge=0.0, bulge_dir=0.0, a=1.0):
    if bulge > 0:
        # exaggerated tidal bulge of ocean water around the planet
        c.save(); c.translate(x, y); c.rotate(bulge_dir)
        bw = r * (1.0 + 0.04 + bulge); bh = r * (1.0 + 0.04 - bulge * 0.15)
        c.drawOval(R.MakeXYWH(-bw, -bh, 2 * bw, 2 * bh), paint(shader=rad(0, 0, bw, [argb((40, 120, 230), 0.0), argb((60, 150, 255), 0.85), argb((150, 220, 255), 0.95)], [0.0, 0.85, 1.0])))
        c.drawOval(R.MakeXYWH(-bw, -bh, 2 * bw, 2 * bh), stroke((210, 240, 255), 3, 0.8))
        c.restore()
    draw_planet(c, 'earth', x, y, r, rot=rot, glow=glow, halo=(90, 150, 255), light=light, a=a)


def moon_ball(c, x, y, r, light=(-0.7, -0.2, 0.68), glow=0.25, a=1.0):
    if a <= 0: return
    if glow > 0: sun_glow(c, x, y, r * 1.6, (200, 210, 230), glow * a)
    im = moon_img(640 if r > 120 else 320, light=tuple(light))
    p = skia.Paint(); p.setAlphaf(a)
    c.drawImageRect(im, R.MakeXYWH(x - r, y - r, 2 * r, 2 * r), LINS, p)


def dist_pill(c, x, y, text, a=1.0, col=(18, 22, 44), size=44):
    if a <= 0: return
    f = font('ant', size); w = f.measureText(text) + size; h = size * 1.4
    c.drawRoundRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), h / 2, h / 2, paint(col, 0.85 * a))
    c.drawRoundRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), h / 2, h / 2, stroke((255, 255, 255), 2.5, 0.6 * a))
    c.drawString(text, x - f.measureText(text) / 2, y + size * 0.36, f, paint((255, 255, 255), a))


def dashed_line(c, x0, y0, x1, y1, col, w=4, a=1.0, dash=18, gap=12, phase=0.0):
    p = skia.Path(); p.moveTo(x0, y0); p.lineTo(x1, y1)
    pp = stroke(col, w, a); pp.setPathEffect(skia.DashPathEffect.Make([dash, gap], phase))
    c.drawPath(p, pp)


def dashed_circle(c, x, y, r, col, w=4, a=1.0, dash=22, gap=14, phase=0.0, sy=1.0):
    p = skia.Path(); p.addOval(R.MakeXYWH(x - r, y - r * sy, 2 * r, 2 * r * sy))
    pp = stroke(col, w, a); pp.setPathEffect(skia.DashPathEffect.Make([dash, gap], phase))
    c.drawPath(p, pp)


# ------------------------------------------------------------------ lunar surface + mirror panel
def lunar_surface(c, t, horizon=1120, earth_pos=(250, 430), earth_r=120, cam=(1, 0, 0)):
    vgrad(c, [(0, (2, 3, 10)), (1, (8, 10, 22))])
    for i in range(160):
        x = hsh(i, 41) * W; y = hsh(i, 42) * horizon
        c.drawCircle(x, y, 0.7 + 1.6 * hsh(i, 43) ** 3, paint((255, 255, 255), 0.7))
    layer(c, 0.1, cam, lambda: earth(c, earth_pos[0], earth_pos[1], earth_r, rot=t * 0.05, light=(0.7, -0.2, 0.68)))
    def ground():
        p = skia.Path(); p.moveTo(-200, horizon + 40)
        for i in range(30):
            x = -200 + i * 60; p.lineTo(x, horizon + 20 * math.sin(i * 0.7) + 10 * hsh(i, 5))
        p.lineTo(W + 200, H + 200); p.lineTo(-200, H + 200); p.close()
        c.drawPath(p, paint(shader=lin(0, horizon, 0, H, [argb((150, 150, 158)), argb((96, 96, 106)), argb((58, 58, 66))], [0, 0.4, 1])))
        c.save(); c.clipPath(p, doAntiAlias=True)
        for i in range(34):
            d = hsh(i, 7) ** 1.4
            y = lerp(horizon + 30, H + 60, d); x = hsh(i, 8) * (W + 300) - 150
            w = lerp(40, 360, d) * (0.5 + hsh(i, 9)); h = w * lerp(0.18, 0.32, d)
            c.drawOval(R.MakeXYWH(x - w / 2, y - h / 2, w, h), paint((40, 40, 48), 0.55, blur=2))
            c.drawArc(R.MakeXYWH(x - w / 2, y - h / 2, w, h), 200, 160, False, stroke((200, 200, 208), max(2, w * 0.03), 0.6))
            c.drawOval(R.MakeXYWH(x - w * 0.42, y - h * 0.3, w * 0.84, h * 0.7), paint((90, 90, 100), 0.5, blur=3))
        for i in range(60):
            d = hsh(i, 17); y = lerp(horizon + 20, H, d ** 1.3); x = hsh(i, 18) * W
            r = lerp(3, 18, d) * (0.5 + hsh(i, 19))
            c.drawOval(R.MakeXYWH(x - r, y - r * 0.6, 2 * r, 1.2 * r), paint((120, 120, 128)))
            c.drawOval(R.MakeXYWH(x - r * 0.6, y - r * 0.55, r * 1.1, r * 0.6), paint((190, 190, 198), 0.7))
        c.restore()
    layer(c, 0.9, cam, ground)


def mirror_panel(c, x, y, s, t, beam=0.0, beam_from=(250, 430)):
    """Apollo-style laser retroreflector: a tilted panel of 100 corner-cube mirrors on legs."""
    c.save(); c.translate(x, y); c.scale(s, s)
    for lx in (-80, 80):
        c.drawLine(lx, 0, lx * 0.8, -70, stroke((60, 60, 70), 10)); c.drawLine(lx, 0, lx * 0.8, -70, stroke((170, 170, 180), 6))
    c.drawOval(R.MakeXYWH(-140, -16, 280, 36), paint((0, 0, 0), 0.45, blur=8))
    c.save(); c.translate(0, -120); c.skew(0.0, 0.0); c.scale(1, 0.62)
    panel = rrect(-140, -120, 280, 240, 10)
    c.drawPath(panel, paint(shader=lin(0, -120, 0, 120, [argb((210, 210, 220)), argb((140, 140, 152))])))
    c.drawPath(panel, stroke((40, 40, 50), 5))
    for i in range(10):
        for j in range(10):
            cx_ = -126 + i * 28 + 14; cy_ = -106 + j * 23 + 11
            c.drawCircle(cx_, cy_, 10, paint((30, 36, 60)))
            g = 0.5 + 0.5 * math.sin(t * 2 + i * 0.7 + j * 0.4)
            c.drawCircle(cx_ - 3, cy_ - 3, 4, paint((180, 220, 255), 0.35 + 0.4 * g))
    c.restore()
    c.restore()
    if beam > 0:
        bx, by = beam_from
        tx, ty = x, y - 120 * s
        k = cl(beam)
        ex, ey = lerp(bx, tx, k), lerp(by, ty, k)
        c.drawLine(bx, by, ex, ey, paint(GRN, 0.25, stroke=26, blur=10, blend=PLUS))
        c.drawLine(bx, by, ex, ey, paint((200, 255, 210), 0.95, stroke=5, blend=PLUS))
        if k >= 1:
            glow_disc(c, tx, ty, 140, GRN, 0.7)


# ------------------------------------------------------------------ observatory + laser
def observatory(c, t, beam=0.0, moon_pos=(820, 360), moon_r=70):
    vgrad(c, [(0, (6, 10, 32)), (0.55, (22, 40, 92)), (1, (60, 84, 140))], 0, 1300)
    c.save(); c.rotate(-28)
    c.drawOval(R.MakeXYWH(-600, 520, 2200, 300), paint((150, 140, 220), 0.22, blur=80, blend=SCREEN))
    c.drawOval(R.MakeXYWH(-500, 590, 2000, 120), paint((255, 230, 220), 0.12, blur=40, blend=SCREEN))
    c.restore()
    stars(c, 9, 1150, 260, 0.95, t)
    moon_ball(c, moon_pos[0], moon_pos[1], moon_r, light=(-0.2, -0.1, 0.97), glow=0.5)
    # mountains
    p = _C.setdefault('obs_m1', ridge_path(1180, 140, 8, 1.4, 0.6))
    fill_layer(c, p, (58, 74, 124), (30, 40, 72), 1000, 1400, edge=(190, 210, 255), edge_a=0.5)
    haze(c, 1210, 70, (90, 110, 170), 0.45)
    p2 = _C.setdefault('obs_m2', ridge_path(1360, 90, 13, 1.0, 0.4))
    fill_layer(c, p2, (26, 32, 58), (8, 10, 22), 1250, 1700, edge=(170, 200, 255), edge_a=0.4)
    c.save(); c.translate(420, 1290); c.scale(1.35, 1.35); c.translate(-420, -1290)
    # dome building on the ridge
    dx, dy = 420, 1290
    base = rrect(dx - 150, dy - 10, 300, 180, 6)
    shade(c, base, (200, 204, 216), L_NIGHT, sz=150, ow=4)
    dome = skia.Path(); dome.addArc(R.MakeXYWH(dx - 160, dy - 160, 320, 320), 180, 180); dome.close()
    shade(c, dome, (226, 230, 240), L_NIGHT, sz=160, ow=4, depth=0.8)
    # slit + telescope
    slit = skia.Path(); slit.moveTo(dx + 10, dy - 156); slit.lineTo(dx + 60, dy - 140); slit.lineTo(dx + 70, dy - 4); slit.lineTo(dx + 20, dy - 4); slit.close()
    c.drawPath(slit, paint((10, 12, 24)))
    c.save(); c.clipPath(slit, doAntiAlias=True)
    c.drawLine(dx + 30, dy - 20, dx + 70, dy - 120, stroke((150, 156, 170), 26)); c.drawLine(dx + 30, dy - 20, dx + 70, dy - 120, stroke((60, 64, 76), 2))
    c.restore()
    for i in range(4):
        c.drawRect(R.MakeXYWH(dx - 120 + i * 70, dy + 50, 30, 40), paint((255, 210, 140), 0.85))
        glow_disc(c, dx - 105 + i * 70, dy + 70, 50, (255, 200, 120), 0.35)
    c.restore()
    if beam > 0:
        sx, sy = 420 + 66 * 1.35, 1290 - 116 * 1.35
        tx, ty = moon_pos
        k = cl(beam)
        ex, ey = lerp(sx, tx, k), lerp(sy, ty, k)
        c.drawLine(sx, sy, ex, ey, paint(GRN, 0.3, stroke=30, blur=12, blend=PLUS))
        c.drawLine(sx, sy, ex, ey, paint((210, 255, 220), 1.0, stroke=5, blend=PLUS))
        glow_disc(c, sx, sy, 60, GRN, 0.8)
        if k >= 1: glow_disc(c, tx, ty, 90, GRN, 0.6 + 0.3 * math.sin(t * 20))


# ------------------------------------------------------------------ UI cards
def glass_card(c, cx, cy, w, h, draw, k=1.0, ry=-6, rx=4, fill=(16, 20, 42), alpha=0.88, border=(255, 255, 255), radius=34):
    if k <= 0: return
    sc_ = 0.7 + 0.3 * eback(cl(k), 1.5)
    d = 2200.0
    cy_, sy_ = math.cos(math.radians(ry)), math.sin(math.radians(ry))
    cx_, sx_ = math.cos(math.radians(rx)), math.sin(math.radians(rx))
    def proj(px, py):
        X, Y, Z = px * cy_, py, px * sy_
        Y, Z = Y * cx_ - Z * sx_, Y * sx_ + Z * cx_
        f = d / (d + Z)
        return skia.Point(cx + X * f * sc_, cy + Y * f * sc_)
    src = [skia.Point(-w / 2, -h / 2), skia.Point(w / 2, -h / 2), skia.Point(w / 2, h / 2), skia.Point(-w / 2, h / 2)]
    dst = [proj(*q) for q in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]]
    M = skia.Matrix(); M.setPolyToPoly(src, dst)
    a = min(1.0, k * 3)
    c.save(); c.translate(10, 22); c.concat(M)
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), radius, radius, paint((0, 0, 0), 0.4 * a, blur=20))
    c.restore()
    c.save(); c.concat(M)
    c.saveLayerAlpha(None, int(255 * a))
    rr = R.MakeXYWH(-w / 2, -h / 2, w, h)
    c.drawRoundRect(rr, radius, radius, paint(fill, alpha))
    c.drawRoundRect(rr, radius, radius, paint(shader=lin(0, -h / 2, 0, h / 2, [argb((255, 255, 255), 0.16), argb((255, 255, 255), 0), argb((0, 0, 0), 0.12)], [0, 0.5, 1])))
    draw(c)
    c.drawRoundRect(rr, radius, radius, stroke(border, 3, 0.55))
    c.restore()
    c.restore()


def big_text(c, s, x, y, size, col=(255, 255, 255), a=1.0, key='ant', stroke_k=0.1):
    f = font(key, size); w = f.measureText(s)
    if stroke_k: c.drawString(s, x - w / 2, y, f, stroke((0, 0, 0), size * stroke_k, a))
    c.drawString(s, x - w / 2, y, f, paint(col, a))
    return w


# ------------------------------------------------------------------ coast + flood
def building_row(seed, base, n, x0, x1, hmin, hmax):
    out = []
    x = x0; k = 0
    while x < x1:
        w = 70 + 90 * hsh(k, seed); h = lerp(hmin, hmax, hsh(k, seed + 1) ** 1.3)
        out.append((x, base - h, w, h, k)); x += w + 6 + 10 * hsh(k, seed + 2); k += 1
    return out

_B1 = building_row(3, 1180, 0, -40, 1120, 160, 560)
_B2 = building_row(9, 1250, 0, -60, 1140, 80, 260)


def coast(c, t, wl=1300, mood='dusk', hero_fn=None):
    """Coastal city at dusk. wl = sea surface y (lower number = higher water)."""
    vgrad(c, [(0, (40, 46, 104)), (0.45, (150, 92, 130)), (0.75, (250, 150, 100)), (1, (255, 200, 130))], 0, 1000)
    sun_glow(c, 820, 860, 520, (255, 190, 120), 0.6)
    c.drawCircle(820, 860, 46, paint((255, 236, 200)))
    cloud_streaks(c, t, 21, 250, 700, (110, 70, 120), 0.5, n=6, drift=10, lit=(255, 170, 120))
    # far sea to the horizon
    c.drawRect(R.MakeLTRB(0, 880, W, 1300), paint(shader=lin(0, 880, 0, 1300, [argb((180, 120, 130)), argb((60, 70, 120))])))
    for i in range(18):
        y = 890 + i * 18; x = 820 + math.sin(i * 1.7 + t) * 30
        c.drawLine(x - 80 + i * 4, y, x + 80 - i * 4, y, stroke((255, 220, 170), 3, 0.5 - i * 0.025))
    # skyline
    def bld(B, col, wincol, a_win=0.8, edge=(255, 190, 140)):
        for (x, y, w, h, k) in B:
            c.drawRect(R.MakeXYWH(x, y, w, h + 400), paint(shader=lin(x, 0, x + w, 0, [argb(mix(col, edge, 0.25)), argb(col), argb(dark(col, 0.35))], [0, 0.35, 1])))
            c.drawLine(x, y, x + w, y, stroke(edge, 3, 0.6))
            for wy in range(int(y + 16), int(y + h - 10), 26):
                for wx in range(int(x + 10), int(x + w - 14), 20):
                    if hsh(wx * 7 + wy, k) > 0.45:
                        c.drawRect(R.MakeXYWH(wx, wy, 10, 14), paint(wincol, a_win * (0.5 + 0.5 * hsh(wx + wy * 3, k + 1))))
    bld(_B1, (70, 62, 96), (255, 210, 140), 0.7)
    haze(c, 1150, 60, (230, 150, 140), 0.35)
    bld(_B2, (110, 80, 92), (255, 220, 160), 0.9)
    # beach + promenade
    c.drawRect(R.MakeLTRB(-20, 1250, W + 20, 1420), paint(shader=lin(0, 1250, 0, 1420, [argb((236, 196, 140)), argb((200, 150, 100))])))
    for i in range(7):
        px = 80 + i * 160
        c.drawLine(px, 1250, px + 6, 1160, stroke((90, 60, 40), 8))
        for j in range(5):
            a = -150 + j * 30
            c.drawLine(px + 6, 1160, px + 6 + math.cos(math.radians(a)) * 60, 1160 + math.sin(math.radians(a)) * 30 + 14, stroke((40, 90, 50), 10))
    # near sea
    c.drawRect(R.MakeLTRB(-20, 1420, W + 20, H + 20), paint(shader=lin(0, 1420, 0, H, [argb((60, 110, 150)), argb((14, 40, 70))])))
    if hero_fn: hero_fn()
    # rising sea in front of everything
    if wl < 1420:
        p = skia.Path(); p.moveTo(-40, H + 40)
        for i in range(0, 41):
            x = -40 + i * 30
            p.lineTo(x, wl + 10 * math.sin(x * 0.02 + t * 3) + 6 * math.sin(x * 0.05 - t * 5))
        p.lineTo(W + 40, H + 40); p.close()
        c.drawPath(p, paint(shader=lin(0, wl, 0, wl + 600, [argb((70, 150, 190), 0.72), argb((20, 60, 110), 0.94), argb((10, 30, 60), 0.98)], [0, 0.4, 1])))
        c.save(); c.clipPath(p, doAntiAlias=True)
        for i in range(30):
            y = wl + 30 + i * 40; ph_ = t * 2 + i
            c.drawLine(-20, y + 8 * math.sin(ph_), W + 20, y + 8 * math.sin(ph_ + 2), stroke((180, 230, 255), 2, 0.12))
        c.restore()
        q = skia.Path(); q.moveTo(-40, wl)
        for i in range(0, 41):
            x = -40 + i * 30
            q.lineTo(x, wl + 10 * math.sin(x * 0.02 + t * 3) + 6 * math.sin(x * 0.05 - t * 5))
        c.drawPath(q, paint((240, 250, 255), 0.9, stroke=9, blur=2))
        for i in range(40):
            fx = (hsh(i, 3) * W + t * 40) % W
            c.drawCircle(fx, wl + 4 + 8 * math.sin(fx * 0.02 + t * 3), 4 + 6 * hsh(i, 4), paint((255, 255, 255), 0.7))


# ------------------------------------------------------------------ underwater beach house
def fish(c, x, y, s, col, t, flip=False):
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    wag = math.sin(t * 9) * 8
    body = oval(0, 0, 90, 46)
    tail = skia.Path(); tail.moveTo(36, 0); tail.lineTo(70, -22 + wag); tail.lineTo(66, 22 + wag); tail.close()
    shade(c, union(body, tail), col, L_WATER, sz=46, ow=3)
    c.drawCircle(-24, -6, 7, paint((255, 255, 255))); c.drawCircle(-26, -6, 4, paint((10, 10, 20)))
    c.drawArc(R.MakeXYWH(-6, -18, 14, 36), -60, 120, False, stroke(dark(col, 0.4), 2.4))
    c.restore()


def house_under(c, t, hero_fn=None):
    # interior wall
    vgrad(c, [(0, (44, 86, 104)), (1, (24, 50, 66))])
    for i in range(12):
        x = i * 100 + 20
        c.drawLine(x, 0, x, 1500, stroke((60, 110, 126), 4, 0.5))
    # window to the sea
    wx, wy, ww, wh = 150, 380, 780, 640
    win = rrect(wx, wy, ww, wh, 24)
    c.save(); c.clipPath(win, doAntiAlias=True)
    vgrad(c, [(0, (40, 170, 210)), (1, (6, 50, 100))], wy, wy + wh, rect=R.MakeXYWH(wx, wy, ww, wh))
    god_rays(c, (wx + ww * 0.6, wy - 200), t, (200, 255, 255), 0.25, n=6, spread=40, length=1100, seed=5)
    for i in range(5):
        sx_ = wx + 60 + i * 170
        p = skia.Path(); p.moveTo(sx_, wy + wh)
        for j in range(8):
            p.lineTo(sx_ + 18 * math.sin(t * 1.5 + j * 0.8 + i), wy + wh - j * 40)
        c.drawPath(p, stroke((30, 120, 70), 14, 0.9))
    fish(c, wx + ((t * 120) % (ww + 300)) - 150, wy + 220, 1.3, (255, 150, 60), t)
    fish(c, wx + ww - ((t * 90 + 200) % (ww + 300)) + 150, wy + 420, 1.0, (255, 220, 70), t, flip=True)
    fish(c, wx + ((t * 70 + 400) % (ww + 300)) - 150, wy + 120, 0.7, (120, 200, 255), t)
    for i in range(14):
        bx = wx + hsh(i, 7) * ww; by = wy + wh - ((t * 90 * (0.5 + hsh(i, 8)) + hsh(i, 9) * wh) % wh)
        c.drawCircle(bx, by, 4 + 8 * hsh(i, 10), stroke((220, 250, 255), 2.4, 0.7))
    c.restore()
    shade(c, union(rrect(wx - 26, wy - 26, ww + 52, 26, 8), rrect(wx - 26, wy + wh, ww + 52, 26, 8), rrect(wx - 26, wy, 26, wh, 4), rrect(wx + ww, wy, 26, wh, 4)),
          (240, 236, 226), L_WATER, sz=26, ow=3)
    c.drawLine(wx + ww / 2, wy, wx + ww / 2, wy + wh, stroke((240, 236, 226), 16)); c.drawLine(wx, wy + wh / 2, wx + ww, wy + wh / 2, stroke((240, 236, 226), 16))
    # caustic light on the wall and floor
    for i in range(8):
        cx_ = 100 + i * 130 + 30 * math.sin(t + i); cy_ = 1250 + 20 * math.cos(t * 1.3 + i)
        c.drawOval(R.MakeXYWH(cx_ - 80, cy_ - 20, 160, 40), paint((150, 255, 255), 0.12, blur=12, blend=SCREEN))
    # floor + sofa
    c.drawRect(R.MakeLTRB(-20, 1460, W + 20, H + 20), paint(shader=lin(0, 1460, 0, H, [argb((120, 90, 70)), argb((60, 44, 40))])))
    sofa = union(rrect(180, 1240, 720, 150, 40), rrect(140, 1320, 800, 160, 40))
    shade(c, sofa, (200, 70, 70), L_WATER, sz=150, ow=4)
    for x in (230, 850):
        shade(c, rrect(x - 50, 1300, 100, 190, 36), (180, 60, 62), L_WATER, sz=100, ow=4)
    if hero_fn: hero_fn()
    # lamp
    c.drawLine(990, 1480, 990, 1150, stroke((50, 50, 60), 8))
    shade(c, smooth_closed([(940, 1150), (1040, 1150), (1020, 1060), (960, 1060)]), (255, 220, 160), L_WATER, sz=80, ow=3)
    glow_disc(c, 990, 1110, 160, (255, 220, 160), 0.4)


# ------------------------------------------------------------------ bedroom under a bright moon
def bedroom(c, t, shine=1.0, cover=0.0, face=None, blink=False):
    vgrad(c, [(0, (16, 22, 52)), (1, (10, 14, 34))])
    wx, wy, ww, wh = 110, 300, 460, 560
    win = rrect(wx, wy, ww, wh, 16)
    c.save(); c.clipPath(win, doAntiAlias=True)
    vgrad(c, [(0, (40, 70, 140)), (1, (90, 130, 200))], wy, wy + wh, rect=R.MakeXYWH(wx, wy, ww, wh))
    draw_moon(c, wx + ww * 0.55, wy + wh * 0.45, 230, glow=(220, 235, 255), ga=0.9, warm=0.0, lha=0.0)
    c.restore()
    shade(c, union(rrect(wx - 20, wy - 20, ww + 40, 20, 6), rrect(wx - 20, wy + wh, ww + 40, 24, 6), rrect(wx - 20, wy, 20, wh, 4), rrect(wx + ww, wy, 20, wh, 4)),
          (230, 230, 240), L_ROOM, sz=22, ow=3)
    c.drawLine(wx + ww / 2, wy, wx + ww / 2, wy + wh, stroke((230, 230, 240), 12)); c.drawLine(wx, wy + wh / 2, wx + ww, wy + wh / 2, stroke((230, 230, 240), 12))
    # light shaft from the window across the room
    beam = skia.Path(); beam.moveTo(wx, wy); beam.lineTo(wx + ww, wy); beam.lineTo(W + 200, 1700); beam.lineTo(380, 1900); beam.close()
    c.drawPath(beam, paint(shader=lin(wx, wy, 700, 1800, [argb((200, 220, 255), 0.4 * shine), argb((200, 220, 255), 0.1 * shine)]), blur=20, blend=SCREEN))
    dust(c, t, 40, 6, (200, 400, 1080, 1700), col=(220, 235, 255), a=0.5 * shine, size=2.4, wind=(8, -4))
    # floor
    c.drawRect(R.MakeLTRB(-20, 1500, W + 20, H + 20), paint(shader=lin(0, 1500, 0, H, [argb((60, 50, 80)), argb((24, 20, 40))])))
    # bed
    shade(c, rrect(120, 1180, 120, 420, 20), (120, 80, 60), L_ROOM, sz=120, ow=4)
    shade(c, rrect(120, 1400, 900, 160, 30), (230, 230, 240), L_ROOM, sz=160, ow=4)
    shade(c, oval(330, 1310, 300, 130), (246, 246, 252), L_ROOM, sz=130, ow=4)
    hc = (330, 1215)
    c.save(); c.translate(*hc); c.scale(1.35, 1.35)
    draw_head(c, face or Face('open', 'flat', 'angry'), L_ROOM, t, blink, acc='sleepmask' if cover < 0.01 else None)
    c.restore()
    by = lerp(1330, 1080, eio(cover))
    blank = skia.Path(); blank.moveTo(170, by + 30); blank.cubicTo(400, by - 30, 700, by + 20, 1040, by + 10)
    blank.lineTo(1060, 1560); blank.lineTo(150, 1560); blank.close()
    shade(c, blank, (70, 96, 190), L_ROOM, sz=260, ow=4, depth=0.5)
    c.save(); c.clipPath(blank, doAntiAlias=True)
    for i in range(6):
        c.drawLine(200 + i * 150, by, 200 + i * 150 + 40, 1560, stroke((255, 255, 255), 10, 0.12))
    c.restore()


# ------------------------------------------------------------------ ground tides cross-section
def ground_section(c, t, k=0.0, quake=0.0, hero_fn=None):
    vgrad(c, SKIES['dusk'], -200, 1200)
    sun_glow(c, 540, 1000, 600, (255, 190, 130), 0.5)
    p = _C.setdefault('gs_far', ridge_path(1000, 70, 5, 1.3, 0.5))
    fill_layer(c, p, (130, 100, 140), (170, 120, 140), 900, 1100)
    haze(c, 1010, 50, (255, 170, 140), 0.45)
    amp = 9 + 120 * k
    gy = 1180 - amp * math.sin(t * (1.2 + 3 * k))
    surf = skia.Path(); surf.moveTo(-40, H + 40)
    for i in range(0, 46):
        x = -40 + i * 26
        y = gy + quake * 30 * math.sin(x * 0.03 + t * 9) + quake * 14 * math.sin(x * 0.11 - t * 13)
        surf.lineTo(x, y)
    surf.lineTo(W + 40, H + 40); surf.close()
    c.drawPath(surf, paint(shader=lin(0, gy, 0, H, [argb((120, 86, 60)), argb((90, 60, 46)), argb((60, 40, 34)), argb((40, 28, 26))], [0, 0.3, 0.6, 1])))
    c.save(); c.clipPath(surf, doAntiAlias=True)
    for j, (yy, col) in enumerate([(120, (140, 100, 70)), (260, (110, 76, 56)), (430, (80, 60, 50))]):
        q = skia.Path(); q.moveTo(-40, gy + yy)
        for i in range(0, 46):
            x = -40 + i * 26
            q.lineTo(x, gy + yy + 14 * math.sin(x * 0.012 + j) + quake * 20 * math.sin(x * 0.04 + t * 9))
        c.drawPath(q, stroke(dark(col, 0.3), 6, 0.6))
    for i in range(40):
        x = hsh(i, 11) * W; y = gy + 60 + hsh(i, 12) * 700
        r = 6 + 16 * hsh(i, 13)
        shade(c, oval(x, y, r * 2, r * 1.3), (150, 130, 120), L_DUSK, sz=r * 1.3, ow=2, rim=0)
    c.drawRect(R.MakeLTRB(-40, gy - 40, W + 40, gy + 28), paint((60, 120, 50)))
    if k > 0.3 or quake > 0:
        for i, (x0, x1) in enumerate([(200, 300), (640, 760), (880, 940)]):
            cp = skia.Path(); cp.moveTo(x0, gy + 20)
            for j in range(6):
                cp.lineTo(lerp(x0, x1, j / 5) + 20 * math.sin(j * 2 + i), gy + 20 + j * 70)
            c.drawPath(cp, paint((255, 120, 40), 0.7 * max(k, quake), stroke=22, blur=10, blend=PLUS))
            c.drawPath(cp, stroke((30, 14, 10), 6, max(k, quake)))
    c.restore()
    GR_WIDE.draw(c, t, wind=1.0 + quake * 3, light=(255, 196, 150), band_range=range(5, 6)) if False else None
    for i in range(70):
        x = hsh(i, 21) * W
        h_ = 14 + 26 * hsh(i, 22)
        c.drawLine(x, gy + 2, x + 6 * math.sin(t * 2 + i), gy - h_, stroke((90, 160, 70), 5))
    if hero_fn: hero_fn(gy)
    return gy


def ruler(c, x, y0, y1, label, a=1.0, col=(255, 214, 10)):
    if a <= 0: return
    c.drawLine(x, y0, x, y1, stroke(col, 6, a))
    for yy in (y0, y1):
        c.drawLine(x - 22, yy, x + 22, yy, stroke(col, 6, a))
    for yy, d in ((y0, 1), (y1, -1)):
        p = skia.Path(); p.moveTo(x, yy); p.lineTo(x - 14, yy + d * 22); p.lineTo(x + 14, yy + d * 22); p.close()
        c.drawPath(p, paint(col, a))
    f = font('ant', 54)
    c.drawString(label, x - 30 - f.measureText(label), (y0 + y1) / 2 + 18, f, stroke((0, 0, 0), 8, a))
    c.drawString(label, x - 30 - f.measureText(label), (y0 + y1) / 2 + 18, f, paint(col, a))


# ------------------------------------------------------------------ Earth as a stress ball
def earth_squeeze(c, t, sq=0.0, crack=0.0):
    space_bg(c, t, seed=8, neb=((140, 60, 120), (40, 80, 170)), na=0.3)
    cx, cy, r = 540, 1000, 300
    sx_, sy_ = 1 - 0.22 * sq, 1 + 0.18 * sq
    c.save(); c.translate(cx, cy); c.scale(sx_, sy_)
    earth(c, 0, 0, r, rot=t * 0.1)
    if crack > 0:
        rng = np.random.default_rng(3)
        for i in range(7):
            a0 = rng.uniform(0, 6.28); p = skia.Path(); x, y = math.cos(a0) * r * 0.2, math.sin(a0) * r * 0.2; p.moveTo(x, y)
            for j in range(5):
                a0 += rng.normal(0, 0.5); x += math.cos(a0) * r * 0.18; y += math.sin(a0) * r * 0.18; p.lineTo(x, y)
            c.drawPath(p, paint((255, 140, 40), 0.8 * crack, stroke=18, blur=8, blend=PLUS))
            c.drawPath(p, stroke((255, 230, 150), 4, crack))
    c.restore()
    # two giant hands pressing from the sides
    gap = r * sx_ + 20
    for side in (-1, 1):
        hx = cx + side * (gap + 40)
        c.save(); c.translate(hx, cy + 40); c.scale(side * -9.0, 9.0); c.rotate(-90)
        hp = hand_shape('open', thumb_up=True)
        shade(c, hp, SKIN, L_DAY, sz=24, ow=2.2, depth=0.8)
        c.restore()
        for k in range(3):
            yy = cy - 120 + k * 120
            c.drawLine(cx + side * (gap + 230), yy, cx + side * (gap + 290), yy, stroke((255, 255, 255), 6, 0.6 * sq))


# ------------------------------------------------------------------ volcano lands (present day + early Earth)
def lava_glow(c, path, a=1.0, w=16):
    c.drawPath(path, paint((255, 110, 30), 0.6 * a, stroke=w * 2.2, blur=w * 0.8, blend=PLUS))
    c.drawPath(path, stroke((255, 190, 80), w * 0.6, a))
    c.drawPath(path, stroke((255, 245, 200), w * 0.2, a))


def volcano_land(c, t, erupt=1.0, quake=0.0, early=False, moon_r=0, hero_fn=None):
    if early:
        vgrad(c, [(0, (20, 8, 16)), (0.5, (80, 26, 30)), (0.8, (180, 70, 40)), (1, (255, 140, 60))], 0, 1200)
    else:
        vgrad(c, [(0, (30, 26, 60)), (0.5, (110, 60, 80)), (0.85, (230, 110, 70)), (1, (255, 170, 100))], 0, 1200)
    stars(c, 2, 600, 60, 0.4, t)
    if moon_r:
        draw_moon(c, 560, 640, moon_r, glow=(255, 170, 120), ga=0.6, warm=0.35, low_haze=(255, 120, 80), lha=0.6)
    # volcano cone
    vx, vy = 540, 1060
    cone = skia.Path(); cone.moveTo(vx - 520, 1240); cone.cubicTo(vx - 300, 1150, vx - 140, vy, vx - 70, vy - 10)
    cone.lineTo(vx + 70, vy - 10); cone.cubicTo(vx + 140, vy, vx + 300, 1150, vx + 520, 1240); cone.close()
    shade(c, cone, (70, 40, 44) if early else (64, 52, 66), L_LAVA, sz=400, ow=0, depth=0.4, rim=1.0)
    for i, (x0, w) in enumerate([(-40, 18), (30, 14), (-10, 12)]):
        p = skia.Path(); p.moveTo(vx + x0, vy)
        for j in range(8):
            p.lineTo(vx + x0 + 40 * math.sin(j * 0.9 + i * 2) + (j * 30 if i == 1 else -j * 26 if i == 0 else j * 6), vy + j * 26)
        lava_glow(c, p, erupt * (0.6 + 0.4 * math.sin(t * 3 + i)), w)
    if erupt > 0:
        glow_disc(c, vx, vy, 300, (255, 120, 40), 0.7 * erupt)
        for i in range(16):
            ph_ = (t * 0.25 + hsh(i, 5)) % 1.0
            x = vx + (hsh(i, 6) - 0.5) * 300 * ph_ + 40 * math.sin(t + i)
            y = vy - 80 - ph_ * 620
            r = 60 + 160 * ph_
            col = mix((60, 40, 46), (30, 26, 34), ph_)
            c.drawCircle(x, y, r, paint(col, 0.75 * (1 - ph_ * 0.6) * erupt, blur=r * 0.2))
            c.drawCircle(x - r * 0.2, y + r * 0.3, r * 0.6, paint((255, 120, 50), 0.25 * (1 - ph_) * erupt, blur=r * 0.3, blend=SCREEN))
        for i in range(24):
            ph_ = (t * 0.9 + hsh(i, 15)) % 1.0
            vxx = (hsh(i, 16) - 0.5) * 600; vyy = -900 - 500 * hsh(i, 17)
            x = vx + vxx * ph_; y = vy + vyy * ph_ + 1600 * ph_ * ph_
            glow_disc(c, x, y, 26, (255, 140, 40), 0.8 * erupt); c.drawCircle(x, y, 6, paint((255, 230, 160), erupt))
    # ground
    gp = skia.Path(); gp.moveTo(-40, H + 40)
    for i in range(46):
        x = -40 + i * 26; gp.lineTo(x, 1230 + 16 * math.sin(x * 0.01) + quake * 22 * math.sin(x * 0.05 + t * 11))
    gp.lineTo(W + 40, H + 40); gp.close()
    c.drawPath(gp, paint(shader=lin(0, 1200, 0, H, [argb((60, 36, 36) if early else (52, 70, 46)), argb((26, 14, 16) if early else (20, 28, 22))])))
    c.save(); c.clipPath(gp, doAntiAlias=True)
    rng = np.random.default_rng(9 if early else 4)
    for i in range(6 if early else 3):
        x0 = rng.uniform(0, W); y0 = rng.uniform(1300, 1850); p = skia.Path(); p.moveTo(x0, y0)
        for j in range(6): x0 += rng.uniform(40, 120) * (1 if i % 2 else -1); y0 += rng.normal(0, 40); p.lineTo(x0, y0)
        lava_glow(c, p, (1.0 if early else quake) * (0.7 + 0.3 * math.sin(t * 2 + i)), 12)
    c.restore()
    if early:
        for i in range(10):
            ph_ = (t * 0.2 + hsh(i, 31)) % 1.0
            x = hsh(i, 32) * W; y = 1400 - ph_ * 400
            c.drawCircle(x, y, 60 + ph_ * 120, paint((200, 160, 160), 0.18 * (1 - ph_), blur=40))
    if hero_fn: hero_fn()


# ------------------------------------------------------------------ Jupiter + Io
_IO = {}


def io_img(size):
    if size in _IO: return _IO[size]
    from ed import _upnoise
    rng = np.random.default_rng(12)
    n = size
    y, x = np.mgrid[0:n, 0:n].astype(np.float32)
    x = (x + 0.5) / n * 2 - 1; y = (y + 0.5) / n * 2 - 1
    r2 = x * x + y * y; m = r2 < 1; z = np.sqrt(np.clip(1 - r2, 0, 1))
    nz = _upnoise(rng, 6, 6, n, n) + _upnoise(rng, 20, 20, n, n) * 0.5 + _upnoise(rng, 60, 60, n, n) * 0.25
    base = np.array([238, 214, 96], np.float32); org = np.array([226, 140, 50], np.float32); wht = np.array([250, 244, 210], np.float32)
    k1 = np.clip((nz + 0.1) * 2.5, 0, 1)[..., None]; k2 = np.clip((-nz - 0.2) * 3, 0, 1)[..., None]
    col = base * (1 - k1) + org * k1
    col = col * (1 - k2) + wht * k2
    for i in range(40):
        cx, cy = rng.uniform(-0.9, 0.9, 2); rr = rng.uniform(0.015, 0.05)
        d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / rr
        col = col * (1 - np.exp(-(d / 0.8) ** 2)[..., None] * 0.85)
        col = col * (1 - (np.exp(-((d - 2.0) / 0.8) ** 2) * 0.45)[..., None]) + np.array([200, 60, 30]) * (np.exp(-((d - 2.0) / 0.8) ** 2) * 0.45)[..., None]
    Lv = np.array([-0.6, -0.3, 0.74]); Lv /= np.linalg.norm(Lv)
    lam = np.clip(x * Lv[0] + y * Lv[1] + z * Lv[2], 0, 1)
    col *= (0.05 + 0.95 * lam ** 0.8)[..., None]
    edge = np.clip((1 - np.sqrt(r2)) * n / 2.0, 0, 1)
    out = np.zeros((n, n, 4), np.float32); out[..., :3] = np.clip(col, 0, 255) * edge[..., None]; out[..., 3] = edge * 255; out[~m] = 0
    _IO[size] = img_from(out.astype(np.uint8), False)
    return _IO[size]


def jupiter_io(c, t, plume=1.0):
    space_bg(c, t, seed=14, neb=((120, 70, 40), (60, 40, 120)), na=0.25)
    draw_planet(c, 'jupiter', 860, 520, 720, rot=t * 0.04, glow=(255, 220, 180), light=(-0.7, 0.2, 0.68))
    ix, iy, ir = 470, 1160, 250
    sun_glow(c, ix, iy, ir * 1.4, (255, 230, 150), 0.25)
    c.drawImageRect(io_img(640), R.MakeXYWH(ix - ir, iy - ir, 2 * ir, 2 * ir), LINS, skia.Paint())
    if plume > 0:
        for j, (ang, hgt) in enumerate([(-130, 150), (-60, 110), (-160, 90)]):
            a = math.radians(ang)
            px, py = ix + math.cos(a) * ir, iy + math.sin(a) * ir
            c.save(); c.translate(px, py); c.rotate(ang + 90)
            for i in range(26):
                ph_ = (t * 0.6 + hsh(i, j + 3)) % 1.0
                spread = (hsh(i, j + 4) - 0.5) * 2
                xx = spread * hgt * 0.9 * math.sin(ph_ * math.pi * 0.9); yy = -hgt * 1.4 * math.sin(ph_ * math.pi)
                c.drawCircle(xx, yy, 5 + 10 * ph_, paint((170, 200, 255), 0.5 * plume * (1 - ph_ * 0.5), blur=4, blend=SCREEN))
            p = skia.Path(); p.moveTo(-hgt * 0.9, 0); p.quadTo(0, -hgt * 2.8, hgt * 0.9, 0)
            c.drawPath(p, paint((180, 210, 255), 0.25 * plume, stroke=20, blur=14, blend=SCREEN))
            c.restore()


# ------------------------------------------------------------------ Roche limit: the Moon breaks into a ring
_RING = None


def ring_particles():
    global _RING
    if _RING is None:
        rng = np.random.default_rng(21)
        n = 1500
        ang = rng.uniform(0, 2 * math.pi, n)
        rad_ = np.concatenate([rng.uniform(1.45, 2.05, n // 2), rng.uniform(2.15, 2.9, n - n // 2)])
        size = rng.uniform(1.2, 4.6, n) ** 1.2
        shade_ = rng.uniform(0.55, 1.0, n)
        spread = rng.uniform(-1, 1, n)
        _RING = (ang, rad_, size, shade_, spread)
    return _RING


def roche(c, t, cx=540, cy=1080, er=150, moon_d=760, stretch=0.0, shatter=0.0, ring=0.0, moon_ang=-0.9, tilt=0.32, show_limit=1.0, planet='earth'):
    """Moon at moon_d px from the planet centre; shatter 0..1 breaks it; ring 0..1 spreads debris into a ring."""
    ang, rad_, size, sh, spread = ring_particles()
    mx, my = cx + math.cos(moon_ang) * moon_d, cy + math.sin(moon_ang) * moon_d * tilt * 2.2
    def debris(front):
        if shatter <= 0: return
        for i in range(0, len(ang), 1):
            k = ring
            a_ring = ang[i]; r_ring = rad_[i] * er
            # start: a clump at the moon, then smeared along the orbit, then the full ring
            a0 = moon_ang + spread[i] * 0.25 * shatter
            a = a0 + (a_ring - a0) * eio(k) if k > 0 else a0
            rr = lerp(moon_d + spread[i] * 40 * shatter, r_ring, eio(k))
            x = cx + math.cos(a) * rr; y = cy + math.sin(a) * rr * tilt
            infront = math.sin(a) > 0
            if infront != front: continue
            if k < 0.02:
                x = lerp(mx, x, shatter * 0.35) + (hsh(i, 3) - 0.5) * 120 * shatter; y = lerp(my, y, shatter * 0.35) + (hsh(i, 4) - 0.5) * 120 * shatter
            col = mix((150, 146, 140), (250, 244, 232), sh[i])
            if not front: col = mix(col, (60, 60, 80), 0.25)
            c.drawCircle(x, y, size[i] * (1.3 if k < 0.5 else 1.0), paint(col, 0.9))
    debris(False)
    if show_limit > 0:
        dashed_circle(c, cx, cy, er * 2.95, (255, 120, 110), 4, 0.8 * show_limit, phase=-t * 30, sy=tilt * 2.2 / 2.2 if False else 1.0)
    if planet == 'earth':
        earth(c, cx, cy, er, rot=t * 0.08)
    else:
        draw_planet(c, 'mars', cx, cy, er, rot=t * 0.05, glow=(255, 160, 120), halo=(255, 140, 100), light=(-0.65, -0.3, 0.70))
    debris(True)
    if shatter < 1 and ring < 0.05:
        a = 1 - shatter
        c.save(); c.translate(mx, my); c.rotate(math.degrees(moon_ang)); c.scale(1 + 0.45 * stretch, 1 - 0.18 * stretch); c.rotate(-math.degrees(moon_ang))
        moon_ball(c, 0, 0, 62, light=(-0.6, -0.4, 0.7), glow=0.2, a=a)
        if stretch > 0.4:
            rng = np.random.default_rng(5)
            for i in range(5):
                p = skia.Path(); a0 = rng.uniform(0, 6.28); x, y = 0, 0; p.moveTo(x, y)
                for j in range(4): a0 += rng.normal(0, 0.6); x += math.cos(a0) * 18; y += math.sin(a0) * 18; p.lineTo(x, y)
                c.drawPath(p, stroke((40, 30, 30), 3, (stretch - 0.4) * 1.6 * a))
        c.restore()


def phobos(c, x, y, s, t, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = smooth_closed([(-60, -10), (-44, -36), (-6, -42), (34, -34), (60, -8), (52, 26), (14, 40), (-30, 36), (-58, 18)])
    shade(c, p, (150, 126, 108), L_DAY, sz=70, ow=3, depth=0.9)
    c.save(); c.clipPath(p, doAntiAlias=True)
    for (cx_, cy_, r) in [(-30, -6, 16), (14, 10, 10), (34, -14, 7), (-8, 24, 6)]:
        c.drawOval(R.MakeXYWH(cx_ - r, cy_ - r * 0.8, 2 * r, 1.6 * r), paint((90, 74, 64), 0.8))
        c.drawArc(R.MakeXYWH(cx_ - r, cy_ - r * 0.8, 2 * r, 1.6 * r), 20, 140, False, stroke((200, 176, 156), 2.2, 0.8))
    c.restore()
    c.restore()


# ------------------------------------------------------------------ clock (18-hour day), fingernail, sneaky moon
def clock18(c, t, x, y, r, spin=1.0, hours=18):
    shade(c, circ(x, y, r * 1.1), (226, 40, 52), L_DAY, sz=r * 2.2, ow=5)
    c.drawCircle(x, y, r, paint((250, 248, 240))); c.drawCircle(x, y, r, stroke((40, 30, 30), 5))
    f = font('ant', r * 0.16)
    for i in range(hours):
        a = math.radians(-90 + 360 * i / hours)
        c.drawLine(x + math.cos(a) * r * 0.86, y + math.sin(a) * r * 0.86, x + math.cos(a) * r * 0.96, y + math.sin(a) * r * 0.96, stroke((40, 30, 30), 5))
        lab = str(hours if i == 0 else i)
        c.drawString(lab, x + math.cos(a) * r * 0.72 - f.measureText(lab) / 2, y + math.sin(a) * r * 0.72 + r * 0.06, f, paint((40, 30, 30)))
    ah = math.radians(-90 + t * 60 * spin); am = math.radians(-90 + t * 720 * spin)
    c.drawLine(x, y, x + math.cos(ah) * r * 0.45, y + math.sin(ah) * r * 0.45, stroke((40, 30, 30), 12))
    c.drawLine(x, y, x + math.cos(am) * r * 0.7, y + math.sin(am) * r * 0.7, stroke((226, 40, 52), 7))
    c.drawCircle(x, y, 12, paint((40, 30, 30)))


def fingernail(c, t, grow=0.0, x=560, y=1900):
    vgrad(c, [(0, (40, 30, 70)), (1, (20, 16, 40))])
    sun_glow(c, 540, 900, 700, (120, 90, 200), 0.4)
    finger = union(capsule((x, y + 200), (x, y - 760), 150, 140))
    shade(c, finger, SKIN, L_DAY, sz=300, ow=5, depth=0.6)
    for k in (-420, -330):
        c.drawArc(R.MakeXYWH(x - 110, y + k - 20, 220, 40), 200, 140, False, stroke(dark(SKIN, 0.3), 4, 0.5))
    nail = rrect(x - 100, y - 880 - grow * 70, 200, 330 + grow * 70, 70)
    shade(c, nail, (255, 214, 206), L_DAY, sz=200, ow=4, gloss=1.0)
    tip = rrect(x - 100, y - 880 - grow * 70, 200, 40 + grow * 70, 40)
    c.save(); c.clipPath(nail, doAntiAlias=True)
    c.drawPath(tip, paint((255, 252, 245)))
    c.restore()
    c.drawPath(nail, stroke(dark((255, 214, 206), 0.5), 4))


def sneaky_moon(c, x, y, r, t, look=-1.0):
    moon_ball(c, x, y, r, light=(-0.4, -0.3, 0.86), glow=0.3)
    for sx in (-1, 1):
        ex, ey = x + sx * r * 0.32, y - r * 0.08
        c.drawOval(R.MakeXYWH(ex - r * 0.16, ey - r * 0.2, r * 0.32, r * 0.4), paint((255, 255, 255)))
        c.drawOval(R.MakeXYWH(ex - r * 0.16, ey - r * 0.2, r * 0.32, r * 0.4), stroke((40, 30, 40), 4))
        c.drawCircle(ex + look * r * 0.08, ey + r * 0.04, r * 0.09, paint((30, 20, 30)))
        c.drawLine(ex - r * 0.17, ey - r * 0.3 + sx * r * 0.04, ex + r * 0.17, ey - r * 0.3 - sx * r * 0.04, stroke((60, 50, 60), 6))
    p = skia.Path(); p.moveTo(x - r * 0.2, y + r * 0.35); p.quadTo(x, y + r * 0.45, x + r * 0.22, y + r * 0.3)
    c.drawPath(p, stroke((60, 50, 60), 6))
