"""NextBigNow's own drawing kit (Skia), used by OopsMyBusiness since 5 Nov 2026 (owner, 4 Nov: "make it like NextBigNow").
nbn_gfx.py, nbn_ed.py, nbn_toon.py = copies of whatif-v3/ gfx, ed, toon (imports renamed: studio/lib has its own gfx); this file adds fonts + reusable OMB helpers."""
import os, sys, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import numpy as np, skia
import nbn_gfx as _gfx
_S = os.environ.get("STUDIO", "/home/claude/studio")
_TTF = f"{_S}/fonts/ttf"; os.makedirs(_TTF, exist_ok=True)
for _src, _dst in ((f"{_S}/fonts/anton/package/files/anton-latin-400-normal.woff", "Anton.ttf"),
                   (f"{_S}/fonts/montserrat/package/files/montserrat-latin-500-normal.woff", "Montserrat-Medium.ttf"),
                   (f"{_S}/fonts/montserrat/package/files/montserrat-latin-600-normal.woff", "Montserrat-SemiBold.ttf"),
                   (f"{_S}/fonts/montserrat/package/files/montserrat-latin-800-normal.woff", "Montserrat-ExtraBold.ttf"),
                   (f"{_S}/fonts/montserrat/package/files/montserrat-latin-900-normal.woff", "Montserrat-Black.ttf"),
                   (f"{_S}/fonts/permanent-marker/package/files/permanent-marker-latin-400-normal.woff", "PermanentMarker.ttf"),
                   (f"{_S}/fonts/kalam/package/files/kalam-latin-700-normal.woff", "Kalam-Bold.ttf"),
                   (f"{_S}/fonts/kalam/package/files/kalam-latin-400-normal.woff", "Kalam-Regular.ttf"),
                   (f"{_S}/fonts/caveat/package/files/caveat-latin-500-normal.woff", "Caveat-Medium.ttf"),      # notebook look (7 Nov)
                   (f"{_S}/fonts/caveat/package/files/caveat-latin-700-normal.woff", "Caveat-Bold.ttf"),
                   (f"{_S}/fonts/gochi-hand/package/files/gochi-hand-latin-400-normal.woff", "GochiHand.ttf")):
    if not os.path.exists(f"{_TTF}/{_dst}") and os.path.exists(_src):
        from fontTools.ttLib import TTFont
        _f = TTFont(_src); _f.flavor = None; _f.save(f"{_TTF}/{_dst}")
_gfx.FONTDIR = _TTF
_gfx._TF.update({"pm": "PermanentMarker.ttf", "kb": "Kalam-Bold.ttf", "kr": "Kalam-Regular.ttf",
                  "cv": "Caveat-Medium.ttf", "cb": "Caveat-Bold.ttf", "gh": "GochiHand.ttf"})   # whiteboard look (6 Nov)
from nbn_toon import *        # noqa
from nbn_toon import draw_stick, draw_face, Face, POSES, LEN, walk_pose, lerp_pose, two_tier, set_bg, rig_points, stroke, make_mini, minis, ground_shadow
from nbn_gfx import paint, font, cl, pr, eo, eio, eback, lerp, mix, hsh, argb, lin, rad, poly, partial, WHITE, PLUS, SCREEN, glow_disc

FLOOR = 1420
ORANGE = (255, 140, 40); YEL = (255, 210, 70); RED_C = (235, 70, 60); GRN = (60, 205, 120); TEAL_C = (40, 190, 180); CREAM = (250, 240, 220); LAMP = (255, 214, 140)
PINK = (240, 90, 140); BLUE_C = (70, 140, 250)


def surface(): return skia.Surface(W, H)


def to_rgb(surf):
    arr = surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)
    return arr[..., :3].astype(np.float32) / 255.0


def blink_at(t, seed=0.0):
    ph = (t * 0.31 + seed + 0.2) % 1.0
    return ph < 0.035


def mouth_at(t, t0, t1, a="smile"):
    return a


def _rot_stick(c, x, y, s, pose, flip, squash, a, fn):
    P = rig_points(pose)
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s * squash)
    if a < 1: c.saveLayerAlpha(None, int(255 * a))
    hdx, hdy = P["head"]; lean = pose[0] + pose[1]
    c.save(); c.translate(hdx, hdy); c.rotate(lean)
    fn(c, LEN["head"], P)
    c.restore()
    if a < 1: c.restore()
    c.restore()


def hero(c, x, y, s, pose, face, t, flip=False, prop=None, squash=1.0, a=1.0, scarf=ORANGE, shirt=None):
    """OMB hero = 'you': NBN rig, orange scarf, short spiky dark hair."""
    r = draw_stick(c, x, y, s, pose, face, t=t, scarf=scarf, flip=flip, prop=prop, squash=squash, a=a, blink=blink_at(t))
    def hair(c, hr, P):
        p = skia.Path(); xs = [(-0.95, -0.25), (-0.86, -0.82), (-0.52, -0.72), (-0.46, -1.26), (-0.14, -0.95), (0.02, -1.36), (0.28, -0.98), (0.56, -1.2), (0.62, -0.74), (0.9, -0.72), (0.96, -0.25)]
        p.moveTo(xs[0][0] * hr, xs[0][1] * hr)
        for q in xs[1:]: p.lineTo(q[0] * hr, q[1] * hr)
        p.arcTo(R.MakeXYWH(-hr * 0.96, -hr * 0.96, hr * 1.92, hr * 1.92), 345, -150, False) if False else None
        p.quadTo(0, -hr * 0.78, xs[0][0] * hr, xs[0][1] * hr); p.close()
        c.drawPath(p, paint(INK))
    _rot_stick(c, x, y, s, pose, flip, squash, a, hair)
    return r


def extra(c, x, y, s, pose, face, t, flip=False, prop=None, scarf=(70, 140, 250), hat=None, glasses=False, bald=False, a=1.0, hair_col=INK):
    """a man in the cast: coloured scarf, side hair or a cap."""
    r = draw_stick(c, x, y, s, pose, face, t=t, scarf=scarf, flip=flip, prop=prop, a=a, blink=blink_at(t, 0.37))
    def top(c, hr, P):
        if hat:
            c.drawArc(R.MakeXYWH(-hr * 1.02, -hr * 1.14, hr * 2.04, hr * 2.04), 180, 180, True, paint(hat)); c.drawArc(R.MakeXYWH(-hr * 1.02, -hr * 1.14, hr * 2.04, hr * 2.04), 180, 180, True, stroke(INK, 5))
            c.drawRoundRect(R.MakeXYWH(-hr * 1.08, -hr * 0.2, hr * 2.7, 13), 6, 6, paint(hat)); c.drawRoundRect(R.MakeXYWH(-hr * 1.08, -hr * 0.2, hr * 2.7, 13), 6, 6, stroke(INK, 4))
        elif not bald:
            c.drawArc(R.MakeXYWH(-hr * 1.0, -hr * 1.04, hr * 2.0, hr * 2.0), 190, 160, False, stroke(hair_col, 14))
        if glasses:
            for sx in (-1, 1): c.drawCircle(sx * 15, -6, 13, stroke(INK, 3.5))
            c.drawLine(-2, -6, 2, -6, stroke(INK, 3.5))
    _rot_stick(c, x, y, s, pose, flip, 1.0, a, top)
    return r


def girl(c, x, y, s, pose, face, t, flip=False, prop=None, dress=TEAL_C, hair_col=(66, 44, 34), style="long", a=1.0, scarf=None):
    """a girl in the cast: dress + hair, same rig."""
    if style == "long":
        def back(c, hr, P):
            c.drawRoundRect(R.MakeXYWH(-hr * 1.16, -hr * 0.9, hr * 2.32, hr * 2.0), hr * 0.9, hr * 0.9, paint(hair_col))
        _rot_stick(c, x, y, s, pose, flip, 1.0, a, back)
    r = draw_stick(c, x, y, s, pose, face, t=t, scarf=scarf, flip=flip, prop=prop, a=a, blink=blink_at(t, 0.61))
    P = rig_points(pose); nx, ny = P["neck"]; hx, hy = P["hip"]
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    if a < 1: c.saveLayerAlpha(None, int(255 * a))
    dr = poly([(nx - 12, ny + 2), (nx + 12, ny + 2), (hx + 34, hy + 22), (hx - 34, hy + 22)], True)
    c.drawPath(dr, paint(dress)); c.drawPath(dr, stroke(INK, 5))
    if a < 1: c.restore()
    c.restore()
    def top(c, hr, P):
        c.drawArc(R.MakeXYWH(-hr * 1.04, -hr * 1.06, hr * 2.08, hr * 2.08), 186, 168, True, paint(hair_col))
        c.drawCircle(hr * 0.2, -hr * 0.2, 0.1, paint(WHITE))
        if style == "bun": c.drawCircle(0, -hr * 1.14, 18, paint(hair_col)); c.drawCircle(0, -hr * 1.14, 18, stroke(INK, 3))
    _rot_stick(c, x, y, s, pose, flip, 1.0, a, top)
    # the fringe hides the eyes' top only: redraw the face
    def fc(c, hr, P): draw_face(c, face, hr, blink_at(t, 0.61), t)
    _rot_stick(c, x, y, s, pose, flip, 1.0, a, fc)
    return r


# ------------------------------------------------------------------ places + atmosphere
def fg_dust(c, t, n=8, seed=5, a=0.25, col=LAMP):
    for i in range(n):
        x = (hsh(i, seed) * W + 26 * math.sin(t * 0.28 + i * 1.7)) % W
        y = 240 + ((hsh(i, seed + 1) * (H - 300) - t * (9 + 16 * hsh(i, seed + 2))) % (H - 300))
        r = 12 + 34 * hsh(i, seed + 3)
        c.drawCircle(x, y, r, paint(col, a * (0.35 + 0.65 * hsh(i, seed + 4)), blur=r * 0.55))


