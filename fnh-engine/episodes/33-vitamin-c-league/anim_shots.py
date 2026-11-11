# ================= shots: FreshNestHub 33 — "Which foods have more vitamin C than an orange?" (Chubby INK, ep 14 of the ink look) ===
# COLOUR SCRIPT: VITAMIN-C ORANGE (ACC) = vitamin C only (the bar, every mg number, the vitamin C buddies, the leaderboard bars, titles). The foods keep their
# own colours. Story = lit places (NEW: THE STADIUM, a sunny athletics ground with a crowd that does a wave; the morning worktop; the stove); every explanation
# = the white BOARD. METAPHOR for the whole video: a HIGH JUMP where the height cleared = mg of vitamin C per 100 g (the orange sets the bar).
# NO music bed (owner 9 Nov). Craft skill (sound): PLACE THE FOLEY IN THE ROOM (per-place reverb send + pan by screen x), see mix.py.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "top") - 0.12, "punch"),
    ("S1", T("i2", "Your") - 0.12, "erase"), ("S1b", T("i2", "and") - 0.1, "whip"),
    ("S2", T("i3", "So") - 0.1, "whip"), ("S2b", T("i3", "and") - 0.1, "punch"),
    ("S3", T("a0", "Fair") - 0.12, "whip"), ("S3b", T("a0", "Every") - 0.1, "punch"),
    ("S4", T("a1", "The") - 0.1, "whip"), ("S4b", T("a1", "Thats") - 0.1, "punch"),
    ("S5", T("a2", "First") - 0.12, "whip"),
    ("S6", T("a3", "Fifty-three") - 0.15, "punch"), ("S6b", T("a3", "Sour") - 0.12, "erase"),
    ("S7", T("b0", "Papaya") - 0.12, "whip"),
    ("S8", T("b1", "But") - 0.1, "flash"),
    ("S9", T("b2", "Red") - 0.1, "punch"), ("S9b", T("b2", "Thats") - 0.1, "erase"),
    ("S10", T("c0", "Then") - 0.12, "whip"),
    ("S10b", T("c1", "Thats") - 0.12, "erase"),
    ("S11", T("c1", "And") - 0.1, "whip"), ("S11b", T("c1", "so") - 0.1, "erase"),
    ("S12", T("c2", "So") - 0.12, "erase"),
    ("S13", T("d0", "And") - 0.12, "flash"), ("S13b", T("d0", "green") - 0.15, "punch"),
    ("S14", T("d1", "The") - 0.12, "whip"), ("S14b", T("d1", "You") - 0.1, "punch"), ("S14c", T("d1", "so") - 0.1, "erase"),
    ("S15", T("e0", "One") - 0.12, "flash"), ("S15b", T("e0", "Vitamin") - 0.12, "erase"),
    ("S16", T("e1", "So") - 0.12, "whip"), ("S16b", T("e1", "or") - 0.1, "punch"),
    ("S17", T("e2", "Steaming") - 0.12, "erase"), ("S17b", T("e2", "And") - 0.1, "whip"),
    ("S18", T("f0", "So") - 0.12, "erase"),
    ("S19", T("f1", "Save") - 0.1, "whip"), ("S20", T("f1", "and") - 0.12, "whip"),
]

SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
MORPH = {}
_write_on0 = write_on


def write_on(f, text, x, y, t, t0, size=56, col=BP_INK, cps=22.0, op=1.0):
    """phone-size hand lettering (ep 27: the kit default reads too small)."""
    _write_on0(f, text, x, y, t, t0, int(size * 1.3), col, cps, op)


def st_(sid): return SHOT[sid]["start"]


def en_(sid): return SHOT[sid]["end"]


def ui_word(f, lead, big, y, t, t0, col=INKC, acc=ACC, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


def t3(f, text, y, t, t0, size=200, face=None, side=None, x=540):
    if t >= t0: title_ink(f, text, y, t, t0, size=size, face=face or ACC_L, side=side or ACC_S, depth=18, x=x)


def nolean(p): return {k: v for k, v in p.items() if k != "lean"}


def src(f, text, t, t0, y=1462):
    if t >= t0: comp(f, chip(text, INKC, MILK, 22), 540, y, op=clamp((t - t0) / 0.2))


def cc(f, text, x, y, t, t0, bg=None, fg=None, size=34):
    if t >= t0: comp(f, chip(text, bg or INKC, fg or MILK, size), x, y, scale=pin(t, t0))


def kw(f, text, x, y, t, t0, mode="pop", size=130, col=None, **k):
    """kinetic word in hand lettering with an ink stroke (anim_fx.kin_word)."""
    kin_word(f, text, x, y, t, t0, mode, size, col or ACC_S, stroke=2, stroke_col=INKC, **k)


def el_at(f, el, x, y, s=1.0, t=None, t0=None, rot=0.0, op=1.0):
    """place an element; with t/t0 it snaps in (4-frame overshoot)."""
    k = 1.0 if t0 is None else (snap(t, t0, 4) if t >= t0 else 0.0)
    if k > 0.01: rot_comp(f, scale_el(el, s), x, y, rot, k, op, 0.0)


def stamp_x(f, x, y, r, k, col=(176, 40, 44), w=22):
    for sg in (-1, 1): cv2.line(f, (int(x - r * k), int(y - sg * r * k)), (int(x + r * k), int(y + sg * r * k)), C(col), w, cv2.LINE_AA)


def tick(f, x, y, r, k, col=None, w=22):
    col = col or INK_MINT_S
    P = [(x - r, y), (x - r * 0.3, y + r * 0.7), (x + r, y - r * 0.8)]
    draw_on(f, P, k, col, w, seed=5, tip=False)


def peek(f, t, x, y, s, expr="sus", look=(0, 0), brow=None, mouth=None):
    s = s * 1.7
    chub_head_only(f, x, y, s, t, mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow or ("sus" if expr == "sus" else "up"), look=look, turn=clamp(look[0]) * 0.5)


def ref(f, x, y, s, t, pose="idle", whistle=False, clip=False, **k):
    """Chubby as the REFEREE: a striped black-and-white shirt, a whistle on a cord, an optional clipboard (other kwargs go to chub)."""
    p = dict(POSE[pose]); p.update(k)
    chub(f, x, y, s, t=t, shirt=(244, 244, 240), **p)
    for j in range(4):                                                           # the stripes on the referee shirt (over the torso)
        xx = x - 70 * s + j * 46 * s
        cv2.line(f, (int(xx), int(y - 330 * s)), (int(xx), int(y - 175 * s)), C((52, 48, 46)), max(3, int(14 * s)), cv2.LINE_AA)
    cv2.line(f, (int(x - 30 * s), int(y - 360 * s)), (int(x), int(y - 300 * s)), C(INKC), max(2, int(3 * s)), cv2.LINE_AA)
    cv2.line(f, (int(x + 30 * s), int(y - 360 * s)), (int(x), int(y - 300 * s)), C(INKC), max(2, int(3 * s)), cv2.LINE_AA)
    if not whistle: el_at(f, whistle_el(), x, y - 296 * s, 0.6 * s)
    if clip: el_at(f, clip_el(), x - 150 * s, y - 250 * s, 0.75 * s, rot=8)


def bubble_cloud(f, x, y, w, h, k=1.0):
    """a thought bubble (cloud + two trailing dots toward the bottom-left)."""
    if k <= 0: return
    for i in range(10):
        a = 2 * math.pi * i / 10; px, py = x + w * 0.42 * math.cos(a) * k, y + h * 0.4 * math.sin(a) * k
        cv2.circle(f, (int(px), int(py)), int(h * 0.3 * k), C(INKC), 6, cv2.LINE_AA)
    for i in range(10):
        a = 2 * math.pi * i / 10; px, py = x + w * 0.42 * math.cos(a) * k, y + h * 0.4 * math.sin(a) * k
        cv2.circle(f, (int(px), int(py)), int(h * 0.3 * k) - 3, C(MILK), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(x), int(y)), (int(w * 0.42 * k), int(h * 0.42 * k)), 0, 0, 360, C(MILK), -1, cv2.LINE_AA)
    for r_, dx, dy in ((26, -w * 0.38, h * 0.62), (16, -w * 0.5, h * 0.85)):
        cv2.circle(f, (int(x + dx), int(y + dy)), int(r_ * k), C(MILK), -1, cv2.LINE_AA); cv2.circle(f, (int(x + dx), int(y + dy)), int(r_ * k), C(INKC), 5, cv2.LINE_AA)


