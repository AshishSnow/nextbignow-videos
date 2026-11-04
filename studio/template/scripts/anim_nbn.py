# ================= NBN look (exec'd after anim_clean.py, before anim_shots.py) — owner, 4 Nov 2026 =================
# "Looking too cartoon ... make it like NextBigNow." OopsMyBusiness now uses the NextBigNow what-if visual language:
#   * the NBN stick rig: small round white head with dot eyes, thick black stick limbs, a coloured scarf, small hands — no big
#     goggle eyes, no outlined white limbs. Same person() API as before, so every storyboard keeps working.
#   * NBN two-tier type: a small Montserrat line over ONE big clean Anton word/number (no comic outline), rising in.
#   * one brand pill at the top ("● OOPSMYBUSINESS · <SERIES>") instead of stacked badges; the story clock is one quiet line under it
#   * deeper night-to-colour gradients and slow floating light dust, like the NBN sets
# NBN=0 restores the line-art cartoon cast + old captions.
import os as _os
NBN = _os.environ.get("NBN", "1") != "0"
F_MS6 = f"{R}/fonts/montserrat/package/files/montserrat-latin-600-normal.woff"
F_MS8 = f"{R}/fonts/montserrat/package/files/montserrat-latin-800-normal.woff"
if not _os.path.exists(F_MS6): F_MS6 = F_MS8 = F_ANTON
_NBN_INK = (22, 22, 28)
_NL = dict(torso=78, uarm=48, farm=44, leg=108, head=46)
_SERIES_TXT = ["OOPSMYBUSINESS"]
_LINE = [None, None]   # [step/clock line, series title line] — one quiet line under the pill per frame


def _ink(a=1.0): return tuple(v / 255 for v in _NBN_INK)


def _nbn_look(who):
    L = _slook(who) if "_slook" in globals() else {}
    acc = L.get("tie") or L.get("shirt") or L.get("jacket") or (255, 128, 0)
    return L, acc


# ---------------------------------------------------------------- head (cached element)
_MOUTHS = {"va": "open", "vh": "open", "vo": "o", "vu": "o_s", "ve": "wide", "vl": "small", "vf": "small", "vm": "flat"}