def top_shade(c, a=0.45, col=(10, 6, 24)):
    c.drawRect(R.MakeLTRB(0, 0, W, 860), paint(shader=lin(0, 250, 0, 860, [argb(col, a), argb(col, 0)])))


def night_bg(c, t, top, bot, lamp=(540, 1150), lamp_a=0.55, lamp_col=LAMP, floor=FLOOR, floor_top=None, floor_bot=None, blobs=None, seed=11):
    """NBN place: deep two-colour wall, soft blurred wall shapes, one warm light pool, dark floor with an ink line, light dust."""
    c.drawRect(R.MakeWH(W, H), paint(shader=lin(0, 0, 0, H, [argb(top), argb(bot)])))
    bl = blobs or mix(bot, (255, 255, 255), 0.25)
    for i in range(22):
        x = hsh(i, seed) * W; y = hsh(i, seed + 1) * (floor or FLOOR); r = 80 + 220 * hsh(i, seed + 2)
        c.drawOval(R.MakeXYWH(x - r, y - r * 0.6, 2 * r, 1.2 * r), paint(mix(bl, top, 0.55), 0.16 + 0.1 * hsh(i, seed + 3), blur=r * 0.3))
    if lamp:
        lx, ly = lamp
        c.drawCircle(lx, ly, 760, paint(shader=rad(lx, ly, 760, [argb(lamp_col, lamp_a), argb(lamp_col, lamp_a * 0.35), argb(lamp_col, 0)], [0, 0.4, 1])))
    if floor is not None:
        ft = floor_top or mix(bot, (0, 0, 0), 0.3); fb = floor_bot or mix(bot, (0, 0, 0), 0.62)
        c.drawRect(R.MakeLTRB(0, floor, W, H), paint(shader=lin(0, floor, 0, H, [argb(ft), argb(fb)])))
        c.drawLine(0, floor, W, floor, stroke(INK, 5))


def diagram_bg(c, top, bot, disc=None, cx=540, cy=1040, r=430, k=1.0, floor=None):
    """NBN 'idea' frame: gradient + one big soft disc behind the prop."""
    set_bg(c, top, bot, circle=disc, cx=cx, cy=cy, r=r, floor=floor, circ_k=k)


# ------------------------------------------------------------------ type
def pill(c, text="OOPSMYBUSINESS", y=288):
    f = font("ant", 34); tw_ = f.measureText(text) + 2 * max(0, len(text) - 1)
    w = tw_ + 78; x0 = W / 2 - w / 2
    c.drawRoundRect(R.MakeXYWH(x0, y - 27, w, 54), 27, 27, paint((14, 14, 20), 0.72)); c.drawRoundRect(R.MakeXYWH(x0, y - 27, w, 54), 27, 27, stroke(WHITE, 2.5, 0.28))
    c.drawCircle(x0 + 28, y, 8, paint((236, 40, 52)))
    xx = x0 + 50
    for ch in text:
        c.drawString(ch, xx, y + 14, f, paint(WHITE)); xx += f.measureText(ch) + 2


def src_chip(c, text, a=1.0, y=1478, x=540, dark=True, size=27):
    """the one small footnote: dark translucent pill in Montserrat, centred under the action"""
    if a <= 0.01 or not text: return
    f = font("mxb", size); w = f.measureText(text); 
    while w > 770 and size > 20:
        size -= 1; f = font("mxb", size); w = f.measureText(text)
    h = size + 26
    c.drawRoundRect(R.MakeXYWH(x - w / 2 - 22, y - h / 2, w + 44, h), h / 2, h / 2, paint((12, 12, 18), 0.74 * a))
    c.drawString(text, x - w / 2, y + size * 0.36, f, paint(WHITE, a))


def card(c, x, y, w, h, a=1.0, fill=WHITE, r=22, tilt=0.0, shadow=True, k=1.0):
    """NBN white rounded card (centre x, y). Leaves the canvas translated to its centre: use with card_end()."""
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k, k)
    if shadow: c.drawRoundRect(R.MakeXYWH(-w / 2 + 6, -h / 2 + 12, w, h), r, r, paint((0, 0, 0), 0.25 * a, blur=10))
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), r, r, paint(fill, a)); c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), r, r, stroke(INK, 6, a))


def card_end(c): c.restore()


def ctext(c, s, x, y, key="ant", size=60, col=INK, a=1.0):
    f = font(key, size); c.drawString(s, x - f.measureText(s) / 2, y, f, paint(col, a))


def label_card(c, x, y, text, size=72, col=INK, fill=WHITE, k=1.0, tilt=0.0, sub=None, sub_col=(90, 90, 100), pad=44):
    f = font("ant", size); w = f.measureText(text) + 2 * pad; h = size * 1.5 + (size * 0.55 if sub else 0)
    if sub: w = max(w, font("mxb", size * 0.32).measureText(sub) + 2 * pad)
    if k <= 0: return
    card(c, x, y, w, h, fill=fill, k=k, tilt=tilt)
    if sub:
        ctext(c, text, 0, size * 0.1, "ant", size, col); ctext(c, sub, 0, size * 0.1 + size * 0.62, "mxb", size * 0.32, sub_col)
    else:
        ctext(c, text, 0, size * 0.36, "ant", size, col)
    card_end(c)


def calendar(c, x, y, s, month, big, k=1.0):
    """NBN calendar card: red top, big word"""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    c.drawRoundRect(R.MakeXYWH(-96 + 5, -96 + 10, 192, 192), 20, 20, paint((0, 0, 0), 0.25, blur=8))
    c.drawRoundRect(R.MakeXYWH(-96, -96, 192, 192), 20, 20, paint(WHITE))
    c.save(); c.clipRect(R.MakeXYWH(-96, -96, 192, 56)); c.drawRoundRect(R.MakeXYWH(-96, -96, 192, 192), 20, 20, paint(RED_C)); c.restore()
    c.drawRoundRect(R.MakeXYWH(-96, -96, 192, 192), 20, 20, stroke(INK, 6))
    for sx in (-52, 52): c.drawRoundRect(R.MakeXYWH(sx - 7, -110, 14, 34), 7, 7, paint(INK))
    ctext(c, month, 0, -54, "mxb", 26, WHITE)
    f = 84
    while font("ant", f).measureText(big) > 170: f -= 4
    ctext(c, big, 0, 40 + f * 0.1, "ant", f, INK)
    c.restore()


def speech(c, x, y, w, h, text, k=1.0, size=66, col=INK, tail=-1):
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k)
    p = skia.Path(); p.addRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), h * 0.42, h * 0.42)
    tx = tail * w * 0.22
    q = poly([(tx - 26, h / 2 - 4), (tx + 26, h / 2 - 4), (tx + tail * 18, h / 2 + 46)], True)
    c.drawPath(p, paint(WHITE)); c.drawPath(q, paint(WHITE)); c.drawPath(p, stroke(INK, 6)); 
    c.drawLine(tx - 26, h / 2, tx + tail * 18, h / 2 + 46, stroke(INK, 6)); c.drawLine(tx + 26, h / 2, tx + tail * 18, h / 2 + 46, stroke(INK, 6))
    c.drawRect(R.MakeXYWH(tx - 22, h / 2 - 8, 44, 8), paint(WHITE))
    ctext(c, text, 0, size * 0.36, "ant", size, col)
    c.restore()


# ------------------------------------------------------------------ small props
def coin(c, x, y, r=26, spin=0.0, a=1.0):
    sx = max(0.12, abs(math.cos(spin)))
    c.save(); c.translate(x, y); c.scale(sx, 1)
    if a < 1: c.saveLayerAlpha(None, int(255 * a))
    c.drawCircle(0, 0, r, paint((255, 200, 50))); c.drawCircle(-r * 0.2, -r * 0.2, r * 0.62, paint((255, 228, 120), 0.8))
    c.drawCircle(0, 0, r, stroke(INK, max(3, r * 0.16))); c.drawCircle(0, 0, r * 0.62, stroke((190, 130, 20), max(2, r * 0.09)))
    if a < 1: c.restore()
    c.restore()


def note(c, x, y, s=1.0, a=1.0, col=WHITE):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(R.MakeXYWH(-26, 12, 30, 22), paint(col, a)); c.drawLine(2, 22, 2, -30, stroke(col, 7, a)); c.drawLine(2, -30, 28, -20, stroke(col, 9, a))
    c.restore()


def notes(c, x, y, t, n=4, seed=3, col=WHITE):
    for i in range(n):
        ph = (t * 0.34 + hsh(i, seed)) % 1.0
        note(c, x + (i - n / 2) * 50 + 34 * math.sin(ph * 6 + i), y - ph * 280, 0.7 + 0.5 * hsh(i, seed + 1), a=min(1, ph * 5) * (1 - ph), col=col)


def mic_stand(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawLine(0, 0, 0, -220, stroke(INK, 9)); c.drawLine(-44, 0, 44, 0, stroke(INK, 10))
    c.drawRoundRect(R.MakeXYWH(-22, -284, 44, 74), 22, 22, paint((205, 210, 225))); c.drawRoundRect(R.MakeXYWH(-22, -284, 44, 74), 22, 22, stroke(INK, 6))
    for q in (-266, -250, -234): c.drawLine(-14, q, 14, q, stroke((110, 116, 140), 3))
    c.restore()


def contract(c, x, y, w=300, k=1.0, title="YOUR DEAL", tilt=0.0):
    if k <= 0: return
    h = w * 1.3; card(c, x, y, w, h, fill=(250, 246, 236), r=14, k=k, tilt=tilt)
    ctext(c, title, 0, -h / 2 + w * 0.19, "ant", w * 0.14, INK)
    for i in range(5):
        yy = -h / 2 + w * (0.34 + i * 0.13); c.drawRoundRect(R.MakeXYWH(-w * 0.36, yy, w * 0.72 if i % 3 else w * 0.56, w * 0.035), 4, 4, paint((170, 170, 182)))
    c.drawLine(-w * 0.34, h / 2 - w * 0.16, w * 0.14, h / 2 - w * 0.16, stroke(INK, 4))
    card_end(c)


def phone(c, x, y, w=150, glow=0.5, tilt=0.0):
    h = w * 1.9
    c.save(); c.translate(x, y); c.rotate(tilt)
    if glow > 0: c.drawCircle(0, 0, h * 0.8, paint(shader=rad(0, 0, h * 0.8, [argb((200, 220, 255), 0.4 * glow), argb((200, 220, 255), 0)])))
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), w * 0.16, w * 0.16, paint((26, 26, 36))); c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), w * 0.16, w * 0.16, stroke(INK, 5))
    c.drawRoundRect(R.MakeXYWH(-w * 0.42, -h * 0.44, w * 0.84, h * 0.88), w * 0.08, w * 0.08, paint(shader=lin(0, -h / 2, 0, h / 2, [argb((70, 60, 140)), argb((180, 80, 130))])))
    p = poly([(-w * 0.14, -h * 0.13), (-w * 0.14, h * 0.05), (w * 0.2, -h * 0.04)], True); c.drawPath(p, paint(WHITE))
    c.drawRoundRect(R.MakeXYWH(-w * 0.32, h * 0.17, w * 0.64, h * 0.03), 3, 3, paint(WHITE, 0.8))
    c.restore()


