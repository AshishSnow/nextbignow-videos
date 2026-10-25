"""NESSA — FreshNestHub's stick-figure host. Pure PIL, supersampled, returns RGBA + feet anchor.

nessa(pose="stand", expr="smile", t=0.0, scale=1.0, mouth=0.0, look=(0,0), tilt=0.0, prop=None, flip=False)
  -> (PIL.Image RGBA, (ax, ay))   paste so that (ax, ay) lands on the floor point.
"""
import math
from PIL import Image, ImageDraw

SS = 3
INK = (14, 14, 18, 255)
SKIN = (255, 255, 255, 255)
JADE = (0, 178, 114, 255)
JADE_D = (0, 120, 78, 255)
PINK = (255, 178, 196, 255)
TONGUE = (240, 90, 110, 255)
LENS = (176, 226, 255, 255)
SWEAT = (90, 190, 255, 255)

# geometry (scale 1, y down, origin = point between feet)
HIP_Y, SH_Y, NECK_Y = -150, -305, -322
HEAD_R, HEAD_Y = 72, -400
UP, LO = 95, 90
LW, OW = 9, 7

# arm angles in degrees (0 = right, 90 = down). (left_upper, left_lower, right_upper, right_lower)
POSES = {
    "stand":   dict(arms=(122, 105, 58, 75), legs=24),
    "wave":    dict(arms=(-175, -110, 58, 75), legs=24, wave=True),
    "point":   dict(arms=(122, 105, -4, -8), legs=30),
    "pointup": dict(arms=(122, 105, -55, -82), legs=24),
    "shock":   dict(arms=(140, -72, 40, -108), legs=36),
    "cheer":   dict(arms=(-128, -112, -52, -68), legs=44, hop=True),
    "think":   dict(arms=(150, 58, 50, -121), legs=20),
    "whisper": dict(arms=(122, 105, 20, -127), legs=20),
    "shrug":   dict(arms=(165, -125, 15, -55), legs=28),
    "hips":    dict(arms=(150, 58, 30, 122), legs=34),
    "magnify": dict(arms=(122, 105, 8, -48), legs=30, prop="magnifier"),
    "mirror":  dict(arms=(122, 105, 12, -60), legs=26, prop="mirror"),
    "cover":   dict(arms=(150, -60, 30, -120), legs=18),
    "cradle":  dict(arms=(115, -10, 65, 190), legs=26),
    "wipe":    dict(arms=(122, 105, -10, -136), legs=24, prop="pad"),
    "stretch": dict(arms=(-128, -112, -52, -68), legs=30),
}

STYLES = {
    "nessa": dict(hair="pony", hc=(14, 14, 18, 255), acc=(0, 178, 114, 255), dress=(0, 178, 114, 255)),
    "mom":   dict(hair="bun", hc=(60, 34, 22, 255), acc=(255, 96, 120, 255), dress=(255, 104, 96, 255)),
    "guy":   dict(hair="short", hc=(14, 14, 18, 255), acc=None, dress=None, shirt=(40, 120, 255, 255)),
    "guy2":  dict(hair="short", hc=(92, 54, 30, 255), acc=None, dress=None, shirt=(255, 170, 0, 255)),
    "bald":  dict(hair="none", hc=None, acc=None, dress=None, shirt=(150, 90, 255, 255)),
    "girl":  dict(hair="long", hc=(120, 62, 28, 255), acc=(255, 210, 0, 255), dress=(150, 90, 255, 255)),
    "girl2": dict(hair="pony", hc=(200, 120, 40, 255), acc=(40, 120, 255, 255), dress=(255, 120, 190, 255)),
}


def _pt(o, ang, ln):
    a = math.radians(ang)
    return (o[0] + math.cos(a) * ln, o[1] + math.sin(a) * ln)


