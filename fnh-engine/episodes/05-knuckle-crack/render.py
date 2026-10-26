"""BODY FILES 05 — 'What really happens when you crack your knuckles'. White-paper medical explainer (plates.py kit).
Usage: render.py OUT.mp4 [frame,frame,...]   (GUIDES=1 draws IG/Shorts safe-zone overlay on test frames)"""
import os, sys, json, math, subprocess
import numpy as np, cv2

sys.path.insert(0, "/home/claude/reel-kit/english/scripts")
from plates import *  # noqa: F401,F403
import plates as P

B = "/home/claude/reel-kit/english"
OUT = sys.argv[1]
ONLY = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else None
TL = json.load(open(f"{B}/work/timeline.json"))
EV, LN, END = TL["events"], TL["lines"], TL["END"]
SHOTS = TL["shots"]; SHOT = {s["id"]: s for s in TL["shots"]}
FPS = 30
N = int(round(END * FPS))
E = EV
GUIDES = os.environ.get("GUIDES")


def S(k):
    return SHOT[k]["start"]


def Eend(k):
    return SHOT[k]["end"]


# ---------------- reusable scene pieces ----------------
def xray_page(f, t, pull, glow, w=700, h=730, cy=1092, label_l="R HAND  ·  PA VIEW", label_r="FIG. 1"):
    img, info = xray_hand(w, h, pull=pull, glow=glow)
    x0, y0 = dark_plate_with(f, img, CX, cy, label_l, label_r)
    jx, jy = hand_joint_xy(info, 0, w)
    return x0 + jx, y0 + jy


def crack_curve(t, tc, pre=1.2):
    """pull grows before the crack, snaps at tc; glow flashes after"""
    if t < tc:
        pull = 0.85 * eio((t - (tc - pre)) / pre)
        glow = 0.0
    else:
        q = t - tc
        pull = 0.85 * math.exp(-q / 0.25) + 0.25 * (1 - math.exp(-q / 0.25))
        glow = math.exp(-q / 0.35)
    return pull, glow


DIA = dict(size=760, cx=CX, cy=1000)   # joint diagram placement


def dia_xy(x, y):
    return DIA["cx"] - DIA["size"] / 2 + x, DIA["cy"] - DIA["size"] / 2 + y


def joint_page(f, gap, fluid, cav, cap, bones, plate=True):
    if plate:
        put(f, plate_light(800, 860), CX, DIA["cy"])
    put(f, joint_img(gap=gap, fluid=fluid, cav=cav, cap=cap, bones=bones, size=DIA["size"]), DIA["cx"], DIA["cy"])


def label_below(f, ax, ay, text, prog, y_text=1462, col=INK):
    """vertical leader from an anchor down to a centred label under the plate"""
    if prog <= 0:
        return
    p1 = clamp(prog / 0.6)
    cv2.circle(f, (int(ax), int(ay)), 9, C(col).tolist(), -1, cv2.LINE_AA)
    cv2.circle(f, (int(ax), int(ay)), 15, C(col).tolist(), 2, cv2.LINE_AA)
    yb = ay + (y_text - 30 - ay) * p1
    cv2.line(f, (int(ax), int(ay)), (int(ax), int(yb)), C(col).tolist(), 3, cv2.LINE_AA)
    if prog > 0.5:
        im = text_img(text, MONO, 28, col, 2)
        put(f, im, ax, y_text, op=clamp((prog - 0.5) / 0.5))


# ---------------- shots ----------------
def shot_H1(t, n):
    f = paper(); header(f)
    headline(f, t, -0.3, [[("CRACK YOUR", INK)], [("KNUCKLES", RED), ("?", INK)]], 372, size=124, lead="what really happens when you")
    pull, glow = crack_curve(t, E["t_crack0"], 1.3)
    jx, jy = xray_page(f, t, pull, glow)
    ring_pulse(f, jx, jy, t, E["t_crack0"], rmax=160, dur=0.45)
    return f