def _nbn_head_el(who, mouth, blink, brow, lx, ly, expr, sweat, back, k):
    key = ("nbnhead", str(who), str(mouth), blink, brow, round(lx, 1), round(ly, 1), expr, sweat, back, k)

    def mk():
        L, acc = _nbn_look(who)
        sc = 3; u = 1.5 * k * sc; hr = _NL["head"] * u; P = int(hr * 2 + 70 * u); c0 = P / 2
        rgb = np.zeros((P, P, 3), np.float32); al = np.zeros((P, P), np.float32)
        ink = tuple(v / 255 for v in _NBN_INK); I = lambda v: int(round(v))

        def shape(fn):   # draw on colour + alpha together
            fn(rgb, None); fn(al, 1.0)
        hair = L.get("hair") or _NBN_INK; hcol = tuple(v / 255 for v in hair); st = L.get("style", "spikes")
        # back hair (long / ponytail) first
        if st in ("long",):
            shape(lambda a, o: cv2.ellipse(a, (I(c0), I(c0 + hr * 0.25)), (I(hr * 1.12), I(hr * 1.2)), 0, 0, 360, (o if o else hcol), -1, cv2.LINE_AA))
        if st == "ponytail":
            shape(lambda a, o: cv2.ellipse(a, (I(c0 + hr * 1.05), I(c0 + hr * 0.1)), (I(hr * 0.32), I(hr * 0.7)), -20, 0, 360, (o if o else hcol), -1, cv2.LINE_AA))
        if st == "bun":
            shape(lambda a, o: cv2.circle(a, (I(c0), I(c0 - hr * 1.02)), I(hr * 0.36), (o if o else hcol), -1, cv2.LINE_AA))
        # head disc + soft NBN shading + outline
        shape(lambda a, o: cv2.circle(a, (I(c0), I(c0)), I(hr + 3.5 * u), (o if o else ink), -1, cv2.LINE_AA))
        cv2.circle(rgb, (I(c0), I(c0)), I(hr - 3.5 * u), (1, 1, 1), -1, cv2.LINE_AA)
        yy, xx = np.mgrid[0:P, 0:P].astype(np.float32)
        d = np.sqrt((xx - (c0 - 10 * u)) ** 2 + (yy - (c0 - 12 * u)) ** 2) / (hr * 1.3)
        inside = (np.sqrt((xx - c0) ** 2 + (yy - c0) ** 2) < hr - 3.5 * u)
        sh = np.clip((d - 0.6) / 0.4, 0, 1) * 0.16 * inside
        rgb[:] = rgb * (1 - sh[..., None]) + np.array([0.16, 0.2, 0.35], np.float32) * sh[..., None]
        lw = lambda v: max(1, I(v * u))
        # hair on top
        if st == "spikes":
            for i, dx in enumerate((-0.5, -0.15, 0.2, 0.52)):
                pts = np.array([(c0 + (dx - 0.2) * hr, c0 - hr * 0.86 + abs(dx) * hr * 0.3), (c0 + (dx + 0.06) * hr, c0 - hr * (1.32 - 0.1 * (i % 2))),
                                (c0 + (dx + 0.24) * hr, c0 - hr * 0.88 + abs(dx) * hr * 0.25)], np.int32)
                shape(lambda a, o, pts=pts: cv2.fillPoly(a, [pts], (o if o else hcol), cv2.LINE_AA))
        elif st in ("side", "curls", "long", "ponytail", "bun"):
            shape(lambda a, o: cv2.ellipse(a, (I(c0), I(c0 - hr * 0.2)), (I(hr * 1.02), I(hr * 0.88)), 0, 180, 360, (o if o else hcol), -1, cv2.LINE_AA))
            cv2.ellipse(rgb, (I(c0 + hr * 0.15), I(c0 - hr * 0.05)), (I(hr * 0.75), I(hr * 0.42)), 0, 180, 360, (1, 1, 1), -1, cv2.LINE_AA)
        elif st in ("cap", "hardhat", "hat"):
            cc = tuple(v / 255 for v in (L.get("cap") if isinstance(L.get("cap"), tuple) else (255, 200, 30) if st == "hardhat" else acc))
            shape(lambda a, o: cv2.ellipse(a, (I(c0), I(c0 - hr * 0.3)), (I(hr * 1.02), I(hr * 0.9)), 0, 180, 360, (o if o else cc), -1, cv2.LINE_AA))
            shape(lambda a, o: cv2.rectangle(a, (I(c0 - hr * 1.15), I(c0 - hr * 0.36)), (I(c0 + hr * (1.5 if st == "cap" else 1.15)), I(c0 - hr * 0.2)), (o if o else cc), -1, cv2.LINE_AA))
            cv2.ellipse(rgb, (I(c0), I(c0 - hr * 0.3)), (I(hr * 1.02), I(hr * 0.9)), 0, 180, 360, ink, lw(3), cv2.LINE_AA)
        if back:
            return el_from(_rgba(rgb, al, sc))
        # face (NBN draw_face, scaled)
        ex = 15 * u; mx, my_ = lx * 6 * u, ly * 5 * u
        wide = expr in ("wow", "shock", "scared")
        if blink:
            for sx in (-1, 1): cv2.line(rgb, (I(c0 + sx * ex - 8 * u + mx), I(c0 - 4 * u + my_)), (I(c0 + sx * ex + 8 * u + mx), I(c0 - 4 * u + my_)), ink, lw(5), cv2.LINE_AA)
        elif expr in ("happy", "joy"):
            for sx in (-1, 1): cv2.ellipse(rgb, (I(c0 + sx * ex + mx), I(c0 - 2 * u + my_)), (I(9 * u), I(9 * u)), 0, 200, 340, ink, lw(5), cv2.LINE_AA)
        else:
            big = 1.35 if wide else 1.0
            for sx in (-1, 1):
                cv2.ellipse(rgb, (I(c0 + sx * ex + mx), I(c0 - 4 * u * big + my_ - 2 * u)), (I(6 * u * big), I(10 * u * big)), 0, 0, 360, ink, -1, cv2.LINE_AA)
                cv2.circle(rgb, (I(c0 + sx * ex - 2 * u * big + mx), I(c0 - 8 * u * big + my_ - 2 * u)), max(1, I(3 * u * big)), (1, 1, 1), -1, cv2.LINE_AA)
        b = brow if brow not in (None, "n") else {"sad": "worried", "angry": "angry", "sus": "sus", "wow": "up"}.get(expr, "n")
        for sx in (-1, 1):
            if b == "worried": p, q = (-9, -26 - sx * 4), (9, -26 + sx * 4)
            elif b == "angry": p, q = (-9, -28 + sx * 4), (9, -28 - sx * 4)
            elif b == "up" or (b == "sus" and sx == 1): p, q = (-8, -32), (8, -34)
            elif b == "sus": p, q = (-9, -26), (9, -26)
            else: continue
            cv2.line(rgb, (I(c0 + sx * ex + p[0] * u), I(c0 + p[1] * u)), (I(c0 + sx * ex + q[0] * u), I(c0 + q[1] * u)), ink, lw(4), cv2.LINE_AA)
        if L.get("glasses"):
            for sx in (-1, 1): cv2.circle(rgb, (I(c0 + sx * ex + mx), I(c0 - 6 * u + my_)), I(13 * u), ink, lw(3), cv2.LINE_AA)
            cv2.line(rgb, (I(c0 - ex + 13 * u + mx), I(c0 - 6 * u + my_)), (I(c0 + ex - 13 * u + mx), I(c0 - 6 * u + my_)), ink, lw(3), cv2.LINE_AA)
        mo = _MOUTHS.get(mouth, "open" if (isinstance(mouth, (int, float)) and mouth >= 2) else "small" if mouth == 1 else None)
        my = c0 + 16 * u + my_ * 0.5; cx = c0 + mx
        if mo is None:
            mo = {"wow": "o", "shock": "o", "sad": "frown", "angry": "flat", "smirk": "smirk", "happy": "grin", "joy": "grin", "sus": "flat", "worried": "frown"}.get(expr, "smile")
        if mo == "smile": cv2.ellipse(rgb, (I(cx), I(my - 4 * u)), (I(12 * u), I(10 * u)), 0, 20, 160, ink, lw(5), cv2.LINE_AA)
        elif mo == "smirk": cv2.ellipse(rgb, (I(cx + 4 * u), I(my - 4 * u)), (I(11 * u), I(8 * u)), -12, 10, 120, ink, lw(5), cv2.LINE_AA)
        elif mo == "grin": cv2.ellipse(rgb, (I(cx), I(my - 2 * u)), (I(15 * u), I(13 * u)), 0, 0, 180, ink, -1, cv2.LINE_AA)
        elif mo == "frown": cv2.ellipse(rgb, (I(cx), I(my + 10 * u)), (I(11 * u), I(8 * u)), 0, 200, 340, ink, lw(5), cv2.LINE_AA)
        elif mo == "flat": cv2.line(rgb, (I(cx - 9 * u), I(my + 4 * u)), (I(cx + 9 * u), I(my + 4 * u)), ink, lw(5), cv2.LINE_AA)
        elif mo == "o": cv2.ellipse(rgb, (I(cx), I(my + 5 * u)), (I(7 * u), I(9 * u)), 0, 0, 360, ink, -1, cv2.LINE_AA)
        elif mo == "o_s": cv2.ellipse(rgb, (I(cx), I(my + 4 * u)), (I(5 * u), I(6 * u)), 0, 0, 360, ink, -1, cv2.LINE_AA)
        elif mo == "open": cv2.ellipse(rgb, (I(cx), I(my + 2 * u)), (I(12 * u), I(10 * u)), 0, 0, 180, ink, -1, cv2.LINE_AA); cv2.line(rgb, (I(cx - 12 * u), I(my + 2 * u)), (I(cx + 12 * u), I(my + 2 * u)), ink, lw(4), cv2.LINE_AA)
        elif mo == "wide": cv2.ellipse(rgb, (I(cx), I(my + 3 * u)), (I(13 * u), I(6 * u)), 0, 0, 360, ink, -1, cv2.LINE_AA)
        elif mo == "small": cv2.ellipse(rgb, (I(cx), I(my + 3 * u)), (I(7 * u), I(5 * u)), 0, 0, 360, ink, -1, cv2.LINE_AA)
        if L.get("mustache"): cv2.ellipse(rgb, (I(cx), I(my - 4 * u)), (I(14 * u), I(5 * u)), 0, 0, 360, ink, -1, cv2.LINE_AA)
        if sweat:
            dx, dy = c0 + hr * 0.82, c0 - hr * 0.55
            pts = np.array([(dx, dy - 12 * u), (dx - 7 * u, dy + 4 * u), (dx + 7 * u, dy + 4 * u)], np.int32)
            shape(lambda a, o: (cv2.fillPoly(a, [pts], o if o else (0.45, 0.75, 1.0), cv2.LINE_AA), cv2.circle(a, (I(dx), I(dy + 4 * u)), I(7 * u), o if o else (0.45, 0.75, 1.0), -1, cv2.LINE_AA)))
        return el_from(_rgba(rgb, al, sc))
    return gcache(key, mk)


