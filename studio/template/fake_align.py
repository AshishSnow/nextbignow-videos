"""fake_align.py <proj>: writes comic/cd/align.json from scripts/maya_paras.py at ~150 wpm (layout tests only)"""
import sys, os, json, re
d = sys.argv[1]; sys.path.insert(0, os.path.join(d, 'scripts')); from maya_paras import PARAS
t = 0.0; out = []
for txt, _, _ in PARAS:
    for w in txt.split():
        tok = re.sub(r"[^\w'’-]", '', w); 
        if not tok: continue
        out.append([tok, round(t, 3), round(t + 0.36, 3)]); t += 0.4
        if w[-1] in '.?!': t += 0.35
        elif w[-1] == ',': t += 0.15
os.makedirs(os.path.join(d, 'comic/cd'), exist_ok=True); json.dump(out, open(os.path.join(d, 'comic/cd/align.json'), 'w')); open(os.path.join(d, 'comic/cd/script.txt'), 'w').write(' '.join(t for t, _, _ in PARAS)); print(d, 'fake dur', round(t, 1))
