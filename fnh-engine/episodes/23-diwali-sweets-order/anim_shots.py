# ================= shots: FreshNestHub 23 — "Which Diwali sweet goes bad first?" (Chubby INK, ep 7 of the ink look) ===
# COLOUR SCRIPT: MARIGOLD = fuses' sparks, titles, chips; WATER BLUE = water; MOULD grey-green = only when something has gone off. Warm room = the box, cold blue = the fridge.
# THE IDEA: every sweet is a firecracker with its own fuse (Diwali-native metaphor for a whole system). The hero device: fuse_chart = THE LIST as a bar chart whose bars are burning fuses, paid as a screenshot card.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "Because") - 0.2, "whip"), ("S1b", T("i2", "and") - 0.1, "punch"), ("S2", T("i3", "Every") - 0.15, "flash"), ("S2b", T("i3", "and") - 0.1, "zoom"),
    ("S3", T("a1", "Im") - 0.2, "focus"), ("S4", T("a2", "The") - 0.2, "flash"), ("S4b", T("a2", "Youre") - 0.1, "whip"), ("S5", T("a3", "Rusgoola") - 0.2, "whip"), ("S6", T("a4", "Milk") - 0.15, "whip"), ("S7", T("a5", "Kaaju") - 0.12, "punch"), ("S8", T("a6", "And") - 0.15, "whip"), ("S8b", T("a6", "in") - 0.1, "zoom"),
    ("S9", T("b1", "So") - 0.2, "flash"), ("S10", T("b2", "Mostly") - 0.2, "whip"), ("S10b", T("b2", "A") - 0.12, "punch"), ("S11", T("b3", "Baysun") - 0.15, "whip"), ("S12", T("b4", "And") - 0.2, "focus"), ("S12b", T("b4", "Milks") - 0.12, "whip"),
    ("S13", T("c1", "Scientists") - 0.2, "flash"), ("S14", T("c2", "Most") - 0.12, "zoom"), ("S15", T("c3", "Burfee") - 0.12, "punch"), ("S15b", T("c3", "Too") - 0.12, "whip"), ("S16", T("c4", "Thats") - 0.15, "whip"), ("S17", T("c5", "And") - 0.2, "punch"), ("S17b", T("c5", "What") - 0.12, "focus"), ("S18", T("c6", "On") - 0.1, "zoom"), ("S18b", T("c6", "The", 1) - 0.12, "whip"),
    ("S19", T("d1", "So") - 0.2, "flash"), ("S20", T("d2", "In") - 0.2, "whip"), ("S21", T("d3", "But") - 0.2, "focus"), ("S22", T("d4", "Thats") - 0.12, "punch"), ("S22b", T("d4", "So") - 0.12, "whip"),
    ("S23", T("e1", "Which") - 0.2, "flash"), ("S24", T("e2", "Your") - 0.15, "whip"), ("S25", T("e3", "Nobodys") - 0.2, "whip"), ("S25b", T("e3", "That") - 0.12, "focus"), ("S26", T("e4", "At") - 0.2, "flash"), ("S26b", T("e4", "Since") - 0.1, "zoom"), ("S27", T("e5", "With") - 0.2, "whip"), ("S27b", T("e5", "Its") - 0.1, "punch"),
    ("S28", T("f1", "So") - 0.2, "flash"), ("S29", T("f2", "Screenshot") - 0.15, "cut"), ("S30", T("f3", "If") - 0.2, "whip"), ("S31", T("g1", "Send") - 0.2, "whip"),
]


SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}

def lt(t, sid): return t - SHOT[sid]["start"]


def st_(sid): return SHOT[sid]["start"]


def en_(sid): return SHOT[sid]["end"]


def ui_word(f, lead, big, y, t, t0, col=INKC, acc=ACC, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def icap(f, lead, big, t, t0, acc=ACC_S, size=150, y=440, out=None, tail="", dark=False):
    if dark: ui_word(f, lead, big, y, t, t0, col=WHITE, acc=acc, size=size, shadow=0.6, lead_col=WHITE, out=out, tail=tail)
    else: ui_word(f, lead, big, y, t, t0, col=INKC, acc=acc, size=size, shadow=0.0, lead_col=INKC, out=out, tail=tail)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def ichip(text, size=26, inv=False): return chip(text, INKC if not inv else MILK, MILK if not inv else INKC, size)


def achip(text, size=30): return chip(text, ACC_S, MILK, size)


def bchip(text, size=30): return chip(text, WATER_S, MILK, size)


def t3(f, text, y, t, t0, size=230, face=None, side=None, x=540):
    if t >= t0: title_ink(f, text, y, t, t0, size=size, face=face or ACC_L, side=side or ACC_S, depth=18, x=x)


def nolean(p): return {k: v for k, v in p.items() if k != "lean"}


def src(f, text, t, t0, y=1462):
    if t >= t0: comp(f, chip(text, INKC, MILK, 22), 540, y, op=clamp((t - t0) / 0.2))


def card(f, x, y, w, h, col=(252, 248, 238), edge=INKC, k=1.0):
    if k <= 0: return
    ww, hh = int(w * k / 2), int(h * k / 2)
    cv2.rectangle(f, (int(x - ww + 8), int(y - hh + 10)), (int(x + ww + 8), int(y + hh + 10)), C((120, 100, 80)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - ww), int(y - hh)), (int(x + ww), int(y + hh)), C(col), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - ww), int(y - hh)), (int(x + ww), int(y + hh)), C(edge), 6, cv2.LINE_AA)


def crumbs(f, x, y, t, t0, n=12, spread=240, col=None, seed=3):
    if t < t0 or t > t0 + 0.9: return
    d = t - t0; rng = np.random.default_rng(seed); c = col or N_G
    for i in range(n):
        vx = rng.uniform(-spread, spread); vy = rng.uniform(-420, -120); xx = x + vx * d; yy = y + vy * d + 900 * d * d; r_ = int(rng.uniform(7, 15))
        cv2.circle(f, (int(xx), int(yy)), r_ + 3, C(INKC), -1, cv2.LINE_AA); cv2.circle(f, (int(xx), int(yy)), r_, C(c), -1, cv2.LINE_AA)

SRC_F = "Source: FSSAI Guidance Note 14/2020 (a guide, not law)"
SRC_W = "Source: J Ethnic Foods 2021 · Thikare 2020 · Badola 2018"
SRC_A = "Source: Shrivas 2018 · Badola 2018 (J Food Sci Technol)"
SRC_U = "Source: USDA FSIS, Molds on Food (soft foods)"
SRC_L = "Source: Shrivas et al. 2018 (lab test, sealed pouches)"
SRC_B = "Source: FSSAI order, from 1 Oct 2020 · Deccan Herald"
TOP = 1330
RED_I = (176, 52, 44)
ROW4 = [(450, 0.62), (610, 0.62), (770, 0.62), (920, 0.62)]
TF = T("i1", "first") - 0.22


def row_sweets(f, t, ks, moods=(None, None, None, None), fz=0.0, y=1262):
    """kalakand, rasgulla, barfi, besan laddoo on the table with their fuses."""
    els = [(kalakand_el, 450, 0.74, y, 60, 3), (rasgulla_el, 625, 0.72, y - 6, 90, 5), (barfi_ink_el, 780, 0.7, y, 130, 2), (besan_el, 925, 0.68, y - 14, 240, 4)]
    for i, (fn, x, s_, yy, L, sd) in enumerate(els):
        top = yy - 66 * s_ * 1.3
        comp(f, scale_el(fn(moods[i]), s_), x, yy)
        sweet_fuse(f, x, top, L, ks[i], t, seed=sd)
    if fz > 0: fuzz(f, 450, y - 40, 160, 34, fz, t, 7, n=30)


