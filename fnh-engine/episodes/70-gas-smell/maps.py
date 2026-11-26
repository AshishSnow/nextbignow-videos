"""maps.py — documentary map graphics (Natural Earth via world-atlas / us-atlas, public domain).
globe(W,H,T,lon0,lat0,R,hl={'India':col}, arc=(p0,p1,k)) -> float32 HxWx3
statemap(W,H,center,scale,focus='Texas',pin=(lat,lon),t) -> float32"""
import sys, math, numpy as np, cv2
sys.path.insert(0, '/home/claude/studio/tools'); import topo
M = '/home/claude/studio/assets/map/'
_C = None; _RAS = {}; _ST = None
def countries():
    global _C
    if _C is None: _C = topo.load(M + 'package/countries-50m.json', 'countries')
    return _C
def states():
    global _ST
    if _ST is None: _ST = topo.load(M + 'us/package/states-10m.json', 'states')
    return _ST
def raster(hl=(), RW=4096):
    """equirect layers: 0 land, 1 borders, 2.. highlight masks"""
    k = (tuple(hl), RW)
    if k in _RAS: return _RAS[k]
    RH = RW // 2; L = np.zeros((RH, RW, 2 + len(hl)), np.uint8)
    def px(r): return np.stack([(r[:, 0] + 180) / 360 * RW, (90 - r[:, 1]) / 180 * RH], 1).astype(np.int32)
    land = np.zeros((RH, RW), np.uint8); bord = np.zeros((RH, RW), np.uint8)
    for nm, rings in countries().items():
        for r in rings:
            if np.ptp(r[:, 0]) > 300: continue   # antimeridian slivers
            p = px(r); cv2.fillPoly(land, [p], 255); cv2.polylines(bord, [p], True, 255, 2, cv2.LINE_AA)
    L[..., 0] = land; L[..., 1] = bord
    for i, nm in enumerate(hl):
        m = np.zeros((RH, RW), np.uint8)
        for r in countries().get(nm, []):
            if np.ptp(r[:, 0]) > 300: continue
            cv2.fillPoly(m, [px(r)], 255)
        L[..., 2 + i] = m
    _RAS[k] = L; return L

def rot(lat, lon, lat0, lon0):
    """geographic -> orthographic (x,y,z visible if z>0)"""
    la, lo, la0, lo0 = map(np.radians, (lat, lon, lat0, lon0))
    x = np.cos(la) * np.sin(lo - lo0)
    y = np.cos(la0) * np.sin(la) - np.sin(la0) * np.cos(la) * np.cos(lo - lo0)
    z = np.sin(la0) * np.sin(la) + np.cos(la0) * np.cos(la) * np.cos(lo - lo0)
    return x, y, z
