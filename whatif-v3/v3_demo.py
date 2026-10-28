"""v3 look test: 'What if the Moon came closer?' opener, three cinematic shots with the new hero."""
import sys, os, math, time, subprocess
import skia
from hero import *
from cine import *

OUTD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hero_demo')
OUTFIT = os.environ.get('OUTFIT', 'explorer')

# dusk palette
SKY = [(0.0, (18, 28, 66)), (0.30, (52, 50, 104)), (0.52, (132, 82, 122)), (0.66, (226, 120, 96)), (0.74, (255, 170, 104)), (1.0, (255, 196, 128))]
LIGHT_WIDE = Light(key=(-0.45, -0.9), key_col=(255, 226, 196), ka=0.24, tint=(168, 150, 206), sa=0.95,
                   rim=(-0.6, -0.8), rim_col=(200, 220, 255), ra=0.9, ground=(14, 10, 24), ga=0.6, amb=(0.86, 0.84, 0.94))

GR_WIDE = Grass(1178, H + 60, n=2200, seed=5, h_near=210, h_far=10, cols=((26, 60, 40), (78, 132, 66)), tip=(255, 206, 150))
GR_LOW = Grass(1440, H + 160, n=3200, seed=9, h_near=480, h_far=24, cols=((22, 62, 38), (80, 136, 62)), tip=(255, 206, 150))

_CACHE = {}


def layer(c, d, cam, fn):
    """Parallax layer: d=0 static sky, d=1 moves with the subject plane."""
    z, px, py = cam
    zz = 1 + (z - 1) * d
    c.save(); c.translate(W / 2, H / 2); c.scale(zz, zz); c.translate(-W / 2 - px * d, -H / 2 - py * d)
    fn(); c.restore()


def landscape(c, t, cam, moon_r, moon_c=(540, 880), horizon=1060, blur_far=2.0, blur_mid=1.0, grass=GR_WIDE, wind=1.0, gust=0.0, moon_warm=0.12):
    mx, my = moon_c
    def sky():
        vgrad(c, SKY, -200, horizon + 140)
        stars(c, 4, 700, 90, 0.7, t)
        cloud_streaks(c, t, 2, 300, 760, (70, 58, 110), 0.5, n=6, drift=8, lit=(255, 150, 120))
    layer(c, 0.05, cam, sky)
    def moon():
        draw_moon(c, mx, my, moon_r, glow=(255, 226, 206), ga=0.75, warm=moon_warm, low_haze=(255, 168, 120), lha=0.55)
        cloud_streaks(c, t, 8, my - moon_r * 0.1, my + moon_r * 0.7, (96, 64, 112), 0.6, n=4, drift=14, lit=(255, 170, 130))
    layer(c, 0.12, cam, moon)
    rim = ((mx - W / 2) / 1000, -1)
    def far():
        p = _CACHE.setdefault(('r1', horizon), crown_row_path(horizon + 20, 31, h=70, spacing=46, conifer=0.25))
        rim_fill(c, p, (150, 112, 150), (196, 130, 140), horizon - 70, horizon + 30, (255, 200, 170), 0.18, rim, 3)
        haze(c, horizon + 22, 40, (255, 170, 136), 0.5)
    layer(c, 0.25, cam, lambda: blurred(c, blur_far, far, bounds=R.MakeLTRB(-400, horizon - 260, W + 400, horizon + 200)))
    def mid():
        p = _CACHE.setdefault(('r2', horizon), crown_row_path(horizon + 70, 17, h=115, spacing=60, conifer=0.18))
        rim_fill(c, p, (92, 84, 120), (104, 86, 116), horizon - 60, horizon + 80, (230, 220, 255), 0.22, rim, 3)
        haze(c, horizon + 72, 46, (226, 156, 156), 0.42)
    layer(c, 0.38, cam, lambda: blurred(c, blur_mid * 1.4, mid, bounds=R.MakeLTRB(-400, horizon - 260, W + 400, horizon + 260)))
    def near():
        p = _CACHE.setdefault(('r3', horizon), crown_row_path(horizon + 125, 23, h=170, spacing=78, conifer=0.12, tall=0.2))
        rim_fill(c, p, (48, 58, 78), (34, 40, 54), horizon - 60, horizon + 130, (210, 222, 255), 0.3, rim, 4)
        haze(c, horizon + 128, 34, (190, 140, 160), 0.45)
    layer(c, 0.5, cam, lambda: blurred(c, blur_mid, near, bounds=R.MakeLTRB(-400, horizon - 300, W + 400, horizon + 320)))
    def field():
        ground_tex(c, horizon + 118, H + 100, (98, 104, 86), (20, 34, 26), seed=4, blotch=(10, 20, 16), ba=0.35)
        grass.draw(c, t, wind=wind, light=(255, 196, 150), band_range=range(0, 4), gust=gust)
        haze(c, horizon + 150, 40, (200, 150, 170), 0.35)
    layer(c, 0.85, cam, field)


