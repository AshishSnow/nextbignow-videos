"""YouTube thumbnail 1280x720 for the bus-economics long-form (vintage comic)."""
import os
os.environ['NBN_ORIENT'] = 'land'
import sys
sys.argv = [sys.argv[0]]
import skia, cv2, numpy as np
import render_be as RB
from render_be import *

S_ = skia.Surface(W, H); c = S_.getCanvas()
bg_flat(c, NAVY, (40, 60, 130))
photo(c, 'night', 1000, 80, 860, 520, 2, 1.0, 0, cred=False)
coach(c, 820, 1010, 1.25, 1.0, CBLU, 0, '', lights=True, rot=-2)
title(c, '$500,000 BUS.', 70, 260, 150, CYEL, 1.0, rot=-2)
title(c, 'WHO PROFITS?', 70, 450, 170, CRED, 1.0, rot=-1)
burst(c, 1690, 760, 190, '~5%', 1.0, size=110, col=CYEL, txt=CRED, rot=8)
caption(c, 'BUS BUSINESS . USA + EUROPE', 80, 520, 1.0, col=PAPER, size=40)
im = S_.makeImageSnapshot().toarray()[..., :3]
im = cv2.cvtColor(np.ascontiguousarray(im), cv2.COLOR_RGB2BGR) if False else np.ascontiguousarray(im)
cv2.imwrite(os.path.join(RB.D, 'thumb.jpg'), cv2.resize(im, (1280, 720), interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 92])
print('thumb ok')
