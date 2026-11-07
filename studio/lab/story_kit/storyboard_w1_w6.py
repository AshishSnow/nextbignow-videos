"""Lab sheet for the 7 Nov 2026 board props (queue/15-same-cart + queue/16-prime-iliad): renders 8 storyboard frames with the new
nbnkit/board.py drawings (tag_m, carton_m, phone_m, cart_m, coin_m, cursor_m, button_m, door_m, maze_m, helmet_m) mid-draw and finished.
Run: python3 studio/lab/story_kit/storyboard_w1_w6.py  → $STUDIO/projects/lab_20261107/storyboard_w1_w6.jpg (not committed)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "..", "template", "scripts"))
import skia
from nbnkit.board import *   # noqa
OUT = os.path.join(os.environ.get("STUDIO", "/home/claude/studio"), "projects", "lab_20261107"); os.makedirs(OUT, exist_ok=True)


def frame(fn, t):
    surf = skia.Surface(W, H); c = surf.getCanvas(); board_bg(c, t); fn(c, t)
    pill(c, "OOPSMYBUSINESS · HOW IT WORKS")
    return surf.makeImageSnapshot().toarray()[:, :, 2::-1]   # skia N32 = BGRA


def f1(c, t):   # same-cart row 1: carton + five tags
    carton_m(c, 540, 1180, t, 0.0)
    for i, p in enumerate(["$3.99", "$4.28", "$4.59", "$4.69", "$4.79"]):
        tag_m(c, 200 + i * 170, 900 - 60 * (i % 2), p, t, 0.6 + i * 0.3, tilt=-14 + i * 7, s=0.62, hot=(i == 4))
    say(c, t, 0.2, "same eggs, same store", "5 PRICES", under=RD)


def f2(c, t):   # row 3: two phones
    scr = lambda col, p: (lambda cc, x, y, w, h: (carton_m(cc, x, y + 60, 9, 0, s=0.5), tag_m(cc, x, y - 120, p, 9, 0, col=col, s=0.7)))
    phone_m(c, 300, 1050, t, 0.0, s=0.95, screen=scr(BLU, "$3.99")); phone_m(c, 780, 1050, t, 0.3, s=0.95, screen=scr(RD, "$4.79"))
    say(c, t, 0.1, "same carton", "$3.99 vs $4.79")


def f3(c, t):   # row 8: carts + coin
    cart_m(c, 300, 1250, t, 0.0, s=0.8, items=1.0); cart_m(c, 780, 1250, t, 0.2, s=0.8, items=1.0)
    coin_m(c, 540, 1000, t, 0.6); say(c, t, 0.1, "whole baskets", "~7% APART")


def f4(c, t):   # row 17: phone + cursor + browser
    phone_m(c, 540, 1100, t, 0.0, s=1.1); cursor_m(c, 700, 1180, t, 0.5); browser_m(c, 300, 880, t, 0.3, url="any-shop.example", title="", w=480, h=300)
    say(c, t, 0.1, "they can use", "YOUR MOUSE")


def f5(c, t):   # prime row 2: helmet + scroll
    scroll_m(c, 380, 1080, 480, 420, t, 0.0, ["ILIAD"], [0.6], size=90); helmet_m(c, 820, 1150, t, 0.4)
    say(c, t, 0.1, "like Homer's", "ILIAD")


def f6(c, t):   # row 4: two doors
    door_m(c, 300, 1400, t, 0.0, label="IN"); door_m(c, 780, 1400, t, 0.3, label="OUT", open_=0.6, col=RD)
    say(c, t, 0.1, "settling cost Amazon", "$2.5 BILLION")


def f7(c, t):   # row 6/7: button + small link
    button_m(c, 540, 1050, "JOIN PRIME", t, 0.0); button_m(c, 540, 1230, "No, I don't want Free Shipping", t, 0.6, small=True)
    say(c, t, 0.1, "to skip it", "NO FREE SHIPPING?")


def f8(c, t):   # row 9: maze solved
    maze_m(c, 540, 1180, t, 0.0, size=600, solve_t=1.4); say(c, t, 0.1, "door two", "LABYRINTHINE")


if __name__ == "__main__":
    import numpy as np
    from PIL import Image
    fr = [f1, f2, f3, f4, f5, f6, f7, f8]
    cells = [frame(f, tm) for f in fr for tm in (0.7, 4.0)]
    small = [Image.fromarray(a).resize((270, 480)) for a in cells]
    sheet = Image.new("RGB", (270 * 8, 480 * 2), "white")
    for i, im in enumerate(small): sheet.paste(im, ((i // 2) * 270, (i % 2) * 480))
    sheet.save(os.path.join(OUT, "storyboard_w1_w6.jpg"), quality=88)
    Image.fromarray(cells[1]).save(os.path.join(OUT, "f1_done.png")); Image.fromarray(cells[13]).save(os.path.join(OUT, "f7_done.png"))
    Image.fromarray(cells[15]).save(os.path.join(OUT, "f8_done.png")); Image.fromarray(cells[9]).save(os.path.join(OUT, "f5_done.png"))
    print("ok", OUT)
