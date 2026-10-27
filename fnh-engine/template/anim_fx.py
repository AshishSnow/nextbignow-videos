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
