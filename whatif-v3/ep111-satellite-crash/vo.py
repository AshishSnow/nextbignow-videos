import os, json, subprocess, numpy as np, soundfile as sf
os.chdir("/home/claude/tts")
from kokoro_onnx import Kokoro
k=Kokoro("kokoro.onnx","voices.npz"); VO=np.load("voices.npz")
# tag: voice, speed, gain dB, pause after
TAGS={"fast":("mix_michael_puck",1.1,0.5,0.1),"story":("mix_michael_puck",1.0,0,0.18),"excited":("hype",1.05,1,0.15),"deadpan":("calm",0.95,-1,0.22),
 "tease":("calm",0.97,-1.5,0.26),"reveal":("hype",1.02,1.5,0.2),"serious":("calm",0.97,0,0.2),"hype":("hype",1.05,1.5,0.18),
 "aside":("calm",1.05,-2.5,0.12),"friend":("mix_michael_puck",1.02,0,0.18),"punchline":("calm",0.93,1,0.3),"question":("mix_michael_puck",1.03,0.5,0.15),"count":("hype",1.0,1.5,0.5)}
CHAIN="highpass=f=80,lowpass=f=9500,equalizer=f=200:t=q:w=1:g=1.5,equalizer=f=6500:t=q:w=1.5:g=-4,deesser=i=0.6:m=0.5:f=0.5,afftdn=nf=-40,agate=threshold=0.012:ratio=6:attack=4:release=180:range=0.02,acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120:knee=4"
SEED = "2009 Iridium 33 / Kosmos 2251: first satellite-satellite crash, 789 km over Siberia, 11.7 km/s, 2,000+ catalogued fragments, ~1,128 still up in 2024; ISS crew sheltered in Soyuz in 2012. Today 16,686 active sats of 32,092 tracked objects; Starlink 355k dodges/yr; CRASH clock 2.8 days (128 in 2018)."
TEXT_HOOK = "WHAT IF TWO SATELLITES CRASHED?"
HYPOTHESIS = "Reference-logic script + glow-lit world; new: slow-motion hypervelocity crash with debris particle physics, highway metaphor, CRASH clock."
PURPOSE = "Viewer learns what a satellite collision does (shrapnel that lingers for decades), how crowded orbit is now, and Kessler syndrome."
L=[("hype","What would happen if two satellites crashed... right over your head?",0.1),
("punchline","Not a fender bender. A hit ten times faster than a bullet.",0.15),
("story","It already happened. February two thousand nine, almost five hundred miles over Siberia.",0.05),
("story","A working American satellite... and a dead Russian one that nobody was steering.",0.3),
("reveal","In a split second, both were gone. Over two thousand pieces of shrapnel.",0.35),
("tease","And fifteen years later... over a thousand of those pieces are still up there.",0.1),
("story","In twenty twelve, astronauts on the space station had to hide in their escape capsules from one of them.",0.4),
("excited","But that was one crash.",0.2),
("story","Today, there are over sixteen thousand working satellites. And half of everything we track up there is dead junk. Like a highway where half the cars have no driver.",0.1),
("story","Starlink alone dodges a crash almost a thousand times a day.",0.15),
("story","Scientists even built a clock for it. If every satellite lost control, say in a huge solar storm, the first crash would come in under three days. In twenty eighteen, it was four months.",0.25),
("tease","And every crash makes more junk... that causes more crashes.",0.4),
("punchline","Right now, satellites are dodging a crash every ninety seconds...",0.5),
("punchline","and they have to win every single time.",0.0)]
SR=48000; parts=[]; lines=[]; t=0.0
for i,(tag,text,extra) in enumerate(L):
    v,sp,g,pa=TAGS[tag]; a,sr=k.create(text,voice=VO[v],speed=sp*0.92,lang="en-us")
    idx=np.where(np.abs(a)>0.008)[0]; a=a[max(0,idx[0]-480):idx[-1]+960].astype(np.float32)
    fi,fo=int(.012*sr),int(.03*sr); a[:fi]*=np.linspace(0,1,fi); a[-fo:]*=np.linspace(1,0,fo); a*=10**(g/20)
    sf.write("/tmp/n.wav",a,sr); subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/tmp/n.wav","-af","aresample=48000:resampler=soxr,"+CHAIN,"-ar","48000","-ac","1","/tmp/n2.wav"],check=True)
    b=sf.read("/tmp/n2.wav",dtype="float32")[0]; lines.append(dict(i=i,tag=tag,text=text,start=round(t,3),dur=round(len(b)/SR,3)))
    pa=pa*0.5+extra; parts+=[b,np.zeros(int(pa*SR),np.float32)]; t+=len(b)/SR+pa
sf.write("/home/claude/sat/vo_raw.wav",np.concatenate(parts),SR)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/home/claude/sat/vo_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","/home/claude/sat/vo.wav"],check=True)
json.dump(lines,open("/home/claude/sat/lines.json","w"),indent=1); print("dur",round(t,2))
