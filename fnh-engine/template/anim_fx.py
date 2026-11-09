import bisect, re
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


# ================= EXPLAINING (ep 09): Mayer's multimedia principles turned into helpers =================
# Signalling = point the eye at what the voice is talking about (spotlight, arrows, pulses).
# Spatial contiguity = put the label ON/BESIDE the part it names (label_at with a leader line), not in a far caption.
# Temporal contiguity = start each picture on the word that names it (use T(line, word)).
# Segmenting / pre-training = name the parts first (nerve, alarm, brain), then show the process step by step.
# Coherence / redundancy = short labels only; the voice explains, the picture shows. (u.osu.edu/multimedialearning; Mayer 2020)
def spotlight(f, x, y, r, amt=0.55, feather=90.0):
    """signalling: dim everything except a soft circle (radius r) around the focus point."""
    if amt <= 0.01: return
    m = np.clip((np.hypot(_xx - x, _yy - y) - r) / feather, 0, 1) * amt
    f *= (1 - m)[..., None]


def path_point(pts, k):
    """point at fraction k (0..1) along a polyline (by length)."""
    P = np.asarray(pts, np.float32); seg = np.hypot(*(P[1:] - P[:-1]).T); L = float(seg.sum()) + 1e-6
    d = clamp(k) * L
    for i, s_ in enumerate(seg):
        if d <= s_ or i == len(seg) - 1:
            q = 0 if s_ < 1e-6 else min(1.0, d / s_); return float(P[i][0] + (P[i + 1][0] - P[i][0]) * q), float(P[i][1] + (P[i + 1][1] - P[i][1]) * q)
        d -= s_


def draw_arrow(f, x0, y0, x1, y1, k=1.0, col=INK, th=10, head=34, op=1.0):
    """arrow that draws itself from (x0, y0) to (x1, y1); k 0..1 = drawn fraction (animate it with ramp())."""
    if k <= 0.01 or op <= 0.01: return
    ex, ey = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    g = f if op >= 0.999 else f.copy()
    cv2.line(g, (int(x0), int(y0)), (int(ex), int(ey)), C(col), int(th), cv2.LINE_AA)
    a = math.atan2(ey - y0, ex - x0)
    P = np.array([[ex + head * 0.35 * math.cos(a), ey + head * 0.35 * math.sin(a)],
                  [ex - head * math.cos(a - 0.5), ey - head * math.sin(a - 0.5)],
                  [ex - head * math.cos(a + 0.5), ey - head * math.sin(a + 0.5)]], np.int32)
    cv2.fillPoly(g, [P], C(col), cv2.LINE_AA)
    if op < 0.999: f[:] = f * (1 - op) + g * op


def label_at(f, text, x, y, t, t0, tx=None, ty=None, bg=INK, fg=WHITE, size=30, d=0.3):
    """spatial contiguity: a label pill at (x, y) that pops in at t0, with a leader arrow to the part (tx, ty) it names."""
    if t < t0: return
    k = clamp((t - t0) / d)
    if tx is not None: draw_arrow(f, x, y, tx, ty, eo(clamp((t - t0 - 0.08) / 0.3)), bg, 7, 24)
    comp(f, chip(text, bg, fg, size), x, y, scale=0.85 + 0.15 * eback(k) if k < 1 else 1.0, op=clamp(k * 3))


def pulse_path(f, pts, t, t0, dur=0.6, col=(255, 236, 110), r=20, n=1, gap=0.25, trail=7, wire=None):
    """travelling signal pulse(s) along a polyline (nerve signals, flows), with a fading trail. wire = colour to light the path."""
    if wire is not None and t >= t0:
        cv2.polylines(f, [np.asarray(pts, np.int32)], False, C(wire), 10, cv2.LINE_AA)
    for j in range(n):
        k = (t - t0 - j * gap) / dur
        if k < 0 or k > 1.15: continue
        for i in range(trail, -1, -1):
            kk = k - i * 0.025
            if kk < 0 or kk > 1: continue
            px, py = path_point(pts, kk); rr = r * (1 - i / (trail + 1))
            cv2.circle(f, (int(px), int(py)), max(2, int(rr)), C(col), -1, cv2.LINE_AA)
        if k <= 1:
            px, py = path_point(pts, k); glow(f, px, py, r * 1.6, col, 0.5)


def recap_steps(f, items, y, t, t0s, gap=330, size=1.0):
    """visual recap: a row of icons (el, label) that build up one by one (1 -> 2 -> 3) with arrows between them."""
    n = len(items); x0 = W / 2 - gap * (n - 1) / 2
    for i, ((el, lab), ts) in enumerate(zip(items, t0s)):
        if t < ts: continue
        k = pin(t, ts, 0.3); x = x0 + i * gap
        comp(f, el, x, y, scale=k * size)
        comp(f, chip(lab, INK, WHITE, 28), x, y + 150 * size, op=clamp((t - ts) / 0.2))
        if i > 0: draw_arrow(f, x - gap + 120 * size, y, x - 120 * size, y, eo(clamp((t - ts) / 0.25)), INK, 9, 26)


def inset(f, cx, cy, r, draw, k=1.0, ring=WHITE, th=12):
    """magnified close-up window (scale cue / zoom-in explanation): draw(g) paints the close-up on a frame copy,
    shown only inside a circle of radius r*k at (cx, cy) with an outlined rim. (ep 09)"""
    if k <= 0.01: return
    g = f.copy(); draw(g)
    m = np.zeros((H, W), np.float32); cv2.circle(m, (int(cx), int(cy)), int(r * k), 1.0, -1, cv2.LINE_AA)
    f[:] = f * (1 - m[..., None]) + g * m[..., None]
    cv2.circle(f, (int(cx), int(cy)), int(r * k), C(INK), th + 8, cv2.LINE_AA); cv2.circle(f, (int(cx), int(cy)), int(r * k), C(ring), th, cv2.LINE_AA)


def count_up(t, t0, v1, dur=0.8):
    """kinetic number: integer that counts up from 0 to v1 with ease-out (use as the BIG word of ui_word)."""
    return int(round(v1 * eo(clamp((t - t0) / dur))))


# ================= REFUTATION + CONTRAST (ep 10): myth -> refute -> explain =================
# Refutation text (Tippett 2010; Kendeou's KReC framework, Educ Psychol Rev 2021): name the myth out loud, refute it
# explicitly, then give the correct explanation, so the old idea and the new one are active at the same time and the new
# one wins. Contrasting cases (Schwartz & Bransford 1998): show "what people think / what really happens" side by side.
def myth_tag(f, x, y, t, t0, t_bust=None, size=56, word="MYTH"):
    """red MYTH tag that pops in at t0; at t_bust a fat red X slashes across it + 'BUSTED' stamp slams."""
    if t < t0: return
    comp(f, tag_el(word, RED_, WHITE, size), x, y, scale=pin(t, t0, 0.3))
    if t_bust is not None and t >= t_bust:
        k = clamp((t - t_bust) / 0.18); L = 150 * size / 56
        for sgn in (-1, 1):
            p0 = (x - L, y - sgn * L * 0.55); p1 = (x - L + 2 * L * k, y - sgn * L * 0.55 + sgn * 1.1 * L * k)
            cv2.line(f, (int(p0[0]), int(p0[1])), (int(p1[0]), int(p1[1])), C(INK), 34, cv2.LINE_AA)
            cv2.line(f, (int(p0[0]), int(p0[1])), (int(p1[0]), int(p1[1])), C(RED_), 22, cv2.LINE_AA)
        if t >= t_bust + 0.15: rot_comp(f, stamp_el("BUSTED", RED_, int(size * 0.9)), x, y + 110 * size / 56, -8,
                                        1.5 - 0.5 * eo(clamp((t - t_bust - 0.15) / 0.18)), clamp((t - t_bust - 0.15) / 0.1), 0.3)


