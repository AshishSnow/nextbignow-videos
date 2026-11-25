"""Script linter for NextBigNow shorts (framework v4).
Optional in vo.py: SEED = "...", TEXT_HOOK = "...", HYPOTHESIS = "..." (framework section 8).
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
print(f'words {words}  (~{words / 2.7:.0f}s at our pace; target 80-95 words / 30-35 s)')
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

# v4 bricks (section 8)
def grab(k):
    m = re.search(k + r'\s*=\s*"((?:[^"\\]|\\.)*)"', src); return m[1] if m else None
seed, th, hyp = grab('SEED'), grab('TEXT_HOOK'), grab('HYPOTHESIS')
if not seed: print('  WARN no SEED (one-line premise: you/your thing + surprise + why it matters)')
else: print('SEED:', seed)
if not th: print('  WARN no TEXT_HOOK (frame-1 title, 3-6 words, adds a gap the voice does not say)')
else:
    tw = th.split(); print(f'TEXT_HOOK: "{th}" ({len(tw)} words)')
    if not 3 <= len(tw) <= 6: print('  WARN text hook should be 3-6 words')
    ov = set(w.lower().strip(".,?!") for w in tw) & set(w.lower().strip(".,?!") for w in first.split()) - {'the', 'a', 'an', 'you', 'your', 'is', 'of', 'in', 'to'}
    if len(ov) >= max(2, len(tw) - 1): print('  WARN text hook mostly repeats the spoken hook; make it add new info')
    if re.match(r'^(why|how|what)\b', th.lower()) and not re.search(r'\d', th): print('  WARN text hook reads like a topic label; try a number, paradox or stake')
if not hyp: print('  WARN no HYPOTHESIS (one brick changed + expected effect; log it in tools/experiments.md)')
else: print('HYPOTHESIS:', hyp)
abstract = re.findall(r'\b(ai|fed|stock|market|bank|company|ceo|startup|bitcoin|crypto|inflation)\b', first.lower())
if abstract and not re.search(r'\byou(r)?\b', first.lower()): print('  WARN abstract money/tech opener without "you" (our 3s rate: 21-32%)')
