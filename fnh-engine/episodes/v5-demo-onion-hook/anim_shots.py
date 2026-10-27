# ================= DEMO (Chubby v2 + cinematic light + M2 voice) built from FreshNestHub 13 — "Why do onions make you cry?" (the onion's booby trap) =================
# COLOUR SCRIPT (ep 13): warm KITCHEN sets (kitchen / yellow / cream / orange) = the everyday moment at your chopping board;
# ONION purple + pale cell green = inside the onion (the trap's rooms); sickly GAS green = the tear factor; TEAR blue = your
# eyes + tears; sky / steel = the scientists; back to warm kitchen for the takeaways.
# CRAFT (ep 13): progressive CHAIN MAP (anim_fx.chain_map) - the reaction CUT > MIX > ACID > GAS > NERVES > TEARS builds one
# link per shot at the bottom (past links dim, current ringed, future = empty slots) and lights up whole for the recap.
# Chubby really chops (2-bone IK grip + knife pivoting at the grip), slow-motion high-speed-camera look for the Cornell study.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "It's") - 0.15, "punch"), ("S1b", T("i2", "And") - 0.1, "zoom"),
    ("S2", T("i3", "Stick") - 0.15, "whip"), ("S3", T("a1", "Here's") - 0.2, "iris"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
# iris match cuts: where the circle opens, in the PREVIOUS shot's picture (a round/central object)
IRIS = {"S3": (720, 1080)}


def lt(t, sid): return t - SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def wui(f, lead, big, t, t0, acc=YEL_, size=170, y=470, out=None, tail=""):   # white caption on dark/colour sets
    ui_word(f, lead, big, y, t, t0, col=WHITE, acc=acc, size=size, shadow=0.5, lead_col=WHITE, out=out, tail=tail)


def rays(f, x, y, r, col, amt, t, nr=14):
    if amt <= 0.01: return
    ov = np.zeros((H, W), np.float32); a0 = t * 0.25
    for i in range(nr):
        a = a0 + i * 2 * math.pi / nr; da = math.pi / nr * 0.5
        pts = np.array([[x, y], [x + r * math.cos(a - da), y + r * math.sin(a - da)], [x + r * math.cos(a + da), y + r * math.sin(a + da)]], np.int32)
        cv2.fillPoly(ov, [pts], 1.0, cv2.LINE_AA)
    ov = cv2.GaussianBlur(ov, (0, 0), 6) * np.clip(1 - np.hypot(_xx - x, _yy - y) / r, 0, 1)
    f += ov[..., None] * np.array(C(col), np.float32) * amt


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / d))


def munch(t, rate=0.42):
    ph = (t / rate) % 1.0
    return (2 if ph < 0.5 else 0), int(t / rate)


def st_(sid): return SHOT[sid]["start"]


# ---------------- shared pieces ----------------
CHAIN = None


def chain_items():
    global CHAIN
    if CHAIN is None:
        CHAIN = [(scale_el(knife_el(), 0.5), "CUT"), (mix_icon_el(), "MIX"), (acid_icon_el(), "ACID"), (gas_el("sly"), "GAS"),
                 (sting_eye_el(), "NERVES"), (drop_el(), "TEARS")]
    return CHAIN


def chain(f, t, cur, t_cur, y=1395):
    chain_map(f, chain_items(), cur, t, t_cur, y=y, gap=146, r=48)


def chop_pose(t, t0, period=0.5, up=1140, down=1250, gx=560):
    """grip point for a vertical chop (fast down, slower up). returns (gx, gy, hit 0..1)."""
    if t < t0: return gx, up, 0.0
    ph = ((t - t0) % period) / period
    gy = up + (down - up) * (eo(ph / 0.35) if ph < 0.35 else 1 - eio((ph - 0.35) / 0.65))
    hit = math.exp(-((ph - 0.35) % 1.0) * 14) if ph >= 0.33 else 0.0
    return gx, gy, hit