class _Pen:
    def __init__(self, d, ox, oy, k):
        self.d, self.ox, self.oy, self.k = d, ox, oy, k

    def P(self, p):
        return (self.ox + p[0] * self.k, self.oy + p[1] * self.k)

    def line(self, a, b, w=LW, fill=INK):
        A, B = self.P(a), self.P(b)
        ww = max(1, int(w * self.k))
        self.d.line([A, B], fill=fill, width=ww)
        for q in (A, B):
            r = ww / 2
            self.d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=fill)

    def circle(self, c, r, fill=None, outline=None, w=OW):
        C = self.P(c)
        R = r * self.k
        self.d.ellipse([C[0] - R, C[1] - R, C[0] + R, C[1] + R], fill=fill, outline=outline,
                       width=max(1, int(w * self.k)) if outline else 0)

    def ellipse(self, c, rx, ry, fill=None, outline=None, w=OW):
        C = self.P(c)
        self.d.ellipse([C[0] - rx * self.k, C[1] - ry * self.k, C[0] + rx * self.k, C[1] + ry * self.k], fill=fill,
                       outline=outline, width=max(1, int(w * self.k)) if outline else 0)

    def poly(self, pts, fill=None, outline=None, w=OW):
        P = [self.P(p) for p in pts]
        self.d.polygon(P, fill=fill)
        if outline:
            ww = max(1, int(w * self.k))
            self.d.line(P + [P[0]], fill=outline, width=ww, joint="curve")

    def arc(self, c, rx, ry, a0, a1, w=5, fill=INK):
        C = self.P(c)
        self.d.arc([C[0] - rx * self.k, C[1] - ry * self.k, C[0] + rx * self.k, C[1] + ry * self.k], a0, a1, fill=fill,
                   width=max(1, int(w * self.k)))