def shot_MY(t, n):
    s = S("MY")
    f = paper(); header(f)
    headline(f, t, s + 0.05, [[("BONES ", INK), ("GRINDING", RED), ("?", INK)]], 372, size=118, lead="most people think it's")
    # X-ray close-up of the knuckle with 'grinding' sparks
    img, info = xray_hand(720, 800, pull=0.0, glow=0.0)
    jx, jy = hand_joint_xy(info, 0, 720)
    zoom = 2.3
    M = np.float32([[zoom, 0, 360 - zoom * jx], [0, zoom, 330 - zoom * jy]])
    jit = 5 * math.sin(t * 38) if t < E["t_isnt"] else 0
    M[0, 2] += jit
    crop = cv2.warpAffine(img, M, (720, 660), flags=cv2.INTER_LINEAR)
    x0, y0 = dark_plate_with(f, crop, CX, 1010, "INDEX KNUCKLE  ·  ×2.3", "FIG. 1B")
    if t < E["t_isnt"]:
        rng = np.random.default_rng(int(t * 30))
        for i in range(14):
            a = rng.uniform(0, 2 * math.pi); r = rng.uniform(30, 120)
            px, py = x0 + 360 + math.cos(a) * r, y0 + 330 + math.sin(a) * r * 0.5
            cv2.line(f, (int(px), int(py)), (int(px + math.cos(a) * 16), int(py + math.sin(a) * 16)), (1.0, 0.75, 0.35), 3, cv2.LINE_AA)
    if t > E["t_isnt"] - 0.05:
        k = popk(t, E["t_isnt"] - 0.05, 0.3)
        put(f, stamp("MYTH", RED, 130, -9), CX, 1010, op=clamp(k * 3), sc=1.6 - 0.6 * k)
        # strike through the headline keyword
        q = eo((t - E["t_isnt"]) / 0.25)
        cv2.line(f, (300, 520), (int(300 + 480 * q), 512), C(RED).tolist(), 10, cv2.LINE_AA)
    return f


def shot_JT(t, n):
    s = S("JT")
    f = paper(); header(f)
    fig_label(f, "FIG. 2  —  INSIDE ONE KNUCKLE", 420, op=appear(t, s))
    bones = 0.25 + 0.75 * appear(t, E["t_two"] - 0.2, 0.4)
    cap = eio((t - (E["t_capsule"] - 0.35)) / 0.8)
    joint_page(f, 8, 0.0, 0.0, cap, bones)
    leader(f, *dia_xy(318, 150), 300, 690, "BONE", appear(t, E["t_two"] - 0.1, 0.6), align="l")
    leader(f, *dia_xy(440, 640), 720, 1330, "BONE", appear(t, E["t_bones0"] if False else E["t_two"] + 0.15, 0.6), align="r")
    leader(f, *dia_xy(520, 262), 760, 680, "CAPSULE", appear(t, E["t_capsule"], 0.6), align="r", col=(200, 60, 90))
    return f


def shot_FL(t, n):
    s = S("FL")
    f = paper(); header(f)
    fig_label(f, "FIG. 2  —  INSIDE ONE KNUCKLE", 420)
    fl = eio((t - s) / 0.9)
    joint_page(f, 8, fl, 0.0, 1.0, 1.0)
    # shimmer sweep across the fluid ("slippery")
    if E["t_slippery"] - 0.1 < t < E["t_slippery"] + 0.9:
        q = (t - E["t_slippery"] + 0.1) / 1.0
        x = DIA["cx"] - 220 + 440 * q
        cv2.line(f, (int(x), 905), (int(x + 40), 1080), (1, 1, 1), 10, cv2.LINE_AA)
    label_below(f, *dia_xy(380 - 150, 395), "SYNOVIAL FLUID", appear(t, E["t_synovial"] - 0.1, 0.7), col=(170, 110, 0))
    return f


def gap_at(t):
    return 8 + 40 * eio((t - E["t_pull"]) / (E["t_apart"] + 0.4 - E["t_pull"]))


