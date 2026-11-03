#!/usr/bin/env python3
"""R&D Story run 3 Nov 2026: does hook wording / length line up with retention on our animated reels?
IG rows: Metricool pull 3 Nov 2026 02:50 UTC. Lengths: PERFORMANCE.md / topics.md ('~' = PERFORMANCE estimate).
Hook = i1 from examples/*/vo_lines.py. Excludes posts < 24 h old (food truck) and pre-animation AI-footage reels."""
import random, re, statistics as st
R = [ # name, len s, views, reach, avg watch s, 3-s %, shares, saves, hook
("drone",115,1319,1187,27.495,75.9,6,14,"How can one drone start a whole business?"),
("vending",99,501,441,36.458,68.2,0,5,"Before you buy a vending machine, do you know what a singer is?"),
("glasses",145,149,122,18.257,43.4,0,1,"How can your sunglasses, the shop, and your eye insurance all be one company?"),
("banana",132,147,127,23.414,56.2,0,0,"Why is almost every banana you buy a copy of the exact same plant?"),
("hoover",136,157,135,14.893,44.2,0,0,"What happens when a vacuum company gives away free flights, and everyone says yes?"),
("monopoly",135,188,163,30.842,60.7,0,0,"Did you know Monopoly was invented to warn against monopolies?"),
("debeers",118,164,148,17.267,48.0,1,0,"Why does a tiny rock cost two months' salary?"),
("airline",101,589,539,28.312,63.8,0,1,"Why would a credit card company pay an airline eight billion dollars?"),
("gas",81,1523,1185,22.264,66.7,1,0,"Do you know your gas station barely makes any money… on gas?"),
("duolingo",93,166,148,12.897,23.5,0,0,"Duolingo gives away every single lesson for free… so how did it make over a billion dollars last year?"),
("visa",70,66,58,14.356,52.5,0,0,"Did you know Visa never lends you a single dollar… yet it keeps about half of everything it makes as profit?"),
("popcorn",75,145,123,12.703,53.7,0,0,"Did you know AMC makes almost as much money from popcorn… as from every single movie ticket it sells?"),
("planet",75,1283,1087,26.145,69.4,2,1,"How does Planet Fitness charge just fifteen dollars a month... and still make over two hundred million dollars?"),
("printer",75,1376,1195,21.425,73.7,0,0,"Did you know printer ink can cost seven times more than fancy champagne?"),
("chickfila",75,182,150,18.16,54.1,0,0,"Why is Chick-fil-A closed every single Sunday… and still beating almost everyone?"),
("amazon",70,231,200,12.794,50.5,0,1,"Do you think Amazon makes its money… by selling you stuff?"),
("starbucks",55,412,342,17.275,61.6,2,0,"Do you know Starbucks is sitting on one point seven billion dollars… of your money?"),
("costco",68,1229,1071,22.996,64.0,0,3,"Do you know Costco sells a hot dog and a soda for just a dollar fifty?"),
]
def rank(x):
    s=sorted(range(len(x)),key=lambda i:x[i]); r=[0.0]*len(x); i=0
    while i<len(s):
        j=i
        while j+1<len(s) and x[s[j+1]]==x[s[i]]: j+=1
        for k in range(i,j+1): r[s[k]]=(i+j)/2
        i=j+1
    return r
def rho(a,b):
    ra,rb=rank(a),rank(b); ma,mb=st.mean(ra),st.mean(rb)
    n=sum((p-ma)*(q-mb) for p,q in zip(ra,rb)); d=(sum((p-ma)**2 for p in ra)*sum((q-mb)**2 for q in rb))**.5
    return n/d if d else 0.0
def perm(a,b,N=20000,seed=1):
    r0=abs(rho(a,b)); rnd=random.Random(seed); b=list(b); c=0
    for _ in range(N):
        rnd.shuffle(b)
        if abs(rho(a,b))>=r0-1e-9: c+=1
    return c/N
L=[r[1] for r in R]; AW=[r[4] for r in R]; S3=[r[5] for r in R]; HOLD=[100*r[4]/r[1] for r in R]
HW=[len(r[8].split()) for r in R]
YOU=[int(bool(re.search(r"\byou(r)?\b",r[8].lower().replace("do you know","").replace("did you know","").replace("do you think","")))) for r in R]
ELL=[int("…" in r[8] or "..." in r[8]) for r in R]
if __name__ == "__main__":
    print(f"n={len(R)}")
    for nm,a,b in [("length vs avg-watch s",L,AW),("length vs hold % of length",L,HOLD),("length vs 3-s rate",L,S3),
                   ("hook words vs 3-s rate",HW,S3),("hook words vs avg-watch s",HW,AW),("real you/your in hook vs 3-s",YOU,S3),("ellipsis in hook vs 3-s",ELL,S3),
                   ("3-s rate vs views",S3,[r[2] for r in R])]:
        print(f"{nm:34s} rho {rho(a,b):+.2f}  perm p {perm(a,b):.3f}")
    for lo,hi in [(0,80),(80,105),(105,125),(125,999)]:
        g=[r for r in R if lo<=r[1]<hi]
        print(f"len {lo:3d}-{hi:3d}: n={len(g):2d} mean len {st.mean(r[1] for r in g):5.1f} | avg watch {st.mean(r[4] for r in g):5.1f} s | hold {st.mean(100*r[4]/r[1] for r in g):4.1f} % | 3-s {st.mean(r[5] for r in g):4.1f} %")
    for k in (9,12,14,16,99):
        g=[r for r in R if r[8] and len(r[8].split())<=k]
        print(f"hook <= {k:2d} words: n={len(g):2d} 3-s {st.mean(r[5] for r in g):4.1f} % views median {st.median(r[2] for r in g)}")
    g=[r for r in R if len(r[8].split())>12]; print(f"hook > 12 words: n={len(g)} 3-s {st.mean(r[5] for r in g):.1f} % views median {st.median(r[2] for r in g)}")
    print("\nreach/reactions: per 1k", sorted([(round(1000*(r[6]+r[7])/r[3],1),r[0]) for r in R],reverse=True)[:6])
    print("\nhook | words | 3-s, sorted")
    for r in sorted(R,key=lambda r:-r[5]): print(f"{r[5]:5.1f} {len(r[8].split()):3d}w {r[0]:10s} {r[8]}")