def chopper(f, t, x=330, y=1470, s=1.0, period=0.5, t0=0.0, dull=False, ang=-6, gx=560, up=1140, down=1250, expr="happy", mouth=None,
            brow="up", look=(1, 0.4), la=(20, 10)):
    """Chubby holding a knife in his right hand (2-bone IK) and chopping. returns the hit strength (for squash/SFX)."""
    gx, gy, hit = chop_pose(t, t0, period, up, down, gx)
    sh = (x + 118 * s, y - 215 * s - 46 * s)
    a1, a2 = arm_ik(sh, (gx, gy), 76 * s, 70 * s)
    chub(f, x, y, s, la=la, ra=(a1, a2), mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow, look=look)
    knife_at(f, gx, gy, ang, 0.7 * s, dull)
    cv2.circle(f, (int(gx), int(gy)), int(19 * s), C(INK), -1, cv2.LINE_AA); cv2.circle(f, (int(gx), int(gy)), int(14 * s), C(CH_SKIN), -1, cv2.LINE_AA)
    return hit


def board_onion(f, t, x=760, y=1395, s=0.75, os_=0.7, face=False, mood="n", look=(0, 0)):
    comp(f, scale_el(board_el(), s), x - 40, y)
    oy = y - 30 - 126 * os_ / 0.7
    comp(f, scale_el(onion_el(face, mood, look), os_), x, oy)
    return x, oy


def zz(f, x, y, t, n=3, col=WHITE):
    for i in range(n):
        ph = (t * 0.6 + i / n) % 1.0
        comp(f, ed_el("", "Z", "", big_col=col, big_size=int(40 + 30 * ph)), x + 40 * ph + 10 * i, y - 160 * ph, op=math.sin(math.pi * ph))


def shield_el():
    def mk():
        w, h, sc = 220, 260, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        sh = lambda m: m.polygon(S(20, 30, 110, 10, 200, 30, 196, 140, 110, 246, 24, 140), fill=255)
        _outline(im, sh, 11); shape_grad(im, sh, (120, 180, 255), (40, 90, 200))
        d.polygon(S(110, 40, 172, 56, 168, 140, 110, 214, 52, 140, 48, 56), outline=(255, 255, 255, 255), width=6 * sc)
        d.line(S(110, 60, 110, 190), fill=(255, 255, 255, 255), width=8 * sc); d.line(S(66, 110, 154, 110), fill=(255, 255, 255, 255), width=8 * sc)
        return _done(im, w, h)
    return gcache("shield", mk)


def gland(f, x, y, s, lit=0.0):
    cv2.ellipse(f, (int(x), int(y)), (int(46 * s), int(24 * s)), -18, 0, 360, C(INK), -1, cv2.LINE_AA)
    col = tuple(int(a + (b - a) * clamp(lit)) for a, b in zip((255, 160, 180), (120, 210, 255)))
    cv2.ellipse(f, (int(x), int(y)), (int(40 * s), int(18 * s)), -18, 0, 360, C(col), -1, cv2.LINE_AA)


def ring_el():
    def mk():
        w, h, sc = 200, 160, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(10, 10, 190, 150), outline=INK + (255,), width=34 * sc)
        d.ellipse(S(16, 16, 184, 144), outline=(236, 176, 80, 255), width=22 * sc)
        return _done(im, w, h)
    return gcache("oring", mk)


# ---- v2 LOOK (27 Oct owner request): real places with light instead of flat colour circles for story moments; the
# colour-circle stage stays for diagram shots (S3). Kitchen = warm window light; the TRAP = lights drop, red rim + spot;
# the tear-free onion = golden-hour backlight. Big 3D words sit BEHIND the hero (reference: cinematic AI reels).
CTR = 1330                     # counter top in the kitchen shots (Chubby stands behind it, cooking-show framing)
TC = T("i1", "cry...") - 0.1; TP = T("i1", "purpose?") - 0.1


