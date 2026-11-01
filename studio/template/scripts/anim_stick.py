# ================= line-art stick cast (exec'd after anim_mascot3d.py) — owner, 1 Nov 2026 =================
# Owner sent a reference (white cartoon guy, thick black outline, big round head + ears, big eyes, wide grin, spiky hair strokes,
# white collar shirt + coloured tie, slim outlined limbs, ground line) and said: "use this type of character; change the dress colour
# like the tie colour, or sometimes the hair". Our own design in that spirit (never a copy of any artist's character):
#   white skin/body, black ink outline, ONE or TWO colour accents per character: tie, shirt/top, hair, dress, cap.
# Same API as the lit cast: person(f, x, y, s, who, la, ra, ll, rl, lean, sit, mouth, blink, brow, look, expr, bob, hold, hold_off,
# face_dir, op, shadow, sweat, back) and person_head_at(...). guy() = the hero (orange tie). STICK=0 -> lit 2.5D cast.
import os as _os
STICK = _os.environ.get("STICK", "1") != "0"
INK_ = (22, 22, 26); PAPER = (252, 252, 248)

STICK_LOOKS = {   # tie / shirt / hair (None = white with ink lines) / hairstyle / girl / extras
    "hero":     dict(tie=(255, 128, 0), shirt=None, hair=None, style="spikes"),
    "friend":   dict(tie=None, shirt=(40, 150, 255), hair=(40, 30, 26), style="curls"),
    "girl":     dict(tie=None, shirt=(255, 80, 160), hair=(60, 40, 30), style="ponytail", girl=True),
    "girl2":    dict(tie=None, shirt=(150, 90, 240), hair=(250, 200, 60), style="long", girl=True),
    "lady":     dict(tie=None, shirt=(235, 50, 60), hair=(40, 30, 26), style="bun", girl=True),
    "inventor": dict(tie=None, shirt=(0, 180, 170), hair=(120, 70, 40), style="bun", girl=True, glasses=True),
    "exec":     dict(tie=(220, 30, 40), shirt=None, jacket=(40, 60, 150), hair=None, style="side"),
    "creator":  dict(tie=None, shirt=(120, 200, 40), hair=None, style="cap", cap=(120, 200, 40)),
    "worker":   dict(tie=None, shirt=(255, 140, 0), hair=None, style="hardhat", cap=(255, 210, 0)),
    "oldman":   dict(tie=(130, 80, 200), shirt=None, hair=(220, 220, 220), style="bald", glasses=True, mustache=True),
    "kid":      dict(tie=None, shirt=(255, 205, 0), hair=None, style="spikes", small=True),
    "mystery":  dict(tie=None, shirt=(40, 40, 50), hair=None, style="hat", cap=(30, 30, 36)),
    "judge":    dict(tie=None, shirt=(40, 40, 50), hair=(230, 230, 230), style="long", girl=True),
}


def _slook(who):
    if isinstance(who, dict):
        L = dict(STICK_LOOKS.get(who.get("base", "hero"), STICK_LOOKS["hero"]))
        for k_, v in who.items():
            if k_ == "base": continue
            if k_ in ("col", "top"): L["shirt"] = tuple(v)
            else: L[k_] = v
        return L
    return STICK_LOOKS.get(who, STICK_LOOKS["hero"])


def _c3(c): return tuple(float(v) / 255 for v in c)


def _lighter(c, k=0.35): return tuple(int(v + (255 - v) * k) for v in c)


def _darker(c, k=0.7): return tuple(int(v * k) for v in c)


def _limb(g, p, q, th, col=PAPER, ow=None):
    ow = ow if ow is not None else max(4, th * 0.42)
    P = (int(round(p[0])), int(round(p[1]))); Q = (int(round(q[0])), int(round(q[1])))
    cv2.line(g, P, Q, _c3(INK_), int(th + 2 * ow), cv2.LINE_AA)
    cv2.line(g, P, Q, _c3(col), max(1, int(th)), cv2.LINE_AA)


