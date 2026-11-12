# lab sheet for the 12 Nov overbooking props: python3 studio/lab/story_kit/props_12nov.py OUT.jpg
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "template", "scripts"))
import skia
from nbnkit.board import *
surf = skia.Surface(W, H); c = surf.getCanvas(); board_bg(c, 2.0) if board_bg.__code__.co_argcount <= 2 else board_bg(c, 2.0, 0)
t = 3.0
plane_m(c, 470, 520, t, 0, s=1.0, n=10, filled=9, extra=2, label="TICKETS 110 · SEATS 100")
boardpass_m(c, 540, 1000, t, 0, s=1.0, seat="12C", stamp="BUMPED", stamp_t=1.0)
gatedesk_m(c, 600, 1650, t, 0, s=1.0, bubble="VOLUNTEERS?", bubble_t=1.0)
img = surf.makeImageSnapshot(); img.save(sys.argv[1] if len(sys.argv) > 1 else "props_12nov.jpg", skia.kJPEG)
