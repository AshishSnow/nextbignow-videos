import os, sys, skia
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa import *
from neon import person
s = skia.Surface(W, H); c = s.getCanvas()
sunburst(c, 'red', 0.7); logo(c)
headline(c, 'WHY IS GAS ALWAYS', '$2.99 AND 9/10?', y=430, s1=96, s2=112)
polaroid(c, 520, 980, 660, 620, -4, 1, lambda cc, w, h: pic_station(cc, w, h, 0.5))
burst(c, 840, 740, 140, '9/10\n¢?', 1, rot=10)
person(c, 800, 1640, 0.62, (255, 140, 40), (36, 44, 90), mood='shock', look=(-0.6, -0.6), sweat=2, t=0.4, arm_r=(40, 220), arm_l=(-120, -120))
s.makeImageSnapshot().save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thumbnail_gas.png'), skia.kPNG)
print('ok')
