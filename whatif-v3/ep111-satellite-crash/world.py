"""Glow-lit world for the space-nuke episode: everything is lit by light sources (flash, aurora, lamps),
then bloom + grade + grain, then crisp UI on top. New look: silhouettes against a glowing sky."""
import math, numpy as np, cairo, cv2
W, H = 1080, 1920; CX = W // 2

def hx(h, a=1.0): return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (a,)
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3

def surface():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); return s, cairo.Context(s)
def to_np(s):
    a = np.ndarray((H, W, 4), np.uint8, s.get_data()).copy(); return a[:, :, [2, 1, 0]].astype(np.float32) / 255

def grad(c, stops, y0=0, y1=H):
    g = cairo.LinearGradient(0, y0, 0, y1)
    for p, col in stops: g.add_color_stop_rgb(p, *hx(col)[:3])
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()

def stars(c, T, n=260, seed=3, ymax=H, a=1.0):
    r = np.random.RandomState(seed)
    for k in range(n):
        x, y, s = r.uniform(0, W), r.uniform(0, ymax), r.uniform(.6, 2.6)
        tw = .55 + .45 * math.sin(T * r.uniform(1, 4) + k)
        c.arc(x, y, s, 0, 6.29); c.set_source_rgba(1, 1, 1, a * tw * r.uniform(.4, 1)); c.fill()

def glow(c, x, y, r, col, a=1.0):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *hx(col)[:3], a); g.add_color_stop_rgba(.25, *hx(col)[:3], a * .45); g.add_color_stop_rgba(1, *hx(col)[:3], 0)
    c.arc(x, y, r, 0, 6.29); c.set_source(g); c.fill()

def earth(c, cx, cy, r, T, night=.55, lights=1.0, belt=0.0, seed=5):
    # atmosphere halo
    g = cairo.RadialGradient(cx, cy, r * .95, cx, cy, r * 1.18)
    g.add_color_stop_rgba(0, .35, .7, 1, .9); g.add_color_stop_rgba(1, .2, .5, 1, 0); c.arc(cx, cy, r * 1.18, 0, 6.29); c.set_source(g); c.fill()
    c.save(); c.arc(cx, cy, r, 0, 6.29); c.clip()
    g = cairo.RadialGradient(cx - r * .35, cy - r * .4, r * .1, cx, cy, r * 1.05)
    g.add_color_stop_rgb(0, *hx('3FA9F5')[:3]); g.add_color_stop_rgb(.7, *hx('0D4C9C')[:3]); g.add_color_stop_rgb(1, *hx('06224A')[:3])
    c.rectangle(cx - r, cy - r, 2 * r, 2 * r); c.set_source(g); c.fill()
    rs = np.random.RandomState(seed); rot = T * .02
    for k in range(9):                                       # continents: soft blobs that drift with rotation
        a0 = rs.uniform(0, 6.28) + rot; la = rs.uniform(-.9, .9)
        px = cx + r * math.sin(a0) * math.cos(la); py = cy + r * math.sin(la) * .95
        if math.cos(a0) < -.1: continue
        for j in range(6):
            bx, by, br = px + rs.uniform(-.18, .18) * r, py + rs.uniform(-.12, .12) * r, rs.uniform(.06, .14) * r
            c.arc(bx, by, br, 0, 6.29); c.set_source_rgba(*hx(('3E9B4F', '7DB35A', 'C9B37A')[j % 3])[:3], .95); c.fill()
    for k in range(7):                                       # clouds
        y = cy + rs.uniform(-.8, .8) * r; x = cx + ((rs.uniform(-1, 1) + T * .01) % 2 - 1) * r
        c.save(); c.translate(x, y); c.scale(1, .25); c.arc(0, 0, rs.uniform(.15, .35) * r, 0, 6.29); c.restore(); c.set_source_rgba(1, 1, 1, .35); c.fill()
    # night side shading + city lights
    g = cairo.LinearGradient(cx - r, 0, cx + r, 0)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1 - night, 0, 0, .02, 0); g.add_color_stop_rgba(min(1, 1.25 - night), 0, 0, .03, .88); g.add_color_stop_rgba(1, 0, 0, .03, .95)
    c.rectangle(cx - r, cy - r, 2 * r, 2 * r); c.set_source(g); c.fill()
    for k in range(260):
        u = rs.uniform(.15, 1) ** .7; x = cx + r * (1 - 2 * (1 - u) * night * 1.4); y = cy + rs.uniform(-.85, .85) * r
        if x > cx + r * .3 and (x - cx) ** 2 + (y - cy) ** 2 < r * r * .96:
            c.arc(x, y, rs.uniform(1, 3), 0, 6.29); c.set_source_rgba(1, .8, .4, .9 * lights * rs.uniform(.3, 1)); c.fill()
    c.restore()
    if belt > 0:                                             # artificial radiation belt (glowing torus)
        for k, (sc, a) in enumerate(((1.55, .5), (1.75, .35), (1.95, .2))):
            c.save(); c.translate(cx, cy); c.rotate(-.35); c.scale(sc * r, .42 * sc * r)
            c.arc(0, 0, 1, 0, 6.29); c.restore()
            c.set_source_rgba(1, .35, .65, a * belt); c.set_line_width(16 - k * 4 + 4 * math.sin(T * 3 + k)); c.stroke()