_GRID = {}
def globe(W, H, lon0, lat0, R, hl=None, cx=None, cy=None, arc=None, T=0.0, land=(64, 72, 80), ocean=(12, 24, 42)):
    hl = hl or {}; names = list(hl); L = raster(tuple(names))
    RH, RW = L.shape[:2]; cx = W / 2 if cx is None else cx; cy = H / 2 if cy is None else cy
    gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    x = (gx - cx) / R; y = -(gy - cy) / R; rr = x * x + y * y; inside = rr <= 1
    z = np.sqrt(np.clip(1 - rr, 0, 1))
    la0, lo0 = math.radians(lat0), math.radians(lon0)
    lat = np.arcsin(np.clip(z * math.sin(la0) + y * math.cos(la0), -1, 1))
    lon = lo0 + np.arctan2(x, z * math.cos(la0) - y * math.sin(la0))
    mx = ((np.degrees(lon) + 180) % 360) / 360 * RW; my = (90 - np.degrees(lat)) / 180 * RH
    S = cv2.remap(L, mx.astype(np.float32), my.astype(np.float32), cv2.INTER_LINEAR).astype(np.float32) / 255
    if S.ndim == 2: S = S[..., None]
    # background: deep space with stars
    o = np.zeros((H, W, 3), np.float32) + np.array([6, 8, 14], np.float32)
    r = np.random.default_rng(3); st = r.random((90, 3))
    for sx, sy, sb in st: cv2.circle(o, (int(sx * W), int(sy * H)), 1, (110 + 120 * sb,) * 3, -1)
    shade = (0.35 + 0.75 * np.clip(z * .8 + (x * -.35 + y * .35), 0, 1))[..., None]
    col = np.array(ocean, np.float32) * (1 - S[..., :1]) + np.array(land, np.float32) * S[..., :1]
    col = col + S[..., 1:2] * 40
    for i, nm in enumerate(names):
        c, a = hl[nm]; m = S[..., 2 + i:3 + i] * a; col = col * (1 - m) + np.array(c, np.float32) * m
    sph = col * shade
    edge = np.clip((np.sqrt(rr) - .86) / .14, 0, 1)[..., None]                 # atmosphere rim
    sph = sph + edge * np.array([60, 120, 200], np.float32) * .55
    o = np.where(inside[..., None], sph, o)
    halo = np.clip(1 - (np.sqrt(rr) - 1) / .12, 0, 1) * (rr > 1)
    o = o + halo[..., None] * np.array([40, 90, 170], np.float32) * .5
    for nm, (c, a) in hl.items():   # soft glow around highlighted countries
        pass
    if arc is not None:
        (la1, lo1), (la2, lo2), k = arc
        n = 120; p1 = np.array(sph_xyz(la1, lo1)); p2 = np.array(sph_xyz(la2, lo2)); om = math.acos(np.clip(p1 @ p2, -1, 1))
        pts = []
        for i in range(int(n * k) + 1):
            s = i / n; v = (math.sin((1 - s) * om) * p1 + math.sin(s * om) * p2) / math.sin(om)
            h = 1 + .05 * math.sin(math.pi * s)                                # arc lifts off the surface
            la = math.degrees(math.asin(v[2])); lo = math.degrees(math.atan2(v[1], v[0]))
            X, Y, Z = rot(la, lo, lat0, lon0); pts.append((cx + X * R * h, cy - Y * R * h, Z))
        lay = np.zeros((H, W), np.float32)
        for a_, b_ in zip(pts[:-1], pts[1:]):
            if a_[2] > .02 and b_[2] > .02: cv2.line(lay, (int(a_[0]), int(a_[1])), (int(b_[0]), int(b_[1])), float(min(1, a_[2] * 3) ** 1.5), 4, cv2.LINE_AA)
        if pts:
            hx, hy, hz = pts[-1]
            if hz > .02: cv2.circle(lay, (int(hx), int(hy)), 9, 1.0, -1, cv2.LINE_AA)
        glow = cv2.GaussianBlur(lay, (0, 0), 9)
        o = o * (1 - lay[..., None]) + np.array([255, 70, 60], np.float32) * lay[..., None] + glow[..., None] * np.array([255, 80, 60], np.float32) * 1.4
    return o
def sph_xyz(lat, lon):
    la, lo = math.radians(lat), math.radians(lon); return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))
def proj(lat, lon, lat0, lon0, R, cx, cy):
    X, Y, Z = rot(lat, lon, lat0, lon0); return cx + X * R, cy - Y * R, Z

def statemap(W, H, lat0, lon0, scale, focus='Texas', pin=None, tpin=0.0, T=0.0):
    """flat local map (equirect, cos-lat corrected) of US states, focus state lit"""
    o = np.zeros((H, W, 3), np.float32) + np.array([12, 22, 38], np.float32)
    k = math.cos(math.radians(lat0))
    def P(r): return np.stack([W / 2 + (r[:, 0] - lon0) * k * scale, H / 2 - (r[:, 1] - lat0) * scale], 1).astype(np.int32)
    lay = np.zeros((H, W), np.uint8); fz = np.zeros((H, W), np.uint8); bd = np.zeros((H, W), np.uint8)
    for nm, rings in states().items():
        for r in rings:
            p = P(r)
            if p[:, 0].max() < -50 or p[:, 0].min() > W + 50 or p[:, 1].max() < -50 or p[:, 1].min() > H + 50: continue
            cv2.fillPoly(fz if nm == focus else lay, [p], 255); cv2.polylines(bd, [p], True, 255, 2, cv2.LINE_AA)
    # Mexico / Canada context from countries
    for nm in ('Mexico', 'Canada'):
        for r in countries().get(nm, []): cv2.fillPoly(lay, [P(r)], 255)
    o = o * (1 - lay[..., None] / 255) + np.array([52, 60, 68], np.float32) * lay[..., None] / 255
    o = o * (1 - fz[..., None] / 255) + np.array([150, 38, 34], np.float32) * fz[..., None] / 255
    o = o + bd[..., None] / 255 * 45
    g = cv2.GaussianBlur(fz.astype(np.float32) / 255, (0, 0), 30); o = o + g[..., None] * np.array([200, 60, 40], np.float32) * .35
    if pin is not None and tpin > 0:
        x, y = P(np.array([[pin[1], pin[0]]]))[0]; kk = min(1, tpin / .25)
        for j in range(3):                                               # pulse rings
            ph = (T * 1.2 + j / 3) % 1; cv2.circle(o, (int(x), int(y)), int(14 + 70 * ph), (255 * (1 - ph),) * 3, 2, cv2.LINE_AA)
        yy = int(y - 40 * (1 - kk))
        cv2.circle(o, (int(x), yy), 13, (255, 255, 255), -1, cv2.LINE_AA); cv2.circle(o, (int(x), yy), 7, (226, 36, 36), -1, cv2.LINE_AA)
    return o
