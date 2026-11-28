import os, sys
os.environ['V'] = 'final'
sys.argv = ['comic.py']
import importlib.util
spec = importlib.util.spec_from_file_location('cm', 'comic.py'); cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
from PIL import Image
import numpy as np
cm.CUR[0] = 0.0; cm.LT[0] = 2.0; cm.LT[1] = 's1'
fr = np.zeros((cm.H, cm.W, 3), np.uint8)
cm.ebg(fr, 'black', 0)
cm._put0(fr, cm.LIPS, cm.CX, 1080, 1.15, 1.0, -3)
cm.overlay(fr, cm.cairo_layer(lambda c: (cm.tongue(c, 470, 1040, 1.9), cm.balm_guy(c, 880, 1330, 1.0, 0.4, 'evil'))))
cm.title_line(fr, [('होंठ ', 0), ('चाटते', 1), (' हो?', 0)], 360, 2.0, 132)
cm.title_line(fr, [('यहीं गलती है', 3)], 560, 2.0, 132)
cm.overlay(fr, cm.BADGE)
Image.fromarray(fr).save('/home/claude/outputs/75-phate-honth_thumb.jpg', quality=92)
print('ok')
