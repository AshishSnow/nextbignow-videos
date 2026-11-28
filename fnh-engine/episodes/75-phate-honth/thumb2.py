import os, sys
os.environ['V'] = 'final'; sys.argv = ['comic.py']
import importlib.util
spec = importlib.util.spec_from_file_location('cm', 'comic.py'); cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
from PIL import Image
import numpy as np
cm.CUR[0] = 0.0; cm.MODE[0] = 'cream'
fr = np.zeros((cm.H, cm.W, 3), np.uint8)
cm.overlay(fr, cm.cairo_layer(lambda c: cm.world(c, 3.0, 1750, 1.0, 0, None, 1.0, 1.0, 1.0, 0, 0, 0, 0)))
cm._put0(fr, cm.LIPS, cm.CX, 1060, 1.12, 1.0, -4)
cm.overlay(fr, cm.cairo_layer(lambda c: (cm.tongue(c, 430, 1020, 1.8), cm.balm_guy(c, 900, 1330, 1.05, 0.4, 'evil'), cm.sparks(c, 160, 830, 1.0))))
cm.title_line(fr, [('फटे होंठ?', 3)], 330, 2.0, 140)
cm.title_line(fr, [('होंठ चाटना बंद करो', 0)], 545, 2.0, 104)
cm.overlay(fr, cm.BADGE)
Image.fromarray(fr).save('/home/claude/outputs/75-phate-honth_thumb2.jpg', quality=92)
print('ok')