def hero_in_field(c, t, cam, x, y, s, pose, face, L, grass=GR_WIDE, wind=1.0, gust=0.0, **kw):
    def fg():
        r = draw_hero(c, x, y, s, pose, face, outfit=OUTFIT, L=L, t=t, **kw)
        # near grass in front of the feet integrates the character with the ground
        grass.draw(c, t, wind=wind, light=(255, 196, 150), band_range=range(4, 6), gust=gust)
        return r
    out = {}
    layer(c, 1.0, cam, lambda: out.setdefault('r', fg()))
    return out.get('r')


# ------------------------------------------------------------------ shots
def shot_wide(c, t):
    u = t
    cam = (1.0 + 0.06 * eio(cl(u / 4.3)), 0, -30 * eio(cl(u / 4.3)))
    moon_r = 250 + 40 * eio(cl((u - 0.5) / 3.5))
    landscape(c, t, cam, moon_r)
    layer(c, 0.9, cam, lambda: fireflies(c, t, 26, 3, (40, 1180, 1040, 1700), size=3.4))
    look_up = cl((u - 0.9) / 0.4)
    face = Face('open', 'o' if u > 1.4 else 'smile', 'up' if u > 1.4 else 'none', look=(0, -look_up))
    pose = lerp_pose(POSES['stand'], (0, -10, 205, 15, 155, -15, 186, 0, 174, 0), look_up)
    hero_in_field(c, t, cam, 540, 1660, 1.32, pose, face, LIGHT_WIDE, blink=(1.0 < u < 1.1), sweat=cl((u - 2.6) / 0.3) * 0.0)
    caption(c, t, 0.35, [('WHAT IF THE MOON', WHITE)], 390, size=92)
    caption(c, t, 0.9, [('CAME ', WHITE), ('CLOSER?', YEL)], 545, size=170)


def bokeh(c, t, n, seed, box, col=(255, 214, 150), a=0.5, rmin=18, rmax=46):
    x0, y0, x1, y1 = box
    for i in range(n):
        ph = hsh(i, seed) * 6.283
        x = lerp(x0, x1, hsh(i, seed + 1)) + math.sin(t * 0.4 + ph) * 20
        y = lerp(y0, y1, hsh(i, seed + 2)) + math.cos(t * 0.3 + ph) * 14
        r = lerp(rmin, rmax, hsh(i, seed + 3))
        k = 0.55 + 0.45 * math.sin(t * (0.8 + hsh(i, seed + 4)) + ph)
        c.drawCircle(x, y, r, paint(shader=rad(x, y, r, [argb(col, a * k * 0.55), argb(col, a * k * 0.7), argb(col, 0)], [0, 0.85, 1]), blend=SCREEN))


def leaves(c, t, n, seed, wind=900, col=(120, 150, 70), a=1.0, y0=300, y1=1700, size=14):
    for i in range(n):
        ph = hsh(i, seed) * 6.283
        sp = wind * (0.6 + 0.8 * hsh(i, seed + 1))
        x = (hsh(i, seed + 2) * (W + 600) + t * sp) % (W + 600) - 300
        y = lerp(y0, y1, hsh(i, seed + 3)) + math.sin(t * 3 + ph) * 60 - t * 40
        ang = t * 400 * (0.5 + hsh(i, seed + 4)) + ph * 57
        sz = size * (0.6 + 0.9 * hsh(i, seed + 5))
        c.save(); c.translate(x, y); c.rotate(ang); c.scale(1, 0.35 + 0.65 * abs(math.sin(t * 5 + ph)))
        lp = skia.Path(); lp.moveTo(-sz, 0); lp.quadTo(0, -sz * 0.6, sz, 0); lp.quadTo(0, sz * 0.6, -sz, 0); lp.close()
        cc = mix(col, (200, 150, 60), hsh(i, seed + 6) * 0.6)
        c.drawPath(lp, paint(cc, a)); c.drawLine(-sz, 0, sz, 0, stroke(dark(cc, 0.4), 1.2, a))
        c.restore()


LIGHT_CU = Light(key=(-0.55, -0.75), key_col=(255, 226, 200), ka=0.26, tint=(170, 148, 204), sa=0.95,
                 rim=(0.35, -1.0), rim_col=(255, 232, 210), ra=1.0, ground=(14, 10, 24), ga=0.0, amb=(0.9, 0.88, 0.96))


def shot_close(c, t):
    u = t
    def bg():
        landscape(c, t + 4.3, (1.0, 0, 0), 430, moon_c=(540, 760), horizon=1240, blur_far=0, blur_mid=0, moon_warm=0.1)
    blurred(c, 11, bg)
    bokeh(c, t, 14, 21, (60, 1150, 1020, 1750), a=0.5)
    z = 1.0 + 0.05 * eo(cl(u / 4.0))
    c.save(); c.translate(540, 1000); c.scale(z, z); c.translate(-540, -1000)
    pt = cl((u - 1.25) / 0.25)
    pose = lerp_pose((-2, -8, 205, 15, 158, -15, 186, 0, 174, 0), (0, -4, 207, 163, 153, -163, 186, 0, 174, 0), eback(pt))
    if u < 1.25: face = Face('wide', 'o', 'up', look=(0, -0.6))
    else: face = Face('wide', 'teeth', 'worried', look=(0.6, -1))
    jolt = math.exp(-u / 0.12) * 0.06
    draw_hero(c, 540, 2050, 3.6, pose, face, outfit=OUTFIT, L=LIGHT_CU, t=t, squash=1 + jolt, sweat=cl((u - 1.6) / 0.25),
              hands=('open', 'open') if u > 1.2 else ('relaxed', 'relaxed'), shadow=0, arm_over='both' if u > 1.3 else False)
    c.restore()
    def fg():
        GR_WIDE.draw(c, t, wind=1.2, light=(255, 196, 150), band_range=range(5, 6))
    c.save(); c.translate(0, 120); c.scale(1.0, 1.25)
    blurred(c, 9, fg, 0.9)
    c.restore()
    caption(c, t, 0.35, [('IT WOULD LOOK', WHITE)], 390, size=92)
    caption(c, t, 0.75, [('10X ', YEL), ('BIGGER', WHITE)], 550, size=170)