def _rgba(rgb, al, sc):
    im = np.dstack([np.clip(rgb, 0, 1) * 255, np.clip(al, 0, 1) * 255]).astype(np.uint8)
    im = Image.fromarray(im, "RGBA")
    return im.resize((max(1, im.size[0] // sc), max(1, im.size[1] // sc)), Image.LANCZOS)


# ---------------------------------------------------------------- body
def nbn_person(f, x, y, s=1.0, who="hero", la=(18, 8), ra=(18, 8), ll=7, rl=7, lean=0.0, sit=False, mouth=0, blink=False, brow="n",
               look=(0, 0), expr="n", bob=0.0, hold=None, hold_off=(0, 0), face_dir=1, op=1.0, shadow=True, sweat=False, back=False):
    L, acc = _nbn_look(who)
    if L.get("small"): s = s * 0.82
    if y > 1700 and not sit: y = 1548 + (y - 1700) * 0.3     # old cast stood at ~1840; the NBN figure stands on the floor line, clear of the caption bar
    u = 1.5 * s; g = f if op >= 0.999 else f.copy(); ink = _ink(); I = lambda v: int(round(v))
    lr = math.radians(lean); bb = bob * s
    if not sit:
        hip = (x, y - _NL["leg"] * u + bb)
        if shadow: _shadow(g, x, y, 46 * u)
    else:
        hip = (x, y)
    neck = (hip[0] + _NL["torso"] * u * math.sin(lr), hip[1] - _NL["torso"] * u * math.cos(lr))
    shp = (hip[0] + (_NL["torso"] - 8) * u * math.sin(lr), hip[1] - (_NL["torso"] - 8) * u * math.cos(lr))
    lw = I(13 * u)
    rim = (0.93, 0.95, 1.0); rw = lw + max(4, I(6 * u))
    rimg = None
    feet = []
    if not sit:
        for side, ang in ((-1, ll), (1, rl)):
            a = math.radians(ang); kn = (hip[0] + side * math.sin(a) * 54 * u * 0.9, hip[1] + math.cos(a) * 54 * u)
            ft = (hip[0] + side * math.sin(a) * 108 * u, hip[1] + math.cos(a) * 108 * u)
            _limb2(g, rimg, hip, kn, ft, ink, lw, rim, rw)
            feet.append(ft)
    else:
        for side in (-1, 1):
            kn = (hip[0] + side * 22 * u + 50 * u, hip[1] - 4 * u); ft = (kn[0] + 4 * u, kn[1] + 54 * u)
            _limb2(g, rimg, hip, kn, ft, ink, lw, rim, rw)
            feet.append(ft)
    for ft in feet: cv2.ellipse(g, (I(ft[0] + 3 * u), I(ft[1] - 2 * u)), (I(14 * u), I(7 * u)), 0, 0, 360, ink, -1, cv2.LINE_AA)
    # girls: a small coloured A-line dress over the hip (still a stick figure)
    if L.get("girl"):
        dc = tuple(v / 255 for v in (L.get("shirt") or acc))
        pts = np.array([(shp[0] - 12 * u, shp[1] + 4 * u), (shp[0] + 12 * u, shp[1] + 4 * u), (hip[0] + 34 * u, hip[1] + 24 * u), (hip[0] - 34 * u, hip[1] + 24 * u)], np.int32)
        cv2.fillPoly(g, [pts], dc, cv2.LINE_AA); cv2.polylines(g, [pts], True, ink, max(2, I(4 * u)), cv2.LINE_AA)
    else:   # NBN cave figure: a coloured shirt on the stick torso
        tc = tuple(v / 255 for v in (L.get("shirt") or L.get("jacket") or (250, 250, 252)))
        _limb2(g, rimg, hip, neck, None, ink, I(26 * u), rim, I(26 * u) + max(4, I(6 * u)))
        cv2.line(g, (I(hip[0]), I(hip[1] - 4 * u)), (I(neck[0]), I(neck[1] + 6 * u)), tc, I(17 * u), cv2.LINE_AA)
    # NBN scarf in the character's accent colour (hero = orange)
    sc_ = tuple(v / 255 for v in acc); nx, ny = neck
    p = np.array([(nx - 18 * u, ny + 4 * u), (nx + 18 * u, ny + 4 * u), (nx + 14 * u, ny + 18 * u), (nx - 14 * u, ny + 18 * u)], np.int32)
    tail = np.array([(nx - 10 * u, ny + 14 * u), (nx - 22 * u, ny + 34 * u), (nx - 34 * u, ny + 54 * u), (nx - 22 * u, ny + 60 * u), (nx - 10 * u, ny + 36 * u), (nx + 2 * u, ny + 16 * u)], np.int32)
    for q in (tail, p):
        cv2.fillPoly(g, [q], sc_, cv2.LINE_AA); cv2.polylines(g, [q], True, ink, max(2, I(4 * u)), cv2.LINE_AA)
    # arms (old la/ra convention: angles from straight down, outward)
    hands = {}
    for side, (a1, a2) in ((-1, la), (1, ra)):
        e = (shp[0] + side * math.sin(math.radians(a1)) * _NL["uarm"] * u, shp[1] + math.cos(math.radians(a1)) * _NL["uarm"] * u)
        hd = (e[0] + side * math.sin(math.radians(a2)) * _NL["farm"] * u, e[1] + math.cos(math.radians(a2)) * _NL["farm"] * u)
        _limb2(g, rimg, shp, e, hd, ink, lw, rim, rw)
        hands[side] = hd
    if hold is not None:
        hx, hy = hands[1]; comp(g, hold, hx + hold_off[0] * s, hy + hold_off[1] * s)
    for hd in hands.values():
        cv2.circle(g, (I(hd[0]), I(hd[1])), I(11.5 * u), ink, -1, cv2.LINE_AA); cv2.circle(g, (I(hd[0]), I(hd[1])), I(7.5 * u), (1, 1, 1), -1, cv2.LINE_AA)
    k = max(0.2, round(s * 20) / 20)
    hel = _nbn_head_el(who if not isinstance(who, dict) else repr(sorted(who.items())), mouth, blink, brow, look[0], look[1], expr, sweat, back, k) \
        if not isinstance(who, dict) else _nbn_head_dict(who, mouth, blink, brow, look, expr, sweat, back, k)
    hs = s / k
    hc = (neck[0] + (_NL["head"] + 6) * u * math.sin(lr), neck[1] - (_NL["head"] + 6) * u * math.cos(lr))
    comp(g, hel, hc[0], hc[1], scale=hs if abs(hs - 1) > 0.02 else 1.0)
    if op < 0.999: f[:] = f * (1 - op) + g * op
    return hands


def _nbn_head_dict(who, mouth, blink, brow, look, expr, sweat, back, k):
    # dict looks ({"base": "exec", "tie": ...}) are cached by their repr; _slook() resolves the dict
    key = repr(sorted((kk, str(vv)) for kk, vv in who.items()))
    _NBN_DICTS[key] = who
    return _nbn_head_el(_DictWho(key), mouth, blink, brow, look[0], look[1], expr, sweat, back, k)


_NBN_DICTS = {}


class _DictWho(str):
    pass


def _limb2(g, rimg, a, b, c, ink, lw, rim, rw):
    """black stick limb with a soft light rim (45 %) so it reads on dark floors; works on the limb's bounding box only"""
    I = lambda v: int(round(v)); pts = [p for p in (a, b, c) if p is not None]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; m_ = rw + 4
    x0, x1 = max(0, I(min(xs) - m_)), min(W, I(max(xs) + m_)); y0, y1 = max(0, I(min(ys) - m_)), min(H, I(max(ys) + m_))
    if x1 <= x0 or y1 <= y0: return
    sub = g[y0:y1, x0:x1]; msk = np.zeros(sub.shape[:2], np.float32)
    for p, q in zip(pts, pts[1:]):
        cv2.line(msk, (I(p[0] - x0), I(p[1] - y0)), (I(q[0] - x0), I(q[1] - y0)), 1.0, rw, cv2.LINE_AA)
    m3 = (msk * 0.45)[..., None]; sub[:] = sub * (1 - m3) + np.array(rim, np.float32) * m3
    for p, q in zip(pts, pts[1:]):
        cv2.line(g, (I(p[0]), I(p[1])), (I(q[0]), I(q[1])), ink, lw, cv2.LINE_AA)


def _shadow(g, x, y, r):
    I = lambda v: int(round(v))
    ov = g.copy(); cv2.ellipse(ov, (I(x), I(y)), (I(r), I(r * 0.18)), 0, 0, 360, (0, 0, 0), -1, cv2.LINE_AA)
    g[:] = g * 0.82 + ov * 0.18


# ---------------------------------------------------------------- two-tier type + brand pill
def _tt_el(text, fnp, size, col, shadow=True):
    fn = font(fnp, size); tw = int(fn.getlength(text)) + 40; hh = int(size * 1.45)
    im = Image.new("RGBA", (tw + 30, hh), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((im.size[0] // 2 + 4, hh // 2 + 7), text, font=fn, fill=(0, 0, 0, 80), anchor="mm")
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(5)))
    ImageDraw.Draw(im).text((im.size[0] // 2, hh // 2), text, font=fn, fill=tuple(col) + (255,), anchor="mm")
    return el_from(im)


def _fits(text, size, max_w): return font(F_ANTON, size).getlength(text) <= max_w


def _split_two_tier(text, max_w):
    if _fits(text, 200, max_w): return None, text, 200
    if _fits(text, 160, max_w): return None, text, 160
    toks = text.split()
    # biggest-first: a number/money token group goes big when it fits
    for i, tk in enumerate(toks):
        if any(ch.isdigit() for ch in tk) or tk.startswith("$"):
            big = " ".join(toks[i:])
            if i > 0 and _fits(big, 170, max_w): return " ".join(toks[:i]), big, 200 if _fits(big, 200, max_w) else 170
    for i in range(1, len(toks)):
        big = " ".join(toks[i:])
        if _fits(big, 170, max_w): return " ".join(toks[:i]), big, 200 if _fits(big, 200, max_w) else 170
    return None, text, 200


def _sentence(s):
    s = s.lower(); return s[:1].upper() + s[1:]


def nbn_say(f, text, y=1240, size=150, col=(255, 255, 255), t=None, t0=None, max_w=800, keep=False, small=None):
    """NBN two-tier caption: small Montserrat line + one big clean Anton word; big word's centre at y=620 unless keep=True"""
    mw = min(max_w, 860)
    if small is None:
        small, big, bs = _split_two_tier(text, mw)
    else:
        big, bs = text, 200
    if not _fits(big, bs, mw):
        bs = max(90, int(bs * mw / font(F_ANTON, bs).getlength(big)))
    yc = y if keep else 590
    k1 = k2 = 1.0
    if t is not None and t0 is not None:
        if t < t0: return
        k1 = eo(clamp((t - t0) / 0.35)); k2 = eo(clamp((t - t0 - 0.12) / 0.45))
        if k2 <= 0 and not small: return
    elb = gcache(("ttbig", big, bs, tuple(col)), lambda: _tt_el(big, F_ANTON, bs, col))
    if small:
        els = gcache(("ttsm", small, tuple(col)), lambda: _tt_el(_sentence(small), F_MS6, 52, tuple(int(v * 0.92 + 20) if v < 235 else v for v in col), shadow=False))
        ys = yc - bs * 0.62 - 34 + (1 - k1) * 40
        comp(f, els, 540, ys, op=k1)
    if k2 > 0:
        comp(f, elb, 540, yc + (1 - k2) * bs * 0.5, op=min(1.0, k2 * 1.6))


def _nbn_pill_el(text):
    fn = font(F_MS8, 27); tw = int(fn.getlength(text)); w, h = tw + 74, 50; sc = 2
    im = Image.new("RGBA", (w * sc, h * sc), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w * sc - 1, h * sc - 1], h * sc // 2, fill=(14, 14, 20, 200), outline=(255, 255, 255, 60), width=2 * sc)
    d.ellipse([20 * sc, (h // 2 - 6) * sc, 32 * sc, (h // 2 + 6) * sc], fill=(236, 40, 52, 255))
    d.text((44 * sc, h * sc // 2), text, font=font(F_MS8, 27 * sc), fill=(255, 255, 255, 255), anchor="lm")
    return el_from(im.resize((w, h), Image.LANCZOS))


def nbn_series(f, series="YOUR MOVE", title=None, x=None, y=None):
    """one centred brand pill: ● OOPSMYBUSINESS · SERIES (title goes as a quiet line under it)"""
    _SERIES_TXT[0] = f"OOPSMYBUSINESS · {series}".upper()
    if title and not _LINE[0]: _LINE[1] = (str(title).upper(), (236, 238, 246))


def nbn_clock(f, top="DAY 1", mid="6:14 AM", sub=None, x=72, y=272, op=1.0):
    """story clock = one quiet line under the brand pill (NBN: 'Beatriz Flamini, Granada')"""
    _LINE[0] = (" · ".join(str(v) for v in (top, mid, sub) if v).upper(), (255, 214, 90))


# ---------------------------------------------------------------- atmosphere
_DUST = np.random.default_rng(7).random((22, 4))


def _dust(f, n):
    t = n / 30.0
    for i, (a, b, c, d) in enumerate(_DUST):
        x = (a * W + 30 * math.sin(t * 0.3 + i)) % W; y = (b * H * 0.9 - t * (10 + 18 * c)) % (H * 0.9) + 120
        r = 5 + 20 * d; al = 0.05 + 0.07 * c
        x0, y0, x1, y1 = int(max(0, x - r * 2)), int(max(0, y - r * 2)), int(min(W, x + r * 2)), int(min(H, y + r * 2))
        if x1 <= x0 or y1 <= y0: continue
        yy, xx = np.mgrid[y0:y1, x0:x1]
        m = np.exp(-(((xx - x) ** 2 + (yy - y) ** 2) / (r * r)))[..., None] * al
        f[y0:y1, x0:x1] = f[y0:y1, x0:x1] * (1 - m) + m


if NBN:
    person = nbn_person          # noqa: F811
    guy = lambda f, x, y, s=1.0, **kw: nbn_person(f, x, y, s, "hero", **kw)   # noqa: E731,F811
    head_el = lambda mouth=0, blink=False, brow="n", lx=0, ly=0, expr="n": _nbn_head_el("hero", mouth, blink, brow, lx, ly, expr, False, False, 1.0)   # noqa: E731,F811

    def person_head_at(f, cx, cy, s, who="hero", **kw):   # noqa: F811
        return nbn_person(f, cx, cy + (_NL["leg"] + _NL["torso"] + _NL["head"] + 6) * 1.5 * s, s, who, **kw)

    if "_slook" in globals():
        _slook_prev = _slook

        def _slook(who):   # noqa: F811
            if isinstance(who, _DictWho): who = _NBN_DICTS[str(who)]
            return _slook_prev(who)

    say = nbn_say                 # noqa: F811
    series_badge = nbn_series     # noqa: F811
    part_badge = lambda f, part="PART 1", title=None, x=None, y=None: nbn_series(f, part, title)   # noqa: E731,F811
    hud_clock = nbn_clock         # noqa: F811
    mini_card = lambda f, top, mid, x=72, y=262, op=1.0: nbn_clock(f, top, mid, op=op)   # noqa: E731,F811
    cold_open = lambda f, year, place, role=None, op=1.0: nbn_clock(f, year, place, role, op=op)   # noqa: E731,F811

    if "_clean_base" in globals():
        _clean_base_flat = _clean_base

        def _clean_base(name):   # noqa: F811 — deeper NBN sky: the top third sinks toward night
            b = _clean_base_flat(name).copy()
            k = np.clip(1 - _yy / (H * 0.55), 0, 1)[..., None] ** 1.3
            return np.clip(b * (1 - 0.42 * k) + np.array([0.03, 0.03, 0.10], np.float32) * 0.42 * k, 0, 1).astype(np.float32)

        def _set_base(name):   # noqa: F811
            return _clean_base(name)

    _stxt_el_comic = _stxt_el

    def _stxt_el(text, size, col=(255, 255, 255), fpath=None, stroke=0, scol=(10, 10, 14)):   # noqa: F811 — NBN: no comic outline, a soft drop shadow instead
        if not stroke: return _stxt_el_comic(text, size, col, fpath, 0, scol)
        fn = font(fpath or F_ANTON, size); tw = int(fn.getlength(text)) + 24; hh = int(size * 1.35) + 12
        im = Image.new("RGBA", (tw, hh), (0, 0, 0, 0))
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((tw // 2 + 3, hh // 2 + 5), text, font=fn, fill=(0, 0, 0, 110), anchor="mm")
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(4)))
        ImageDraw.Draw(im).text((tw // 2, hh // 2), text, font=fn, fill=tuple(col) + (255,), anchor="mm")
        return im

    _finish_clean = finish

    def finish(f, n, vig=0.14, grain=0.0):   # noqa: F811
        f = np.array(f, np.float32, copy=True); _dust(f, n)
        comp(f, gcache(("pill", _SERIES_TXT[0]), lambda: _nbn_pill_el(_SERIES_TXT[0])), 540, 292)
        ln = _LINE[0] or _LINE[1]; _LINE[0] = _LINE[1] = None
        if ln: comp(f, gcache(("nbnln", ln), lambda: _tt_el(ln[0], F_MS8, 30, ln[1], shadow=False)), 540, 354)
        return _finish_clean(f, n)
