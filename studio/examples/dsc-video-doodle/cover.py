"""Render the post COVER image (grid thumbnail) = the hook frame with the big title card. Usage: python3 scripts/cover.py OUT.jpg [seconds=1.0]
The same title is on frame 0 of the video, so Instagram's default cover also shows it; pass the hosted JPG as videoThumbnailUrl."""
import sys, os
_D = os.path.dirname(os.path.abspath(__file__))
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read())
t = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
cv2.imwrite(sys.argv[1], cv2.cvtColor(compose(int(t * FPS)), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
print("cover", sys.argv[1])