def chop_scene(f, t, x=330, y=1480, s=1.0, period=0.5, t0=0.0, up=1087, down=1197, gx=560, expr="happy", mouth=None, brow="up",
               look=(1, 0.4), face=False, mood_="sly", olook=(-1, -0.3), bx=760):
    gx, gy, hit = chop_pose(t, t0, period, up, down, gx)
    sh = (x + 118 * s, y - 215 * s - 46 * s)
    a1, a2 = arm_ik(sh, (gx, gy), 76 * s, 70 * s)
    chub(f, x, y, s, la=(20, 10), ra=(a1, a2), mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow, look=look)
    counter_front(f, CTR)
    ox, oy = board_onion(f, t, bx, CTR + 12, 0.75, 0.7, face=face, mood=mood_, look=olook)
    knife_at(f, gx, gy, -6, 0.7 * s); grip_hand(f, gx, gy, s)
    return ox, oy, hit


def wcap(f, lead, big, t, t0, acc=YEL_, size=200, out=None, y=470):
    ui_word(f, lead, big, y, t, t0, col=WHITE, acc=acc, size=size, shadow=0.65, lead_col=WHITE, out=out)


# ---- S0: HOOK — Chubby chops an onion in a sunny kitchen; green gas sneaks up; at "cry" his eyes gush; "ON PURPOSE?" ----
def shot_S0(t, n):
    f = set_kitchen(t)
    if t >= TP: title3d(f, "ON PURPOSE?", 560, t, TP, size=210, face=(255, 96, 70), side=(110, 24, 20), depth=22)
    cry = t >= TC
    ox, oy, hit = chop_scene(f, t, expr="wow" if cry else "happy", mouth=3 if cry else munch(t, 0.5)[0], brow="sad" if cry else "up",
                             look=(1, 0.4) if not cry else (0, -0.3), face=t >= TP)
    wisps(f, ox, oy - 110, t, 0.0, 5, 520, 1.0, 0.7)
    k = ramp(t, 0.35, TC - 0.35)
    if t < TC + 0.4:
        gx_, gy_ = ox + (395 - ox) * k, oy - 140 + (1060 - (oy - 140)) * k - 120 * math.sin(math.pi * k)
        gas(f, gx_, gy_, 0.42 + 0.1 * k, t, "sly", op=1.0 - clamp((t - TC) / 0.35))
    hx, hy = head_pos(330, 1480, 1.0)
    if cry: tear_streams(f, hx, hy, 1.0, t, TC, 1.0, 1.0)
    if cry: comp(f, burst_el("CRY?!", TEAR, INK, 56), 700, 760, scale=pin(t, TC + 0.05, 0.22) * (1 - clamp((t - TP + 0.1) / 0.2)))
    if t >= TP: mood(f, (255, 70, 60), 0.22 * ramp(t, TP, 0.4))
    f = cam(f, 1 + 0.02 * t, 540, 1150)
    f = np.ascontiguousarray(f, np.float32)
    wcap(f, "do you know an onion makes you", "[CRY]...", t, 0.1, acc=TEAR, size=210, out=TP - 0.05)
    # after "purpose" the giant 3D title IS the caption (no duplicate text)
    return finish(f, n)


# ---- S1: it's a TRAP! (lights drop; red rim light behind the sly onion; Chubby, unaware, grins in the dark) ----
def shot_S1(t, n):
    u = lt(t, "S1"); tt = T("i2", "trap!") - 0.1
    f = set_kitchen(t) * 0.38
    mood(f, (255, 40, 50), 0.55, 700, 1150, 900)
    if t >= tt: title3d(f, "TRAP!", 930, t, tt, size=360, face=(255, 70, 60), side=(90, 10, 16), depth=28)
    chub(f, 230, 1425, 0.86, la=(20, 10), ra=(70, 40), mouth=0, expr="happy", brow="up", look=(1, 0), hold=scale_el(knife_el(), 0.4), hold_off=(40, -10), hold_front=True)
    counter_front(f, CTR)
    glow(f, 720, 1120, 400, (255, 60, 70), 0.45)
    oel = scale_el(onion_el(True, "sly", (-0.8, 0)), 1.35)
    rot_comp(f, oel, 720, 1170 + 8 * math.sin(t * 3), 4 * math.sin(t * 2), pin(t, st_("S1"), 0.3), 1.0, 0.35)
    light_wrap(f, oel, 720, 1170 + 8 * math.sin(t * 3), (255, 90, 90), 0.5)
    spotlight(f, 640, 1120, 430, 0.55, 300)
    if t < tt + 0.05: wcap(f, "it's a", "", t, st_("S1") + 0.05, acc=YEL_, size=230)
    return finish(f, n, look="night")


