import os, sys
os.environ['V'] = 'final'; sys.argv = ['comic.py']
import importlib.util
spec = importlib.util.spec_from_file_location('cm', 'comic.py'); cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
from PIL import Image
import numpy as np
cm.CUR[0] = 0.0; cm.LT[1] = 'h1'
fr = np.zeros((cm.H, cm.W, 3), np.uint8)
cm.ebg(fr, 'black', 0)
cm._put0(fr, cm.wanted_poster(), 640, 1110, .78, 1.0, 5)
cm._put0(fr, cm.CHAPPAL, 640, 1120, .85, 1.0, 10)
cm.stamp(fr, 'पकड़ा गया', 700, 1320, 1.0, cm.REDP, -14)
cm._put0(fr, cm.SCRUB, 290, 1260, .5, 1.0, -8)
cm.title_line(fr, [('एड़ी फटी?', 3)], 330, 2.0, 140)
cm.title_line(fr, [('गुनहगार: चप्पल', 0)], 535, 2.0, 112)
cm.overlay(fr, cm.BADGE)
Image.fromarray(fr).save('/home/claude/outputs/76-phati-ediyan_thumb.jpg', quality=92)
print('ok')
