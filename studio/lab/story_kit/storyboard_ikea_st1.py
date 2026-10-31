# Story-kit 2 demo (R&D Visuals run, 31 Oct 2026): renders 12 storyboard frames of SPOT THE TRICK #1 (episodes/queue/03-ikea-maze)
# with the template scripts + anim_story2.py, each with the PLAYBOOK §6 safe-zone guides (red = UI zones) on a second copy.
# Usage: python3 storyboard_ikea_st1.py <out_dir>   (makes its own fake align.json; no audio, no project needed)
import os, sys, math, json
TPL_ = "/home/claude/nextbignow-videos/studio/template/scripts"
OUT = sys.argv[1]; os.makedirs(f"{OUT}/work", exist_ok=True)
if not os.path.exists(f"{OUT}/work/align.json"):
    json.dump(dict(lines={"i1": dict(start=0.0, end=3.0)}, words=[dict(line="i1", w="why", t=0.3)], dur=4.0, LEAD=0.0, fake=True), open(f"{OUT}/work/align.json", "w"))
if not os.path.exists(f"{OUT}/work/vo.wav"):
    import numpy as _np, soundfile as _sf; _sf.write(f"{OUT}/work/vo.wav", 0.02 * _np.sin(_np.arange(48000 * 4) * 0.05).astype(_np.float32), 48000)
os.environ["PROJ"] = OUT
for _p in ("anim_base.py", "anim_cine.py", "anim_mascot3d.py", "anim_sets.py", "anim_props.py", "anim_props2.py", "anim_props3.py", "anim_story.py", "anim_story2.py"):
    exec(open(f"{TPL_}/{_p}").read())
import time
out, names, costs = [], [], []
def fin(f, n, name):
    costs.append(time.time() - T0[0]); out.append(cine_grade(f, n)); names.append(name)
T0 = [time.time()]
def start(): T0[0] = time.time()

# i1 — frame 1: maze_store WIDE, hero mid-path on a grey arrow, looking back; EXIT far behind him
start(); f = set_view("maze_store", 0.0)
person(f, 540, 1760, 1.05, "hero", la=(20, 10), ra=(60, 30), expr="sus", brow="sus", look=(-1, -1), face_dir=-1)
series_badge(f, "SPOT THE TRICK", "#1 · THE FLAT-PACK MAZE")
say(f, "WHY HIDE THE EXIT?", y=1010, size=140)
fin(f, 1, "i1 frame 1")
# i2 — store entrance MEDIUM: turnstile + wire baskets, cold open card, the list
start(); f = set_view("store", 0.5, zoom=1.2, cx=540, cy=1100, blur=2.0)
comp(f, turnstile_el(520), 300, 1380)
for i in range(3): comp(f, basket_el(300), 860, 1480 - i * 26)
person(f, 600, 1860, 1.3, "hero", la=(30, 60), ra=(40, 80), mouth=1, brow="up", hold=list_el("LAMP", 200), hold_off=(0, -10))
cold_open(f, "TODAY", "THE FLAT-PACK STORE", "YOU: SHOPPER, $20")
say(f, "$20 · ONE LAMP", y=760)
fin(f, 2, "i2 entrance")
# i3 — roadmap: four numcards over the cash desk
start(); f = set_view("store", 1.0, zoom=1.1, cx=540, cy=900, blur=4)
for i, (lab, c) in enumerate((("PATH", (40, 110, 220)), ("BINS", (226, 120, 40)), ("FOOD", (200, 50, 60)), ("SHELF", (40, 150, 90)))):
    comp(f, numcard_el(i + 1, lab, c, 230), 200 + i * 226, 1120)