# ---- S1b: your knife sets it off (close-up on the board, shallow focus; knife touches -> BOOM, green gas) ----
def shot_S1b(t, n):
    u = lt(t, "S1b"); tk = T("i2", "knife") - 0.05
    f = dof(set_kitchen(t), 9) * 0.55
    counter_front(f, CTR)
    k = ramp(t, st_("S1b"), max(0.2, tk - st_("S1b")))
    if t >= tk: mood(f, GAS, 0.28 * ramp(t, tk, 0.4), 540, 1100, 1000); glow(f, 540, 1100, 520, GAS, 0.35 * ramp(t, tk, 0.3))
    comp(f, scale_el(board_el(), 1.25), 520, CTR + 20)
    comp(f, scale_el(onion_el(True, "sly" if t < tk else "happy"), 1.2), 540, CTR - 190)
    knife_at(f, 700 - 120 * k, 960 + 110 * k, 20, 0.75)
    if t >= tk:
        q = t - tk
        for i in range(7):
            a = 2 * math.pi * i / 7 + 0.4; rr = 120 + 260 * eo(clamp(q / 0.5))
            gas(f, 540 + rr * math.cos(a), CTR - 220 + rr * math.sin(a) * 0.8, 0.45 + 0.1 * (i % 2), t + i, "sly", op=1 - clamp((q - 0.8) / 0.6))
        comp(f, burst_el("BOOM!", YEL_, INK, 64), 540, 800, scale=pin(t, tk, 0.22))
    wcap(f, "and your", "[KNIFE] sets it off", t, st_("S1b") + 0.05, acc=YEL_, size=150)
    return finish(f, n, look="cool")


# ---- S2: open loop — a tear-free onion, back-lit by a golden-hour sun; Chubby amazed; "NO TEARS" behind ----
def shot_S2(t, n):
    u = lt(t, "S2"); tc = T("i3", "can't") - 0.1
    f = set_dusk(t)
    if t >= tc: title3d(f, "NO TEARS", 940, t, tc, size=230, face=(120, 240, 150), side=(20, 90, 50), depth=24)
    cast_shadow(f, 300, 1482, 230, 420, 0.05, 0.4)
    chub(f, 300, 1480, 0.92, la=(20, 10), ra=(150, 175), mouth=talk(t), expr="wow" if t >= tc else "happy", brow="up", look=(1, -0.3))
    oel = scale_el(onion_el(True, "happy"), 0.85)
    oy = 1080 + 10 * math.sin(t * 3)
    rot_comp(f, oel, 720, oy, 5 * math.sin(t * 2), pin(t, st_("S2") + 0.2, 0.3), 1.0, 0.3)
    light_wrap(f, oel, 720, oy, (255, 220, 160), 0.7)
    if t >= tc:
        comp(f, chip("COMING UP", INK, YEL_, 30), 540, 1440, op=clamp((t - tc - 0.3) / 0.3))
        sparkles(f, 720, 1060, t, tc, 12, 220)
    wcap(f, "scientists made an onion that", "[CAN'T]", t, st_("S2") + 0.1, acc=(255, 228, 90), size=220)
    return finish(f, n, look="golden")


# ---- S3: PART 1 — the secret: an onion is made of tiny cells (powers-of-ten push from the onion's rings into its cells) ----
def _s3_far(t):
    f = stage("cream", (255, 240, 220), 540, 1060, 420)
    comp(f, scale_el(onion_half_el(), 1.6), 540, 1060)
    return f


