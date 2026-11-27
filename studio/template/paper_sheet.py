"""paper_sheet.py <proj dir> <module> <out.png> — one still per scene (late in each scene) with IG safe-zone guides."""
import sys, os, importlib
d, m, out = sys.argv[1:4]; sys.path.insert(0, d); sys.path.insert(0, '/home/claude/studio'); os.chdir(d)
R = importlib.import_module(m.replace('.py', '')); from PIL import Image, ImageDraw
import numpy as np
st = R.S.starts + [R.S.END]; ims = []
for i in range(len(R.S.SC)):
    t = st[i] + 0.8 * (st[i + 1] - st[i]); s = R.S.frame(t)
    a = np.asarray(s.makeImageSnapshot().toarray())[..., :3]
    im = Image.fromarray(np.ascontiguousarray(a[..., ::-1])).resize((270, 480))
    dr = ImageDraw.Draw(im); dr.rectangle([0, 0, 269, 62], outline=(255, 0, 0)); dr.rectangle([0, 480 - 105, 269, 479], outline=(255, 0, 0)); dr.line([240, 0, 240, 479], fill=(255, 0, 0))
    dr.text((4, 66), f'{i} {t:.1f}s', fill=(255, 255, 0)); ims.append(im)
cols = 7; rows = (len(ims) + cols - 1) // cols; sheet = Image.new('RGB', (cols * 270, rows * 480))
for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 270, (k // cols) * 480))
sheet.save(out); print(out)