# ---- S0: HOOK — a table of sweets, fuses already burning at frame 0, Chubby reaching for the kalakand; on 'first' its fuse hits the end: POOF of mould, take + jump back ----
def shot_S0(t, n):
    f = set_droom(t)
    t3(f, "FIRST?", 800, t, TF + 0.02, 240)
    tk = take(t, TF + 0.02); jb = jump_back(t, TF + 0.02, 70)
    rr = t > TF
    hair = (drag(t, lambda q: -jump_back(q, TF + 0.02, 70) if q > TF else 0, 3, 0.4), 0)
    hs = chub(f, 215 - (jb if rr else 0), 1500 + (tk["dy"] if rr else 0), 1.0, t=t, la=(24, 14), ra=(74 + 6 * math.sin(t * 3), 34) if not rr else (140, 160), mouth=("jaw" if TF + 0.02 < t < TF + 0.9 else talk(t)), expr=tk["expr"] if rr else "hungry" if False else ("happy" if not rr else "wow"), brow=tk["brow"] if rr else "up", look=(1, 0.3), lean=(tk["lean"] if rr else 4), squash=tk["squash"] if rr else 0, turn=0.5, hair=hair if rr else (0, 0))
    table_front(f, TOP)
    ks = [clamp(t / max(TF, 0.1)), 0.16 + t * 0.05, 0.1 + t * 0.03, 0.05 + t * 0.012]
    row_sweets(f, t, ks, ("wow" if t < TF else "sad", "wow" if rr else None, "wow" if rr else None, "happy" if rr else None), ramp(t, TF, 0.5))
    poof(f, 450, 1200, t, TF)
    f = push_in(f, t, 0.0, 2.0, 1.035, 540, 1050)
    icap(f, "do you know which sweet", "goes bad [FIRST]?", t, 0.06, size=110, y=450, acc=ACC_S)
    return finish(f, n, look="warm")


# ---- S1: 'one of them's done by tonight' — kalakand under a moon; S1b: 'the one right next to it has got a month' — besan laddoo on a calendar, smug ----
def shot_S1(t, n):
    f = set_droom(t, dim=0.3); t0 = st_("S1"); tn = T("i2", "tonight") - 0.15
    glow(f, 780, 660, 260, (240, 240, 210), 0.3); cv2.circle(f, (780, 660), 92, C((246, 244, 216)), -1, cv2.LINE_AA); cv2.circle(f, (780, 660), 92, C(INKC), 6, cv2.LINE_AA)
    chub(f, 215, 1500, 0.96, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="sad", brow="sad", look=(1, -0.2), hand_r="point", turn=0.5)
    table_front(f, TOP)
    comp(f, scale_el(kalakand_el("sad"), 1.25), 660, 1190, scale=pin(t, t0)); fuzz(f, 660, 1110, 310, 60, 0.35 + 0.65 * ramp(t, t0, 1.4), t, 7)
    if t >= tn: t3(f, "TONIGHT", 480, t, tn, 170, ACC_L, ACC_S)
    else: icap(f, "one of them", "[DONE]", t, t0 + 0.05, size=130, y=450, dark=True, acc=ACC_L)
    return finish(f, n, look="night")


def shot_S1b(t, n):
    f = ink_set("marig", (255, 244, 190), 540, 980, 480); t0 = st_("S1b"); tm = T("i2", "month") - 0.2
    for i, xx in enumerate((230, 390, 550, 710, 870)):
        if t >= t0 + i * 0.06: comp(f, scale_el(calendar_el("NOV" if i < 4 else "DEC", str((8, 15, 22, 29, 6)[i])), 0.5), xx, 700, scale=pin(t, t0 + i * 0.06))
    comp(f, scale_el(besan_el("happy", (0.3, 0)), 1.5), 640, 1160 + 10 * math.sin(t * 3), scale=pin(t, t0 + 0.05))
    comp(f, scale_el(kalakand_el("sad"), 0.5), 180, 1320); fuzz(f, 180, 1285, 130, 26, 1.0, t, 8, n=20)
    comp(f, chip("NEXT TO IT", INKC, MILK, 28), 190, 1190, scale=pin(t, t0 + 0.15))
    icap(f, "the one next to it has got", "A [MONTH]", t, t0 + 0.05, size=130, y=450, acc=ACC_S)
    return finish(f, n, look="golden")


# ---- S2: 'Every sweet is like a cracker with its own fuse' — a real firecracker beside a laddoo, same fuse: match ----
def shot_S2(t, n):
    f = set_lunch(t) if False else ink_set("rosep", (255, 255, 255), 540, 1000, 470); t0 = st_("S2"); tc = T("i3", "cracker") - 0.15; tf = T("i3", "fuse") - 0.15
    if t >= tc:
        comp(f, scale_el(patakha_el(), 1.25), 300, 1100, scale=pin(t, tc)); 
        sweet_fuse(f, 300, 930, 170, 0.12 + (t - tc) * 0.08, t, seed=2)
    else: comp(f, chip("?", ACC_S, MILK, 120), 300, 1080, scale=pin(t, t0 + 0.05))
    comp(f, scale_el(boondi_el("n"), 1.3), 780, 1110, scale=pin(t, t0 + 0.05))
    if t >= tf: sweet_fuse(f, 780, 985, 170, 0.12 + (t - tf) * 0.08, t, seed=4); comp(f, chip("ITS OWN FUSE", ACC_S, MILK, 44), 540, 1370, scale=pin(t, tf))
    icap(f, "every sweet is", "a [CRACKER]", t, t0 + 0.05, size=130, y=450, acc=ACC_S)
    return finish(f, n, look="warm")


