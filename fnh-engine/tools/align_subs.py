import json,re,difflib,sys
chunks,scriptf,total,out=sys.argv[1],sys.argv[2],float(sys.argv[3]),sys.argv[4]
CH=[]
for ln in open(chunks,encoding='utf-8'):
    m=re.match(r'([\d.]+)-([\d.]+)\s+(.*)',ln.strip())
    if m and m[3].strip(): CH.append((float(m[1]),float(m[2]),m[3]))
wch=[];wt=[]
for s,e,txt in CH:
    t=txt.replace(' ','')
    for i,ch in enumerate(t): wch.append(ch); wt.append(s+(e-s)*i/max(1,len(t)))
script=re.sub(r'\[[a-z ]+\]','',open(scriptf,encoding='utf-8').read()).split()
sc=[];owner=[]
for wi,w in enumerate(script):
    for ch in w: sc.append(ch); owner.append(wi)
sm=difflib.SequenceMatcher(None,sc,wch,autojunk=False)
first=[None]*len(script)
for a,b,n in sm.get_matching_blocks():
    for k in range(n):
        wi=owner[a+k]
        if first[wi] is None: first[wi]=wt[b+k]
known=[(i,t) for i,t in enumerate(first) if t is not None]
times=[]
for i in range(len(script)):
    if first[i] is not None: times.append(first[i]); continue
    prev=max([k for k in known if k[0]<i],default=(0,0.0),key=lambda k:k[0]); nxt=min([k for k in known if k[0]>i],default=(len(script),total),key=lambda k:k[0])
    times.append(prev[1]+(nxt[1]-prev[1])*(i-prev[0])/max(1,nxt[0]-prev[0]))
for i in range(1,len(times)):
    if times[i]<times[i-1]: times[i]=times[i-1]+0.05
subs=[];g=[];gt=[]
for i,w in enumerate(script):
    g.append(w);gt.append(round(times[i],2))
    if len(g)==3 or re.search(r'[,।?!:.]$',w) or i==len(script)-1:
        subs.append(dict(w=g,t=gt,s=gt[0]));g=[];gt=[]
for i,sb in enumerate(subs):
    nxt=subs[i+1]['s'] if i+1<len(subs) else total
    sb['e']=round(min(nxt, sb['t'][-1]+1.2),2)
o=[]
for g in subs:
    k=[(w.strip('—"').strip(),t) for w,t in zip(g['w'],g['t']) if w.strip('—"…').strip()]
    if not k: continue
    g['w']=[w for w,_ in k]; g['t']=[t for _,t in k]; g['s']=g['t'][0]; o.append(g)
json.dump(o,open(out,'w'),ensure_ascii=False); print(len(o))