def split_contrast(f, t, t0, draw_l, draw_r, title_l="WHAT YOU THINK", title_r="WHAT REALLY HAPPENS",
                   col_l=(230, 60, 40), col_r=(20, 160, 110), y0=620, y1=1500, wipe=0.35, t_r=None, xl=120, xr=960):
    """worked-example contrast: two tinted panels (left = myth / belief, right = reality) with a divider wiping in.
    Panels span xl..540..xr (inside the safe zone, centred on x=540). draw_l(g) / draw_r(g) paint on full-frame copies
    (left panel centre = (xl+540)/2, right = (540+xr)/2); t_r = when the right panel appears."""
    if t < t0: return
    k = eio(clamp((t - t0) / wipe)); xm = int(xl + (540 - xl) * k)
    t_r = t0 if t_r is None else t_r
    for side, draw, col, x0, x1, ts in ((0, draw_l, col_l, xl, 540, t0), (1, draw_r, col_r, 540, xr, t_r)):
        if t < ts: continue
        g = f.copy(); g[y0:y1, x0:x1] = g[y0:y1, x0:x1] * 0.72 + np.array(C(col), np.float32) * 0.28; draw(g)
        m = np.zeros((H, W), np.float32)
        if side == 0: m[y0:y1, xl:max(xl, xm)] = 1.0
        else: m[y0:y1, 540:540 + int((xr - 540) * clamp((t - ts) / wipe))] = 1.0
        f[:] = f * (1 - m[..., None]) + g * m[..., None]
    cv2.line(f, (540, y0), (540, y1), C(INK), 8, cv2.LINE_AA)
    cv2.rectangle(f, (xl, y0), (xr, y1), C(INK), 6, cv2.LINE_AA)
    comp(f, chip(title_l, INK, WHITE, 26), (xl + 540) / 2, y0 + 44, op=clamp((t - t0) / 0.2))
    if t >= t_r: comp(f, chip(title_r, INK, WHITE, 26), (540 + xr) / 2, y0 + 44, op=clamp((t - t_r) / 0.2))


def chapter_card(f, t, t0, num, title, y=1380, dur=1.6, col=YEL_):
    """signposting for 2-3 min videos: a small 'PART n' chip + title that slides in at a re-hook and leaves after dur."""
    if t < t0 or t > t0 + dur: return
    k = eo(clamp((t - t0) / 0.25)); out = clamp((t0 + dur - t) / 0.2)
    x = 540 - 600 * (1 - k)
    comp(f, chip(f"PART {num}", INK, col, 28), x, y - 52, op=out)
    comp(f, chip(title, col, INK, 40), x, y + 8, op=out)


# ================= SCALE CUES (ep 11): show HOW SMALL something is before explaining it =================
# Explainers make tiny things understandable with a chain of familiar reference objects (you -> tongue -> nerve ending ->
# sensor), a continuous "powers of ten" zoom with a magnification readout, and a "you are here" mini-map (Eames,
# "Powers of Ten" 1977; advids.co "Visualizing scale and scope" guide: chained reference objects, continuous zoom with
# a graphical scale overlay). Use zoom_through() for the jump between levels and scale_ladder() to keep the viewer oriented.
def zoom_through(t, t0, dur, far, near, cx, cy, zmax=6.0):
    """continuous zoom: far() is pushed into the point (cx, cy) (which slides to the centre) up to zmax, then near()
    takes over, settling from a slight over-zoom. far / near = callables returning full frames. Returns the frame."""
    k = clamp((t - t0) / max(1e-3, dur))
    if k <= 0: return far()
    if k >= 1: return near()
    e = eio(k)
    if k < 0.55:
        z = zmax ** (eio(k / 0.55) * 0.85)
        q = eio(k / 0.55)
        return cam(far(), z, cx, cy, (W / 2 - cx) * q, (H / 2 - cy) * q)
    m = eio((k - 0.55) / 0.45)
    a = cam(far(), zmax ** 0.85, cx, cy, W / 2 - cx, H / 2 - cy)
    b = cam(near(), 1 + 0.5 * (1 - m))
    return a * (1 - m) + b * m


def scale_ladder(f, items, cur, t, t_cur, y=1400, gap=200, s=0.5):
    """'you are here' mini-map: a row of the zoom levels so far (el, label), the current one ringed + bigger,
    with 'x10'-style magnification chips on the arrows. items = [(el, label, mag_text_or_None), ...]; cur = index."""
    n = cur + 1; x0 = W / 2 - gap * (n - 1) / 2
    for i in range(n):
        el, lab, mag = items[i]; x = x0 + i * gap
        k = pin(t, t_cur, 0.3) if i == cur else 1.0
        sc_ = s * (1.25 if i == cur else 0.9) * k
        cv2.circle(f, (int(x), int(y)), int(70 * (1.25 if i == cur else 0.9) * k), C(WHITE), -1, cv2.LINE_AA)
        comp(f, el, x, y, scale=sc_)
        cv2.circle(f, (int(x), int(y)), int(70 * (1.25 if i == cur else 0.9) * k), C(YEL_ if i == cur else INK), 8 if i == cur else 5, cv2.LINE_AA)
        comp(f, chip(lab, INK, WHITE, 22), x, y + 92, op=k)
        if i > 0:
            draw_arrow(f, x - gap + 80, y, x - 95, y, 1.0 if i < cur else eo(clamp((t - t_cur) / 0.25)), INK, 7, 20)
            if mag: comp(f, chip(mag, YEL_, INK, 20), x - gap / 2, y - 44, op=1.0 if i < cur else clamp((t - t_cur - 0.15) / 0.2))


# ================= PRE-TRAINING + MATCH CUTS (ep 12) =================
# Pre-training principle (Mayer, Multimedia Learning ch. 10; 5 of 5 tests, median d = 0.85): people follow a fast narrated
# process far better when they already know the NAMES and the possible STATES of its parts. So before a process shot, show a
# 2-3 s "cast" card: each part pops in with its name + its state change (LUMP -> LEAF), then the process can run uninterrupted.
def cast_card(f, items, t, t0s, y=1000, gap=300, title="MEET THE CAST", t_title=None, panel=(255, 255, 255), size=1.0):
    """pre-training cast: items = [(el, name, state_or_None), ...] pop in at t0s on white panels, centred on x=540."""
    n = len(items); x0 = W / 2 - gap * (n - 1) / 2
    if title and t >= (t_title if t_title is not None else t0s[0] - 0.15):
        comp(f, chip(title, INK, YEL_, 34), W / 2, y - 250 * size, op=clamp((t - (t_title if t_title is not None else t0s[0] - 0.15)) / 0.2))
    for i, ((el, name, state), ts) in enumerate(zip(items, t0s)):
        if t < ts: continue
        k = pin(t, ts, 0.3); x = x0 + i * gap
        pw, ph = int(gap * 0.44 * size), int(180 * size)
        g = f.copy()
        cv2.rectangle(g, (int(x - pw), int(y - ph)), (int(x + pw), int(y + ph)), C(INK), -1, cv2.LINE_AA)
        cv2.rectangle(g, (int(x - pw + 7), int(y - ph + 7)), (int(x + pw - 7), int(y + ph - 7)), C(panel), -1, cv2.LINE_AA)
        a = clamp((t - ts) / 0.15); f[:] = f * (1 - a) + g * a
        comp(f, el, x, y - 30 * size + 4 * math.sin(t * 3 + i), scale=k)
        comp(f, chip(name, INK, WHITE, int(28 * size)), x, y + ph - 40 * size, op=a)
        if state: comp(f, chip(state, YEL_, INK, int(22 * size)), x, y - ph + 34 * size, op=clamp((t - ts - 0.2) / 0.2))


def iris_mix(prev, cur, p, cx, cy, ring=WHITE, th=12):
    """match-cut iris: the new shot opens as a growing circle from (cx, cy) (put it on a round object that the next shot
    is 'inside' of, e.g. a sweet -> its close-up). p 0..1. Classic cartoon 'iris in' used as a shape match cut. (ep 12)"""
    r = (60 + math.hypot(W, H) * eio(clamp(p)))
    m = np.zeros((H, W), np.float32); cv2.circle(m, (int(cx), int(cy)), int(r), 1.0, -1, cv2.LINE_AA)
    out = prev * (1 - m[..., None]) + cur * m[..., None]
    if p < 0.98:
        cv2.circle(out, (int(cx), int(cy)), int(r), C(INK), th + 8, cv2.LINE_AA); cv2.circle(out, (int(cx), int(cy)), int(r), C(ring), th, cv2.LINE_AA)
    return out


# 2-bone IK (ep 12): make Chubby's right arm reach a fixed point (tool grip). shoulder for chub(x, y, s): (x + 118s, y - 215s - 46s).
def arm_ik(sh, tg, L1, L2):
    """2-bone IK for Chubby's right arm (chub angle convention: degrees from straight down, + outward)."""
    dx, dy = tg[0] - sh[0], tg[1] - sh[1]; d = min(L1 + L2 - 1e-3, math.hypot(dx, dy))
    th = math.degrees(math.atan2(dx, dy)); al = math.degrees(math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1)))
    a1 = th - al; ex, ey = sh[0] + L1 * math.sin(math.radians(a1)), sh[1] + L1 * math.cos(math.radians(a1))
    return a1, math.degrees(math.atan2(tg[0] - ex, tg[1] - ey))


