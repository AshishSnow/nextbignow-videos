# ================= colourful stick cast (exec'd after anim_mascot3d.py) — owner, 31 Oct 2026 =================
# "Visual not good, use colourful stick men and girls." Every character is a bright single-colour stick figure with a big round
# head, white eyes, thick rounded limbs and a dark outline, plus one or two accessories (hair, bow, cap, tie, glasses, dress).
# Same API as anim_mascot3d.person(): person(f, x, y, s, who, la, ra, ll, rl, lean, sit, mouth, blink, brow, look, expr, bob,
# hold, hold_off, face_dir, op, shadow, sweat, back) and person_head_at(f, cx, cy, s, who, ...). guy() = the hero (orange).
# STICK=0 switches back to the lit 2.5D cast.
import os as _os
STICK = _os.environ.get("STICK", "1") != "0"

STICK_LOOKS = {   # col = body + head colour (bright, saturated); acc = accessories
    "hero":     dict(col=(255, 120, 20), acc=("tuft",)),
    "friend":   dict(col=(30, 150, 255), acc=("curls",)),
    "girl":     dict(col=(255, 70, 160), acc=("ponytail", "bow"), girl=True),
    "girl2":    dict(col=(150, 80, 240), acc=("long", "clip"), girl=True),
    "lady":     dict(col=(230, 40, 60), acc=("bun",), girl=True),
    "inventor": dict(col=(0, 180, 170), acc=("bun", "glasses"), girl=True),
    "exec":     dict(col=(40, 70, 190), acc=("slick", "tie")),
    "creator":  dict(col=(120, 200, 30), acc=("cap",)),
    "worker":   dict(col=(30, 170, 80), acc=("hardhat",)),
    "oldman":   dict(col=(140, 140, 160), acc=("glasses", "mustache")),
    "kid":      dict(col=(255, 200, 0), acc=("tuft",), small=True),
    "mystery":  dict(col=(40, 36, 48), acc=("hat",), dark=True),
    "judge":    dict(col=(50, 46, 60), acc=("long",), girl=True),
}
_OUTL = (26, 22, 34)


def _slook(who):
    if isinstance(who, dict):
        base = who.get("base", "hero"); L = dict(STICK_LOOKS.get(base, STICK_LOOKS["hero"]))
        if "col" in who: L["col"] = tuple(who["col"])
        elif "top" in who: L["col"] = tuple(who["top"])
        if "acc" in who: L["acc"] = tuple(who["acc"])
        if "girl" in who: L["girl"] = who["girl"]
        return L
    return STICK_LOOKS.get(who, STICK_LOOKS["hero"])


def _c3(c): return tuple(float(v) / 255 for v in c)


def _lighter(c, k=0.35): return tuple(int(v + (255 - v) * k) for v in c)


def _darker(c, k=0.7): return tuple(int(v * k) for v in c)


def _limb(g, p, q, th, col):
    P = (int(round(p[0])), int(round(p[1]))); Q = (int(round(q[0])), int(round(q[1])))
    cv2.line(g, P, Q, _c3(_OUTL), int(th + 8), cv2.LINE_AA)
    cv2.line(g, P, Q, _c3(col), int(th), cv2.LINE_AA)