def shot_PL(t, n):
    s = S("PL")
    f = paper(); header(f)
    fig_label(f, "FIG. 3  —  PULLING THE FINGER", 420)
    g = gap_at(t)
    joint_page(f, g, 1.0, 0.0, 1.0, 1.0)
    k = appear(t, E["t_pull"] - 0.1, 0.4)
    ax, ay = dia_xy(380, 120 - g * 0.5)
    arrow(f, ax, ay, ax, ay - 140, prog=k, col=RED, w=9, head=30)
    bx, by = dia_xy(380, 660)
    arrow(f, bx, by, bx, by + 120, prog=k, col=RED, w=9, head=30)
    if t > E["t_apart"] - 0.3:
        mono(f, "THE BONES MOVE APART", CX, 1462, 28, INK, op=appear(t, E["t_apart"] - 0.3))
    return f


def shot_PR(t, n):
    s = S("PR")
    f = paper(); header(f)
    fig_label(f, "FIG. 3  —  PULLING THE FINGER", 420)
    g = gap_at(t)
    joint_page(f, g, 1.0, 0.0, 1.0, 1.0)
    # inward 'vacuum' arrows around the capsule
    k = appear(t, E["t_pressure"] - 0.1, 0.5)
    cx_, cy_ = dia_xy(380, 470 - 95 - g / 2)
    for i in range(8):
        a = i / 8 * 2 * math.pi + 0.2
        r0, r1 = 270, 215
        pul = 8 * math.sin(t * 6 + i)
        arrow(f, cx_ + math.cos(a) * (r0 + pul), cy_ + math.sin(a) * (r0 + pul) * 0.95, cx_ + math.cos(a) * r1, cy_ + math.sin(a) * r1 * 0.95,
              prog=k, col=BLUE, w=6, head=18)
    gk = appear(t, E["t_pressure"], 0.4)
    if gk > 0:
        put(f, gauge_icon(1.0 - 0.75 * eio((t - E["t_drops"] + 0.4) / 0.6), 210), 812, 640, op=gk)
    if t > E["t_drops"] - 0.2:
        mono(f, "PRESSURE DROPS", CX, 1462, 30, BLUE, op=appear(t, E["t_drops"] - 0.2))
    return f


def shot_CV(t, n):
    s = S("CV")
    f = paper(); header(f)
    fig_label(f, "FIG. 4  —  THE CRACK", 420)
    cav = eback((t - E["t_pocket"] + 0.15) / 0.35) if t > E["t_pocket"] - 0.15 else 0.0
    joint_page(f, 48, 1.0, min(1.05, cav), 1.0, 1.0)
    bx, by = dia_xy(380, (470 - 122 + (470 - 48 - 131)) / 2)
    ring_pulse(f, bx, by, t, E["t_pocket"] - 0.1, rmax=220, dur=0.5, col=BLUE)
    leader(f, bx + 70, by, 720, by - 230, "GAS POCKET", appear(t, E["t_pocket"] + 0.15, 0.6), align="r", col=BLUE, size=26)
    if t > E["t_crack"] - 0.06:
        k = popk(t, E["t_crack"] - 0.06, 0.28)
        put(f, stamp("CRACK!", RED, 120, -6), CX, 1250, op=clamp(k * 3), sc=1.5 - 0.5 * k)
        ring_pulse(f, bx, by, t, E["t_crack"] - 0.04, rmax=300, dur=0.45, col=RED, th=8)
    return f


def shot_MR(t, n):
    s = S("MR")
    f = paper(); header(f)
    headline(f, t, E["t_2015"] - 0.1, [[("FILMED ", INK), ("ON MRI", RED)]], 372, size=118, lead="in 2015, scientists")
    q = (t - (E["t_filmed"] - 0.2)) / 1.6
    g = 8 + 40 * eio(q)
    cav = 1.0 if q > 0.85 else 0.0
    img = cv2.resize(joint_img(gap=g, cav=cav, mode="mri", size=760), (660, 660), interpolation=cv2.INTER_AREA)
    frame_no = max(1, int((t - s) * 8) % 40 + 1)
    x0, y0 = dark_plate_with(f, img, CX, 1030, "REAL-TIME MRI", f"FRAME {frame_no:02d}")
    if cav > 0:
        cyy = y0 + (470 - 122 + 470 - g - 131) / 2 * 660 / 760
        ring_pulse(f, x0 + 330, cyy, t, E["t_filmed"] - 0.2 + 0.85 * 1.6, rmax=160, dur=0.5, col=(255, 255, 255))
        leader(f, x0 + 370, cyy, 790, 640, "CAVITY", appear(t, E["t_filmed"] - 0.2 + 1.45, 0.5), align="r", col=RED, size=24)
    mono(f, "SOURCE: UNIVERSITY OF ALBERTA, PLOS ONE 2015", CX, 1400, 20, GREY, op=appear(t, s + 0.4))
    return f


