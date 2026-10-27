# ================= cast: lit 2.5D characters (exec'd after anim_base.py / anim_cine.py) =================
# Owner, 27 Oct (reference: top cartoon story reels): "not about the face or dress — colours, looking more natural and 3D,
# change the style of clothes, more things".
# How it looks 3D: every body part is drawn into a small G-buffer (albedo + normal + AO). Normals come from a rounded height
# map built from the part's own distance field, so sleeves, legs, torso and head read as soft rounded volumes. One lighting
# pass then applies a key light, a coloured ambient (sky) light, a rim/back light, a little specular (hair, shoes) and
# contact occlusion where parts overlap; the figure casts a soft shadow on the floor. Lighting presets match the scene:
#   set_light("day" | "warm" | "dusk" | "night" | "cool")      (set_view() in anim_sets.py picks one per set)
#   person(f, x, y, s, who="hero", ...)  — same pose args as guy(); who = a LOOKS key or a dict of overrides {"base": key, ...}
#   person_head_at(f, cx, cy, s, who, ...) — same, placed by head centre (medium shots / close-ups)
#   guy(...) = person(who="hero")  (MASCOT3D=0 restores the old flat stick figure)
# Looks: hero (hoodie), friend (tee), creator (jacket), exec (suit), inventor (dress, bun), lady (long hair, dress),
#        oldman (cardigan, glasses), worker (overalls, cap), kid (hoodie), mystery (dark coat + hat, face in shadow)
import os as _os
MASCOT3D = _os.environ.get("MASCOT3D", "1") != "0"
OUT_ = (52, 34, 32)

LIGHTS = {   # dir = towards the light (x right, y down, z to camera); colours ~ mean 1; k = strength
    "day":   dict(dir=(-0.50, -0.62, 0.62), key=(1.00, 0.97, 0.90), keyk=0.80, amb=(0.88, 0.95, 1.12), ambk=0.46, rim=(1.0, 0.98, 0.92), rimk=0.30, shadow=0.34),
    "warm":  dict(dir=(-0.55, -0.55, 0.62), key=(1.06, 0.95, 0.80), keyk=0.82, amb=(0.98, 0.88, 1.02), ambk=0.44, rim=(1.0, 0.82, 0.58), rimk=0.42, shadow=0.38),
    "dusk":  dict(dir=(0.72, -0.34, 0.50), key=(1.12, 0.78, 0.56), keyk=0.78, amb=(0.80, 0.78, 1.10), ambk=0.50, rim=(1.0, 0.62, 0.32), rimk=1.00, shadow=0.42),
    "night": dict(dir=(-0.40, -0.50, 0.72), key=(0.80, 0.90, 1.12), keyk=0.66, amb=(0.66, 0.70, 1.00), ambk=0.48, rim=(0.55, 0.85, 1.00), rimk=0.85, shadow=0.45),
    "cool":  dict(dir=(-0.45, -0.60, 0.66), key=(0.97, 0.99, 1.04), keyk=0.80, amb=(0.86, 0.94, 1.14), ambk=0.47, rim=(0.85, 0.92, 1.00), rimk=0.36, shadow=0.32),
}
LIGHT = dict(LIGHTS["day"]); _LID = ["day"]


def set_light(name="day", **kw):
    global LIGHT
    LIGHT = dict(LIGHTS[name]); LIGHT.update(kw); _LID[0] = name + repr(sorted(kw.items()))


def _mtone(c, k):  # lighter (k>1) / darker (k<1) version of a colour
    return tuple(int(np.clip(v * k + (255 - v) * max(0, k - 1) * 0.35, 0, 255)) for v in c)


_PC = {}; _PCPX = [0]    # per-part geometry cache (mask, normals, outline, occlusion) — static parts are drawn once