def partial_pts(pts, k):
    """the first k (0..1) of a polyline, as points"""
    ds = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]; tgt = sum(ds) * cl(k); out = [pts[0]]; acc = 0.0
    for a, b, d in zip(pts, pts[1:], ds):
        if acc + d >= tgt:
            q = (tgt - acc) / max(d, 1e-6); out.append((a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q)); return out
        out.append(b); acc += d
    return out


def quad_pts(a, m, b, n=40):
    return [((1 - u) ** 2 * a[0] + 2 * u * (1 - u) * m[0] + u * u * b[0], (1 - u) ** 2 * a[1] + 2 * u * (1 - u) * m[1] + u * u * b[1]) for u in (i / n for i in range(n + 1))]


def arrow_line(c, pts, prog, col=WHITE, w=9, dash=True, a=1.0):
    if prog <= 0: return
    pl = quad_pts(*pts) if len(pts) == 3 else list(pts)
    seg = partial_pts(pl, prog)
    p = stroke(col, w, a)
    if dash: p.setPathEffect(skia.DashPathEffect.Make([26, 18], 0))
    c.drawPath(poly(seg), p)
    if prog > 0.98:
        (x0, y0), (x1, y1) = pl[-2], pl[-1]; ang = math.atan2(y1 - y0, x1 - x0)
        h = poly([(x1 + 26 * math.cos(ang), y1 + 26 * math.sin(ang)), (x1 + 22 * math.cos(ang + 2.3), y1 + 22 * math.sin(ang + 2.3)), (x1 + 22 * math.cos(ang - 2.3), y1 + 22 * math.sin(ang - 2.3))], True)
        c.drawPath(h, paint(col, a))


# ------------------------------------------------------------------ HOW IT WORKS props (money machine): pot, gate, dot grid, booth, pie
def pot(c, x, y, w=560, fill=0.6, k=1.0, t=0.0, glow=0.0):
    """coin pot, x = centre, y = bottom"""
    if k <= 0: return
    h = w * 0.78
    c.save(); c.translate(x, y); c.scale(k, k); c.translate(-w / 2, -h)
    if glow > 0: c.drawCircle(w / 2, h * 0.4, w * 0.8, paint(shader=rad(w / 2, h * 0.4, w * 0.8, [argb((255, 210, 90), 0.5 * glow), argb((255, 210, 90), 0)])))
    c.drawOval(R.MakeXYWH(w * 0.02, h * 0.92, w * 0.96, h * 0.14), paint((0, 0, 0), 0.25, blur=10))
    for hx in (0.0, 0.88):
        c.drawOval(R.MakeXYWH(w * hx, h * 0.22, w * 0.12, h * 0.26), stroke(INK, 11))
    body = skia.Path(); body.moveTo(w * 0.08, h * 0.18); body.lineTo(w * 0.92, h * 0.18); body.cubicTo(w * 0.96, h * 0.7, w * 0.86, h * 1.0, w * 0.7, h * 1.0); body.lineTo(w * 0.3, h * 1.0); body.cubicTo(w * 0.14, h * 1.0, w * 0.04, h * 0.7, w * 0.08, h * 0.18); body.close()
    c.drawPath(body, paint(shader=lin(0, 0, w, 0, [argb((70, 74, 96)), argb((38, 40, 58)), argb((22, 24, 36))], [0, 0.5, 1])))
    fl = cl(fill)
    if fl > 0.005:
        c.save(); c.clipPath(body, True)
        top = h * (0.96 - 0.72 * fl)
        c.drawRect(R.MakeLTRB(0, top, w, h), paint(shader=lin(0, top, 0, h, [argb((255, 214, 80)), argb((226, 150, 30))])))
        for i in range(int(16 + 46 * fl)):
            cx_ = w * (0.14 + 0.72 * hsh(i, 41)); cy_ = top + (h - top) * hsh(i, 42); rr = w * 0.036
            c.drawCircle(cx_, cy_, rr, paint((255, 228, 120))); c.drawCircle(cx_, cy_, rr, stroke((184, 124, 20), 3))
        c.drawCircle(w * 0.5, top, w * 0.03, paint(WHITE, 0.0))
        c.restore()
    c.drawPath(body, stroke(INK, 7))
    c.drawRoundRect(R.MakeXYWH(w * 0.03, h * 0.08, w * 0.94, h * 0.13), 22, 22, paint((86, 90, 116))); c.drawRoundRect(R.MakeXYWH(w * 0.03, h * 0.08, w * 0.94, h * 0.13), 22, 22, stroke(INK, 7))
    c.restore()


def gate(c, x, y=FLOOR, w=560, count="999", arm=0.0, col_ok=False, k=1.0, shake=0.0, need="NEED 1,000", flash=0.0):
    """barrier gate, x = centre, y = floor. arm 0 = down (closed), 1 = up (open). Counter panel on the crossbar."""
    if k <= 0: return
    h = w * 0.98; pw = w * 0.09
    c.save(); c.translate(x + shake, y); c.scale(k, k)
    c.drawOval(R.MakeXYWH(-w * 0.58, -14, w * 1.16, 30), paint((0, 0, 0), 0.25, blur=8))
    for sx in (-1, 1):
        rr = R.MakeXYWH(sx * w * 0.44 - pw / 2, -h * 0.84, pw, h * 0.84)
        c.drawRoundRect(rr, 12, 12, paint(shader=lin(rr.left(), 0, rr.right(), 0, [argb(CREAM), argb(mix(CREAM, (120, 110, 130), 0.35))]))); c.drawRoundRect(rr, 12, 12, stroke(INK, 6))
    # crossbar + counter
    c.drawRoundRect(R.MakeXYWH(-w * 0.5, -h * 0.90, w, h * 0.075), 12, 12, paint(CREAM)); c.drawRoundRect(R.MakeXYWH(-w * 0.5, -h * 0.90, w, h * 0.075), 12, 12, stroke(INK, 6))
    pan = R.MakeXYWH(-w * 0.31, -h * 1.09, w * 0.62, h * 0.21); dc = GRN if col_ok else (255, 84, 76)
    c.drawRoundRect(pan, 18, 18, paint((18, 18, 26))); c.drawRoundRect(pan, 18, 18, stroke(INK, 6))
    f = font("ant", h * 0.145); s_ = str(count); tw_ = f.measureText(s_)
    while tw_ > w * 0.54: f = font("ant", f.getSize() * 0.92); tw_ = f.measureText(s_)
    by = -h * 1.09 + h * 0.105 + f.getSize() * 0.36
    c.drawString(s_, -tw_ / 2, by, f, paint(dc, 0.55, blur=9)); c.drawString(s_, -tw_ / 2, by, f, paint(dc))
    # boom rises straight up between the posts (a swinging arm crossed the counter): red + low = closed, green + high = open
    ay = lerp(-h * 0.40, -h * 0.74, eo(cl(arm))); col = GRN if arm > 0.5 else RED_C
    rr = R.MakeXYWH(-w * 0.44, ay - 22, w * 0.88, 44); c.drawRoundRect(rr, 20, 20, paint(col)); c.drawRoundRect(rr, 20, 20, stroke(INK, 6))
    fn = font("ant", 28); c.drawString(need, -fn.measureText(need) / 2, ay + 10, fn, paint(WHITE))
    if flash > 0: c.drawCircle(0, -h * 0.4, w * 0.7, paint(shader=rad(0, -h * 0.4, w * 0.7, [argb((255, 70, 60), 0.4 * flash), argb((255, 70, 60), 0)])))
    c.restore()


