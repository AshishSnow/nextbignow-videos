"""script_check.py <project dir> — packaging-first gate before any TTS.
Reads scripts/maya_paras.py (PARAS) and optional PACKAGING.md; prints word count, est. length at 150 wpm,
when the reward (first line marked with '*' in PACKAGING.md 'Reward:' or the 2nd sentence) lands, and fails loudly on:
  - no PACKAGING.md (title + cover line must exist BEFORE the script)
  - > 80 words for a 30 s quip/tip (> 155 for a 60 s story) -> cut or split into two reels
  - reward later than ~6 s"""
import sys, os, re
d = sys.argv[1]; sys.path.insert(0, os.path.join(d, 'scripts')); from maya_paras import PARAS
text = ' '.join(t for t, _, _ in PARAS); words = text.split(); n = len(words); wpm = 150
print(f'words {n}  ->  ~{n / wpm * 60:.0f} s at {wpm} wpm')
pk = os.path.join(d, 'PACKAGING.md'); ok = True
if not os.path.exists(pk): print('FAIL: write PACKAGING.md first (type, title, cover line, reward line, gap question)'); ok = False
else:
    s = open(pk).read(); m = re.search(r'Reward:\s*(.+)', s); typ = re.search(r'Type:\s*(\w+)', s)
    t_ = typ.group(1).lower() if typ else 'quip'
    limit = {'story': 155, 'long': 1000}.get(t_, 80)   # long = 5-6 min YouTube video (~150 wpm)
    if n > limit: print(f'FAIL: {n} words > {limit} — cut filler or split into two reels'); ok = False
    if m:
        key = m.group(1).strip().split()[:3]; low = [w.lower().strip('.,?!') for w in words]
        idx = next((i for i in range(n) if low[i:i + len(key)] == [k.lower().strip('.,?!') for k in key]), None)
        if idx is None: print('WARN: reward line not found in script text')
        else:
            t = (idx + len(m.group(1).split())) / wpm * 60; print(f'reward lands by ~{t:.1f} s')
            if t > 6.5: print('FAIL: reward after ~6 s — hand over the shock earlier, then open the gap'); ok = False
print('PASS' if ok else 'NOT READY'); sys.exit(0 if ok else 1)
