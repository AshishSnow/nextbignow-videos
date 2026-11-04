# ================= CLEAN look (exec'd last before anim_shots.py) — owner, 3 Nov 2026 =================
# "It's not clean like you are doing for NextBigNow." -> OopsMyBusiness gets the NextBigNow-style clean flat look:
#   * deep, saturated two-colour gradient backgrounds + one soft light spot, a flat floor band, ONE simple flat silhouette
#     layer per place (skyline / houses / trees / shelves / window / counter) — no bricks, no textures, no busy rooms
#   * no film grain, no chromatic aberration, no bloom haze, no warm cast (whites stay white); a light vignette only
#   * captions live in ONE place: the top band (say() -> y ~ 560, two-tier style), characters + props in the lower half
#   * lots of empty space: one idea per frame
# Every set name keeps working (set_view("street") etc. now returns the clean version). CLEAN=0 restores the old look.
import os as _os
CLEAN = _os.environ.get("CLEAN", "1") != "0"

# name -> (top colour, bottom colour, floor y, silhouette kind)
CLEAN_SETS = {
    "street":     ((52, 60, 150), (120, 70, 170), 1420, "houses"),
    "office":     ((10, 120, 140), (6, 70, 100), 1440, "window"),
    "store":      ((230, 90, 40), (170, 30, 60), 1440, "shelves"),
    "study":      ((80, 50, 150), (40, 24, 90), 1440, "frames"),
    "parlor":     ((150, 60, 110), (80, 30, 80), 1440, "frames"),
    "dusk":       ((70, 40, 130), (240, 110, 70), 1400, "trees"),
    "airport":    ((40, 120, 220), (20, 60, 150), 1440, "skyline"),
    "bedroom90s": ((60, 50, 140), (30, 24, 80), 1440, "frames"),
    "schoolyard": ((40, 140, 200), (20, 80, 150), 1420, "houses"),
    "courtroom":  ((120, 60, 40), (60, 26, 20), 1440, "counter"),
    "commissary": ((20, 130, 110), (8, 70, 70), 1440, "counter"),
    "mall":       ((200, 50, 120), (110, 20, 90), 1440, "shelves"),
    "optician":   ((20, 110, 170), (10, 50, 110), 1440, "shelves"),
    "wintry":     ((14, 22, 78), (38, 44, 130), 1400, "houses"),      # 3 Nov, EP 4: winter street, snow floor
    "garage":     ((96, 44, 170), (46, 20, 104), 1440, "counter"),
    "frostdusk":  ((58, 40, 140), (226, 88, 120), 1400, "trees"),
    "roofday":    ((24, 118, 214), (96, 190, 240), 1400, "trees"),
    "depot":      ((8, 120, 92), (6, 62, 62), 1440, "shelves"),
    "january":    ((66, 86, 128), (38, 50, 92), 1400, "houses"),
    "ladderday":  ((30, 134, 210), (120, 205, 235), 1400, "trees"),   # dry daytime: every ladder / roof shot (fresh-eyes review: never model frost or dusk)
    "recording":  ((120, 36, 150), (54, 18, 96), 1440, "frames"),     # 4 Nov, HOW IT WORKS EP 1: small home studio
    "gatehall":   ((10, 110, 140), (6, 50, 90), 1440, "skyline"),     # the four gates (one plain blue-teal hall)
    "subscriber": ((226, 76, 90), (130, 30, 90), 1440, "houses"),     # the viewer on the sofa side
    "carlot":     ((30, 110, 210), (240, 150, 80), 1420, "skyline"),  # 4 Nov, HOW IT WORKS EP 2: car lot at golden hour
    "lenderdesk": ((14, 120, 96), (6, 62, 62), 1440, "window"),       # the loan desk
    "homedesk":   ((70, 50, 150), (30, 24, 86), 1440, "frames"),      # your kitchen table with the card bill
}
_CLEAN_FLOOR = {"wintry": ((196, 212, 246), (130, 150, 218)), "frostdusk": ((236, 214, 232), (176, 140, 196)),
                "roofday": ((236, 244, 252), (176, 202, 236)), "january": ((176, 186, 206), (120, 130, 164)), "ladderday": ((104, 182, 100), (60, 134, 72))}
_CLEAN_PALETTES = [((30, 90, 200), (14, 40, 120)), ((120, 40, 170), (60, 20, 110)), ((10, 140, 130), (6, 70, 80)),
                   ((220, 80, 40), (150, 30, 50)), ((40, 150, 70), (14, 80, 50)), ((200, 50, 110), (100, 20, 80))]