def satellite(c, x, y, s, T, dead=0.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot + dead * T * 3); c.scale(s, s)
    for d in (-1, 1):
        c.rectangle(d * 34 - (60 if d > 0 else -0) - (0 if d > 0 else 60), -18, 60, 36)
        c.set_source_rgba(*hx('2F5DA8' if dead < .5 else '444A55')); c.fill_preserve(); c.set_source_rgba(.85, .9, 1, 1); c.set_line_width(2); c.stroke()
    c.rectangle(-26, -22, 52, 44); c.set_source_rgba(*hx('E8C26A' if dead < .5 else '7A7468')); c.fill()
    c.restore()
    if dead < .5: glow(c, x + 30 * s, y, 18 * s, 'B8F1FF', .8)

def flash(c, x, y, T, t0, big=1.0):
    u = T - t0
    if u < 0: return
    a = math.exp(-u * 1.6) * big
    glow(c, x, y, 900 * eout(u / .35) * big, 'FFF3C4', .95 * a)
    glow(c, x, y, 260 * big, 'FFFFFF', a)
    c.set_source_rgba(1, .95, .8, .55 * a); c.set_line_width(5)
    c.move_to(x - 700, y); c.line_to(x + 700, y); c.stroke()
    c.move_to(x, y - 300); c.line_to(x, y + 300); c.set_line_width(3); c.stroke()

def aurora(c, T, a=1.0, cols=('FF3355', '33FF99', 'FF66CC'), top=250, bot=1150):
    for b, col in enumerate(cols):
        for i in range(0, W + 20, 12):
            x = i + 40 * math.sin(i * .006 + T * .7 + b * 2)
            hgt = (bot - top) * (.55 + .35 * math.sin(i * .011 + T * .9 + b))
            y1 = bot - b * 70 + 30 * math.sin(i * .02 + T)
            g = cairo.LinearGradient(0, y1 - hgt, 0, y1)
            g.add_color_stop_rgba(0, *hx(col)[:3], 0); g.add_color_stop_rgba(.75, *hx(col)[:3], .16 * a); g.add_color_stop_rgba(1, *hx(col)[:3], 0)
            c.rectangle(x, y1 - hgt, 13, hgt); c.set_source(g); c.fill()

def palm(c, x, y, s, T, col=(0.02, 0.02, 0.05)):
    c.save(); c.translate(x, y); c.scale(s, s); c.set_source_rgba(*col, 1)
    c.move_to(-14, 0); c.curve_to(10, -220, -20, -420, 20, -560); c.line_to(44, -556); c.curve_to(10, -420, 40, -220, 14, 0); c.close_path(); c.fill()
    for k in range(8):
        ang = -3.0 + k * .43 + .04 * math.sin(T * 1.5 + k)
        ex, ey = 32 + 250 * math.cos(ang), -560 + 250 * math.sin(ang) + 70
        c.move_to(32, -560); c.curve_to(32 + 120 * math.cos(ang), -620 + 120 * math.sin(ang), ex - 20 * math.cos(ang), ey - 60, ex, ey)
        c.curve_to(ex - 30, ey - 50, 32 + 110 * math.cos(ang), -590 + 110 * math.sin(ang), 32, -548); c.fill()
    c.restore()

def roof_people(c, y, T, n=5, col=(0.02, 0.02, 0.05)):
    c.set_source_rgba(*col, 1); c.rectangle(0, y, W, H - y); c.fill()
    c.move_to(0, y); c.line_to(W, y - 40); c.line_to(W, y + 10); c.line_to(0, y + 10); c.fill()
    for k in range(n):
        x = 140 + k * 200 + (30 if k % 2 else 0); h = (1.0 if k % 2 else .85) * 1.0
        c.save(); c.translate(x, y - 10 - k * 8); c.scale(h, h)
        c.arc(0, -300, 42, 0, 6.29); c.fill()
        c.move_to(-58, -240); c.curve_to(-70, -120, -60, -40, -50, 0); c.line_to(50, 0); c.curve_to(60, -40, 70, -120, 58, -240); c.close_path(); c.fill()
        if k in (1, 3):                                      # arm pointing up at the sky
            c.move_to(40, -230); c.line_to(120, -380 - 10 * math.sin(T * 2 + k)); c.set_line_width(26); c.set_line_cap(1); c.stroke()
        c.restore()

