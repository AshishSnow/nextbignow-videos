"""Chubby pose + SILHOUETTE sheet (ep 17 staging skill): 8 acting poses drawn normally (top row) and as flat ink silhouettes (bottom row).
Usage: python3 engine/tools/ink_sheet.py <project_dir> OUT.jpg   -> a pose reads only if its black shape reads (arms clear of the body, asymmetry, a lean)."""
import sys, os
B = sys.argv[1]; os.environ["PROJ"] = B; D = f"{B}/scripts"
for p in ("anim_base.py", "anim_props.py", "anim_props2.py", "anim_props3.py", "anim_props4.py", "fnh_char.py", "fnh_char3d.py", "fnh_char_v3.py", "fnh_char_ink.py", "anim_fx.py", "anim_cine.py", "anim_props5.py"):
    if os.path.exists(f"{D}/{p}"): exec(open(f"{D}/{p}").read())
POSES = [dict(la=(20, 10), ra=(20, 10), expr="n", brow="n", mouth=0, name="idle"),
         dict(la=(150, 170), ra=(150, 170), expr="happy", brow="up", mouth=3, name="cheer"),
         dict(la=(20, 10), ra=(70, 40), expr="n", brow="up", mouth=1, look=(1, 0), name="point"),
         dict(la=(-150, -150), ra=(20, 10), expr="sus", brow="sus", mouth=0, lean=-6, name="scratch"),
         dict(la=(110, 160), ra=(110, 160), expr="wow", brow="up", mouth="o", lean=8, name="shock"),
         dict(la=(148, -130), ra=(20, 10), expr="sad", brow="sad", mouth=0, look=(-1, 1), name="hand-to-mouth"),
         dict(la=(40, 30), ra=(150, 175), expr="smirk", brow="n", mouth=0, look=(1, -0.3), lean=5, name="hold-up"),
         dict(la=(20, 10), ra=(20, 10), expr="sleepy", brow="sad", mouth=0, lean=-4, name="tired")]
out = np.ones((960, 8 * 380, 3), np.float32) * np.array(C(PAPER), np.float32)
for i, P in enumerate(POSES):
    name = P.pop("name"); x0 = i * 380
    f = np.ones((H, W, 3), np.float32) * np.array(C(PAPER), np.float32)
    chub(f, 540, 1300, 1.2, t=0.3, **P)
    crop = f[560:1380, 180:900]; out[20:20 + 410, x0 + 10:x0 + 10 + 360] = cv2.resize(crop, (360, 410))
    g = np.ones((H, W, 3), np.float32)
    chub(g, 540, 1300, 1.2, t=0.3, shadow=False, **P)
    sil = (np.abs(g - 1).sum(2) > 0.08).astype(np.float32)
    s = np.ones((H, W, 3), np.float32) * np.array(C(PAPER), np.float32); s[sil > 0] = np.array(C(INKC), np.float32)
    crop = s[560:1380, 180:900]; out[460:460 + 410, x0 + 10:x0 + 10 + 360] = cv2.resize(crop, (360, 410))
    comp(out, chip(name, INKC, WHITE, 26), x0 + 180, 900)
cv2.imwrite(sys.argv[2], cv2.cvtColor((np.clip(out, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("ok")
