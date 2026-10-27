# Rank-correlate story_check metrics with Instagram retention. Run from studio/: python3 lab/story/corr.py
# D = {example_dir: (real length s, IG avg watch s, IG 3-s rate %)} — add rows as Metricool data returns.
import sys,runpy,os
sys.argv=['x']; m=runpy.run_path('tools/story_check.py')
D={'costco':(68,23.0,64.1),'starbucks':(55,17.3,61.6),'amazon':(70,13.1,50.0),'chickfila':(75,18.3,54.2),'planetfitness':(75,22.2,64.0),'printerink':(75,21.5,74.0)}
from statistics import mean
def rank(v):
    s=sorted(range(len(v)),key=lambda i:v[i]);r=[0]*len(v)
    i=0
    while i<len(s):
        j=i
        while j+1<len(s) and v[s[j+1]]==v[s[i]]: j+=1
        for k in range(i,j+1): r[s[k]]=(i+j)/2
        i=j+1
    return r
def sp(a,b):
    ra,rb=rank(a),rank(b);ma,mb=mean(ra),mean(rb)
    num=sum((x-ma)*(y-mb) for x,y in zip(ra,rb));den=(sum((x-ma)**2 for x in ra)*sum((y-mb)**2 for y in rb))**.5
    return num/den if den else float('nan')
rows={}
for k,(L,aw,h3) in D.items():
    R,_=m['check'](f'examples/{k}/vo_lines.py',L); rows[k]=(R,aw/L*100,h3,aw)
keys=['count_promise','item_labels','hook_words','claim_by_s','max_gap_s','gaps_over_20s','turns_per_min','causal_openers_pct','words_per_sentence','multi_number_sentences','twist_to_end_s','rules_passed','loop_events']
print('script'.ljust(14),'aw%','3s',*[k[:8] for k in keys])
for k,(R,awp,h3,aw) in rows.items(): print(k.ljust(14),round(awp),h3,*[R[x] for x in keys])
for x in keys:
    a=[rows[k][0][x] for k in rows]
    print(f'{x:24s} rho(avg-watch%)={sp(a,[rows[k][1] for k in rows]):+.2f}  rho(avg-watch s)={sp(a,[rows[k][3] for k in rows]):+.2f}  rho(3s)={sp(a,[rows[k][2] for k in rows]):+.2f}')
