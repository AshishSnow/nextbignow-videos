#!/usr/bin/env python3
"""Calibrate the blind hook panel against real IG 3-s rates. Usage: hook_panel_score.py <panel_map.json> <lists_dir>"""
import json,sys,random,statistics as st
sys.path.insert(0,'.')
from hook_panel_items import H,C
from hook_length_audit import R,rho,perm
pm={int(k):v for k,v in json.load(open(sys.argv[1])).items()}; ld=sys.argv[2]
Rt=json.load(open('hook_panel_ratings.json')); raters={}
for s in range(4):
    order=[int(l.split(':')[0]) for l in open(f'{ld}/list{s}.txt')]
    raters[s]={pm[order[int(p)-1]]:v for p,v in Rt[f'list{s}'].items()}
raters[4]={pm[int(i)]:v for i,v in Rt['list4_by_id'].items()}
real={r[0]:r[5] for r in R}; keys=list(H)
print("items per rater",[len(v) for v in raters.values()])
for s,v in raters.items():
    k=[x for x in keys if x in v]
    print(f"rater {s}: rho vs real 3-s {rho([v[x] for x in k],[real[x] for x in k]):+.2f} (n={len(k)}) spread sd {st.pstdev(v.values()):.1f}")
mean={x:st.mean(v[x] for v in raters.values() if x in v) for x in list(H)+list(C)}
a=[mean[x] for x in keys]; b=[real[x] for x in keys]
print(f"PANEL MEAN vs real 3-s: rho {rho(a,b):+.2f}  perm p {perm(a,b):.3f} n={len(keys)}")
print("views: rho",round(rho(a,[r[2] for r in sorted(R,key=lambda r:keys.index(r[0]))]),2))
pairs=[]; rs=list(raters)
for i in rs:
    for j in rs:
        if i<j:
            k=[x for x in raters[i] if x in raters[j]]; pairs.append(rho([raters[i][x] for x in k],[raters[j][x] for x in k]))
print(f"inter-rater mean rho {st.mean(pairs):+.2f} (min {min(pairs):+.2f} max {max(pairs):+.2f})")
# best guess split: top-half panel vs bottom-half
sk=sorted(keys,key=lambda x:-mean[x]); t=sk[:9]; bm=sk[9:]
print("real 3-s: panel top 9",round(st.mean(real[x] for x in t),1),"bottom 9",round(st.mean(real[x] for x in bm),1))
print("\nhistoric: panel vs real")
for x in sk: print(f"{mean[x]:5.1f} real {real[x]:5.1f} {x}")
print("\ncandidates (same scale)")
for x in sorted(C,key=lambda x:-mean[x]): print(f"{mean[x]:5.1f} {x}: {C[x]}  [{[raters[s].get(x) for s in rs]}]")