# ================= PROGRESSIVE CHAIN MAP (ep 13): explain a chain reaction / multi-step process =================
# Build-up diagram (progressive disclosure): a cause-and-effect chain is shown one link at a time, and a compact map of the
# WHOLE chain stays on screen while the close-ups change, so the viewer always knows (1) which step we're on, (2) what came
# before it and (3) how many steps are left. Past links stay but dim (they become context), the current link is ringed and
# bigger (signalling), future links are empty slots (the open loop "there's more"). Colour-code each icon to match the
# character in the main picture (Gestalt similarity). Then the same map lights up link by link as the 5-s recap.
# Sources: Mayer's segmenting + signalling principles (Mayer 2020, Multimedia Learning); progressive-reveal of complex figures
# (G. Fisk, "Progressive reveal animations for complex technical figures", 2025: reveal in the order of the process, colour-
# coded labels linked to parts, nothing else competing on screen).
def chain_map(f, items, cur, t, t_cur, y=1400, gap=146, r=50, slots=True, dim=0.55, panel=True):
    """items = [(el, label), ...] (the whole chain); cur = index of the current link (-1 = none yet); t_cur = when it
    became current (pop + arrow draw-in). Centred on x=540; keep y inside the safe zone (<= 1440)."""
    n = len(items); x0 = W / 2 - gap * (n - 1) / 2
    if panel:
        g = f.copy(); cv2.rectangle(g, (int(x0 - r - 26), int(y - r - 22)), (int(x0 + gap * (n - 1) + r + 26), int(y + r + 52)), C(INK), -1, cv2.LINE_AA)
        f[:] = f * 0.45 + g * 0.55
    for i, (el, lab) in enumerate(items):
        x = x0 + i * gap
        if i > cur:
            if slots:
                cv2.circle(f, (int(x), int(y)), int(r * 0.55), C((255, 255, 255)), 3, cv2.LINE_AA)
                comp(f, chip("?", (60, 60, 70), WHITE, 20), x, y)
            continue
        k = pin(t, t_cur, 0.3) if i == cur else 1.0
        rr = r * (1.18 if i == cur else 0.9) * k
        cv2.circle(f, (int(x), int(y)), int(rr) + 5, C(INK), -1, cv2.LINE_AA)
        cv2.circle(f, (int(x), int(y)), int(rr), C(WHITE), -1, cv2.LINE_AA)
        pm, a = el; s_ = (2 * rr * 0.78) / max(a.shape)
        comp(f, scale_el(el, s_), x, y)
        if i < cur and dim > 0:
            g = f.copy(); cv2.circle(g, (int(x), int(y)), int(rr) + 5, C((40, 40, 50)), -1, cv2.LINE_AA)
            m = np.zeros((H, W), np.float32); cv2.circle(m, (int(x), int(y)), int(rr) + 5, 1.0, -1, cv2.LINE_AA)
            m *= (1 - dim) * 0.8; f[:] = f * (1 - m[..., None]) + g * m[..., None]
        cv2.circle(f, (int(x), int(y)), int(rr), C(YEL_ if i == cur else (200, 200, 210)), 7 if i == cur else 3, cv2.LINE_AA)
        comp(f, chip(lab, YEL_ if i == cur else WHITE, INK, 22 if i == cur else 18), x, y + r + 26, op=clamp((t - t_cur) / 0.2) if i == cur else 0.85)
        if i > 0:
            draw_arrow(f, x - gap + r * 0.95, y, x - rr - 6, y, 1.0 if i < cur else eo(clamp((t - t_cur) / 0.25)), WHITE, 6, 18)


# ================= CHARTS ON VIDEO (ep 14): a graph of a HIDDEN quantity over time, drawn while you watch =================
# Things you can't see (sleepy chemical piling up, caffeine leaving the body) become clear as a line that grows across the
# day. Rules for charts in video (P. Bradshaw, Online Journalism Blog, 'Showing charts on video', Jun 2026; Knaflic,
# Storytelling with Data): (1) remove to improve - few lines, no legend, no grid, no numbers the voice doesn't need; (2) the
# title states the FINDING, not the variable; (3) direct labels at the end of each line instead of a legend; (4) wipe the line
# left -> right in sync with the narration, reveal in stages; (5) one strong colour for the focus line, others grey;
# (6) annotate the key moment with an icon + arrow; (7) a presenter interacting with the chart (Chubby rides the 'now' point).
def day_graph(f, t, now, lines, x0=120, x1=960, y0=700, y1=1290, h0=7.0, h1=24.0, ticks=((8, "8 AM"), (14, "2 PM"), (20, "8 PM"), (24, "12")),
              marks=(), title=None, op=1.0, panel=(255, 252, 244), ylab=None, label_k=1.0):
    """lines = [(fn(hour)->0..1, col, label, start_hour[, (label_dx, label_dy)]), ...] drawn from start_hour to `now` (hours); marks = [(hour, el, text, t_show)].
    Returns (X, Y) mapping functions hour->px and value->px so shots can annotate. Keep x0..x1 inside 60..960, y inside 250..1500."""
    X = lambda h: x0 + (x1 - x0) * (h - h0) / (h1 - h0)
    Y = lambda v: y1 - (y1 - y0) * clamp(v, -0.05, 1.08)
    g = f if op >= 0.999 else f.copy()
    if panel is not None:
        cv2.rectangle(g, (x0 - 50, y0 - 70), (x1 + 40, y1 + 90), C(INK), -1, cv2.LINE_AA)
        cv2.rectangle(g, (x0 - 44, y0 - 64), (x1 + 34, y1 + 84), C(panel), -1, cv2.LINE_AA)
    cv2.line(g, (x0, y1), (x1, y1), C(INK), 6, cv2.LINE_AA); cv2.line(g, (x0, y0 - 20), (x0, y1), C(INK), 6, cv2.LINE_AA)
    for h, lab in ticks:
        cv2.line(g, (int(X(h)), y1), (int(X(h)), y1 + 14), C(INK), 5, cv2.LINE_AA)
        comp(g, chip(lab, INK, WHITE, 24), X(h), y1 + 50)
    if ylab: comp(g, chip(ylab, INK, YEL_, 20), x0 + 10 + len(ylab) * 6, y0 - 34)
    for h, el, txt, ts in marks:
        if t < ts: continue
        k = pin(t, ts, 0.3); xm = int(X(h))
        for yy in range(y0 - 10, y1, 26): cv2.line(g, (xm, yy), (xm, min(y1, yy + 13)), C((150, 150, 160)), 4, cv2.LINE_AA)
        if el is not None: comp(g, el, xm, y0 - 10, scale=k)
        if txt: comp(g, chip(txt, INK, YEL_, 20), xm, y0 + 48, op=clamp((t - ts) / 0.25))
    heads = []
    for ln in lines:
        fn, col, lab, hs = ln[:4]; ldx, ldy = ln[4] if len(ln) > 4 else (0, -44)
        if now <= hs: heads.append(None); continue
        hh = np.linspace(hs, min(now, h1), max(2, int(80 * (min(now, h1) - hs) / (h1 - h0)) + 2))
        P = np.array([[X(h), Y(fn(h))] for h in hh], np.int32)
        cv2.polylines(g, [P], False, C(INK), 17, cv2.LINE_AA); cv2.polylines(g, [P], False, C(col), 10, cv2.LINE_AA)
        hx, hy = P[-1]; cv2.circle(g, (int(hx), int(hy)), 15, C(INK), -1, cv2.LINE_AA); cv2.circle(g, (int(hx), int(hy)), 10, C(col), -1, cv2.LINE_AA)
        heads.append((hx, hy))
        if lab and label_k > 0: comp(g, chip(lab, col, WHITE if sum(col) < 500 else INK, 26), min(x1 - 60, max(x0 + 80, hx + ldx)), hy + ldy, op=label_k)
    if title: comp(g, chip(title, INK, WHITE, 34), (x0 + x1) / 2, y0 - 112)
    if op < 0.999: f[:] = f * (1 - op) + g * op
    return X, Y, heads