def street(c, T, lit, y=1500):
    grad(c, [(0, '0A0F2E'), (.6, '1B1446'), (1, '2A1A3A')])
    for k in range(5):
        x = 120 + k * 210; s = .7 + k * .08
        c.set_source_rgba(.03, .03, .06, 1); c.rectangle(x - 7, y - 560 * s, 14, 560 * s); c.fill()
        c.rectangle(x - 7, y - 560 * s, 70, 12); c.fill()
        on = lit[k] if isinstance(lit, (list, tuple)) else lit
        if on > 0:
            glow(c, x + 60, y - 545 * s, 220, 'FFC266', .6 * on)
            g = cairo.LinearGradient(0, y - 540 * s, 0, y)
            g.add_color_stop_rgba(0, 1, .8, .45, .35 * on); g.add_color_stop_rgba(1, 1, .8, .45, 0)
            c.move_to(x + 45, y - 540 * s); c.line_to(x - 60, y); c.line_to(x + 180, y); c.line_to(x + 75, y - 540 * s); c.close_path(); c.set_source(g); c.fill()
        c.arc(x + 60, y - 535 * s, 12, 0, 6.29); c.set_source_rgba(1, .9, .6, .3 + .7 * on); c.fill()
    c.set_source_rgba(.02, .02, .04, 1); c.rectangle(0, y, W, H - y); c.fill()

