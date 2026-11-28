"""Lab contact sheet for the 28 Nov doodle-kit assets (queue 28 Poppi, 30 Gymshark, 39 Jellycat, 40 Bombas).
Run: python3 studio/lab/visuals/kit_28nov/sheet.py OUT_DIR [t]   -> one 1080x1920 frame per episode set + a small contact sheet."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.join(HERE, "../../../template/scripts/doodlekit.py")
g = {}; exec(open(KIT).read(), g)
skia, np, cv2 = g["skia"], g["np"], g["cv2"]
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/kit28"; T = float(sys.argv[2]) if len(sys.argv) > 2 else 0.6
os.makedirs(OUT, exist_ok=True)


def frame(name, draw):
    surf = skia.Surface(1080, 1920); c = surf.getCanvas(); g["page"](c); g["ground"](c, 1440)
    draw(c, g); g["text"](c, name, 540, 1700, 46, g["INK"], g["MARK_F"])
    img = surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[..., :3]
    cv2.imwrite(f"{OUT}/{name}.png", cv2.cvtColor(img, cv2.COLOR_RGB2BGR)); return img


def poppi(c, d):
    d["market_stall"](c, 540, 1440, 0.95, 3, 1.0, "FARMERS MARKET", d["RED"], T, True, "$3")
    d["char"](c, "sodacan", 300, 1440, 0.8, T, 0.3, mood="happy", arms="wave", label="VINEGAR SODA")
    d["vinegar_bottle"](c, 800, 1440, 0.9, 5)
    d["shark_fin"](c, 540, 640, 0.9, 7, 1.0, T)


def gym(c, d):
    d["garage"](c, 540, 1440, 900, 700, 3, 1.0, 0.8, True, T)
    d["sewing_machine"](c, 330, 1440, 0.62, 4, 1.0, T)
    d["screen_printer"](c, 770, 1440, 0.62, 5, 1.0, 0.6, d["BLU"], "GYM")
    d["pizza_box"](c, 540, 1560, 0.7, 6, 1.0, 0.7)
    d["expo_stand"](c, 540, 420, 0.55, 8, 1.0, "FITNESS EXPO", T)


def jelly(c, d):
    d["toy_shelf"](c, 300, 1440, 0.62, 3, 1.0, 3, 4, T, 0.85)
    d["cloche_plate"](c, 800, 1000, 0.8, 4, 1.0, 0.8, d["FELT"], 1, "$75", T)
    d["char"](c, "fries", 770, 1440, 0.7, T, 0.4, mood="happy", arms="hips")
    d["chip_paper"](c, 560, 640, 0.6, 5)
    d["checkin_desk"](c, 300, 640, 0.6, 6, 1.0, "GATE 1", True, "2.3 KG")
    d["lab_flask"](c, 860, 560, 0.6, 7, 1.0, T, d["GRN"], 0.8)
    d["receipt_printer"](c, 540, 1440, 0.6, 8, 1.0, 0.6, ["DINER", "x1 TOY", "$75.00"], T)


def bombas(c, d):
    for j in range(5): d["shark_chair"](c, 140 + j * 200, 760, 0.6, 3 + j, 1.0, "tick" if j == 4 else "x", 0.0)
    d["char"](c, "sock", 220, 1440, 0.8, T, 0.3, mood="happy", arms="wave")
    d["shelter_list"](c, 820, 1060, 0.7, 5, 1.0)
    d["donate_box"](c, 640, 1440, 0.7, 6, 1.0, socks=0.9)
    d["tm_seal"](c, 900, 1330, 0.6, 7)
    d["popup_table"](c, 540, 400, 0.5, 8, 1.0, "POP-UP", d["YEL"], T)
    d["plush_blob"](c, 120, 1100, 0.5, 9, 1.0, (180, 220, 255), 2, T)


imgs = [frame(n, f) for n, f in (("28-poppi", poppi), ("30-gymshark", gym), ("39-jellycat", jelly), ("40-bombas", bombas))]
sheet = np.concatenate([cv2.resize(i, (540, 960)) for i in imgs], axis=1)
cv2.imwrite(f"{OUT}/sheet.jpg", cv2.cvtColor(sheet, cv2.COLOR_RGB2BGR)); print(OUT)


def states(c, d):
    d["garage"](c, 300, 700, 520, 440, 3, 1.0, 0.0, True, T, True)
    d["pizza_box"](c, 800, 700, 0.8, 6, 1.0, 0.0)
    d["screen_printer"](c, 300, 1100, 0.6, 5, 1.0, 1.0, d["RED"], "GYM")
    d["cloche_plate"](c, 800, 1100, 0.7, 4, 1.0, 0.0)
    d["shark_chair"](c, 200, 1440, 0.6, 3, 1.0, "x", 0.7)
    d["receipt_printer"](c, 540, 1440, 0.5, 8, 1.0, 1.0, ["$200M", "$450M", "PROFIT"], T)
    d["char"](c, "sodacan", 860, 1440, 0.6, T, 0.0, mood="shock", arms="up", label="SODA", col=d["BLU"], fizz=0.0)


imgs.append(frame("states", states))


def extra(c, d):
    d["crates"](c, 300, 1440, 0.8, 3, 1.0, 5, "ORDERS")
    d["stopwatch"](c, 780, 1100, 1.0, 4, 1.0, 0.35, "6 HOURS")
    d["shark_chair"](c, 780, 1440, 0.5, 5, 1.0, "x", 0.45)


imgs.append(frame("extra", extra))