# ---------------- ep 16: ROUTE MAP — a journey through a system drawn like a metro map (explaining a path + time) ----------------
def route_map(f, stops, k, t, token=None, pts=None, col=(255, 210, 90), line_col=(255, 255, 255), times=None, lab_side=None, dim=0.45):
    """stops = [(x, y, NAME)] along a route; k = progress 0..len(stops)-1 (float) of the travelling token (an element).
    visited stops are filled + labelled, the current one is ringed, future ones are hollow; times = optional chip per stop.
    The track is drawn from stop to stop with rounded corners; the travelled part glows in `col`. Returns token (x, y)."""
    P = pts or [(x, y) for x, y, _ in stops]
    seg = [math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1]) for i in range(len(P) - 1)]
    for i in range(len(P) - 1):
        cv2.line(f, (int(P[i][0]), int(P[i][1])), (int(P[i + 1][0]), int(P[i + 1][1])), C(OUT3), 30, cv2.LINE_AA)
        cv2.line(f, (int(P[i][0]), int(P[i][1])), (int(P[i + 1][0]), int(P[i + 1][1])), C(tuple(int(c * dim + 40 * (1 - dim)) for c in line_col)), 18, cv2.LINE_AA)
    kk = clamp(k, 0, len(P) - 1); i0 = min(int(kk), len(P) - 2); fr = kk - i0
    tx = P[i0][0] + (P[i0 + 1][0] - P[i0][0]) * fr; ty = P[i0][1] + (P[i0 + 1][1] - P[i0][1]) * fr
    for i in range(i0 + 1):
        q = P[i + 1] if i < i0 else (tx, ty)
        cv2.line(f, (int(P[i][0]), int(P[i][1])), (int(q[0]), int(q[1])), C(col), 18, cv2.LINE_AA)
    for i, (x, y, name) in enumerate(stops):
        vis = kk >= i - 0.02; cur = abs(kk - i) < 0.5
        if not name: continue                                                   # bend point, not a stop
        cv2.circle(f, (int(x), int(y)), 30, C(OUT3), -1, cv2.LINE_AA)
        cv2.circle(f, (int(x), int(y)), 22, C(col if vis else (90, 80, 90)), -1, cv2.LINE_AA)
        if not vis: cv2.circle(f, (int(x), int(y)), 12, C(OUT3), -1, cv2.LINE_AA)
        if cur: cv2.circle(f, (int(x), int(y)), int(42 + 4 * math.sin(t * 8)), C(WHITE), 5, cv2.LINE_AA)
        side = (lab_side[i] if lab_side else (1 if x < 540 else -1))
        if vis or cur:
            el = chip(name, INK if vis else (70, 64, 70), WHITE, 28)
            comp(f, el, x + side * (60 + el[1].shape[1] / 2), y)
            if times and times[i]:
                el2 = chip(times[i], col, INK, 24); comp(f, el2, x + side * (60 + el2[1].shape[1] / 2), y + 44)
    if token is not None: comp(f, token, tx, ty)
    return tx, ty


# ================= ep 17 (31 Oct): ACTING KIT — staging + silhouette (Thomas & Johnston, 'The Illusion of Life': staging = present an idea so it is
# unmistakably clear; a pose reads only if its SILHOUETTE reads). Check poses with engine/tools/ink_sheet.py (black-shape row). =================
POSE = {"idle": dict(la=(28, 14), ra=(22, 12)), "point": dict(la=(20, 10), ra=(72, 42), lean=4), "present": dict(la=(90, 120), ra=(90, 120)),
        "cheer": dict(la=(150, 170), ra=(150, 170)), "shock": dict(la=(112, 160), ra=(112, 160), lean=8), "think": dict(la=(-160, -115), ra=(30, 16), lean=-6),
        "whisper": dict(la=(20, 10), ra=(140, -140), lean=6), "cheek": dict(la=(150, -120), ra=(26, 12), lean=-8), "shrug": dict(la=(80, 150), ra=(80, 150)),
        "hold_up": dict(la=(40, 30), ra=(150, 175), lean=5), "arms_out": dict(la=(96, 60), ra=(96, 60)), "tada": dict(la=(120, 150), ra=(160, 150), lean=6),
        # ep 20: queasy (hand on belly + hand to mouth), STOP (palm out, warning), yawn (hands behind the head, the walk-away at night)
        "sick": dict(la=(26, -112), ra=(148, -130), lean=-6), "stop": dict(la=(22, 10), ra=(100, 70), lean=-5), "yawn": dict(la=(160, -150), ra=(160, -150), lean=-3)}


def double_take(t, t0, d=0.55):
    """look away -> snap back -> wide eyes: returns (look, lean, expr, brow) for the 0.55 s after t0 (ep 17 acting kit)."""
    q = t - t0
    if q < 0: return (0.6, 0), 0.0, "n", "n"
    if q < d * 0.3: return (0.6, 0), 0.0, "n", "n"
    if q < d * 0.45: return (-0.8, -0.2), -6.0, "sus", "sus"
    k = clamp((q - d * 0.45) / (d * 0.3))
    return (-0.9, -0.3), -10.0 * (1 + 0.6 * math.sin(k * math.pi)), "wow", "up"


def flinch(t, t0, amp=1.0):
    """a quick recoil (lean + squash) after a hit at t0."""
    q = t - t0
    if q < 0: return 0.0, 0.0
    return -12 * amp * math.exp(-q * 5) * math.cos(q * 18), 0.35 * amp * math.exp(-q * 6)


# ================= ep 18 (31 Oct): FOLLOW-THROUGH, OVERLAPPING ACTION + DRAG (Thomas & Johnston principle 5; "things don't come to a
# stop all at once - first one part and then another"). Motion flows core -> limbs -> extremities -> appendages: hair lags the head
# by 2-4 frames and keeps moving 4-8 frames after the head stops; liquids show the most follow-through (RebusFarm 'Follow through
# and overlapping action', Aug 2026; Wikipedia / The Illusion of Life). =================
def drag(t, fn, frames=3, gain=1.0):
    """DRAG: the appendage follows the main motion `fn(t)` (a number or a tuple) a few frames late -> returns the offset to add to the
    appendage = gain * (fn(t - frames/FPS) - fn(t)). Use it for Chubby's hair (chub(..., hair=drag(t, head_x))), an apron hem, a tail."""
    a, b = fn(t - frames / FPS), fn(t)
    if isinstance(b, (tuple, list)): return tuple(gain * (x - y) for x, y in zip(a, b))
    return gain * (a - b)


def follow(t, t0, amp=1.0, frames_lag=3, freq=14.0, decay=7.0):
    """FOLLOW-THROUGH after the main part stops at t0: the loose part overshoots and settles (damped wobble that starts frames_lag late)."""
    return settle(t, t0 + frames_lag / FPS, amp, freq, decay)


def jump_back(t, t0, dist=140.0, dur=0.28):
    """a recoil jump away from something hot: x offset that eases out with a small overshoot, then holds (moving hold)."""
    k = clamp((t - t0) / dur)
    return dist * (ease_out_back(k) if k < 1 else 1.0)


# ================= ep 19 (31 Oct): TIMING & SPACING — snappy cartoon timing (timing = how many frames an action takes; spacing = how far it
# moves per frame). Rules learned: a 6-frame action feels snappy, a 24-frame one deliberate; a long anticipation followed by an instant
# move creates 'snap'; fix 'rushed' by HOLDING the key pose longer, not by adding in-betweens; a hold must never freeze (the moving hold:
# tiny drift + eyes alive, 'a frozen character instantly appears dead' - Shawn Kelly, Animation Mentor); heavy impact = ~2 frames of
# contact then 12+ frames of settle; blinks 2-4 frames; a take: anticipation back, extreme pose held ~3 frames, settle with a small
# 'shock absorber' forward move (Brian LeMay, Take Keys). =================
def snap(t, t0, frames=4, over=1.7):
    """0..1 in `frames` frames with a small overshoot: a snappy pose change (use instead of a slow ease for arms / head / props)."""
    k = clamp((t - t0) / max(1e-3, frames / FPS))
    return ease_out_back(k, over) if k < 1 else 1.0


def keyed(t, keys, frames=4, over=1.7):
    """step through key values on their times with snap transitions and HOLDS in between: keys = [(t0, value), ...] (values = numbers
    or tuples of numbers, e.g. arm angles). Before the first key = first value. Snappy timing: 4-frame moves, long holds."""
    if t <= keys[0][0]: return keys[0][1]
    cur = keys[0][1]
    for (ta, va), (tb, vb) in zip(keys, keys[1:]):
        if t < tb:
            k = snap(t, ta, frames, over)
            return tuple(a + (b - a) * k for a, b in zip(cur, va)) if isinstance(va, (tuple, list)) else cur + (va - cur) * k
        cur = va
    ta, va = keys[-1]; prev = keys[-2][1] if len(keys) > 1 else va
    k = snap(t, ta, frames, over)
    return tuple(a + (b - a) * k for a, b in zip(prev, va)) if isinstance(va, (tuple, list)) else prev + (va - prev) * k


def pose_mix(a, b, k):
    """blend two POSE dicts (la, ra, lean) by k 0..1."""
    out = {}
    for key in set(a) | set(b):
        va, vb = a.get(key, (0, 0) if key != "lean" else 0.0), b.get(key, (0, 0) if key != "lean" else 0.0)
        out[key] = tuple(x + (y - x) * k for x, y in zip(va, vb)) if isinstance(va, (tuple, list)) else va + (vb - va) * k
    return out


def pose_keys(t, keys, frames=4):
    """snappy pose changes with holds: keys = [(t0, POSE_dict), ...] -> a POSE dict for chub(**pose)."""
    if t <= keys[0][0]: return dict(keys[0][1])
    cur = keys[0][1]
    for (ta, pa), (tb, pb) in zip(keys, keys[1:]):
        if t < tb: return pose_mix(cur, pa, snap(t, ta, frames))
        cur = pa
    prev = keys[-2][1] if len(keys) > 1 else keys[-1][1]
    return pose_mix(prev, keys[-1][1], snap(t, keys[-1][0], frames))


