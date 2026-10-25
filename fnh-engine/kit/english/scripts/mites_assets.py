"""Procedural assets for the face-mites reel: realistic skin macro, shaded 3D mites, follicle cross-section block."""
import math, os
import numpy as np, cv2
from scipy.spatial import cKDTree
from scipy import ndimage

CACHE = "/home/claude/reel-kit/english/work/cache_mites"
os.makedirs(CACHE, exist_ok=True)


def _noise(h, w, scale, rng):
    """smooth value noise in [-1,1]"""
    gh, gw = max(2, int(h / scale) + 3), max(2, int(w / scale) + 3)
    g = rng.standard_normal((gh, gw)).astype(np.float32)
    n = cv2.resize(g, (int(gw * scale), int(gh * scale)), interpolation=cv2.INTER_CUBIC)[:h, :w]
    return n / (np.abs(n).max() + 1e-6)


def gen_skin(w=1400, h=2300, seed=3, tone="warm"):
    """returns (rgb float32 HxWx3 0..1, pores Nx3 [x, y, r])"""
    key = f"{CACHE}/skin_{w}x{h}_{seed}_{tone}.npz"
    if os.path.exists(key):
        z = np.load(key)
        return z["img"], z["pores"]
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    P = np.stack([xx.ravel(), yy.ravel()], 1)

    def vedge(cell):
        n = int(w * h / cell ** 2 * 1.15)
        pts = rng.uniform([-40, -40], [w + 40, h + 40], (n, 2))
        d, _ = cKDTree(pts).query(P, k=2, workers=-1)
        return (d[:, 1] - d[:, 0]).reshape(h, w).astype(np.float32)

    e1 = vedge(185)
    e2 = vedge(70)
    low = _noise(h, w, 260, rng) * 0.6 + _noise(h, w, 90, rng) * 0.4
    mid = _noise(h, w, 22, rng)
    hi = _noise(h, w, 5, rng)
    H = -0.62 * np.exp(-e1 / 9.0) - 0.09 * np.exp(-e2 / 4.0) + 0.42 * low + 0.16 * mid + 0.03 * hi
    # pores on jittered grid
    pores = []
    sp = 170
    for gy in range(-1, h // sp + 2):
        for gx in range(-1, w // sp + 2):
            x = gx * sp + (sp / 2 if gy % 2 else 0) + rng.uniform(-45, 45)
            y = gy * sp * 0.9 + rng.uniform(-40, 40)
            r = rng.uniform(10, 17)
            if -30 < x < w + 30 and -30 < y < h + 30:
                pores.append((x, y, r))
    pores = np.array(pores, np.float32)
    dmin = np.full((h, w), 1e9, np.float32)
    pr = np.zeros((h, w), np.float32)
    pore_in = np.zeros((h, w), np.float32)
    for x, y, r in pores:
        x0, x1, y0, y1 = int(max(0, x - 4 * r)), int(min(w, x + 4 * r)), int(max(0, y - 4 * r)), int(min(h, y + 4 * r))
        if x1 <= x0 or y1 <= y0:
            continue
        d = np.sqrt((xx[y0:y1, x0:x1] - x) ** 2 + ((yy[y0:y1, x0:x1] - y) * 1.15) ** 2) / r
        H[y0:y1, x0:x1] += -2.2 * np.exp(-(d ** 2) * 1.6) + 0.25 * np.exp(-((d - 1.35) ** 2) * 6)
        pore_in[y0:y1, x0:x1] = np.maximum(pore_in[y0:y1, x0:x1], np.clip(1.25 - d, 0, 1) ** 0.8)
    H = cv2.GaussianBlur(H, (0, 0), 1.8)
    gx = cv2.Sobel(H, cv2.CV_32F, 1, 0, ksize=3) / 8
    gy = cv2.Sobel(H, cv2.CV_32F, 0, 1, ksize=3) / 8
    s = 6.5
    N = np.dstack([-gx * s, -gy * s, np.ones_like(H)])
    N /= np.linalg.norm(N, axis=2, keepdims=True)
    L = np.array([-0.42, -0.55, 0.72], np.float32); L /= np.linalg.norm(L)
    diff = np.clip((N * L).sum(2), 0, 1)
    Hv = L + np.array([0, 0, 1], np.float32); Hv /= np.linalg.norm(Hv)
    spec = np.clip((N * Hv).sum(2), 0, 1) ** 70
    oil = np.clip(0.55 + 0.6 * _noise(h, w, 140, rng), 0, 1)
    base = np.array([0.95, 0.66, 0.54], np.float32) if tone == "warm" else np.array([0.93, 0.70, 0.60], np.float32)
    red = np.array([0.88, 0.46, 0.42], np.float32)
    a = np.clip(0.5 + 0.55 * low, 0, 1)[..., None]
    alb = base * (1 - a * 0.55) + red * (a * 0.55)
    fur = np.exp(-e1 / 7.0)[..., None] * 0.22 + np.exp(-e2 / 3.0)[..., None] * 0.04
    alb = alb * (1 - fur) + np.array([0.70, 0.36, 0.32], np.float32) * fur
    pin = pore_in[..., None]
    alb = alb * (1 - pin) + np.array([0.30, 0.13, 0.11], np.float32) * pin
    img = alb * (0.30 + 0.80 * diff[..., None]) + spec[..., None] * (0.55 * oil[..., None]) * np.array([1.0, 0.97, 0.92], np.float32)
    sss = cv2.GaussianBlur(1 - diff, (0, 0), 6)[..., None]
    img = img + sss * np.array([0.10, 0.015, 0.0], np.float32)
    # fine vellus hairs from some pores
    canvas = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    for x, y, r in pores[rng.random(len(pores)) < 0.22]:
        ang = rng.uniform(0, 2 * math.pi); ln = rng.uniform(90, 220); cur = rng.uniform(-0.004, 0.004)
        pts = []
        for i in range(24):
            u = i / 23
            a2 = ang + cur * ln * u
            pts.append((x + math.cos(a2) * ln * u, y + math.sin(a2) * ln * u))
        for i in range(23):
            th = max(1, int(round(3.2 * (1 - i / 23) + 1)))
            cv2.line(canvas, tuple(int(v) for v in pts[i]), tuple(int(v) for v in pts[i + 1]), (92, 58, 44), th, cv2.LINE_AA)
            if i % 3 == 0:
                cv2.line(canvas, (int(pts[i][0] - 1), int(pts[i][1] - 1)), (int(pts[i + 1][0] - 1), int(pts[i + 1][1] - 1)), (190, 150, 130), 1,
                         cv2.LINE_AA)
    img = canvas.astype(np.float32) / 255
    np.savez(key, img=img, pores=pores)
    return img, pores


# ---------------- 3D mites (stamped shaded spheres) ----------------
_SPH = {}


def sphere(r, col, rim=0.55, spec=0.7):
    key = (int(r * 4), col)
    if key in _SPH:
        return _SPH[key]
    R = r
    n = int(math.ceil(R)) * 2 + 3
    c = n / 2
    y, x = np.mgrid[0:n, 0:n].astype(np.float32)
    nx, ny = (x - c + 0.5) / R, (y - c + 0.5) / R
    d = np.sqrt(nx ** 2 + ny ** 2)
    nz = np.sqrt(np.clip(1 - d ** 2, 0, 1))
    L = np.array([-0.45, -0.55, 0.7]); L /= np.linalg.norm(L)
    diff = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
    sp = np.exp(-((nx + 0.33) ** 2 + (ny + 0.42) ** 2) / 0.028) * spec
    edge = (1 - rim) + rim * nz ** 0.45
    cc = np.array(col, np.float32)
    rgb = cc * (0.58 + 0.52 * diff)[..., None] * edge[..., None] + sp[..., None] * np.array([1, 1, 0.96], np.float32)
    # back-lit translucency glow at the rim (warm)
    rgb += (np.clip(1 - nz, 0, 1) ** 3)[..., None] * np.array([0.10, 0.05, 0.0]) * 0.6
    a = np.clip((1 - d) * R + 0.5, 0, 1)
    out = (np.clip(rgb, 0, 1).astype(np.float32), a.astype(np.float32))
    _SPH[key] = out
    return out


def stamp(canvas, alpha, spr, x, y, op=1.0):
    rgb, a = spr
    n = a.shape[0]
    x0, y0 = int(round(x - n / 2)), int(round(y - n / 2))
    H, W = alpha.shape
    sx0, sy0 = max(0, -x0), max(0, -y0)
    x0c, y0c = max(0, x0), max(0, y0)
    x1c, y1c = min(W, x0 + n), min(H, y0 + n)
    if x1c <= x0c or y1c <= y0c:
        return
    aa = a[sy0:sy0 + y1c - y0c, sx0:sx0 + x1c - x0c][..., None] * op
    canvas[y0c:y1c, x0c:x1c] = canvas[y0c:y1c, x0c:x1c] * (1 - aa) + rgb[sy0:sy0 + y1c - y0c, sx0:sx0 + x1c - x0c] * aa
    alpha[y0c:y1c, x0c:x1c] = alpha[y0c:y1c, x0c:x1c] * (1 - aa[..., 0]) + aa[..., 0]


BODY = (1.0, 0.94, 0.80)


def radius(s, L):
    if s < 0.05:
        return L * (0.040 + 0.35 * s)
    if s < 0.32:
        return L * (0.060 + 0.010 * math.sin((s - 0.05) / 0.27 * math.pi))
    u = (s - 0.32) / 0.68
    return L * (0.062 - 0.030 * u ** 1.4)


def spine(x, y, ang, L, t, wig=1.0, curl=0.0, phase=0.0):
    """head at (x,y), body extends opposite to `ang` (radians = facing direction). returns list of (px,py,tx,ty) for s in [0,1]"""
    pts = []
    hx, hy = math.cos(ang), math.sin(ang)
    px, py = x, y
    a = ang + math.pi
    ds = L / 80
    for i in range(81):
        s = i / 80
        pts.append((px, py, s, a))
        a2 = a + (0.020 * wig * math.sin(s * 5.0 - t * 6.0 + phase) + curl * 0.012) * (0.3 + s)
        a = a2
        px += math.cos(a) * ds; py += math.sin(a) * ds
    return pts


def draw_mite(canvas, alpha, x, y, ang, L, t, vis=1.0, wig=1.0, legs=True, eyes=False, curl=0.0, phase=0.0, gut=True, col=BODY,
              walk=1.0):
    """draws a mite whose head is at (x,y) facing `ang`. vis<1 -> only the front part (rest hidden in a pore)."""
    pts = spine(x, y, ang, L, t, wig, curl, phase)
    vis_n = max(2, int(80 * vis))
    # legs (behind the body)
    if legs:
        for j, s0 in enumerate((0.10, 0.15, 0.20, 0.25)):
            i = int(s0 * 80)
            if i >= vis_n:
                continue
            px, py, s, a = pts[i]
            r = radius(s, L)
            fx, fy = -math.cos(a), -math.sin(a)  # toward head
            for side in (-1, 1):
                nx, ny = -fy * side, fx * side
                sw = math.sin(t * 11 * walk + j * 1.4 + (0 if side > 0 else math.pi)) * 0.35 * walk
                for k in range(4):
                    u = k / 3
                    lx = px + nx * (r * 0.75 + u * L * 0.045) + fx * (u * L * (0.012 + 0.02 * sw))
                    ly = py + ny * (r * 0.75 + u * L * 0.045) + fy * (u * L * (0.012 + 0.02 * sw))
                    stamp(canvas, alpha, sphere(max(1.5, L * (0.022 - 0.007 * u)), (0.96, 0.88, 0.72), 0.35, 0.5), lx, ly)
                stamp(canvas, alpha, sphere(max(1.2, L * 0.009), (0.62, 0.48, 0.34), 0.3, 0.2), lx + nx * L * 0.008, ly + ny * L * 0.008)
    # body: tail -> head so head ends on top
    step = 1 if L > 260 else 2
    for i in range(vis_n - 1, -1, -step):
        px, py, s, a = pts[i]
        r = radius(s, L)
        tone = 1.0 - (0.06 if (i // 2) % 2 and s > 0.33 else 0.0)
        c = tuple(round(v * tone, 3) for v in col)
        stamp(canvas, alpha, sphere(r, c, 0.38, 0.75), px, py)
    if gut:
        for i in range(min(vis_n, 74) - 1, 30, -3):
            px, py, s, a = pts[i]
            r = radius(s, L) * 0.42
            rgb, aa = sphere(r, (0.62, 0.42, 0.20), 0.2, 0.0)
            stamp(canvas, alpha, (rgb, aa * 0.16), px, py)
    # mouthparts
    px, py, s, a = pts[0]
    fx, fy = -math.cos(a), -math.sin(a)
    for side in (-1, 1):
        nx, ny = -fy * side, fx * side
        stamp(canvas, alpha, sphere(L * 0.016, (0.86, 0.76, 0.60), 0.5, 0.5), px + fx * L * 0.02 + nx * L * 0.022,
              py + fy * L * 0.02 + ny * L * 0.022)
    if eyes:
        px, py, s, a = pts[5]
        for side in (-1, 1):
            nx, ny = -fy * side, fx * side
            ex, ey = px + nx * L * 0.026 + fx * L * 0.01, py + ny * L * 0.026 + fy * L * 0.01
            stamp(canvas, alpha, sphere(L * 0.016, (1, 1, 1), 0.2, 0.0), ex, ey)
            stamp(canvas, alpha, sphere(L * 0.009, (0.05, 0.05, 0.07), 0.1, 0.0), ex + fx * L * 0.004, ey + fy * L * 0.004)
    return pts


def mite_layer(w, h, items, t):
    """items: list of dicts for draw_mite. returns rgb, alpha (float) with a soft contact shadow."""
    can = np.zeros((h, w, 3), np.float32)
    al = np.zeros((h, w), np.float32)
    for it in items:
        draw_mite(can, al, t=t, **it)
    return can, al


def comp_mites(frame, can, al, ox=0, oy=0, shadow=0.55, sh_off=(14, 22), blur=9, op=1.0):
    """composite mite layer onto frame (float rgb) at offset with drop shadow"""
    h, w = al.shape
    H, W = frame.shape[:2]
    x0, y0 = int(ox), int(oy)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xb <= xa or yb <= ya:
        return frame
    if shadow > 0:
        M = np.float32([[1, 0, sh_off[0]], [0, 1, sh_off[1]]])
        sa = cv2.warpAffine(al, M, (w, h))
        sa = cv2.GaussianBlur(sa, (0, 0), blur) * shadow * op
        s = sa[ya - y0:yb - y0, xa - x0:xb - x0][..., None]
        frame[ya:yb, xa:xb] *= (1 - s * 0.85)
    a = al[ya - y0:yb - y0, xa - x0:xb - x0][..., None] * op
    frame[ya:yb, xa:xb] = frame[ya:yb, xa:xb] * (1 - a) + can[ya - y0:yb - y0, xa - x0:xb - x0] * a
    return frame