class _Fig:
    """G-buffer for one figure (frame coords, clipped to the frame + margin) or a free-standing element (clip=False)"""

    def __init__(self, x0, y0, x1, y1, s=1.0, clip=True):
        if clip:
            M = 160; x0, y0, x1, y1 = max(x0, -M), max(y0, -M), min(x1, W + M), min(y1, H + M)
        self.x0, self.y0 = int(math.floor(x0)), int(math.floor(y0)); self.s = s
        self.w, self.h = max(1, int(math.ceil(x1)) - self.x0), max(1, int(math.ceil(y1)) - self.y0)
        z = lambda *sh: np.zeros((self.h, self.w) + sh, np.float32)
        self.alb = z(3); self.nrm = z(3); self.nrm[..., 2] = 1; self.a = z(); self.lit = z(); self.gl = z(); self.ao = np.ones((self.h, self.w), np.float32)

    def _bb(self, xs, ys, pad):
        b = (max(0, int(math.floor(min(xs) - pad)) - self.x0), max(0, int(math.floor(min(ys) - pad)) - self.y0),
             min(self.w, int(math.ceil(max(xs) + pad)) - self.x0), min(self.h, int(math.ceil(max(ys) + pad)) - self.y0))
        return b if b[2] > b[0] + 1 and b[3] > b[1] + 1 else None

    def _pad(self): return 8 + 20 * self.s

    def _o(self, b): return np.array([self.x0 + b[0], self.y0 + b[1]], np.float32)

    def poly(self, pts, col, r0=None, **kw):
        pts = np.asarray(pts, np.float32); b = self._bb(pts[:, 0], pts[:, 1], self._pad())
        if b is None: return
        q = np.round((pts - self._o(b)) * 4).astype(np.int32)

        def mk():
            m = np.zeros((b[3] - b[1], b[2] - b[0]), np.float32); cv2.fillPoly(m, [q], 1.0, cv2.LINE_AA, shift=2); return m
        self._put(mk, b, col, 30 * self.s if r0 is None else r0, key=("p", q.tobytes()), **kw)

    def capsule(self, p, q, th, col, r0=None, **kw):
        b = self._bb((p[0], q[0]), (p[1], q[1]), th / 2 + self._pad())
        if b is None: return
        o = self._o(b)
        P = tuple(int(v) for v in np.round((np.array(p, np.float32) - o) * 4)); Q = tuple(int(v) for v in np.round((np.array(q, np.float32) - o) * 4))

        def mk():
            m = np.zeros((b[3] - b[1], b[2] - b[0]), np.float32)
            cv2.line(m, P, Q, 1.0, max(1, int(round(th))), cv2.LINE_AA, shift=2)
            for c in (P, Q): cv2.circle(m, c, int(th * 2), 1.0, -1, cv2.LINE_AA, shift=2)
            return m
        self._put(mk, b, col, th / 2 if r0 is None else r0, key=("c", P, Q, round(th, 2)), **kw)

    def ellipse(self, c, ax, col, ang=0, r0=None, **kw):
        b = self._bb((c[0],), (c[1],), max(ax) + self._pad())
        if b is None: return
        o = self._o(b); C = tuple(int(v) for v in np.round((np.array(c, np.float32) - o) * 4)); A = (int(ax[0] * 4), int(ax[1] * 4))

        def mk():
            m = np.zeros((b[3] - b[1], b[2] - b[0]), np.float32); cv2.ellipse(m, C, A, ang, 0, 360, 1.0, -1, cv2.LINE_AA, shift=2); return m
        self._put(mk, b, col, min(ax) if r0 is None else r0, key=("e", C, A, round(ang, 1)), **kw)

    def rrect(self, x0, y0, x1, y1, rad, col, r0=None, **kw):
        b = self._bb((x0, x1), (y0, y1), self._pad())
        if b is None: return
        hh, ww = b[3] - b[1], b[2] - b[0]; o = self._o(b)

        def mk():
            im = Image.new("L", (ww * 2, hh * 2), 0)
            ImageDraw.Draw(im).rounded_rectangle([(x0 - o[0]) * 2, (y0 - o[1]) * 2, (x1 - o[0]) * 2, (y1 - o[1]) * 2], int(rad * 2), fill=255)
            return cv2.resize(np.asarray(im, np.float32) / 255, (ww, hh), interpolation=cv2.INTER_AREA)
        self._put(mk, b, col, rad if r0 is None else r0, **kw)

    def _put(self, mk, b, col, r0, gloss=0.0, ow=None, ao=0.30, oc=None, soft=0.12, key=None):
        bx0, by0, bx1, by1 = b; sub = (slice(by0, by1), slice(bx0, bx1))
        ow = max(1, int(round(2.2 * self.s))) if ow is None else int(ow)
        ck = None if key is None else (key, b, round(float(r0), 2), soft, ow, ao > 0, round(self.s, 3))
        hit = _PC.get(ck) if ck is not None else None
        if hit is not None:
            m, n, ol, sh = (None if v is None else v.astype(np.float32) for v in hit)
        else:
            m = mk() if callable(mk) else mk
            mb = (m > 0.5).astype(np.uint8)
            if mb.sum() < 3: return
            d = cv2.distanceTransform(mb, cv2.DIST_L2, 5)
            r = max(1.0, min(float(r0), float(d.max())))
            k = np.minimum(d / r, 1.0)
            ht = cv2.GaussianBlur(r * np.sqrt(np.clip(1 - (1 - k) ** 2, 0, 1)), (0, 0), max(0.9, soft * r)) * np.clip(m * 1.2, 0, 1)
            gx = cv2.Sobel(ht, cv2.CV_32F, 1, 0, ksize=3) / 8; gy = cv2.Sobel(ht, cv2.CV_32F, 0, 1, ksize=3) / 8
            n = np.dstack([-gx, -gy, np.ones_like(gx)]); n /= np.sqrt((n * n).sum(2, keepdims=True))
            ol = np.clip(cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * ow + 1, 2 * ow + 1))) - m, 0, 1) if ow > 0 else None
            sh = cv2.GaussianBlur(m, (0, 0), max(1.5, 7 * self.s)) * (1 - m) if ao > 0 else None
            if ck is not None:
                if _PCPX[0] > 9_000_000: _PC.clear(); _PCPX[0] = 0
                _PC[ck] = tuple(None if v is None else v.astype(np.float16) for v in (m, n, ol, sh)); _PCPX[0] += m.size * (6 if ol is None else 7)
        A = self.a[sub]
        if sh is not None and A.max() > 0:
            self.ao[sub] *= 1 - ao * sh * A
        c = np.array(col, np.float32) / 255
        if ol is not None:
            occ = np.array(oc, np.float32) / 255 if oc is not None else (c * 0.36 + np.array(OUT_, np.float32) / 255 * 0.64)
            self.alb[sub] = self.alb[sub] * (1 - ol[..., None]) + occ * ol[..., None]
            self.lit[sub] *= 1 - ol; self.a[sub] = np.maximum(self.a[sub], ol)
        m3 = m[..., None]
        self.alb[sub] = self.alb[sub] * (1 - m3) + c * m3
        self.nrm[sub] = self.nrm[sub] * (1 - m3) + n * m3
        self.lit[sub] = self.lit[sub] * (1 - m) + m
        self.gl[sub] = self.gl[sub] * (1 - m) + gloss * m
        self.ao[sub] = self.ao[sub] * (1 - m) + m
        self.a[sub] = np.maximum(self.a[sub], m)

    def line(self, p, q, th, col, op=0.55):   # decal stroke (seams, folds), drawn on top, keeps lighting
        o = np.array([self.x0, self.y0], np.float32)
        P = tuple(int(v) for v in np.round((np.array(p, np.float32) - o) * 4)); Q = tuple(int(v) for v in np.round((np.array(q, np.float32) - o) * 4))
        xs, ys = sorted((p[0], q[0])), sorted((p[1], q[1]))
        b = self._bb(xs, ys, th + 4)
        if b is None: return
        m = np.zeros((self.h, self.w), np.float32)
        cv2.line(m, P, Q, 1.0, max(1, int(round(th))), cv2.LINE_AA, shift=2)
        sub = (slice(b[1], b[3]), slice(b[0], b[2])); mm = (m[sub] * self.a[sub] * op)[..., None]
        self.alb[sub] = self.alb[sub] * (1 - mm) + np.array(col, np.float32) / 255 * mm

    def _crop(self):
        rows = np.flatnonzero(self.a.max(1) > 0.002); cols = np.flatnonzero(self.a.max(0) > 0.002)
        if len(rows) == 0: return None
        return slice(rows[0], rows[-1] + 1), slice(cols[0], cols[-1] + 1)

    def shade(self, cr=None):
        """lit RGB + alpha for the crop cr (default: the whole buffer)"""
        cr = cr or (slice(0, self.h), slice(0, self.w))
        alb, nr, aa, gl, ao1, lt = self.alb[cr], self.nrm[cr], self.a[cr], self.gl[cr], self.ao[cr], self.lit[cr]
        L = np.array(LIGHT["dir"], np.float32); L /= np.linalg.norm(L)
        n = nr / (np.sqrt(np.einsum("ijk,ijk->ij", nr, nr))[..., None] + 1e-6)
        ndl = n @ L; wrap = 0.5
        diff = np.clip((ndl + wrap) * (1 / (1 + wrap)), 0, 1)
        sky = 0.82 + 0.18 * np.clip(-n[..., 1] * 1.4 + 0.3, 0, 1)
        ao = ao1[..., None]
        light = (np.array(LIGHT["amb"], np.float32) * LIGHT["ambk"] * (sky[..., None] * ao)
                 + np.array(LIGHT["key"], np.float32) * LIGHT["keyk"] * (diff[..., None] * (0.5 + 0.5 * ao)))
        rgb = alb * light
        Hv = L + np.array([0, 0, 1], np.float32); Hv /= np.linalg.norm(Hv)
        sp = np.clip(n @ Hv, 0, 1); sp *= sp; sp *= sp; sp *= sp; sp *= sp; sp *= sp          # ^32
        sx, sy = LIGHT["dir"][0], LIGHT["dir"][1]; ln = math.hypot(sx, sy) or 1.0
        e = 1 - np.clip(n[..., 2], 0, 1)
        rim = e * e * np.clip((n[..., 0] * sx + n[..., 1] * sy) * (1 / ln), 0, 1) * LIGHT["rimk"]
        rgb += (sp * gl * 0.55)[..., None]
        rgb += rim[..., None] * (np.array(LIGHT["rim"], np.float32) * 0.75) * (0.4 + 0.6 * np.sqrt(alb.mean(2, keepdims=True)))
        lit = lt[..., None]
        return np.clip(alb + (rgb - alb) * lit, 0, 1), aa

    def comp(self, f, op=1.0, blur=0.0):
        cr = self._crop()
        if cr is None: return
        if blur > 0.3:   # grow the crop so the blur can spread
            g = int(3 * blur) + 2
            cr = (slice(max(0, cr[0].start - g), min(self.h, cr[0].stop + g)), slice(max(0, cr[1].start - g), min(self.w, cr[1].stop + g)))
        rgb, a = self.shade(cr)
        ox, oy = self.x0 + cr[1].start, self.y0 + cr[0].start; hh, ww = a.shape
        X0, Y0 = max(0, ox), max(0, oy); X1, Y1 = min(W, ox + ww), min(H, oy + hh)
        if X1 <= X0 or Y1 <= Y0: return
        pm = rgb * a[..., None]
        if blur > 0.3: pm = cv2.GaussianBlur(pm, (0, 0), blur); a = cv2.GaussianBlur(a, (0, 0), blur)
        ls = (slice(Y0 - oy, Y1 - oy), slice(X0 - ox, X1 - ox))
        aa = a[ls][..., None] * op
        f[Y0:Y1, X0:X1] = f[Y0:Y1, X0:X1] * (1 - aa) + pm[ls] * op

    def cast_shadow(self, f, foot_y, s, k=None):
        """soft shadow of the figure on the floor, thrown away from the key light"""
        k = LIGHT["shadow"] if k is None else k
        sq = 0.20; shx = -0.75 * LIGHT["dir"][0] / max(0.2, abs(LIGHT["dir"][2]))
        fy = foot_y - self.y0
        rx0, rx1 = self.x0 - int(420 * s), self.x0 + self.w + int(420 * s); ry0, ry1 = int(foot_y - 30 * s), int(foot_y + 220 * s)
        X0, Y0, X1, Y1 = max(0, rx0), max(0, ry0), min(W, rx1), min(H, ry1)
        if X1 <= X0 or Y1 <= Y0: return
        # src (x, y) in fig-local -> dst (x + shx*(fy-y) + x0 - X0, fy + sq*(fy-y) + y0 - Y0)
        Mx = np.float32([[1, -shx, shx * fy + self.x0 - X0], [0, -sq, fy + sq * fy + self.y0 - Y0]])
        sh = cv2.warpAffine(self.a, Mx, (X1 - X0, Y1 - Y0), flags=cv2.INTER_LINEAR)
        sh = cv2.GaussianBlur(sh, (0, 0), 3 + 5 * s)
        tint = np.array(LIGHT["amb"], np.float32); tint = 1 - (1 - tint / tint.max()) * 0.5
        f[Y0:Y1, X0:X1] *= (1 - k * sh[..., None] * (1 - 0.25 * tint))