def post(img, T, bloom=1.0, sat=1.2, grain=.035, vig=.5, seed=None):
    """bloom (bright-pass blur, added), saturation, vignette, film grain."""
    br = np.clip(img - .72, 0, None)
    small = cv2.resize(br, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    b = cv2.GaussianBlur(small, (0, 0), 18) * .9 + cv2.GaussianBlur(small, (0, 0), 6) * .6
    img = img + cv2.resize(b, (W, H)) * bloom
    gray = img.mean(2, keepdims=True); img = gray + (img - gray) * sat
    yy, xx = np.mgrid[0:H, 0:W]; d = ((xx - CX) / W) ** 2 + ((yy - H / 2) / H) ** 2
    img = img * (1 - vig * np.clip(d * 2.2, 0, 1))[..., None]
    r = np.random.RandomState(int(T * 30) if seed is None else seed)
    img = img + r.normal(0, grain, (H // 2, W // 2, 1)).repeat(2, 0).repeat(2, 1)
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)

# ---------- photoreal-ish procedural Earth (numpy sphere, lit, rotating)
def _fbm(h, w, seed, oct=6, base=4):
    r = np.random.RandomState(seed); out = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    for o in range(oct):
        g = r.rand(base * 2 ** o, 2 * base * 2 ** o).astype(np.float32)
        g = np.concatenate([g, g[:, :1]], 1)
        out += cv2.resize(g, (w, h), interpolation=cv2.INTER_CUBIC) * amp; tot += amp; amp *= .5
    return out / tot
_TEX = {}
def earth_tex():
    if 'c' in _TEX: return _TEX['c'], _TEX['cl'], _TEX['land']
    h, w = 512, 1024; n = _fbm(h, w, 7); land = np.clip((n - .53) * 12, 0, 1)
    lat = np.abs(np.linspace(-1, 1, h))[:, None]
    ocean = np.stack([.03 + .05 * n, .18 + .2 * n, .42 + .25 * n], -1)
    m = _fbm(h, w, 11, 5)[..., None]
    green = np.array([.16, .42, .15]) * (1 - m) + np.array([.62, .55, .32]) * m
    ice = np.clip((lat - .82) * 8, 0, 1)[..., None]
    col = ocean * (1 - land[..., None]) + green * land[..., None]; col = col * (1 - ice) + .92 * ice
    cl = np.clip((_fbm(h, w, 23, 5, 12) - .5) * 2.6, 0, 1) * .8
    _TEX.update(c=col.astype(np.float32), cl=cl.astype(np.float32), land=land); return _TEX['c'], _TEX['cl'], _TEX['land']

def earth_np(img, cx, cy, r, T, light=(-.6, -.45, .66), lights=1.0, spin=.03, aura=1.0):
    col, cl, land = earth_tex(); th, tw = cl.shape
    x0, x1, y0, y1 = int(max(0, cx - r * 1.25)), int(min(W, cx + r * 1.25)), int(max(0, cy - r * 1.25)), int(min(H, cy + r * 1.25))
    if x1 <= x0 or y1 <= y0: return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32); nx = (xx - cx) / r; ny = (yy - cy) / r; d2 = nx * nx + ny * ny
    inside = d2 < 1; nz = np.sqrt(np.clip(1 - d2, 0, 1))
    lon = (np.arctan2(nx, nz) / (2 * np.pi) + .5 + T * spin) % 1; lat = np.arcsin(np.clip(ny, -1, 1)) / np.pi + .5
    u = (lon * (tw - 1)).astype(np.int32); v = (lat * (th - 1)).astype(np.int32)
    base = col[v, u]; c2 = cl[v, (u + int(T * 6)) % tw][..., None]
    L = np.array(light, np.float32); L /= np.linalg.norm(L)
    lam = np.clip(nx * L[0] + ny * L[1] + nz * L[2], -1, 1)[..., None]
    day = np.clip(lam * 1.25 + .08, 0, 1)
    surf = (base * (1 - c2 * .8) + c2 * .78) * (.05 + day * .95)
    spec = np.clip(lam, 0, 1) ** 24 * (1 - land[v, u][..., None]) * .55
    night = np.clip(-lam * 3, 0, 1) * land[v, u][..., None] * (_fbm(th, tw, 31, 4)[v, u][..., None] > .55) * np.array([1., .72, .35]) * .9 * lights
    rim = (1 - nz)[..., None] ** 3 * np.array([.3, .6, 1.]) * (.4 + .6 * day)
    sph = surf + spec + night + rim
    halo = np.clip(1 - (np.sqrt(d2) - 1) / .18, 0, 1) ** 2 * (~inside) * aura
    reg = img[y0:y1, x0:x1]
    reg[:] = np.where(inside[..., None], sph, reg + halo[..., None] * np.array([.25, .55, 1.]) * (.3 + .7 * np.clip(nx * L[0] + ny * L[1] + .3, 0, 1))[..., None])

def human(c, x, y, s, T, pose='stand', hair=0, k=0):
    """clean silhouette: head, neck, shoulders, torso, arms, legs (filled with the current source)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.translate(0, -330); c.scale(.86, 1); c.arc(0, 0, 40, 0, 6.29); c.restore(); c.fill()
    if hair == 1: c.arc(18, -360, 24, 0, 6.29); c.fill()                       # bun
    if hair == 2: c.move_to(-40, -340); c.curve_to(-50, -280, -46, -250, -30, -235); c.line_to(30, -235); c.curve_to(46, -250, 50, -280, 40, -340); c.fill()
    c.rectangle(-14, -295, 28, 30); c.fill()
    c.move_to(-62, -262); c.curve_to(-30, -275, 30, -275, 62, -262); c.curve_to(70, -200, 60, -120, 48, -110)
    c.line_to(-48, -110); c.curve_to(-60, -120, -70, -200, -62, -262); c.close_path(); c.fill()
    c.move_to(-46, -112); c.line_to(-40, 0); c.line_to(-8, 0); c.line_to(0, -90); c.line_to(8, 0); c.line_to(40, 0); c.line_to(46, -112); c.close_path(); c.fill()
    c.set_line_cap(1); c.set_line_width(24)
    if pose == 'point':
        c.move_to(52, -250); c.line_to(105, -330 - 8 * math.sin(T * 2 + k)); c.line_to(140, -420 - 12 * math.sin(T * 2 + k)); c.stroke()
    elif pose == 'cover':                                                    # hands over mouth
        c.move_to(-56, -250); c.curve_to(-80, -200, -40, -230, -14, -300); c.stroke(); c.move_to(56, -250); c.curve_to(80, -200, 40, -230, 14, -300); c.stroke()
    else:
        c.move_to(-58, -250); c.curve_to(-74, -190, -70, -150, -64, -120); c.stroke(); c.move_to(58, -250); c.curve_to(74, -190, 70, -150, 64, -120); c.stroke()
    c.restore()

def roof_people2(c, y, T, col=(0.015, 0.01, 0.03)):
    c.set_source_rgba(*col, 1)
    c.move_to(0, y); c.line_to(W, y - 30); c.line_to(W, H); c.line_to(0, H); c.close_path(); c.fill()
    for k in range(13): c.rectangle(20 + k * 82, y - 70 - k * 2.3, 8, 70); c.fill()
    c.rectangle(0, y - 78, W, 8); c.fill()
    for (x, s, pose, hair) in ((150, 1.05, 'stand', 2), (330, 1.15, 'point', 0), (560, .95, 'cover', 1), (760, 1.2, 'stand', 0), (930, 1.0, 'point', 2)):
        human(c, x, y - 4 - x * .028, s, T, pose, hair, int(x))