# ---- S2b: 'and they're all already lit' — the gift box from above, a nest of burning fuses; Chubby looks in over the edge ----
def shot_S2b(t, n):
    f = set_droom(t, dim=0.45); tl = T("i3", "lit") - 0.2; cx, cy = 540, 1040; w, h = 860, 560
    cv2.rectangle(f, (cx - w // 2 + 14, cy - h // 2 + 16), (cx + w // 2 + 14, cy + h // 2 + 16), C((50, 30, 34)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), C(ACC), -1, cv2.LINE_AA); cv2.rectangle(f, (cx - w // 2 + 26, cy - h // 2 + 26), (cx + w // 2 - 26, cy + h // 2 - 26), C((252, 236, 200)), -1, cv2.LINE_AA); cv2.rectangle(f, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), C(INKC), 9, cv2.LINE_AA)
    items = [(kalakand_el(), 300, 900, 0.7, 70), (rasgulla_el(), 540, 890, 0.72, 100), (barfi_ink_el(), 780, 890, 0.7, 130), (kaju_ink_el(), 300, 1150, 0.66, 170), (boondi_el(), 540, 1150, 0.7, 150), (besan_el(), 780, 1150, 0.68, 190)]
    for i, (el, x, y, s_, L) in enumerate(items):
        comp(f, scale_el(el, s_), x, y)
        sweet_fuse(f, x, y - 40, L * 0.8, 0.1 + 0.02 * i, t + i, curl=44, seed=i + 1)
    if t >= tl: slam(f, stamp_el("ALL LIT", RED_I, 86), 540, 1420, -4, t, tl)
    return finish(f, n, look="night")


# ---- S3: 'I'm not making this up. India's food regulator actually has a list.' — he unrolls a scroll to the floor ----
def shot_S3(t, n):
    f = set_droom(t); t0 = st_("S3"); tl = T("a1", "list") - 0.3; tr = T("a1", "food") - 0.1
    hs = chub(f, 300, 1500, 1.02, t=t, la=(150, 165), ra=(40, 26), mouth=talk(t), expr="smirk" if t < tr else "happy", brow="up", look=(0.8, -0.2), hand_l="grip", turn=0.4, lean=3)
    k = ramp(t, tr, en_("S3") - tr - 0.1)
    scroll(f, 700, 620, 440, 790, k, t)
    comp(f, chip("INDIA'S FOOD REGULATOR", INKC, MILK, 30), 700, 590, scale=pin(t, tr))
    if k > 0.3: comp(f, chip("FSSAI", ACC_S, MILK, 60), 700, 710, scale=pin(t, tr + 0.25))
    if k > 0.6:
        comp(f, scale_el(kalakand_el(), 0.42), 590, 900); comp(f, scale_el(rasgulla_el(), 0.42), 700, 900); comp(f, scale_el(besan_el(), 0.42), 810, 900)
    icap(f, "not making", "this [UP]", t, t0 + 0.05, size=120, y=450, out=tr + 0.5)
    src(f, SRC_F, t, tl, 1462)
    return finish(f, n, look="warm")


# ---- S4: 'The shortest fuse is kalakand.' close-up, tiny fuse; S4b: 'eat it the same day' — the sun crosses a window, he munches fast ----
def shot_S4(t, n):
    f = ink_set("marig", (255, 244, 190), 540, 980, 480); tk = T("a2", "kalaakund") - 0.15; t0 = st_("S4")
    comp(f, scale_el(kalakand_el("wow" if t > tk else None), 2.0), 540, 1160)
    sweet_fuse(f, 540, 980, 90, 0.1 + 0.25 * ramp(t, t0, 1.5), t, seed=2, w=18, curl=16)
    if t >= tk: t3(f, "KALAKAND", 720, t, tk, 170)
    icap(f, "the", "[SHORTEST] fuse", t, t0 + 0.05, size=120, y=450, acc=ACC_S)
    chub_head_only(f, 190, 1370, 1.05, t=t, mouth=talk(t), expr="sus", brow="sus", look=(1, -0.3), turn=0.6)
    return finish(f, n, look="golden")


def shot_S4b(t, n):
    f = set_lunch(t); t0 = st_("S4b"); ts = T("a2", "same") - 0.1
    h = t - t0; dd = en_("S4b") - t0; hrs = clamp(h / dd) * 11
    clock_hands(f, 240, 420, 8 + hrs)
    m_ = munch(t) if "munch" in globals() else 2
    chub(f, 540, 1500, 1.15, t=t, la=(24, 14), ra=(148, -130), mouth=m_, expr="wow", brow="up", look=(0, 0.2), hold=scale_el(kalakand_el(), 0.34), hold_off=(26, -30), hold_front=True, lean=2 + 3 * math.sin(t * 10))
    cloth_front(f, TOP + 60)
    icap(f, "eat it", "[THE SAME DAY]", t, ts, size=120, y=640, acc=ACC_S)
    return finish(f, n, look="warm")


# ---- S5: 'Rasgulla, rasmalai, sandesh, those get two days, and only in the fridge.' — the fridge door swings open on all three ----
def shot_S5(t, n):
    f = set_worktop(t); t0 = st_("S5"); tt = T("a3", "two") - 0.1; tf = T("a3", "fridge") - 0.2
    chub(f, 180, 1500, 0.9, t=t, **nolean(POSE["present"]), mouth=talk(t), expr="n", brow="up", look=(1, -0.2), turn=0.5)
    comp(f, scale_el(fridge_ink_el(open_=True, eggs=False, milk=False), 1.0), 660, 1000)
    ws = [("Rusgoola", rasgulla_el(), 590, 830), ("rusmalaai", rasmalai_el(), 760, 980), ("sundaysh", sandesh_el(), 590, 1160)]
    for w_, el, x, y in ws:
        tw = T("a3", w_) - 0.1
        if t >= tw: comp(f, scale_el(el, 0.62), x, y, scale=pin(t, tw)); comp(f, chip({"Rusgoola": "RASGULLA", "rusmalaai": "RASMALAI", "sundaysh": "SANDESH"}[w_], INKC, MILK, 26), x, y + 76, scale=pin(t, tw))
    if t >= tt:
        comp(f, chip("2 DAYS", ACC_S, MILK, 72), 540, 560, scale=pin(t, tt))
    if t >= tf: comp(f, chip("IN THE FRIDGE", WATER_S, MILK, 36), 540, 660, scale=pin(t, tf))
    return finish(f, n, look="fresh")


# ---- S6: 'Milk barfi, peda, boondi laddoo, about four days.' — three on a plate, a tear-off calendar rips 4 pages ----
def shot_S6(t, n):
    f = set_droom(t); t0 = st_("S6"); tf = T("a4", "four") - 0.15
    table_front(f, TOP)
    for w_, el, x in (("Milk", barfi_ink_el("happy"), 230), ("payda", peda_el("happy"), 480), ("boondee", boondi_el("happy"), 720)):
        tw = T("a4", w_) - 0.1
        if t >= tw: comp(f, scale_el(el, 1.0), x, 1240, scale=pin(t, tw)); comp(f, chip({"Milk": "MILK BARFI", "payda": "PEDA", "boondee": "BOONDI LADDOO"}[w_], INKC, MILK, 26), x, 1110, scale=pin(t, tw))
    for j in range(4):
        tp = tf + j * 0.14
        if t < tp: pg = str(4 - j); comp(f, scale_el(calendar_el("DAY", pg), 0.72), 880, 770 - 0); break
        else:
            p = (t - tp) / 0.3
            if p < 1: rot_comp(f, scale_el(calendar_el("DAY", str(4 - j)), 0.72), 880 + 120 * p, 770 + 340 * p * p, 40 * p, 1.0, 1 - p)
    else: comp(f, chip("4 DAYS", ACC_S, MILK, 60), 840, 770, scale=pin(t, tf + 0.5))
    icap(f, "these get about", "[4 DAYS]", t, t0 + 0.1, size=130, y=450, acc=ACC_S)
    return finish(f, n, look="warm")


# ---- S7: 'Kaju katli gets a week.' — he holds it up, a 7-tick strip fills ----
def shot_S7(t, n):
    f = ink_set("rosep", (255, 255, 255), 540, 1000, 480); t0 = st_("S7"); tw = T("a5", "week") - 0.15
    hs = chub(f, 320, 1500, 1.0, t=t, **nolean(POSE["hold_up"]), mouth=talk(t), expr="happy", brow="up", look=(0.7, -0.5), hand_r="pinch", turn=0.4)
    comp(f, scale_el(kaju_ink_el("happy"), 1.2), 720, 960, scale=pin(t, t0))
    for j in range(7):
        k_ = clamp((t - t0 - 0.1) / 0.06 - j)
        xx = 250 + j * 96; cv2.rectangle(f, (xx - 38, 620), (xx + 38, 696), C(ACC if k_ >= 1 else (252, 240, 220)), -1, cv2.LINE_AA); cv2.rectangle(f, (xx - 38, 620), (xx + 38, 696), C(INKC), 5, cv2.LINE_AA)
    comp(f, chip("KAJU KATLI", INKC, MILK, 34), 720, 1090, scale=pin(t, t0 + 0.05))
    if t >= tw: icap(f, "gets", "A [WEEK]", t, tw, size=120, y=450, acc=ACC_S)
    return finish(f, n, look="warm")


# ---- S8: 'And besan laddoo gets a whole month' — he WALKS along its fuse and it never ends ----
def shot_S8(t, n):
    t0 = st_("S8"); camx = 300 * (t - t0); f = set_lane(t, camx); tm = T("a6", "month") - 0.2; x0 = 240 - camx
    pts = [(x0 + q * 3000, 1455 + 6 * math.sin(q * 26)) for q in np.linspace(0, 1, 120)]
    fuse(f, pts, 0, t, 20, spark=False)
    comp(f, scale_el(besan_el("happy", (0.6, 0)), 1.0), x0 - 30, 1430)
    w = walk(t, 520, 1490, 1.0, speed=300, t0=t0, track=True); w.pop("la"); w.pop("ra")
    chub(f, s=1.0, t=t, la=(28, 14), ra=(150, 170) if t > tm else (30, 16), mouth=talk(t), expr="wow" if t > tm else "happy", brow="up", **w)
    lane_front(f, camx)
    if t >= tm: t3(f, "A MONTH", 730, t, tm, 200, ACC_L, ACC_S)
    icap(f, "besan laddoo", "[30 DAYS]", t, t0 + 0.05, size=130, y=450, dark=True, acc=ACC_L)
    return finish(f, n, look="golden")


# ---- S8b: 'in the same box' — THE LIST, whole ----
def shot_S8b(t, n):
    f = ink_set("rosep", (255, 255, 255), 540, 1000, 500); t0 = st_("S8b"); ts = [t0 + j * 0.08 for j in range(5)]
    fuse_chart(f, t, ts, 640, 166)
    icap(f, "all in the", "[SAME BOX]", t, t0 + 0.05, size=120, y=450, acc=ACC_S)
    return finish(f, n, look="warm")


# ---- S9: 'So how does a laddoo outlive a rasgulla by a month?' — boxing-ring standoff; Chubby the referee scratches his head ----
def shot_S9(t, n):
    f = ink_set("marig", (255, 244, 190), 540, 1000, 480); t0 = st_("S9"); tm = T("b1", "month") - 0.15
    comp(f, scale_el(besan_el("angry" if t < tm else "happy"), 1.15), 240, 1160 + 8 * math.sin(t * 5)); comp(f, scale_el(rasgulla_el("sad"), 1.15), 840, 1160 + 8 * math.sin(t * 5 + 1))
    chub(f, 540, 1500, 0.86, t=t, **nolean(POSE["think"]), mouth=talk(t), expr="sus", brow="sus", look=(0.0, -0.4), lean=4 * math.sin(t * 2))
    t3(f, "HOW?", 780, t, tm - 0.15, 230)
    comp(f, chip("DAY 30", INKC, MILK, 40), 240, 960, scale=pin(t, t0 + 0.2)); comp(f, chip("DAY 2", RED_I, MILK, 40), 840, 960, scale=pin(t, t0 + 0.2))
    return finish(f, n, look="golden")


# ---- S10: 'Mostly, it's water.' — a big drop lands; S10b: three test tubes fill ----
def shot_S10(t, n):
    f = ink_set("coldp", (255, 255, 255), 540, 1000, 500); t0 = st_("S10")
    y = drop_land(t, t0 + 0.02, 260, 1120, 0.3)[0]
    comp(f, scale_el(drop_el("happy"), 2.2), 540, y)
    t3(f, "WATER", 660, t, T("b2", "water") - 0.1, 240, (190, 224, 250), WATER_S)
    return finish(f, n, look="fresh")


def shot_S10b(t, n):
    f = ink_set("coldp", (255, 255, 255), 540, 1000, 500); t0 = st_("S10b")
    tq = [T("b2", "rusgoola") - 0.1, T("b2", "kalaakund") - 0.1, T("b2", "milk") - 0.1]
    for j, (el, x, lvl, lab, sz) in enumerate(((rasgulla_el("wow"), 230, 0.5, "ABOUT HALF", 34), (kalakand_el("n"), 540, 0.26, "ABOUT 1/4", 34), (barfi_ink_el("n"), 850, 0.15, "AROUND 15%", 34))):
        if t < tq[j]: continue
        k = ramp(t, tq[j], 0.5)
        gauge(f, x, 1340, 460, lvl * k, t + j)
        comp(f, scale_el(el, 0.72), x, 760, scale=pin(t, tq[j]))
        comp(f, chip(lab, WATER_S, MILK, sz), x, 1400, scale=pin(t, tq[j] + 0.15)); comp(f, chip(("RASGULLA", "KALAKAND", "MILK BARFI")[j], INKC, MILK, 26), x, 640, scale=pin(t, tq[j]))
    icap(f, "how much of it is", "[WATER]", t, t0 + 0.02, size=120, y=450, acc=WATER_S)
    src(f, SRC_W, t, tq[2], 1470)
    return finish(f, n, look="fresh")


# ---- S11: 'Besan laddoo is roasted flour, ghee and sugar. No milk, and hardly any water' — ingredients drop in; the gauge stays dry ----
def shot_S11(t, n):
    f = set_stove(t, on=0.5, flame_w=300); f = inkify(f, 0.1); t0 = st_("S11"); tn = T("b3", "No") - 0.1; th = T("b3", "hardly") - 0.1
    chub(f, 190, 1500, 0.9, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="n", brow="up", look=(1, 0.2), hand_r="point", turn=0.5)
    comp(f, scale_el(kadai_el(), 1.0), 620, 1160); comp(f, scale_el(besan_el("happy"), 0.86), 620, 1050, scale=pin(t, t0))
    for w_, txt, x, y in (("roasted", "ROASTED FLOUR", 380, 760), ("ghee", "GHEE", 640, 660), ("sugar", "SUGAR", 860, 800)):
        tw = T("b3", w_) - 0.12
        if t >= tw: comp(f, chip(txt, ACC_S, MILK, 36), x, y, scale=pin(t, tw))
    if t >= tn: slam(f, stamp_el("NO MILK", RED_I, 70), 790, 900, -6, t, tn)
    if t >= th: gauge(f, 910, 1300, 300, 0.04, t, 74); comp(f, chip("HARDLY ANY", WATER_S, MILK, 30), 830, 1370, scale=pin(t, th))
    return finish(f, n, look="warm")


# ---- S12: 'And germs need water, same as you.' — Chubby and a germ drink side by side; S12b: 'a full meal' — germs at a banquet on a rasgulla ----
def shot_S12(t, n):
    f = set_droom(t); t0 = st_("S12"); ts = T("b4", "same") - 0.1
    chub(f, 280, 1500, 1.02, t=t, la=(24, 14), ra=(148, -130), mouth=talk(t), expr="happy", brow="up", look=(1, 0.1), hold=scale_el(glass_el(0.7), 0.6), hold_off=(40, 10), hold_front=True, turn=0.5)
    table_front(f, TOP)
    comp(f, scale_el(germ_el("happy", ph=int(t * 8) % 4), 1.2), 760, 1150 + 10 * math.sin(t * 4)); rot_comp(f, scale_el(glass_el(0.6), 0.5), 870, 1230, 0, 1.0, 1.0, 0)
    icap(f, "germs need", "[WATER]", t, t0 + 0.06, size=130, y=450, acc=WATER_S, out=ts)
    if t >= ts: icap(f, "same as", "[YOU]", t, ts, size=140, y=450, acc=ACC_S)
    return finish(f, n, look="warm")


def shot_S12b(t, n):
    f = ink_set("marig", (255, 244, 190), 540, 1000, 490); tm = T("b4", "meal") - 0.15; t0 = st_("S12b")
    comp(f, scale_el(glass_el(0.9), 1.4), 230, 1120, scale=pin(t, t0)); comp(f, chip("MILK", WATER_S, MILK, 40), 230, 1330, scale=pin(t, t0 + 0.1))
    comp(f, scale_el(rasgulla_el(None), 1.5), 680, 1140)
    if t >= tm - 0.3: germ_crowd(f, 680, 1000, t, 7, 0.5, 240, "happy", 4)
    if t >= tm: t3(f, "FULL MEAL", 690, t, tm, 160)
    else: icap(f, "milk is", "[EVEN WORSE]", t, t0 + 0.04, size=120, y=450)
    src(f, "Source: FSSAI · BVC Patna dairy-microbiology notes", t, t0 + 0.2, 1462)
    return finish(f, n, look="golden")


# ---- S13: 'Scientists score this from zero to one' — the plank from our namkeen video, he walks on ----
def shot_S13(t, n):
    f = ink_set("coldp", (255, 255, 255), 540, 980, 480); t0 = st_("S13"); stop = t0 + 2.2; X = thirst_meter(f, t)
    amt = 1 - ramp(t, stop - 0.25, 0.25)
    w = walk(t, -60 + 280 * max(0.0, min(t - t0, stop - t0)), 1270, 0.82, speed=280, t0=t0, amt=amt, track=True)
    chub(f, s=0.82, t=t, mouth=talk(t), expr="happy", brow="up", **w)
    comp(f, chip("REAL NAME: WATER ACTIVITY", INKC, MILK, 30), 540, 1440, scale=pin(t, T("c1", "zero") - 0.1))
    icap(f, "how much water can a", "germ [USE]?", t, t0 + 0.05, size=110, y=450, acc=WATER_S)
    return finish(f, n, look="fresh")


def flag(f, x, y, el, txt, col, k=1.0, h=430):
    cv2.line(f, (int(x), int(y)), (int(x), int(y - h * k)), C(INKC), 7, cv2.LINE_AA)
    comp(f, el, x, y - h - 90, scale=k); comp(f, chip(txt, col, MILK, 36), x, y - h + 4, scale=k)


# ---- S14: 'Most bacteria need about 0.9, but mould gets by on 0.7' — two flags on the plank ----
def shot_S14(t, n):
    f = ink_set("coldp", (255, 255, 255), 540, 980, 480); X = thirst_meter(f, t); t9 = T("c2", "nine") - 0.3; t7 = T("c2", "seven") - 0.3
    chub(f, X(0.36), 1270, 0.72, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="n", brow="up", look=(1, -0.2), hand_r="point", turn=0.5)
    if t >= T("c2", "bacteria") - 0.15: flag(f, X(0.9), 1270, scale_el(germ_el("n"), 0.66), "0.9", INKC, pin(t, T("c2", "bacteria") - 0.15))
    if t >= T("c2", "mould") - 0.15: flag(f, X(0.7), 1270, scale_el(mould_el("happy"), 0.66), "0.7", MOULD_S, pin(t, T("c2", "mould") - 0.15))
    icap(f, "bacteria need", "[0.9]", t, st_("S14") + 0.05, size=130, y=450, out=t7)
    if t >= t7: icap(f, "mould gets by on", "[0.7]", t, t7, size=130, y=450, acc=MOULD_S)
    src(f, SRC_A, t, t7, 1462)
    return finish(f, n, look="fresh")


# ---- S15: 'Barfi sits right in between, around 0.8.' he walks it there; S15b: 'too dry for most bacteria, not for mould' — germ sulks off, mould climbs on ----
def shot_S15(t, n):
    f = ink_set("coldp", (255, 255, 255), 540, 980, 480); X = thirst_meter(f, t); t0 = st_("S15"); te = T("c3", "zero") - 0.1
    k = clamp((t - t0) / 1.4)
    flag(f, X(0.9), 1270, scale_el(germ_el("n"), 0.66), "0.9", INKC); flag(f, X(0.7), 1270, scale_el(mould_el("happy"), 0.66), "0.7", MOULD_S)
    xw = X(0.1) + (X(0.8) - X(0.1) - 60) * k; am = 1.0 if 0 < k < 0.9 else 0.0
    wk = walk(min(t, t0 + 1.4), xw, 1270, 0.72, speed=(X(0.8) - X(0.1)) / 1.4, t0=t0, amt=am, track=True); wk.pop("la"); wk.pop("ra")
    hs = chub(f, s=0.72, t=t, la=(28, 14), ra=(130, 150), mouth=talk(t), expr="happy", brow="up", hand_r="grip", **wk)
    comp(f, scale_el(barfi_ink_el("n"), 0.5), hs[1][0] + 16, hs[1][1] - 40)
    if t >= te: comp(f, chip("BARFI: 0.8", ACC_S, MILK, 50), 540, 1440, scale=pin(t, te))
    icap(f, "barfi sits", "[IN BETWEEN]", t, t0 + 0.05, size=120, y=450, acc=ACC_S)
    return finish(f, n, look="fresh")


def shot_S15b(t, n):
    f = ink_set("mouldp", (255, 255, 255), 540, 1000, 490); t0 = st_("S15b"); tm = T("c3", "mould") - 0.2
    comp(f, scale_el(barfi_ink_el("wow"), 1.9), 540, 1160)
    k = ramp(t, t0, 1.1); comp(f, scale_el(germ_el("sad"), 0.9), 280 - 130 * k, 930 + 60 * k); comp(f, chip("TOO DRY", INKC, MILK, 46), 300, 780, scale=pin(t, t0 + 0.08))
    if t >= tm:
        d_ = eo(clamp((t - tm) / 0.35)); comp(f, scale_el(mould_el("love" if False else "happy"), 1.0), 760, 1000 - 200 * (1 - d_)); fuzz(f, 540, 1090, 300, 80, ramp(t, tm, 1.0), t, 11)
    icap(f, "too dry for", "most [BACTERIA]", t, t0 + 0.04, size=110, y=450, out=tm)
    if t >= tm: icap(f, "not for", "[MOULD]", t, tm, size=150, y=450, acc=MOULD_S)
    return finish(f, n, look="warm")


# ---- S16: 'That's why barfi's classic problem is a bit of fuzz on top.' — Chubby lifts the lid of a box: fuzz grows in time-lapse, take ----
def shot_S16(t, n):
    f = set_droom(t); t0 = st_("S16"); tf = T("c4", "fuzz") - 0.15; tk = take(t, tf)
    chub(f, 210, 1500 + (tk["dy"] if t > tf else 0), 0.98, t=t, **nolean(POSE["cheek"]), mouth=("jaw" if tf < t < tf + 0.7 else talk(t)), expr=tk["expr"] if t > tf else "sus", brow=tk["brow"] if t > tf else "sus", look=(1, 0.2), turn=0.5, squash=tk["squash"] if t > tf else 0)
    table_front(f, TOP)
    comp(f, scale_el(barfi_ink_el("sad" if t > tf else "n"), 1.6), 660, 1170)
    fuzz(f, 660, 1110, 330, 90, ramp(t, tf - 0.7, 1.6), t, 13)
    if t >= tf: t3(f, "FUZZ", 720, t, tf, 240, MOULD_L, MOULD_S)
    icap(f, "barfi's classic", "[PROBLEM]", t, t0 + 0.04, size=120, y=450)
    src(f, "Source: Badola et al. 2018, J Food Sci Technol", t, t0 + 0.3, 1462)
    return finish(f, n, look="warm")


# ---- S17: 'please don't just scrape it off' — knife in hand, he scrapes: looks clean! ; S17b: 'What you can see is only the top' — a magnifier reveals what's under ----
def shot_S17(t, n):
    f = set_droom(t); ts = T("c5", "scrape") - 0.2; t0 = st_("S17")
    k = ramp(t, ts, 1.0); sw = 14 * math.sin((t - ts) * 12) if t > ts else 0
    hs = chub(f, 210, 1500, 0.98, t=t, la=(24, 14), ra=(76 + sw, 50), mouth=talk(t), expr="smirk", brow="up", look=(1, 0.3), hand_r="grip", turn=0.5)
    table_front(f, TOP)
    comp(f, scale_el(barfi_ink_el("n"), 1.6), 660, 1170); fuzz(f, 660, 1110, 330, 90, 1 - k, t, 13)
    hx, hy = hs[1]; knife_ink_at(f, hx, hy, 25 + sw * 0.8, 0.9); grip_hand(f, hx, hy, 0.98)
    if t > ts + 0.05 and k < 1: crumbs(f, 720, 1090, t, ts + 0.05, 9, 180, MOULD)
    if t >= ts: slam(f, stamp_el("DON'T", RED_I, 80), 760, 800, -5, t, ts + 0.1)
    icap(f, "just", "[SCRAPE] it?", t, t0 + 0.05, size=130, y=450, acc=MOULD_S)
    return finish(f, n, look="warm")


def shot_S17b(t, n):
    f = set_droom(t, dim=0.5); t0 = st_("S17b"); tt = T("c5", "top") - 0.2
    spotlight(f, 540, 1100, 400, 0.5)
    k = ramp(t, t0, tt - t0 + 0.2)
    roots_cut(f, 540, 1120, 620, 420, 0.0, t, top=1.0, bugs=False)
    if t >= tt:
        comp(f, chip("ONLY THE TOP", MOULD_S, MILK, 56), 540, 790, scale=pin(t, tt))
    icap(f, "what you can see", "is [ONLY THE TOP]", t, t0 + 0.04, size=90, y=450, dark=True, acc=MOULD_L)
    return finish(f, n, look="night")


# ---- S18: 'On soft food the roots go deeper...' — the cut-away: threads + hidden bacteria; S18b: the whole piece goes in the bin ----
def shot_S18(t, n):
    f = set_droom(t, dim=0.5); t0 = st_("S18"); tr = T("c6", "roots") - 0.15; tb = T("c6", "bacteria") - 0.15
    spotlight(f, 540, 1100, 460, 0.5)
    roots_cut(f, 540, 1120, 620, 420, ramp(t, tr, 1.1), t, 1.0, bk=pin(t, tb))
    if t >= tr: comp(f, chip("ROOTS", MOULD_S, MILK, 44), 900, 900, scale=pin(t, tr))
    if t >= tb: comp(f, chip("BACTERIA YOU CAN'T SEE", INKC, MILK, 34), 540, 1400, scale=pin(t, tb))
    icap(f, "on soft food the roots", "go [DEEPER]", t, t0 + 0.04, size=110, y=450, dark=True, acc=MOULD_L)
    src(f, SRC_U, t, t0 + 0.3, 1466)
    return finish(f, n, look="night")


def shot_S18b(t, n):
    f = set_droom(t); t0 = st_("S18b"); tb = T("c6", "bin") - 0.25
    op = ramp(t, tb - 0.3, 0.2)
    chub(f, 250, 1500, 1.0, t=t, la=(24, 14), ra=(70 - 30 * op, 40), mouth=talk(t), expr="gross", brow="sad", look=(1, 0.3), hand_r="pinch", turn=0.5)
    comp(f, scale_el(bin_ink_el(op), 1.3), 740, 1300)
    if t < tb + 0.1: comp(f, scale_el(barfi_ink_el("sad"), 0.8), 480 + 260 * ramp(t, t0, tb - t0 + 0.1), 1020 - 30 * math.sin(3.14 * ramp(t, t0, tb - t0 + 0.1)))
    icap(f, "the", "[WHOLE PIECE]", t, t0 + 0.05, size=130, y=450, acc=MOULD_S)
    return finish(f, n, look="warm")


# ---- S19: 'So do you just put everything in the fridge? Nearly.' — he's mid-stuff, freezes on 'Nearly' ----
def shot_S19(t, n):
    f = set_fridge_night(t); f = inkify(f, 0.1); tn = T("d1", "Nearly") - 0.1; t0 = st_("S19")
    fz = t > tn
    tt = tn if fz else t
    hs = chub(f, 330, 1490, 1.04, t=t, la=(30, 16), ra=(88 + 8 * math.sin(tt * 8), 60), mouth=talk(t), expr="wow" if fz else "happy", brow="up", look=(1, -0.2), turn=0.6, lean=5, hand_r="grip")
    giftbox(f, hs[1][0] + 120, hs[1][1] + 80, 0.46, 0.0)
    for i in range(3):
        if t >= t0 + 0.1 + i * 0.14: comp(f, scale_el((kalakand_el(), rasgulla_el(), barfi_ink_el())[i], 0.5), 560 + 130 * i, 1440 + 10 * math.sin(tt * 6 + i))
    icap(f, "put", "[EVERYTHING] in the fridge?", t, t0 + 0.05, size=84, y=450, dark=True, acc=(170, 220, 250), out=tn)
    if fz: t3(f, "NEARLY", 500, t, tn, 200, (190, 224, 250), WATER_S)
    return finish(f, n, look="cool")


# ---- S20: 'In one lab test, sealed barfi lasted nine days at thirty degrees, and thirty five days in the fridge.' — two race bars ----
def shot_S20(t, n):
    f = ink_set("coldp", (255, 255, 255), 540, 1000, 500); t0 = st_("S20"); t9 = T("d2", "nine") - 0.1; t3_ = T("d2", "thirty", 1) - 0.1
    comp(f, chip("ONE LAB TEST · SEALED POUCH", INKC, MILK, 34), 540, 610, scale=pin(t, t0 + 0.05))
    for yy, tt_, dd, col, lab, th in ((830, t9, 9, ACC, "ROOM, 30°C", 0.85), (1120, t3_, 35, WATER, "FRIDGE, 7°C", 0.25)):
        comp(f, scale_el(thermo_ink_el(th, False), 0.6), 150, yy, scale=pin(t, t0 + 0.1)); comp(f, chip(lab, INKC, MILK, 28), 490, yy - 90, scale=pin(t, t0 + 0.1))
        k = ramp(t, tt_, 0.8); L_ = 18 * dd * k + 2
        cv2.rectangle(f, (250, yy - 40), (int(250 + L_), yy + 40), C(col), -1, cv2.LINE_AA); cv2.rectangle(f, (250, yy - 40), (int(250 + L_), yy + 40), C(INKC), 6, cv2.LINE_AA)
        comp(f, scale_el(barfi_ink_el(), 0.34), 250 + L_, yy, scale=pin(t, t0 + 0.1))
        if k > 0: comp(f, chip(f"{int(round(dd * k))} DAYS", col if col == ACC else WATER_S, MILK, 40), min(800, 250 + L_ + 100), yy + 78, scale=pin(t, tt_))
    src(f, SRC_L, t, t0 + 0.3, 1320)
    icap(f, "the fridge", "[BUYS TIME]", t, t3_, size=120, y=450, acc=WATER_S)
    return finish(f, n, look="fresh")


# ---- S21: 'But it wasn't mould that finished it off. It went dry, hard and sandy.' — mould shrugs, the barfi cracks word by word ----
def shot_S21(t, n):
    f = set_fridge_night(t); f = inkify(f, 0.12); t0 = st_("S21"); td = T("d3", "dry") - 0.1; th = T("d3", "hard") - 0.1; ts = T("d3", "sandy") - 0.15
    k = ramp(t, td, ts - td + 0.4)
    comp(f, scale_el(barfi_ink_el("sad" if k > 0.2 else "n", dry=k), 1.8), 540, 1120)
    comp(f, scale_el(mould_el("sad"), 0.7), 860, 1370, op=clamp(1 - ramp(t, td, 0.3)))
    if t < td: comp(f, chip("NOT MOULD", RED_I, MILK, 40), 800, 1230, scale=pin(t, T("d3", "mould") - 0.2))
    for tt_, wd, x, y in ((td, "DRY", 250, 760), (th, "HARD", 560, 700), (ts, "SANDY", 850, 790)):
        if t >= tt_: t3(f, wd, y, t, tt_, 110, (190, 224, 250), WATER_S, x=x)
    return finish(f, n, look="cool")


# ---- S22: 'That's your rock hard fridge barfi.' he bites: CLANK, double take; S22b: 'So keep it airtight, not in the cardboard box' ----
def shot_S22(t, n):
    f = set_droom(t); t0 = st_("S22"); tb = T("d4", "rock") - 0.15; tk = flinch(t, tb)
    t3(f, "ROCK HARD", 760, t, tb, 150)
    hit = t > tb
    hs = chub(f, 540, 1540, 1.25, t=t, la=(30, 14), ra=(148, -130), mouth=("jaw" if tb < t < tb + 0.4 else talk(t)), expr="gross" if hit else "n", brow="sad" if hit else "up", look=(0.4, 0), hold=scale_el(barfi_ink_el(None, dry=1.0), 0.5), hold_off=(26, -30), hold_front=True, lean=tk[0], squash=tk[1])
    if tb <= t < tb + 0.5: comp(f, burst_el("KLONK!", ACC_L, INKC, 66), 820, 980, scale=pin(t, tb, 0.08))
    table_front(f, TOP + 70)
    return finish(f, n, look="warm")


def shot_S22b(t, n):
    f = set_worktop(t); t0 = st_("S22b"); ta = T("d4", "airtight") - 0.15; tc = T("d4", "cardboard") - 0.15
    chub(f, 170, 1500, 0.86, t=t, **nolean(POSE["present"]), mouth=talk(t), expr="happy", brow="up", look=(1, -0.1), turn=0.5)
    worktop_front(f, TOP)
    comp(f, scale_el(jar_ink_el(ramp(t, ta, 0.2), "none"), 1.05), 470, 1170, scale=pin(t, t0)); comp(f, scale_el(barfi_ink_el("happy"), 0.46), 470, 1230)
    if t >= ta: comp(f, chip("AIRTIGHT", WATER_S, MILK, 44), 470, 830, scale=pin(t, ta))
    if t >= tc:
        giftbox(f, 800, 1320, 0.56, 0.0); cv2.line(f, (650, 980), (960, 1320), C(RED_I), 18, cv2.LINE_AA); cv2.line(f, (960, 980), (650, 1320), C(RED_I), 18, cv2.LINE_AA)
    return finish(f, n, look="fresh")


# ---- S23: 'Which brings us to the great Diwali re-gift.' — Chubby in the corridor, he presents the box like a trophy; ink title ----
def shot_S23(t, n):
    f = set_corridor(t, 420); t0 = st_("S23"); tg = T("e1", "regift") - 0.3
    t3(f, "RE-GIFT", 470, t, tg, 190)
    tk = keyed(t, [(t0, 0.0), (tg, 1.0)])
    yb = 1400 - 540 * tk
    hs = chub(f, 540, 1500, 1.1, t=t, la=(60 + 80 * tk, 70 + 80 * tk), ra=(60 + 80 * tk, 70 + 80 * tk), mouth=talk(t), expr="smirk", brow="up", look=(0, -0.6 * tk))
    giftbox(f, 540, yb, 0.5, 0.0)
    sweet_fuse(f, 540, yb - 200, 90, 0.3, t, seed=2)
    return finish(f, n, look="warm")


# ---- S24: 'Your neighbour gives you a box, you pass it to your cousin, and your cousin gives it to your boss.' — ONE tracking shot down the corridor, the box flies on ARCS hand to hand, its fuse keeps burning ----
PEOPLE = [(210, "aunty", (230, 70, 130), "NEIGHBOUR"), (1050, None, None, "YOU"), (1890, "cousin", (70, 130, 190), "COUSIN"), (2730, "boss", (130, 130, 150), "BOSS")]


def box_world(t):
    keys = [T("e2", "gives") - 0.05, T("e2", "pass") - 0.05, T("e2", "gives", 1) - 0.05]
    xs = [p[0] for p in PEOPLE]; dur = 0.8; x = xs[0]; lift = 0.0
    for i, k_ in enumerate(keys):
        if t >= k_:
            p = clamp((t - k_) / dur); e = eio(p); x = xs[i] + (xs[i + 1] - xs[i]) * e; lift = 300 * 4 * p * (1 - p) if p < 1 else 0.0
    return x + 110, lift


def shot_S24(t, n):
    bx, lift = box_world(t); camx = bx - 540; f = set_corridor(t, camx); t0 = st_("S24")
    for i, (wx, kind, shirt, lab) in enumerate(PEOPLE):
        sx = wx - camx
        if sx < -240 or sx > W + 240: continue
        kw = dict(shirt=shirt) if shirt else {}
        here = abs(bx - 110 - wx) < 60
        chub(f, sx, 1500, 0.98, t=t, la=(30, 16), ra=(84, 62) if here else (24, 12), mouth=talk(t) if kind is None else (1 if here else 0), expr="happy" if here else "n", brow="up", look=((bx - wx) / 300 if abs(bx - wx) > 60 else 0.5, 0), turn=0.5 if bx > wx else -0.5, **kw)
        if kind: dress(f, sx, 1500, 0.98, kind)
        comp(f, chip(lab, ACC_S if kind is None else INKC, MILK, 34), sx, 900)
    sx = bx - camx; yb = 1395 - lift
    giftbox(f, sx, yb, 0.38, 0.0)
    pr = clamp((t - t0) / (en_("S24") - t0))
    sweet_fuse(f, sx, yb - 150, 46, 0.2 + 0.6 * pr, t, seed=3)
    day = 1 + int(clamp((t - t0) / (en_("S24") - t0)) * 6.9)
    comp(f, chip(f"DAY {day}", RED_I, MILK, 54), 540, 620)
    icap(f, "and the", "[FUSE] keeps burning", t, T("e2", "cousin") - 0.2, size=84, y=450, acc=ACC_S)
    return finish(f, n, look="warm")


# ---- S25: 'Nobody's fuse resets.' the boss lifts the lid: stink; S25b: 'That kalakand has been dead since Tuesday.' tombstone ----
def shot_S25(t, n):
    f = set_corridor(t, 2730 + 110 - 540 + 100); t0 = st_("S25"); tr = T("e3", "resets") - 0.15
    op = ramp(t, t0 + 0.05, 0.3); tk = take(t, t0 + 0.3)
    chub(f, 300, 1500, 1.0, shirt=(130, 130, 150), t=t, la=(70, 60), ra=(84, 62), mouth="jaw" if t > t0 + 0.35 else 0, expr=tk["expr"] if t > t0 + 0.3 else "n", brow=tk["brow"] if t > t0 + 0.3 else "n", look=(1, 0.3), turn=0.5, squash=tk["squash"] if t > t0 + 0.3 else 0)
    dress(f, 300, 1500, 1.0, "boss")
    giftbox(f, 690, 1380, 0.76, op)
    stink(f, 660, 1050, t, 3, 260, MOULD_S)
    if t >= tr: slam(f, stamp_el("NO RESET", RED_I, 80), 620, 760, -5, t, tr)
    icap(f, "nobody's fuse", "[RESETS]", t, t0 + 0.05, size=120, y=450)
    return finish(f, n, look="warm")


def shot_S25b(t, n):
    f = set_droom(t, dim=0.48); t0 = st_("S25b"); tt = T("e3", "Tuesday") - 0.15
    spotlight(f, 540, 1130, 380, 0.5)
    table_front(f, TOP + 10)
    comp(f, scale_el(tomb_el(), 1.25), 540, 1050, scale=pin(t, t0, 0.2)); comp(f, chip("R.I.P.", INKC, MILK, 50), 540, 960, scale=pin(t, t0 + 0.05, 0.2))
    comp(f, scale_el(kalakand_el("sad"), 0.9), 540, 1290); fuzz(f, 540, 1240, 230, 50, 1.0, t, 15)
    icap(f, "that kalakand has been", "[DEAD]", t, t0 + 0.04, size=130, y=450, dark=True, acc=ACC_L, out=tt)
    if t >= tt: comp(f, chip("SINCE TUESDAY", RED_I, MILK, 66), 540, 480, scale=pin(t, tt))
    return finish(f, n, look="night")


# ---- S26: 'At the shop, you can check.' the mithai counter; S26b: 'best before date on the tray' — a tag pops on the tray, Chubby's magnifier ----
def shot_S26(t, n):
    f = set_shop(t); t0 = st_("S26"); tc = T("e4", "check") - 0.2
    chub(f, 760, 1500, 1.0, t=t, **nolean(POSE["think"]), mouth=talk(t), expr="sus", brow="sus", look=(-1, 0.6), turn=-0.5)
    shop_front(f, 1300, t)
    for x in (220, 570):
        comp(f, scale_el(tray_el(), 0.74), x, 1250)
        for j in range(3): comp(f, scale_el((kalakand_el(), barfi_ink_el(), kaju_ink_el())[j if x == 220 else 2 - j], 0.36), x - 100 + j * 100, 1190)
    if t >= tc: t3(f, "CHECK", 720, t, tc, 200)
    icap(f, "at the", "[SHOP]", t, t0 + 0.05, size=130, y=450)
    return finish(f, n, look="golden")


def shot_S26b(t, n):
    f = set_shop(t, 0.1); f = dof(f, 5); t0 = st_("S26b"); tb = T("e4", "best") - 0.15; tt = T("e4", "tray") - 0.2
    x0 = 540; comp(f, scale_el(tray_el(), 1.8), x0, 1290)
    for j in range(3): comp(f, scale_el(barfi_ink_el("happy"), 0.82), x0 - 240 + j * 240, 1140)
    comp(f, chip("SINCE 2020", INKC, MILK, 52), 540, 620, scale=pin(t, t0 + 0.05))
    if t >= tb:
        k = pin(t, tb); comp(f, scale_el(tag_el2(), 1.6), 540, 880, scale=k)
        if k > 0.8: comp(f, chip("BEST BEFORE", ACC_S, MILK, 40), 556, 840); comp(f, chip("6 NOV", INKC, MILK, 62), 556, 920)
    icap(f, "loose sweets", "must [SHOW IT]", t, t0 + 0.05, size=110, y=450, acc=ACC_S)
    src(f, SRC_B, t, tb, 1462)
    return finish(f, n, look="golden")


# ---- S27: 'With a gift box, go by the list.' he holds the list next to a dateless box; S27b: 'It's a guide, and a hot kitchen means less time' — the fuses speed up, thermometer climbs ----
def shot_S27(t, n):
    f = set_droom(t); t0 = st_("S27"); tl = T("e5", "list") - 0.2
    chub(f, 230, 1500, 1.0, t=t, la=(24, 14), ra=(124, 40), mouth=talk(t), expr="n", brow="up", look=(1, 0), hand_r="grip", turn=0.5)
    table_front(f, TOP)
    giftbox(f, 740, 1370, 0.74, 0.0)
    comp(f, chip("NO DATE?", RED_I, MILK, 44), 740, 900, scale=pin(t, t0 + 0.1))
    if t >= tl: scroll(f, 420, 760, 230, 340, ramp(t, tl, 0.3)); comp(f, chip("THE LIST", ACC_S, MILK, 34), 420, 730, scale=pin(t, tl))
    icap(f, "gift box?", "go by [THE LIST]", t, t0 + 0.05, size=110, y=450, acc=ACC_S)
    return finish(f, n, look="warm")


def shot_S27b(t, n):
    f = set_worktop(t); mood(f, (250, 110, 40), 0.18); t0 = st_("S27b"); th = T("e5", "hot") - 0.15
    worktop_front(f, TOP)
    sp = 0.1 + (0.03 if t < th else 0.03 + 0.5 * (t - th))
    for x, el, L, sd in ((330, kaju_ink_el("wow"), 180, 1), (620, boondi_el("wow"), 160, 2), (880, barfi_ink_el("wow"), 150, 3)):
        comp(f, scale_el(el, 0.8), x, 1240); sweet_fuse(f, x, 1170, L, clamp(sp + 0.02 * sd * (t - t0)), t + sd, seed=sd)
    comp(f, scale_el(thermo_ink_el(0.45 + 0.5 * ramp(t, th, 0.7), False), 1.0), 130, 1060)
    if t >= th: t3(f, "HOT = LESS TIME", 740, t, th, 104)
    icap(f, "it's only", "a [GUIDE]", t, t0 + 0.04, size=130, y=450, acc=ACC_S)
    return finish(f, n, look="warm")


# ---- S28: 'Milky and soft first, dry and nutty last.' — sweets slide into a queue on the belt of an arrow ----
def shot_S28(t, n):
    f = ink_set("marig", (255, 244, 190), 540, 1000, 490); t0 = st_("S28"); tf = T("f1", "first") - 0.15; tl = T("f1", "last") - 0.15
    icap(f, "so here's", "the [ORDER]", t, t0 + 0.05, size=120, y=450, acc=ACC_S, out=tf - 0.2)
    if t < tf + 0.05: chub(f, 540, 1500, 1.15, t=t, **nolean(POSE["hold_up"]), mouth=talk(t), expr="happy", brow="up", look=(0.2, -0.3), hand_r="point", lean=4)
    if t >= tf: 
        comp(f, scale_el(rasgulla_el("wow"), 0.8), 200, 780, scale=pin(t, tf)); comp(f, scale_el(kalakand_el("wow"), 0.72), 410, 790, scale=pin(t, tf + 0.08))
        t3(f, "FIRST", 560, t, tf, 170, ACC_L, ACC_S, x=330); comp(f, chip("MILKY + SOFT", ACC_S, MILK, 40), 300, 930, scale=pin(t, tf))
    if t >= tl:
        comp(f, scale_el(kaju_ink_el("happy"), 0.8), 620, 1280, scale=pin(t, tl)); comp(f, scale_el(besan_el("happy"), 0.8), 840, 1270, scale=pin(t, tl + 0.08))
        t3(f, "LAST", 1100, t, tl, 170, (232, 196, 140), (150, 100, 50), x=750); comp(f, chip("DRY + NUTTY", N_S, MILK, 40), 730, 1420, scale=pin(t, tl))
    if t >= tf: draw_arrow(f, 420, 990, 590, 1040, ramp(t, tf + 0.1, tl - tf), INKC, 12, 40)
    return finish(f, n, look="golden")


# ---- S29: 'Screenshot this.' a shutter flash, then THE LIST as a clean card, held ----
def shot_S29(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 560); t0 = st_("S29")
    tt = [t0, T("f2", "Kalaakund") - 0.1, T("f2", "rusgoola") - 0.1, T("f2", "burfee") - 0.1, T("f2", "kaaju") - 0.1, T("f2", "luddoo") - 0.1]
    cv2.rectangle(f, (64, 500), (1016, 1460), C((254, 250, 240)), -1, cv2.LINE_AA); cv2.rectangle(f, (64, 500), (1016, 1460), C(INKC), 7, cv2.LINE_AA)
    fuse_chart(f, t, tt[1:], 610, 164, cur=next((i for i in range(4, -1, -1) if t >= tt[i + 1]), None), s_chip=40)
    ui_word(f, "screenshot", "[THIS]", 410, t, t0 + 0.02, col=INKC, acc=ACC_S, size=110)
    if t >= tt[5]: src(f, "Source: FSSAI guidance note (a guide, not law)", t, tt[5] + 0.1, 1436)
    if t0 + 0.2 < t < t0 + 0.32:
        f = f * 0.3 + 0.7
    return finish(f, n, look="warm")


# ---- S30: 'And if it smells sour or grows fuzz, bin it, whatever the list says.' — the sniff, gross face, bin ----
def shot_S30(t, n):
    f = set_droom(t); t0 = st_("S30"); ts = T("f3", "sour") - 0.2; tb = T("f3", "bin") - 0.15
    sn = ts < t < tb; bk = 0.04 * math.sin((t - t0) * 22) if sn else 0
    hs = chub(f, 300, 1500, 1.12, t=t, la=(24, 14), ra=(148, -120), mouth=talk(t), expr="gross" if t > ts + 0.2 else "sus", brow="sad" if t > ts + 0.2 else "sus", look=(0.4, 0.2), lean=4 + 40 * bk, turn=0.4, hand_r="pinch")
    hx, hy = hs[1]
    if t < tb: comp(f, scale_el(barfi_ink_el("sad"), 0.55), hx + 56, hy + 6); fuzz(f, hx + 56, hy - 26, 120, 26, ramp(t, T("f3", "fuzz") - 0.3, 0.6), t, 17, n=22)
    stink(f, hx + 70, hy - 40, t, 3, 150, MOULD_S)
    table_front(f, TOP + 70)
    if t >= tb:
        comp(f, scale_el(bin_ink_el(0.0), 1.2), 780, 1300); slam(f, stamp_el("BIN IT", RED_I, 96), 700, 860, -6, t, tb)
    icap(f, "smells", "[SOUR]?", t, ts, size=130, y=450, acc=MOULD_S, out=tb)
    return finish(f, n, look="warm")


# ---- S31: send it — the corridor, he rings the neighbour's bell, phone + logo ----
def shot_S31(t, n):
    t0 = st_("S31"); f = set_corridor(t, 200); vend = LINES["g1"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("g1", "Send") + 0.3
        comp(f, scale_el(phone2_el("your box. it's day 6.", "i know you know", pr), 0.82), 760, 960, scale=pin(t, t0))
        if pr and t < T("g1", "Send") + 0.75:
            rr = (t - T("g1", "Send") - 0.3) / 0.45; cv2.circle(f, (760, 1230), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        chub(f, 300, 1500, 1.05, t=t, la=(20, 12), ra=(70, 40), mouth=talk(t), expr="smirk", brow="up", hand_r="point", look=(1, -0.1), turn=0.5)
        ui_word(f, "send this to whoever gave you", "THAT [BOX]", 440, t, T("g1", "whoever") - 0.1, col=INKC, acc=ACC_S, size=110)
    else:
        k = pin(t, vend + 0.2, 0.4); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INKC, lead_size=42), 540, 1030, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 540, 1500, 0.7, t=t, la=(150, 170), ra=(150, 170), mouth=3, expr="happy", brow="up")
    return finish(f, n, look="golden")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TF, 0.45, 18), (T("i2", "tonight") - 0.15, 0.3, 10), (T("i2", "month") - 0.2, 0.3, 10), (T("i3", "cracker") - 0.15, 0.3, 12), (T("i3", "lit") - 0.2, 0.35, 14), (T("a2", "kalaakund") - 0.15, 0.3, 12), (T("a3", "two") - 0.1, 0.3, 10), (T("a4", "four") - 0.15, 0.25, 8), (T("a5", "week") - 0.15, 0.25, 8), (T("a6", "month") - 0.2, 0.35, 14),
           (T("b1", "month") - 0.3, 0.3, 10), (T("b2", "water") - 0.1, 0.3, 12), (T("b3", "No") - 0.1, 0.3, 12), (T("b4", "meal") - 0.15, 0.3, 10), (T("c3", "mould") - 0.2, 0.3, 10), (T("c4", "fuzz") - 0.15, 0.35, 14), (T("c5", "scrape") - 0.1, 0.3, 12), (T("c6", "bin") - 0.25, 0.3, 10),
           (T("d1", "Nearly") - 0.1, 0.35, 14), (T("d3", "hard") - 0.1, 0.25, 8), (T("d4", "rock") - 0.15, 0.4, 18), (T("e1", "regift") - 0.3, 0.3, 12), (T("e3", "resets") - 0.15, 0.3, 12), (T("e3", "Tuesday") - 0.15, 0.35, 14), (T("e4", "check") - 0.2, 0.25, 8), (T("e5", "hot") - 0.15, 0.3, 10), (T("f1", "first") - 0.15, 0.25, 8), (T("f1", "last") - 0.15, 0.25, 8), (T("f3", "bin") - 0.15, 0.4, 16), (T("g1", "Send") + 0.3, 0.2, 8)]


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