# ---------------- looks (natural palettes, not neon) ----------------
LOOKS = {
    "hero":     dict(skin=(246, 204, 168), hair="spiky", hair_col=(70, 46, 34), outfit="hoodie", top=(214, 104, 54), trim=(246, 236, 218),
                     pants=(58, 76, 112), shoes=(242, 240, 234), accent=(214, 104, 54)),
    "friend":   dict(skin=(214, 160, 122), hair="curly", hair_col=(44, 32, 28), outfit="tee", top=(242, 196, 72), trim=(242, 196, 72),
                     pants=(72, 98, 140), shoes=(236, 82, 70)),
    "creator":  dict(skin=(240, 196, 160), hair="slick", hair_col=(92, 60, 40), outfit="jacket", top=(98, 112, 72), inner=(246, 244, 238), trim=(80, 90, 58),
                     pants=(48, 50, 60), shoes=(250, 250, 248), accent=(98, 112, 72)),
    "exec":     dict(skin=(236, 192, 152), hair="slick", hair_col=(42, 36, 34), outfit="suit", top=(40, 52, 82), trim=(246, 246, 248),
                     tie=(182, 38, 44), pants=(40, 52, 82), shoes=(46, 32, 26)),
    "inventor": dict(skin=(248, 208, 174), hair="bun", hair_col=(104, 62, 40), outfit="dress", top=(52, 104, 104), trim=(242, 234, 216),
                     pants=(52, 104, 104), shoes=(56, 38, 30), lashes=True),
    "lady":     dict(skin=(232, 184, 146), hair="long", hair_col=(58, 36, 28), outfit="dress", top=(168, 52, 70), trim=(246, 230, 220),
                     pants=(168, 52, 70), shoes=(60, 34, 34), lashes=True),
    "oldman":   dict(skin=(240, 198, 162), hair="white", hair_col=(228, 228, 224), outfit="cardigan", top=(140, 100, 66), trim=(238, 232, 218),
                     tie=(156, 44, 50), pants=(180, 162, 128), shoes=(76, 50, 36), glasses=True, mustache=True),
    "worker":   dict(skin=(214, 162, 122), hair="cap", hair_col=(40, 30, 26), cap=(200, 66, 50), outfit="overalls", top=(184, 76, 64), trim=(70, 106, 156),
                     pants=(70, 106, 156), shoes=(86, 58, 40)),
    "kid":      dict(skin=(250, 216, 182), hair="spiky", hair_col=(184, 114, 54), outfit="hoodie", top=(76, 156, 116), trim=(242, 242, 232),
                     pants=(76, 86, 116), shoes=(238, 238, 232), accent=(76, 156, 116)),
    "mystery":  dict(skin=(150, 120, 110), hair="hat", hair_col=(30, 26, 28), outfit="coat", top=(40, 36, 42), trim=(70, 62, 58),
                     pants=(34, 32, 36), shoes=(26, 22, 22), shadow_face=True),
}