def dot_grid(c, cx, cy, total, mine=5, w=720, k=None, flash=0.0, t=0.0, cols=None, keep_gap=None):
    """YOUR dots orange, everybody else's white. Double `total` and the orange share shrinks on screen."""
    cols = cols or int(math.ceil(math.sqrt(total * 1.5))); gap = keep_gap or w / cols; r = gap * 0.36; rows = int(math.ceil(total / cols))
    x0 = cx - (cols - 1) * gap / 2; y0 = cy - (rows - 1) * gap / 2
    for i in range(total):
        kk = 1.0 if k is None else cl(k * total - i)
        if kk <= 0: break
        x = x0 + (i % cols) * gap; y = y0 + (i // cols) * gap; rr = r * eback(kk, 2.0)
        if i < mine:
            c.drawCircle(x, y, rr * (1.0 + 0.25 * flash), paint(ORANGE))
            if flash > 0: c.drawCircle(x, y, rr * 2.1, paint(shader=rad(x, y, rr * 2.1, [argb(ORANGE, 0.6 * flash), argb(ORANGE, 0)])))
            c.drawCircle(x, y, rr * (1.0 + 0.25 * flash), stroke(INK, 4))
        else:
            c.drawCircle(x, y, rr, paint((244, 246, 252))); c.drawCircle(x, y, rr, stroke(INK, 3))


def booth(c, x, y=FLOOR, w=520, text="LABEL OR DISTRIBUTOR", k=1.0, sign=(255, 196, 60)):
    if k <= 0: return
    h = w * 0.92
    c.save(); c.translate(x, y); c.scale(k, k); c.translate(-w / 2, -h)
    c.drawOval(R.MakeXYWH(-10, h - 12, w + 20, 30), paint((0, 0, 0), 0.25, blur=8))
    c.drawRect(R.MakeXYWH(w * 0.05, h * 0.2, w * 0.9, h * 0.8), paint(CREAM)); c.drawRect(R.MakeXYWH(w * 0.05, h * 0.2, w * 0.9, h * 0.8), stroke(INK, 7))
    c.drawRect(R.MakeXYWH(w * 0.14, h * 0.28, w * 0.72, h * 0.32), paint((52, 58, 84))); c.drawRect(R.MakeXYWH(w * 0.14, h * 0.28, w * 0.72, h * 0.32), stroke(INK, 6))
    c.drawRoundRect(R.MakeXYWH(0, h * 0.6, w, h * 0.07), 8, 8, paint(sign)); c.drawRoundRect(R.MakeXYWH(0, h * 0.6, w, h * 0.07), 8, 8, stroke(INK, 6))
    c.drawRoundRect(R.MakeXYWH(-w * 0.02, 0, w * 1.04, h * 0.2), 14, 14, paint(sign)); c.drawRoundRect(R.MakeXYWH(-w * 0.02, 0, w * 1.04, h * 0.2), 14, 14, stroke(INK, 7))
    f = h * 0.12
    while font("ant", f).measureText(text) > w * 0.92: f -= 2
    ctext(c, text, w / 2, h * 0.1 + f * 0.36, "ant", f, INK)
    c.restore()


def pie_wedge(c, x, y, r, frac=0.14, k=1.0, col=ORANGE, base=(36, 40, 60), a0=-90):
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k)
    c.drawCircle(6, 10, r, paint((0, 0, 0), 0.25, blur=8)); c.drawCircle(0, 0, r, paint(base)); c.drawCircle(0, 0, r, stroke(INK, 7))
    for i in range(12):
        an = math.radians(i * 30 + a0); c.drawLine(0, 0, r * math.cos(an), r * math.sin(an), stroke((70, 76, 104), 3))
    oval = R.MakeXYWH(-r, -r, 2 * r, 2 * r); off = r * 0.1; md = math.radians(a0 + 180 * frac)
    c.translate(off * math.cos(md), off * math.sin(md))
    c.drawArc(oval, a0, 360 * frac, True, paint(col)); c.drawArc(oval, a0, 360 * frac, True, stroke(INK, 7))
    c.restore()


# ------------------------------------------------------------------ HOW TO START EP 5 (reselling): the pack room + flat props (R&D 5 Nov 2026)
def pack_room(c, t, lamp=(560, 1120), lamp_a=0.5, top=(30, 34, 74), bot=(70, 78, 132)):
    """one held world: a night stockroom. Shelf silhouette across the top, a clothes rail + stacked parcels at the edges, dark floor."""
    night_bg(c, t, top, bot, lamp=lamp, lamp_a=lamp_a, floor=None)
    dk = (14, 16, 38)
    c.drawRect(R.MakeLTRB(0, 0, W, 70), paint(dk))
    for i in range(9):      # boxes on the top shelf, read as a silhouette
        x = i * 128 - 20 + 16 * hsh(i, 3); w = 92 + 30 * hsh(i, 4); h = 34 + 24 * hsh(i, 5)
        c.drawRect(R.MakeXYWH(x, 70, w, h), paint(mix(dk, (60, 66, 110), 0.25)))
    c.drawRect(R.MakeLTRB(0, 70 + 58, W, 70 + 70), paint(dk))
    for x, y0, w, n in ((44, FLOOR, 130, 3), (980, FLOOR, 120, 2)):
        for j in range(n):
            ww = w * (1 - 0.12 * j); h = 74
            c.drawRect(R.MakeXYWH(x - ww / 2, y0 - (j + 1) * h, ww, h - 3), paint(mix(dk, (120, 90, 60), 0.3)))
            c.drawLine(x, y0 - (j + 1) * h, x, y0 - j * h - 3, stroke(mix(dk, (200, 170, 120), 0.25), 8))
    c.drawRect(R.MakeLTRB(0, FLOOR, W, H), paint(shader=lin(0, FLOOR, 0, H, [argb(mix(bot, (0, 0, 0), 0.45)), argb(mix(bot, (0, 0, 0), 0.75))])))
    c.drawLine(0, FLOOR, W, FLOOR, stroke(INK, 5))
    fg_dust(c, t, n=7, seed=9, a=0.2)


def jacket(c, x, y, w=300, col=(70, 120, 200), k=1.0, tilt=0.0, hanger=True, worn=0.0):
    """a plain flat jacket on a hanger; x, y = hanger hook. worn 0..1 greys it a little (the old closet one)."""
    if k <= 0: return
    col = mix(col, (130, 130, 140), 0.45 * worn); dk = mix(col, (0, 0, 0), 0.28)
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k, k)
    s = w / 300.0; c.scale(s, s)
    if hanger:
        hk = skia.Path(); hk.moveTo(0, 34); hk.lineTo(0, 16); hk.cubicTo(0, 0, 24, 0, 22, 16); c.drawPath(hk, stroke((225, 228, 236), 7))
        c.drawPath(poly([(-92, 62), (0, 30), (92, 62)]), stroke((225, 228, 236), 8))
    body = poly([(-60, 42), (60, 42), (140, 86), (150, 262), (98, 268), (92, 138), (88, 340), (-88, 340), (-92, 138), (-98, 268), (-150, 262), (-140, 86)], True)
    c.drawPath(body, paint(col)); c.drawPath(body, stroke(INK, 7))
    c.drawLine(0, 60, 0, 340, stroke(dk, 8))
    for sx in (-1, 1):
        c.drawPath(poly([(sx * 2, 62), (sx * 44, 42), (sx * 58, 100), (sx * 8, 158)], True), paint(mix(col, (255, 255, 255), 0.18)))
        c.drawPath(poly([(sx * 2, 62), (sx * 44, 42), (sx * 58, 100), (sx * 8, 158)], True), stroke(INK, 5))
        c.drawRoundRect(R.MakeXYWH(sx * 46 - 24, 258, 48, 12), 4, 4, paint(dk))
    for yy in (130, 190, 250): c.drawCircle(-14, yy, 6, paint(INK))
    c.restore()


def price_tag(c, x, y, text, k=1.0, tilt=-6.0, col=INK, fill=(250, 244, 226), size=64):
    """string tag with a hole, centre x, y."""
    if k <= 0: return
    f = font("ant", size); w = f.measureText(text) + 96; h = size * 1.5
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k, k)
    p = poly([(-w / 2, -h / 2 + 18), (-w / 2 + 34, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2 + 34, h / 2), (-w / 2, h / 2 - 18)], True)
    c.drawPath(p, paint((0, 0, 0), 0.25, blur=8)); c.drawPath(p, paint(fill)); c.drawPath(p, stroke(INK, 6))
    c.drawCircle(-w / 2 + 28, 0, 9, paint(mix(fill, (0, 0, 0), 0.5))); c.drawCircle(-w / 2 + 28, 0, 9, stroke(INK, 4))
    c.drawString(text, -w / 2 + 52, size * 0.36, f, paint(col))
    c.restore()


def stamp(c, x, y, text, col=RED_C, k=1.0, tilt=-10.0, size=74):
    """a rubber stamp mark that slams in: pass k from pop_()."""
    if k <= 0: return
    f = font("ant", size); w = f.measureText(text) + 54; h = size * 1.42
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k, k)
    c.drawRoundRect(R.MakeXYWH(-w / 2 - 6, -h / 2 - 6, w + 12, h + 12), 16, 16, paint((12, 12, 18), 0.55, blur=5))
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), 12, 12, paint(WHITE)); c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), 12, 12, stroke(col, 9))
    c.drawString(text, -f.measureText(text) / 2, size * 0.36, f, paint(col))
    c.restore()


def listing_card(c, x, y, w, price, state="ASKING", k=1.0, tilt=0.0, col=None):
    """a plain online listing: picture box, price, one status strip. No site chrome or logos."""
    if k <= 0: return
    h = w * 1.22; card(c, x, y, w, h, k=k, tilt=tilt)
    c.drawRoundRect(R.MakeXYWH(-w * 0.42, -h * 0.44, w * 0.84, h * 0.46), 12, 12, paint((226, 230, 240)))
    jacket(c, 0, -h * 0.44 + 4, w * 0.48, hanger=False, col=(70, 120, 200))
    ctext(c, price, 0, h * 0.2, "ant", w * 0.23, INK)
    sc = col or (GRN if state == "SOLD" else (150, 154, 170))
    c.drawRoundRect(R.MakeXYWH(-w * 0.42, h * 0.27, w * 0.84, h * 0.15), 14, 14, paint(sc))
    ctext(c, state, 0, h * 0.27 + h * 0.105, "ant", w * 0.1, WHITE)
    card_end(c)