def _stick_head_el(who, mouth, blink, brow, lx, ly, expr, sweat, back, k):
    key = ("stickhead", repr(_slook(who)), mouth, blink, brow, lx, ly, expr, sweat, back, round(k, 2))
    if key in _gc: return _gc[key]
    L = _slook(who); col = L["col"]; acc = L.get("acc", ())
    SS = 3; R = 74; w = h = 260; sc = k * SS
    W3 = int(w * sc); H3 = int(h * sc); S = lambda *v: [x * sc for x in v]; lw = lambda v: max(1, int(v * sc))
    im = Image.new("RGBA", (W3, H3), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, cy = 130, 140; o = _OUTL + (255,); c = tuple(col) + (255,)
    hair = _darker(col, 0.45) + (255,)
    # back hair / accessories behind the head
    if "long" in acc: d.rounded_rectangle(S(cx - 84, cy - 40, cx + 84, cy + 92), int(40 * sc), fill=hair, outline=o, width=lw(5))
    if "ponytail" in acc:
        d.ellipse(S(cx + 54, cy - 30, cx + 112, cy + 70), fill=hair, outline=o, width=lw(5))
    if "bun" in acc: d.ellipse(S(cx - 30, cy - R - 44, cx + 30, cy - R + 12), fill=hair, outline=o, width=lw(5))
    d.ellipse(S(cx - R - 4, cy - R - 4, cx + R + 4, cy + R + 4), fill=o)
    d.ellipse(S(cx - R, cy - R, cx + R, cy + R), fill=c)
    d.ellipse(S(cx - R * 0.62, cy - R * 0.78, cx - R * 0.05, cy - R * 0.38), fill=_lighter(col, 0.55) + (150,))   # gloss
    if not back:
        dark = (26, 22, 34, 255)
        for i, ex in enumerate((cx - 28, cx + 28)):
            ey = cy - 4
            if blink:
                d.arc(S(ex - 16, ey - 8, ex + 16, ey + 10), 20, 160, fill=dark, width=lw(6)); continue
            rx, ry = (21, 25) if expr == "wow" else (18, 21)
            if expr == "sus": ry = 11
            d.ellipse(S(ex - rx, ey - ry, ex + rx, ey + ry), fill=(255, 255, 255, 255), outline=dark, width=lw(4))
            px, py = ex + lx * 7, ey + ly * 6 + 2
            d.ellipse(S(px - 9, py - 10, px + 9, py + 10), fill=dark)
            d.ellipse(S(px - 6, py - 7, px - 1, py - 2), fill=(255, 255, 255, 255))
        if "glasses" in acc:
            for ex in (cx - 28, cx + 28): d.ellipse(S(ex - 27, cy - 31, ex + 27, cy + 23), outline=dark, width=lw(5))
            d.line(S(cx - 1, cy - 6, cx + 1, cy - 6), fill=dark, width=lw(5))
        for i, ex in enumerate((cx - 28, cx + 28)):
            if brow == "up": a_, b_ = ((ex - 18, cy - 40), (ex + 16, cy - 46)) if i == 0 else ((ex - 16, cy - 46), (ex + 18, cy - 40))
            elif brow in ("sus", "mad"): a_, b_ = ((ex - 18, cy - 44), (ex + 16, cy - 32)) if i == 0 else ((ex - 16, cy - 32), (ex + 18, cy - 44))
            elif brow == "sad": a_, b_ = ((ex - 18, cy - 32), (ex + 16, cy - 44)) if i == 0 else ((ex - 16, cy - 44), (ex + 18, cy - 32))
            else: a_, b_ = ((ex - 18, cy - 38), (ex + 16, cy - 40)) if i == 0 else ((ex - 16, cy - 40), (ex + 18, cy - 38))
            d.line(S(*a_, *b_), fill=dark, width=lw(7))
        if "mustache" in acc: d.chord(S(cx - 28, cy + 16, cx + 28, cy + 40), 180, 360, fill=(240, 240, 240, 255), outline=dark, width=lw(3))
        my = cy + 40
        if expr == "wow" and mouth == 0: mouth = "o"
        if mouth == 0:
            if expr == "sad": d.arc(S(cx - 20, my - 2, cx + 20, my + 20), 200, 340, fill=dark, width=lw(6))
            elif expr == "smirk": d.arc(S(cx - 22, my - 16, cx + 20, my + 6), 10, 120, fill=dark, width=lw(6))
            elif expr in ("sus", "mad"): d.line(S(cx - 14, my + 4, cx + 14, my + 2), fill=dark, width=lw(6))
            else: d.arc(S(cx - 24, my - 22, cx + 24, my + 10), 25, 155, fill=dark, width=lw(6))
        elif mouth == "o":
            d.ellipse(S(cx - 11, my - 8, cx + 11, my + 16), fill=(120, 20, 40, 255), outline=dark, width=lw(4))
        else:
            hh = {1: 10, 2: 17, 3: 24}.get(mouth, 10); ww = {1: 18, 2: 22, 3: 26}.get(mouth, 18)
            d.chord(S(cx - ww, my - 10, cx + ww, my - 10 + hh * 2), 0, 180, fill=(120, 20, 40, 255), outline=dark, width=lw(4))
            if mouth >= 2: d.ellipse(S(cx - ww * 0.5, my - 10 + hh * 0.9, cx + ww * 0.5, my - 10 + hh * 1.8), fill=(255, 110, 130, 255))
        for bx in (cx - 50, cx + 50): d.ellipse(S(bx - 13, cy + 14, bx + 13, cy + 28), fill=(255, 255, 255, 70))
        if sweat:
            d.polygon(S(cx + 74, cy - 50, cx + 64, cy - 24, cx + 84, cy - 24), fill=(120, 200, 255, 255))
            d.ellipse(S(cx + 62, cy - 34, cx + 86, cy - 10), fill=(120, 200, 255, 255), outline=dark, width=lw(3))
    # front accessories
    if "tuft" in acc:
        d.chord(S(cx - R + 6, cy - R - 2, cx + R - 6, cy - R + 46), 180, 360, fill=hair, outline=o, width=lw(4))
        d.polygon(S(cx - 44, cy - R + 14, cx - 30, cy - R - 26, cx - 10, cy - R + 4, cx + 2, cy - R - 32, cx + 20, cy - R + 4,
                    cx + 40, cy - R - 22, cx + 46, cy - R + 14), fill=hair, outline=o, width=lw(4))
    if "curls" in acc:
        for bx in (-46, -18, 12, 42): d.ellipse(S(cx + bx - 20, cy - R - 16, cx + bx + 20, cy - R + 22), fill=hair, outline=o, width=lw(4))
    if "slick" in acc: d.chord(S(cx - R, cy - R - 6, cx + R, cy - R + 70), 180, 360, fill=hair, outline=o, width=lw(4))
    if "bow" in acc:
        d.polygon(S(cx + 30, cy - R + 4, cx + 6, cy - R - 20, cx + 6, cy - R + 26), fill=(255, 230, 60, 255), outline=o, width=lw(4))
        d.polygon(S(cx + 30, cy - R + 4, cx + 56, cy - R - 20, cx + 56, cy - R + 26), fill=(255, 230, 60, 255), outline=o, width=lw(4))
        d.ellipse(S(cx + 22, cy - R - 4, cx + 38, cy - R + 12), fill=(255, 200, 30, 255), outline=o, width=lw(3))
    if "clip" in acc: d.rounded_rectangle(S(cx - 60, cy - 66, cx - 22, cy - 52), int(6 * sc), fill=(255, 230, 60, 255), outline=o, width=lw(3))
    if "long" in acc and not back: d.chord(S(cx - R - 6, cy - R - 8, cx + R + 6, cy - R + 60), 180, 360, fill=hair, outline=o, width=lw(4))
    if "cap" in acc:
        d.chord(S(cx - R, cy - R - 10, cx + R, cy - R + 74), 180, 360, fill=(255, 255, 255, 255), outline=o, width=lw(5))
        d.rounded_rectangle(S(cx - 10, cy - R + 18, cx + R + 40, cy - R + 34), int(8 * sc), fill=(255, 255, 255, 255), outline=o, width=lw(4))
    if "hardhat" in acc:
        d.chord(S(cx - R - 4, cy - R - 16, cx + R + 4, cy - R + 70), 180, 360, fill=(255, 210, 0, 255), outline=o, width=lw(5))
        d.rounded_rectangle(S(cx - R - 18, cy - R + 22, cx + R + 18, cy - R + 36), int(6 * sc), fill=(255, 210, 0, 255), outline=o, width=lw(4))
    if "hat" in acc:
        d.rounded_rectangle(S(cx - R - 26, cy - R + 6, cx + R + 26, cy - R + 24), int(8 * sc), fill=(20, 18, 24, 255), outline=o, width=lw(3))
        d.rounded_rectangle(S(cx - 50, cy - R - 54, cx + 50, cy - R + 12), int(14 * sc), fill=(20, 18, 24, 255), outline=o, width=lw(3))
    el = el_from(im.resize((int(w * k), int(h * k)), Image.LANCZOS))
    _gc[key] = el; return el


def stick_person(f, x, y, s=1.0, who="hero", la=(18, 8), ra=(18, 8), ll=7, rl=7, lean=0.0, sit=False, mouth=0, blink=False, brow="n",
                 look=(0, 0), expr="n", bob=0.0, hold=None, hold_off=(0, 0), face_dir=1, op=1.0, shadow=True, sweat=False, back=False):
    L = _slook(who); col = L["col"]; acc = L.get("acc", ())
    if L.get("small"): s = s * 0.82;
    g = f if op >= 0.999 else f.copy()
    th = 26 * s; lr = math.radians(lean)
    if not sit:
        hip = (x, y - 190 * s)
        if shadow: contact(g, x, y + 6 * s, 220 * s, 0.4)
    else:
        hip = (x, y)
    neck = (hip[0] + 170 * s * math.sin(lr), hip[1] - 170 * s * math.cos(lr))
    # legs
    if not sit:
        for side, ang in ((-1, ll), (1, rl)):
            hp = (hip[0] + side * 10 * s, hip[1])
            kn = (hp[0] + side * math.sin(math.radians(ang)) * 92 * s, hp[1] + math.cos(math.radians(ang)) * 92 * s)
            ft = (hp[0] + side * math.sin(math.radians(ang)) * 184 * s, hp[1] + math.cos(math.radians(ang)) * 184 * s)
            _limb(g, hp, ft, th, col)
            sx = ft[0] + side * 14 * s
            cv2.ellipse(g, (int(sx), int(ft[1])), (int(26 * s), int(15 * s)), 0, 0, 360, _c3(_OUTL), -1, cv2.LINE_AA)
            cv2.ellipse(g, (int(sx), int(ft[1])), (int(21 * s), int(10 * s)), 0, 0, 360, _c3(_darker(col, 0.55)), -1, cv2.LINE_AA)
    else:
        for side in (-1, 1):
            hp = (hip[0] + side * 10 * s, hip[1]); kn = (hip[0] + side * 60 * s, hip[1] + 10 * s); ft = (hip[0] + side * 64 * s, hip[1] + 120 * s)
            _limb(g, hp, kn, th, col); _limb(g, kn, ft, th, col)
    # body
    if L.get("girl"):
        cv2.fillPoly(g, [np.array([(neck[0] - 26 * s, neck[1] + 20 * s), (neck[0] + 26 * s, neck[1] + 20 * s), (hip[0] + 70 * s, hip[1] + 40 * s),
                                   (hip[0] - 70 * s, hip[1] + 40 * s)], np.int32)], _c3(_OUTL), cv2.LINE_AA)
        cv2.fillPoly(g, [np.array([(neck[0] - 20 * s, neck[1] + 26 * s), (neck[0] + 20 * s, neck[1] + 26 * s), (hip[0] + 62 * s, hip[1] + 34 * s),
                                   (hip[0] - 62 * s, hip[1] + 34 * s)], np.int32)], _c3(col), cv2.LINE_AA)
        cv2.line(g, (int(hip[0] - 50 * s), int(hip[1] + 22 * s)), (int(hip[0] + 50 * s), int(hip[1] + 22 * s)), _c3(_lighter(col, 0.5)), max(2, int(6 * s)), cv2.LINE_AA)
    else:
        _limb(g, neck, hip, th * 1.15, col)
    if "tie" in acc:
        p0 = (neck[0], neck[1] + 20 * s)
        cv2.fillPoly(g, [np.array([(p0[0] - 10 * s, p0[1]), (p0[0] + 10 * s, p0[1]), (p0[0] + 8 * s, p0[1] + 70 * s), (p0[0], p0[1] + 84 * s), (p0[0] - 8 * s, p0[1] + 70 * s)], np.int32)],
                     _c3((230, 30, 40)), cv2.LINE_AA)
    # arms
    sh = (neck[0], neck[1] + 22 * s); hands = {}
    for side, (a1, a2) in ((-1, la), (1, ra)):
        a1 = a1 + 14 if a1 < 60 else a1          # stick arms read better a little away from the body
        e = (sh[0] + side * math.sin(math.radians(a1)) * 82 * s, sh[1] + math.cos(math.radians(a1)) * 82 * s)
        hd = (e[0] + side * math.sin(math.radians(a2)) * 76 * s, e[1] + math.cos(math.radians(a2)) * 76 * s)
        _limb(g, sh, e, th * 0.9, col); _limb(g, e, hd, th * 0.9, col); hands[side] = hd
    if hold is not None:
        hx, hy = hands[1]; comp(g, hold, hx + hold_off[0] * s, hy + hold_off[1] * s)
    for side, hd in hands.items():
        cv2.circle(g, (int(hd[0]), int(hd[1])), int(17 * s), _c3(_OUTL), -1, cv2.LINE_AA)
        cv2.circle(g, (int(hd[0]), int(hd[1])), int(13 * s), _c3(_lighter(col, 0.25)), -1, cv2.LINE_AA)
    # head (centre ~ y - 446 s when standing, same as the lit cast)
    k = max(0.2, round(s * 20) / 20)
    hel = _stick_head_el(who, mouth, blink, brow, look[0], look[1], expr, sweat, back, k)
    hs = hel[1].shape[1] / 260.0
    hel = hel if abs(hs - s) < 0.02 else scale_el(hel, s / hs)
    comp(g, hel, neck[0], neck[1] - 76 * s + bob * s - 10 * s)
    if op < 0.999: f[:] = f * (1 - op) + g * op
    return hands


if STICK:
    _person_lit = person
    person = stick_person          # noqa: F811
    guy = lambda f, x, y, s=1.0, **kw: stick_person(f, x, y, s, "hero", **kw)   # noqa: E731,F811
    head_el = lambda mouth=0, blink=False, brow="n", lx=0, ly=0, expr="n": _stick_head_el("hero", mouth, blink, brow, lx, ly, expr, False, False, 1.0)   # noqa: E731,F811

    def person_head_at(f, cx, cy, s, who="hero", **kw):   # noqa: F811
        return stick_person(f, cx, cy + 446 * s, s, who, **kw)


# ---------------- drone prop (HOW TO START EP 1; generic quadcopter, no brand) ----------------
def drone_el(w=420, t=0.0, col=(245, 245, 250), accent=(255, 120, 20)):
    """front-3/4 quadcopter: body, 4 arms, spinning rotor discs (t animates), camera gimbal, accent stripe"""
    sc = 2; h = int(w * 0.62)
    im = Image.new("RGBA", (w * sc, h * sc), (0, 0, 0, 0)); d = ImageDraw.Draw(im); S = lambda *v: [x * sc for x in v]
    o = _OUTL + (255,); c = tuple(col) + (255,); cx, cy = w / 2, h * 0.52
    for side in (-1, 1):
        for dz, yy in ((0.0, -0.06), (0.12, 0.10)):
            ax = cx + side * w * (0.36 - dz * 0.4); ay = cy + h * yy
            d.line(S(cx, cy, ax, ay - h * 0.08), fill=o, width=int(16 * sc)); d.line(S(cx, cy, ax, ay - h * 0.08), fill=c, width=int(10 * sc))
            d.rounded_rectangle(S(ax - 9, ay - h * 0.14, ax + 9, ay - h * 0.04), int(4 * sc), fill=(60, 62, 70, 255), outline=o, width=int(3 * sc))
            rw = w * 0.17; rh = h * 0.06; ph = (t * 40 + side + dz * 7) % 1.0
            d.ellipse(S(ax - rw, ay - h * 0.17 - rh, ax + rw, ay - h * 0.17 + rh), fill=(200, 220, 240, 90), outline=(80, 90, 110, 160), width=int(2 * sc))
            bx = rw * math.cos(ph * 6.283); d.line(S(ax - bx, ay - h * 0.17, ax + bx, ay - h * 0.17), fill=(50, 52, 60, 200), width=int(5 * sc))
    d.rounded_rectangle(S(cx - w * 0.17, cy - h * 0.15, cx + w * 0.17, cy + h * 0.12), int(26 * sc), fill=c, outline=o, width=int(5 * sc))
    d.rounded_rectangle(S(cx - w * 0.17, cy - h * 0.02, cx + w * 0.17, cy + h * 0.03), int(4 * sc), fill=tuple(accent) + (255,))
    d.ellipse(S(cx - w * 0.06, cy + h * 0.10, cx + w * 0.06, cy + h * 0.27), fill=(40, 42, 50, 255), outline=o, width=int(4 * sc))
    d.ellipse(S(cx - w * 0.03, cy + h * 0.15, cx + w * 0.03, cy + h * 0.22), fill=(90, 160, 255, 255))
    d.ellipse(S(cx - w * 0.12, cy - h * 0.12, cx - w * 0.02, cy - h * 0.05), fill=(255, 255, 255, 170))
    return el_from(im.resize((w, h), Image.LANCZOS))
