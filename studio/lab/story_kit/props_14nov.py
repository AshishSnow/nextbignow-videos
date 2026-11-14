# lab sheet for the 14 Nov writers'-room props (24 ZIP code, 25 Domino's): python3 studio/lab/story_kit/props_14nov.py OUT.jpg
import sys, os
os.environ.setdefault("BOIL", "0")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "template", "scripts"))
import skia
from nbnkit.board import *
surf = skia.Surface(W, H); c = surf.getCanvas(); board_bg(c, 2.0) if board_bg.__code__.co_argcount <= 2 else board_bg(c, 2.0, 0)
t = 4.0
pizza_m(c, 300, 620, t, 0, s=0.9, open_=1.0, sad=True, lid_text="CARDBOARD?")
pizza_m(c, 790, 620, t, 0, s=0.9, open_=1.0, garlic=True, lid_text="NEW RECIPE")
ketchup_m(c, 540, 980, t, 0, s=1.0)
zippad_m(c, 300, 1250, t, 0, digits="90210", hot=3.0)
house_m(c, 870, 1200, 1.0, t, 0)
road_m(c, (420, 1150), (800, 1180), t, 0)
gaspump_m(c, 540, 1800, t, 0, s=1.0)
img = surf.makeImageSnapshot(); img.save(sys.argv[1] if len(sys.argv) > 1 else "props_14nov.jpg", skia.kJPEG)
