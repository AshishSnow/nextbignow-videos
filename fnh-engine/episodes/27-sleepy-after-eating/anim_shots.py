# ================= shots: FreshNestHub 27 — "Why do you feel sleepy after a big meal?" (Chubby INK, ep 10 of the ink look) ===
# COLOUR SCRIPT: warm Diwali room = the feast (gold lamps); DUSK LAVENDER (ACC) = sleepiness: the dip on the graph, the dimmer's SLEEPY end, the lights dropping.
# BOARD shots (white paper, blueprint-blue ink that DRAWS ITSELF in sync with the voice, ONE lavender pop) carry every explanation; the lit room carries the story.
# Blood red = the myth only. The hero craft: the DRAW-ON BOARD kit (anim_fx draw_on / write_on / hatch_on / erase_mix). Acting: Chubby NODS OFF (anim_fx.doze).
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "isnt") - 0.12, "erase"),
    ("S1", T("i2", "Thats") - 0.15, "whip"), ("S1b", T("i2", "Your") - 0.1, "erase"), ("S1c", T("i2", "your", 1) - 0.1, "punch"),
    ("S2", T("i3", "Scientists") - 0.15, "flash"), ("S2b", T("i3", "Its") - 0.08, "punch"),
    ("S3", T("i4", "So") - 0.15, "whip"), ("S3b", T("i4", "need") - 0.1, "punch"),
    ("S4", T("a0", "Whats") - 0.15, "erase"),
    ("S5", T("a1", "Thing") - 0.15, "flash"), ("S6", T("a2", "It") - 0.1, "erase"), ("S6b", T("a2", "around") - 0.1, "zoom"),
    ("S7", T("a3", "Your") - 0.1, "punch"), ("S7b", T("a3", "Skip") - 0.1, "whip"), ("S8", T("a4", "So") - 0.15, "erase"),
    ("S9", T("b1", "Thing") - 0.15, "flash"), ("S10", T("b2", "As") - 0.1, "erase"), ("S10b", T("b2", "and") - 0.1, "punch"),
    ("S11", T("b3", "One") - 0.1, "whip"), ("S11b", T("b3", "after") - 0.1, "punch"), ("S12", T("b4", "Think") - 0.1, "whip"), ("S12b", T("b4", "A", 1) - 0.1, "punch"),
    ("S13", T("b5", "And") - 0.1, "erase"),
    ("S14", T("c1", "In") - 0.1, "whip"), ("S14b", T("c1", "Almost") - 0.1, "erase"), ("S15", T("c2", "Four") - 0.12, "flash"),
    ("S16", T("c3", "To") - 0.1, "erase"), ("S16b", T("c3", "But") - 0.1, "punch"),
    ("S17", T("d0", "So") - 0.15, "flash"), ("S18", T("d1", "One") - 0.15, "whip"), ("S18b", T("d1", "You") - 0.1, "punch"),
    ("S19", T("d2", "Two") - 0.15, "whip"), ("S19b", T("d2", "Ten") - 0.1, "punch"), ("S20", T("d3", "Three") - 0.15, "whip"),
    ("S21", T("d4", "And") - 0.1, "whip"), ("S21b", T("d4", "Hand") - 0.1, "punch"),
    ("S22", T("e1", "If") - 0.15, "erase"), ("S22b", T("e1", "or") - 0.1, "punch"),
    ("S23", T("f1", "So") - 0.15, "erase"), ("S24", T("f2", "Send") - 0.15, "whip"),
]

SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
path_at = path_point
_write_on0 = write_on


def write_on(f, text, x, y, t, t0, size=56, col=BP_INK, cps=22.0, op=1.0):
    """phone-size hand lettering: the board text reads 30 % bigger than the kit default (test frames: 36-50 px was too small)."""
    _write_on0(f, text, x, y, t, t0, int(size * 1.3), col, cps, op)


def st_(sid): return SHOT[sid]["start"]


def en_(sid): return SHOT[sid]["end"]