def receipt(c, x, y, w, rows, k=1.0, tilt=3.0, total=None, prog=1.0):
    """paper receipt with a torn bottom. rows = [(label, value)]; prog 0..1 reveals rows one by one."""
    if k <= 0: return
    n = len(rows) + (1 if total else 0); rh = w * 0.15; h = w * 0.2 + n * rh + w * 0.08
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k, k)
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2)]
    for i in range(1, 12): pts.append((w / 2 - i * w / 12, h / 2 + (-14 if i % 2 else 0)))
    pts.append((-w / 2, h / 2))
    p = poly(pts, True); c.drawPath(p, paint((0, 0, 0), 0.25, blur=9)); c.drawPath(p, paint((252, 250, 242))); c.drawPath(p, stroke(INK, 5))
    fs = rh * 0.58; fl = font("mxb", fs); fr = font("ant", fs * 1.14); shown = int(math.ceil(cl(prog) * n))
    for i, (a_, b_) in enumerate(rows[:shown]):
        yy = -h / 2 + w * 0.2 + i * rh
        c.drawString(a_, -w * 0.42, yy, fl, paint((70, 72, 86))); c.drawString(b_, w * 0.42 - fr.measureText(b_), yy, fr, paint(INK))
    if total and shown > len(rows):
        yy = -h / 2 + w * 0.2 + len(rows) * rh; c.drawLine(-w * 0.42, yy - rh * 0.72, w * 0.42, yy - rh * 0.72, stroke(INK, 4))
        c.drawString(total[0], -w * 0.42, yy, fl, paint(INK)); c.drawString(total[1], w * 0.42 - fr.measureText(total[1]), yy, fr, paint((30, 150, 90)))
    c.restore()


def tax_form(c, x, y, w=420, title="TAX FORM", k=1.0, tilt=-3.0, ghost=False):
    """a generic form sheet. ghost=True draws it as a dashed outline: the form that never came."""
    if k <= 0: return
    h = w * 1.28
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k, k)
    rr = R.MakeXYWH(-w / 2, -h / 2, w, h)
    if ghost:
        pp = stroke(WHITE, 7, 0.75); pp.setPathEffect(skia.DashPathEffect.Make([26, 18], 0)); c.drawRoundRect(rr, 12, 12, pp)
        ctext(c, "NO FORM", 0, 18, "ant", w * 0.17, WHITE, 0.85)
    else:
        c.drawRoundRect(rr, 12, 12, paint((0, 0, 0), 0.25, blur=9)); c.drawRoundRect(rr, 12, 12, paint(WHITE)); c.drawRoundRect(rr, 12, 12, stroke(INK, 6))
        c.drawRect(R.MakeXYWH(-w / 2 + 8, -h / 2 + 8, w - 16, h * 0.14), paint((226, 232, 244)))
        ctext(c, title, 0, -h / 2 + h * 0.115, "ant", h * 0.08, INK)
        for i in range(5):
            yy = -h / 2 + h * (0.24 + 0.135 * i); c.drawRect(R.MakeXYWH(-w * 0.4, yy, w * 0.8, h * 0.085), paint((245, 246, 250))); c.drawRect(R.MakeXYWH(-w * 0.4, yy, w * 0.8, h * 0.085), stroke((150, 154, 170), 3))
    c.restore()


def line_tally(c, x, y, w, rows, k=1.0, prog=1.0):
    """the takeaway: one simple notebook list, columns PAID / SOLD / FEES. rows = [(paid, sold, fees)]"""
    if k <= 0: return
    rh = w * 0.13; h = rh * (len(rows) + 1) + w * 0.14
    card(c, x, y, w, h, fill=(252, 250, 240), k=k, r=16)
    hdr = ("PAID", "SOLD", "FEES"); xs = (-w * 0.28, 0, w * 0.28); top = -h / 2 + w * 0.13
    for hx, s_ in zip(xs, hdr): ctext(c, s_, hx, top, "ant", rh * 0.62, INK)
    c.drawLine(-w * 0.44, top + rh * 0.24, w * 0.44, top + rh * 0.24, stroke(INK, 5))
    shown = int(math.ceil(cl(prog) * len(rows)))
    for i, rw in enumerate(rows[:shown]):
        yy = top + rh * (i + 1)
        for hx, s_ in zip(xs, rw): ctext(c, s_, hx, yy, "mxb", rh * 0.5, (60, 62, 76))
    card_end(c)


def parcel(c, x, y, w=220, k=1.0, label=None):
    """cardboard parcel, x = centre, y = bottom"""
    if k <= 0: return
    h = w * 0.72
    c.save(); c.translate(x, y); c.scale(k, k)
    c.drawOval(R.MakeXYWH(-w * 0.56, -12, w * 1.12, 26), paint((0, 0, 0), 0.25, blur=8))
    c.drawRect(R.MakeXYWH(-w / 2, -h, w, h), paint((206, 160, 104))); c.drawRect(R.MakeXYWH(-w / 2, -h, w, h), stroke(INK, 6))
    c.drawRect(R.MakeXYWH(-w * 0.08, -h, w * 0.16, h), paint((232, 200, 150)))
    if label: ctext(c, label, 0, -h * 0.34, "ant", w * 0.16, INK)
    c.restore()


# ------------------------------------------------------------------ HOW IT WORKS EP 3 (Shorts money): the waterworks + flat props
def waterworks(c, t, lamp=(540, 1130), lamp_a=0.42, top=(14, 40, 62), bot=(30, 96, 110)):
    """one held world: a pump room at night. Big pipes framing the top, a gauge on the wall, wet dark floor."""
    night_bg(c, t, top, bot, lamp=lamp, lamp_a=lamp_a, lamp_col=(150, 230, 230), floor=None)
    dk = (8, 22, 34)
    c.drawRect(R.MakeLTRB(0, 0, W, 74), paint(dk)); c.drawRect(R.MakeLTRB(0, 74, W, 118), paint(mix(dk, (70, 120, 130), 0.25))); c.drawLine(0, 118, W, 118, stroke(INK, 5))
    for x in (130, 400, 690, 960):
        c.drawRect(R.MakeXYWH(x - 15, 66, 30, 62), paint(dk))
        c.drawRect(R.MakeXYWH(x - 26, 118, 52, 72), paint(mix(dk, (70, 120, 130), 0.2))); c.drawRect(R.MakeXYWH(x - 26, 118, 52, 72), stroke(INK, 4))
    c.drawRect(R.MakeLTRB(0, FLOOR, W, H), paint(shader=lin(0, FLOOR, 0, H, [argb(mix(bot, (0, 0, 0), 0.5)), argb(mix(bot, (0, 0, 0), 0.8))])))
    c.drawLine(0, FLOOR, W, FLOOR, stroke(INK, 5))
    fg_dust(c, t, n=7, seed=21, a=0.16, col=(190, 240, 240))


def tank(c, x, y, w=520, fill=0.6, k=1.0, t=0.0, label=None, liquid=(255, 206, 70)):
    """a glass money tank with a coin-gold level; x = centre, y = bottom"""
    if k <= 0: return
    h = w * 1.05
    c.save(); c.translate(x, y); c.scale(k, k)
    c.drawOval(R.MakeXYWH(-w * 0.56, -16, w * 1.12, 32), paint((0, 0, 0), 0.3, blur=9))
    rr = R.MakeXYWH(-w / 2, -h, w, h)
    c.drawRoundRect(rr, 36, 36, paint((26, 50, 66), 0.9))
    fl = cl(fill)
    if fl > 0.004:
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(rr, 36, 36), True)
        top_ = -h + h * (1 - fl); wob = 7 * math.sin(t * 2.2)
        c.drawRect(R.MakeLTRB(-w, top_ + wob, w, 0), paint(shader=lin(0, top_, 0, 0, [argb(liquid), argb(mix(liquid, (170, 90, 10), 0.55))])))
        for i in range(int(10 + 34 * fl)):
            cx_ = w * (hsh(i, 61) - 0.5) * 0.9; cy_ = lerp(top_ + 26, -18, hsh(i, 62)); rr_ = w * 0.03
            c.drawCircle(cx_, cy_, rr_, paint((255, 232, 130))); c.drawCircle(cx_, cy_, rr_, stroke((170, 112, 20), 3))
        c.restore()
    c.drawRoundRect(rr, 36, 36, stroke(INK, 8))
    c.drawRoundRect(R.MakeXYWH(-w / 2 + 20, -h + 26, 20, h * 0.6), 10, 10, paint(WHITE, 0.16))
    if label:
        f = w * 0.13
        while font("ant", f).measureText(label) > w * 0.82: f -= 2
        ctext(c, label, 0, -h * 0.84 + f * 0.36, "ant", f, WHITE)
    c.restore()


def pipe(c, pts, w=46, flow=0.0, t=0.0, col=(92, 112, 128), coins=True, a=1.0):
    """a thick pipe along a polyline. flow > 0 moves coins through it (they sit on top, so the money is visible)."""
    path = poly(pts); c.drawPath(path, stroke(INK, w + 12, a)); c.drawPath(path, stroke(col, w, a)); c.drawPath(path, stroke(mix(col, (255, 255, 255), 0.3), w * 0.18, a))
    if flow > 0 and coins:
        n = 7
        for i in range(n):
            q = ((t * 0.34 * max(flow, 0.2) + i / n) % 1.0); seg = partial_pts(pts, q)
            coin(c, seg[-1][0], seg[-1][1], w * 0.42, spin=t * 4 + i, a=min(1, q * 8) * min(1, (1 - q) * 8) * min(1, flow * 3))


def valve(c, x, y, r=78, turn=0.0, col=RED_C, k=1.0):
    """hand wheel valve"""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k); c.rotate(turn * 150)
    c.drawCircle(0, 0, r, stroke(INK, r * 0.34)); c.drawCircle(0, 0, r, stroke(col, r * 0.22))
    for a_ in (0, 60, 120): 
        c.save(); c.rotate(a_); c.drawLine(-r, 0, r, 0, stroke(INK, r * 0.2)); c.drawLine(-r, 0, r, 0, stroke(col, r * 0.1)); c.restore()
    c.drawCircle(0, 0, r * 0.22, paint(mix(col, (0, 0, 0), 0.2))); c.drawCircle(0, 0, r * 0.22, stroke(INK, 5))
    c.restore()