def moving_hold(t, seed=0, amp=1.0):
    """idle drift during a held pose so it never freezes: returns dict(lean, look, bob) to add to a pose (tiny, slow, out of phase)."""
    return dict(lean=1.6 * amp * math.sin(t * 0.9 + seed), look=(0.12 * amp * math.sin(t * 0.7 + seed * 2.1), 0.08 * amp * math.cos(t * 0.5 + seed)),
                bob=2.0 * amp * math.sin(t * 1.3 + seed * 0.7))


def take(t, t0, amp=1.0, hold=8):
    """a cartoon TAKE on a surprise at t0: 3 frames anticipation (down + squash), a 2-frame snap up (stretch + wide eyes), a `hold`-frame
    extreme held (moving), then a 6-frame settle with a small forward 'shock absorber'. Returns dict(dy, squash, lean, expr, brow, look)."""
    q = (t - t0) * FPS
    if q < 0: return dict(dy=0.0, squash=0.0, lean=0.0, expr="n", brow="n", look=(0, 0))
    if q < 3: k = q / 3; return dict(dy=10 * amp * k, squash=0.45 * amp * k, lean=-3 * amp * k, expr="n", brow="n", look=(0, 0.3))
    if q < 5: k = (q - 3) / 2; return dict(dy=-22 * amp * k, squash=-0.4 * amp * k, lean=6 * amp * k, expr="wow", brow="up", look=(0, -0.4))
    if q < 5 + hold: k = (q - 5) / hold; return dict(dy=-22 * amp + 2 * math.sin(k * 6), squash=-0.4 * amp * (1 - 0.3 * k), lean=6 * amp, expr="wow", brow="up", look=(0, -0.3))
    k = clamp((q - 5 - hold) / 6); s_ = math.sin(math.pi * k)
    return dict(dy=-22 * amp * (1 - k), squash=-0.4 * amp * (1 - k) + 0.12 * amp * s_, lean=6 * amp * (1 - k) + 3 * amp * s_, expr="wow" if k < 0.6 else "happy", brow="up", look=(0, -0.2 * (1 - k)))


# --- CAMERA LANGUAGE kit (ep 20, 1 Nov; craft skill 'camera language'): each move carries ONE meaning, used where that meaning is the beat.
#     crash zoom = a comic beat / sudden realisation (snaps in 3 frames, HOLDS, no ease back); dutch angle = unease ('something is wrong here');
#     handheld drift = urgency / documentary closeness (the CCTV night); rack focus = move attention between depth planes without a cut;
#     push-in (push_in above) = pull the viewer into a thought. Rule: one camera idea per shot, motivated by the line (HowToFilmSchool 'crash zoom';
#     Morphic camera-movement reference: 'crash zoom - comic beats, shocks and punchlines', 'dutch angle - unease', 'rack focus - move attention
#     without a cut', 'handheld - realism, urgency').
def crash_zoom(f, t, t0, z=1.35, cx=W / 2, cy=900, frames=3):
    """snap zoom onto (cx, cy): reaches z in `frames` frames (tiny overshoot) and holds - a punchline / realisation beat."""
    if t < t0: return f
    k = clamp((t - t0) * FPS / frames)
    zz = 1 + (z - 1) * (k + 0.06 * math.sin(math.pi * k) if k < 1 else 1 + 0.04 * math.exp(-(t - t0 - frames / FPS) * 14))
    return cam(f, zz, cx, cy)


def dutch(f, t, t0, deg=7.0, dur=0.35, cx=W / 2, cy=H / 2, z=1.08):
    """dutch angle: the frame eases into a tilt (zoomed slightly so no edge shows) - unease / 'something is off'."""
    if t < t0: return f
    k = eio(clamp((t - t0) / max(1e-3, dur)))
    return cam(f, 1 + (z - 1) * k, cx, cy, rot=deg * k)


def handheld(t, amp=1.0, seed=0):
    """(dx, dy, rot) of a breathing handheld camera (layered slow sines, never repeats visibly) -> cam(f, z, cx, cy, dx, dy, rot)."""
    p = seed * 1.7
    dx = amp * (9 * math.sin(t * 1.3 + p) + 4 * math.sin(t * 3.1 + 2 * p))
    dy = amp * (7 * math.sin(t * 1.7 + 0.5 + p) + 3 * math.sin(t * 2.6 + p))
    return dx, dy, amp * 0.6 * math.sin(t * 0.9 + p)


def rack_layer(f, draw, sigma=0.0, op=1.0):
    """draw a FOREGROUND layer with its own focus: draw(g) paints onto a copy; only what changed is blended back, blurred by `sigma`.
    Rack focus = animate sigma on the fg layer (sharp -> soft) while the background goes the other way with dof()."""
    g = f.copy(); draw(g)
    m = (np.abs(g - f).max(2) > 1e-3).astype(np.float32)
    if sigma > 0.4:
        sm = cv2.GaussianBlur(g, (0, 0), sigma); m = cv2.GaussianBlur(m, (0, 0), sigma * 0.8); g = sm
    m = np.clip(m * 1.4, 0, 1) * op
    f[:] = f * (1 - m[..., None]) + g * m[..., None]
    return f


def cctv(f, t, label="KITCHEN CAM 2", clock=None, rec=True):
    """security-camera look (night): green-grey grade, scanlines, vignette, REC dot, a big timestamp. clock = 'HH:MM' text."""
    gry = f.mean(2, keepdims=True)
    f[:] = np.clip((f * 0.6 + gry * 0.4) * np.array([0.86, 1.0, 0.9], np.float32), 0, 1)
    f[::4] *= 0.9
    f[:] = f * (1 - 0.35 * np.clip(np.hypot(_xx - W / 2, _yy - H / 2) / 1100, 0, 1) ** 2)[..., None]
    if rec and (int(t * 2) % 2 == 0): cv2.circle(f, (110, 300), 16, (0.9, 0.12, 0.1), -1, cv2.LINE_AA)
    comp(f, ed_el(label, "", lead_col=(235, 240, 230), lead_size=30), 260 if rec else 220, 300)
    if clock: comp(f, ed_el(clock, "", lead_col=(235, 240, 230), lead_size=58), 820, 300)
    for (x0, y0, sx, sy) in ((80, 270, 1, 1), (1000, 270, -1, 1), (80, 1460, 1, -1), (1000, 1460, -1, -1)):
        cv2.line(f, (x0, y0), (x0 + 60 * sx, y0), (0.9, 0.95, 0.88), 4, cv2.LINE_AA); cv2.line(f, (x0, y0), (x0, y0 + 60 * sy), (0.9, 0.95, 0.88), 4, cv2.LINE_AA)
    return f


# ================= VISEMES (ep 21): Chubby's mouth follows the actual SOUNDS of the narration, not only its loudness =================
# Craft: mouths don't track letters, they track a small set of sound groups (Preston Blair's chart; Rhubarb Lip Sync's 6 basic + 3 extended shapes): lips closed
# for M B P, teeth on the lip for F V, wide/teeth for EE S T K, tall open for AH, medium for EH, round for OH, pucker for OO W, tongue up for L N D TH.
# The mouth shape should arrive a frame or so BEFORE the sound; flicker between shapes under ~2 frames reads as noise, so short sounds merge; hard closes (M B P) stay.
_V_DIG = [("tion", "ve"), ("ough", "vo"), ("igh", "ve"), ("ee", "ve"), ("ea", "ve"), ("oo", "vu"), ("ou", "vh"), ("ow", "vo"), ("oa", "vo"), ("ai", "vh"), ("ay", "vh"),
          ("th", "vl"), ("sh", "ve"), ("ch", "ve"), ("ph", "vf"), ("qu", "vu"), ("wh", "vu"), ("ck", "ve"), ("ng", "vl"), ("er", "vh"), ("ar", "va"), ("or", "vo"), ("ir", "vh"), ("ur", "vh")]
_V_ONE = dict(a="vh", e="vh", i="ve", o="vo", u="vh", y="ve", m="vm", b="vm", p="vm", f="vf", v="vf", w="vu", l="vl", n="vl", d="vl", t="ve", s="ve", z="ve", c="ve", k="ve", g="ve", j="ve", x="ve", r="vu", h="vh", q="ve")
_V_WEIGHT = dict(vh=1.3, va=1.4, vo=1.4, vu=1.1, ve=0.9, vl=0.7, vm=0.9, vf=0.9)