def shot_WT(t, n):
    s = S("WT")
    f = paper(); header(f)
    headline(f, t, E["t_half"] - 0.15, [[("WAIT ", INK), ("30 MINUTES", RED)]], 372, size=118, lead="before the same knuckle cracks again")
    prog = eio((t - E["t_wait"]) / (E["t_again"] - E["t_wait"] + 0.4))
    put(f, plate_light(860, 640), CX, 1010)
    put(f, clock_icon(prog, 150), 320, 990)
    cav = 1.0 - prog
    put(f, joint_img(gap=48, cav=cav, size=760), 745, 990, sc=400 / 760)
    mono(f, "GAS SLOWLY DISSOLVES", 745, 1240, 22, BLUE, op=appear(t, s + 0.6))
    mono(f, "ABOUT HALF AN HOUR", 320, 1240, 22, RED, op=appear(t, E["t_half"]))
    return f


def shot_QU(t, n):
    s = S("QU")
    f = paper(); header(f)
    headline(f, t, s + 0.05, [[("ARTHRITIS", RED), ("?", INK)]], 400, size=170, lead="so, does it cause")
    img, info = xray_hand(600, 700, pull=0.0)
    x0, y0 = dark_plate_with(f, img, CX, 1090, "R HAND", "FIG. 5")
    for i in range(4):
        jx, jy = hand_joint_xy(info, i, 600)
        k = popk(t, E["t_arthritis"] - 0.2 + i * 0.08, 0.3)
        put(f, text_img("?", ANTON, 70, RED), x0 + jx, y0 + jy - 40, op=clamp(k * 3), sc=0.5 + 0.5 * k)
    return f


def two_hands(f, t, scan=None):
    pw, ph = 380, 540
    out = []
    for i, (cx, mirror, lab, col) in enumerate(((330, True, "LEFT  ·  CRACKED", RED), (750, False, "RIGHT  ·  NEVER", GREY))):
        glow = 0.0
        if mirror and t < S("RS"):
            q = ((t - S("UN")) % 0.9) / 0.9
            glow = math.exp(-q / 0.15) if t > E["t_twice"] - 0.3 else 0.0
        img, info = xray_hand(pw, ph, pull=0.0, glow=glow, mirror=mirror)
        if scan is not None and 0 <= scan <= 1:
            img = img.copy()
            yl = int(scan * ph)
            img[max(0, yl - 4):yl + 4] = np.maximum(img[max(0, yl - 4):yl + 4], np.array([0.3, 1.0, 0.9]))
            img[:yl] = np.minimum(1, img[:yl] * 1.12)
        x0, y0 = dark_plate_with(f, img, cx, 1090, "L" if mirror else "R", "")
        mono(f, lab, cx, 1395, 22, col)
        out.append((x0, y0, info))
    return out


def shot_UN(t, n):
    s = S("UN")
    f = paper(); header(f)
    headline(f, t, s + 0.05, [[("LEFT HAND ", RED), ("ONLY", INK)]], 372, size=118, lead="one doctor cracked his")
    two_hands(f, t)
    if t > E["t_sixty"] - 0.15:
        k = popk(t, E["t_sixty"] - 0.15, 0.3)
        put(f, badge("60+ YEARS", INK, 38, icon="check"), CX, 760, op=clamp(k * 3), sc=0.7 + 0.3 * k)
    return f


