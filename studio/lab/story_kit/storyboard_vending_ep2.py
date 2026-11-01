# Vending kit demo (R&D run, 1 Nov 2026): renders 5 storyboard frames of HOW TO START EP 2 (episodes/queue/05-vending-machines)
# + the 1950 variant for the nickel-Coke board, each also with the PLAYBOOK §6 safe-zone guides. Usage: python3 storyboard_vending_ep2.py <out_dir>
import os, sys, json, time
TPL_ = "/home/claude/nextbignow-videos/studio/template/scripts"
OUT = sys.argv[1]; os.makedirs(f"{OUT}/work", exist_ok=True)
if not os.path.exists(f"{OUT}/work/align.json"):
    json.dump(dict(lines={"i1": dict(start=0.0, end=3.0)}, words=[dict(line="i1", w="before", t=0.3)], dur=4.0, LEAD=0.0, fake=True), open(f"{OUT}/work/align.json", "w"))
if not os.path.exists(f"{OUT}/work/vo.wav"):
    import numpy as _np, soundfile as _sf; _sf.write(f"{OUT}/work/vo.wav", 0.02 * _np.sin(_np.arange(48000 * 4) * 0.05).astype(_np.float32), 48000)
os.environ["PROJ"] = OUT
for _p in ("anim_base.py", "anim_cine.py", "anim_mascot3d.py", "anim_stick.py", "anim_sets.py", "anim_props.py", "anim_props2.py", "anim_props3.py", "anim_story.py", "anim_story2.py", "anim_props4.py"):
    exec(open(f"{TPL_}/{_p}").read())
out, names, costs = [], [], []
T0 = [time.time()]
def start(): T0[0] = time.time()
def fin(f, n, name): costs.append(time.time() - T0[0]); out.append(cine_grade(f, n)); names.append(name)
SELLER = {"base": "exec", "col": (150, 152, 160)}

# i1 — frame 1
start(); f = set_view("store", 0.0)
comp(f, vending_el(640), 540, 1300)
person(f, 300, 1840, 1.0, "hero", la=(20, 10), ra=(60, 30), expr="sus", brow="sus", look=(1, -1))
person(f, 820, 1840, 0.95, SELLER, la=(30, 60), ra=(80, 90), mouth=2, hold=phone_el(), hold_off=(0, -10))
cold_open(f, "US", "VENDING MACHINES", "YOU: FIRST-TIME BUYER")
say(f, "A SINGER?", y=1000, size=150)
fin(f, 1, "i1 frame 1")
# a2 — dead hallway
start(); f = set_view("office", 0.4, zoom=1.1)
comp(f, vending_el(520, fill=1.0, glow=0.5), 700, 1350)
person(f, 330, 1840, 1.0, "hero", la=(20, 40), ra=(40, 80), brow="up")
say(f, "COUNT PEOPLE", y=760)
fin(f, 2, "a2 dead hallway")
# c3 — CU panel, bills broken
start(); f = set_view("street", 1.0, zoom=1.4, blur=4)
comp(f, vending_el(820, broken="bills"), 540, 1150)
hud_rule(f, 3, "TEST BEFORE YOU PAY")
fin(f, 3, "c3 test panel")
# a2b — empty machine (fill 0.2) for the 'sells nothing' beat
start(); f = set_view("airport", 0.6)
comp(f, vending_el(560, fill=0.2), 760, 1330)
person(f, 360, 1840, 1.0, "girl2", la=(30, 70), ra=(60, 30), mouth=2)
fin(f, 4, "fill 0.2 airport")
# nickel-Coke variant (04 board BUILD BRIEF)
start(); f = set_view("store", 0.2)
comp(f, vending_el(560, era="1950"), 540, 1300)
person(f, 820, 1840, 1.0, {"base": "hero", "outfit": "suit"}, la=(20, 40), ra=(40, 80), brow="sus")
fin(f, 5, "1950 cooler (nickel Coke)")

import numpy as np, cv2
def guides(img):
    g = img.copy(); H_, W_ = g.shape[:2]
    for (x0, y0, x1, y1) in ((0, 0, W_, 220), (0, H_ - 420, W_, H_), (W_ - 140, 0, W_, H_)):
        sub = g[y0:y1, x0:x1].astype(np.float32); g[y0:y1, x0:x1] = (sub * 0.6 + np.array([0, 0, 255]) * 0.4).astype(np.uint8)
    return g
tiles = []
for img in out:
    a = (np.clip(img, 0, 1) * 255).astype(np.uint8)[..., ::-1] if img.dtype != np.uint8 else img[..., ::-1]
    tiles.append(np.hstack([cv2.resize(a, (360, 640)), cv2.resize(guides(a), (360, 640))]))
sheet = np.vstack([np.hstack(tiles[i:i + 2]) if i + 1 < len(tiles) else np.hstack([tiles[i], np.zeros_like(tiles[i])]) for i in range(0, len(tiles), 2)])
cv2.imwrite(f"{OUT}/storyboard_vending_ep2.jpg", sheet, [cv2.IMWRITE_JPEG_QUALITY, 80])
print("frames", names, "s/frame", [round(c, 2) for c in costs])