def _word_visemes(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if len(w) > 2 and w.endswith("e") and w[-2] not in "aeiou": w = w[:-1]                # silent e
    out = []; i = 0
    while i < len(w):
        for dg, v in _V_DIG:
            if w.startswith(dg, i): out.append(v); i += len(dg); break
        else:
            out.append(_V_ONE.get(w[i], "vh")); i += 1
    res = []
    for v in out:
        if not res or res[-1] != v: res.append(v)
    return res or ["vh"]


def _build_visemes(lead=0.042, min_d=0.075):
    W_ = AL["words"]; tl = []
    for i, w in enumerate(W_):
        t0 = w["t"]; nxt = W_[i + 1]["t"] if i + 1 < len(W_) and W_[i + 1]["line"] == w["line"] else None
        lend = AL["lines"][w["line"]]["end"]
        t1 = nxt if nxt is not None else lend
        t1 = min(t1, t0 + 0.09 * max(2, len(w["w"])) + 0.12)                                  # don't hold a mouth through a pause inside a line
        vs = _word_visemes(w["w"])
        if (t1 - t0) / len(vs) < min_d:                                                       # too fast: keep the hard closes + the vowels only
            keep = [v for v in vs if v in ("vm", "vf", "vh", "va", "vo", "vu")] or vs[:1]; vs = keep[: max(1, int((t1 - t0) / min_d))]
        tw = sum(_V_WEIGHT.get(v, 1.0) for v in vs); c = t0
        for v in vs:
            d_ = (t1 - t0) * _V_WEIGHT.get(v, 1.0) / tw; tl.append((c - lead, c + d_ - lead, v)); c += d_
    return tl


_VIS = None


def viseme(t):
    """the mouth for time t (from work/align.json) or 0 between words. Upgrade open vowels on stressed-loud moments to the tall mouth."""
    global _VIS
    if _VIS is None: _VIS = _build_visemes(); _VIS_T = None
    i = bisect.bisect_right(_VIS_S(), t) - 1
    if i >= 0 and _VIS[i][0] <= t < _VIS[i][1]:
        v = _VIS[i][2]
        if v == "vh":
            j = int(t * FPS)
            if j < len(_env) and _env[j] > 0.85: return "va"
        return v
    return 0


_VIS_ST = None


def _VIS_S():
    global _VIS_ST
    if _VIS_ST is None: _VIS_ST = [x[0] for x in _VIS]
    return _VIS_ST


def talk(t, on=True):
    """ep 21: lip sync = visemes (replaces the loudness-only 0/1/2/3 of anim_base)."""
    return viseme(t) if on else 0



# ================= ep 22 (3 Nov): THE WALK CYCLE (animation craft: contact -> down -> passing -> up; Adobe / GarageFarm / Brian Lemay walk guides, improvements.md G) =================
# One full cycle = 2 steps; heavyset = flat plants, a clear dip on the down pose, ~26 frames. The planted foot NEVER slides: during stance it moves back relative to the body at
# exactly the body's ground speed (stride = speed x period / 2). The swing foot travels forward on an ARC. Pelvis: lowest ~3 frames after contact (down), highest ~9 frames (up).
# Arms swing opposite to the same-side leg and the forearm lags (follow-through). Head + hair lag the body. The shot passes **walk(...) straight into chub().
def _ik2(hip, ank, L1, L2, bend=1.0):
    """2-bone knee: the knee bends toward `bend` (+1 = screen right)."""
    dx, dy = ank[0] - hip[0], ank[1] - hip[1]; D = max(1e-3, math.hypot(dx, dy)); D2 = min(D, L1 + L2 - 0.5)
    a = (L1 * L1 - L2 * L2 + D2 * D2) / (2 * D2); h_ = math.sqrt(max(0.0, L1 * L1 - a * a))
    ux, uy = dx / D, dy / D
    return (hip[0] + ux * a - uy * h_ * bend * -1, hip[1] + uy * a + ux * h_ * bend * -1)


def walk(t, x, y, s=1.0, speed=300.0, dir=1, period=1.08, t0=0.0, lift=30.0, bob=9.0, amt=1.0, arm=26.0, arm_base=14.0, track=False):
    """returns dict(x, y, legs, la, ra, lean, turn, look, hair, bob) for chub(). speed = ground speed px/s at this s. track=True: x stays (the set scrolls by walk_shift); else x + speed*(t-t0).
    amt 0..1 scales the whole walk so he can walk to a stop. Foot times for the foley: walk_steps()."""
    amt = clamp(amt); sl = speed * period / 2 * amt
    ph = (t - t0) / period
    wx = x if track else x + dir * speed * (t - t0)
    def foot(p):
        p = p % 1.0
        if p < 0.5:                                                          # stance: heel strike at 0, flat, rolling to the toe at the end; locked to the ground
            rel = sl / 2 - sl * (p / 0.5); up = 0.0
            frot = (14.0 * clamp(1 - p / 0.05) - 24.0 * clamp((p - 0.36) / 0.14)) * amt     # + = toe up (heel strike), - = toe down (toe off); flat plants for a heavy guy
        else:                                                                # swing: forward on an arc, highest just after passing
            k = (p - 0.5) / 0.5; e_ = k * k * (3 - 2 * k)
            rel = -sl / 2 + sl * e_; up = lift * s * amt * math.sin(math.pi * k ** 0.85)
            frot = (-24.0 * (1 - clamp(k / 0.45)) + 14.0 * clamp((k - 0.7) / 0.3)) * amt
        return rel, up, frot
    drop = bob * s * amt * math.cos(4 * math.pi * (ph - 0.11))               # + = down: lowest 3 frames after contact, highest ~10 frames after
    yb = y + drop
    hip_y = yb - 112 * s; L = 57 * s
    legs = []
    for (off, side_) in ((0.5, -dir), (0.0, dir)):                           # far leg (drawn first) is half a cycle away
        rel, up, frot = foot(ph + off)
        hipx = wx + side_ * 16 * s
        ank = (wx + dir * rel + side_ * 8 * s, y - 8 * s - up)
        knee = _ik2((hipx, hip_y), ank, L, L, dir)
        legs.append(((hipx, hip_y), knee, ank, frot * dir, dir))
    swing = math.cos(2 * math.pi * ph); lag = math.cos(2 * math.pi * (ph - 0.09))     # + = the near leg is forward
    # this body is drawn front-on, so 'forward' reads as the arm lifting + the forearm bending; arms alternate, opposite to their leg, forearm lags (follow-through)
    a_r = arm_base + arm * 0.55 * amt * (-swing) * dir; f_r = 10 + arm * 1.5 * amt * max(0.0, -lag * dir) - 6 * amt * max(0.0, lag * dir)
    a_l = arm_base + arm * 0.55 * amt * (swing) * dir; f_l = 10 + arm * 1.5 * amt * max(0.0, lag * dir) - 6 * amt * max(0.0, -lag * dir)
    hair_x = -dir * 7 * amt + 3 * amt * math.sin(2 * math.pi * ph * 2 - 1.0); hair_y = 3 * amt * math.cos(4 * math.pi * (ph - 0.2))
    wx += 7 * s * amt * math.sin(2 * math.pi * (ph + 0.15))                     # the S-curve: the weight shifts over the planted foot
    return dict(x=wx, y=yb, legs=legs, la=(a_l, f_l), ra=(a_r, f_r), lean=dir * (3.0 * amt + 1.5 * amt * math.sin(2 * math.pi * ph)), turn=dir * 0.75, look=(dir * 0.7, 0), hair=(hair_x, hair_y), bob=drop * 0.35)


def walk_steps(t0, t1, period=1.08):
    """contact times (for the footstep foley)."""
    out = []; k = 0
    while t0 + k * period / 2 < t1: out.append(t0 + k * period / 2); k += 1
    return out


# ================= ep 24 (5 Nov): SPEED RAMPS = slow motion without a cut (craft: Morphic 'Speed ramping': 'action flows from normal speed into dramatic slow motion at a key moment, then ramps back out, creating
# emphasis without a cut'; typical = 100 % -> 10-20 % over 0.5-1 s, hold 1-2 s at the key moment, back out over 0.5-1 s; sync the peak to a beat. Filmed slow motion judders with too few frames; ours is drawn, so every frame is new). =================
def speed_ramp(t, keys):
    """STORY TIME for clock time t. keys = [(clock_t, speed), ...]: speed is linear between keys (1 = real time, 0.15 = slow motion, 0 = freeze), constant outside. Drive the physics of a shot with it: y = y0 + 0.5 * g * s(t)^2."""
    if t <= keys[0][0]: return (t - keys[0][0]) * keys[0][1]
    s = 0.0
    for (a, va), (b, vb) in zip(keys, keys[1:]):
        if t <= b:
            k = (t - a) / max(1e-6, b - a); vt = va + (vb - va) * k
            return s + (t - a) * (va + vt) / 2
        s += (b - a) * (va + vb) / 2
    return s + (t - keys[-1][0]) * keys[-1][1]


def slowmo_frame(f, t, on=1.0, label=None):
    """a thin cue that time has slowed: soft vignette + a tiny speed tag (optional). on 0..1."""
    if on <= 0: return f
    f[:] = f * (1 - 0.3 * on * np.clip(np.hypot(_xx - W / 2, _yy - H / 2) / 1100, 0, 1) ** 2)[..., None]
    return f


# --- ACTING (ep 25): THE EYES LEAD. A look-change travels up the body in order: eyes first (2 frames), head a few frames later, body last; a blink lands on the head turn. Replaces a whole-body turn all at once.
def eye_lead(t, t0, frm=-1.0, to=1.0, turn_amt=0.6, lean_amt=4.0):
    """-> dict(look, turn, lean, blink) moving from side frm to side to (-1..1), starting at t0."""
    e = clamp((t - t0) * FPS / 2); h = clamp(((t - t0) * FPS - 3) / 5); b = clamp(((t - t0) * FPS - 5) / 7)
    side = lambda k: frm + (to - frm) * (k * k * (3 - 2 * k))
    blink = 3 <= (t - t0) * FPS < 6
    return dict(look=(side(e), 0.0), turn=side(h) * turn_amt, lean=side(b) * lean_amt, blink=blink)


# ================= ep 27 (7 Nov): the DRAW-ON BOARD kit (whiteboard / blueprint explainer, owner 6 Nov: 'blueprint, board style with white background, 2D').
# Craft rules (Epipheo whiteboard production guide 2026; Knowlify): draw each element IN SYNC with the word that names it; one visual per idea; minimal blank
# background; mostly one ink colour + ONE pop of accent for the key point; hand-lettered, readable type; the scene change is an ERASE ('one drawing erases
# itself as the next one takes shape'); small swoosh / pop sounds. Mine: big shape first, then details, then the label (Disney 'staging' order), a pen tip on
# the moving end, a fixed wobble so lines never boil. Chubby INK stays the actor: put him (or peek()) beside the board drawing.
BP_INK = (34, 86, 168); BP_GRID = (214, 228, 246); BP_GRID2 = (190, 210, 238); BP_PAPER = (253, 252, 248)
F_HAND = f"{R}/fonts/hand/ArchitectsDaughter-Regular.ttf"
if not os.path.exists(F_HAND): F_HAND = F_BOLD


def board_bg(grid=60):
    """white drawing paper with a pale blue blueprint grid (major line every 5 cells)."""
    def mk():
        f = np.ones((H, W, 3), np.float32) * np.array(C(BP_PAPER), np.float32)
        for i, x in enumerate(range(0, W + 1, grid)): cv2.line(f, (x, 0), (x, H), C(BP_GRID2 if i % 5 == 0 else BP_GRID), 2 if i % 5 == 0 else 1, cv2.LINE_AA)
        for i, y in enumerate(range(0, H + 1, grid)): cv2.line(f, (0, y), (W, y), C(BP_GRID2 if i % 5 == 0 else BP_GRID), 2 if i % 5 == 0 else 1, cv2.LINE_AA)
        return f
    return gcache(("board_bg", grid), mk).copy()


def _cut_poly(P, k):
    """the first k (0..1) of a polyline by length -> (points, end point)."""
    P = [tuple(map(float, p)) for p in P]
    if k >= 1 or len(P) < 2: return P, P[-1]
    seg = [math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1]) for i in range(len(P) - 1)]; L = sum(seg) * max(0.0, k); out = [P[0]]
    for i, s in enumerate(seg):
        if L <= s:
            q = L / max(s, 1e-6); e = (P[i][0] + (P[i + 1][0] - P[i][0]) * q, P[i][1] + (P[i + 1][1] - P[i][1]) * q); out.append(e); return out, e
        L -= s; out.append(P[i + 1])
    return out, P[-1]