def shot_RS(t, n):
    s = S("RS")
    f = paper(); header(f)
    if t < E["t_no"] - 0.1:
        headline(f, t, s - 1, [[("LEFT HAND ", RED), ("ONLY", INK)]], 372, size=118, lead="one doctor cracked his")
    else:
        headline(f, t, E["t_no"] - 0.1, [[("NO ", INK), ("ARTHRITIS", GREEN)]], 372, size=124, lead="his X-rays showed")
    scan = (t - E["t_xrays"] + 0.1) / 1.0
    two_hands(f, t, scan=scan if 0 <= scan <= 1 else None)
    for i, cx in enumerate((330, 750)):
        k = popk(t, E["t_no"] + 0.05 + i * 0.18, 0.3)
        if k > 0:
            put(f, badge("NO ARTHRITIS", GREEN, 30), cx, 1260, op=clamp(k * 3), sc=0.7 + 0.3 * k)
    return f


def shot_NU(t, n):
    s = S("NU")
    f = paper(); header(f)
    headline(f, t, s + 0.05, [[("BUT ONE STUDY ", INK), ("FOUND", RED)]], 372, size=112, lead="a small catch")
    mono(f, "1990 STUDY  ·  300 PEOPLE", CX, 650, 24, GREY, op=appear(t, E["t_study"]))
    for i, (cx, tt) in enumerate(((330, E["t_swelling"]), (750, E["t_grip"]))):
        k = popk(t, s + 0.25 + i * 0.2, 0.35)
        if k <= 0:
            continue
        put(f, plate_light(380, 520), cx, 1010, op=clamp(k * 3), sc=0.85 + 0.15 * k)
        if i == 0:
            sw = eio((t - tt + 0.2) / 0.6)
            put(f, hand_icon(sw, 260), cx, 960, op=clamp(k * 3))
            mono(f, "MORE SWELLING", cx, 1180, 24, RED, op=appear(t, tt - 0.2))
        else:
            v = 0.85 - 0.5 * eio((t - tt + 0.2) / 0.6)
            put(f, gauge_icon(v, 260), cx, 960, op=clamp(k * 3))
            mono(f, "WEAKER GRIP", cx, 1180, 24, RED, op=appear(t, tt - 0.2))
    return f


def shot_TP(t, n):
    s = S("TP")
    f = paper(); header(f)
    k = popk(t, s + 0.1, 0.35)
    put(f, badge("BODY FILES TIP", RED, 30, icon="check"), CX, 640, op=clamp(k * 3))
    put(f, tip_card("Pain or swelling?", "Talk to a doctor.", t > E["t_talk"] - 0.05), CX, 860, op=clamp(k * 3), sc=0.85 + 0.15 * k)
    put(f, hand_icon(0.6 * appear(t, E["t_hurt"] - 0.2, 0.5), 380), CX, 1220, op=appear(t, s + 0.3))
    return f


def shot_LP(t, n):
    s, e = S("LP"), Eend("LP")
    f = paper(); header(f)
    headline(f, t, s + 0.05, [[("CRACK YOUR", INK)], [("KNUCKLES", RED), ("?", INK)]], 372, size=124, lead="now you know what happens when you")
    pull, glow = crack_curve(t, E["t_crack2"], 1.4)
    jx, jy = xray_page(f, t, pull, glow)
    ring_pulse(f, jx, jy, t, E["t_crack2"], rmax=160, dur=0.45)
    return f


RENDER = {k: globals()[f"shot_{k}"] for k in SHOT}


def rs(sid, t, n):
    s = SHOT[sid]
    return RENDER[sid](min(max(t, s["start"]), s["end"] - 1e-3), n)


# ---------------- camera ----------------
PUNCH = [(E["t_crack0"], 0.05, 0.3), (E["t_isnt"], 0.06, 0.3), (E["t_crack"], 0.08, 0.35), (E["t_arthritis"], 0.04, 0.3), (E["t_no"], 0.05, 0.3),
         (E["t_crack2"], 0.05, 0.3), (E["t_pocket"], 0.03, 0.3)]
