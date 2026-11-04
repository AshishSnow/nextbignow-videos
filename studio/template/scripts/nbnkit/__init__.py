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
                   (f"{_S}/fonts/montserrat/package/files/montserrat-latin-900-normal.woff", "Montserrat-Black.ttf")):
    if not os.path.exists(f"{_TTF}/{_dst}"):
        from fontTools.ttLib import TTFont
        _f = TTFont(_src); _f.flavor = None; _f.save(f"{_TTF}/{_dst}")
_gfx.FONTDIR = _TTF
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