def _look(who):
    if isinstance(who, dict):
        L = dict(LOOKS[who.get("base", "hero")]); L.update({k: v for k, v in who.items() if k != "base"}); return L
    return LOOKS[who]


def _lkey(who): return who if isinstance(who, str) else repr(sorted(who.items()))


# ---------------- heads: lit volumes + drawn features, rendered at the shown size (sharp in close-ups) ----------------
_HC = {}; _HCPX = [0]


def head2_el(who="hero", mouth=0, blink=False, brow="n", lx=0, ly=0, expr="n", sweat=False, back=False, k=1.0):
    k = max(0.2, round(k * 20) / 20)
    key = (_lkey(who), mouth, blink, brow, lx, ly, expr, sweat, back, k, _LID[0])
    if key in _HC: return _HC[key]
    L = _look(who); sk = L["skin"]; hc = L["hair_col"]; hs = L["hair"]
    w, h = int(250 * k), int(270 * k)
    U = lambda *v: [x * k for x in v]
    fg = _Fig(0, 0, w, h, s=k, clip=False)
    Pp = lambda pts: [(x * k, y * k) for x, y in pts]
    hgl = 0.38 if sum(hc) < 500 else 0.2
    if back:
        for ex in (30, 220): fg.ellipse(U(ex, 160), U(15, 19), sk, gloss=0.05)
        fg.rrect(*U(40, 56, 210, 240), 66 * k, hc, gloss=hgl, r0=400 * k, soft=0.24)
        if hs not in ("cap", "hat", "white"):
            for ang in (-50, -25, 0, 25, 50, 75, -75):
                ca, sa = math.cos(math.radians(ang + 90)), math.sin(math.radians(ang + 90))
                fg.line(U(125 + ca * 18, 96 + sa * 10), U(125 + ca * 80, 96 + sa * 120), 4 * k, _mtone(hc, 0.55), op=0.45)
            fg.ellipse(U(125, 96), U(9, 7), _mtone(hc, 0.7), ow=0, ao=0, r0=3 * k)
        if hs == "white": fg.rrect(*U(40, 56, 210, 240), 66 * k, sk, gloss=0.1, r0=400 * k, soft=0.24); fg.rrect(*U(40, 150, 210, 236), 50 * k, hc, r0=30 * k)
        if hs == "bun": fg.ellipse(U(125, 40), U(34, 30), hc, gloss=hgl)
        if hs == "long": fg.rrect(*U(26, 70, 224, 268), 50 * k, hc, gloss=hgl, r0=30 * k)
        if hs == "cap": fg.poly(Pp([(28, 106), (40, 48), (125, 26), (210, 48), (222, 106)]), L["cap"], r0=30 * k)
        if hs == "hat":
            fg.ellipse(U(125, 104), U(136, 22), hc, r0=10 * k); fg.rrect(*U(52, 12, 198, 102), 30 * k, hc, r0=30 * k)
    else:
        if hs == "long": fg.rrect(*U(22, 60, 228, 268), 56 * k, _mtone(hc, 0.85), gloss=hgl, r0=34 * k)
        if hs == "bun": fg.ellipse(U(125, 36), U(34, 30), hc, gloss=hgl)
        for ex in (30, 220):
            fg.ellipse(U(ex, 160), U(15, 19), sk, gloss=0.05)
        fg.rrect(*U(36, 62, 214, 240), 62 * k, sk, gloss=0.07, r0=400 * k, soft=0.24)
        if hs == "spiky":
            fg.poly(Pp([(38, 128), (36, 92), (52, 64), (70, 40), (84, 52), (98, 22), (116, 44), (132, 14), (146, 42), (168, 30), (176, 56), (200, 52),
                        (212, 90), (212, 128), (196, 100), (172, 92), (150, 104), (126, 90), (100, 104), (76, 92), (56, 112)]), hc, gloss=hgl, r0=22 * k, soft=0.2)
        elif hs == "slick":
            fg.poly(Pp([(36, 128), (38, 86), (60, 58), (100, 44), (150, 44), (190, 58), (212, 88), (214, 124), (200, 96), (150, 84), (120, 88), (70, 90), (50, 108)]),
                    hc, gloss=hgl, r0=22 * k, soft=0.2)
        elif hs in ("bun", "long"):
            fg.poly(Pp([(34, 166), (34, 96), (56, 62), (100, 46), (150, 46), (194, 62), (216, 96), (216, 166), (204, 114), (170, 88), (125, 84), (80, 88), (46, 114)]),
                    hc, gloss=hgl, r0=22 * k, soft=0.2)
        elif hs == "curly":
            for cx, cy, rr in ((60, 92, 30), (92, 66, 32), (128, 56, 34), (164, 66, 32), (194, 92, 30), (46, 124, 20), (206, 124, 20), (110, 86, 22), (150, 86, 22)):
                fg.ellipse(U(cx, cy), U(rr, rr), hc, gloss=hgl * 0.7, ow=max(1, int(1.6 * k)))
        elif hs == "white":
            for side in (-1, 1): fg.ellipse(U(125 + side * 92, 120), U(30, 30), hc, gloss=0.15)
        elif hs == "cap":
            fg.poly(Pp([(30, 108), (40, 52), (125, 28), (210, 52), (220, 108)]), L["cap"], r0=30 * k, gloss=0.1)
            fg.rrect(*U(20, 94, 236, 114), 10 * k, _mtone(L["cap"], 0.75), r0=6 * k)
        elif hs == "hat":
            fg.ellipse(U(125, 104), U(136, 22), hc, r0=10 * k, gloss=0.1); fg.rrect(*U(52, 12, 198, 102), 30 * k, hc, r0=30 * k, gloss=0.1)
            fg.rrect(*U(54, 74, 196, 92), 4 * k, (100, 26, 30), r0=4 * k, ao=0)
    rgb, a = fg.shade()
    if L.get("shadow_face") and not back: rgb = rgb * 0.45
    im = Image.fromarray((np.dstack([rgb, a]) * 255).astype(np.uint8), "RGBA")
    if not back:
        SS = 3; sc = k * SS; S = lambda *v: [x * sc for x in v]; lw = lambda v: max(1, int(v * sc))
        ov = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
        sh = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
        if hs in ("spiky", "slick", "bun", "long", "curly"): ds.chord(S(44, 76, 206, 146), 0, 180, fill=_mtone(sk, 0.70) + (80,))
        if not L.get("shadow_face"):
            for cx in (74, 176): ds.ellipse(S(cx - 22, 186, cx + 22, 206), fill=(240, 120, 112, 90))
            ds.ellipse(S(112, 178, 138, 196), fill=_mtone(sk, 0.75) + (70,))                       # soft nose shadow
        ov = Image.alpha_composite(ov, sh.filter(ImageFilter.GaussianBlur(5 * sc)))
        d = ImageDraw.Draw(ov)
        dark = (40, 26, 22); ox, oy = lx * 8, ly * 5
        if not L.get("shadow_face"): d.arc(S(116, 174, 134, 188), 200, 340, fill=_mtone(sk, 0.58) + (255,), width=lw(3))
        for i, cx in enumerate((92, 158)):
            x = cx + ox; y = 160 + oy
            if L.get("shadow_face"):
                d.ellipse(S(x - 10, y - 5, x + 10, y + 5), fill=(255, 196, 70, 255)); continue
            if blink:
                d.arc(S(x - 13, y - 8, x + 13, y + 8), 20, 160, fill=dark + (255,), width=lw(4)); continue
            rx, ry = (11, 15) if expr == "wow" else (9.5, 12.5)
            if expr == "sus": ry = 6
            d.ellipse(S(x - rx, y - ry, x + rx, y + ry), fill=dark + (255,))
            if ry > 7:
                d.ellipse(S(x - rx * 0.72, y + ry * 0.0, x + rx * 0.72, y + ry * 0.92), fill=(118, 76, 52, 255))   # warm iris glow
                d.ellipse(S(x - rx * 0.45, y + ry * 0.12, x + rx * 0.45, y + ry * 0.7), fill=dark + (255,))
            d.ellipse(S(x - rx * 0.62, y - ry * 0.78, x - rx * 0.02, y - ry * 0.2), fill=(255, 255, 255, 255))
            d.ellipse(S(x + rx * 0.2, y + ry * 0.3, x + rx * 0.5, y + ry * 0.6), fill=(255, 255, 255, 200))
            if L.get("lashes"):
                d.line(S(x + (rx if i else -rx), y - ry * 0.55, x + (rx + 6 if i else -rx - 6), y - ry - 3), fill=dark + (255,), width=lw(3))
            if L.get("glasses"):
                d.ellipse(S(cx - 24, 160 - 22, cx + 24, 160 + 22), outline=(64, 52, 46, 255), width=lw(4))
                d.arc(S(cx - 18, 160 - 16, cx + 18, 160 + 16), 200, 250, fill=(255, 255, 255, 170), width=lw(3))
        if L.get("glasses"): d.line(S(116, 156, 134, 156), fill=(64, 52, 46, 255), width=lw(4))
        bc = _mtone(hc, 0.85) if sum(hc) < 500 else (150, 140, 130)
        if not L.get("shadow_face"):
            for i, cx in enumerate((92, 158)):
                if brow == "up": a_, b_ = ((cx - 18, 132), (cx + 16, 126)) if i == 0 else ((cx - 16, 126), (cx + 18, 132))
                elif brow in ("sus", "mad"): a_, b_ = ((cx - 18, 128), (cx + 16, 138)) if i == 0 else ((cx - 16, 138), (cx + 18, 128))
                elif brow == "sad": a_, b_ = ((cx - 18, 138), (cx + 16, 128)) if i == 0 else ((cx - 16, 128), (cx + 18, 138))
                else: a_, b_ = ((cx - 18, 136), (cx + 16, 132)) if i == 0 else ((cx - 16, 132), (cx + 18, 136))
                d.line(S(*a_, *b_), fill=bc + (255,), width=lw(8))
                for pt in (a_, b_): d.ellipse(S(pt[0] - 4, pt[1] - 4, pt[0] + 4, pt[1] + 4), fill=bc + (255,))
        if L.get("mustache"):
            d.chord(S(98, 194, 152, 222), 180, 360, fill=hc + (255,), outline=_mtone(hc, 0.6) + (255,), width=lw(2))
        mx, my = 125, 214
        if expr == "wow" and mouth == 0: mouth = "o"
        if L.get("shadow_face"): mouth = -1
        if mouth == 0:
            if expr == "sad": d.arc(S(mx - 16, my - 2, mx + 16, my + 14), 200, 340, fill=dark + (255,), width=lw(4))
            elif expr == "smirk": d.arc(S(mx - 18, my - 12, mx + 16, my + 6), 10, 120, fill=dark + (255,), width=lw(4))
            elif expr in ("sus", "mad"): d.line(S(mx - 12, my + 2, mx + 12, my), fill=dark + (255,), width=lw(4))
            else: d.arc(S(mx - 16, my - 12, mx + 16, my + 8), 25, 155, fill=dark + (255,), width=lw(4))
        elif mouth == "o":
            d.ellipse(S(mx - 8, my - 6, mx + 8, my + 12), fill=(96, 36, 38, 255), outline=dark + (255,), width=lw(2))
        elif mouth in (1, 2, 3):
            hh = {1: 7, 2: 12, 3: 17}[mouth]; ww = {1: 13, 2: 16, 3: 19}[mouth]
            d.rounded_rectangle(S(mx - ww, my - 6, mx + ww, my - 6 + hh * 1.5), int(hh * 0.8 * sc), fill=(100, 36, 38, 255), outline=dark + (255,), width=lw(2))
            if mouth >= 2: d.ellipse(S(mx - ww * 0.5, my - 6 + hh * 0.85, mx + ww * 0.5, my - 6 + hh * 1.5), fill=(228, 112, 112, 255))
            d.rectangle(S(mx - ww + 5, my - 4, mx + ww - 5, my), fill=(255, 255, 255, 255))
        if sweat:
            d.polygon(S(206, 92, 196, 116, 216, 116), fill=(126, 196, 244, 255))
            d.ellipse(S(194, 106, 218, 130), fill=(126, 196, 244, 255), outline=(60, 110, 160, 255), width=lw(2))
            d.ellipse(S(200, 111, 206, 119), fill=(240, 250, 255, 255))
        ov = ov.resize((w, h), Image.LANCZOS)
        a0 = im.getchannel("A"); im = Image.alpha_composite(im, ov); im.putalpha(a0)
    el = el_from(im)
    if _HCPX[0] > 14_000_000: _HC.clear(); _HCPX[0] = 0
    _HC[key] = el; _HCPX[0] += w * h
    return el