def split_bar(c, x, y, w, frac, left, right, k=1.0, lc=ORANGE, rc=(90, 104, 130), h=120):
    """one bar cut in two: frac on the left in colour, the rest grey, each named. k 0..1 draws the cut opening."""
    if k <= 0: return
    gap = 18 * cl(k); xl = x - w / 2; wl = w * frac
    for rx, rw, col, s_ in ((xl - gap / 2, wl, lc, left), (xl + wl + gap / 2, w - wl, rc, right)):
        rr = R.MakeXYWH(rx, y - h / 2, rw, h); c.drawRoundRect(rr, 16, 16, paint(col)); c.drawRoundRect(rr, 16, 16, stroke(INK, 7))
        f = h * 0.42
        while font("ant", f).measureText(s_) > rw - 22 and f > 20: f -= 2
        c.drawString(s_, rx + rw / 2 - font("ant", f).measureText(s_) / 2, y + f * 0.36, font("ant", f), paint(WHITE))


def feed_phone(c, x, y, w=340, t=0.0, tilt=0.0, ad=True, k=1.0):
    """a phone with a scrolling feed: short video cards with an AD card between them. Plain shapes, no app UI."""
    if k <= 0: return
    h = w * 1.9
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k, k)
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), w * 0.14, w * 0.14, paint((22, 22, 32))); c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), w * 0.14, w * 0.14, stroke(INK, 6))
    scr = R.MakeXYWH(-w * 0.44, -h * 0.46, w * 0.88, h * 0.92)
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(scr, w * 0.08, w * 0.08), True)
    ch = h * 0.92; off = (t * 0.18 % 3.0) * ch; cols = ((76, 60, 150), (255, 196, 60), (40, 130, 150))
    for i in range(-1, 5):
        yy = -h * 0.46 + i * ch - (off % (ch * 3))
        j = i % 3; c.drawRect(R.MakeXYWH(-w * 0.44, yy, w * 0.88, ch + 1), paint(cols[j]))
        if j == 1 and ad: ctext(c, "AD", 0, yy + ch * 0.55, "ant", w * 0.3, INK)
        else: c.drawPath(poly([(-w * 0.08, yy + ch * 0.42), (-w * 0.08, yy + ch * 0.58), (w * 0.12, yy + ch * 0.5)], True), paint(WHITE, 0.92))
    c.restore(); c.restore()


def line_meter(c, x, y, w, frac, label, need="10M", k=1.0, ok=False, t=0.0):
    """a progress bar with one hard mark at its end: are you past the line?"""
    if k <= 0: return
    h = 76; c.save(); c.translate(x, y); c.scale(k, k)
    rr = R.MakeXYWH(-w / 2, -h / 2, w, h); c.drawRoundRect(rr, h / 2, h / 2, paint((24, 30, 46))); 
    fl = w * cl(frac)
    if fl > 8: c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, fl, h), h / 2, h / 2, paint(GRN if ok else ORANGE))
    c.drawRoundRect(rr, h / 2, h / 2, stroke(INK, 7))
    c.drawLine(w / 2 - 8, -h, w / 2 - 8, h, stroke(RED_C, 11))
    f = font("ant", 46); c.drawString(need, w / 2 - 8 - f.measureText(need) / 2, -h - 16, f, paint(WHITE))
    fl2 = font("mxb", 32); c.drawString(label, -w / 2, h + 34, fl2, paint(WHITE))
    c.restore()


# ------------------------------------------------------------------ HOW TO START EP 5 (reselling): the rack as a held object + a count you can see
def swing(t, t0, a=7.0):
    """damped hanger swing in degrees after t0: pass as tilt= to jacket()"""
    return a * math.exp(-max(t - t0, 0) * 2.4) * math.sin(max(t - t0, 0) * 8.5) if t >= t0 else 0.0


def rack(c, y=772, x0=70, x1=1010, floor=FLOOR):
    """clothes rack: one thin pipe across the room, two posts. Hang jackets from y - 4. Put step numbers on them and it is a roadmap."""
    for x in (x0, x1):
        c.drawLine(x, y, x, floor - 6, stroke((20, 22, 44), 16)); c.drawLine(x, y, x, floor - 6, stroke((96, 104, 136), 7))
    c.drawLine(x0 - 12, y, x1 + 12, y, stroke((20, 22, 44), 18)); c.drawLine(x0 - 12, y, x1 + 12, y, stroke((196, 202, 220), 8))


def jacket_grid(c, t, t0, d, worn=0.0, n=30, cols=6, x0=130, y0=790, dx=92, dy=112, w=76):
    """n small jackets landing one by one, d seconds apart: makes a legal count visible. Returns how many have landed."""
    pal = ((70, 120, 200), (200, 80, 70), (60, 160, 120), (150, 110, 190), (230, 160, 60)); landed = 0
    for i in range(n):
        q = pr(t, t0 + i * d, 0.16)
        if q <= 0: continue
        landed += 1
        jacket(c, x0 + (i % cols) * dx, y0 + (i // cols) * dy + 60 * (1 - eo(q)), w, col=mix(pal[i % 5], (130, 130, 140), 0.5 * worn), k=eo(q), hanger=False)
    return landed



# ------------------------------------------------------------------ HOW TO START EP 6 (home bakery): the night kitchen + bakes
def home_kitchen(c, t, lamp=(540, 1140), lamp_a=0.5, top=(46, 26, 58), bot=(120, 66, 84)):
    """one held world: a home kitchen at night. Wall shelf with jars across the top, pendant lamp, worktop line at the back, dark floor."""
    night_bg(c, t, top, bot, lamp=lamp, lamp_a=lamp_a, floor=None)
    dk = (24, 12, 30)
    c.drawRect(R.MakeLTRB(0, 0, W, 66), paint(dk)); c.drawRect(R.MakeLTRB(0, 118, W, 132), paint(dk))
    for i in range(9):      # jars on the shelf, read as a silhouette
        x = 40 + i * 122 + 14 * hsh(i, 6); w = 46 + 34 * hsh(i, 7); h = 30 + 20 * hsh(i, 8)
        c.drawRoundRect(R.MakeXYWH(x, 118 - h, w, h), 8, 8, paint(mix(dk, (150, 110, 110), 0.3)))
    c.drawLine(lamp[0], 132, lamp[0], 470, stroke(dk, 6))
    c.drawPath(poly([(lamp[0] - 60, 520), (lamp[0] + 60, 520), (lamp[0] + 26, 470), (lamp[0] - 26, 470)], True), paint(dk))
    c.drawRect(R.MakeLTRB(0, FLOOR - 250, 150, FLOOR), paint(mix(dk, bot, 0.25))); c.drawRect(R.MakeLTRB(930, FLOOR - 250, W, FLOOR), paint(mix(dk, bot, 0.25)))
    c.drawRect(R.MakeLTRB(0, FLOOR - 262, 164, FLOOR - 242), paint(mix(dk, (220, 190, 170), 0.3))); c.drawRect(R.MakeLTRB(916, FLOOR - 262, W, FLOOR - 242), paint(mix(dk, (220, 190, 170), 0.3)))
    c.drawRect(R.MakeLTRB(0, FLOOR, W, H), paint(shader=lin(0, FLOOR, 0, H, [argb(mix(bot, (0, 0, 0), 0.5)), argb(mix(bot, (0, 0, 0), 0.8))])))
    c.drawLine(0, FLOOR, W, FLOOR, stroke(INK, 5))
    fg_dust(c, t, n=7, seed=33, a=0.18)


def oven(c, x, y=FLOOR, w=360, glow=0.6, k=1.0):
    """home oven, x = centre, y = bottom; glow = the window lit from inside"""
    if k <= 0: return
    h = w * 1.05
    c.save(); c.translate(x, y); c.scale(k, k)
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h, w, h), 16, 16, paint((226, 226, 232))); c.drawRoundRect(R.MakeXYWH(-w / 2, -h, w, h), 16, 16, stroke(INK, 7))
    for i in range(4): c.drawCircle(-w * 0.3 + i * w * 0.2, -h + 42, 15, paint(INK))
    wx, wy, ww, wh = -w * 0.36, -h * 0.72, w * 0.72, h * 0.46
    c.drawRoundRect(R.MakeXYWH(wx, wy, ww, wh), 12, 12, paint(mix((40, 30, 34), (255, 170, 70), glow))); c.drawRoundRect(R.MakeXYWH(wx, wy, ww, wh), 12, 12, stroke(INK, 6))
    c.drawLine(wx + 10, wy + wh * 0.68, wx + ww - 10, wy + wh * 0.68, stroke(INK, 4))
    c.drawLine(-w * 0.32, -h * 0.8, w * 0.32, -h * 0.8, stroke(INK, 11))
    c.restore()


def cookie(c, x, y, r=46, k=1.0, spin=0.0):
    """one flat cookie with chocolate chips"""
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(spin); c.scale(k, k)
    c.drawCircle(0, 0, r, paint((214, 160, 96))); c.drawCircle(0, 0, r, stroke(INK, max(3, r * 0.1)))
    for i in range(6):
        a = i * 1.05 + 0.4; d = r * (0.25 + 0.42 * hsh(i, 2))
        c.drawCircle(math.cos(a) * d, math.sin(a) * d, r * 0.13, paint((70, 42, 30)))
    c.restore()


def cookie_tray(c, x, y, w=440, cols=4, rows=3, k=1.0, shown=None):
    """baking tray of cookies seen from above; shown = how many have landed"""
    if k <= 0: return
    h = w * (rows / cols) * 0.96
    c.save(); c.translate(x, y); c.scale(k, k)
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), 14, 14, paint((96, 100, 112))); c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), 14, 14, stroke(INK, 7))
    n = rows * cols if shown is None else shown; r = w / cols * 0.38
    for j in range(rows):
        for i in range(cols):
            if j * cols + i < n: cookie(c, -w / 2 + (i + 0.5) * w / cols, -h / 2 + (j + 0.5) * h / rows, r, spin=(i * 37 + j * 11) % 360)
    c.restore()