def _stick_head_el(who, mouth, blink, brow, lx, ly, expr, sweat, back, k):
    L = _slook(who)
    key = ("inkhead", repr(sorted((a, repr(b)) for a, b in L.items())), mouth, blink, brow, lx, ly, expr, sweat, back, round(k, 2))
    if key in _gc: return _gc[key]
    SS = 3; w = h = 280; sc = k * SS; R = 86; cx, cy = 140, 150
    S = lambda *v: [x * sc for x in v]; lw = lambda v: max(1, int(v * sc))
    im = Image.new("RGBA", (int(w * sc), int(h * sc)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ink = INK_ + (255,); pap = PAPER + (255,); st = L.get("style", "spikes")
    hairc = (tuple(L["hair"]) + (255,)) if L.get("hair") else pap
    if st == "long": d.rounded_rectangle(S(cx - 98, cy - 50, cx + 98, cy + 104), int(44 * sc), fill=hairc, outline=ink, width=lw(6))
    if st == "ponytail":
        d.ellipse(S(cx + 62, cy - 40, cx + 128, cy + 64), fill=hairc, outline=ink, width=lw(6))
    if st == "bun": d.ellipse(S(cx - 34, cy - R - 50, cx + 34, cy - R + 14), fill=hairc, outline=ink, width=lw(6))
    for ex in (-1, 1):   # ears
        d.ellipse(S(cx + ex * (R + 2) - 16, cy - 6, cx + ex * (R + 2) + 16, cy + 30), fill=pap, outline=ink, width=lw(6))
        d.arc(S(cx + ex * (R + 2) - 8, cy + 2, cx + ex * (R + 2) + 8, cy + 22), 90 if ex > 0 else 270, 270 if ex > 0 else 90, fill=ink, width=lw(3))
    d.ellipse(S(cx - R, cy - R, cx + R, cy + R), fill=pap, outline=ink, width=lw(7))
    if not back:
        # eyes: big white ovals, thick ink rim, big pupils looking slightly sideways (lx/ly), sparkle
        for i, ex in enumerate((cx - 34, cx + 34)):
            ey = cy - 2
            if blink:
                d.arc(S(ex - 24, ey - 10, ex + 24, ey + 14), 20, 160, fill=ink, width=lw(7)); continue
            rx, ry = (28, 30) if expr == "wow" else (25, 26)
            if expr == "sus": ry = 13
            d.ellipse(S(ex - rx, ey - ry, ex + rx, ey + ry), fill=pap, outline=ink, width=lw(6))
            px, py = ex + 6 + lx * 9, ey - 2 + ly * 7
            pr = 13 if expr != "sus" else 8
            d.ellipse(S(px - pr, py - pr, px + pr, py + pr), fill=ink)
            d.ellipse(S(px - pr * 0.55, py - pr * 0.6, px - pr * 0.05, py - pr * 0.1), fill=pap)
        if L.get("glasses"):
            for ex in (cx - 34, cx + 34): d.rounded_rectangle(S(ex - 32, cy - 32, ex + 32, cy + 28), int(14 * sc), outline=ink, width=lw(5))
        # brows: thick ink strokes
        for i, ex in enumerate((cx - 34, cx + 34)):
            sgn = -1 if i == 0 else 1
            if brow == "up": a_, b_ = (ex - 24 * sgn * -1, cy - 50), (ex + 22 * sgn * -1, cy - 60)
            elif brow in ("sus", "mad"): a_, b_ = (ex - 24 * sgn, cy - 58), (ex + 18 * sgn * -1 * -1, cy - 40)
            elif brow == "sad": a_, b_ = (ex - 22 * sgn, cy - 42), (ex + 20 * sgn, cy - 58)
            else: a_, b_ = (ex - 22, cy - 46), (ex + 22, cy - 50)
            if brow in ("sus", "mad"): a_, b_ = ((ex - 24, cy - 58), (ex + 20, cy - 42)) if i == 0 else ((ex - 20, cy - 42), (ex + 24, cy - 58))
            if brow == "up": a_, b_ = ((ex - 22, cy - 50), (ex + 22, cy - 62)) if i == 0 else ((ex - 22, cy - 62), (ex + 22, cy - 50))
            d.line(S(*a_, *b_), fill=ink, width=lw(8))
        if L.get("mustache"): d.chord(S(cx - 34, cy + 28, cx + 34, cy + 52), 180, 360, fill=(235, 235, 235, 255), outline=ink, width=lw(4))
        my = cy + 44
        if expr == "wow" and mouth == 0: mouth = "o"
        if mouth == 0:
            if expr == "sad": d.arc(S(cx - 26, my, cx + 26, my + 26), 200, 340, fill=ink, width=lw(7))
            elif expr in ("sus", "mad"): d.line(S(cx - 20, my + 8, cx + 22, my + 4), fill=ink, width=lw(7))
            elif expr == "smirk":   # the reference's lopsided grin
                d.polygon(S(cx - 48, my - 6, cx + 50, my + 2, cx + 30, my + 26, cx - 16, my + 24), fill=pap, outline=ink)
                d.line(S(cx - 48, my - 6, cx + 50, my + 2), fill=ink, width=lw(6)); d.arc(S(cx - 48, my - 34, cx + 50, my + 30), 20, 160, fill=ink, width=lw(6))
            else:      # wide open grin with teeth
                d.chord(S(cx - 46, my - 24, cx + 46, my + 34), 10, 170, fill=pap, outline=ink, width=lw(6))
                d.line(S(cx - 44, my - 2, cx + 44, my - 2), fill=ink, width=lw(5))
        elif mouth == "o":
            d.ellipse(S(cx - 14, my - 6, cx + 14, my + 26), fill=(150, 30, 40, 255), outline=ink, width=lw(5))
        else:
            hh = {1: 14, 2: 22, 3: 30}.get(mouth, 14); ww = {1: 34, 2: 40, 3: 44}.get(mouth, 34)
            d.chord(S(cx - ww, my - 16, cx + ww, my - 16 + hh * 2), 0, 180, fill=(150, 30, 40, 255), outline=ink, width=lw(6))
            d.chord(S(cx - ww + 8, my - 14, cx + ww - 8, my - 2), 0, 180, fill=pap)
            if mouth >= 2: d.ellipse(S(cx - ww * 0.45, my - 16 + hh * 1.1, cx + ww * 0.45, my - 16 + hh * 1.9), fill=(255, 120, 130, 255))
        if sweat:
            d.polygon(S(cx + 78, cy - 70, cx + 66, cy - 40, cx + 90, cy - 40), fill=(130, 205, 255, 255))
            d.ellipse(S(cx + 64, cy - 52, cx + 92, cy - 24), fill=(130, 205, 255, 255), outline=ink, width=lw(4))
    # hair on top (in front of the head)
    if st == "spikes":
        pts = [(cx - 52, cy - R + 26), (cx - 30, cy - R - 26), (cx - 18, cy - R + 8), (cx + 4, cy - R - 40), (cx + 14, cy - R + 6),
               (cx + 40, cy - R - 22), (cx + 52, cy - R + 24)]
        if L.get("hair"): d.polygon(S(*sum(pts, ())), fill=hairc, outline=ink, width=lw(6))
        else:
            for a_, b_ in zip(pts[:-1], pts[1:]): d.line(S(*a_, *b_), fill=ink, width=lw(7))
            d.polygon(S(*sum(pts, ())), fill=pap)
            for a_, b_ in zip(pts[:-1], pts[1:]): d.line(S(*a_, *b_), fill=ink, width=lw(7))
    elif st == "curls":
        for bx in (-54, -20, 16, 50): d.ellipse(S(cx + bx - 24, cy - R - 18, cx + bx + 24, cy - R + 28), fill=hairc, outline=ink, width=lw(5))
    elif st == "side":
        d.chord(S(cx - R - 2, cy - R - 6, cx + R + 2, cy - R + 76), 180, 360, fill=hairc, outline=ink, width=lw(6))
        d.line(S(cx - 20, cy - R - 2, cx - 34, cy - R + 34), fill=ink, width=lw(5))
    elif st in ("long", "ponytail", "bun"):
        d.chord(S(cx - R - 4, cy - R - 8, cx + R + 4, cy - R + 74), 180, 360, fill=hairc, outline=ink, width=lw(6))
        if L.get("girl"):
            d.polygon(S(cx + 38, cy - R - 2, cx + 14, cy - R - 26, cx + 14, cy - R + 22), fill=(255, 220, 60, 255), outline=ink, width=lw(4)) if st == "ponytail" else None
    elif st == "bald":
        for ex in (-1, 1): d.arc(S(cx + ex * 70 - 26, cy - 50, cx + ex * 70 + 26, cy - 4), 200 if ex < 0 else 270, 340 if ex < 0 else 60, fill=ink, width=lw(6))
    elif st == "cap":
        capc = tuple(L.get("cap", (120, 200, 40))) + (255,)
        d.chord(S(cx - R - 2, cy - R - 12, cx + R + 2, cy - R + 80), 180, 360, fill=capc, outline=ink, width=lw(6))
        d.rounded_rectangle(S(cx - 6, cy - R + 26, cx + R + 46, cy - R + 42), int(8 * sc), fill=capc, outline=ink, width=lw(5))
    elif st == "hardhat":
        capc = tuple(L.get("cap", (255, 210, 0))) + (255,)
        d.chord(S(cx - R - 6, cy - R - 20, cx + R + 6, cy - R + 76), 180, 360, fill=capc, outline=ink, width=lw(6))
        d.rounded_rectangle(S(cx - R - 22, cy - R + 26, cx + R + 22, cy - R + 42), int(8 * sc), fill=capc, outline=ink, width=lw(5))
    elif st == "hat":
        capc = tuple(L.get("cap", (30, 30, 36))) + (255,)
        d.rounded_rectangle(S(cx - R - 30, cy - R + 8, cx + R + 30, cy - R + 28), int(8 * sc), fill=capc, outline=ink, width=lw(4))
        d.rounded_rectangle(S(cx - 56, cy - R - 60, cx + 56, cy - R + 14), int(14 * sc), fill=capc, outline=ink, width=lw(4))
    el = el_from(im.resize((int(w * k), int(h * k)), Image.LANCZOS))
    _gc[key] = el; return el


def stick_person(f, x, y, s=1.0, who="hero", la=(18, 8), ra=(18, 8), ll=7, rl=7, lean=0.0, sit=False, mouth=0, blink=False, brow="n",
                 look=(0, 0), expr="n", bob=0.0, hold=None, hold_off=(0, 0), face_dir=1, op=1.0, shadow=True, sweat=False, back=False):
    L = _slook(who)
    if L.get("small"): s = s * 0.82
    g = f if op >= 0.999 else f.copy()
    th = 16 * s; lr = math.radians(lean); ink = _c3(INK_)
    shirt = L.get("shirt"); jacket = L.get("jacket"); top = jacket or shirt or PAPER
    if not sit:
        hip = (x, y - 190 * s)
        if shadow:
            contact(g, x, y + 6 * s, 200 * s, 0.30)
            cv2.line(g, (int(x - 120 * s), int(y + 14 * s)), (int(x + 120 * s), int(y + 14 * s)), ink, max(2, int(7 * s)), cv2.LINE_AA)   # ground line
    else:
        hip = (x, y)
    neck = (hip[0] + 170 * s * math.sin(lr), hip[1] - 170 * s * math.cos(lr))
    # legs (white, outlined) + ink shoes
    if not sit:
        for side, ang in ((-1, ll), (1, rl)):
            hp = (hip[0] + side * 16 * s, hip[1])
            ft = (hp[0] + side * math.sin(math.radians(ang)) * 184 * s, hp[1] + math.cos(math.radians(ang)) * 184 * s)
            _limb(g, hp, ft, th * 1.25, PAPER if not L.get("girl") else PAPER)
            sx = ft[0] + side * 16 * s
            cv2.ellipse(g, (int(sx), int(ft[1])), (int(30 * s), int(14 * s)), 0, 180, 360, ink, -1, cv2.LINE_AA)
            cv2.rectangle(g, (int(sx - 30 * s), int(ft[1] - 1)), (int(sx + 30 * s), int(ft[1] + 6 * s)), ink, -1, cv2.LINE_AA)
    else:
        for side in (-1, 1):
            hp = (hip[0] + side * 16 * s, hip[1]); kn = (hip[0] + side * 62 * s, hip[1] + 10 * s); ft = (hip[0] + side * 66 * s, hip[1] + 120 * s)
            _limb(g, hp, kn, th * 1.25); _limb(g, kn, ft, th * 1.25)
    # torso: slim rounded shirt shape (white or coloured), collar + tie; girls: coloured dress
    ow = max(3, int(7 * s))
    if L.get("girl"):
        pts = np.array([(neck[0] - 30 * s, neck[1] + 14 * s), (neck[0] + 30 * s, neck[1] + 14 * s), (hip[0] + 78 * s, hip[1] + 46 * s),
                        (hip[0] - 78 * s, hip[1] + 46 * s)], np.int32)
        cv2.fillPoly(g, [pts], _c3(shirt or (255, 80, 160)), cv2.LINE_AA); cv2.polylines(g, [pts], True, ink, ow, cv2.LINE_AA)
        cv2.line(g, (int(hip[0] - 60 * s), int(hip[1] + 30 * s)), (int(hip[0] + 60 * s), int(hip[1] + 30 * s)), _c3(_lighter(shirt or (255, 80, 160), 0.5)), max(2, int(6 * s)), cv2.LINE_AA)
    else:
        pts = np.array([(neck[0] - 34 * s, neck[1] + 10 * s), (neck[0] + 34 * s, neck[1] + 10 * s), (hip[0] + 38 * s, hip[1] + 6 * s),
                        (hip[0] - 38 * s, hip[1] + 6 * s)], np.int32)
        cv2.fillPoly(g, [pts], _c3(top), cv2.LINE_AA); cv2.polylines(g, [pts], True, ink, ow, cv2.LINE_AA)
        if jacket:   # white shirt V under an open jacket
            v = np.array([(neck[0] - 18 * s, neck[1] + 12 * s), (neck[0] + 18 * s, neck[1] + 12 * s), (neck[0], neck[1] + 90 * s)], np.int32)
            cv2.fillPoly(g, [v], _c3(PAPER), cv2.LINE_AA); cv2.polylines(g, [v], True, ink, max(2, ow - 2), cv2.LINE_AA)
        # collar
        for side in (-1, 1):
            c = np.array([(neck[0], neck[1] + 12 * s), (neck[0] + side * 22 * s, neck[1] + 6 * s), (neck[0] + side * 16 * s, neck[1] + 30 * s)], np.int32)
            cv2.fillPoly(g, [c], _c3(PAPER), cv2.LINE_AA); cv2.polylines(g, [c], True, ink, max(2, ow - 3), cv2.LINE_AA)
        if L.get("tie"):
            p0 = (neck[0], neck[1] + 14 * s)
            t_ = np.array([(p0[0] - 9 * s, p0[1]), (p0[0] + 9 * s, p0[1]), (p0[0] + 14 * s, p0[1] + 70 * s), (p0[0], p0[1] + 86 * s), (p0[0] - 14 * s, p0[1] + 70 * s)], np.int32)
            cv2.fillPoly(g, [t_], _c3(L["tie"]), cv2.LINE_AA); cv2.polylines(g, [t_], True, ink, max(2, ow - 3), cv2.LINE_AA)
    # arms + hands (white, outlined; sleeves take the top colour near the shoulder)
    sh = (neck[0], neck[1] + 20 * s); hands = {}
    for side, (a1, a2) in ((-1, la), (1, ra)):
        a1 = a1 + 10 if a1 < 60 else a1
        sp = (sh[0] + side * 26 * s, sh[1])
        e = (sp[0] + side * math.sin(math.radians(a1)) * 80 * s, sp[1] + math.cos(math.radians(a1)) * 80 * s)
        hd = (e[0] + side * math.sin(math.radians(a2)) * 74 * s, e[1] + math.cos(math.radians(a2)) * 74 * s)
        _limb(g, sp, e, th, top if top != PAPER else PAPER); _limb(g, e, hd, th); hands[side] = hd
    if hold is not None:
        hx, hy = hands[1]; comp(g, hold, hx + hold_off[0] * s, hy + hold_off[1] * s)
    for side, hd in hands.items():
        cv2.circle(g, (int(hd[0]), int(hd[1])), int(19 * s), ink, -1, cv2.LINE_AA)
        cv2.circle(g, (int(hd[0]), int(hd[1])), int(14 * s), _c3(PAPER), -1, cv2.LINE_AA)
        cv2.ellipse(g, (int(hd[0] + side * 12 * s), int(hd[1] - 8 * s)), (int(7 * s), int(10 * s)), 0, 0, 360, ink, max(2, int(4 * s)), cv2.LINE_AA)
    k = max(0.2, round(s * 20) / 20)
    hel = _stick_head_el(who, mouth, blink, brow, look[0], look[1], expr, sweat, back, k)
    hs = hel[1].shape[1] / 280.0
    hel = hel if abs(hs - s) < 0.02 else scale_el(hel, s / hs)
    comp(g, hel, neck[0], neck[1] - 92 * s + bob * s)
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
    o = INK_ + (255,); c = tuple(col) + (255,); cx, cy = w / 2, h * 0.52
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
