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
        "hold_up": dict(la=(40, 30), ra=(150, 175), lean=5), "arms_out": dict(la=(96, 60), ra=(96, 60)), "tada": dict(la=(120, 150), ra=(160, 150), lean=6)}


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