LIGHT_LOW = Light(key=(-0.5, -0.6), key_col=(255, 214, 180), ka=0.24, tint=(160, 138, 200), sa=1.0,
                  rim=(0.0, -1.0), rim_col=(255, 236, 214), ra=1.2, ground=(14, 10, 24), ga=0.5, amb=(0.84, 0.82, 0.94))


def shot_low(c, t):
    u = t
    gust = cl((u - 0.6) / 0.6) * 0.8
    shx = math.sin(u * 37) * 7 * gust + math.sin(u * 23) * 4 * gust
    cam = (1.0 + 0.04 * u / 3.7, 0, 0)
    c.save(); c.translate(shx, shx * 0.5)
    def sky_low():
        landscape(c, t + 8.0, cam, 560 + 30 * u / 3.7, moon_c=(540, 700), horizon=1330, blur_far=1.5, blur_mid=1.0,
                  grass=GR_LOW, wind=1.0 + gust * 2, gust=gust, moon_warm=0.2)
    sky_low()
    leaves(c, t, 16 if u > 0.6 else 0, 7, wind=900, a=0.95)
    braced = cl((u - 0.7) / 0.3)
    pose = lerp_pose((0, -6, 205, 15, 155, -15, 186, 0, 174, 0), (-10, 6, 222, 40, 20, -112, 198, 6, 166, -4), eback(braced))
    face = Face('squint', 'teeth', 'angry') if braced > 0.5 else Face('open', 'flat', 'worried', look=(0, -1))
    layer(c, 1.0, cam, lambda: draw_hero(c, 540, 1740, 2.15, pose, face, outfit=OUTFIT, L=LIGHT_LOW, t=t,
                                         hands=('fist', 'fist'), sweat=braced, arm_over=braced > 0.3))
    def fg():
        GR_LOW.draw(c, t, wind=1.0 + gust * 2.5, light=(255, 196, 150), band_range=range(3, 6), gust=gust)
    blurred(c, 6, fg, bounds=R.MakeLTRB(-200, 1200, W + 200, H + 200))
    leaves(c, t + 3, 6 if u > 0.6 else 0, 19, wind=1400, a=0.9, size=34)
    c.restore()
    caption(c, t, 0.3, [('AND TIDES', WHITE)], 420, size=96)
    caption(c, t, 0.65, [('1000X ', YEL), ('STRONGER', WHITE)], 580, size=170)


SHOTS = [(0.0, 4.3, shot_wide), (4.3, 8.3, shot_close), (8.3, 12.2, shot_low)]
DURATION = 12.2


def render(t, post):
    S = _CACHE.setdefault('surf', skia.Surface(W, H))
    c = S.getCanvas(); c.clear(skia.ColorBLACK)
    for i, (t0, t1, fn) in enumerate(SHOTS):
        if t0 <= t < t1:
            u = t - t0
            c.save()
            if i > 0 and u < 0.3:
                z = 1 + 0.08 * (1 - eo(u / 0.3)); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
            fn(c, u); c.restore()
            if i > 0 and u < 0.16:
                c.drawRect(FULLR, paint((255, 240, 225), 0.55 * (1 - u / 0.16), blend=PLUS))
    if t < 0.25:
        c.drawRect(FULLR, paint((0, 0, 0), 1 - t / 0.25))
    img = post.apply(S.makeImageSnapshot(), t)
    return img


if __name__ == '__main__':
    post = Post()
    mode = sys.argv[1]
    if mode == 'still':
        for v in sys.argv[2:]:
            st = time.time(); img = render(float(v), post); print('t=%s %.2fs' % (v, time.time() - st))
            img.save(os.path.join(OUTD, 'v3_%05.2f.png' % float(v)), skia.kPNG)

    if mode == 'video':
        f0, f1, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', '%dx%d' % (W, H), '-r', '30',
               '-i', '-', '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14',
               '-profile:v', 'high', '-threads', '1', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', out]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        st = time.time()
        for f in range(f0, f1):
            p.stdin.write(render(f / 30, post).toarray().tobytes())
            if (f - f0) % 30 == 0: print('frame', f, '%.1fs' % (time.time() - st), flush=True)
        p.stdin.close(); p.wait(); print('done', out, time.time() - st)