say(f, "€44.6 BILLION", y=760, size=140); say(f, "A YEAR", y=900, size=110)
comp(f, chip("Source: Inter IKEA, FY25 (Oct 2025)", INK, WHITE, 24), 540, 1430)
fin(f, 3, "i3 roadmap")
# a2 — maze_store MEDIUM: hero walks forward on an arrow, the EXIT sign slides away behind
start(); f = set_view("maze_store", 1.5, zoom=1.25, cx=540, cy=1150, blur=2.0)
arrow_floor(f, 540, 1700, 1.8, 90, (150, 152, 158), 0.85)
comp(f, exit_sign_el(200, mirror=True), 540, 640)
person(f, 540, 1880, 1.35, "hero", la=(40, 90), ra=(20, 10), ll=10, rl=4, expr="n", brow="up", look=(-1, 0))
say(f, "EXIT: BEHIND YOU", y=840)
fin(f, 4, "a2 exit behind")
# a5 — staff opens the shortcut door in the maze wall
start(); f = set_view("maze_store", 2.0, zoom=1.15, cx=640, cy=1050, blur=1.5)
comp(f, shortcut_door_el(0.75, 260, 460), 780, 900)
person(f, 760, 1700, 1.0, {"base": "worker", "top": (150, 152, 156), "trim": (150, 152, 156), "pants": (60, 62, 70), "hair": "slick", "cap": None}, la=(90, 120), ra=(20, 10), mouth=1, brow="up")
person(f, 330, 1760, 1.1, "hero", la=(20, 10), ra=(70, 90), expr="wow", look=(1, 0))
say(f, "BEAT IT:", y=1180, size=120, col=(120, 240, 150)); say(f, "ASK FOR THE SHORTCUT", y=1310, size=120, col=(120, 240, 150))
fin(f, 5, "a5 shortcut door")
# b1 — market_hall WIDE: three giant bins, hero small
start(); f = set_view("market_hall", 0.0)
for (x, y, s, it) in ((230, 1500, 0.9, "cushions"), (560, 1560, 1.05, "candles"), (880, 1500, 0.9, "plants")):
    comp(f, bin_el(it, 620), x, y, scale=s)
person(f, 400, 1860, 0.9, "hero", la=(20, 10), ra=(40, 20), expr="wow", look=(1, -1))
comp(f, chip("TRICK #2 · THE BINS", (228, 34, 42), WHITE, 34), 540, 560)
fin(f, 6, "b1 the bins")
# b2 — bin CU: hundreds of candles, a worker whispers "bulla bulla"
start(); f = set_view("market_hall", 0.6, zoom=1.5, cx=540, cy=1200, blur=5)
comp(f, bin_el("candles", 900), 540, 1500)
person_head_at(f, 860, 820, 1.6, {"base": "worker", "top": (150, 152, 156), "trim": (150, 152, 156), "hair": "slick", "cap": None}, mouth=1, brow="up", look=(-1, 0), ra=(120, 150))
say(f, "BULLA BULLA", y=560, size=160)
comp(f, chip("The New Yorker, Oct 2011", INK, WHITE, 24), 540, 1430)
fin(f, 7, "b2 bulla bulla")
# c1 — store_cafe WIDE: queue, trays, menu board; hero rubs his stomach
start(); f = set_view("store_cafe", 0.0)
person(f, 300, 1250, 0.6, "friend", look=(1, 0)); person(f, 420, 1250, 0.6, "lady", look=(1, 0))
person(f, 760, 1820, 1.1, "hero", la=(60, 80), ra=(40, 20), expr="sad", brow="sad", sweat=True, hold=tray_el(300), hold_off=(0, 20))
comp(f, chip("TRICK #3 · THE FOOD", (228, 34, 42), WHITE, 34), 540, 560)
fin(f, 8, "c1 the food")
# c2 — counter CU: hot dog with a $1 tag
start(); f = set_view("store_cafe", 0.4, zoom=1.6, cx=540, cy=900, blur=5)
comp(f, hotdog_el(), 540, 1180, scale=1.1)
comp(f, tag_el("$1", (228, 34, 42), WHITE, 84), 820, 1020)
person_head_at(f, 230, 1500, 1.8, "hero", expr="wow", sweat=True, look=(1, -1))
say(f, "$1 HOT DOG", y=700, size=160)
fin(f, 9, "c2 hot dog")
# c4 — hero with a tray walks back onto the grey arrow
start(); f = set_view("maze_store", 2.0, zoom=1.2, cx=540, cy=1150, blur=1.5)
arrow_floor(f, 540, 1760, 1.6, 90, (150, 152, 158), 0.85)
person(f, 540, 1880, 1.3, "hero", la=(60, 80), ra=(60, 80), expr="n", mouth=1, brow="up", hold=tray_el(360), hold_off=(0, 40))
say(f, "€2 BILLION+ ON FOOD", y=800, size=130)
fin(f, 10, "c4 tray walk")
# d2 — study: flat box -> wobbly shelf, heart pops
start(); f = set_view("study", 0.0, zoom=1.1, cx=540, cy=1100, blur=1.0)
comp(f, flatpack_el(0.0, 520), 250, 1640, scale=0.8)
comp(f, flatpack_el(1.0, 520), 760, 1560)
comp(f, heart_el(150), 760, 1180)
person(f, 420, 1860, 1.2, "hero", la=(80, 100), ra=(80, 100), expr="wow", look=(1, 0))
say(f, "YOU LOVE IT ANYWAY", y=820, size=130)
fin(f, 11, "d2 flat-pack")
# e1 — end card: hero centre on the frame-1 path, four trick chips, choice card
start(); f = set_view("maze_store", 3.0, zoom=1.05, cx=540, cy=1000, blur=2.5)
person(f, 540, 1700, 1.0, "hero", la=(30, 40), ra=(30, 40), mouth=1, brow="up")
for i, (lab, x, y) in enumerate((("#1 PATH", 240, 700), ("#2 BINS", 840, 700), ("#3 FOOD", 240, 1200), ("#4 SHELF", 840, 1200))):
    comp(f, chip(lab, (228, 34, 42), WHITE, 32), x, y)