def draw_on(f, pts, k, col=BP_INK, w=7, seed=0, wob=1.4, tip=True, closed=False):
    """DRAW-ON: the polyline appears from its first point to its last as k goes 0 -> 1 (a pen tip rides the moving end). Returns the end point."""
    if k <= 0.001: return None
    P = list(pts) + ([pts[0]] if closed else [])
    if wob: P = _wob(P, wob, seed)
    Q, e = _cut_poly(P, clamp(k))
    if len(Q) >= 2: cv2.polylines(f, [np.int32(np.round(np.array(Q)))], False, C(col), int(w), cv2.LINE_AA)
    if tip and k < 0.999: cv2.circle(f, (int(e[0]), int(e[1])), int(w * 0.75) + 2, C(col), -1, cv2.LINE_AA)
    return e


def draw_ell_on(f, cx, cy, rx, ry, k, col=BP_INK, w=7, seed=0, a0=-100, wob=1.4):
    return draw_on(f, _arcpts(cx, cy, rx, ry, a0, a0 + 360, 56), k, col, w, seed, wob)


def draw_arrow_on(f, p0, p1, k, col=BP_INK, w=7, head=26, bend=0.0, seed=0):
    """a hand-drawn arrow (optionally bent) that draws itself; the head appears at the end."""
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2; nx, ny = -(p1[1] - p0[1]), p1[0] - p0[0]; nl = math.hypot(nx, ny) or 1
    c = (mx + nx / nl * bend, my + ny / nl * bend)
    P = [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * c[0] + u * u * p1[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * c[1] + u * u * p1[1]) for u in np.linspace(0, 1, 24)]
    draw_on(f, P, k, col, w, seed, 0.8)
    if k > 0.92:
        a = math.atan2(P[-1][1] - P[-3][1], P[-1][0] - P[-3][0]); hk = clamp((k - 0.92) / 0.08)
        for s_ in (-1, 1):
            q = (p1[0] - head * hk * math.cos(a + s_ * 0.5), p1[1] - head * hk * math.sin(a + s_ * 0.5))
            cv2.line(f, (int(p1[0]), int(p1[1])), (int(q[0]), int(q[1])), C(col), int(w), cv2.LINE_AA)


