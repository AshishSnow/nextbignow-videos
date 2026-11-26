"""usage: render.py plat f0 f1 out.mp4"""
import sys, subprocess, numpy as np
plat, f0, f1, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
sys.argv = ['x']; exec(open('/home/claude/docu/scenes2.py').read().split("if __name__")[0])
from PIL import Image
TH = None
vf = 'scale=1440:2560:flags=lanczos,format=yuv420p' if plat == 'yt' else 'format=yuv420p'
p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
    '-vf', vf, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', out + '.tmp.mp4'], stdin=subprocess.PIPE)
for f in range(f0, f1):
    fr = TH if (plat == 'yt' and f < 9) else frame(f / 30, plat)
    p.stdin.write(fr.tobytes())
p.stdin.close(); p.wait()
import os; os.replace(out + '.tmp.mp4', out); print('done', out)