def head3d_el(mouth=0, blink=False, brow="n", lx=0, ly=0, expr="n"):   # old API (props)
    return head2_el("hero", mouth, blink, brow, lx, ly, expr, k=1.0)


# ---------------- the figure ----------------
def _hands(fg, hands, s, skin):
    for side, (hx, hy) in hands.items():
        fg.ellipse((hx, hy + 4 * s), (21 * s, 21 * s), skin, gloss=0.06, r0=16 * s)
        fg.ellipse((hx + side * 18 * s, hy - 5 * s), (8 * s, 12 * s), skin, ang=side * 30, gloss=0.05, ow=max(1, int(1.8 * s)), ao=0.2)


def person(f, x, y, s=1.0, who="hero", la=(18, 8), ra=(18, 8), ll=7, rl=7, lean=0.0, sit=False, mouth=0, blink=False, brow="n", look=(0, 0),
           expr="n", bob=0.0, hold=None, hold_off=(0, 0), face_dir=1, op=1.0, shadow=True, sweat=False, back=False):
    """lit 2.5D character. (x, y) = feet baseline (or seat point when sit=True). Returns {side: hand point}.
    back=True: seen from behind (over-the-shoulder shots)."""
    L = _look(who); lr = math.radians(lean)
    pants, shoes, top = L["pants"], L["shoes"], L["top"]; o = L["outfit"]
    fg = _Fig(x - 300 * s, y - 640 * s, x + 300 * s, y + 200 * s, s)
    dress = o == "dress"; thin = max(1, int(1.6 * s))
    if not sit:
        hip = (x, y - 178 * s)
        for side, ang in ((-1, ll), (1, rl)):
            hp = (hip[0] + side * 26 * s, hip[1] - 6 * s)
            ft = (hp[0] + side * math.sin(math.radians(ang)) * 158 * s, hp[1] + math.cos(math.radians(ang)) * 158 * s)
            if dress: fg.capsule((hp[0], hp[1] + 60 * s), ft, 30 * s, L["skin"])
            else: fg.capsule(hp, ft, 42 * s, pants, gloss=0.02)
            sx = ft[0] + side * 8 * s
            fg.poly([(sx - 32 * s, ft[1] - 2 * s), (sx + 32 * s, ft[1] - 2 * s), (sx + 38 * s, ft[1] + 14 * s), (sx - 36 * s, ft[1] + 14 * s)],
                    _mtone(shoes, 0.9) if sum(shoes) < 600 else (226, 222, 214), r0=5 * s, gloss=0.2)
            fg.poly([(sx - 30 * s, ft[1] - 24 * s), (sx + 6 * s, ft[1] - 26 * s), (sx + 34 * s, ft[1] - 4 * s), (sx - 32 * s, ft[1] - 2 * s)], shoes,
                    r0=14 * s, gloss=0.35)
            if L.get("accent") and sum(shoes) > 600:
                fg.line((sx - 14 * s, ft[1] - 10 * s), (sx + 18 * s, ft[1] - 13 * s), 6 * s, L["accent"], op=0.9)
    else:
        hip = (x, y)
        for side in (-1, 1):
            hp = (hip[0] + side * 26 * s, hip[1]); kn = (hip[0] + side * 48 * s, hip[1] + 30 * s); ft = (hip[0] + side * 50 * s, hip[1] + 136 * s)
            fg.capsule(hp, kn, 42 * s, pants); fg.capsule(kn, ft, 38 * s, pants)
            fg.poly([(ft[0] - 30 * s, ft[1] - 16 * s), (ft[0] + 32 * s, ft[1] - 16 * s), (ft[0] + 36 * s, ft[1] + 12 * s), (ft[0] - 32 * s, ft[1] + 12 * s)],
                    shoes, r0=12 * s, gloss=0.3)
    neck = (hip[0] + 168 * s * math.sin(lr), hip[1] - 168 * s * math.cos(lr))
    ux, uy = math.sin(lr), -math.cos(lr); px_, py_ = -uy, ux
    P = lambda a, b: (hip[0] + ux * a * s + px_ * b * s, hip[1] + uy * a * s + py_ * b * s)
    sh_ = (neck[0] - ux * 22 * s, neck[1] - uy * 22 * s)
    arms = []; hands = {}
    for side, (a1, a2) in ((-1, la), (1, ra)):
        sp = (sh_[0] + side * 66 * s, sh_[1] + 8 * s)
        e = (sp[0] + side * math.sin(math.radians(a1)) * 84 * s, sp[1] + math.cos(math.radians(a1)) * 84 * s)
        hd = (e[0] + side * math.sin(math.radians(a2)) * 76 * s, e[1] + math.cos(math.radians(a2)) * 76 * s)
        arms.append((side, sp, e, hd)); hands[side] = hd
    # ---- torso by outfit ----
    if dress:
        fg.poly([P(186, -80), P(194, 0), P(186, 80), P(70, 64), P(-150, 128), P(-162, 0), P(-150, -128), P(70, -64)], top, r0=40 * s)
        fg.poly([P(84, -62), P(84, 62), P(64, 64), P(64, -64)], _mtone(top, 0.72), r0=8 * s, ow=thin)
        if not back: fg.poly([P(188, -26), P(188, 26), P(150, 0)], L["trim"], r0=6 * s, ow=thin)
        for b in (-60, 0, 60): fg.line(P(40, b * 0.6), P(-150, b * 1.4), 3 * s, _mtone(top, 0.55))
    elif o == "coat":
        fg.poly([P(190, -84), P(198, 0), P(190, 84), P(-100, 98), P(-108, 0), P(-100, -98)], top, r0=40 * s)
        if not back:
            fg.poly([P(190, -30), P(190, 30), P(110, 0)], (120, 30, 34), r0=6 * s, ow=thin)
            for side in (-1, 1): fg.poly([P(194, side * 30), P(194, side * 70), P(80, side * 10), P(96, side * 2)], _mtone(top, 1.25), r0=8 * s, ow=thin)
            for a_ in (40, -10, -60): fg.ellipse(P(a_, 14), (6 * s, 6 * s), (196, 168, 96), gloss=0.5, ow=1)
    else:
        body_col = L.get("inner", top) if o == "jacket" else top
        fg.poly([P(190, -82), P(198, 0), P(190, 82), P(34, 78), P(-12, 74), P(-24, 0), P(-12, -74), P(34, -78)], body_col, r0=42 * s)
        if o == "hoodie":
            hood = _mtone(top, 0.86)
            if back:
                fg.poly([P(214, -70), P(222, 0), P(214, 70), P(120, 52), P(96, 0), P(120, -52)], hood, r0=26 * s)
                fg.line(P(206, 0), P(120, 0), 3 * s, _mtone(top, 0.6))
            else:
                fg.poly([P(214, -74), P(228, 0), P(214, 74), P(178, 60), P(190, 0), P(178, -60)], hood, r0=16 * s)
                fg.poly([P(14, -76), P(14, 76), P(-22, 72), P(-22, -72)], hood, r0=10 * s, ow=thin)        # ribbed hem
                fg.poly([P(96, -54), P(96, 54), P(24, 64), P(24, -64)], _mtone(top, 0.94), r0=12 * s, ow=thin)  # pocket
                for b in (-16, 16):
                    fg.capsule(P(184, b * 0.8), P(116, b * 1.4), 6 * s, L["trim"], ow=1, ao=0.15)
                    fg.ellipse(P(112, b * 1.4), (5 * s, 7 * s), _mtone(L["trim"], 0.8), ow=1, ao=0)
        elif o in ("suit", "cardigan") and not back:
            fg.poly([P(188, -28), P(188, 28), P(108, 0)], L["trim"], r0=8 * s, ow=thin)
            if o == "suit":
                fg.poly([P(178, -10), P(178, 10), P(160, 8), P(82, 16), P(66, 0), P(82, -16), P(160, -8)], L["tie"], r0=8 * s, ow=thin, gloss=0.2)
                for side in (-1, 1): fg.poly([P(192, side * 28), P(192, side * 50), P(104, side * 6), P(116, side * 2)], _mtone(top, 1.18), r0=8 * s, ow=thin)
                fg.ellipse(P(40, 0), (6 * s, 6 * s), _mtone(top, 0.6), ow=1, ao=0)
            else:
                fg.poly([P(186, -16), P(186, 16), P(170, 0)], L["tie"], r0=5 * s, ow=1)
                for side in (-1, 1): fg.line(P(186, side * 26), P(0, side * 12), 4 * s, _mtone(top, 0.6))
                for yb in (130, 96, 62, 28): fg.ellipse(P(yb, 0), (5 * s, 5 * s), (232, 214, 176), gloss=0.4, ow=1, ao=0)
        elif o == "overalls":
            fg.poly([P(150, -50), P(150, 50), P(-20, 60), P(-20, -60)], L["trim"], r0=24 * s)
            for side in (-1, 1):
                fg.capsule(P(194, side * 54), P(150, side * 40), 14 * s, L["trim"], r0=5 * s)
                fg.ellipse(P(150, side * 40), (6 * s, 6 * s), (232, 204, 124), gloss=0.6, ow=1, ao=0)
            fg.poly([P(124, -26), P(124, 26), P(82, 26), P(82, -26)], _mtone(L["trim"], 0.9), r0=8 * s, ow=1)
        elif o == "jacket":
            for side in (-1, 1):
                fg.poly([P(194, side * 30), P(196, side * 84), P(-16, side * 78), P(-20, side * 36), P(60, side * 26)], top, r0=26 * s)
            if not back:
                for side in (-1, 1): fg.poly([P(200, side * 22), P(200, side * 58), P(150, side * 30)], L["trim"], r0=6 * s, ow=1)
            fg.poly([P(6, -80), P(6, 80), P(-22, 76), P(-22, -76)], L["trim"], r0=8 * s, ow=thin)
        elif o == "tee" and not back:
            fg.poly([P(190, -26), P(192, 0), P(190, 26), P(176, 0)], _mtone(top, 0.75), r0=4 * s, ow=1)
    # ---- arms ----
    sleeve = top
    for side, sp, e, hd in arms:
        if o == "tee":
            mid = (sp[0] + (e[0] - sp[0]) * 0.62, sp[1] + (e[1] - sp[1]) * 0.62)
            fg.capsule(mid, e, 30 * s, L["skin"], gloss=0.05); fg.capsule(e, hd, 28 * s, L["skin"], gloss=0.05)
            fg.capsule(sp, mid, 44 * s, sleeve)
        else:
            fg.capsule(sp, e, 39 * s, sleeve); fg.capsule(e, hd, 35 * s, sleeve)
            v = np.array(hd) - np.array(e); v = v / (np.hypot(*v) or 1)
            cf = (hd[0] - v[0] * 12 * s, hd[1] - v[1] * 12 * s)
            cuff = L["trim"] if o in ("suit", "cardigan", "dress", "jacket") else _mtone(sleeve, 0.85)
            fg.ellipse(cf, (18 * s, 18 * s), cuff, r0=8 * s, ow=thin)
    if shadow and not sit:
        fg.cast_shadow(f, y + 8 * s, s); contact(f, x, y + 8 * s, 230 * s, 0.38)
    if hold is None:
        _hands(fg, hands, s, L["skin"]); fg.comp(f, op)
    else:
        fg.comp(f, op)
        hx, hy = hands[1]; comp(f, hold, hx + hold_off[0] * s, hy + hold_off[1] * s, op=op)
        xs = [p[0] for p in hands.values()]; ys = [p[1] for p in hands.values()]
        fh = _Fig(min(xs) - 60 * s, min(ys) - 60 * s, max(xs) + 60 * s, max(ys) + 60 * s, s)
        _hands(fh, hands, s, L["skin"]); fh.comp(f, op)
    hel = head2_el(who, mouth, blink, brow, look[0], look[1], expr, sweat, back, s)
    hs_ = hel[1].shape[1] / 250.0
    comp(f, hel if abs(hs_ - s) < 0.02 else scale_el(hel, s / hs_), neck[0], neck[1] - 100 * s + bob * s, op=op)
    return hands


def person_head_at(f, cx, cy, s, who="hero", **kw):
    """place a (standing) character so its head centre lands on (cx, cy) — for medium shots and close-ups"""
    return person(f, cx, cy + 446 * s, s, who, **kw)


def guy3d(f, x, y, s=1.0, **kw):
    return person(f, x, y, s, "hero", **kw)


_guy_flat, _head_flat = guy, head_el
if MASCOT3D:
    guy = guy3d             # noqa: F811 — every existing shot gets the new hero
    head_el = head3d_el     # noqa: F811