GROUND = 1440


def jump_shot(f, t, kind, t0, mg, s=0.75, x0=250, x1=700, dur=1.05, bar=None, mood_air="wow", mood_land="happy", px=None, **k):
    """one food clears `mg` on the rig: runs in, crouches, arcs over (in front of the bar while rising, behind it while falling), lands on the mat."""
    px = px or PX_MG
    peak = GROUND - mg * px - 40 * s
    j = jump_xy(t, t0, x0, x1, GROUND, peak, dur)
    if j["phase"] == "wait":                                                     # the run-up from the left edge
        q = clamp(1 - (t0 - t) / 0.9); xr = x0 - 260 * (1 - q)
        draw = lambda: athlete(f, kind, xr, GROUND, s, t, "n", (1, 0), run=1.0 if q < 1 else 0.0, **k)
        behind = False
    else:
        land = j["phase"] == "land"
        mood = mood_land if land else (mood_air if j["phase"] == "air" else "n")
        yy = j["y"] if not land else GROUND - 70 * s
        draw = lambda: athlete(f, kind, j["x"], yy, s, t, mood, (0, -0.5 if j["phase"] == "air" else 0), tuck=j["tuck"], rot=j["rot"], sq=j["sq"], **k)
        behind = j["phase"] == "land" or (j["phase"] == "air" and (t - t0 - 0.18) / dur > 0.5)
    if behind: draw()
    by = hj_rig(f, bar=bar, t=t, mat=True, px=px)
    if not behind: draw()
    return j


def num(f, v, y, t, t0, size=220, x=540, unit=" mg"):
    """the big mg number for a jump (counts up with the jump), ink block title in the accent."""
    if t >= t0: t3(f, f"{v}{unit}", y, t, t0, size, x=x)