_SIL_KINDS = ["skyline", "houses", "trees", "shelves", "window", "counter"]


def _clean_spec(name):
    if name in CLEAN_SETS: return CLEAN_SETS[name]
    h = sum(ord(ch) * (i + 1) for i, ch in enumerate(name))
    top, bot = _CLEAN_PALETTES[h % len(_CLEAN_PALETTES)]
    return (top, bot, 1440, _SIL_KINDS[(h // 7) % len(_SIL_KINDS)])


def _cmix(a, b, k): return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def _clean_base(name):
    top, bot, fy, kind = _clean_spec(name)
    f = np.zeros((H, W, 3), np.float32)
    k = np.clip(_yy / H, 0, 1)[..., None]
    f[:] = _c(top) * (1 - k) + _c(bot) * k
    spot = np.exp(-(((_xx - W / 2) / 620) ** 2 + ((_yy - H * 0.40) / 760) ** 2))[..., None]
    f[:] = f + spot * 0.16
    sil = _cmix(top, (0, 0, 0), 0.35); sil2 = _cmix(top, (0, 0, 0), 0.22)
    m = np.zeros((H, W), np.uint8)
    r = np.random.default_rng(sum(map(ord, name)) + 11)
    if kind in ("skyline", "window"):
        x = -20
        while x < W:
            bw = int(r.integers(70, 150)); bh = int(r.integers(160, 460))
            cv2.rectangle(m, (x, fy - bh), (x + bw, fy), 255, -1); x += bw + int(r.integers(6, 24))
        if kind == "window":
            f[m > 0] = _c(sil)
            for xx in (0, 360, 720, 1080): cv2.line(f, (xx, 260), (xx, fy), _scv(_cmix(top, (255, 255, 255), 0.18)), 18, cv2.LINE_AA)
            cv2.line(f, (0, 260), (W, 260), _scv(_cmix(top, (255, 255, 255), 0.18)), 18, cv2.LINE_AA)
            m[:] = 0
    elif kind == "houses":
        x = -40
        while x < W:
            bw = int(r.integers(160, 240)); bh = int(r.integers(150, 240))
            cv2.rectangle(m, (x, fy - bh), (x + bw, fy), 255, -1)
            cv2.fillPoly(m, [np.array([(x - 14, fy - bh), (x + bw // 2, fy - bh - int(bw * 0.42)), (x + bw + 14, fy - bh)], np.int32)], 255, cv2.LINE_AA)
            x += bw + int(r.integers(20, 50))
    elif kind == "trees":
        for layer, (base, col) in enumerate(((fy - 120, sil2), (fy - 20, sil))):
            mm = np.zeros((H, W), np.uint8); x = -40
            while x < W:
                tw = int(r.integers(60, 110)); th = int(r.integers(140, 280))
                cv2.fillPoly(mm, [np.array([(x, base), (x + tw // 2, base - th), (x + tw, base)], np.int32)], 255, cv2.LINE_AA); x += tw - 14
            cv2.rectangle(mm, (0, base - 2), (W, fy), 255, -1)
            f[mm > 0] = _c(col)
    elif kind == "shelves":
        for xx0, xx1 in ((-20, 400), (680, 1100)):
            cv2.rectangle(m, (xx0, fy - 760), (xx1, fy), 255, -1)
        f[m > 0] = _c(sil); m[:] = 0
        for xx0, xx1 in ((0, 380), (700, 1080)):
            for yy in range(fy - 700, fy, 170):
                cv2.line(f, (xx0, yy + 120), (xx1, yy + 120), _scv(_cmix(top, (255, 255, 255), 0.12)), 10, cv2.LINE_AA)
                for bx in range(xx0 + 20, xx1 - 40, 70):
                    cc = [(255, 200, 40), (255, 255, 255), (60, 220, 160), (255, 120, 90)][(bx // 70 + yy // 170) % 4]
                    cv2.rectangle(f, (bx, yy + 40), (bx + 44, yy + 116), _scv(_cmix(cc, sil, 0.35)), -1, cv2.LINE_AA)
    elif kind == "frames":
        for (x0, y0, x1, y1) in ((120, 520, 400, 820), (680, 470, 960, 900)):
            cv2.rectangle(f, (x0, y0), (x1, y1), _scv(sil), -1, cv2.LINE_AA)
            cv2.rectangle(f, (x0 + 22, y0 + 22), (x1 - 22, y1 - 22), _scv(_cmix(top, (255, 255, 255), 0.12)), -1, cv2.LINE_AA)
    elif kind == "counter":
        cv2.rectangle(f, (120, fy - 300), (960, fy), _scv(sil), -1, cv2.LINE_AA)
        cv2.rectangle(f, (100, fy - 330), (980, fy - 290), _scv(_cmix(top, (255, 255, 255), 0.15)), -1, cv2.LINE_AA)
    if m.any(): f[m > 0] = _c(sil)
    fc_top, fc_bot = _CLEAN_FLOOR.get(name, (_cmix(bot, (0, 0, 0), 0.18), _cmix(bot, (0, 0, 0), 0.42)))
    kk = np.clip((_yy[fy:] - fy) / (H - fy), 0, 1)[..., None]
    f[fy:] = _c(fc_top) * (1 - kk) + _c(fc_bot) * kk
    cv2.line(f, (0, fy), (W, fy), _scv(_cmix(bot, (255, 255, 255), 0.25)), 4, cv2.LINE_AA)
    return np.clip(f, 0, 1).astype(np.float32)


def clean_grade(f, n=0, **_kw):
    f = np.clip(f, 0, 1).astype(np.float32)
    lum = f @ LUMA
    f = lum[..., None] + (f - lum[..., None]) * 1.08
    f = f * (1 - 0.14 * np.clip(_rr - 0.35, 0, 1.2))[..., None]
    return np.clip(f, 0, 1)


_CLEAN_STAGE = {"orange": ((255, 140, 30), (220, 70, 20)), "pink": ((240, 80, 150), (170, 30, 100)), "sky": ((40, 150, 240), (20, 80, 180)),
                "yellow": ((255, 200, 40), (240, 140, 20)), "emerald": ((20, 160, 110), (8, 90, 70)), "purple": ((120, 60, 200), (60, 24, 130)),
                "cream": ((60, 70, 160), (30, 34, 100)), "red": ((230, 50, 60), (150, 20, 40)), "teal": ((10, 140, 150), (6, 80, 100))}


def _clean_stage_base(scheme):
    top, bot = _CLEAN_STAGE.get(scheme, _CLEAN_PALETTES[sum(map(ord, str(scheme))) % len(_CLEAN_PALETTES)])
    f = np.zeros((H, W, 3), np.float32); k = np.clip(_yy / H, 0, 1)[..., None]
    f[:] = _c(top) * (1 - k) + _c(bot) * k
    f[:] = f + np.exp(-(((_xx - W / 2) / 640) ** 2 + ((_yy - H * 0.45) / 760) ** 2))[..., None] * 0.14
    return np.clip(f, 0, 1).astype(np.float32)


if CLEAN:
    _set_base_detailed = _set_base

    def _set_base(name):   # noqa: F811 — set_view() calls this; clean flat places for every set name
        return _clean_base(name)

    def stage(scheme, sun=None, sx=540, sy=900, R=420, t=None, kind=None):   # noqa: F811
        if "set_light" in globals(): set_light("day")
        f = gcache(("cstage", scheme), lambda: _clean_stage_base(scheme)).copy()
        if sun is not None and R > 4:   # the old 'big colour disc' becomes one flat soft circle (NextBigNow style)
            cv2.circle(f, (int(sx), int(sy)), int(R), tuple(float(v) / 255 * 0.92 + 0.08 for v in sun), -1, cv2.LINE_AA)
        return f

    def finish(f, n, vig=0.14, grain=0.0):   # noqa: F811 — no grain, no haze
        return clean_grade(f, n)

    cine_grade = clean_grade   # noqa: F811

    _say_detailed = say

    def say(f, text, y=1240, size=150, col=(255, 255, 255), t=None, t0=None, max_w=800, keep=False):   # noqa: F811
        """captions live in the top band (y ~ 560) so they never sit on faces; keep=True keeps the given y"""
        _say_detailed(f, text, y if keep else 560, size, col, t, t0, max_w)

    def glow_disc(f, col, sx, sy, R, op=0.9):   # noqa: F811 — flat circle instead of a glow
        ov = f.copy(); cv2.circle(ov, (int(sx), int(sy)), int(R), tuple(float(v) / 255 for v in col), -1, cv2.LINE_AA)
        f[:] = f * (1 - 0.55 * op) + ov * 0.55 * op