SHAKE = [(E["t_crack0"], 10, 0.3), (E["t_isnt"], 12, 0.35), (E["t_crack"], 16, 0.4), (E["t_crack2"], 10, 0.3)]


def camera(t):
    z = 1.0
    sh = next((s for s in SHOTS if s["start"] <= t < s["end"]), SHOTS[-1])
    u = (t - sh["start"]) / max(0.5, sh["end"] - sh["start"])
    z += 0.025 * u
    for t0, a, d in PUNCH:
        if t0 - 0.05 <= t < t0 + d * 4:
            q = t - t0
            z += a * (clamp((q + 0.05) / 0.05) if q < 0 else math.exp(-q / d))
    dx = dy = 0.0
    for t0, a, d in SHAKE:
        if t0 <= t < t0 + d:
            q = (t - t0) / d
            amp = a * (1 - q) ** 2
            dx += amp * math.sin(t * 91); dy += amp * math.cos(t * 77 + 1)
    return z, dx, dy


def zoom_frame(f, z, dx=0.0, dy=0.0, cx=W / 2, cy=H / 2):
    if abs(z - 1) < 1e-3 and abs(dx) < 0.3 and abs(dy) < 0.3:
        return f
    M = np.float32([[z, 0, (1 - z) * cx + dx], [0, z, (1 - z) * cy + dy]])
    return cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


# ---------------- transitions ----------------
def slide_trans(A, Bf, q):
    """new page slides up over the old one (paper feel)"""
    e = eio(q)
    off = int(H * (1 - e))
    out = A * (1 - 0.25 * e)
    if off < H:
        out[off:] = Bf[:H - off]
        sh = np.linspace(0.75, 1, min(40, off))[:, None, None] if off > 0 else None
        if sh is not None:
            out[off - len(sh):off] *= sh
    return out


def push_trans(A, Bf, q):
    e = eio(q)
    off = int(W * e)
    out = np.empty_like(A)
    out[:, :W - off] = A[:, off:]
    out[:, W - off:] = Bf[:, :off]
    return out


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; nx = SHOTS[i + 1] if i + 1 < len(SHOTS) else None
    f = None
    for cur, nxt in ((SHOTS[i - 1] if i > 0 else None, sh), (sh, nx)):
        if cur is None or nxt is None or f is not None:
            continue
        b, k = nxt["start"], nxt["trans"]
        if k == "slide" and b - 0.18 <= t < b + 0.18:
            f = slide_trans(rs(cur["id"], t, n), rs(nxt["id"], t, n), (t - b + 0.18) / 0.36)
        elif k == "push" and b - 0.16 <= t < b + 0.16:
            f = push_trans(rs(cur["id"], t, n), rs(nxt["id"], t, n), (t - b + 0.16) / 0.32)
    if f is None:
        f = rs(sh["id"], t, n)
    z, dx, dy = camera(t)
    f = zoom_frame(np.clip(f, 0, 1), z, dx, dy, cy=1000)
    # loop: last 0.3 s dives into the knuckle and flashes white -> matches frame 0
    if t > END - 0.32:
        q = (t - (END - 0.32)) / 0.32
        f = zoom_frame(f, 1 + 1.6 * q * q, cx=500, cy=1010)
        f = f * (1 - q) + q
    if GUIDES:
        f = guides(f)
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)


def main():
    if ONLY:
        os.makedirs(f"{B}/frames", exist_ok=True)
        for n in ONLY:
            cv2.imwrite(f"{B}/frames/r_{n:04d}.jpg", cv2.cvtColor(compose(n), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
        return
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "medium",
                            "-crf", "16", "-profile:v", "high",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                            "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    a, b = int(os.environ.get("SEG_A", 0)), int(os.environ.get("SEG_B", N))
    for n in range(a, min(b, N)):
        enc.stdin.write(compose(n).tobytes())
        if n % 60 == 0:
            print(f"frame {n}/{N}", flush=True)
    enc.stdin.close(); enc.wait()
    print("done", OUT, N)


if __name__ == "__main__":
    main()
