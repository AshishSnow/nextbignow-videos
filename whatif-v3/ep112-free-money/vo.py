import os, json, subprocess, numpy as np, soundfile as sf
os.chdir("/home/claude/tts")
from kokoro_onnx import Kokoro
k=Kokoro("kokoro.onnx","voices.npz"); VO=np.load("voices.npz")
# tag: voice, speed, gain dB, pause after
TAGS={"fast":("mix_michael_puck",1.1,0.5,0.1),"story":("mix_michael_puck",1.0,0,0.18),"excited":("hype",1.05,1,0.15),"deadpan":("calm",0.95,-1,0.22),
 "tease":("calm",0.97,-1.5,0.26),"reveal":("hype",1.02,1.5,0.2),"serious":("calm",0.97,0,0.2),"hype":("hype",1.05,1.5,0.18),
 "aside":("calm",1.05,-2.5,0.12),"friend":("mix_michael_puck",1.02,0,0.18),"punchline":("calm",0.93,1,0.3),"question":("mix_michael_puck",1.03,0.5,0.15),"count":("hype",1.0,1.5,0.5)}
CHAIN="highpass=f=80,lowpass=f=9500,equalizer=f=200:t=q:w=1:g=1.5,equalizer=f=6500:t=q:w=1.5:g=-4,deesser=i=0.6:m=0.5:f=0.5,afftdn=nf=-40,agate=threshold=0.012:ratio=6:attack=4:release=180:range=0.02,acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120:knee=4"
SEED = "Musk (19 Oct 2026) pledged one SpaceX share (~$146) to every US child (~72M, ~$10.5B). Case: Alaska PFD since 1982 ($1,000 first; $3,284 in 2022 incl. energy relief; family of five >$16k); UChicago (Jones & Marinescu): no drop in employment, part-time +17%; Stockton SEED: $500/mo, full-time 28%->40% in a year."
TEXT_HOOK = "FREE MONEY MADE PEOPLE WORK MORE"
HYPOTHESIS = "Money/fairness topic (new topic type) + 'won't it make people lazy?' myth flipped by a 40-year real case; warm golden glow world."
PURPOSE = "Viewer learns what decades of real free-money programs show (Alaska dividend, Stockton) and why the 'lazy' fear didn't come true."
# v2 (27 Nov lessons): packaging first (cover = "FREE MONEY MADE PEOPLE WORK MORE"), reward by ~4 s, ~120 words
L=[("hype","Free money made people work more.",0.15),
("reveal","A California city gave people five hundred dollars a month. Full-time jobs jumped from twenty-eight percent... to forty.",0.2),
("story","Now Elon Musk says he'll give every kid in America a SpaceX share. That's seventy-two million kids.",0.1),
("tease","So... will they grow up lazy?",0.3),
("story","Alaska already ran this test. Since nineteen eighty-two, almost everyone there, even babies, gets a yearly oil check.",0.05),
("story","In twenty twenty-two, it hit over three thousand dollars each.",0.15),
("reveal","Economists checked. Jobs didn't drop. Part-time work went up.",0.2),
("story","Turns out a cushion doesn't make people quit. It gives them room to find better work.",0.35),
("punchline","So the real question isn't if these kids get lazy. It's what they'll build.",0.0)]
SR=48000; parts=[]; lines=[]; t=0.0
for i,(tag,text,extra) in enumerate(L):
    v,sp,g,pa=TAGS[tag]; a,sr=k.create(text,voice=VO[v],speed=sp*0.92,lang="en-us")
    idx=np.where(np.abs(a)>0.008)[0]; a=a[max(0,idx[0]-480):idx[-1]+960].astype(np.float32)
    fi,fo=int(.012*sr),int(.03*sr); a[:fi]*=np.linspace(0,1,fi); a[-fo:]*=np.linspace(1,0,fo); a*=10**(g/20)
    sf.write("/tmp/n.wav",a,sr); subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/tmp/n.wav","-af","aresample=48000:resampler=soxr,"+CHAIN,"-ar","48000","-ac","1","/tmp/n2.wav"],check=True)
    b=sf.read("/tmp/n2.wav",dtype="float32")[0]; lines.append(dict(i=i,tag=tag,text=text,start=round(t,3),dur=round(len(b)/SR,3)))
    pa=pa*0.5+extra; parts+=[b,np.zeros(int(pa*SR),np.float32)]; t+=len(b)/SR+pa
sf.write("/home/claude/cash/vo_raw.wav",np.concatenate(parts),SR)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/home/claude/cash/vo_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","/home/claude/cash/vo.wav"],check=True)
json.dump(lines,open("/home/claude/cash/lines.json","w"),indent=1); print("dur",round(t,2))