def muffin(c, x, y, w=200, k=1.0, tilt=0.0):
    """x = centre, y = bottom"""
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k, k)
    c.drawPath(poly([(-w * 0.34, -w * 0.5), (w * 0.34, -w * 0.5), (w * 0.26, 0), (-w * 0.26, 0)], True), paint((236, 120, 110))); c.drawPath(poly([(-w * 0.34, -w * 0.5), (w * 0.34, -w * 0.5), (w * 0.26, 0), (-w * 0.26, 0)], True), stroke(INK, 6))
    for i in range(1, 5): c.drawLine(-w * 0.34 + i * w * 0.136, -w * 0.5, -w * 0.26 + i * w * 0.104, 0, stroke(INK, 3))
    top = skia.Path(); top.addOval(R.MakeXYWH(-w * 0.46, -w * 0.92, w * 0.92, w * 0.56))
    c.drawPath(top, paint((214, 160, 96))); c.drawPath(top, stroke(INK, 6))
    for i in range(5): c.drawCircle(-w * 0.24 + i * w * 0.12, -w * (0.68 + 0.08 * hsh(i, 9)), w * 0.03, paint((70, 42, 30)))
    c.restore()


def cell_bars(c, x0, y0, x1, y1, n=7):
    """plain prison-window bars laid over a prop, no people behind them"""
    for i in range(n):
        xx = x0 + (i + 0.5) * (x1 - x0) / n
        c.drawLine(xx, y0, xx, y1, stroke((40, 44, 54), 16))
    c.drawRect(R.MakeLTRB(x0, y0 - 10, x1, y0 + 10), paint((40, 44, 54))); c.drawRect(R.MakeLTRB(x0, y1 - 10, x1, y1 + 10), paint((40, 44, 54)))


def cake_box(c, x, y, w=560, lines=None, k=1.0, tilt=0.0, size=34, title=None):
    """a plain white bakery box with a paper label; lines = the label text, one string per row. x = centre, y = bottom"""
    if k <= 0: return
    h = w * 0.72
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k, k)
    c.drawOval(R.MakeXYWH(-w * 0.56, -14, w * 1.12, 30), paint((0, 0, 0), 0.25, blur=10))
    c.drawRect(R.MakeXYWH(-w / 2, -h, w, h), paint((248, 246, 240))); c.drawRect(R.MakeXYWH(-w / 2, -h, w, h), stroke(INK, 7))
    c.drawPath(poly([(-w / 2, -h), (w / 2, -h), (w * 0.42, -h - w * 0.09), (-w * 0.42, -h - w * 0.09)], True), paint((232, 228, 220))); c.drawPath(poly([(-w / 2, -h), (w / 2, -h), (w * 0.42, -h - w * 0.09), (-w * 0.42, -h - w * 0.09)], True), stroke(INK, 6))
    if lines:
        lw, lh = w * 0.86, h * 0.8
        c.drawRect(R.MakeXYWH(-lw / 2, -h * 0.9, lw, lh), paint((255, 236, 170))); c.drawRect(R.MakeXYWH(-lw / 2, -h * 0.9, lw, lh), stroke(INK, 4))
        y0 = -h * 0.9 + 16
        if title: ctext(c, title, 0, y0 + size, "ant", size * 1.15, INK); y0 += size * 1.5
        for i, s in enumerate(lines): ctext(c, s, 0, y0 + size * (i + 1) * 1.2, "ant", size, INK)
    c.restore()


def cookie_grid(c, cx, cy, n=80, cols=10, w=780, k=1.0, shown=None):
    """a count you can see: n small cookies in rows (eighty dozen a week)"""
    d = w / cols; m = n if shown is None else int(shown)
    rows = math.ceil(n / cols)
    for j in range(rows):
        for i in range(cols):
            idx = j * cols + i
            if idx < min(n, m): cookie(c, cx - w / 2 + (i + 0.5) * d, cy - rows * d / 2 + (j + 0.5) * d, d * 0.38 * k, spin=idx * 29)


# ------------------------------------------------------------------ HOW IT WORKS EP 4 (hotel fees): the lobby + elevator
def hotel_lobby(c, t, lamp=(540, 1130), lamp_a=0.45, top=(16, 32, 66), bot=(44, 72, 118)):
    """one held world: a hotel lobby at night. Dark ceiling with a row of small lights across the top, marble line, potted plants at the edges, dark floor."""
    night_bg(c, t, top, bot, lamp=lamp, lamp_a=lamp_a, floor=None)
    dk = (8, 14, 34)
    c.drawRect(R.MakeLTRB(0, 0, W, 104), paint(dk))
    for i in range(7):
        x = 90 + i * 150
        c.drawLine(x, 104, x, 148, stroke(dk, 5)); c.drawCircle(x, 158, 15, paint(LAMP, 0.95)); c.drawCircle(x, 158, 42, paint(LAMP, 0.2, blur=18))
    for x, s in ((64, 1.0), (1016, 0.9)):       # plants
        c.drawRect(R.MakeXYWH(x - 42 * s, FLOOR - 92 * s, 84 * s, 92 * s), paint((30, 26, 44))); c.drawRect(R.MakeXYWH(x - 42 * s, FLOOR - 92 * s, 84 * s, 92 * s), stroke(INK, 4))
        for a in (-40, -15, 15, 40): 
            xx = x + 110 * s * math.sin(math.radians(a)); yy = FLOOR - 92 * s - 190 * s * math.cos(math.radians(a))
            c.drawLine(x, FLOOR - 92 * s, xx, yy, stroke((14, 44, 48), 26))
    c.drawRect(R.MakeLTRB(0, FLOOR, W, H), paint(shader=lin(0, FLOOR, 0, H, [argb(mix(bot, (0, 0, 0), 0.45)), argb(mix(bot, (0, 0, 0), 0.8))])))
    c.drawLine(0, FLOOR, W, FLOOR, stroke(INK, 5))
    fg_dust(c, t, n=6, seed=41, a=0.16)


def elevator(c, x, y=FLOOR, w=420, price="$199", floor_=None, open_=0.0, k=1.0, col=LAMP):
    """brass elevator doors with a price where the floor number should be. Same object all episode: the price climbs. x = centre, y = bottom; open_ 0..1"""
    if k <= 0: return
    h = w * 1.5
    c.save(); c.translate(x, y); c.scale(k, k)
    c.drawRect(R.MakeXYWH(-w / 2 - 22, -h - 22, w + 44, h + 22), paint((70, 56, 40))); c.drawRect(R.MakeXYWH(-w / 2 - 22, -h - 22, w + 44, h + 22), stroke(INK, 6))
    c.drawRect(R.MakeXYWH(-w / 2, -h, w, h), paint((20, 18, 26)))
    if open_ > 0: c.drawRect(R.MakeXYWH(-w / 2, -h, w, h), paint(LAMP, 0.5 * open_))
    dw = w / 2 * (1 - 0.86 * cl(open_))
    for side in (-1, 1):
        xx = -w / 2 if side < 0 else w / 2 - dw
        c.drawRect(R.MakeXYWH(xx, -h, dw, h), paint((186, 150, 96))); c.drawRect(R.MakeXYWH(xx, -h, dw, h), stroke(INK, 5))
    pw = w * 0.72; ph = w * 0.3
    c.drawRoundRect(R.MakeXYWH(-pw / 2, -h - 22 - ph - 12, pw, ph), 14, 14, paint((12, 12, 18))); c.drawRoundRect(R.MakeXYWH(-pw / 2, -h - 22 - ph - 12, pw, ph), 14, 14, stroke(INK, 5))
    ctext(c, price, 0, -h - 22 - 12 - ph * 0.22, "ant", ph * 0.72, col)
    if floor_ is not None:
        for i in range(4):
            cx = -w * 0.24 + i * w * 0.16; on = i + 1 == floor_
            c.drawCircle(cx, -h - 22 - ph - 34, 13, paint(col if on else (60, 56, 66)))
    c.restore()


def hotel_card(c, x, y, w, rate, name="HOTEL A", note=None, k=1.0, hl=False, tilt=0.0):
    """a plain listing row on a booking page: no site UI. x, y = centre"""
    if k <= 0: return
    h = w * 0.34
    card(c, x, y, w, h, 1.0, tilt=tilt, k=k)
    c.drawRoundRect(R.MakeXYWH(-w / 2 + 16, -h / 2 + 16, h - 32, h - 32), 10, 10, paint((86, 110, 160)))
    for i in range(3):
        for j in range(3): c.drawRect(R.MakeXYWH(-w / 2 + 34 + i * (h - 32) * 0.26, -h / 2 + 32 + j * (h - 32) * 0.26, (h - 32) * 0.15, (h - 32) * 0.15), paint(LAMP))
    ctext(c, name, -w * 0.02, -h * 0.1, "ant", h * 0.24, (90, 90, 104))
    if note: ctext(c, note, -w * 0.02, h * 0.28, "mss", h * 0.13, (150, 60, 50))
    ctext(c, rate, w * 0.32, h * 0.14, "ant", h * 0.46, RED_C if hl else INK)
    card_end(c)


def ticket(c, x, y, w=320, k=1.0, tilt=-6.0, label="TICKET"):
    """plain event ticket with a torn notch, no venue or seller"""
    if k <= 0: return
    h = w * 0.46
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k, k)
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), 12, 12, paint((250, 214, 110))); c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), 12, 12, stroke(INK, 6))
    c.drawLine(w * 0.22, -h / 2 + 8, w * 0.22, h / 2 - 8, stroke(INK, 4))
    ctext(c, label, -w * 0.12, h * 0.14, "ant", h * 0.36, INK)
    c.restore()


def front_desk(c, x=540, y=FLOOR, w=760, k=1.0):
    """reception desk seen from the guest side, with a small bell"""
    if k <= 0: return
    h = 240
    c.save(); c.translate(x, y); c.scale(k, k)
    c.drawRect(R.MakeXYWH(-w / 2, -h, w, h), paint((88, 62, 44))); c.drawRect(R.MakeXYWH(-w / 2, -h, w, h), stroke(INK, 6))
    c.drawRect(R.MakeXYWH(-w / 2 - 22, -h - 22, w + 44, 26), paint((212, 192, 160))); c.drawRect(R.MakeXYWH(-w / 2 - 22, -h - 22, w + 44, 26), stroke(INK, 5))
    c.drawCircle(w * 0.3, -h - 40, 26, paint((226, 190, 90))); c.drawCircle(w * 0.3, -h - 40, 26, stroke(INK, 4)); c.drawCircle(w * 0.3, -h - 72, 7, paint(INK))
    c.restore()


