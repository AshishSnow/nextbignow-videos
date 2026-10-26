# ================= anim_fx.py — FreshNestHub craft library (grows every run; see improvements.md section G) =================
# Each technique here was learned, used in an episode and kept. Add new ones at the bottom with a one-line note:
# what it is, where it came from (principle / source), which episode first used it.


# --- slow in / slow out + overshoot curves (12 principles: "slow in and slow out", "follow-through") ---
def ease_out_back(k, s=1.70158):
    k = clamp(k) - 1; return k * k * ((s + 1) * k + s) + 1


def ease_out_elastic(k, period=0.35):
    k = clamp(k)
    if k in (0.0, 1.0): return k
    return 2 ** (-10 * k) * math.sin((k - period / 4) * (2 * math.pi) / period) + 1


def settle(t, t0, amp=1.0, freq=11.0, decay=6.0):
    """damped wobble after an impact (follow-through / overlapping action). returns 0 before t0."""
    q = t - t0
    return 0.0 if q < 0 else amp * math.exp(-decay * q) * math.sin(freq * q)


# --- squash & stretch (12 principles #1): keep volume, sx * sy = 1 ---
def squash_xy(amount):
    """amount > 0 squashes (wide + short), < 0 stretches (thin + tall)."""
    sy = 1.0 - 0.25 * amount; return 1.0 / max(0.3, sy), sy


def scale_xy(el, sx, sy):
    pm, a = el; h, w = a.shape; nw, nh = max(2, int(w * sx)), max(2, int(h * sy))
    return cv2.resize(pm, (nw, nh), interpolation=cv2.INTER_AREA), cv2.resize(a, (nw, nh), interpolation=cv2.INTER_AREA)


def drop_land(t, t0, y_top, y_floor, dur=0.35):
    """object falls from y_top and lands at y_floor at t0+dur with a squash on impact.
    returns (y, sx, sy)."""
    k = clamp((t - t0) / dur)
    y = y_top + (y_floor - y_top) * (k * k)
    if k < 1: return y, *squash_xy(-0.35 * k)                 # stretch while falling
    w_ = settle(t, t0 + dur, 1.0, 18.0, 9.0)
    return y_floor, *squash_xy(0.6 * w_)                        # squash + wobble on landing


# --- anticipation (12 principles #2): a small move the opposite way before the main action ---
def anticipate(t, t0, lead=0.18, back=0.12):
    """0..1 progress with a short dip below 0 just before t0 (use to pull back before a throw / jump / pop)."""
    if t < t0 - lead: return 0.0
    if t < t0: return -back * math.sin(math.pi * (t - (t0 - lead)) / lead)
    return ease_out_back(clamp((t - t0) / 0.35))


# --- camera language: keyframed push-ins / pans (staging, reveal emphasis) ---
def cam_keys(t, keys):
    """keys = [(time, zoom, cx, cy), ...] -> (zoom, cx, cy) with smooth easing between keys."""
    if t <= keys[0][0]: return keys[0][1:]
    for (t0, z0, x0, y0), (t1, z1, x1, y1) in zip(keys, keys[1:]):
        if t <= t1:
            k = eio(clamp((t - t0) / max(1e-3, t1 - t0)))
            return z0 + (z1 - z0) * k, x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    return keys[-1][1:]


def push_in(f, t, t0, t1, z1=1.12, cx=W / 2, cy=1000):
    """slow push-in on a reveal (use sparingly: 1–2 per video)."""
    k = eio(clamp((t - t0) / max(1e-3, t1 - t0)))
    return cam(f, 1 + (z1 - 1) * k, cx, cy)


# --- secondary action: idle life so nothing is ever frozen ---
def idle_bob(t, seed=0, amp=6.0, speed=2.2):
    return amp * math.sin(t * speed + seed * 1.7)


def blink_k(t, seed=0, every=3.1, dur=0.12):
    ph = (t + seed * 1.37) % every
    return ph < dur


# --- particles: sparkles / confetti / dust puffs on reveals and impacts ---
def sparkles(f, x, y, t, t0, n=10, radius=220, col=(255, 240, 160), seed=1, dur=0.9):
    q = t - t0
    if q < 0 or q > dur: return
    rng = np.random.default_rng(seed); k = q / dur
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi); r_ = radius * (0.3 + 0.7 * eo(k)) * rng.uniform(0.6, 1.0)
        px, py = x + r_ * math.cos(a), y + r_ * math.sin(a); s_ = (1 - k) * rng.uniform(8, 16)
        for ang in (0, math.pi / 2):
            dx, dy = s_ * math.cos(ang), s_ * math.sin(ang)
            cv2.line(f, (int(px - dx), int(py - dy)), (int(px + dx), int(py + dy)), C(col), 3, cv2.LINE_AA)


def confetti(f, t, t0, n=40, seed=3, dur=2.0, cols=((255, 92, 40), (255, 199, 30), (22, 170, 76), (60, 140, 240), (236, 72, 140))):
    q = t - t0
    if q < 0 or q > dur: return
    rng = np.random.default_rng(seed)
    for i in range(n):
        x0 = rng.uniform(80, 1000); vy = rng.uniform(300, 600); sw = rng.uniform(1.5, 3.5)
        x = x0 + 40 * math.sin(q * sw + i); y = 300 + vy * q + 120 * q * q
        if y > 1500: continue
        ang = q * sw * 90 + i * 20; w_, h_ = 18, 8 * abs(math.cos(q * 6 + i))
        box = cv2.boxPoints(((x, y), (w_, max(2, h_)), ang)).astype(np.int32)
        cv2.fillPoly(f, [box], C(cols[i % len(cols)]), cv2.LINE_AA)


def dust_puff(f, x, y, t, t0, n=7, dur=0.5, seed=2):
    q = t - t0
    if q < 0 or q > dur: return
    rng = np.random.default_rng(seed); k = q / dur
    for i in range(n):
        side = -1 if i % 2 else 1; dx = side * (30 + 120 * eo(k)) * rng.uniform(0.6, 1.0)
        ov = f.copy(); cv2.circle(ov, (int(x + dx), int(y - 20 * k)), int(14 + 26 * k), (1, 1, 1), -1, cv2.LINE_AA)
        a_ = 0.45 * (1 - k); f[:] = f * (1 - a_) + ov * a_


# --- motion trail for fast-moving props (smear frames, like classic cartoons) ---
def smear(f, el, x0, y0, x1, y1, steps=5, op=0.35):
    for i in range(steps):
        k = i / steps; comp(f, el, x0 + (x1 - x0) * k, y0 + (y1 - y0) * k, op=op * (k ** 2))
    comp(f, el, x1, y1)


# --- soft contact shadow under any prop (grounding = solid drawing) ---
def ground_shadow(f, x, y, w, op=0.28):
    contact(f, x, y, w, op)
