import os, json, subprocess, numpy as np, soundfile as sf
os.chdir("/home/claude/tts")
from kokoro_onnx import Kokoro
k=Kokoro("kokoro.onnx","voices.npz"); VO=np.load("voices.npz")
# tag: voice, speed, gain dB, pause after
TAGS={"story":("mix_michael_puck",1.0,0,0.18),"excited":("hype",1.05,1,0.15),"deadpan":("calm",0.95,-1,0.22),
 "tease":("calm",0.97,-1.5,0.26),"reveal":("hype",1.02,1.5,0.2),"serious":("calm",0.97,0,0.2),"hype":("hype",1.05,1.5,0.18),
 "aside":("calm",1.05,-2.5,0.12),"friend":("mix_michael_puck",1.02,0,0.18),"punchline":("calm",0.93,1,0.3),"question":("mix_michael_puck",1.03,0.5,0.15)}
CHAIN="highpass=f=80,lowpass=f=9500,equalizer=f=200:t=q:w=1:g=1.5,equalizer=f=6500:t=q:w=1.5:g=-4,deesser=i=0.6:m=0.5:f=0.5,afftdn=nf=-40,agate=threshold=0.012:ratio=6:attack=4:release=180:range=0.02,acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120:knee=4"
L=[("hype","What if you dug in the Saudi desert... and hit a hippo?"),
("question","Sounds fake. But it's real."),
("story","A hundred twenty-five thousand years ago, this sand was a lake. Hippos swam in it."),
("tease","And people camped right on the shore. Three clues prove it."),
("reveal","Clue one. Over five thousand stone tools, in one spot."),
("story","Clue two. Bones. Hippo, ostrich, camel, buffalo. All butchered."),
("excited","But clue three is the creepy one. Traces of a plant hunters used for poison arrows."),
("serious","So this wasn't a desert people ran through. It was a home."),
("friend","And from space, scientists have spotted thousands more old lakes."),
("punchline","Any one could hide the next camp. You'd just have to dig in the Saudi desert.")]
SR=48000; parts=[]; lines=[]; t=0.0
for i,(tag,text) in enumerate(L):
    v,sp,g,pa=TAGS[tag]; a,sr=k.create(text,voice=VO[v],speed=sp*0.88,lang="en-us")
    idx=np.where(np.abs(a)>0.008)[0]; a=a[max(0,idx[0]-480):idx[-1]+960].astype(np.float32)
    fi,fo=int(.012*sr),int(.03*sr); a[:fi]*=np.linspace(0,1,fi); a[-fo:]*=np.linspace(1,0,fo); a*=10**(g/20)
    sf.write("/tmp/n.wav",a,sr); subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/tmp/n.wav","-af","aresample=48000:resampler=soxr,"+CHAIN,"-ar","48000","-ac","1","/tmp/n2.wav"],check=True)
    b=sf.read("/tmp/n2.wav",dtype="float32")[0]; lines.append(dict(i=i,tag=tag,text=text,start=round(t,3),dur=round(len(b)/SR,3)))
    parts+=[b,np.zeros(int(pa*SR),np.float32)]; t+=len(b)/SR+pa
sf.write("/home/claude/hippo/vo_raw.wav",np.concatenate(parts),SR)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/home/claude/hippo/vo_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","/home/claude/hippo/vo.wav"],check=True)
json.dump(lines,open("/home/claude/hippo/lines.json","w"),indent=1); print("dur",round(t,2))