def _head(expr, t, mouth, look, k, style="nessa"):
    """Head layer (own canvas) so it can tilt. Returns RGBA image centered on head center."""
    ST = STYLES[style]
    HC = ST["hc"]
    S = int(360 * k)
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    p = _Pen(d, S / 2, S / 2, k)
    R = HEAD_R
    sway = math.sin(t * 3.2) * 7
    # ponytail (behind head): smooth tapered bezier
    base = (R * 0.6, -R * 0.66)
    c1 = (R * 1.32, -R * 0.92)
    c2 = (R * 1.55 + sway, -R * 0.05)
    tip = (R * 1.22 + sway * 1.4, R * 0.78)
    if ST["hair"] == "pony":
        for i in range(48):
            u = i / 47
            x = (1-u)**3*base[0] + 3*(1-u)**2*u*c1[0] + 3*(1-u)*u*u*c2[0] + u**3*tip[0]
            y = (1-u)**3*base[1] + 3*(1-u)**2*u*c1[1] + 3*(1-u)*u*u*c2[1] + u**3*tip[1]
            p.circle((x, y), 17 * (1 - u) ** 0.8 + 3.5, fill=HC)
    elif ST["hair"] == "bun":
        p.circle((R * 0.15, -R * 1.02), R * 0.42, fill=HC, outline=INK, w=5)
    elif ST["hair"] == "long":
        p.poly([(-R * 1.02, -R * 0.2), (-R * 1.1, R * 1.05), (-R * 0.55, R * 1.1), (R * 0.55, R * 1.1), (R * 1.1, R * 1.05), (R * 1.02, -R * 0.2)],
               fill=HC)
    # head
    p.circle((0, 0), R, fill=SKIN, outline=INK)
    # hair cap: black crescent across the top + side-swept fringe
    cap = Image.new("L", (S, S), 0)
    cd = ImageDraw.Draw(cap)
    C = (S / 2, S / 2)
    rr = (R - 2) * k
    cd.ellipse([C[0] - rr, C[1] - rr, C[0] + rr, C[1] + rr], fill=255)
    fx, fy, frx, fry = (7, 24, R + 3, R - 3) if ST["hair"] != "short" else (0, 34, R + 6, R - 6)
    cd.ellipse([C[0] + (fx - frx) * k, C[1] + (fy - fry) * k, C[0] + (fx + frx) * k, C[1] + (fy + fry) * k], fill=0)
    # little bang tip on the forehead
    cd.polygon([(C[0] - 44 * k, C[1] - 52 * k), (C[0] - 6 * k, C[1] - 50 * k), (C[0] - 30 * k, C[1] - 30 * k)], fill=255)
    if ST["hair"] != "none":
        im.paste(Image.new("RGBA", (S, S), HC), (0, 0), cap)
    p.circle((0, 0), R, outline=INK)
    # scrunchie / hair clip
    if ST["acc"] and ST["hair"] == "pony":
        p.ellipse((base[0] + 2, base[1] + 2), 11, 14, fill=ST["acc"], outline=INK, w=4)
    elif ST["acc"]:
        p.ellipse((-R * 0.55, -R * 0.62), 12, 9, fill=ST["acc"], outline=INK, w=4)

    lx, ly = look[0] * 9, look[1] * 7
    E = [(-25 + lx, 6 + ly), (25 + lx, 6 + ly)]
    blink = (t % 3.7) < 0.12
    # blush
    for s in (-1, 1):
        p.ellipse((s * 42, 30), 13, 7, fill=PINK)

    def eyes_dot(sc=1.0, glint=True):
        for i, (ex, ey) in enumerate(E):
            if blink:
                p.arc((ex, ey + 2), 11, 6, 200, 340, w=5)
                continue
            p.ellipse((ex, ey), 9.5 * sc, 13 * sc, fill=INK)
            if glint:
                p.circle((ex - 3 * sc, ey - 5 * sc), 3.4 * sc, fill=SKIN)
            s = -1 if i == 0 else 1
            p.line((ex + s * 7 * sc, ey - 10 * sc), (ex + s * 15 * sc, ey - 17 * sc), w=3.5)
            p.line((ex + s * 10 * sc, ey - 5 * sc), (ex + s * 18 * sc, ey - 9 * sc), w=3.5)

    def brows(dy=-26, tilt_in=0, raise_one=False):
        for i, (ex, ey) in enumerate(E):
            s = -1 if i == 0 else 1
            yy = ey + dy - (8 if raise_one and i == 1 else 0)
            p.line((ex - 10, yy + (tilt_in if s < 0 else -tilt_in) * 0 + (tilt_in if s > 0 else 0)),
                   (ex + 10, yy + (tilt_in if s < 0 else 0)), w=4.5)

    M = (lx * 0.6, 36 + ly * 0.5)
    if expr in ("smile", "talk"):
        eyes_dot()
        if expr == "talk" and mouth > 0.08:
            h = 5 + 17 * mouth
            p.ellipse(M, 13 + 3 * mouth, h, fill=INK)
            p.ellipse((M[0], M[1] + h * 0.45), 8, h * 0.4, fill=TONGUE)
        else:
            p.arc((M[0], M[1] - 8), 15, 11, 20, 160, w=5)
    elif expr == "wow":
        eyes_dot(1.25)
        brows(-34)
        p.ellipse(M, 9, 12 + 4 * mouth, fill=INK)
    elif expr == "shock":
        for ex, ey in E:
            p.ellipse((ex, ey - 2), 17, 20, fill=SKIN, outline=INK, w=4.5)
            p.circle((ex + lx * 0.2, ey), 5.5, fill=INK)
        brows(-38)
        p.ellipse((M[0], M[1] + 4), 15, 15 + 5 * mouth, fill=INK)
        p.ellipse((M[0], M[1] + 13), 8, 5, fill=TONGUE)
        p.poly([(-R * 0.98, -18), (-R * 0.9, -2), (-R * 1.05, 6), (-R * 1.12, -4)], fill=SWEAT)
    elif expr == "whisper":
        for ex, ey in E:
            p.ellipse((ex, ey + 2), 9.5, 10, fill=INK)
            p.line((ex - 12, ey - 3), (ex + 12, ey - 3), w=5)
        p.ellipse((M[0] + 4, M[1]), 6, 6 + 3 * mouth, fill=INK)
    elif expr == "mischief":
        for i, (ex, ey) in enumerate(E):
            p.ellipse((ex, ey + 2), 9.5, 10, fill=INK)
            p.line((ex - 12, ey - 4), (ex + 12, ey - 1 if i == 0 else ey - 6), w=5)
        brows(-24, raise_one=True)
        p.arc((M[0] + 6, M[1] - 8), 16, 10, 10, 120, w=5)
    elif expr == "laugh":
        for ex, ey in E:
            p.arc((ex, ey + 6), 11, 10, 200, 340, w=5.5)
        p.poly([(M[0] - 18, M[1] - 6), (M[0] + 18, M[1] - 6), (M[0] + 10, M[1] + 14), (M[0] - 10, M[1] + 14)], fill=INK)
        p.ellipse((M[0], M[1] + 9), 8, 4, fill=TONGUE)
    elif expr == "worried":
        eyes_dot(1.0)
        for i, (ex, ey) in enumerate(E):
            s = -1 if i == 0 else 1
            p.line((ex + 11 * s, ey - 20), (ex - 9 * s, ey - 30), w=4.5)
        p.arc((M[0], M[1] + 8), 12, 8, 200, 340, w=5)
    elif expr == "gross":
        for i, (ex, ey) in enumerate(E):
            s = 1 if i == 0 else -1
            p.line((ex - 10 * s, ey - 8), (ex + 8 * s, ey), w=5)
            p.line((ex + 8 * s, ey), (ex - 10 * s, ey + 8), w=5)
        pts = [(M[0] - 16 + i * 4, M[1] + (3 if i % 2 else -3)) for i in range(9)]
        for a, b in zip(pts, pts[1:]):
            p.line(a, b, w=4.5)
        p.ellipse((M[0] + 6, M[1] + 9), 6, 7, fill=TONGUE, outline=INK, w=3)
    elif expr in ("sleep", "sleepsmile"):
        for ex, ey in E:
            p.arc((ex, ey + 1), 11, 8, 20, 160, w=5)
        if expr == "sleepsmile":
            p.arc((M[0], M[1] - 6), 11, 8, 20, 160, w=4.5)
        else:
            p.ellipse((M[0], M[1] + 2), 5, 4 + 3 * mouth, fill=INK)
    elif expr == "nervous":
        for ex, ey in E:
            p.ellipse((ex + lx * 0.4, ey), 9.5, 13, fill=INK)
            p.circle((ex - 3 + lx * 0.4, ey - 5), 3.4, fill=SKIN)
        for i, (ex, ey) in enumerate(E):
            s_ = -1 if i == 0 else 1
            p.line((ex + 11 * s_, ey - 20), (ex - 9 * s_, ey - 30), w=4.5)
        pts = [(M[0] - 14 + i * 3.5, M[1] + 4 + (2.5 if i % 2 else -2.5)) for i in range(9)]
        for a_, b_ in zip(pts, pts[1:]):
            p.line(a_, b_, w=4)
    elif expr == "think":
        for ex, ey in E:
            p.ellipse((ex + 4, ey - 4), 9.5, 13, fill=INK)
            p.circle((ex + 1, ey - 9), 3.4, fill=SKIN)
        brows(-30, raise_one=True)
        p.line((M[0] - 10, M[1]), (M[0] + 12, M[1] - 3), w=5)
    else:
        eyes_dot()
    return im


