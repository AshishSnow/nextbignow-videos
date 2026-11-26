#!/usr/bin/env python3
"""Hook-form audit (R&D 26 Nov 2026) — does the FORM of line 1 predict whether an IG reel escapes the ~150-350-view test pool?
Data: lab/story/ig_reels_26nov.csv (Metricool IGRE02/03/23/24/28/21, brand 7643430, posts 6-25 Nov 2026; the caption's first line
is a proxy for the spoken/text hook). Only posts >= ~24 h old are scored. Usage: python3 lab/story/hook_form_audit.py [csv]
Caveats: n = 70, look (doodle / sketch / comic) and series label are confounded with hook form; this is evidence, not proof."""
import csv, re, sys, statistics as st
from collections import defaultdict
path = sys.argv[1] if len(sys.argv) > 1 else "studio/lab/story/ig_reels_26nov.csv"
rows = [r for r in csv.DictReader(open(path)) if r["published_utc"] < "202611250500"]
def form(c):
    if re.match(r"(Case Study|Mind Tricks|Business Idea|Money Explained|Founder Mindset) N", c): return "series label first"
    if re.match(r"(How to start|How .* got so big|.*, explained)", c): return "how-to / explained"
    if c.split()[0] in ("Would", "Could", "Why", "How", "Can", "Too", "Pay", "That", "Pick"): return "question"
    return "statement"
g = defaultdict(list)
for r in rows: g[form(r["caption_first_line"])].append(r)
print(f"{len(rows)} reels >= 24 h old")
for k, v in sorted(g.items(), key=lambda kv: -st.median(int(r['views']) for r in kv[1])):
    vs = [int(r["views"]) for r in v]
    print(f"  {k:20s} n={len(v):2d}  median views {st.median(vs):6.0f}  >=1k {sum(x >= 1000 for x in vs):2d}  median 3-s {st.median(float(r['three_s_pct']) for r in v):.1f} %")
for t in (60, 65, 70):
    a = [r for r in rows if float(r["three_s_pct"]) >= t]
    print(f"  3-s >= {t} %: n={len(a):2d}, share that broke 1k views {sum(int(r['views']) >= 1000 for r in a) / len(a):.0%}")
a = [r for r in rows if float(r["three_s_pct"]) < 60]
print(f"  3-s <  60 %: n={len(a):2d}, share that broke 1k views {sum(int(r['views']) >= 1000 for r in a) / len(a):.0%}")