def hand_text_el(text, size=56, col=BP_INK):
    def mk():
        fn = font(F_HAND, size * 2); tw = fn.getlength(text) / 2; w_, h_ = int(tw + 30), int(size * 1.55)
        im = Image.new("RGBA", (w_ * 2, h_ * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.text((w_, h_), text, font=fn, fill=tuple(col) + (255,), anchor="mm", stroke_width=max(1, size // 22), stroke_fill=tuple(col) + (255,))
        return el_from(im.resize((w_, h_), Image.LANCZOS))
    return gcache(("htext", text, size, col), mk)


def write_on(f, text, x, y, t, t0, size=56, col=BP_INK, cps=22.0, op=1.0):
    """hand lettering that WRITES itself left to right at cps characters a second (a soft edge, no pop). Starts at t0."""
    if t < t0: return
    pm, a = hand_text_el(text, size, col); h_, w_ = a.shape
    k = clamp((t - t0) * cps / max(1, len(text)))
    if k < 1:
        xx = np.arange(w_, dtype=np.float32)[None, :]; edge = k * (w_ + 30) - 15
        m = np.clip((edge - xx) / 15.0, 0, 1); pm = pm * m[..., None]; a = a * m
    comp(f, (pm, a), x, y, op=op)


def hatch_on(f, poly, k, col=None, gap=16, ang=45, w=4, op=0.85):
    """accent hatching that sweeps into a closed shape (the ONE pop of colour on the board)."""
    if k <= 0.001: return
    col = col or ACC; P = np.int32(np.round(np.array(poly)))
    x0, y0 = P[:, 0].min(), P[:, 1].min(); x1, y1 = P[:, 0].max(), P[:, 1].max()
    m = np.zeros((H, W), np.uint8); cv2.fillPoly(m, [P], 255)
    lay = np.zeros((H, W), np.uint8); L = (x1 - x0) + (y1 - y0)
    for d_ in range(-int(y1 - y0), int(x1 - x0) + 1, gap):
        cv2.line(lay, (int(x0 + d_), int(y1)), (int(x0 + d_ + (y1 - y0)), int(y0)), 255, w, cv2.LINE_AA)
    sweep = np.zeros((H, W), np.float32); xe = int(x0 + (x1 - x0 + 40) * clamp(k)); sweep[:, :max(0, min(W, xe))] = 1
    a = (lay.astype(np.float32) / 255) * (m.astype(np.float32) / 255) * sweep * op
    f[:] = f * (1 - a[..., None]) + np.array(C(col), np.float32) * a[..., None]


def erase_mix(prev, cur, p):
    """ERASE transition: a soft eraser band sweeps diagonally; the old drawing is wiped away and the new one is under it (Epipheo: the wipe)."""
    yy, xx = np.mgrid[0:H:4, 0:W:4].astype(np.float32)
    d = (xx + yy * 0.45) / (W + H * 0.45); edge = p * 1.25 - 0.1
    m = np.clip((edge - d) / 0.08, 0, 1); band = np.exp(-((d - edge + 0.04) / 0.03) ** 2) * 0.55
    m = cv2.resize(m, (W, H))[..., None]; band = cv2.resize(band, (W, H))[..., None]
    return prev * (1 - m) + cur * m + band * (1.0 - cur) * 0.6


def doze(t, t0=0.0, period=2.6, depth=1.0):
    """NODDING OFF (acting, ep 27): the head sinks slowly (eyes closing, lean + drop), then JERKS back up in 3 frames with wide eyes; repeats.
    -> dict(lean, look, bob, blink, expr, brow) for chub()."""
    ph = ((t - t0) % period) / period; q = (t - t0) % period
    if t < t0: return dict(lean=0.0, look=(0, 0.1), bob=0.0, blink=False, expr="sleepy", brow="sad")
    if ph < 0.82: d = eio(ph / 0.82) * depth; return dict(lean=9 * d, look=(0.1, 0.25 + 0.7 * d), bob=16 * d, blink=d > 0.55, expr="sleepy", brow="sad")
    j = (q - 0.82 * period) * FPS
    if j < 3: d = depth * (1 - j / 3); return dict(lean=9 * d - 2, look=(0, -0.2), bob=16 * d - 4, blink=False, expr="wow", brow="up")
    return dict(lean=-2.0, look=(0, -0.3), bob=-3.0, blink=False, expr="wow", brow="up")


# ================= MORPH CUT (ep 28): a shape-match transition between two shots =================
# Rules (ProVideo Coalition, D. Allen 'The literal invisible cut: mastering the fluid morph' 2019; School of Motion 'Six essential motion design transitions'):
# match POSITION in frame first, then size; momentum matters more than a perfect pose; 8-10 frames work best (the half-second default is too long); hide the
# seam at a pause or at the fastest movement (motion blur hides it). In our 2D look: the object in shot A (a board drawing) slides + scales onto the matching
# object in shot B (the lit version) while A dissolves into B, with a little blur at the middle. Use: transition "morph" in compose + MORPH[shot] = (a, b),
# a = (x, y, size) of the thing in the outgoing shot, b = (x, y, size) of the same thing in the incoming shot.
def morph_mix(prev, cur, p, a, b):
    e = eio(clamp(p)); r = b[2] / max(1.0, a[2])
    cx = a[0] + (b[0] - a[0]) * e; cy = a[1] + (b[1] - a[1]) * e
    so = 1 + (r - 1) * e; si = (1 / r) + (1 - 1 / r) * e
    Mo = np.float32([[so, 0, cx - so * a[0]], [0, so, cy - so * a[1]]]); Mi = np.float32([[si, 0, cx - si * b[0]], [0, si, cy - si * b[1]]])
    po = cv2.warpAffine(prev, Mo, (W, H), borderMode=cv2.BORDER_REPLICATE); pi_ = cv2.warpAffine(cur, Mi, (W, H), borderMode=cv2.BORDER_REPLICATE)   # replicate, not reflect: a reflected edge shows a second copy of the scene when the incoming shot starts smaller
    w = eio(clamp((p - 0.12) / 0.7))
    out = po * (1 - w) + pi_ * w
    bl = 7 * math.sin(math.pi * clamp(p))
    if bl > 0.8: out = cv2.GaussianBlur(out, (0, 0), bl)
    return out


# ---------------- KINETIC TYPOGRAPHY that REACTS to the action (ep 29, 9 Nov; SVGator 'kinetic typography guide', Designshack intro, Upskillist 7 principles) ----------------
# Rules: the motion must MEAN something (a word wobbles because it stinks, is blown away by the thing that beats it, shakes because it's loud, falls when it's
# deflated, sneaks in like the sneaky gas); per-letter stagger with an ease-out-back entrance; time it to the voice; keep it readable (big, high contrast, hold it);
# one mode per word, few words per video (if everything moves nothing stands out).
def _kin_glyph(ch, size, col, fnt=None, stroke=0, stroke_col=(46, 32, 26)):
    def mk():
        fn = font(fnt or F_HAND, size * 2); tw = max(size * 0.28, fn.getlength(ch) / 2); w_, h_ = int(tw + 24 + stroke * 2), int(size * 1.5)
        im = Image.new("RGBA", (w_ * 2, h_ * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.text((w_, h_), ch, font=fn, fill=tuple(col) + (255,), anchor="mm", stroke_width=stroke * 2, stroke_fill=tuple(stroke_col) + (255,))
        return el_from(im.resize((w_, h_), Image.LANCZOS)), tw
    return gcache(("kglyph", ch, size, tuple(col), fnt, stroke, tuple(stroke_col)), mk)


def kin_word(f, text, x, y, t, t0, mode="pop", size=130, col=(46, 32, 26), fnt=None, stroke=0, stroke_col=(46, 32, 26), src=None, t1=None,
             amp=1.0, stagger=0.045, track=0.0, wisp_col=None, op=1.0):
    """draw `text` centred at (x, y), letter by letter. Entrance: each letter pops in (ease-out-back) `stagger` s after the previous one, rising 30 px.
    mode: 'pop' (entrance only) | 'stink' (letters bob + sway out of phase, smell wisps rise off them) | 'shake' (vibration = loud / alarm) |
    'blow' (from t1 the letters are pushed away from src=(sx, sy), nearest first, spinning + fading = beaten by something) |
    'drop' (from t1 they fall, bounce once and lie tilted = deflated / busted) | 'sneak' (they tiptoe in sideways from the left, low, one hop each) |
    'breathe' (the whole word swells and shrinks slowly, like lungs)."""
    if t < t0 or op <= 0: return
    gl = [_kin_glyph(ch, size, col, fnt, stroke, stroke_col) for ch in text]
    ws = [g[1] + track for g in gl]; tot = sum(ws); cx = x - tot / 2
    for i, (ch, (el, tw)) in enumerate(zip(text, gl)):
        lx = cx + ws[i] / 2; cx += ws[i]
        if ch == " ": continue
        ti = t0 + i * stagger; q = (t - ti) / 0.22
        if q <= 0: continue
        s = eback(clamp(q)) if q < 1 else 1.0; dy = 30 * (1 - eo(clamp(q))); dx = 0.0; rot = 0.0; o = op * clamp(q * 3)
        if mode == "sneak":
            qq = clamp((t - ti) / 0.45); dx = -260 * (1 - eo(qq)); dy = -40 * math.sin(math.pi * qq) * amp; rot = 8 * (1 - qq); s = 1.0; o = op * clamp(qq * 4)
        if mode == "stink":
            dy += 12 * amp * math.sin(t * 5.2 + i * 0.9); rot = 7 * amp * math.sin(t * 3.7 + i * 1.3); dx = 4 * amp * math.sin(t * 4.1 + i)
        if mode == "shake":
            dx = 6 * amp * math.sin(t * 91 + i * 7); dy += 6 * amp * math.cos(t * 83 + i * 5); rot = 3 * amp * math.sin(t * 67 + i)
        if mode == "breathe":
            s *= 1 + 0.07 * amp * math.sin(t * 2.6)
        if mode == "blow" and t1 is not None and src is not None:
            dd = math.hypot(lx - src[0], y - src[1]) + 1e-3; tb = t1 + 0.0012 * dd
            if t > tb:
                u = t - tb; v = (lx - src[0]) / dd, (y - src[1]) / dd
                dx += v[0] * (900 * u + 1500 * u * u); dy += v[1] * (900 * u + 1500 * u * u) - 200 * u; rot = (1 if v[0] > 0 else -1) * 400 * u; o *= clamp(1 - u / 0.6)
        if mode == "drop" and t1 is not None:
            tb = t1 + i * 0.03
            if t > tb:
                u = t - tb; fy = 900 * u * u
                if fy > 140: u2 = u - math.sqrt(140 / 900); fy = 140 - max(0, 260 * u2 - 900 * u2 * u2)
                dy += fy; rot = (-1) ** i * 18 * clamp(u / 0.5)
        if o > 0.01: rot_comp(f, el, lx + dx, y + dy, rot, s, o, 0.0)
        if mode == "stink" and i % 2 == 0 and t > ti + 0.3:
            wc = wisp_col or (150, 96, 168)
            for j in range(2):
                ph = ((t * 0.9 + i * 0.37 + j * 0.5) % 1.0); bx = lx + dx; by = y - size * 0.55 - 120 * ph
                P = np.array([(bx + 12 * math.sin(k * 0.9 + t * 4 + j * 2) + (j - 0.5) * 22, by - k * 9) for k in range(8)], np.int32)
                cv2.polylines(f, [P], False, C(wc) if op * (1 - ph) > 0.5 else C((210, 186, 220)), 6, cv2.LINE_AA)