def ui_word(f, lead, big, y, t, t0, col=INKC, acc=ACC, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def icap(f, lead, big, t, t0, acc=ACC_S, size=150, y=420, out=None, tail="", dark=False):
    if dark: ui_word(f, lead, big, y, t, t0, col=WHITE, acc=ACC_L, size=size, shadow=0.6, lead_col=WHITE, out=out, tail=tail)
    else: ui_word(f, lead, big, y, t, t0, col=INKC, acc=acc, size=size, shadow=0.0, lead_col=INKC, out=out, tail=tail)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def t3(f, text, y, t, t0, size=200, face=None, side=None, x=540):
    if t >= t0: title_ink(f, text, y, t, t0, size=size, face=face or ACC_L, side=side or ACC_S, depth=18, x=x)


def nolean(p): return {k: v for k, v in p.items() if k != "lean"}


def src(f, text, t, t0, y=1462):
    if t >= t0: comp(f, chip(text, INKC, MILK, 22), 540, y, op=clamp((t - t0) / 0.2))


def cc(f, text, x, y, t, t0, bg=None, fg=None, size=34):
    if t >= t0: comp(f, chip(text, bg or INKC, fg or MILK, size), x, y, scale=pin(t, t0))


def peek(f, t, x, y, s, expr="sus", look=(0, 0), brow=None, mouth=None):
    s = s * 1.7
    chub_head_only(f, x, y, s, t, mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow or ("sus" if expr == "sus" else "up"), look=look, turn=clamp(look[0]) * 0.5)


def figure(f, k, cx=540, hy=560, col=BP_INK, w=7):
    """board drawing: a front-view head + torso outline (head first, then the body)."""
    draw_ell_on(f, cx, hy, 150, 160, clamp(k / 0.4), col, w, seed=11)
    kb = clamp((k - 0.4) / 0.6)
    for sg in (-1, 1):
        P = [(cx + sg * 52, hy + 152), (cx + sg * 58, hy + 205), (cx + sg * 210, hy + 250), (cx + sg * 250, hy + 330), (cx + sg * 240, hy + 760), (cx + sg * 150, hy + 830)]
        draw_on(f, P, kb, col, w, seed=12 + sg, tip=sg > 0)


SRC_OX = "Source: Healthline (2022) · ScienceABC · Cleveland Clinic"
SRC_BATH = "Source: University of Bath, Br J Nutr (2020)"
TN = T("i1", "meal") - 0.05


# ---- S0: HOOK: frame 0, Diwali lunch: Chubby behind a heaped thali is ALREADY nodding off; on 'meal' his head drops (thunk) ----
def shot_S0(t, n):
    f = set_droom(t); dz = doze(t, -1.6, 2.25, 1.0)
    big = t >= TN
    if big: dz = dict(lean=14, look=(0.1, 1.0), bob=26 + 4 * math.exp(-(t - TN) * 9) * math.sin((t - TN) * 40), blink=True, expr="sleepy", brow="sad")
    chub(f, 540, 1500, 1.12, t=t, la=(150, -120), ra=(30, 18), mouth=0, **dz)
    table_front(f, 1330)
    comp(f, scale_el(thali_el("full"), 0.95), 540, 1372)
    if big: zzs(f, 700, 820, t - TN, 3, INKC, 1.1)
    icap(f, "after a big meal, that", "[SLEEPY] feeling", t, 0.05, size=118, y=360)
    return finish(f, n, look="warm")


# ---- S0b: '...isn't your blood leaving your brain?' BOARD: a head + body draw themselves, blood drops slide from the brain to the stomach, a big '?' ----
def shot_S0b(t, n):
    f = board_bg(); t0 = st_("S0b"); k = ramp(t, t0, 0.9)
    figure(f, k, 540, 640)
    if k > 0.35: comp(f, scale_el(brain_ink_el("wow"), 0.8), 540, 630, scale=pin(t, t0 + 0.35))
    if k > 0.8: comp(f, scale_el(stomach_ink_el("happy"), 0.75), 560, 1150, scale=pin(t, t0 + 0.75))
    P = [(560, 720), (600, 860), (590, 980), (570, 1080)]
    draw_on(f, P, ramp(t, T("i1", "blood") - 0.1, 0.5), BLOOD_C, 6, seed=3)
    for j in range(4):
        q = ((t - T("i1", "leaving")) * 0.8 + j * 0.25)
        if q > 0 and t > T("i1", "leaving") - 0.1: x, y = path_at(P, q % 1.0); comp(f, scale_el(blood_el("happy"), 0.32), x, y)
    tq = T("i1", "brain") - 0.05
    if t >= tq: rot_comp(f, hand_text_el("?", 220, ACC_S), 860, 640, -8, snap(t, tq, 4), 1.0)
    icap(f, "isn't your", "[BLOOD] leaving your brain?", t, t0 + 0.05, size=76, y=330)
    return finish(f, n, look="fresh")


# ---- S1: 'That's the story we all grew up with.' an aunty wags her finger at little Chubby ----
def shot_S1(t, n):
    f = set_droom(t, dim=0.05); t0 = st_("S1")
    wag = 14 * math.sin(t * 13)
    chub(f, 300, 1500, 1.08, t=t, la=(24, 14), ra=(150, 170 + wag), shirt=(220, 80, 130), mouth=talk(t), expr="sus", brow="sus", look=(1, 0.2), turn=0.5, lean=4)
    dress(f, 300, 1500, 1.08, "aunty", 4)
    chub(f, 760, 1500, 0.8, t=t, **POSE["idle"], mouth=0, expr="happy", brow="up", look=(-1, -0.3), turn=-0.5, bob=4 * math.sin(t * 6.5))
    table_front(f, 1380)
    icap(f, "the story we all", "[GREW UP] with", t, t0 + 0.05, size=110, y=400)
    return finish(f, n, look="warm")


# ---- S1b: 'Your stomach steals the blood' BOARD: a greedy stomach reaches up and pulls the blood drops down from the brain ----
def shot_S1b(t, n):
    f = board_bg(); t0 = st_("S1b"); ts = T("i2", "steals") - 0.1
    figure(f, 1.0, 540, 640)
    comp(f, scale_el(brain_ink_el("wow", level=1 - 0.4 * ramp(t, ts, 1.4)), 0.8), 540, 630)
    comp(f, scale_el(stomach_ink_el("hungry", grab=0.3 + 0.7 * ramp(t, t0, 0.4)), 0.8), 560, 1150 + 6 * math.sin(t * 9))
    for j in range(6):
        q = (t - ts) * 0.9 - j * 0.16
        if q > 0:
            x0 = 540 + (j % 3 - 1) * 60; qq = clamp(q % 1.2)
            x = x0 + (560 - x0) * qq; y = 680 + (1110 - 680) * eio(qq) - 80 * math.sin(math.pi * qq)
            comp(f, scale_el(blood_el("sad" if qq > 0.3 else "wow"), 0.3), x, y)
    write_on(f, "steals the blood?", 540, 410, t, ts, 64, BLOOD_C)
    return finish(f, n, look="fresh")


# ---- S1c: 'your brain runs dry, and you're out.' the brain drains grey; on 'out' the lights go OUT ----
def shot_S1c(t, n):
    f = board_bg(); t0 = st_("S1c"); to = T("i2", "out") - 0.05
    figure(f, 1.0, 540, 640)
    lv = 0.6 - 0.6 * ramp(t, t0 + 0.2, 1.3)
    comp(f, scale_el(brain_ink_el("sad" if lv < 0.3 else "wow", level=lv), 0.8), 540, 630)
    comp(f, scale_el(stomach_ink_el("love"), 0.8), 560, 1150)
    cx, cy = 840, 520; draw_ell_on(f, cx, cy, 90, 90, 1.0, BP_INK, 5, seed=4, a0=180)
    a = math.radians(-160 + 140 * lv / 0.6); cv2.line(f, (cx, cy), (int(cx + 75 * math.cos(a)), int(cy + 75 * math.sin(a))), C(BLOOD_C), 7, cv2.LINE_AA)
    write_on(f, "E", cx - 70, cy + 40, t, t0, 44); write_on(f, "F", cx + 70, cy + 40, t, t0, 44)
    if t >= to:
        k = clamp((t - to) / 0.08); f[:] = f * (1 - 0.86 * k)
        zzs(f, 700, 600, t - to, 3, WHITE, 1.2)
        icap(f, "and you're", "OUT", t, to, size=170, y=1000, dark=True)
    return finish(f, n, look="night" if t >= to else "fresh")


# ---- S2: 'Scientists checked.' Dr Chubby in a white coat holds a magnifier over the brain; the MYTH tag appears ----
def shot_S2(t, n):
    f = ink_set("mintp", (255, 255, 255), 540, 980, 600); t0 = st_("S2")
    podium(f, 640, 1250, 420, 110, t)
    comp(f, scale_el(brain_ink_el("n", look=(-0.6, 0)), 0.95), 640, 1150)
    chub(f, 250, 1500, 1.05, t=t, **nolean(POSE["hold_up"]), shirt=(250, 250, 250), mouth=talk(t), expr="sus", brow="sus", look=(1, 0.3), turn=0.5, hand_r="grip")
    dress(f, 250, 1500, 1.05, "cousin")
    comp(f, scale_el(magnifier_ink_el(), 0.9), 450 + 20 * math.sin(t * 2.5), 980 + 14 * math.cos(t * 3))
    icap(f, "", "SCIENTISTS [CHECKED]", t, t0 + 0.05, size=96, y=380)
    return finish(f, n, look="fresh")


# ---- S2b: 'It's a myth.' BUSTED: the MYTH tag + a red X over the blood drop; Chubby's take; crash zoom ----
def shot_S2b(t, n):
    f = board_bg(); t0 = st_("S2b"); tm = T("i3", "myth") - 0.05; tk = take(t, tm)
    comp(f, scale_el(blood_el("sad"), 1.4), 540, 900)
    if t >= tm:
        k = snap(t, tm, 4)
        for sg in (-1, 1): cv2.line(f, (int(540 - 180 * k), int(900 - sg * 180 * k)), (int(540 + 180 * k), int(900 + sg * 180 * k)), C(BLOOD_S), 30, cv2.LINE_AA)
    myth_tag(f, 540, 560, t, t0 - 0.2, tm, 70)
    chub(f, 800, 1520 + tk["dy"], 0.8, t=t, la=(110, 150), ra=(110, 150), mouth="jaw" if tm < t < tm + 0.8 else talk(t), expr=tk["expr"] if t >= tm else "sus", brow=tk["brow"] if t >= tm else "sus", look=(-0.8, -0.2), squash=tk["squash"], lean=tk["lean"], turn=-0.5)
    f = crash_zoom(f, t, tm, 1.15, 540, 800)
    return finish(f, n, look="fresh")


# ---- S3: 'So tomorrow's Diwali lunch nap...' Chubby flops on the sofa, yawning; S3b: '...is going to need a new excuse.' he shrugs, ink title ----
def shot_S3(t, n):
    f = set_droom(t, dim=0.05); t0 = st_("S3")
    comp(f, sofa_el(), 540, 1340)
    y = 1440 + 30 * ramp(t, t0, 0.3)
    chub(f, 540, y, 1.0, t=t, **nolean(POSE["yawn"]), sit=True, mouth="jaw" if T("i4", "nap") - 0.1 < t < T("i4", "nap") + 0.6 else 0, expr="sleepy", brow="sad", look=(0, -0.2), lean=-4 + 3 * math.sin(t * 1.5))
    icap(f, "tomorrow's Diwali lunch", "[NAP]", t, T("i4", "nap") - 0.15, size=150, y=380)
    return finish(f, n, look="golden")


def shot_S3b(t, n):
    f = set_droom(t, dim=0.05); t0 = st_("S3b"); tx = T("i4", "new") - 0.1
    comp(f, sofa_el(), 540, 1340)
    chub(f, 540, 1470, 1.0, t=t, **POSE["shrug"], sit=True, mouth=talk(t), expr="smirk", brow="up", look=(0.4, -0.1))
    t3(f, "NEW EXCUSE?", 560, t, tx, 170)
    return finish(f, n, look="golden")


# ---- S4: 'What's really going on is two things, and one happens even if you skip lunch.' BOARD: two boxes draw themselves; an empty plate under box 1 ----
def shot_S4(t, n):
    f = board_bg(); t0 = st_("S4"); tt = T("a0", "two") - 0.1; ts = T("a0", "skip") - 0.1
    write_on(f, "what's really going on", 540, 380, t, t0 + 0.05, 60)
    for i, x in enumerate((300, 780)):
        k = ramp(t, tt + i * 0.3, 0.6)
        draw_on(f, [(x - 170, 560), (x + 170, 560), (x + 170, 900), (x - 170, 900)], k, BP_INK, 7, seed=20 + i, closed=True)
        if k > 0.9: rot_comp(f, hand_text_el(str(i + 1), 150), x, 700, 0, snap(t, tt + i * 0.3 + 0.5, 4), 1.0)
        if k > 0.9: write_on(f, "?", x, 830, t, tt + i * 0.3 + 0.6, 70, ACC_S)
    if t >= ts:
        comp(f, scale_el(thali_el("empty"), 0.5), 300, 1060, scale=snap(t, ts, 4))
        draw_arrow_on(f, (300, 1000), (300, 920), ramp(t, ts + 0.2, 0.3), ACC_S, 6)
        write_on(f, "no lunch, still there", 330, 1200, t, ts + 0.3, 40, ACC_S)
    peek(f, t, 860, 1250, 0.55, "sus", (-0.6, -0.4))
    return finish(f, n, look="fresh")


# ---- S5: 'Thing one is your body clock.' PART 1: a big ink clock, the hands sweep a whole day; Chubby points ----
def shot_S5(t, n):
    f = set_lunch(t); t0 = st_("S5")
    hrs = 8 + 14 * ramp(t, t0, 2.2)
    glow(f, 600, 940, 330, (255, 236, 190), 0.25)
    comp(f, scale_el(clock_ink_el(150, 3), 1.25), 600, 940); clock_hands(f, 600, 940, hrs, 150, 1.25)
    chub(f, 200, 1500, 1.0, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="happy", brow="up", look=(1, -0.4), hand_r="point", turn=0.5)
    cloth_front(f, 1400)
    t3(f, "BODY CLOCK", 500, t, T("a1", "body") - 0.15, 150)
    chapter_card(f, t, t0 + 0.05, 1, "BODY CLOCK", 1340, 1.8, ACC_L)
    return finish(f, n, look="golden")


# ---- S6: 'It runs your day in waves... in the early afternoon, around two to four, there's a little dip.' BOARD: the alertness wave draws itself ----
GX0, GX1, GY0, GY1 = 120, 960, 640, 1180


def alert_curve(h, deep=0.0):
    """alertness 0..1 across the day (8 am .. 10 pm): a wave with a small dip at ~3 pm (deep adds the meal on top) and the evening fall."""
    v = 0.55 + 0.32 * math.sin((h - 8) / 14 * math.pi * 0.95) - (0.16 + 0.22 * deep) * math.exp(-((h - 15) / 1.1) ** 2) - 0.45 * clamp((h - 20) / 2.5) ** 2
    return clamp(v, 0.02, 0.98)


def gxy(h, v): return GX0 + (h - 8) / 14 * (GX1 - GX0), GY1 - v * (GY1 - GY0)


def graph(f, t, k, deep=0.0, zone=0.0, t_lab=0.0):
    draw_on(f, [(GX0, GY0 - 40), (GX0, GY1), (GX1 + 20, GY1)], clamp(k * 3), BP_INK, 6, seed=31)
    if k > 0.2:
        write_on(f, "awake", GX0 + 90, GY0 - 60, t, t_lab, 40); write_on(f, "8 AM", GX0 + 10, GY1 + 50, t, t_lab, 36); write_on(f, "10 PM", GX1 - 60, GY1 + 50, t, t_lab, 36)
    if zone > 0:
        x0, _ = gxy(14, 0); x1, _ = gxy(16, 0)
        hatch_on(f, [(x0, GY0), (x1, GY0), (x1, GY1), (x0, GY1)], zone, ACC, 18, 45, 4, 0.55)
    P = [gxy(8 + 14 * u, alert_curve(8 + 14 * u, deep)) for u in np.linspace(0, 1, 70)]
    return draw_on(f, P, clamp((k - 0.15) / 0.85), BP_INK, 9, seed=32, wob=0.6)


def shot_S6(t, n):
    f = board_bg(); t0 = st_("S6"); tz = T("a2", "early") - 0.1
    graph(f, t, ramp(t, t0, 2.1), zone=ramp(t, tz, 0.6), t_lab=t0 + 0.4)
    write_on(f, "your day, in waves", 540, 440, t, T("a2", "waves") - 0.3, 60)
    if t >= tz: write_on(f, "early afternoon", 640, 1290, t, tz, 46, ACC_S)
    peek(f, t, 880, 1400, 0.5, "happy", (-0.5, -0.6))
    return finish(f, n, look="fresh")


def shot_S6b(t, n):
    f = board_bg(); t0 = st_("S6b"); td = T("a2", "dip") - 0.1
    graph(f, t, 1.0, zone=1.0, t_lab=-9)
    write_on(f, "2 PM", gxy(14, 0)[0], GY1 + 50, t, T("a2", "two") - 0.1, 36, ACC_S); write_on(f, "4 PM", gxy(16, 0)[0], GY1 + 50, t, T("a2", "four") - 0.1, 36, ACC_S)
    hm = 12.5 + 2.5 * ramp(t, t0, td - t0 + 0.1); x, y = gxy(hm, alert_curve(hm))
    chub_head_only(f, x, y - 70, 0.32, t, mouth=0, expr="sleepy" if hm > 14.6 else "happy", brow="sad" if hm > 14.6 else "up")
    f = cam(f, 1 + 0.25 * ramp(t, t0, 0.5), gxy(15, 0.5)[0], 900)
    icap(f, "a little", "[DIP]", t, td, size=150, y=380)
    return finish(f, n, look="fresh")


# ---- S7: 'Your wake-up signals ease off.' BOARD: a bell rings with big sound waves that shrink to nothing ----
def shot_S7(t, n):
    f = board_bg(); t0 = st_("S7"); k = ramp(t, t0, 0.5)
    P = [(440, 1060), (460, 900)] + _arcpts(540, 900, 80, 120, 180, 360, 16) + [(620, 900), (640, 1060), (440, 1060)]
    draw_on(f, P, k, BP_INK, 8, seed=41)
    draw_ell_on(f, 540, 1090, 26, 22, k, BP_INK, 7, seed=42)
    vol = 1 - ramp(t, T("a3", "ease") - 0.1, 0.9)
    wig = 8 * vol * math.sin(t * 30)
    for sg in (-1, 1):
        for j in range(3):
            r = 150 + j * 60
            if vol > j / 3: draw_on(f, _arcpts(540 + wig, 960, r, r, 90 - sg * 90 - 30, 90 - sg * 90 + 30, 10), 1.0, ACC_S if j == 0 else BP_INK, max(2, int(8 * vol)), seed=43 + j + sg * 7)
    write_on(f, "wake-up signals", 540, 560, t, t0 + 0.15, 62)
    write_on(f, "ease off", 540, 1260, t, T("a3", "ease") - 0.1, 62, ACC_S)
    peek(f, t, 880, 1380, 0.5, "sleepy", (-0.5, -0.4), "sad")
    return finish(f, n, look="fresh")


# ---- S7b: 'Skip lunch completely, and the dip still shows up.' Chubby at the lunch table with an EMPTY plate, the clock says 2:30, he nods off anyway ----
def shot_S7b(t, n):
    f = set_lunch(t); t0 = st_("S7b"); dz = doze(t, t0 + 0.3, 1.9, 1.0)
    comp(f, scale_el(clock_ink_el(110, 5), 1.0), 240, 440); clock_hands(f, 240, 440, 14.5 + 0.3 * (t - t0), 110, 1.0)
    chub(f, 470, 1500, 1.08, t=t, la=(30, 16), ra=(30, 16), mouth=0, **dz)
    cloth_front(f, 1330)
    comp(f, scale_el(thali_el("empty"), 0.75), 470, 1372)
    cc(f, "NO LUNCH", 470, 1500, t, t0 + 0.2, INKC, MILK, 34)
    if t >= T("a3", "still") - 0.1: icap(f, "the dip", "[STILL] SHOWS UP", t, T("a3", "still") - 0.1, size=100, y=380)
    return finish(f, n, look="warm")


# ---- S8: 'So lunch doesn't start the slump. It just lands right on top of it.' BOARD: a thali drops INTO the dip and deepens it ----
def shot_S8(t, n):
    f = board_bg(); t0 = st_("S8"); tl = T("a4", "lands") - 0.1; ttop = T("a4", "top") - 0.15
    deep = ramp(t, ttop + 0.05, 0.4)
    graph(f, t, 1.0, deep=deep, zone=1.0, t_lab=-9)
    x, y = gxy(15, alert_curve(15, deep))
    if t >= tl:
        yy = drop_land(t, ttop - 0.35, 300, y - 50, 0.35)[0] if t < ttop + 0.6 else y - 50
        comp(f, scale_el(thali_el("full"), 0.42), x, yy)
    write_on(f, "doesn't start it", 540, 440, t, T("a4", "start") - 0.2, 56)
    if t >= ttop: icap(f, "lands right", "[ON TOP]", t, ttop, size=120, y=1340)
    return finish(f, n, look="fresh")


# ---- S9: 'Thing two is the meal itself.' PART 2: the heaped thali snaps onto the table, Chubby rubs his hands ----
def shot_S9(t, n):
    f = set_droom(t); t0 = st_("S9"); tm = T("b1", "meal") - 0.15
    rub = 10 * math.sin(t * 22)
    chub(f, 540, 1500, 1.1, t=t, la=(60, 100 + rub), ra=(60, 100 - rub), mouth=3 if t > tm else talk(t), expr="happy", brow="up", look=(0, 0.6))
    table_front(f, 1330)
    if t >= tm - 0.2: comp(f, scale_el(thali_el("full"), 1.05), 540, 1380, scale=snap(t, tm - 0.2, 4))
    t3(f, "THE MEAL", 560, t, tm, 170)
    chapter_card(f, t, t0 + 0.05, 2, "THE MEAL", 1500, 1.8, ACC_L)
    return finish(f, n, look="warm")


# ---- S10: 'As food arrives, your gut starts sending messages up to your brain' BOARD: food drops into the stomach; envelopes run up a line to the brain ----
def shot_S10(t, n):
    f = board_bg(); t0 = st_("S10"); tm = T("b2", "messages") - 0.2
    figure(f, 1.0, 540, 640)
    comp(f, scale_el(brain_ink_el("n", look=(0, 1)), 0.8), 540, 630)
    comp(f, scale_el(stomach_ink_el("happy"), 0.8), 560, 1150)
    q = ramp(t, t0, 0.8); comp(f, scale_el(thali_el("small"), 0.25), 560, 300 + (1100 - 300) * q, op=1 - clamp((q - 0.9) / 0.1))
    P = [(610, 1080), (700, 900), (680, 760), (600, 700)]
    draw_on(f, P, ramp(t, tm - 0.3, 0.5), ACC_S, 6, seed=51)
    for j in range(3):
        qq = (t - tm) * 0.9 - j * 0.3
        if qq > 0: x, y = path_at(P, qq % 1.0); comp(f, scale_el(envelope_el(), 0.55), x, y)
    write_on(f, "gut  >  brain", 540, 1420, t, tm, 50, ACC_S)
    return finish(f, n, look="fresh")


# ---- S10b: '...and your blood sugar shifts too.' BOARD: a sugar cube and a little line that rises and settles ----
def shot_S10b(t, n):
    f = board_bg(); t0 = st_("S10b")
    comp(f, scale_el(sugar_ink_el(), 2.0), 230, 780, scale=pin(t, t0))
    draw_on(f, [(380, 1120), (380, 640)], ramp(t, t0, 0.3), BP_INK, 6, seed=61); draw_on(f, [(380, 1120), (980, 1120)], ramp(t, t0, 0.3), BP_INK, 6, seed=62)
    P = [(380 + 600 * u, 1060 - 340 * math.exp(-((u - 0.35) / 0.2) ** 2) - 60 * u) for u in np.linspace(0, 1, 40)]
    draw_on(f, P, ramp(t, T("b2", "shifts") - 0.4, 1.0), ACC_S, 9, seed=63, wob=0.5)
    write_on(f, "blood sugar", 680, 560, t, T("b2", "blood") - 0.1, 62)
    write_on(f, "shifts", 760, 1240, t, T("b2", "shifts") - 0.1, 56, ACC_S)
    return finish(f, n, look="fresh")


# ---- S11: 'One of the chemicals that keeps you awake is called orexin' : OREXIN pops up on the table: a bright little bulb buddy (define on sight) ----
def shot_S11(t, n):
    f = set_droom(t); t0 = st_("S11"); to = T("b3", "orexin") - 0.25
    chub(f, 250, 1500, 1.0, t=t, **nolean(POSE["present"]), mouth=talk(t), expr="wow", brow="up", look=(1, -0.1), turn=0.5)
    table_front(f, 1330)
    glow(f, 690, 1000, 260, (255, 232, 140), 0.35)
    comp(f, scale_el(orexin_el(1.0, "happy"), 1.35), 690, 1080 + 8 * math.sin(t * 4), scale=pin(t, t0 + 0.1))
    if t >= to:
        comp(f, ed_el("OREXIN", "", lead_col=INKC, lead_size=64), 690, 780, scale=snap(t, to, 4))
        cc(f, "KEEPS YOU AWAKE", 690, 850, t, to + 0.25, ACC_S, MILK, 34)
    src(f, SRC_OX, t, t0 + 0.5, 1466)
    return finish(f, n, look="warm")


# ---- S11b: 'and after you eat, it gets turned down.' Orexin dims and yawns; the room light drops with it; Chubby's lids drop ----
def shot_S11b(t, n):
    t0 = st_("S11b"); kd = ramp(t, T("b3", "turned") - 0.2, 0.9)
    f = set_droom(t, dim=0.35 * kd)
    chub(f, 250, 1500, 1.0, t=t, la=(30, 16), ra=(30, 16), mouth=0, expr="sleepy" if kd > 0.4 else "n", brow="sad" if kd > 0.4 else "n", look=(1, 0.3), turn=0.5, lean=4 * kd, bob=8 * kd)
    table_front(f, 1330)
    comp(f, scale_el(thali_el("empty"), 0.7), 330, 1372)
    glow(f, 690, 1000, 260, (255, 232, 140), 0.35 * (1 - kd))
    comp(f, scale_el(orexin_el(1 - 0.85 * kd, "happy" if kd < 0.3 else "sad"), 1.35), 690, 1080 + 4 * kd)
    if kd > 0.3: zzs(f, 790, 860, t, 3, INKC, 0.8)
    mood(f, ACC_S, 0.3 * kd)
    icap(f, "after you eat, it's", "[TURNED DOWN]", t, T("b3", "turned") - 0.15, size=104, y=400)
    return finish(f, n, look="warm")


# ---- S12: 'Think of it like a dimmer switch on how alert you feel.' ; S12b 'A meal nudges it down.' the knob turns, the room dims (the lighting beat) ----
def dimmer_scene(t, k, light):
    f = set_droom(t, dim=0.5 * (1 - light))
    comp(f, scale_el(dimmer_el(k), 1.25), 600, 860)
    chub(f, 190, 1500, 1.02, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="happy" if light > 0.6 else "sleepy", brow="up" if light > 0.6 else "sad", look=(1, -0.3), hand_r="point", turn=0.5)
    mood(f, ACC_S, 0.35 * (1 - light))
    return f


def shot_S12(t, n):
    f = dimmer_scene(t, 0.12, 1.0)
    icap(f, "a", "[DIMMER SWITCH]", t, T("b4", "dimmer") - 0.15, size=110, y=380)
    return finish(f, n, look="warm")


def shot_S12b(t, n):
    k = ramp(t, T("b4", "nudges") - 0.1, 0.9)
    f = dimmer_scene(t, 0.12 + 0.45 * k, 1 - 0.7 * k)
    if t >= T("b4", "down") - 0.15: icap(f, "a meal nudges it", "[DOWN]", t, T("b4", "down") - 0.15, size=150, y=380, dark=True)
    return finish(f, n, look="warm")


# ---- S13: 'And the bigger the meal, the further it goes.' BOARD: three thalis, small to huge, each dimmer turned further; crash zoom on the biggest ----
def shot_S13(t, n):
    f = board_bg(); t0 = st_("S13"); tb = T("b5", "bigger") - 0.15; tf = T("b5", "further") - 0.15
    for i, (x, s_, kk, kind) in enumerate(((210, 0.38, 0.3, "small"), (530, 0.5, 0.55, "full"), (860, 0.66, 0.9, "full"))):
        ti = tb + i * 0.25
        if t >= ti:
            comp(f, scale_el(thali_el(kind), s_), x, 1160, scale=snap(t, ti, 4))
            kq = 0.1 + (kk - 0.1) * ramp(t, tf + i * 0.12, 0.5)
            comp(f, scale_el(dimmer_el(kq, labels=False), 0.66), x, 820, scale=snap(t, ti + 0.05, 4))
    draw_arrow_on(f, (150, 1340), (960, 1340), ramp(t, tb, 0.8), ACC_S, 7)
    write_on(f, "bigger meal", 540, 1410, t, tb + 0.4, 50, ACC_S)
    f = crash_zoom(f, t, tf + 0.5, 1.22, 860, 1000)
    icap(f, "the bigger the meal, the", "[FURTHER]", t, tf, size=120, y=400)
    return finish(f, n, look="fresh")


# ---- S14: 'In one study, men ate pizza until they couldn't manage another bite.' three guys, pizzas vanishing; Chubby stuffed ----
def shot_S14(t, n):
    f = set_droom(t, dim=0.05); t0 = st_("S14"); tb = T("c1", "another") - 0.1; full = t >= tb
    for i, (x, kind, shirt, s_) in enumerate(((190, "cousin", (90, 150, 210), 0.9), (540, None, None, 1.0), (890, "boss", (230, 140, 60), 0.9))):
        kw = dict(shirt=shirt) if shirt else {}
        chew = math.sin(t * 9 + i)
        chub(f, x, 1500, s_, t=t, la=(30, 16), ra=(40, 20) if full else (130, -120 + 10 * chew), mouth=("wavy" if i == 1 else 0) if full else (2 if chew > 0 else 0),
             expr=("gross" if i == 1 else "sleepy") if full else "happy", brow="up", look=(0, 0.4), squash=0.25 if (full and i == 1) else 0.0, **kw)
        if kind: dress(f, x, 1500, s_, kind, 0)
    table_front(f, 1330)
    for i, x in enumerate((190, 540, 890)):
        left = 1 - ramp(t, t0 + 0.2 + i * 0.1, tb - t0)
        comp(f, scale_el(pizza_el(left), 0.75), x, 1385)
    src(f, SRC_BATH, t, t0 + 0.3, 1466)
    icap(f, "one study: pizza until", "[NO MORE ROOM]", t, t0 + 0.1, size=100, y=400)
    return finish(f, n, look="warm")


# ---- S14b: 'Almost twice as much as normal.' BOARD: NORMAL = one pizza, MAX = two, 'x2' in lavender ----
def shot_S14b(t, n):
    f = board_bg(); t0 = st_("S14b")
    draw_on(f, [(120, 1240), (960, 1240)], ramp(t, t0, 0.3), BP_INK, 6, seed=71)
    comp(f, scale_el(pizza_el(1.0), 0.75), 320, 1110, scale=snap(t, t0 + 0.15, 4))
    write_on(f, "normal", 320, 1310, t, t0 + 0.2, 50)
    for j in range(2):
        tj = T("c1", "twice") - 0.15 + j * 0.2
        if t >= tj: comp(f, scale_el(pizza_el(1.0), 0.75), 760, 1110 - j * 240, scale=snap(t, tj, 4))
    write_on(f, "max", 760, 1310, t, T("c1", "twice"), 50)
    if t >= T("c1", "twice"): rot_comp(f, hand_text_el("x2", 170, ACC_S), 560, 600, -6, snap(t, T("c1", "twice") + 0.1, 4), 1.0)
    return finish(f, n, look="fresh")


# ---- S15: 'Four hours later? Still sleepy.' a comic time card, the clock races 4 hours, then all three are flat out on the sofa ----
def shot_S15(t, n):
    t0 = st_("S15"); ts = T("c2", "Still") - 0.1
    if t < ts:
        f = board_bg(); hrs = 13 + 4 * ramp(t, t0, ts - t0 - 0.1)
        comp(f, scale_el(clock_ink_el(150, 7), 1.3), 540, 1000); clock_hands(f, 540, 1000, hrs, 150, 1.3)
        rot_comp(f, hand_text_el("4 hours later...", 90, ACC_S), 540, 560, -3, snap(t, t0 + 0.05, 4), 1.0)
        return finish(f, n, look="fresh")
    f = set_droom(t, dim=0.15)
    comp(f, sofa_el(), 540, 1340)
    for i, (x, kind, shirt) in enumerate(((290, "cousin", (90, 150, 210)), (540, None, None), (790, "boss", (230, 140, 60)))):
        kw = dict(shirt=shirt) if shirt else {}
        dz = doze(t, ts - 0.4 - i * 0.5, 2.4, 1.0)
        chub(f, x, 1470, 0.82, t=t, la=(40, 20), ra=(40, 20), sit=True, mouth=0, **dz, **kw)
        if kind: dress(f, x, 1470, 0.82, kind, dz["lean"])
    zzs(f, 700, 820, t - ts, 3, INKC, 1.0)
    icap(f, "", "STILL [SLEEPY]", t, ts, size=130, y=420)
    return finish(f, n, look="golden")


# ---- S16: 'To be fair, scientists still don't know every piece of this.' BOARD: a jigsaw puzzle draws itself with two pieces missing ----
def puzzle(f, t, t0, done=False):
    for r in range(2):
        for c in range(3):
            i = r * 3 + c; x0, y0 = 210 + c * 220, 640 + r * 220
            if i in (2, 4) and not done: continue
            if i == 4: continue
            k = ramp(t, t0 + i * 0.12, 0.4)
            P = [(x0, y0), (x0 + 80, y0), (x0 + 80, y0 - 22), (x0 + 120, y0 - 22), (x0 + 120, y0), (x0 + 200, y0), (x0 + 200, y0 + 200), (x0, y0 + 200)]
            draw_on(f, P, k, BP_INK, 6, seed=80 + i, closed=True)
    for i in ((4,) if done else (2, 4)):
        r, c = divmod(i, 3); x0, y0 = 210 + c * 220, 640 + r * 220
        draw_on(f, [(x0, y0), (x0 + 200, y0), (x0 + 200, y0 + 200), (x0, y0 + 200)], 1.0, BP_GRID2, 4, seed=90 + i, closed=True)
        write_on(f, "?", x0 + 100, y0 + 100, t, t0 + 0.6, 110, ACC_S)


def shot_S16(t, n):
    f = board_bg(); t0 = st_("S16")
    puzzle(f, t, t0 + 0.05)
    write_on(f, "not every piece known", 540, 470, t, T("c3", "every") - 0.3, 56)
    peek(f, t, 860, 1340, 0.55, "sus", (-0.5, -0.4))
    src(f, "Cleveland Clinic: 'researchers still aren't clear' · Healthline", t, t0 + 0.4, 1466)
    return finish(f, n, look="fresh")


# ---- S16b: 'But the blood part? That one's settled.' the 'blood' piece drops in with a crossed drop; SETTLED stamp ----
def shot_S16b(t, n):
    f = board_bg(); t0 = st_("S16b"); ts = T("c3", "settled") - 0.1
    puzzle(f, t, -9, done=True)
    x0, y0 = 210 + 2 * 220, 640
    yy = drop_land(t, t0 + 0.1, 200, y0 + 100, 0.3)[0]
    comp(f, scale_el(blood_el("sad"), 0.65), x0 + 100, yy)
    if t >= t0 + 0.4:
        for sg in (-1, 1): cv2.line(f, (x0 + 30, int(y0 + 100 - sg * 70)), (x0 + 170, int(y0 + 100 + sg * 70)), C(BLOOD_S), 16, cv2.LINE_AA)
    write_on(f, "blood leaves the brain", 540, 470, t, T("c3", "blood") - 0.1, 52, BLOOD_C)
    slam(f, vstamp_el("SETTLED: MYTH", ACC_S, 80), 540, 1220, -6, t, ts)
    peek(f, t, 860, 1380, 0.5, "smirk", (-0.5, -0.4))
    return finish(f, n, look="fresh")


# ---- S17: 'So, Diwali lunch tomorrow. How do you stay awake?' PART 3: the full table; Chubby fists up, ink title ----
def shot_S17(t, n):
    f = set_droom(t); t0 = st_("S17"); ta = T("d0", "awake") - 0.15
    pk = pose_keys(t, [(t0, POSE["idle"]), (T("d0", "How") - 0.1, POSE["cheer"])])
    chub(f, 540, 1500, 1.08, t=t, **nolean(pk), mouth=talk(t), expr="happy" if t < ta else "smirk", brow="up", look=(0, -0.2))
    table_front(f, 1330)
    for x in (230, 850): comp(f, scale_el(thali_el("full"), 0.6), x, 1372)
    t3(f, "STAY AWAKE?", 560, t, ta, 160)
    chapter_card(f, t, t0 + 0.05, 3, "DIWALI LUNCH", 1520, 1.6, ACC_L)
    return finish(f, n, look="warm")


# ---- S18: 'One, a smaller plate.' Chubby slides the heaped thali away and takes the small one ; S18b 'You can always go back for seconds later.' ----
def shot_S18(t, n):
    f = set_droom(t); t0 = st_("S18"); ts = T("d1", "smaller") - 0.15; e = eye_lead(t, ts - 0.3, 1.0, -1.0)
    chub(f, 540, 1500, 1.05, t=t, la=(60, 40), ra=(60, 40), mouth=talk(t), expr="sus" if t < ts else "happy", brow="sus" if t < ts else "up", look=e["look"], turn=e["turn"], blink=e["blink"])
    table_front(f, 1330)
    xf = 760 + 300 * ramp(t, ts + 0.2, 0.5)
    comp(f, scale_el(thali_el("full"), 0.75), xf, 1372)
    xs = 300 + 120 * ramp(t, ts + 0.2, 0.5)
    comp(f, scale_el(thali_el("small", "happy" if t > ts else None), 0.62), xs, 1372)
    if t >= ts: cv2.ellipse(f, (int(xs), 1372), (200, 120), 0, 0, 360, C(ACC), 9, cv2.LINE_AA)
    icap(f, "1  ·  a", "[SMALLER] PLATE", t, ts, size=110, y=400)
    return finish(f, n, look="warm")


def shot_S18b(t, n):
    f = set_droom(t); t0 = st_("S18b")
    chub(f, 540, 1500, 1.05, t=t, **nolean(POSE["think"]), mouth=talk(t), expr="smirk", brow="up", look=(0.6, -0.4), turn=0.3)
    table_front(f, 1330)
    comp(f, scale_el(thali_el("small"), 0.62), 420, 1372)
    comp(f, scale_el(clock_ink_el(90, 9), 1.0), 820, 720, scale=pin(t, t0 + 0.1)); clock_hands(f, 820, 720, 13 + 1.0 * ramp(t, t0, 2.0), 90, 1.0)
    cc(f, "SECONDS? LATER.", 820, 860, t, T("d1", "seconds") - 0.15, ACC_S, MILK, 36)
    return finish(f, n, look="warm")


# ---- S19: 'Two, walk it off.' the Diwali lane: Chubby walks it off (walk cycle, parallax) ; S19b 'Ten or fifteen minutes, right after you eat.' ----
def lane_walk(t, t0):
    camx = 300 * (t - t0); f = set_lane(t, camx + 600)
    w = walk(t, 520, 1500, 1.08, speed=300, t0=t0, track=True)
    chub(f, s=1.08, t=t, mouth=talk(t), expr="happy", brow="up", **w)
    lane_front(f, camx + 600)
    return f


def shot_S19(t, n):
    t0 = st_("S19"); f = lane_walk(t, t0)
    icap(f, "2  ·", "[WALK] IT OFF", t, T("d2", "walk") - 0.15, size=130, y=400, dark=True)
    return finish(f, n, look="golden")


def shot_S19b(t, n):
    f = lane_walk(t, st_("S19"))
    cc(f, "10 TO 15 MINUTES", 540, 420, t, T("d2", "Ten") - 0.1, ACC_S, MILK, 48)
    cc(f, "RIGHT AFTER YOU EAT", 540, 500, t, T("d2", "right") - 0.1, INKC, MILK, 34)
    src(f, "Source: Cleveland Clinic", t, st_("S19b") + 0.3, 1466)
    return finish(f, n, look="golden")


# ---- S20: 'Three, get a proper night's sleep tonight.' night room, moon, Chubby in lavender pyjamas yawns, clock at 10:30 ----
def shot_S20(t, n):
    f = set_droom(t, dim=0.45); t0 = st_("S20"); ty = T("d3", "sleep") - 0.3
    moon_icon(f, 270, 700, 70, (40, 30, 80))
    chub(f, 600, 1500, 1.08, t=t, **(nolean(POSE["yawn"]) if t > ty else POSE["idle"]), shirt=ACC_L, mouth="jaw" if ty < t < ty + 0.9 else talk(t), expr="sleepy", brow="sad", look=(0, -0.2))
    comp(f, scale_el(clock_ink_el(80, 11), 1.0), 880, 560); clock_hands(f, 880, 560, 22.5, 80, 1.0)
    icap(f, "3  ·  proper", "[SLEEP] TONIGHT", t, T("d3", "proper") - 0.15, size=110, y=400, dark=True)
    return finish(f, n, look="night")


# ---- S21: 'And if your eyes feel heavy, don't drive.' Chubby nods off holding the car keys, jerks awake: STOP ; S21b 'Hand someone else the keys.' ----
def shot_S21(t, n):
    f = set_droom(t, dim=0.1); t0 = st_("S21"); td = T("d4", "dont") - 0.1
    if t < td:
        dz = doze(t, t0 - 0.6, 1.6, 1.0)
        chub(f, 540, 1500, 1.1, t=t, la=(30, 16), ra=(120, 160), hold=scale_el(keys_el(), 0.7), hold_off=(10, -30), mouth=0, **dz)
        icap(f, "eyes feel", "[HEAVY]?", t, T("d4", "heavy") - 0.15, size=130, y=400)
    else:
        tk = take(t, td)
        chub(f, 540, 1500 + tk["dy"], 1.1, t=t, **nolean(POSE["stop"]), mouth=talk(t), expr="sus", brow="sus", look=(0, 0), squash=tk["squash"], lean=tk["lean"])
        slam(f, vstamp_el("DON'T DRIVE", BLOOD_C, 90), 540, 560, -5, t, td + 0.05)
    return finish(f, n, look="warm")


def shot_S21b(t, n):
    f = set_droom(t, dim=0.05); t0 = st_("S21b"); tk_ = T("d4", "keys") - 0.4
    chub(f, 260, 1500, 1.02, t=t, la=(24, 14), ra=(80, 40), mouth=talk(t), expr="sleepy", brow="sad", look=(1, 0), turn=0.5)
    chub(f, 820, 1500, 1.02, t=t, la=(24, 14), ra=(24, 14), shirt=(220, 80, 130), mouth=0, expr="happy", brow="up", look=(-1, 0), turn=-0.5)
    dress(f, 820, 1500, 1.02, "aunty")
    q = ramp(t, tk_, 0.6); x = 380 + (700 - 380) * q; y = 1180 - 260 * math.sin(math.pi * q)
    rot_comp(f, keys_el(), x, y, 360 * q, 0.7, 1.0, 0.2)
    icap(f, "hand someone else", "THE [KEYS]", t, t0 + 0.05, size=120, y=400)
    return finish(f, n, look="warm")


# ---- S22: 'If you're wiped out after nearly every meal, or you're always thirsty too, it's worth seeing a doctor.' BOARD (caution: calm) ----
def shot_S22(t, n):
    f = board_bg(); t0 = st_("S22")
    for i, x in enumerate((230, 540, 850)):
        comp(f, scale_el(thali_el("small"), 0.56), x, 820, scale=snap(t, t0 + 0.1 + i * 0.12, 4))
        if t > T("e1", "every") - 0.2: zzs(f, x + 90, 740, t, 2, BP_INK, 0.9)
    write_on(f, "wiped out after", 540, 470, t, T("e1", "wiped") - 0.1, 54)
    write_on(f, "nearly every meal", 540, 560, t, T("e1", "nearly") - 0.1, 54, ACC_S)
    peek(f, t, 540, 1180, 0.6, "sad", (0, -0.4), "sad")
    return finish(f, n, look="fresh")


def shot_S22b(t, n):
    f = board_bg(); t0 = st_("S22b"); td = T("e1", "doctor") - 0.25
    comp(f, scale_el(glass2_el((150, 200, 240), 0.3), 1.4), 300, 820, scale=snap(t, T("e1", "always") - 0.1, 4))
    write_on(f, "always thirsty", 300, 1080, t, T("e1", "thirsty") - 0.1, 50)
    draw_arrow_on(f, (450, 820), (620, 820), ramp(t, T("e1", "worth") - 0.2, 0.4), ACC_S, 7)
    if t >= td:
        comp(f, scale_el(steth_el(), 1.4), 760, 820, scale=snap(t, td, 4))
        write_on(f, "see a doctor", 760, 1080, t, td + 0.1, 48, ACC_S)
    src(f, "Source: Cleveland Clinic · Healthline", t, t0 + 0.3, 1466)
    return finish(f, n, look="fresh")


# ---- S23: 'So it's your body clock, plus a dimmer switch. Not your blood running away.' BOARD recap card ----
def shot_S23(t, n):
    f = board_bg(); t0 = st_("S23"); tc = T("f1", "body") - 0.15; td = T("f1", "dimmer") - 0.15; tn = T("f1", "Not") - 0.1
    if t >= tc:
        comp(f, scale_el(clock_ink_el(110, 13), 1.0), 250, 720, scale=snap(t, tc, 4)); clock_hands(f, 250, 720, 15.0, 110, 1.0)
        write_on(f, "body clock", 250, 880, t, tc + 0.1, 46)
    if t >= td:
        write_on(f, "+", 410, 720, t, td - 0.1, 110, ACC_S)
        comp(f, scale_el(dimmer_el(0.6, labels=False), 0.6), 590, 720, scale=snap(t, td, 4))
        write_on(f, "dimmer", 590, 880, t, td + 0.1, 46)
        write_on(f, "=", 770, 720, t, td + 0.4, 110, ACC_S)
        if t >= td + 0.4: chub_head_only(f, 905, 720, 0.6, t, mouth=0, expr="sleepy", brow="sad")
    if t >= tn:
        comp(f, scale_el(blood_el("sad"), 1.3), 540, 1160, scale=snap(t, tn, 4))
        k = ramp(t, T("f1", "away") - 0.1, 0.2)
        for sg in (-1, 1): draw_on(f, [(410, 1160 - sg * 130), (670, 1160 + sg * 130)], k, BLOOD_S, 18, seed=100 + sg)
        write_on(f, "not your blood running away", 540, 1340, t, tn + 0.1, 46, BLOOD_C)
    comp(f, chip("SAVE THIS", INKC, ACC_L, 34), 540, 330, op=clamp((t - t0) / 0.2))
    write_on(f, "why a big meal makes you sleepy", 540, 450, t, t0 + 0.1, 38)
    return finish(f, n, look="fresh")


# ---- S24: 'Send this to whoever's planning a nap right after Diwali lunch.' phone + nodding Chubby ; then the logo ----
def shot_S24(t, n):
    t0 = st_("S24"); f = set_droom(t); vend = LINES["f2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("f2", "Send") + 0.25
        comp(f, scale_el(phone2_el("nap after lunch? blame the clock", "not your blood leaving your brain", pr), 0.82), 760, 960, scale=pin(t, t0))
        if pr and t < T("f2", "Send") + 0.7:
            rr = (t - T("f2", "Send") - 0.25) / 0.45; cv2.circle(f, (760, 1230), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        dz = doze(t, T("f2", "nap") - 0.3, 2.0, 0.6) if t > T("f2", "nap") - 0.3 else dict(expr="smirk", brow="up", look=(1, -0.1))
        chub(f, 290, 1500, 1.05, t=t, la=(20, 12), ra=(70, 40), mouth=talk(t), hand_r="point", turn=0.5, **dz)
        ui_word(f, "send this to whoever's planning", "A [NAP] AFTER LUNCH", 440, t, T("f2", "Send") - 0.05, col=INKC, acc=ACC_S, size=84)
    else:
        f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32); k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INKC, lead_size=42), 540, 1030, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 540, 1500, 0.7, t=t, la=(150, 170), ra=(150, 170), mouth=3, expr="happy", brow="up")
    return finish(f, n, look="golden")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TN, 0.4, 16), (T("i1", "brain") - 0.05, 0.25, 8), (T("i2", "out") - 0.05, 0.45, 18), (T("i3", "myth") - 0.05, 0.45, 18), (T("i4", "new") - 0.1, 0.3, 10),
           (T("a1", "body") - 0.15, 0.3, 10), (T("a2", "dip") - 0.1, 0.3, 10), (T("a3", "still") - 0.1, 0.25, 8), (T("a4", "top") - 0.12, 0.45, 18),
           (T("b1", "meal") - 0.15, 0.35, 12), (T("b3", "orexin") - 0.25, 0.25, 8), (T("b4", "down") - 0.15, 0.3, 10), (T("b5", "further") + 0.35, 0.35, 14),
           (T("c1", "twice") - 0.15, 0.3, 10), (T("c2", "Still") - 0.1, 0.35, 12), (T("c3", "settled") - 0.1, 0.4, 16),
           (T("d0", "awake") - 0.15, 0.3, 10), (T("d1", "smaller") - 0.15, 0.25, 8), (T("d4", "dont") - 0.1, 0.4, 16), (T("e1", "doctor") - 0.25, 0.2, 6), (T("f2", "Send") + 0.25, 0.2, 8)]


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
        if k == "erase" and dt < 0.42:
            f = erase_mix(rs(SHOTS[i - 1]["id"], t, n), f, dt / 0.42)
        elif k == "focus" and dt < 0.34:
            p = dt / 0.34; prv = rs(SHOTS[i - 1]["id"], t, n); m = eio(p)
            f = _bl(prv, 40 * m) * (1 - m) + _bl(f, 40 * (1 - m)) * m
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
