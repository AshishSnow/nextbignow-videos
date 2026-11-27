"""wide_sheet.py <proj> <module> <out.png> — one still per scene for 16:9 long videos"""
import sys, os, importlib
os.environ['OMB_WIDE'] = '1'
d, m, out = sys.argv[1:4]; sys.path.insert(0, d); sys.path.insert(0, '/home/claude/studio'); os.chdir(d)
R = importlib.import_module(m.replace('.py', '')); from PIL import Image, ImageDraw
import numpy as np
st = R.S.starts + [R.S.END]; ims = []
for i in range(len(R.S.SC)):
    t = st[i] + 0.85 * (st[i + 1] - st[i]); s = R.S.frame(t)
    a = np.asarray(s.makeImageSnapshot().toarray())[..., :3]
    im = Image.fromarray(np.ascontiguousarray(a[..., ::-1])).resize((480, 270)); ImageDraw.Draw(im).text((4, 4), f'{i} {t:.1f}s', fill=(255, 255, 0)); ims.append(im)
cols = 4; rows = (len(ims) + cols - 1) // cols; sheet = Image.new('RGB', (cols * 480, rows * 270))
for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 480, (k // cols) * 270))
sheet.save(out); print(out, len(ims))