def room_key(c, x, y, w=260, k=1.0, tilt=-8.0):
    """a plain hotel key card, no chain"""
    if k <= 0: return
    h = w * 0.62
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k, k)
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), 14, 14, paint((60, 90, 150))); c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), 14, 14, stroke(INK, 6))
    c.drawRect(R.MakeXYWH(-w / 2, -h * 0.18, w, h * 0.2), paint(INK)); ctext(c, "ROOM", 0, h * 0.42, "ant", h * 0.24, WHITE)
    c.restore()


# ------------------------------------------------------------------ HOW IT WORKS EP 2 (credit score): Skia redraw of the props in anim_props8
def car_lot(c, t, lamp=(540, 1130), lamp_a=0.45, top=(14, 30, 58), bot=(38, 74, 104)):
    """one held world: a car lot at dusk. String of bulbs across the top, flat car silhouettes at the edges, dark floor."""
    night_bg(c, t, top, bot, lamp=lamp, lamp_a=lamp_a, floor=None)
    dk = (8, 16, 32)
    c.drawRect(R.MakeLTRB(0, 0, W, 60), paint(dk))
    pts = [(x, 110 + 34 * math.sin(math.pi * ((x % 270) / 270))) for x in range(0, W + 30, 30)]
    for a, b in zip(pts, pts[1:]): c.drawLine(a[0], a[1], b[0], b[1], stroke(dk, 4))
    for i, p in enumerate(pts):
        if i % 3 == 1: c.drawCircle(p[0], p[1] + 12, 10, paint(LAMP, 0.95)); c.drawCircle(p[0], p[1] + 12, 28, paint(LAMP, 0.18, blur=12))
    for x, flip in ((80, 1), (1000, -1)):
        c.drawRoundRect(R.MakeXYWH(x - 170, FLOOR - 100, 340, 76), 22, 22, paint(mix(dk, bot, 0.3))); c.drawRoundRect(R.MakeXYWH(x - 95 + 20 * flip, FLOOR - 150, 170, 60), 18, 18, paint(mix(dk, bot, 0.3)))
    c.drawRect(R.MakeLTRB(0, FLOOR, W, H), paint(shader=lin(0, FLOOR, 0, H, [argb(mix(bot, (0, 0, 0), 0.5)), argb(mix(bot, (0, 0, 0), 0.8))])))
    c.drawLine(0, FLOOR, W, FLOOR, stroke(INK, 5))
    fg_dust(c, t, n=6, seed=51, a=0.14)


def car(c, x, y, w=560, col=(70, 150, 240), k=1.0, tag=None):
    """generic flat car, x = centre, y = bottom; no brand"""
    if k <= 0: return
    h = w * 0.3
    c.save(); c.translate(x, y); c.scale(k, k)
    c.drawOval(R.MakeXYWH(-w * 0.52, -12, w * 1.04, 26), paint((0, 0, 0), 0.28, blur=10))
    c.drawPath(poly([(-w * 0.26, -h), (-w * 0.14, -h * 1.72), (w * 0.2, -h * 1.72), (w * 0.34, -h)], True), paint(col)); c.drawPath(poly([(-w * 0.26, -h), (-w * 0.14, -h * 1.72), (w * 0.2, -h * 1.72), (w * 0.34, -h)], True), stroke(INK, 6))
    c.drawPath(poly([(-w * 0.2, -h * 1.03), (-w * 0.11, -h * 1.58), (w * 0.02, -h * 1.58), (w * 0.02, -h * 1.03)], True), paint((196, 228, 244))); c.drawPath(poly([(w * 0.06, -h * 1.03), (w * 0.06, -h * 1.58), (w * 0.18, -h * 1.58), (w * 0.27, -h * 1.03)], True), paint((196, 228, 244)))
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h * 1.12, w, h * 0.92), 22, 22, paint(col)); c.drawRoundRect(R.MakeXYWH(-w / 2, -h * 1.12, w, h * 0.92), 22, 22, stroke(INK, 6))
    for xx in (-w * 0.28, w * 0.28):
        c.drawCircle(xx, -h * 0.2, h * 0.3, paint(INK)); c.drawCircle(xx, -h * 0.2, h * 0.13, paint((200, 204, 212)))
    if tag: price_tag(c, w * 0.34, -h * 1.8, tag, tilt=6, size=48)
    c.restore()


_PIE_COLS = [(90, 120, 200), (60, 170, 180), (150, 110, 220), ORANGE, (250, 196, 60)]
def score_slices(c, cx, cy, r, vals=(10, 10, 15, 35, 30), k=(1, 1, 1, 1, 1), hl=None, labels=None, cols=None):
    """one pie that fills through the episode. vals in %, k = 0..1 per slice as it sweeps in, hl = index that pops outward. Dark empty disc behind."""
    cols = cols or _PIE_COLS
    c.drawCircle(cx, cy, r + 8, paint((0, 0, 0), 0.25, blur=14)); c.drawCircle(cx, cy, r, paint((26, 30, 50))); c.drawCircle(cx, cy, r, stroke(INK, 7))
    a0 = -90.0
    for i, v in enumerate(vals):
        sw = v * 3.6; kk = cl(k[i] if i < len(k) else 0)
        if kk > 0:
            m = math.radians(a0 + sw / 2); off = 22 if hl == i else 0; xx = cx + math.cos(m) * off; yy = cy + math.sin(m) * off
            p = skia.Path(); p.moveTo(xx, yy); p.arcTo(R.MakeXYWH(xx - r, yy - r, 2 * r, 2 * r), a0, sw * kk, False); p.close()
            c.drawPath(p, paint(cols[i % len(cols)])); c.drawPath(p, stroke(INK, 6))
            if labels and labels[i] and kk >= 1: ctext(c, labels[i], xx + math.cos(m) * r * 0.62, yy + math.sin(m) * r * 0.62 + r * 0.05, "ant", r * 0.15, INK)
        a0 += sw


def gauge(c, x, y, w=560, frac=0.5, lo="300", hi="850", k=1.0):
    """half-dial score gauge; x, y = needle pivot"""
    if k <= 0: return
    r = w / 2
    c.save(); c.translate(x, y); c.scale(k, k)
    c.drawRoundRect(R.MakeXYWH(-r - 26, -r - 30, w + 52, r + 76), 26, 26, paint((248, 246, 240))); c.drawRoundRect(R.MakeXYWH(-r - 26, -r - 30, w + 52, r + 76), 26, 26, stroke(INK, 6))
    for i, col in enumerate((RED_C, (250, 170, 60), (250, 214, 80), GRN)):
        p = skia.Path(); p.arcTo(R.MakeXYWH(-r + 26, -r + 26, 2 * r - 52, 2 * r - 52), 180 + i * 45, 44, True)
        pp = paint(col); pp.setStyle(skia.Paint.kStroke_Style); pp.setStrokeWidth(46); c.drawPath(p, pp)
    a = math.radians(180 + 180 * cl(frac))
    c.drawLine(0, 0, math.cos(a) * (r - 74), math.sin(a) * (r - 74), stroke(INK, 10)); c.drawCircle(0, 0, 18, paint(INK))
    ctext(c, lo, -r + 30, 36, "ant", 34, INK); ctext(c, hi, r - 30, 36, "ant", 34, INK)
    c.restore()


def cycle_strip(c, x, y, w=860, k=3, pay=None):
    """a month as a strip: 1 PAY DAY?, 2 STATEMENT ENDS = reported, 3 DUE DATE. k = markers shown; pay = 0..1 position of a coin before the red marker"""
    h = 96
    c.drawRoundRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), 22, 22, paint((248, 246, 240))); c.drawRoundRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), 22, 22, stroke(INK, 6))
    for i in range(1, 30):
        xx = x - w / 2 + i * w / 30; c.drawLine(xx, y - 14, xx, y + 14, stroke((190, 190, 196), 3))
    for i, (fx, s, col) in enumerate(((0.12, "MONTH STARTS", (120, 124, 140)), (0.62, "STATEMENT ENDS", RED_C), (0.92, "DUE", (60, 150, 90)))):
        if i < k:
            xx = x - w / 2 + fx * w
            c.drawCircle(xx, y, 22, paint(col)); c.drawCircle(xx, y, 22, stroke(INK, 4))
            ctext(c, s, min(max(xx, x - w / 2 + 130), x + w / 2 - 40), y - 78 if i != 1 else y + 112, "ant", 42, WHITE)
    if pay is not None: coin(c, x - w / 2 + lerp(0.92, 0.5, cl(pay)) * w, y - 2, 28)


def credit_report(c, x, y, w=460, err=False, title="CREDIT REPORT", k=1.0, tilt=-3.0):
    """a generic report sheet with no agency look; x, y = centre; err = one row circled"""
    if k <= 0: return
    h = w * 1.28
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k, k)
    c.drawRect(R.MakeXYWH(-w / 2 + 6, -h / 2 + 8, w, h), paint((0, 0, 0), 0.25, blur=10)); c.drawRect(R.MakeXYWH(-w / 2, -h / 2, w, h), paint(WHITE)); c.drawRect(R.MakeXYWH(-w / 2, -h / 2, w, h), stroke(INK, 6))
    ctext(c, title, 0, -h / 2 + w * 0.14, "ant", w * 0.1, INK)
    for i in range(7):
        yy = -h / 2 + w * 0.26 + i * w * 0.13
        c.drawLine(-w * 0.38, yy, w * 0.14, yy, stroke((150, 154, 170), 8)); c.drawLine(w * 0.22, yy, w * 0.38, yy, stroke((90, 94, 110), 8))
        if err and i == 3:
            c.drawOval(R.MakeXYWH(-w * 0.44, yy - w * 0.06, w * 0.88, w * 0.12), stroke(RED_C, 7))
    c.restore()