choice_card(f, "WHICH TRICK GOT YOU?", "MAZE · BINS", "FOOD · SHELF", y=1410)
series_badge(f, "SPOT THE TRICK", "#1 · THE FLAT-PACK MAZE")
fin(f, 12, "e1 end card")

# write frames + a guided contact sheet (red = UI zones from PLAYBOOK §6: top 250, bottom 420, left 60, right 120)
def guides(img):
    g = img.copy(); ov = g.copy()
    cv2.rectangle(ov, (0, 0), (W, 250), (255, 40, 40), -1); cv2.rectangle(ov, (0, H - 420), (W, H), (255, 40, 40), -1)
    cv2.rectangle(ov, (0, 0), (60, H), (255, 40, 40), -1); cv2.rectangle(ov, (W - 120, 0), (W, H), (255, 40, 40), -1)
    return cv2.addWeighted(ov, 0.22, g, 0.78, 0)
ims = []
for i, (x, nm) in enumerate(zip(out, names)):
    im8 = (np.clip(x, 0, 1) * 255).astype(np.uint8)
    cv2.imwrite(f"{OUT}/sb_{i+1:02d}.jpg", cv2.cvtColor(im8, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
    g = guides(im8); cv2.putText(g, nm, (70, 1480), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (255, 255, 255), 4, cv2.LINE_AA)
    ims.append(cv2.resize(g, (360, 640), interpolation=cv2.INTER_AREA))
gap = np.full((640, 8, 3), 255, np.uint8); rows = []
for r in range(0, len(ims), 6):
    row = [ims[r]]
    for im in ims[r + 1:r + 6]: row += [gap, im]
    while len(row) < 11: row += [gap, np.full((640, 360, 3), 255, np.uint8)]
    rows.append(np.hstack(row))
sheet = np.vstack([rows[0], np.full((8, rows[0].shape[1], 3), 255, np.uint8), rows[1]]) if len(rows) > 1 else rows[0]
cv2.imwrite(f"{OUT}/storyboard_ikea.jpg", cv2.cvtColor(sheet, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 88])
print("ok", len(out), "frames; draw cost per frame (s, before grade):", " ".join(f"{c:.2f}" for c in costs))