def _s3_near(t):
    f = stage("onion"); cell_grid(f, 540, 1000, 1080, 1200, 170, 80, t, hi=(540 + 85, 1000 + 0))
    return f


def shot_S3(t, n):
    u = lt(t, "S3"); tz = T("a1", "An") - 0.2
    f = zoom_through(t, tz, 0.9, lambda: _s3_far(t), lambda: _s3_near(t), 600, 980, 7.0)
    f = np.ascontiguousarray(f, np.float32)
    chapter_card(f, t, st_("S3") + 0.05, 1, "THE TRAP", y=1400, dur=1.4, col=(255, 200, 240))
    if t >= tz + 0.9:
        label_at(f, "ONE CELL", 820, 1260, t, tz + 1.0, 660, 1040, bg=INK)
        comp(f, chip("MAGNIFIED", YEL_, INK, 26), 540, 1440, op=clamp((t - tz - 1.1) / 0.3))
    if t < tz + 0.5: ui_word(f, "here's the", "[SECRET]", 470, t, st_("S3") + 0.1, col=INK, acc=RED_, size=220, out=tz + 0.4)
    else: ui_word(f, "an onion is made of tiny", "[CELLS]", 470, t, tz + 0.5, col=INK, acc=(150, 40, 140), size=210)
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TC, 0.45, 20), (TP, 0.3, 12), (T("i2", "trap!") - 0.1, 0.35, 16), (T("i2", "knife") - 0.05, 0.5, 24), (T("i3", "can't") - 0.1, 0.3, 12),
           (T("a1", "An") + 0.6, 0.25, 10)]


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    f = RENDER[sid](tt, n).astype(np.float32)
    dx = dy = 0.0; z = 1.0
    for ti, d, a in IMPACTS:
        if s["start"] - 0.05 <= ti < s["end"] and ti <= tt < ti + d:
            k = 1 - (tt - ti) / d; dx += a * k * math.sin(tt * 97); dy += a * k * math.cos(tt * 83); z += 0.03 * k
    if dx or dy or abs(z - 1) > 1e-4: f = cam(f, z, W / 2, H / 2, dx, dy)
    return f


def _bl(x, s_):
    if s_ < 0.5: return x
    sm = cv2.resize(x, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    return cv2.resize(cv2.GaussianBlur(sm, (0, 0), s_ / 4), (W, H), interpolation=cv2.INTER_LINEAR)


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; f = rs(sh["id"], t, n); k = sh["trans"]; dt = t - sh["start"]
    if i > 0:
        if k == "focus" and dt < 0.34:
            p = dt / 0.34; prv = rs(SHOTS[i - 1]["id"], t, n); m = eio(p)
            f = _bl(prv, 40 * m) * (1 - m) + _bl(f, 40 * (1 - m)) * m
        elif k == "iris" and dt < 0.42:
            cx, cy = IRIS.get(sh["id"], (540, 1000))
            f = iris_mix(rs(SHOTS[i - 1]["id"], t, n), f, dt / 0.42, cx, cy)
        elif k == "whip" and dt < 0.22:
            p = 1 - dt / 0.22; M = np.float32([[1, 0, -360 * p * p], [0, 1, 0]])
            f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
        elif k == "zoom" and dt < 0.2:
            p = 1 - dt / 0.2; acc = np.zeros_like(f)
            for q in range(5): acc += cam(f, 1 + 0.06 * q * p)
            f = acc / 5
        elif k == "flash" and dt < 0.14: f = f + 0.8 * (1 - dt / 0.14) ** 1.5
        elif k == "punch" and dt < 0.16: f = cam(f, 1 + 0.08 * (1 - dt / 0.16)) + 0.12 * (1 - dt / 0.16)
    nx = SHOTS[i + 1] if i + 1 < len(SHOTS) else None
    if nx is not None and nx["trans"] == "whip" and sh["end"] - t < 0.14:
        p = 1 - (sh["end"] - t) / 0.14; M = np.float32([[1, 0, 360 * p * p], [0, 1, 0]])
        f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
