# ================= shots: FreshNestHub 20 — "Is leftover rice safe? The risky part isn't the reheating." (Chubby INK, ep 4 of the ink look) ===
# COLOUR SCRIPT (5-colour ink palette + ONE accent): WARM ORANGE accent = the 'warm hours' (the germs, the toxin, the warm zone, titles, chips);
# COLD BLUE = the fridge + the fixes; paper = the rice. Places: the NEW night stove (set_stove_night: lights off, moonlit window, one warm lamp
# pooling on the pot) for every 'it sat out' moment, the day stove for cooking, the fridge at night, the lunch table for the happy ending, paper
# stages for the diagrams. CRAFT (ep 20): CAMERA LANGUAGE — each move carries one meaning: a CCTV handheld drift for the night (urgency, 'caught
# on camera'), a DUTCH ANGLE when the warm hours start (unease), CRASH ZOOMS on the punchlines (comic beat / realisation), a RACK FOCUS from
# Chubby to the bowl when the toxin is 'still there' (attention moves without a cut), a slow PUSH-IN on the mnemonic recap.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i2", "It's") - 0.15, "punch"), ("S1", T("i3", "And") - 0.2, "whip"),
    ("S2", T("a1", "Okay.") - 0.2, "flash"), ("S2b", T("a1", "germ") - 0.15, "zoom"),
    ("S3", T("a2", "It") - 0.2, "whip"), ("S3b", T("a2", "like", 1) - 0.12, "punch"),
    ("S4", T("a3", "And") - 0.2, "whip"), ("S4b", T("a3", "some") - 0.15, "zoom"),
    ("S5", T("a4", "On") - 0.2, "focus"),
    ("S6", T("b1", "The") - 0.2, "flash"), ("S6b", T("b1", "That's") - 0.15, "zoom"),
    ("S7", T("b2", "They") - 0.2, "whip"), ("S7b", T("b2", "At") - 0.15, "punch"),
    ("S8", T("b3", "Two") - 0.2, "whip"), ("S8b", T("b3", "and") - 0.12, "zoom"),
    ("S9", T("b4", "And") - 0.2, "whip"),
    ("S10", T("b5", "This") - 0.2, "flash"), ("S10b", T("b5", "Microwave") - 0.15, "whip"),
    ("S11", T("b6", "So") - 0.2, "whip"),
    ("S12", T("b7", "And") - 0.2, "punch"), ("S12b", T("b7", "Leftover") - 0.15, "zoom"),
    ("S13", T("c1", "So,") - 0.2, "whip"), ("S13b", T("c2", "Nope.") - 0.12, "flash"),
    ("S14", T("d1", "Right,") - 0.2, "whip"), ("S15", T("d2", "When") - 0.2, "zoom"),
    ("S16", T("d3", "As") - 0.2, "whip"), ("S16b", T("d4", "That") - 0.2, "punch"),
    ("S17", T("d5", "Heat") - 0.2, "whip"), ("S17b", T("d5", "So") - 0.15, "punch"),
    ("S18", T("e1", "The") - 0.2, "flash"),
    ("S19", T("e2", "One,") - 0.2, "whip"), ("S19b", T("e2", "Spread") - 0.15, "zoom"),
    ("S20", T("e3", "Two,") - 0.2, "whip"), ("S20b", T("e3", "Three,") - 0.12, "punch"), ("S20c", T("e3", "Four,") - 0.12, "punch"),
    ("S21", T("e4", "And") - 0.2, "focus"),
    ("S22", T("f1", "Good") - 0.2, "flash"),
    ("S23", T("g1", "So") - 0.2, "whip"), ("S24", T("g2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
SRC_S = "Source: Food Standards Scotland · McGill OSS"
SRC_M = "Source: McGill Office for Science and Society"
SRC_U = "Source: University of Florida IFAS · McGill OSS"
SRC_R = "Source: Indiana Public Media (A Moment of Science)"
SRC_C = "Source: HealthyWA · Hong Kong Centre for Food Safety"


def lt(t, sid): return t - SHOT[sid]["start"]


def st_(sid): return SHOT[sid]["start"]


def en_(sid): return SHOT[sid]["end"]


def ui_word(f, lead, big, y, t, t0, col=INKC, acc=ACC, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def icap(f, lead, big, t, t0, acc=ACC, size=170, y=470, out=None, tail="", dark=False):
    """ink caption: warm-ink text on paper sets, white with shadow on dark sets."""
    if dark: ui_word(f, lead, big, y, t, t0, col=WHITE, acc=acc, size=size, shadow=0.6, lead_col=WHITE, out=out, tail=tail)
    else: ui_word(f, lead, big, y, t, t0, col=INKC, acc=acc, size=size, shadow=0.0, lead_col=INKC, out=out, tail=tail)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def ring(f, x, y, r, col, th=8, op=1.0):
    ov = f.copy(); cv2.circle(ov, (int(x), int(y)), int(r), C(col), th, cv2.LINE_AA); f[:] = f * (1 - op) + ov * op


def munch(t, rate=0.42):
    ph = (t / rate) % 1.0
    return (2 if ph < 0.5 else 0), int(t / rate)


def ichip(text, size=26, inv=False): return chip(text, INKC if not inv else MILK, MILK if not inv else INKC, size)


def achip(text, size=30): return chip(text, ACC_S, MILK, size)


def bchip(text, size=30): return chip(text, BLUE_S, MILK, size)


def mchip(text, size=30): return chip(text, INK_MINT_S, MILK, size)


def t3(f, text, y, t, t0, size=260, face=None, side=None, x=540):
    """ink 3D title in the accent, snaps in (drawn BEFORE Chubby / the hero)."""
    if t >= t0: title_ink(f, text, y, t, t0, size=size, face=face or ACC_L, side=side or ACC_S, depth=18, x=x)


HOB = 1300


def nolean(p): return {k: v for k, v in p.items() if k != "lean"}
TISNT = T("i1", "isn't") - 0.12


def pot_on_stove(f, warm=0.0, lid=False, mood_=None, x=540, s=1.0):
    comp(f, scale_el(rice_pot_el(0.75, warm, lid, 1, mood_), s), x, HOB - 172 * s)


def night_clock(f, t, x, y, h0, h1, t0, t1, s=0.8):
    comp(f, scale_el(clock_ink_el(), s), x, y)
    clock_hands(f, x, y, h0 + (h1 - h0) * clamp((t - t0) / max(1e-3, t1 - t0)), 110, s)


def hhmm(h):
    h = h % 24; return f"{int(h):02d}:{int((h % 1) * 60):02d}"


# ---- S0: HOOK — CCTV 'KITCHEN CAM': after dinner, Chubby yawns and walks off; the rice pot stays on the stove under the lamp; the timestamp
#      races; on 'isn't' a crash zoom on the pot + 'NOT THE REHEATING' ----
def shot_S0(t, n):
    f = set_stove_night(t)
    warm = 0.25 + 0.75 * ramp(t, 0.3, 3.0)
    pot_on_stove(f, warm)
    steam_wisps(f, 540, 1000, t, 3, 150, 160, (255, 236, 210), 0.45 * (1 - 0.6 * ramp(t, 0, 3)), 4)
    xk = 330 - 330 * ramp(t, 0.9, 2.2)
    pose = nolean(POSE["yawn"] if t < 1.6 else POSE["idle"])
    chub(f, xk, 1500, 0.95, t=t, **pose, mouth="jaw" if 0.2 < t < 1.3 else 0, expr="sleepy", brow="sad", look=(-0.8, 0), lean=-4)
    hh = 22.2 + 5.4 * ramp(t, 0.2, max(0.5, TISNT - 0.2))
    dx, dy, rot = handheld(t, 0.8, 1)
    f = cam(f, 1.0, 540, 1000, dx, dy, rot)
    f = crash_zoom(f, t, TISNT, 1.25, 540, 1100)
    f = cctv(f, t, "KITCHEN CAM", hhmm(hh))
    icap(f, "the risky part of leftover rice", "", t, 0.1, size=120, dark=True, y=700, out=TISNT - 0.05)
    if t >= TISNT: icap(f, "the risky part isn't", "[REHEATING]", t, TISNT, size=150, dark=True, y=700)
    return finish(f, n, look="night")


# ---- S0b: 'It's the hours it spends sitting in the pot before it ever makes it to the fridge' — the night stove, a wall clock spinning,
#      ink title THE HOURS behind the glowing pot; FRIDGE: TOO LATE ----
def shot_S0b(t, n):
    f = set_stove_night(t, 1.2)
    th = T("i2", "hours") - 0.12; tf = T("i2", "fridge.") - 0.12
    t3(f, "THE HOURS", 780, t, th, 230)
    night_clock(f, t, 170, 1010, 22.5, 27.0, st_("S0b"), en_("S0b"), 0.7)
    pot_on_stove(f, 1.0, mood_="n")
    steam_wisps(f, 540, 1000, t, 3, 150, 160, (255, 236, 210), 0.3, 4)
    if t >= tf: slam(f, bchip("FRIDGE: TOO LATE", 34), 540, 1460, 3, t, tf)
    icap(f, "it's the", "[HOURS] in the pot", t, st_("S0b") + 0.05, size=150, dark=True, out=th - 0.05)
    if t >= tf - 0.35: icap(f, "...before it gets to the", "[FRIDGE]", t, tf - 0.35, acc=BLUE_L, size=130, dark=True, y=470)
    return finish(f, n, look="night")


# ---- S1: OPEN LOOP — 'why it turns into little pebbles in there' — fridge at night: Chubby holds a bowl of hard rice; jaw drop + crash zoom ----
def shot_S1(t, n):
    f = set_fridge_night(t)
    tp = T("i3", "pebbles") - 0.12
    tk = take(t, tp, 1.0, 8)
    chub(f, 330, 1500, 0.95, t=t, **nolean(POSE["hold_up"] if t < tp else POSE["shock"]), mouth="jaw" if t >= tp else talk(t), expr=tk["expr"] if t >= tp else "sus",
         brow=tk["brow"] if t >= tp else "sus", look=(0.8, 0), lean=tk["lean"] + 4, squash=tk["squash"], bob=tk["dy"], hand_r="grip",
         hair=(drag(t, lambda q: take(q, tp, 1.0, 8)["dy"], 3, 0.8), 0))
    comp(f, scale_el(rice_bowl_el("hard", 1, "sad" if t >= tp else None), 0.9), 690, 1040 + 4 * math.sin(t * 2))
    if t >= tp: comp(f, achip("PEBBLES?! COMING UP", 30), 690, 1460, scale=pin(t, tp, 0.25))
    icap(f, "and why it turns into little", "[PEBBLES]", t, st_("S1") + 0.05, size=170, dark=True)
    f = crash_zoom(f, t, tp, 1.2, 600, 760)
    return finish(f, n, look="cool")


# ---- S2: PART 1 — 'Raw rice often carries a tiny stowaway' — kitchen: Chubby with a bowl of rice; a magnifier inset finds a sleeping spore ----
def shot_S2(t, n):
    f = inkify(set_kitchen(t), 0.13)
    ts = T("a1", "stowaway,") - 0.12
    chub(f, 300, 1500, 1.0, t=t, **POSE["hold_up"], mouth=talk(t), expr="n", brow="up", look=(0.8, -0.2), hand_r="grip")
    counter_front(f, 1330)
    comp(f, scale_el(rice_bowl_el("fluffy", 3), 0.95), 690, 1260)
    def close(g):
        g[:] = np.array(C(RICE_H), np.float32)
        for i in range(10): comp(g, scale_el(grain_el("n", False, (0, 0), 2 + i), 0.5), 590 + (i % 5) * 70 - 140, 780 + (i // 5) * 150)
        comp(g, scale_el(spore_el("sleepy"), 0.9), 730, 860 + 4 * math.sin(t * 2))
    if t >= ts: inset(f, 730, 860, 200, close, ramp(t, ts, 0.3), MILK, 10)
    if t >= ts + 0.2: label_at(f, "A STOWAWAY", 730, 610, t, ts + 0.2, 730, 680, bg=ACC_S, fg=MILK, size=30)
    chapter_card(f, t, st_("S2") + 0.05, 1, "THE STOWAWAY", y=1440, dur=1.5, col=ACC_L)
    icap(f, "raw rice carries a tiny", "[STOWAWAY]", t, st_("S2") + 0.05, size=160)
    return finish(f, n, look="warm")


# ---- S2b: 'a germ called Bacillus cereus' — the germ big on a warm paper stage, name chip; Chubby points ----
def shot_S2b(t, n):
    f = ink_set("warmp", (255, 255, 255), 600, 980, 420)
    tb = T("a1", "Bacillus") - 0.12
    comp(f, scale_el(germ_el("happy", (-0.6, 0), 1, int(t * 8) % 4), 1.9), 640, 980 + 6 * math.sin(t * 3), scale=snap(t, st_("S2b") + 0.05, 4, 2.0))
    label_at(f, "A GERM", 640, 760, t, st_("S2b") + 0.15, 640, 820, bg=INKC, fg=MILK, size=30)
    if t >= tb: slam(f, achip("BACILLUS CEREUS", 44), 640, 1250, -3, t, tb)
    chub(f, 190, 1500, 0.85, t=t, **POSE["point"], mouth=talk(t), expr="n", brow="up", look=(1, -0.3), hand_r="point")
    icap(f, "a germ called", "", t, st_("S2b") + 0.05, size=150)
    return finish(f, n, look="warm")


# ---- S3: 'It hides inside a spore' — the germ curls up and the armoured shell closes round it (scale swap with a snap) ----
def shot_S3(t, n):
    f = ink_set("warmp", (255, 255, 255), 540, 980, 420)
    th = T("a2", "hides") - 0.12; tsp = T("a2", "spore,") - 0.12
    k = ramp(t, th, 0.45)
    if k < 1: comp(f, scale_el(germ_el("wow" if t >= th else "n", (0, 0), 1, int(t * 8) % 4), 1.6 * (1 - 0.6 * k)), 600, 1000, op=1 - k * 0.8)
    if k > 0.4: comp(f, spore_el("sleepy"), 600, 1000, scale=1.7 * snap(t, th + 0.25, 4, 2.0))
    if t >= tsp: label_at(f, "A SPORE", 600, 720, t, tsp, 600, 790, bg=ACC_S, fg=MILK, size=34)
    chub(f, 180, 1500, 0.8, t=t, **POSE["think"], mouth=talk(t), expr="sus", brow="sus", look=(1, -0.3))
    icap(f, "it hides inside a", "[SPORE]", t, st_("S3") + 0.05, size=190)
    return finish(f, n, look="warm")


# ---- S3b: 'like a seed wearing armour' — SEED + ARMOUR = SPORE as an ink equation ----
def shot_S3b(t, n):
    f = ink_set("ricep", (255, 255, 255), 540, 980, 420)
    ts = st_("S3b") + 0.05; ta = T("a2", "armour.") - 0.12
    if t >= ts:
        comp(f, scale_el(grain_el("happy", False, (0, 0), 7), 0.8), 210, 1000, scale=snap(t, ts, 4, 2.0))
        label_at(f, "SEED", 210, 800, t, ts, 210, 860, bg=INKC, fg=MILK, size=28)
    if t >= ta - 0.2: comp(f, ed_el("+", "", lead_col=INKC, lead_size=110), 365, 1000, op=clamp((t - ta + 0.2) / 0.15))
    if t >= ta:
        comp(f, _rot_el(scale_el(spore_el("n", 0, 3), 0.55), 20), 520, 1000, scale=snap(t, ta, 4, 2.0))
        label_at(f, "ARMOUR", 520, 800, t, ta, 520, 860, bg=INKC, fg=MILK, size=28)
        comp(f, ed_el("=", "", lead_col=INKC, lead_size=110), 680, 1000, op=clamp((t - ta - 0.2) / 0.15))
    if t >= ta + 0.3: comp(f, spore_el("sleepy"), 860, 1000, scale=1.1 * snap(t, ta + 0.3, 4, 2.0))
    icap(f, "a seed wearing", "[ARMOUR]", t, st_("S3b") + 0.05, size=190)
    return finish(f, n, look="warm")


# ---- S4: 'boiling can't crack that armour' — the stove ON, a cut-away pot of boiling water; spores bob in it unharmed; Chubby double-takes ----
def shot_S4(t, n):
    f = set_stove(t, on=1.0)
    tc = T("a3", "crack") - 0.12
    comp(f, pot_el("water", 0.62, 0.0), 540, HOB - 225 + 8)
    rising_bubbles(f, 540, 1230, 1050, t, 300, 8, 14, 160, 3)
    for i in range(3):
        comp(f, scale_el(spore_el("happy" if t >= tc else "n", 0, 4 + i), 0.42), 440 + i * 100, 1130 + 14 * math.sin(t * 5 + i * 2))
    side_flames(f, 540, 1298, t, 470)
    dt_ = double_take(t, tc)
    chub(f, 170, 1500, 0.85, t=t, **nolean(POSE["shrug"]), mouth=talk(t), expr=dt_[2], brow=dt_[3], look=dt_[0], lean=dt_[1])
    if t >= tc: slam(f, achip("CAN'T CRACK IT", 38), 540, 1460, -3, t, tc)
    icap(f, "boiling can't", "[CRACK] the armour", t, st_("S4") + 0.05, size=140)
    return finish(f, n, look="warm")


# ---- S4b: 'some spores are still in your pot, fast asleep' — the cooked pot; a magnifier inset of grains with sleeping spores tucked in ----
def shot_S4b(t, n):
    f = set_stove(t, on=0.0)
    tas = T("a3", "asleep.") - 0.15
    pot_on_stove(f, 0.0)
    steam_wisps(f, 540, 1000, t, 4, 160, 180, (255, 255, 255), 0.6, 4)
    def close(g):
        g[:] = np.array(C(RICE_H), np.float32)
        for i in range(12): comp(g, _rot_el(scale_el(grain_el("n", False, (0, 0), 9 + i), 0.42), (i * 37) % 60 - 30), 330 + (i % 4) * 140, 760 + (i // 4) * 130)
        for i, (x, y) in enumerate(((420, 820), (620, 920), (500, 1020))): comp(g, scale_el(spore_el("sleepy", 0, 5 + i), 0.5), x, y + 3 * math.sin(t * 2 + i))
    inset(f, 540, 900, 230, close, ramp(t, st_("S4b") + 0.1, 0.3), MILK, 10)
    if t >= tas: slam(f, ichip("STILL THERE. ASLEEP.", 34), 540, 1460, -2, t, tas)
    icap(f, "still in your pot,", "[ASLEEP]", t, st_("S4b") + 0.05, size=170, y=430)
    return finish(f, n, look="warm")


# ---- S5: 'on their own, that's fine, because sleeping spores don't hurt anybody' — lunch table, a snoozing spore by the bowl, a check ----
def shot_S5(t, n):
    f = set_lunch(t)
    tf = T("a4", "fine,") - 0.12
    chub(f, 300, 1500, 0.95, t=t, **nolean(POSE["shrug"]), mouth=talk(t), expr="happy", brow="up", look=(0.7, 0), lean=moving_hold(t, 2)["lean"])
    cloth_front(f, 1330)
    comp(f, scale_el(rice_bowl_el("fluffy", 4), 0.8), 720, 1280)
    comp(f, scale_el(spore_el("sleepy", 0, 6), 0.55), 760, 1000 + 5 * math.sin(t * 1.5))
    if t >= tf: comp(f, check_el(54, True), 880, 880, scale=pin(t, tf, 0.25)); comp(f, mchip("ASLEEP = HARMLESS", 32), 720, 1460, scale=pin(t, tf + 0.1, 0.25))
    icap(f, "on their own, that's", "[FINE]", t, st_("S5") + 0.05, acc=INK_MINT_S, size=190)
    return finish(f, n, look="golden")


# ---- S6: PART 2 'The trouble starts when the pot just sits there, warm and damp, for hours' — the night stove, a DUTCH ANGLE eases in
#      (unease), the clock races, the thermometer climbs into the warm zone ----
def shot_S6(t, n):
    f = set_stove_night(t, 1.2)
    tw = T("b1", "warm") - 0.1; tho = T("b1", "hours.") - 0.12
    pot_on_stove(f, 0.4 + 0.6 * ramp(t, tw, 0.6))
    night_clock(f, t, 170, 940, 22.0, 26.0, st_("S6"), en_("S6"), 0.7)
    comp(f, scale_el(thermo_ink_el(0.15 + 0.4 * ramp(t, tw, 0.8)), 0.7), 900, 1020)
    if t >= tw: comp(f, achip("WARM + DAMP", 30), 860, 760, scale=pin(t, tw, 0.25))
    if t >= tho: slam(f, achip("FOR HOURS", 40), 540, 1460, -3, t, tho)
    chapter_card(f, t, st_("S6") + 0.05, 2, "THE WARM HOURS", y=1440, dur=1.4, col=ACC_L)
    icap(f, "the pot just", "[SITS THERE]", t, st_("S6") + 0.05, size=160, dark=True)
    f = dutch(f, t, st_("S6") + 0.5, -6.0, 0.6, 540, 1000)
    return finish(f, n, look="night")


# ---- S6b: 'That's exactly what wakes them up' — inside the warm pot: spores crack open one after another, germs peek out; crash zoom ----
def shot_S6b(t, n):
    f = ink_set("germp", (255, 210, 150), 540, 980, 460)
    tw = T("b1", "wakes") - 0.12
    for i, (x, y) in enumerate(((330, 900), (560, 1060), (780, 900), (450, 1240), (700, 1250))):
        cr = ramp(t, tw - 0.1 + 0.12 * i, 0.25)
        comp(f, scale_el(spore_el("sleepy" if cr <= 0 else "n", cr, 10 + i), 0.85), x, y + 4 * math.sin(t * 3 + i))
    if t >= tw: slam(f, achip("WAKE-UP TIME", 40), 540, 1460, 3, t, tw)
    icap(f, "warm + damp =", "[WAKE UP]", t, st_("S6b") + 0.05, size=170, dark=True)
    f = crash_zoom(f, t, tw, 1.18, 540, 760)
    return finish(f, n, look="warm")


def _split(f, t, t0, x, y, s, mood_="happy"):
    """one germ dividing into two: it stretches, pinches, then two germs slide apart."""
    k = clamp((t - t0) / 0.5)
    if k <= 0: comp(f, scale_el(germ_el(mood_, (0, 0), 1, int(t * 8) % 4), s), x, y); return
    if k < 0.5: comp(f, scale_xy(scale_el(germ_el("wow", (0, 0), 1, int(t * 8) % 4), s), 1 + 0.6 * k, 1 - 0.3 * k), x, y); return
    d = 120 * s * eo((k - 0.5) * 2)
    for sgn in (-1, 1): comp(f, scale_el(germ_el(mood_, (sgn * 0.5, 0), 2 + sgn, int(t * 8) % 4), s * 0.9), x + sgn * d, y)


# ---- S7: 'They hatch, they eat, they multiply' — three beats on the words: hatch (shell pops) / eat (a germ munches a grain) / split ----
def shot_S7(t, n):
    f = ink_set("warmp", (255, 255, 255), 540, 980, 440)
    th = T("b2", "hatch,") - 0.1; te = T("b2", "eat,") - 0.1; tm = T("b2", "multiply.") - 0.12
    comp(f, scale_el(spore_el("n", ramp(t, th - 0.05, 0.2), 20), 0.7), 220, 980)
    if t >= th: comp(f, ichip("HATCH", 30), 220, 1180, scale=pin(t, th, 0.25))
    if t >= te:
        comp(f, scale_el(grain_el("wow", False, (-0.6, 0), 21), 0.45), 570, 980)
        comp(f, scale_el(germ_el("hungry" if int(t * 6) % 2 else "munch", (1, 0), 1, int(t * 8) % 4), 0.9), 480, 980, scale=snap(t, te, 4, 2.0))
        comp(f, ichip("EAT", 30), 540, 1180, scale=pin(t, te, 0.25))
    if t >= tm - 0.3:
        _split(f, t, tm - 0.1, 860, 980, 0.75)
        if t >= tm: comp(f, achip("MULTIPLY", 32), 860, 1180, scale=pin(t, tm, 0.25))
    icap(f, "they hatch, eat and", "[MULTIPLY]", t, st_("S7") + 0.05, size=150)
    return finish(f, n, look="warm")


# ---- S7b: 'At around thirty degrees, they can double every twenty minutes' — thermometer at 30, a 20-min timer, one germ splits ----
def shot_S7b(t, n):
    f = ink_set("warmp", (255, 255, 255), 540, 980, 440); u = lt(t, "S7b")
    t30 = T("b2", "thirty") - 0.12; td = T("b2", "double") - 0.12; t20 = T("b2", "twenty") - 0.12
    comp(f, scale_el(thermo_ink_el(0.55 * ramp(t, st_("S7b"), 0.6)), 0.85), 200, 1000)
    if t >= t30: label_at(f, "30°C", 200, 760, t, t30, 270, 820, bg=ACC_S, fg=MILK, size=34)
    if t >= t20: comp(f, timer_el(ramp(t, t20, 1.2) / 3, "20 MIN", 110), 820, 760, scale=pin(t, t20, 0.3))
    _split(f, t, td, 560, 1080, 0.85)
    if t >= td + 0.3: slam(f, chip("x2", ACC, INKC, 60), 560, 1300, -4, t, td + 0.3)
    comp(f, ichip(SRC_M, 22), 540, 1462, op=clamp((u - 0.6) / 0.3))
    icap(f, "they can", "[DOUBLE] every 20 min", t, st_("S7b") + 0.05, size=130)
    return finish(f, n, look="warm")


# ---- S8: 'Two becomes four, four becomes eight' — a grid that doubles on the words ----
def shot_S8(t, n):
    f = ink_set("warmp", (255, 255, 255), 540, 980, 440)
    cnt = 2 if t < T("b3", "four") - 0.1 else (4 if t < T("b3", "eight,") - 0.1 else 8)
    t_last = st_("S8") if cnt == 2 else (T("b3", "four") - 0.1 if cnt == 4 else T("b3", "eight,") - 0.1)
    for i in range(cnt):
        r_, c = divmod(i, 4)
        sc = snap(t, t_last, 4, 2.0) if i >= cnt // 2 else 1.0
        comp(f, scale_el(germ_el("happy", (0, 0), 1 + i % 3, int(t * 8 + i) % 4), 0.62), 240 + c * 200, 900 + r_ * 180 + 5 * math.sin(t * 4 + i), scale=sc)
    icap(f, "two... four...", f"[{cnt}]", t, st_("S8") + 0.05, size=220)
    return finish(f, n, look="warm")


# ---- S8b: 'and after a few hours on the stove, that's a crowd' — back to the night pot: the rice is crawling with germs; clock spins ----
def shot_S8b(t, n):
    f = set_stove_night(t, 1.2)
    tc = T("b3", "crowd.") - 0.12
    night_clock(f, t, 170, 940, 23.0, 27.5, st_("S8b"), en_("S8b"), 0.7)
    pot_on_stove(f, 1.0)
    germ_crowd(f, 540, 1080, t, 6 + int(26 * ramp(t, st_("S8b"), max(0.5, tc - st_("S8b")))), 0.36, 150, "happy", 7)
    if t >= tc: slam(f, achip("A CROWD", 44), 540, 1460, -3, t, tc)
    icap(f, "a few hours later:", "[A CROWD]", t, st_("S8b") + 0.05, size=170, dark=True)
    f = dutch(f, t, st_("S8b"), -6.0, 0.01, 540, 1000)
    return finish(f, n, look="night")


# ---- S9: 'while they party, they make a toxin. Basically, a poison' — a germ party (hats); the toxin oozes up; = POISON ----
def shot_S9(t, n):
    f = ink_set("germp", (255, 200, 140), 540, 980, 460)
    tt = T("b4", "toxin.") - 0.12; tp = T("b4", "poison.") - 0.15
    for i in range(6):
        x = 200 + i * 136; y = 1260 + 18 * math.sin(t * 7 + i * 1.3)
        comp(f, _rot_el(scale_el(germ_el("happy", (0, 0), 1 + i % 3, int(t * 8 + i) % 4), 0.55), 12 * math.sin(t * 6 + i)), x, y)
        comp(f, scale_el(party_hat_el((255, 140, 60) if i % 2 else (240, 80, 120)), 0.35), x - 10, y - 66)
    if t >= tt: comp(f, toxin_el("angry"), 540, 900 + 6 * math.sin(t * 2), scale=snap(t, tt, 4, 2.2))
    if t >= tp: label_at(f, "= POISON", 800, 720, t, tp, 660, 820, bg=INKC, fg=MILK, size=34)
    icap(f, "they make a", "[TOXIN]", t, st_("S9") + 0.05, size=200, dark=True)
    return finish(f, n, look="warm")


# ---- S10: 'This is the nasty bit. That toxin shrugs off heat.' — the toxin in a fire helmet stands in the flames and shrugs; crash zoom ----
def shot_S10(t, n):
    f = set_stove(t, on=1.0)
    ts = T("b5", "shrugs") - 0.12
    t3(f, "HEAT-PROOF", 760, t, ts + 0.1, 170)
    flames(f, 540, HOB - 2, t, 520, 15, 1.4)
    shr = 14 * math.sin(clamp((t - ts) / 0.5) * math.pi) if t >= ts else 0
    comp(f, toxin_el("happy" if t >= ts else "angry", t >= ts - 0.4), 540, 1110 - shr + 4 * math.sin(t * 3), scale=1.4)
    if t >= ts: slam(f, achip("SHRUGS OFF HEAT", 38), 540, 1460, -3, t, ts)
    icap(f, "the nasty bit: the toxin", "", t, st_("S10") + 0.05, size=130)
    f = crash_zoom(f, t, ts, 1.15, 540, 800)
    return finish(f, n, look="warm")


# ---- S10b: 'Microwave the rice till it's steaming, and the toxin is still there' — RACK FOCUS: sharp on Chubby + the microwave, then the
#      focus pulls to the steaming bowl in front where the toxin pops up ----
def shot_S10b(t, n):
    f = inkify(set_kitchen(t), 0.13)
    tst = T("b5", "steaming,") - 0.12; tsh = T("b5", "still") - 0.12
    k = ramp(t, tsh - 0.25, 0.35)
    def back(g):
        comp(g, scale_el(microwave_el(t < tst + 0.3, "0:%02d" % max(0, 30 - int((t - st_("S10b")) * 12))), 0.95), 640, 860)
        chub(g, 250, 1350, 0.85, t=t, **POSE["present"], mouth=talk(t), expr="happy" if t < tsh else "wow", brow="up", look=(0.8, 0.2))
    rack_layer(f, back, 7.0 * k)
    if t >= tst: steam_wisps(f, 560, 1150, t, 5, 220, 240, (255, 255, 255), 0.75, 5)
    def front(g):
        comp(g, scale_el(rice_bowl_el("fluffy", 6), 1.5), 560, 1330)
        if t >= tsh: comp(g, scale_el(toxin_el("happy"), 0.7), 660, 1170 - 30 * eo(clamp((t - tsh) / 0.25)))
    rack_layer(f, front, 9.0 * (1 - k))
    if t >= tsh: slam(f, achip("STILL THERE", 44), 540, 1460, -3, t, tsh + 0.1)
    icap(f, "steaming hot... and the toxin is", "", t, st_("S10b") + 0.05, size=120)
    return finish(f, n, look="warm")


# ---- S11: 'reheating gets the blame, but the damage was done hours earlier, while the pot sat on the stove' — split contrast ----
def shot_S11(t, n):
    f = ink_set("ricep", (255, 255, 255), 540, 980, 440)
    tb = T("b6", "blame,") - 0.12; te = T("b6", "earlier,") - 0.12
    def L(g):
        comp(g, scale_el(microwave_el(False, "0:00"), 0.6), 330, 1000)
        if t >= tb: comp(g, chip("BLAMED", RED_, MILK, 32), 330, 1220, scale=pin(t, tb, 0.25))
    def R(g):
        g[620:1500, 540:960] = g[620:1500, 540:960] * 0.55 + np.array(C((40, 46, 80)), np.float32) * 0.45
        comp(g, scale_el(rice_pot_el(0.75, 1.0, False, 1, "angry"), 0.62), 750, 1080)
        comp(g, scale_el(clock_ink_el(), 0.5), 750, 820); clock_hands(g, 750, 820, 23 + 4 * ramp(t, te, 1.0), 110, 0.5)
        if t >= te: comp(g, achip("THE REAL DAMAGE", 28), 750, 1290, scale=pin(t, te, 0.25))
    split_contrast(f, t, st_("S11") + 0.05, L, R, "GETS THE BLAME", "HOURS EARLIER", (230, 60, 40), ACC, t_r=te - 0.3)
    icap(f, "the damage was done", "[HOURS EARLIER]", t, st_("S11") + 0.05, size=120, y=440)
    return finish(f, n, look="fresh")


# ---- S12: 'You could be throwing up within a few hours' — Chubby queasy (gross face, hand to mouth), a 1-5 HOURS chip, a green mood ----
def shot_S12(t, n):
    f = set_bathroom(t)
    tt = T("b7", "throwing") - 0.12
    sick = t >= tt - 0.1
    wob = 3 * math.sin(t * 9) if sick else 0
    chub(f, 420, 1500, 1.15, t=t, **nolean(POSE["sick"] if sick else POSE["think"]), mouth=0 if sick else talk(t), expr="gross" if sick else "sus",
         brow="sad", look=(0.3, 0.3), lean=(-6 if sick else -6) + wob, hand_r="open")
    if sick: mood(f, (120, 190, 80), 0.25 * ramp(t, tt - 0.1, 0.4))
    if t >= tt: comp(f, achip("WITHIN 1-5 HOURS", 34), 760, 900, scale=pin(t, tt, 0.25))
    comp(f, ichip(SRC_U, 22), 540, 1462, op=clamp((t - tt - 0.4) / 0.3))
    icap(f, "you could be", "[THROWING UP]", t, st_("S12") + 0.05, size=140)
    return finish(f, n, look="cool")


# ---- S12b: 'Leftover fried rice is the classic case' — a bowl of fried rice under a spotlight, CLASSIC CASE stamp ----
def shot_S12b(t, n):
    f = ink_set("ricep", (255, 230, 190), 540, 980, 440)
    tc = T("b7", "classic") - 0.12
    spotlight(f, 540, 1040, 330, 0.5, 120)
    comp(f, scale_el(rice_bowl_el("fried", 2, "happy" if t >= tc else None), 1.6), 540, 1060, scale=pin(t, st_("S12b"), 0.3))
    if t >= tc: slam(f, stamp_el("CLASSIC CASE", ACC_S, 54), 540, 760, -6, t, tc)
    icap(f, "leftover", "[FRIED RICE]", t, st_("S12b") + 0.05, size=170)
    return finish(f, n, look="warm")


# ---- S13: the GUESS 'does the fridge actually kill these germs?' — fridge at night, Chubby thinks, a big '?' ----
def shot_S13(t, n):
    f = set_fridge_night(t)
    tk = T("c1", "kill") - 0.12
    chub(f, 330, 1500, 0.95, t=t, **nolean(POSE["think"]), mouth=talk(t), expr="sus", brow="sus", look=(0.8, -0.4), lean=moving_hold(t, 3)["lean"] - 4)
    comp(f, scale_el(germ_el("wow", (-0.5, 0), 2, int(t * 8) % 4), 0.7), 820, 900 + 6 * math.sin(t * 3))
    if t >= tk: comp(f, chip(" ? ", ACC_S, MILK, 110), 700, 760 + 6 * math.sin(t * 4), scale=pin(t, tk, 0.25))
    icap(f, "quick guess: does the fridge", "[KILL] them?", t, st_("S13") + 0.05, size=150, dark=True)
    return finish(f, n, look="cool")


# ---- S13b: 'Nope. Cold just slows them right down... as long as the rice gets there fast' — germs in the cold, frosty + sleepy, snow ----
def shot_S13b(t, n):
    f = ink_set("coldp", (255, 255, 255), 540, 980, 440)
    tsl = T("c2", "slows") - 0.12; tfa = T("c2", "fast.") - 0.15
    for i in range(5):
        x = 230 + i * 150; y = 1000 + 30 * math.sin(i * 1.7)
        comp(f, scale_el(germ_el("sad" if t >= tsl else "wow", (0, 0), 1 + i % 3, 0), 0.6), x + 4 * math.sin(t * 0.8 + i), y)
    snow(f, t, 0.8 * ramp(t, tsl - 0.2, 0.5))
    slam(f, chip("NOPE", BLUE_S, MILK, 70), 540, 760, -4, t, st_("S13b") + 0.05)
    if t >= tsl: comp(f, bchip("COLD = SLOW, NOT DEAD", 34), 540, 1260, scale=pin(t, tsl, 0.25))
    if t >= tfa: slam(f, achip("GET IT THERE FAST", 36), 540, 1430, 3, t, tfa)
    icap(f, "cold just", "[SLOWS] them", t, st_("S13b") + 0.3, acc=BLUE, size=170, y=470)
    return finish(f, n, look="cool")


# ---- S14: PART 3 'those little pebbles. Why does rice go hard in the fridge?' — a TAKE + jaw drop, a hard grain pops up; crash zoom ----
def shot_S14(t, n):
    f = set_fridge_night(t)
    th = T("d1", "hard") - 0.12
    tk = take(t, th, 1.0, 8)
    chub(f, 330, 1500, 0.95, t=t, **nolean(POSE["hold_up"]), mouth="jaw" if t >= th else talk(t), expr=tk["expr"] if t >= th else "n",
         brow=tk["brow"] if t >= th else "n", look=(0.8, 0), lean=tk["lean"] + 3, squash=tk["squash"], bob=tk["dy"], hand_r="grip",
         hair=(drag(t, lambda q: take(q, th, 1.0, 8)["dy"], 3, 0.8), 0))
    comp(f, scale_el(rice_bowl_el("hard", 1), 0.9), 700, 1080)
    if t >= th: comp(f, scale_el(grain_el("angry", True, (0, 0), 3), 0.6), 760, 800, scale=snap(t, th, 4, 2.0))
    chapter_card(f, t, st_("S14") + 0.05, 3, "THE PEBBLES", y=1440, dur=1.4, col=BLUE_L)
    icap(f, "why does rice go", "[HARD]?", t, st_("S14") + 0.05, acc=BLUE, size=190, dark=True)
    f = crash_zoom(f, t, th, 1.2, 600, 720)
    return finish(f, n, look="cool")


# ---- S15: 'When you cook rice, the starch inside soaks up water and swells... soft and fluffy' — a plump grain + the loose starch diagram ----
def shot_S15(t, n):
    f = ink_set("ricep", (255, 255, 255), 540, 980, 440)
    ts = T("d2", "starch") - 0.1; tw = T("d2", "water") - 0.1; tsw = T("d2", "swells.") - 0.12; tf = T("d2", "fluffy.") - 0.12
    sw = 1 + 0.18 * ramp(t, tsw, 0.4)
    comp(f, scale_el(grain_el("happy" if t >= tf else "n", False, (0, 0), 4), 0.9 * sw), 190, 1000)
    if t >= ts:
        starch_rows(f, 640, 1000, 0.0, t, 520, 380, 6, t >= tw)
        label_at(f, "STARCH", 640, 760, t, ts, 640, 800, bg=INKC, fg=MILK, size=30)
    if t >= tw: label_at(f, "WATER", 880, 1260, t, tw, 820, 1170, bg=BLUE_S, fg=MILK, size=28)
    if t >= tf: comp(f, mchip("SOFT + FLUFFY", 34), 540, 1430, scale=pin(t, tf, 0.25))
    icap(f, "starch soaks up water and", "[SWELLS]", t, st_("S15") + 0.05, acc=BLUE, size=160)
    return finish(f, n, look="fresh")


# ---- S16: 'As it cools, the starch chains slowly squeeze back together into neat, tight rows, a bit like crystals' — the diagram tightens ----
def shot_S16(t, n):
    f = ink_set("coldp", (255, 255, 255), 540, 980, 440)
    tq = T("d3", "squeeze") - 0.1; tr_ = T("d3", "rows,") - 0.1; tc = T("d3", "crystals.") - 0.12
    k = ramp(t, tq - 0.1, max(0.5, tr_ - tq + 0.3))
    starch_rows(f, 540, 1000, k, t, 560, 400, 6, True)
    if t >= tr_: comp(f, bchip("NEAT, TIGHT ROWS", 34), 540, 1290, scale=pin(t, tr_, 0.25))
    if t >= tc: slam(f, ichip("LIKE CRYSTALS", 32), 540, 1420, 3, t, tc)
    comp(f, scale_el(thermo_ink_el(0.15, False, 2), 0.5), 920, 800)
    icap(f, "as it cools, the starch", "[SQUEEZES]", t, st_("S16") + 0.05, acc=BLUE, size=160)
    return finish(f, n, look="cool")


# ---- S16b: 'That has a name, retrogradation. Fancy word, simple idea: the starch is setting again.' — ink title + Chubby's smirk ----
def shot_S16b(t, n):
    f = ink_set("coldp", (255, 255, 255), 540, 980, 440)
    tr_ = T("d4", "retrogradation.") - 0.15; tfw = T("d4", "Fancy") - 0.1; tse = T("d4", "setting") - 0.12
    t3(f, "RETRO-", 660, t, tr_, 170, BLUE_L, BLUE_S); t3(f, "GRADATION", 840, t, tr_ + 0.1, 140, BLUE_L, BLUE_S)
    chub(f, 250, 1500, 0.85, t=t, **POSE["cheek"], mouth=talk(t), expr="smirk" if t >= tfw else "n", brow="n", look=(1, -0.3))
    starch_rows(f, 760, 1220, 1.0, t, 300, 160, 5, False)
    if t >= tse: comp(f, bchip("= SETTING AGAIN", 34), 760, 1420, scale=pin(t, tse, 0.25))
    if t >= tfw: icap(f, "fancy word,", "[SIMPLE IDEA]", t, tfw, acc=BLUE, size=140, y=440)
    else: comp(f, ichip(SRC_R, 22), 540, 440, op=clamp((t - tr_ - 0.3) / 0.3))
    return finish(f, n, look="cool")


# ---- S17: 'Heat shakes those rows loose, and the rice goes soft again' — steam + the diagram loosens; the hard grain plumps back up ----
def shot_S17(t, n):
    f = ink_set("warmp", (255, 255, 255), 540, 980, 440)
    tsh = T("d5", "shakes") - 0.1; tl = T("d5", "loose,") - 0.12; ts = T("d5", "soft") - 0.12
    k = 1 - ramp(t, tsh, max(0.4, tl - tsh + 0.2))
    jit = 6 * math.sin(t * 40) * (1 - k) * (t < ts)
    starch_rows(f, 640 + jit, 980, k, t, 460, 360, 6, False)
    comp(f, scale_el(grain_el("happy" if t >= ts else "sad", t < ts, (0, 0), 8), 0.8), 170, 1000)
    steam_wisps(f, 640, 780, t, 4, 160, 260, (255, 255, 255), 0.7, 6)
    if t >= ts: comp(f, mchip("SOFT AGAIN", 36), 540, 1350, scale=pin(t, ts, 0.25))
    icap(f, "heat shakes the rows", "[LOOSE]", t, st_("S17") + 0.05, size=180)
    return finish(f, n, look="warm")


# ---- S17b: 'So hard rice isn't bad rice. It's just cold starch.' — the hard bowl gets a check; HARD ≠ BAD ----
def shot_S17b(t, n):
    f = ink_set("ricep", (255, 255, 255), 540, 980, 440)
    tb = T("d5", "bad") - 0.1; tc = T("d5", "cold") - 0.1
    comp(f, scale_el(rice_bowl_el("hard", 1, "happy" if t >= tc else "sad"), 1.3), 600, 1020)
    if t >= tb: comp(f, chip("HARD ≠ BAD", INKC, MILK, 46), 600, 760, scale=pin(t, tb, 0.25))
    if t >= tc: comp(f, check_el(54, True), 860, 900, scale=pin(t, tc, 0.25)); slam(f, bchip("JUST COLD STARCH", 38), 600, 1300, -3, t, tc)
    chub(f, 170, 1500, 0.75, t=t, **POSE["shrug"], mouth=talk(t), expr="happy", brow="up", look=(1, -0.3))
    icap(f, "hard rice isn't", "[BAD RICE]", t, st_("S17b") + 0.05, size=170)
    return finish(f, n, look="fresh")


RULES = [("COOL IT IN AN HOUR", "1"), ("EAT IT IN A DAY", "2"), ("HEAT IT ONCE", "3"), ("HEAT IT HOT", "4")]


def rule_cards(f, lit, t, t_lit, y0=640, gap=170, x=600, w=640):
    """the four-rule mnemonic: numbered ink cards; lit[i] = filled in (pops in at t_lit[i]); unlit = an empty numbered slot."""
    for i, (txt, num) in enumerate(RULES):
        y = y0 + i * gap; k = min(1.0, pin(t, t_lit[i], 0.25)) if lit[i] else 1.0
        g = f.copy()
        cv2.rectangle(g, (int(x - w / 2), int(y - 62)), (int(x + w / 2), int(y + 62)), C(MILK if lit[i] else (236, 230, 216)), -1, cv2.LINE_AA)
        cv2.rectangle(g, (int(x - w / 2), int(y - 62)), (int(x + w / 2), int(y + 62)), C(INKC), 6, cv2.LINE_AA)
        cv2.circle(g, (int(x - w / 2 + 62), int(y)), 40, C(BLUE if lit[i] else (200, 196, 186)), -1, cv2.LINE_AA)
        comp(g, ed_el(num, "", lead_col=MILK, lead_size=50), x - w / 2 + 62, y)
        if lit[i]: comp(g, ed_el(txt, "", lead_col=INKC, lead_size=44), x + 36, y)
        f[:] = f * (1 - k) + g * k


# ---- S18: PART 4 'The good news? The whole fix fits in four simple rules.' — four empty numbered cards, Chubby presents ----
def shot_S18(t, n):
    f = ink_set("coldp", (255, 255, 255), 540, 980, 440)
    tf = T("e1", "four") - 0.12
    rule_cards(f, [False] * 4, t, [0] * 4, 680, 165, 640, 580)
    chub(f, 170, 1500, 0.8, t=t, **POSE["present"], mouth=talk(t), expr="happy", brow="up", look=(1, -0.3))
    if t >= tf: slam(f, bchip("4 SIMPLE RULES", 40), 640, 1380, -3, t, tf)
    chapter_card(f, t, st_("S18") + 0.05, 4, "THE FIX", y=1440, dur=1.3, col=BLUE_L)
    icap(f, "the good news:", "[FOUR] rules", t, st_("S18") + 0.05, acc=BLUE, size=170, y=440)
    return finish(f, n, look="fresh")


# ---- S19: 'One, cool it fast and get it in the fridge within an hour' — Chubby carries the lidded pot to the open fridge; a 1-HOUR timer ----
def shot_S19(t, n):
    f = set_fridge_night(t)
    th = T("e2", "hour.") - 0.12
    u = ramp(t, st_("S19"), max(0.8, th - st_("S19")))
    x = 200 + 220 * u
    chub(f, x, 1500, 0.9, t=t, la=(60, 100), ra=(60, 100), mouth=talk(t), expr="n", brow="up", look=(1, 0), lean=6 + 3 * math.sin(t * 9) * (u < 1))
    comp(f, scale_el(rice_pot_el(0.7, 0.0, True), 0.42), x + 10, 1250)
    comp(f, timer_el(ramp(t, st_("S19") + 0.2, 1.5), "1 HOUR", 100), 860, 900, scale=pin(t, st_("S19") + 0.1, 0.3))
    if t >= th: slam(f, bchip("FRIDGE WITHIN AN HOUR", 34), 540, 1460, -2, t, th)
    icap(f, "cool it fast:", "[1 HOUR]", t, st_("S19") + 0.05, acc=BLUE, size=170, dark=True)
    return finish(f, n, look="cool")


# ---- S19b: 'Spread it out in a wide dish and it cools much quicker' — split: a deep pot (still hot inside) vs a wide dish (cools fast) ----
def shot_S19b(t, n):
    f = ink_set("coldp", (255, 255, 255), 540, 980, 440); u = lt(t, "S19b")
    tw = T("e2", "wide") - 0.1; tq = T("e2", "quicker.") - 0.12
    def L(g):
        comp(g, scale_el(rice_pot_el(0.8, 1.0, False, 2), 0.55), 330, 1060)
        comp(g, scale_el(thermo_ink_el(0.55, True, 3), 0.45), 460, 880)
        if t >= tq: comp(g, chip("SLOW", RED_, MILK, 30), 330, 1300, scale=pin(t, tq, 0.25))
    def R(g):
        comp(g, scale_el(dish_el(2), 0.7), 750, 1080)
        comp(g, scale_el(thermo_ink_el(0.55 - 0.45 * ramp(t, tq - 0.2, 0.8), True, 4), 0.45), 880, 880)
        if t >= tq: comp(g, bchip("FAST", 30), 750, 1300, scale=pin(t, tq, 0.25))
    split_contrast(f, t, st_("S19b") + 0.05, L, R, "DEEP POT", "WIDE DISH", ACC, BLUE, t_r=tw - 0.2)
    comp(f, ichip(SRC_C, 22), 540, 1462 + 20, op=clamp((u - 0.6) / 0.3))
    icap(f, "spread it out in a", "[WIDE DISH]", t, st_("S19b") + 0.05, acc=BLUE, size=140, y=440)
    return finish(f, n, look="fresh")


# ---- S20 / S20b / S20c: rules 2-4 fill in on the card stack (24 h max / once, not twice / steaming all through) ----
def _rules_shot(f, t, upto, icon):
    lit = [i <= upto for i in range(4)]
    tl = [st_("S19") - 1, T("e3", "Two,") - 0.1, T("e3", "Three,") - 0.1, T("e3", "Four,") - 0.1]
    rule_cards(f, lit, t, tl, 620, 160, 540, 700)
    icon(f)


def shot_S20(t, n):
    f = ink_set("coldp", (255, 255, 255), 540, 980, 440)
    td = T("e3", "day.") - 0.12
    def icon(g):
        if t >= td: comp(g, chip("24 HOURS MAX", BLUE_S, MILK, 34), 540, 1340, scale=pin(t, td, 0.25))
    _rules_shot(f, t, 1, icon)
    comp(f, ichip(SRC_S, 22), 540, 1462, op=clamp((lt(t, "S20") - 0.5) / 0.3))
    icap(f, "rule two:", "[1 DAY]", t, st_("S20") + 0.05, acc=BLUE, size=150, y=420)
    return finish(f, n, look="fresh")


def shot_S20b(t, n):
    f = ink_set("coldp", (255, 255, 255), 540, 980, 440)
    to = T("e3", "once.") - 0.12
    def icon(g):
        comp(g, scale_el(microwave_el(True, "1x"), 0.36), 360, 1350)
        if t >= to: comp(g, chip("ONCE. NOT TWICE.", RED_, MILK, 30), 740, 1350, scale=pin(t, to, 0.25))
    _rules_shot(f, t, 2, icon)
    icap(f, "rule three:", "[ONCE]", t, st_("S20b") + 0.05, acc=BLUE, size=150, y=420)
    return finish(f, n, look="fresh")


def shot_S20c(t, n):
    f = ink_set("warmp", (255, 255, 255), 540, 980, 440)
    ts = T("e3", "steaming") - 0.12
    def icon(g):
        comp(g, scale_el(rice_bowl_el("fluffy", 8), 0.5), 330, 1370)
        steam_wisps(g, 330, 1310, t, 4, 120, 150, (255, 255, 255), 0.8, 7)
        if t >= ts: comp(g, achip("STEAMING ALL THE WAY THROUGH", 24), 700, 1370, scale=pin(t, ts, 0.25))
    _rules_shot(f, t, 3, icon)
    icap(f, "rule four:", "[HOT]", t, st_("S20c") + 0.05, size=150, y=420)
    return finish(f, n, look="warm")


# ---- S21: 'And if the pot sat out all night? Don't gamble on it. Bin it.' — morning light on the stove; Chubby STOP pose; the pot flips into the bin ----
def shot_S21(t, n):
    f = set_stove(t, on=0.0)
    tg = T("e4", "gamble") - 0.12; tb = T("e4", "Bin") - 0.1
    night_clock(f, t, 170, 900, 7.0, 7.3, st_("S21"), en_("S21"), 0.7)
    if t < tb: pot_on_stove(f, 1.0, False, "angry", 600, 0.9)
    comp(f, scale_el(bin_ink_el(ramp(t, tb - 0.2, 0.2)), 0.9), 860, 1300)
    if t >= tb:
        k = clamp((t - tb) / 0.35); x = 600 + (860 - 600) * k; y = 1150 - 180 * math.sin(k * math.pi) + 60 * k
        if k < 1: comp(f, _rot_el(scale_el(rice_pot_el(0.75, 1.0, False, 1, "wow"), 0.5), -90 * k), x, y)
    chub(f, 240, 1500, 0.95, t=t, **POSE["stop"], mouth=talk(t), expr="n" if t < tg else "sus", brow="sus", look=(1, 0), hand_r="open")
    if t >= tg: comp(f, chip("DON'T GAMBLE", RED_, MILK, 36), 620, 760, scale=pin(t, tg, 0.25))
    icap(f, "sat out all night?", "[BIN IT]", t, st_("S21") + 0.05, size=190)
    f = crash_zoom(f, t, tb, 1.15, 640, 760)
    return finish(f, n, look="golden")


# ---- S22: 'Good news for rice salad fans: cold rice is fine, if it got into the fridge fast and it's less than a day old' — lunch table ----
def shot_S22(t, n):
    f = set_lunch(t)
    tfi = T("f1", "fine,") - 0.12; tfa = T("f1", "fast") - 0.1; tdy = T("f1", "day") - 0.1
    m = munch(t)[0] if t < tfi else talk(t)
    chub(f, 300, 1500, 0.95, t=t, **POSE["hold_up"], mouth=m, expr="happy", brow="up", look=(0.7, 0.1), hand_r="grip")
    cloth_front(f, 1330)
    comp(f, scale_el(rice_bowl_el("salad", 5, "happy" if t >= tfi else None), 0.9), 720, 1270)
    if t >= tfi: comp(f, check_el(50, True), 880, 1060, scale=pin(t, tfi, 0.25))
    if t >= tfa: comp(f, bchip("FRIDGE FAST", 30), 720, 760, scale=pin(t, tfa, 0.25))
    if t >= tdy: comp(f, bchip("UNDER A DAY OLD", 30), 720, 840, scale=pin(t, tdy, 0.25))
    icap(f, "cold rice salad?", "[FINE]", t, st_("S22") + 0.05, acc=INK_MINT_S, size=190)
    return finish(f, n, look="golden")


# ---- S23: RECAP mnemonic 'cool it in an hour, eat it in a day, heat it once, and heat it hot' — the four cards light up; slow PUSH-IN ----
def shot_S23(t, n):
    f = ink_set("ricep", (255, 255, 255), 540, 980, 440)
    tl = [T("g1", "cool") - 0.1, T("g1", "eat") - 0.1, T("g1", "once,") - 0.25, T("g1", "hot.") - 0.3]
    rule_cards(f, [t >= x for x in tl], t, tl, 640, 165, 540, 720)
    icap(f, "remember it like", "[THIS]", t, st_("S23") + 0.05, acc=BLUE, size=170, y=430)
    f = push_in(f, t, st_("S23") + 0.3, en_("S23"), 1.06, 540, 900)
    return finish(f, n, look="fresh")


# ---- S24: send it + FreshNestHub sting ----
def shot_S24(t, n):
    f = set_lunch(t) * 0.95
    vend = LINES["g2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("g2", "Send") + 0.3
        comp(f, scale_el(phone2_el("left the rice out all night again", "cool it in an hour!", pr), 0.82), 700, 950, scale=pin(t, st_("S24")))
        if pr and t < T("g2", "Send") + 0.75:
            rr = (t - T("g2", "Send") - 0.3) / 0.45
            cv2.circle(f, (700, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        chub(f, 280, 1500, 0.95, t=t, **POSE["point"], mouth=talk(t), expr="happy", brow="up", look=(1, 0), hand_r="point")
        cloth_front(f, 1330)
        comp(f, scale_el(rice_bowl_el("fluffy", 9), 0.6), 770, 1290)
        ui_word(f, "send to the friend who leaves", "[THE RICE OUT]", 420, t, T("g2", "friend") - 0.1, col=INKC, acc=ACC, size=110, shadow=0.0, lead_col=INKC)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INKC, lead_size=42), 540, 1080, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 200, 1500, 0.8, t=t, **POSE["cheer"], mouth=3, expr="happy", brow="up")
        cloth_front(f, 1330)
        comp(f, scale_el(rice_bowl_el("fluffy", 9), 0.5 * k), 840, 1290)
    return finish(f, n, look="golden")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TISNT, 0.4, 16), (T("i2", "fridge.") - 0.12, 0.3, 10), (T("i3", "pebbles") - 0.12, 0.35, 14),
           (T("a1", "stowaway,") - 0.12, 0.25, 8), (T("a1", "Bacillus") - 0.12, 0.3, 12), (T("a2", "spore,") - 0.12, 0.3, 10),
           (T("a2", "armour.") - 0.12, 0.3, 10), (T("a3", "crack") - 0.12, 0.35, 14), (T("a3", "asleep.") - 0.15, 0.25, 8),
           (T("a4", "fine,") - 0.12, 0.25, 8), (T("b1", "hours.") - 0.12, 0.35, 12), (T("b1", "wakes") - 0.12, 0.4, 16),
           (T("b2", "multiply.") - 0.12, 0.3, 10), (T("b2", "double") - 0.12 + 0.3, 0.3, 10), (T("b3", "four") - 0.1, 0.25, 8),
           (T("b3", "eight,") - 0.1, 0.3, 10), (T("b3", "crowd.") - 0.12, 0.35, 14), (T("b4", "toxin.") - 0.12, 0.4, 16),
           (T("b5", "shrugs") - 0.12, 0.35, 14), (T("b5", "still") - 0.02, 0.35, 14), (T("b6", "earlier,") - 0.12, 0.3, 10),
           (T("b7", "throwing") - 0.12, 0.35, 12), (T("b7", "classic") - 0.12, 0.35, 14), (st_("S13b") + 0.05, 0.35, 14),
           (T("d1", "hard") - 0.12, 0.4, 16), (T("d3", "crystals.") - 0.12, 0.25, 8), (T("d4", "retrogradation.") - 0.15, 0.35, 14),
           (T("d5", "cold") - 0.1, 0.3, 10), (T("e1", "four") - 0.12, 0.3, 10), (T("e2", "hour.") - 0.12, 0.3, 10),
           (T("e4", "Bin") - 0.1, 0.4, 16), (T("f1", "fine,") - 0.12, 0.25, 8), (T("g1", "hot.") - 0.3, 0.3, 10), (T("g2", "Send") + 0.3, 0.2, 8)]


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