def nessa(pose="stand", expr="smile", t=0.0, scale=1.0, mouth=0.0, look=(0, 0), tilt=0.0, prop=None, flip=False, style="nessa"):
    P = POSES[pose]
    ST = STYLES[style]
    k = SS * scale
    W, H = int(560 * k), int(760 * k)
    ox, oy = W / 2, H - 40 * k
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    p = _Pen(d, ox, oy, k)

    breath = math.sin(t * 2.4) * 2.5
    hop = -abs(math.sin(t * 7.0)) * 26 if P.get("hop") else 0.0
    dy = hop + breath
    spread = P["legs"]
    # legs
    hipL, hipR = (-16, HIP_Y + dy), (16, HIP_Y + dy)
    if hop < -6:
        kneeL, kneeR = (-30, -70 + dy * 0.4), (30, -70 + dy * 0.4)
        footL, footR = (-spread - 6, hop * 0.3), (spread + 6, hop * 0.3)
        p.line(hipL, kneeL); p.line(kneeL, footL); p.line(hipR, kneeR); p.line(kneeR, footR)
    else:
        footL, footR = (-spread, 0), (spread, 0)
        p.line(hipL, footL); p.line(hipR, footR)
    for f, s in ((footL, -1), (footR, 1)):
        p.ellipse((f[0] + s * 8, f[1] - 2), 15, 8, fill=INK)
    # torso + dress
    neck = (0, NECK_Y + dy)
    p.line(neck, (0, HIP_Y + dy))
    top, bot = SH_Y + 6 + dy, HIP_Y + 12 + dy
    if ST.get("dress"):
        dcol = ST["dress"]
        p.poly([(-20, top), (20, top), (64, bot), (-64, bot)], fill=dcol, outline=INK, w=6)
        p.line((-22, top + 2), (22, top + 2), w=6, fill=tuple(int(c * 0.68) for c in dcol[:3]) + (255,))
        if style == "nessa":
            dc = (0, (top + bot) / 2 + 8)
            p.circle((dc[0], dc[1] + 4), 11, fill=SKIN)
            p.poly([(dc[0] - 9.5, dc[1] + 0), (dc[0], dc[1] - 18), (dc[0] + 9.5, dc[1] + 0)], fill=SKIN)
    elif ST.get("shirt"):
        p.poly([(-30, top - 2), (30, top - 2), (34, HIP_Y - 10 + dy), (-34, HIP_Y - 10 + dy)], fill=ST["shirt"], outline=INK, w=6)
    # head (tilt)
    hk = _head(expr, t, mouth, look, k, style)
    if tilt:
        hk = hk.rotate(-tilt, resample=Image.BICUBIC)
    hx, hy = p.P((0, HEAD_Y + dy))
    im.alpha_composite(hk, (int(hx - hk.width / 2), int(hy - hk.height / 2)))
    d = ImageDraw.Draw(im)
    p.d = d
    # arms (in front)
    lu, ll, ru, rl = P["arms"]
    if P.get("wave"):
        ll += math.sin(t * 9) * 22
        lu += math.sin(t * 9) * 6
    shL, shR = (-18, SH_Y + dy), (18, SH_Y + dy)
    eL = _pt(shL, lu, UP); hL = _pt(eL, ll, LO)
    eR = _pt(shR, ru, UP); hR = _pt(eR, rl, LO)
    p.line(shL, eL); p.line(eL, hL); p.line(shR, eR); p.line(eR, hR)
    prop = prop or P.get("prop")
    if prop == "magnifier":
        a = math.radians(rl)
        c = (hR[0] + math.cos(a) * 62, hR[1] + math.sin(a) * 62)
        p.line(hR, (hR[0] + math.cos(a) * 26, hR[1] + math.sin(a) * 26), w=13, fill=(120, 72, 40, 255))
        p.circle(c, 38, fill=LENS, outline=INK, w=9)
        p.arc(c, 26, 26, 200, 260, w=6, fill=(255, 255, 255, 230))
    if prop == "mirror":
        a = math.radians(rl)
        c = (hR[0] + math.cos(a) * 58, hR[1] + math.sin(a) * 58)
        p.line(hR, (hR[0] + math.cos(a) * 24, hR[1] + math.sin(a) * 24), w=14, fill=JADE)
        p.ellipse(c, 30, 38, fill=(200, 235, 255, 255), outline=JADE, w=10)
        p.arc(c, 20, 26, 205, 255, w=6, fill=(255, 255, 255, 255))
    for h in (hL, hR):
        p.circle(h, 13, fill=SKIN, outline=INK, w=5)
    if prop == "pad":
        p.circle((hR[0] - 6, hR[1] - 4), 24, fill=(255, 255, 255, 255), outline=(170, 170, 185, 255), w=4)
        p.circle((hR[0] - 10, hR[1] - 8), 9, fill=(236, 236, 244, 255))

    im = im.resize((W // SS, H // SS), Image.LANCZOS)
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im, (im.width // 2, int(oy / SS))


def floor_shadow(w=150, h=22, a=90):
    im = Image.new("RGBA", (w * 3, h * 3), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse([0, 0, w * 3 - 1, h * 3 - 1], fill=(0, 0, 0, a))
    from PIL import ImageFilter
    return im.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(4))


def head(expr="smile", t=0.0, scale=1.0, mouth=0.0, look=(0, 0), tilt=0.0, style="nessa"):
    """head only (RGBA, centred on head centre)"""
    k = SS * scale
    hk = _head(expr, t, mouth, look, k, style)
    if tilt:
        hk = hk.rotate(-tilt, resample=Image.BICUBIC)
    return hk.resize((hk.width // SS, hk.height // SS), Image.LANCZOS)