def scoreline(f, x, y, label, mg, k, col=None, w=170, maxmg=242, hgt=900, base=1300, hl=False, shownum=True):
    """a vertical board bar (for 'A vs B' comparisons): grows to mg, label under it, number on top."""
    h = int(hgt * mg / maxmg * k)
    poly = [(x - w // 2, base - h), (x + w // 2, base - h), (x + w // 2, base), (x - w // 2, base)]
    if h > 2:
        cv2.fillPoly(f, [np.array(poly, np.int32)], C(col or (ACC if hl else ACC_L)), cv2.LINE_AA)
        hatch_on(f, poly, 1.0, ACC_S, 14, 45, 3, 0.55)
        cv2.polylines(f, [np.array(poly, np.int32)], True, C(INKC), 5, cv2.LINE_AA)
        if shownum: write_on(f, str(int(round(mg * k))), x, base - h - 34, 99, 0, 62, ACC_S if hl else INKC, 99)
    write_on(f, label, x, base + 76, 99, 0, 50, INKC, 99)


# ---- S0: HOOK at frame 0: the morning worktop, Chubby holds up the ORANGE like a trophy, it wears a crown; moving words ask the question ----
def shot_S0(t, n):
    f = set_worktop(t); kt = T("i1", "close") - 0.25
    k = take(t, kt)
    if t < kt:
        chub(f, 540, 1500, 1.1, t=t, **nolean(POSE["hold_up"]), mouth=talk(t), expr="happy", brow="up", look=(0.4, -0.6), lean=3 + 2 * math.sin(t * 4), hand_r="open")
        el_at(f, food_el("orange", "happy", (0, 0.4), crown=True), 700, 780 + 8 * math.sin(t * 6), 1.05, rot=6 * math.sin(t * 3))
    else:
        chub(f, 540, 1500 + k["dy"], 1.1, t=t, **nolean(POSE["shock"]), mouth="jaw", expr=k["expr"], brow=k["brow"], look=(0.6, -0.4), lean=k["lean"], squash=k["squash"])
        el_at(f, food_el("orange", "wow", (0, -0.4)), 700, 800, 1.05)
        q = ramp(t, kt, 0.6)                                                    # the guava flies in and knocks the crown away
        el_at(f, food_el("guava", "angry", (-1, 0)), 1100 - 380 * min(1, q * 1.6), 650 + 80 * q, 0.8, rot=-30 * q)
        rot_comp(f, scale_el(crown_el(), 0.9), 700 + 300 * q, 640 - 260 * math.sin(math.pi * min(q, 1)) + 500 * max(0, q - 0.6), 400 * q, 1.0, 1.0)
    worktop_front(f, 1330)
    kw(f, "ORANGE =", 540, 330, t, 0.0, "shake", 130, col=ORA_S, amp=0.5)
    kw(f, "VITAMIN C KING?", 540, 480, t, 0.35, "pop", 110, col=INKC)
    return finish(f, n, look="golden")


# ---- S0b: '...top for vitamin C?' the crown lands on the counter, the orange sulks, the guava smirks: NOT EVEN CLOSE ----
def shot_S0b(t, n):
    f = set_worktop(t); t0 = st_("S0b"); f = dof(f, 3)
    el_at(f, food_el("orange", "sad", (0.6, 0.4)), 330, 1150, 1.25)
    el_at(f, food_el("guava", "happy", (-0.6, 0), crown=t > t0 + 0.6), 760, 1120, 1.25, t, t0 + 0.05)
    worktop_front(f, 1330)
    if t < t0 + 0.6:
        q = ramp(t, t0, 0.6); rot_comp(f, scale_el(crown_el(), 1.0), 560 + 200 * q, 700 + 260 * q - 200 * math.sin(math.pi * q), 300 * q, 1.0, 1.0)
    kw(f, "NOT EVEN", 540, 330, t, t0 + 0.05, "shake", 120, col=INKC, amp=0.4)
    kw(f, "CLOSE", 540, 480, t, t0 + 0.3, "pop", 150, col=ACC_S)
    return finish(f, n, look="golden")


# ---- S1: 'Your body can't make vitamin C, so all of it has to come from food,' BOARD: a body outline, a crossed-out factory inside, foods -> mouth ----
def shot_S1(t, n):
    f = board_bg(); t0 = st_("S1"); tf = T("i2", "food") - 0.4
    cx, hy = 540, 640
    draw_ell_on(f, cx, hy, 110, 120, ramp(t, t0, 0.4), BP_INK, 7, seed=11)
    for sg in (-1, 1):
        P = [(cx + sg * 40, hy + 116), (cx + sg * 44, hy + 160), (cx + sg * 170, hy + 196), (cx + sg * 196, hy + 270), (cx + sg * 186, hy + 650)]
        draw_on(f, P, ramp(t, t0 + 0.3, 0.5), BP_INK, 7, seed=12 + sg, tip=sg > 0)
    tk = T("i2", "make") - 0.1                                                  # a little factory in the belly, crossed out on 'can't make'
    if t > t0 + 0.6:
        poly = [(450, 1080), (450, 960), (500, 1000), (500, 960), (550, 1000), (550, 940), (600, 940), (600, 1080)]
        draw_on(f, poly + [poly[0]], ramp(t, t0 + 0.6, 0.4), BP_INK, 6, seed=14, tip=False)
        el_at(f, vitc_el("n"), 640, 1010, 0.6, t, t0 + 0.9)
        stamp_x(f, 540, 1010, 120, ramp(t, tk + 0.2, 0.25))
    write_on(f, "can't make it", 540, 1250, t, tk + 0.3, 44, (176, 40, 44))
    if t > tf:                                                                  # foods slide in from both sides toward the mouth
        for i, (kd, sx, sy) in enumerate((("orange", 150, 420), ("guava", 930, 420), ("capsicum", 140, 860), ("lemon", 940, 860))):
            q = ramp(t, tf + 0.1 * i, 0.6); x = sx + (cx - sx) * 0.35 * q; y = sy + (hy + 40 - sy) * 0.35 * q
            el_at(f, food_el(kd, "happy"), x, y, 0.72, t, tf + 0.1 * i)
            draw_arrow_on(f, (x + (cx - x) * 0.3, y + (hy + 40 - y) * 0.3), (cx + (x - cx) * 0.25, hy + 40 + (y - hy - 40) * 0.25), ramp(t, tf + 0.25 + 0.1 * i, 0.3), ACC_S, 6, 20)
        write_on(f, "food", 540, 360, t, tf + 0.1, 60, ACC_S)
    return finish(f, n, look="fresh")


# ---- S1b: '...and everyone thinks orange.' worktop: Chubby daydreams, a thought bubble pops with a glowing orange ----
def shot_S1b(t, n):
    f = set_worktop(t); t0 = st_("S1b"); to = T("i2", "orange") - 0.3
    chub(f, 420, 1500, 1.15, t=t, **nolean(POSE["think"]), mouth=talk(t), expr="happy", brow="up", look=(0.5, -0.8), lean=-5 + 2 * math.sin(t * 2))
    worktop_front(f, 1330)
    k = snap(t, t0 + 0.15, 5) if t > t0 + 0.15 else 0
    bubble_cloud(f, 720, 640, 420, 300, k)
    if t > to:
        glow(f, 720, 630, 170, (255, 214, 140), 0.35)
        el_at(f, food_el("orange", "happy", (0, 0), crown=True), 720, 650, 0.85, t, to)
    kw(f, "ORANGE!", 540, 330, t, to, "pop", 130, col=ORA_S)
    return finish(f, n, look="golden")


# ---- S2: 'So let's test it. Six everyday foods, one high jump,' NEW PLACE: the STADIUM. Six athletes line up, the crowd does a wave ----
KINDS = ["orange", "lemon", "papaya", "capsicum", "guava", "chilli"]


def shot_S2(t, n):
    t0 = st_("S2"); f = set_stadium(t, wave=T("i3", "Six") - 0.4)
    ts = T("i3", "Six") - 0.15
    ref(f, 900, 1640, 0.85, t, "point", clip=True, mouth=talk(t), expr="happy", brow="up", look=(-1, 0))
    for i, kd in enumerate(KINDS):
        tt = ts + 0.12 * i
        if t >= tt:
            hop = max(0.0, math.sin(min(1.0, (t - tt) / 0.3) * math.pi)) * 50
            athlete(f, kd, 110 + 136 * i, 1500 - hop - (i % 2) * 70, 0.68, t + i, "happy", (0, -0.3), crown=(kd == "orange"))
    cc(f, "6 EVERYDAY FOODS", 540, 330, t, ts, INKC, MILK, 44)
    t3(f, "HIGH JUMP", 520, t, T("i3", "jump") - 0.15, 150)
    return finish(f, n, look="golden")


# ---- S2b: '...and the orange sets the bar.' the bar slides down the uprights and stops where the orange can clear it; the ref blows the whistle ----
def shot_S2b(t, n):
    t0 = st_("S2b"); f = set_stadium(t); tb = T("i3", "bar") - 0.3
    mg = 250 - (250 - 53) * ramp(t, t0 + 0.1, max(0.4, tb - t0 - 0.1))
    hj_rig(f, bar=mg, t=t)
    athlete(f, "orange", 760, 1600, 0.75, t, "smirk" if t > tb else "n", (-1, -0.4), crown=True)
    ref(f, 260, 1640, 0.8, t, "whisper", whistle=True, mouth="o" if t > tb else 0, expr="n", brow="up", look=(1, -0.2))
    if t > tb:
        for j in range(3): cv2.line(f, (int(330 + j * 4), int(1290 - 30 * j)), (int(400 + 30 * j), int(1260 - 40 * j)), C(INKC), 5, cv2.LINE_AA)
        cc(f, "THE BAR", 540, 1150, t, tb, ACC, INKC, 40)
    return finish(f, n, look="golden")


# ---- S3: 'Fair rules first.' close: the referee holds up the clipboard RULES; S3b: '...same weight, a hundred grams.' each food on the scale: 100 g ----
def shot_S3(t, n):
    t0 = st_("S3"); f = set_stadium(t); f = dof(f, 5)
    ref(f, 540, 1700, 1.25, t, "hold_up", mouth=talk(t), expr="sus", brow="sus", look=(0, -0.3))
    el_at(f, clip_el(), 760, 760, 1.4, t, t0 + 0.1, rot=-6)
    kw(f, "FAIR RULES", 540, 360, t, t0 + 0.1, "pop", 130, col=INKC)
    return finish(f, n, look="golden")


def shot_S3b(t, n):
    t0 = st_("S3b"); f = set_stadium(t); f = dof(f, 4); th = T("a0", "hundred") - 0.2
    el_at(f, scale_ink_el("100 g" if t > th else "---"), 540, 1240, 1.6)
    per = max(0.35, (th - t0) / 6)
    i = min(5, int((t - t0) / per)); kd = KINDS[i]; q = ((t - t0) % per) / per
    yy = 1050 - 160 * max(0, 1 - q * 4) ** 2
    el_at(f, food_el(kd, "happy" if t > th else "n", (0, 0.6)), 540, yy, 0.95)
    kw(f, "SAME WEIGHT", 540, 360, t, T("a0", "same") - 0.15, "pop", 120, col=INKC)
    if t > th: t3(f, "100 g", 560, t, th, 190)
    return finish(f, n, look="golden")


# ---- S4: 'The orange clears fifty-three milligrams.' THE FIRST JUMP; S4b: 'That's the bar to beat.' the bar locks at 53 ----
def shot_S4(t, n):
    t0 = st_("S4"); f = set_stadium(t); tj = T("a1", "clears") - 0.35
    j = jump_shot(f, t, "orange", tj, 53, 1.1, x0=230, x1=740, bar=53, px=7.0, crown=True)
    if t > tj + 0.4: num(f, count_up(t, tj + 0.4, 53, 0.6), 400, t, tj + 0.4, 200)
    cc(f, "per 100 g", 540, 560, t, tj + 0.6, INKC, MILK, 34)
    return finish(f, n, look="golden")


def shot_S4b(t, n):
    t0 = st_("S4b"); f = set_stadium(t)
    y = hj_rig(f, bar=53, t=t, px=7.0)
    for x in range(200, 900, 40): cv2.line(f, (x, int(y - 40)), (x + 20, int(y - 40)), C(ACC_S), 5, cv2.LINE_AA)
    athlete(f, "orange", 760, 1340, 0.9, t, "smirk", (-1, 0), crown=True)
    f = crash_zoom(f, t, T("a1", "bar") - 0.1, 1.15, 540, 1100)
    t3(f, "THE BAR: 53", 420, t, t0 + 0.1, 150)
    src(f, SRC_USDA, t, t0 + 0.3)
    return finish(f, n, look="golden")


# ---- S5: 'First up, the lemon. It's so sour, it's got to win, right?' the lemon at the start line, Chubby pulls a sour face ----
def shot_S5(t, n):
    t0 = st_("S5"); f = set_stadium(t); ts = T("a2", "sour") - 0.2
    hj_rig(f, bar=53, t=t, px=7.0)
    sour = t > ts
    ref(f, 300, 1700, 1.0, t, "cheek" if sour else "point", mouth=talk(t), expr="gross" if sour else "happy", brow="sad" if sour else "up", look=(1, 0))
    athlete(f, "lemon", 760, 1640, 0.95, t, "smirk" if t > T("a2", "win") - 0.2 else "happy", (-1, -0.3))
    if sour: kw(f, "SO SOUR", 540, 340, t, ts, "shake", 120, col=LEM_S, amp=0.7)
    if t > T("a2", "right") - 0.3: kw(f, "= WINNER?", 540, 490, t, T("a2", "right") - 0.3, "pop", 110, col=INKC)
    return finish(f, n, look="golden")


# ---- S6: 'Fifty-three. Exactly the same as the orange.' the lemon jumps, brushes the bar at exactly 53: TIE ----
def shot_S6(t, n):
    t0 = st_("S6"); f = set_stadium(t); tj = t0 + 0.02
    jump_shot(f, t, "lemon", tj, 53, 1.1, x0=230, x1=740, bar=53, px=7.0, mood_land="sus")
    if t > tj + 0.5: num(f, count_up(t, tj + 0.5, 53, 0.5), 400, t, tj + 0.5, 200)
    ts = T("a3", "same") - 0.2
    if t > ts:
        el_at(f, food_el("orange", "sus", (1, 0), crown=True), 200, 1180, 0.7, t, ts)
        el_at(f, vstamp_el("TIE", ACC_S, 90), 540, 600, 1.0, t, ts, rot=-8)
    return finish(f, n, look="golden")


# ---- S6b: 'Sour doesn't mean more vitamin C.' BOARD: two meters per fruit: SOUR (lemon way higher) vs VITAMIN C (level) ----
def shot_S6b(t, n):
    f = board_bg(); t0 = st_("S6b")
    for i, (kd, sour) in enumerate((("orange", 0.35), ("lemon", 0.95))):
        x = 300 + 480 * i
        el_at(f, food_el(kd, "n" if kd == "orange" else "gross"), x, 560, 1.15, t, t0 + 0.1 + 0.15 * i)
        ks = ramp(t, t0 + 0.4, 0.6); kv = ramp(t, T("a3", "more") - 0.3, 0.5)
        for j, (lab, v, col) in enumerate((("sour", sour, LEM), ("vit C", 0.5, ACC))):
            xx = x - 85 + 170 * j; base = 1340; h = int(560 * v * (ks if j == 0 else kv))
            poly = [(xx - 62, base - h), (xx + 62, base - h), (xx + 62, base), (xx - 62, base)]
            cv2.rectangle(f, (xx - 62, base - 560), (xx + 62, base), C(BP_INK), 4, cv2.LINE_AA)
            if h > 2: cv2.fillPoly(f, [np.array(poly, np.int32)], C(col), cv2.LINE_AA); hatch_on(f, poly, 1.0, INKC, 14, 45, 3, 0.4)
            write_on(f, lab, xx, base + 70, 99, 0, 44, INKC, 99)
    if t > T("a3", "more") - 0.1: write_on(f, "sour isn't more C", 540, 340, t, T("a3", "more") - 0.1, 54, ACC_S)
    return finish(f, n, look="fresh")


# ---- S7: 'Papaya, sixty-one. Just over the bar. Okay, not bad at all.' the papaya clears, the bar barely wobbles ----
def shot_S7(t, n):
    t0 = st_("S7"); f = set_stadium(t); tj = t0 + 0.05
    to = T("b0", "over") - 0.2
    wob = 14 * math.exp(-(t - to) * 4) * math.sin((t - to) * 30) if t > to else 0
    j = jump_shot(f, t, "papaya", tj, 61, 1.1, x0=230, x1=740, bar=53 if t < to else 61, px=7.0, mood_land="happy")
    if t > tj + 0.5: num(f, count_up(t, tj + 0.5, 61, 0.5), 400, t, tj + 0.5, 200)
    if t > T("b0", "Okay") - 0.2:
        ref(f, 930, 1800, 0.75, t, "present", mouth=talk(t), expr="smirk", brow="up", look=(-1, -0.3))
        kw(f, "not bad", 540, 560, t, T("b0", "Okay") - 0.2, "pop", 100, col=INKC)
    return finish(f, n, look="golden")


# ---- S8: 'But wait till you see who's next, because it isn't even a fruit.' the lights go down, a spotlight on a mystery silhouette ----
def shot_S8(t, n):
    t0 = st_("S8"); f = set_stadium(t, dim=ramp(t, t0, 0.4))
    hj_rig(f, bar=61, t=t, px=7.0)
    spotlight(f, 540, 1250, 300, 0.75 * ramp(t, t0 + 0.2, 0.4), 110)
    sil = food_el("capsicum", None); pm, a = scale_el(sil, 1.3)
    shake = 4 * math.sin(t * 40) if t > T("b1", "fruit") - 0.3 else 0
    rot_comp(f, (np.zeros_like(pm) + np.array(C((30, 26, 30)), np.float32) * a[..., None], a), 540 + shake, 1230, 0, 1.0, 1.0)
    el_at(f, food_el("orange", "wow", (0.6, 0.3), crown=True), 190, 1380, 0.75)
    el_at(f, food_el("guava", "sus", (-0.6, 0.3)), 890, 1380, 0.75)
    kw(f, "?", 540, 900, t, t0 + 0.4, "pop", 220, col=ACC_L)
    if t > T("b1", "fruit") - 0.35: kw(f, "NOT A FRUIT", 540, 380, t, T("b1", "fruit") - 0.35, "shake", 120, col=ACC_L, amp=0.6)
    return finish(f, n, look="night")


# ---- S9: 'Red capsicum! A hundred and twenty-eight.' the lights slam on, the capsicum bursts out and leaps way over ----
def shot_S9(t, n):
    t0 = st_("S9"); f = set_stadium(t, wave=t0 + 0.6); tj = t0 + 0.25
    j = jump_shot(f, t, "capsicum", tj, 128, 1.0, x0=300, x1=720, bar=61 if t < tj + 0.6 else 128, mood_land="smirk")
    if t > tj + 0.5: num(f, count_up(t, tj + 0.5, 128, 0.7), 400, t, tj + 0.5, 210)
    confetti(f, t, tj + 1.2, 40, 9)
    return finish(f, n, look="golden")


# ---- S9b: 'That's more than double the orange.' BOARD: orange 53 vs capsicum 128, x2 ----
def shot_S9b(t, n):
    f = board_bg(); t0 = st_("S9b"); k = ramp(t, t0 + 0.15, 0.6)
    scoreline(f, 330, 0, "orange", 53, k); scoreline(f, 750, 0, "capsicum", 128, ramp(t, t0 + 0.4, 0.7), hl=True)
    el_at(f, food_el("orange", "sad"), 330, 1300 - int(900 * 53 / 242 * k) - 210, 0.9)
    el_at(f, food_el("capsicum", "happy"), 750, 1300 - int(900 * 128 / 242 * ramp(t, t0 + 0.4, 0.7)) - 210, 0.9)
    kw(f, "MORE THAN x2", 540, 380, t, T("b2", "double") - 0.2, "pop", 130, col=ACC_S)
    return finish(f, n, look="fresh")


# ---- S10: 'Then the guava steps up, and it clears two hundred and twenty-eight.' the big one: the camera follows it up, the crowd does a wave ----
def shot_S10(t, n):
    t0 = st_("S10"); f = set_stadium(t, wave=T("c0", "clears")); tj = T("c0", "clears") - 0.45
    if t < tj - 0.9:                                                            # steps up: a swagger to the line
        athlete(f, "guava", 300, GROUND, 1.0, t, "smirk", (1, -0.2), run=0.5)
        hj_rig(f, bar=128, t=t)
    else:
        jump_shot(f, t, "guava", tj, 228, 1.0, x0=300, x1=720, dur=1.25, bar=128 if t < tj + 0.7 else 228, mood_land="love")
    if t > tj + 0.6: num(f, count_up(t, tj + 0.6, 228, 0.8), 360, t, tj + 0.6, 220)
    confetti(f, t, tj + 1.5, 50, 4)
    return finish(f, n, look="golden")


# ---- S10b: 'That's more than four times the orange.' BOARD: four oranges stacked on one side, one guava on the other ----
def shot_S10b(t, n):
    f = board_bg(); t0 = st_("S10b"); tf = T("c1", "four") - 0.25
    draw_on(f, [(540, 640), (540, 1340)], ramp(t, t0, 0.3), BP_INK, 5, seed=3, tip=False)
    el_at(f, food_el("guava", "happy"), 790, 1000, 1.7, t, t0 + 0.1)
    write_on(f, "228", 790, 1330, t, t0 + 0.3, 70, ACC_S)
    for i in range(4):
        el_at(f, food_el("orange", "n"), 290, 1220 - i * 175, 0.82, t, tf - 0.25 + 0.12 * i)
    write_on(f, "53 x 4", 290, 1380, t, tf + 0.2, 56, INKC)
    kw(f, "x4", 540, 420, t, tf, "pop", 190, col=ACC_S)
    return finish(f, n, look="fresh")


# ---- S11: '...one guava weighs about fifty-five grams,' worktop: Chubby puts ONE guava on the kitchen scale: 55 g ----
def shot_S11(t, n):
    f = set_worktop(t); t0 = st_("S11"); tg = T("c1", "fifty-five") - 0.2
    chub(f, 330, 1500, 1.05, t=t, **nolean(POSE["present"]), mouth=talk(t), expr="happy", brow="up", look=(1, 0.4), hand_r="open")
    worktop_front(f, 1330)
    el_at(f, scale_ink_el("55 g" if t > tg else "0 g"), 740, 1230, 1.05)
    yy = 1080 - 240 * (1 - ramp(t, t0 + 0.1, 0.5))
    el_at(f, food_el("guava", "happy", (0, 0.5)), 740, yy, 0.8)
    if t > tg: kw(f, "ONE GUAVA", 540, 360, t, tg, "pop", 110, col=INKC); t3(f, "55 g", 540, t, tg + 0.1, 150)
    return finish(f, n, look="golden")


# ---- S11b: '...so even a single fruit beats a whole orange.' BOARD: ONE guava 125 mg vs ONE whole orange 70 mg ----
def shot_S11b(t, n):
    f = board_bg(); t0 = st_("S11b")
    k1 = ramp(t, t0 + 0.2, 0.6); k2 = ramp(t, T("c1", "whole") - 0.3, 0.6)
    scoreline(f, 330, 0, "1 orange", 70, k1, maxmg=140, hgt=620); scoreline(f, 750, 0, "1 guava", 125, k2, maxmg=140, hgt=620, hl=True)
    el_at(f, food_el("orange", "n"), 330, 520, 0.95, t, t0 + 0.1)
    el_at(f, food_el("guava", "happy"), 750, 520, 0.85, t, t0 + 0.3)
    write_on(f, "a whole fruit each", 540, 330, t, t0 + 0.1, 46, INKC)
    src(f, SRC_USDA, t, t0 + 0.3, y=1470)
    return finish(f, n, look="fresh")


# ---- S12: 'So just one guava gives you more vitamin C than most adults need in a whole day.' BOARD: a DAY jar fills with vitamin C buddies and overflows ----
def shot_S12(t, n):
    f = board_bg(); t0 = st_("S12"); ta = T("c2", "adults") - 0.2
    jar = [(330, 640), (330, 1300), (750, 1300), (750, 640)]
    draw_on(f, jar, ramp(t, t0, 0.4), BP_INK, 8, seed=21, tip=False)
    write_on(f, "a day", 540, 580, t, t0 + 0.3, 50, BP_INK)
    el_at(f, food_el("guava", "happy", (1, 0)), 170, 560, 0.85, t, t0 + 0.1)
    nb = int(14 * ramp(t, t0 + 0.4, max(0.5, T("c2", "day") - t0 - 0.4)))
    for i in range(nb):
        r_, c_ = divmod(i, 3); x = 400 + c_ * 140; y = 1220 - r_ * 140
        if i >= 12: x, y = 400 + 280 * (i - 12), 560 - 60 * math.sin(t * 4 + i)
        el_at(f, vitc_el("happy" if i < 12 else "wow"), x, y, 1.0)
    if t > ta:
        cc(f, "adults: 75 to 90 mg a day", 540, 380, t, ta, INKC, MILK, 48)
    src(f, SRC_NIH, t, t0 + 0.3, y=1470)
    peek(f, t, 900, 1150, 0.55, "happy", (-0.6, -0.3))
    return finish(f, n, look="fresh")


# ---- S13: 'And the gold medal goes to...' stadium at dusk: podium, sweeping spotlights, a drumroll ----
def shot_S13(t, n):
    t0 = st_("S13"); f = set_stadium(t, dim=0.55)
    for k_ in range(3):
        x = 540 + 380 * math.sin(t * 2.4 + k_ * 2.1); spotlight(f, x, 1240, 210, 0.35, 90)
    for i, (dx, h, lab) in enumerate(((-260, 130, "2"), (0, 220, "1"), (260, 90, "3"))):
        x0, x1 = 540 + dx - 120, 540 + dx + 120; y0 = 1460 - h
        cv2.rectangle(f, (x0, y0), (x1, 1460), C((250, 246, 236)), -1, cv2.LINE_AA); cv2.rectangle(f, (x0, y0), (x1, 1460), C(INKC), 5, cv2.LINE_AA)
        write_on(f, lab, 540 + dx, y0 + 80, 99, 0, 60, INKC, 99)
    el_at(f, food_el("capsicum", "sus", (0.6, 0)), 280, 1240, 0.75)
    el_at(f, food_el("guava", "sus", (0, 0)), 800, 1280, 0.7)
    el_at(f, medal_ink(), 540, 960 + 20 * math.sin(t * 5), 1.5, rot=15 * math.sin(t * 3))
    kw(f, "GOLD GOES TO...", 540, 380, t, T("d0", "gold") - 0.2, "shake", 110, col=GOLD, amp=0.4)
    return finish(f, n, look="night")


def medal_ink():
    def mk():
        w, h = 220, 320; im, d, S = _cv(w, h)
        d.polygon(S(70, 0, 110, 150, 150, 0), fill=(60, 110, 200, 255)); d.line(_P([(70, 0), (110, 150), (150, 0)]), fill=INKC + (255,), width=4 * SC3)
        _ink_ell(d, 110, 220, 80, 80, GOLD, 380, INK_W)
        _shade(im, lambda q, S_: q.ellipse(S_(30, 140, 190, 300), fill=255), lambda q, S_, c: q.rectangle(S_(110, 130, 220, 320), fill=c), GOLD_S, 110)
        d.ellipse(S(70, 180, 150, 260), outline=GOLD_S + (255,), width=4 * SC3)
        d.text((110 * SC3, 222 * SC3), "1", font=font(F_HAND, 60 * SC3), fill=GOLD_S + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("medal33",), mk)


# ---- S13b: '...the green chilli. Two hundred and forty-two!' the chilli on the top step with the medal: the highest jump of the day ----
def shot_S13b(t, n):
    t0 = st_("S13b"); f = set_stadium(t, wave=t0 + 0.4); tj = t0 + 0.55
    jump_shot(f, t, "chilli", tj, 242, 1.0, x0=300, x1=720, dur=1.15, bar=228 if t < tj + 0.6 else 242, mood_land="love", medal=t > tj + 1.3)
    if t > tj + 0.6: num(f, count_up(t, tj + 0.6, 242, 0.7), 330, t, tj + 0.6, 220)
    if t < tj: kw(f, "GREEN CHILLI!", 540, 380, t, t0, "shake", 120, col=CHI_S, amp=0.7)
    confetti(f, t, tj + 1.3, 60, 7)
    return finish(f, n, look="golden")


# ---- S14: 'The chilli! But nobody eats a hundred grams of chilli.' worktop: a mountain of chillies on the scale, Chubby sweats ----
def shot_S14(t, n):
    f = set_worktop(t); t0 = st_("S14"); tn = T("d1", "nobody") - 0.2
    tk = take(t, tn)
    chub(f, 300, 1500 + tk["dy"], 1.05, t=t, **nolean(POSE["stop"] if t > tn else POSE["point"]), mouth=talk(t), expr="gross" if t > tn else tk["expr"], brow="sad", look=(1, 0.2), lean=tk["lean"], squash=tk["squash"], hand_r="open")
    worktop_front(f, 1330)
    el_at(f, scale_ink_el("100 g"), 740, 1250, 1.05)
    rng = np.random.default_rng(4)
    for i in range(11):
        r_, c_ = divmod(i, 4); x = 650 + c_ * 70 + 30 * (r_ % 2); y = 1120 - r_ * 70
        el_at(f, food_el("chilli", None), x, y, 0.5, rot=80 + 30 * rng.uniform(-1, 1))
    if t > tn: el_at(f, sweat_drop_el("n"), 420, 840 + 60 * ((t * 1.3) % 1), 0.7)
    kw(f, "100 g of chilli?", 540, 380, t, T("d1", "grams") - 0.2, "shake", 100, col=CHI_S, amp=0.5)
    return finish(f, n, look="golden")


# ---- S14b: 'You eat one or two, just a few grams,' close-up: Chubby nibbles ONE small chilli, his face reddens, steam from his ears ----
def shot_S14b(t, n):
    f = set_worktop(t); t0 = st_("S14b"); f = dof(f, 4); tb = T("d1", "few") - 0.2
    hot = ramp(t, tb, 0.5)
    chub_head_only(f, 540, 1020, 2.4, t, mouth=(3 if int(t * 8) % 2 else 1) if t > tb else talk(t), expr="gross" if t > tb + 0.3 else "happy", brow="sad" if t > tb else "up", look=(0.4, 0.4), tint=0.0)
    if hot > 0:
        f[...] = f  # keep
        glow(f, 540, 1000, 300, (255, 90, 70), 0.25 * hot)
        for sx in (240, 840): steam_wisps(f, sx, 880, t, 3, 140, 70, (255, 255, 255), 0.8 * hot, seed=sx)
    el_at(f, food_el("chilli", "wow", (-0.5, -0.5)), 720, 1240, 0.8, rot=-50)
    kw(f, "a few grams", 540, 380, t, t0 + 0.2, "pop", 110, col=INKC)
    return finish(f, n, look="golden")


# ---- S14c: '...so bite for bite, the guava still wins.' BOARD: one small chilli vs one guava, the guava's bar towers ----
def shot_S14c(t, n):
    f = board_bg(); t0 = st_("S14c")
    scoreline(f, 330, 0, "1 chilli", 14, ramp(t, t0 + 0.2, 0.4), maxmg=140, hgt=620, base=1220, shownum=False); scoreline(f, 750, 0, "1 guava", 125, ramp(t, t0 + 0.4, 0.6), maxmg=140, hgt=620, base=1220, hl=True)
    el_at(f, food_el("chilli", "sad"), 330, 1060, 0.7, t, t0 + 0.1)
    el_at(f, food_el("guava", "love", crown=t > T("d1", "wins") - 0.2), 750, 470, 0.8, t, t0 + 0.3)
    write_on(f, "bite for bite", 540, 330, t, t0 + 0.1, 50, INKC)
    if t > T("d1", "guava") - 0.2: kw(f, "GUAVA WINS", 540, 1430, t, T("d1", "guava") - 0.2, "pop", 90, col=GUA_S)
    return finish(f, n, look="fresh")


# ---- S15: 'One more twist, and it happens in your kitchen.' the STOVE: a pot of water on the boil, Chubby holds chopped capsicum over it ----
def shot_S15(t, n):
    t0 = st_("S15"); f = set_stove(t, on=0.9)
    PX = 640; PY = 1300 - 225 + 8
    chub(f, 260, 1560, 1.0, t=t, **nolean(POSE["hold_up"]), mouth=talk(t), expr="sus", brow="up", look=(1, 0.3), hand_r="grip")
    comp(f, pot_el("water", 0.6), PX, PY)
    side_flames(f, PX, 1298, t, 470 * 1.0, 0.9)
    rising_bubbles(f, PX, PY + 120, PY - 60, t, 300, 7, 12)
    steam_wisps(f, PX, PY - 230, t, 4, 180, 140, (255, 255, 255), 0.7)
    el_at(f, food_el("capsicum", "wow", (0.6, 0.8)), 470, 760 + 10 * math.sin(t * 5), 0.55)
    t3(f, "TWIST", 380, t, T("e0", "twist") - 0.2, 170)
    return finish(f, n, look="warm")


# ---- S15b: 'Vitamin C dissolves in water, and heat breaks it down.' BOARD: a slice of capsicum full of C buddies; water -> they swim out; heat -> they crack ----
def shot_S15b(t, n):
    f = board_bg(); t0 = st_("S15b"); tw = T("e0", "water") - 0.3; th = T("e0", "heat") - 0.2
    draw_ell_on(f, 540, 940, 380, 250, ramp(t, t0, 0.4), CAP_S, 10, seed=31)
    write_on(f, "a piece of capsicum", 540, 620, t, t0 + 0.1, 50, CAP_S)
    for i in range(6):
        a = 2 * math.pi * i / 6; bx, by = 540 + 210 * math.cos(a), 940 + 120 * math.sin(a)
        out = ramp(t, tw + 0.1 * i, 0.9) if i % 2 == 0 else 0
        x = bx + (bx - 540) * 0.8 * out; y = by + 360 * out
        kk = ramp(t, th + 0.08 * i, 0.5) if i % 2 == 1 else 0
        el_at(f, vitc_el("sad" if kk > 0.4 else ("wow" if out > 0 else "happy"), k=kk * 0.75), x, y, 1.05, t, t0 + 0.3 + 0.06 * i)
    if t > tw:
        for j in range(3): cv2.ellipse(f, (380 + 140 * j, 1360), (60, 14), 0, 0, 360, C((98, 168, 228)), 6, cv2.LINE_AA)
        write_on(f, "water", 200, 1300, t, tw, 50, (52, 116, 188))
    if t > th:
        flames(f, 880, 1420, t, 160, 5, 0.8, (255, 170, 60), (240, 90, 40))
        write_on(f, "heat", 880, 1280, t, th, 50, ACC_S)
    return finish(f, n, look="fresh")


# ---- S16: 'So the longer you boil your vegetables, the more of it ends up in the water,' stove close: cut-away pot, buddies drift out of the veg into the water, the clock spins ----
def shot_S16(t, n):
    t0 = st_("S16"); f = set_stove(t, on=1.0); f = dof(f, 3)
    PX, PY, s = 540, 1100, 1.5
    comp(f, scale_el(pot_el("water", 0.62), s), PX, PY)
    g = pot_geom(PX, PY, s, "water", 0.62)
    k = ramp(t, t0 + 0.2, max(0.6, T("e1", "water") - t0))
    for i in range(3): el_at(f, food_el("capsicum", "sad" if k > 0.5 else "n"), PX - 150 + 150 * i, g["y_bot"] - 100 + 10 * math.sin(t * 6 + i), 0.33, rot=30 * i)
    for i in range(8):
        sx = PX - 150 + 150 * (i % 3); sy = g["y_bot"] - 110
        x = sx + 60 * math.sin(i * 2.3 + t * 1.5) * k; y = sy - (sy - g["y_surf"] - 40) * k * ((i % 4) + 1) / 4
        el_at(f, vitc_el("wow" if k > 0.3 else "happy"), x, y, 0.42, op=0.9)
    side_flames(f, PX, 1298, t, 470 * s * 0.8, 1.0)
    steam_wisps(f, PX, g["y_rim"] - 20, t, 4, 200, 160, (255, 255, 255), 0.7)
    el_at(f, clock_ink_el(90), 880, 560, 1.0)
    clock_hands(f, 880, 560, (t - t0) * 6, 90)
    kw(f, "LONGER BOIL", 400, 360, t, T("e1", "longer") - 0.2, "shake", 100, col=ACC_S, amp=0.4)
    return finish(f, n, look="warm")


# ---- S16b: '...or simply gone.' the buddies crack, fade and poof: GONE ----
def shot_S16b(t, n):
    t0 = st_("S16b"); f = set_stove(t, on=1.0); f = dof(f, 5)
    tg = T("e1", "gone") - 0.3
    for i in range(5):
        k = ramp(t, tg + 0.06 * i, 0.5)
        x = 200 + 170 * i; y = 980 - 40 * math.sin(t * 3 + i) - 200 * k
        el_at(f, vitc_el("sad", k=k), x, y, 0.95, op=1 - 0.8 * k)
    steam_wisps(f, 540, 1300, t, 6, 400, 300, (255, 255, 255), 0.6)
    kw(f, "GONE", 540, 420, t, tg, "drop", 170, col=INKC, t1=tg + 0.4)
    return finish(f, n, look="warm")


# ---- S17: 'Steaming or the microwave loses less.' BOARD: a steamer basket and a microwave, the buddies mostly stay: tick ----
def shot_S17(t, n):
    f = board_bg(); t0 = st_("S17"); tm = T("e2", "microwave") - 0.2; tl = T("e2", "less") - 0.3
    pts = [(70, 960), (490, 960), (455, 1200), (105, 1200)]                   # the steamer basket (woven lines) over a pot
    draw_on(f, pts + [pts[0]], ramp(t, t0, 0.4), BP_INK, 7, seed=41, tip=False)
    for j in range(6): draw_on(f, [(110 + 66 * j, 960), (130 + 58 * j, 1200)], ramp(t, t0 + 0.2, 0.3), BP_INK, 3, seed=42 + j, tip=False)
    for j in range(3): el_at(f, vitc_el("happy"), 170 + 110 * j, 890, 0.85, t, t0 + 0.4 + 0.08 * j)
    steam_wisps(f, 280, 820, t, 3, 160, 160, (190, 200, 220), 0.6)
    write_on(f, "steam", 280, 1290, t, t0 + 0.2, 50)
    if t > tm:
        el_at(f, microwave_el(on=True, timer="2:00"), 790, 1070, 0.82, t, tm)
        for j in range(3): el_at(f, vitc_el("happy"), 700 + 65 * j, 1085, 0.48, t, tm + 0.2 + 0.08 * j)
        write_on(f, "microwave", 790, 1290, t, tm, 50)
    if t > tl:
        tick(f, 540, 520, 80, ramp(t, tl, 0.3))
        kw(f, "LOSES LESS", 540, 360, t, tl, "pop", 110, col=INK_MINT_S)
    return finish(f, n, look="fresh")


# ---- S17b: 'And cut fruit is best eaten fresh, not left sitting for days.' worktop: a plate of cut guava; the calendar flips; the pieces go sad ----
def shot_S17b(t, n):
    f = set_worktop(t); t0 = st_("S17b"); tn = T("e2", "not") - 0.2
    chub(f, 280, 1500, 1.0, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="happy" if t < tn else "sad", brow="up" if t < tn else "sad", look=(1, 0.3))
    worktop_front(f, 1330)
    days = 0 if t < tn else min(3, 1 + int((t - tn) / 0.4))
    comp(f, plate_el(), 730, 1310)
    for i in range(3):
        el_at(f, food_el("guava", "happy" if days == 0 else "sad", cut=True), 620 + 110 * i, 1200, 0.6, rot=-10 + 10 * i, op=1 - 0.12 * days)
    if t > tn:
        el_at(f, calendar_el("DAY", str(days)), 800, 700, 0.7)
    kw(f, "EAT IT FRESH", 540, 360, t, T("e2", "fresh") - 0.25, "pop", 110, col=GUA_S)
    return finish(f, n, look="golden")


# ---- S18: the RECAP as a LEADERBOARD to screenshot: rows tick in as each food is named (per 100 g) ----
ROWS = [("orange", "orange", 53, ("f0", "orange")), ("lemon", "lemon", 53, ("f0", "lemon")), ("papaya", "papaya", 61, ("f0", "papaya")),
        ("capsicum", "capsicum", 128, ("f0", "capsicum")), ("guava", "guava", 228, ("f0", "guava")), ("chilli", "chilli", 242, ("f0", "green"))]


def shot_S18(t, n):
    f = board_bg(); t0 = st_("S18")
    comp(f, chip("VITAMIN C  per 100 g", INKC, ACC_L, 50), 540, 340, scale=pin(t, t0))
    for i, (kd, name, mg, (lid, w)) in enumerate(ROWS):
        y = 480 + 160 * i
        board_row(f, y, kd, name, mg, t, T(lid, w) - 0.25, maxw=420, x_ic=110, x_name=290, x_bar=440, hl=(kd in ("guava", "chilli")))
    src(f, SRC_USDA, t, t0 + 0.4, y=1440)
    return finish(f, n, look="fresh")


# ---- S19: 'Save this for your next trip to the market,' worktop: Chubby back from the market with a bag of guava, capsicum, papaya ----
def shot_S19(t, n):
    f = set_worktop(t); t0 = st_("S19")
    chub(f, 360, 1500, 1.1, t=t, **nolean(POSE["tada"]), mouth=talk(t), expr="happy", brow="up", look=(0.6, 0))
    worktop_front(f, 1330)
    el_at(f, bag_el("guava"), 760, 1150, 1.0, t, t0 + 0.05)
    kw(f, "SAVE THIS", 540, 360, t, t0 + 0.1, "pop", 140, col=ACC_S)
    return finish(f, n, look="golden")


# ---- S20: '...send it to the friend who buys oranges every time they catch a cold.' the friend, a bag of oranges, a sneeze; phone; logo ----
FRIEND = (236, 150, 110)


def shot_S20(t, n):
    t0 = st_("S20"); f = set_worktop(t); vend = LINES["f1"]["end"] + 0.15; tc = T("f1", "cold") - 0.25
    if t < vend + 0.2:
        chub(f, 300, 1500, 1.0, t=t, **nolean(POSE["shrug"]), mouth=talk(t), expr="happy", brow="up", look=(1, 0), turn=0.5)
        sneeze = t > tc
        chub(f, 760, 1500, 1.05, t=t, shirt=FRIEND, la=(30, 14), ra=(60, 40), mouth="o" if sneeze else 1, expr="gross" if sneeze else "happy", brow="sad" if sneeze else "up", look=(-0.5, 0), lean=-10 if sneeze else 0)
        dress(f, 760, 1500, 1.05, "cousin")
        worktop_front(f, 1330)
        el_at(f, bag_el("orange"), 900, 1220, 0.75)
        if sneeze:
            for j in range(6): cv2.circle(f, (int(700 - 40 * j * ramp(t, tc, 0.3)), int(900 + 10 * j)), 6, C((200, 220, 240)), -1, cv2.LINE_AA)
            kw(f, "ACHOO", 760, 700, t, tc, "shake", 80, col=INKC, amp=0.6)
        comp(f, scale_el(phone2_el("oranges again?", "try guava!", t > T("f1", "send") + 0.4), 0.5), 540, 760, scale=pin(t, t0 + 0.1))
        ui_word(f, "send this to the friend who", "BUYS [ORANGES]", 380, t, T("f1", "send") - 0.05, col=INKC, acc=ACC_S, size=96, lead_col=INKC)
    else:
        f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32); k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 760, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 540, 1500, 0.62, t=t, la=(150, 170), ra=(150, 170), mouth=3, expr="happy", brow="up")
    return finish(f, n, look="golden")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "close") - 0.25, 0.35, 12), (T("i1", "top") - 0.1, 0.25, 8), (T("i2", "make") - 0.0, 0.25, 8), (T("i2", "orange") - 0.3, 0.25, 8),
           (T("i3", "jump") - 0.15, 0.3, 10), (T("i3", "bar") - 0.3, 0.3, 10), (T("a0", "hundred") - 0.2, 0.3, 10),
           (T("a1", "clears") - 0.35 + 0.18 + 1.05, 0.3, 10), (T("a1", "bar") - 0.1, 0.3, 10), (T("a2", "sour") - 0.2, 0.3, 10),
           (T("a3", "same") - 0.2, 0.35, 12), (T("b0", "over") - 0.2, 0.25, 8), (T("b1", "fruit") - 0.35, 0.4, 14),
           (T("b2", "Red") - 0.1 + 0.25 + 0.18 + 1.05, 0.45, 16), (T("b2", "double") - 0.2, 0.3, 10),
           (T("c0", "clears") - 0.45 + 0.18 + 1.25, 0.5, 18), (T("c1", "four") - 0.25, 0.3, 10), (T("c1", "fifty-five") - 0.2, 0.25, 8),
           (T("c1", "whole") - 0.3, 0.3, 10), (T("c2", "day") - 0.3, 0.3, 10), (T("d0", "green") - 0.15 + 0.55 + 0.18 + 1.15, 0.5, 18),
           (T("d1", "nobody") - 0.2, 0.35, 12), (T("d1", "few") - 0.2, 0.3, 10), (T("d1", "guava") - 0.2, 0.3, 10),
           (T("e0", "twist") - 0.2, 0.3, 10), (T("e0", "heat") - 0.2, 0.3, 10), (T("e1", "gone") - 0.3, 0.35, 12),
           (T("e2", "less") - 0.3, 0.25, 8), (T("e2", "not") - 0.2, 0.25, 8), (T("f1", "cold") - 0.25, 0.3, 10)]


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    f = RENDER[sid](tt, n).astype(np.float32)
    dx = dy = 0.0; z = 1.0
    for ti, d, a in IMPACTS:
        if s["start"] - 0.05 <= ti < s["end"] and ti <= tt < ti + d:
            k = 1 - (tt - ti) / d; dx += a * k * math.sin(tt * 97); dy += a * k * math.cos(tt * 83); z += 0.03 * k
    if dx or dy or abs(z - 1) > 1e-4: f = cam(f, z, W / 2, H / 2, dx, dy)
    return f


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; f = rs(sh["id"], t, n); k = sh["trans"]; dt = t - sh["start"]
    if i > 0:
        if k == "erase" and dt < 0.42:
            f = erase_mix(rs(SHOTS[i - 1]["id"], t, n), f, dt / 0.42)
        elif k == "morph" and dt < 0.42:
            a, b = MORPH[sh["id"]]; f = morph_mix(rs(SHOTS[i - 1]["id"], t, n), f, dt / 0.42, a, b)
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
