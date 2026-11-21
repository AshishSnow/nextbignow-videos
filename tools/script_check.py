"""Script linter for NextBigNow shorts (framework v3).
Usage: python3 script_check.py path/to/vo.py   (reads the L=[(tag, line), ...] list)
"""
import re, sys
def syl(w):
    w = re.sub(r'[^a-z]', '', w.lower())
    if not w: return 0
    n = len(re.findall(r'[aeiouy]+', w)); n -= w.endswith('e') and not w.endswith(('le', 'ee')) and n > 1
    return max(1, n)
def grade(t):
    s = max(1, len(re.findall(r'[.!?]+', t))); ws = re.findall(r"[A-Za-z']+", t)
    return 0.39 * len(ws) / s + 11.8 * sum(map(syl, ws)) / len(ws) - 15.59
src = open(sys.argv[1]).read(); a = src.index('L=['); b = src.index(']\n', a)
lines = [m[1] for m in re.findall(r'\("(\w+)",\s*"((?:[^"\\]|\\.)*)"\)', src[a:b + 1])]
text = ' '.join(lines); words = len(text.split())
print(f'words {words}  (~{words / 2.7:.0f}s at our pace; target 95-125 words / 30-45 s)')
print(f'reading grade {grade(text):.1f}  (target <= 5)')
first = lines[0]
print(f'line 1: {len(first.split())} words (target <= 12): "{first}"')
bad = [p for p in (r'^(on|this|last) (monday|tuesday|wednesday|thursday|friday|saturday|sunday|week)', r'^scientists', r'^researchers', r'^a new study', r'^in \d{4}', r'^hey', r'^today')
       if re.search(p, first.lower())]
if bad: print('  WARN weak opener pattern:', bad)
if not re.search(r'\byou(r)?\b', ' '.join(lines[:2]).lower()): print('  WARN no "you/your" in first two lines')
hed = re.findall(r'\b(basically|essentially|actually|it\'s worth noting|in fact|literally)\b', text.lower())
if hed: print('  WARN hedges:', hed)
tl = text.lower(); nb = len(re.findall(r'\bbut\b', tl)); ns = len(re.findall(r'\bso\b', tl))
print(f'"but": {nb}  "so": {ns}  "and then": {tl.count("and then")}  (want 2+ buts in the body)')
if re.search(r'comment yes or no|subscribe|follow', lines[-1].lower()): print('  WARN spoken sign-off in last line (move CTA to caption)')
for i, l in enumerate(lines):
    if len(l.split()) > 18: print(f'  WARN line {i} long ({len(l.split())} words)')
print('LOOP CHECK (read as one):', lines[-1], '->', first)
