import os, json, subprocess, numpy as np, soundfile as sf
os.chdir("/home/claude/tts")
from kokoro_onnx import Kokoro
k=Kokoro("kokoro.onnx","voices.npz"); VO=np.load("voices.npz")
# tag: voice, speed, gain dB, pause after
TAGS={"fast":("mix_michael_puck",1.1,0.5,0.1),"story":("mix_michael_puck",1.0,0,0.18),"excited":("hype",1.05,1,0.15),"deadpan":("calm",0.95,-1,0.22),
 "tease":("calm",0.97,-1.5,0.26),"reveal":("hype",1.02,1.5,0.2),"serious":("calm",0.97,0,0.2),"hype":("hype",1.05,1.5,0.18),
 "aside":("calm",1.05,-2.5,0.12),"friend":("mix_michael_puck",1.02,0,0.18),"punchline":("calm",0.93,1,0.3),"question":("mix_michael_puck",1.03,0.5,0.15),"count":("hype",1.0,1.5,0.5)}
CHAIN="highpass=f=80,lowpass=f=9500,equalizer=f=200:t=q:w=1:g=1.5,equalizer=f=6500:t=q:w=1.5:g=-4,deesser=i=0.6:m=0.5:f=0.5,afftdn=nf=-40,agate=threshold=0.012:ratio=6:attack=4:release=180:range=0.02,acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120:knee=4"
SEED = "Space nuke: DIA says Russia is developing a nuclear-armed satellite; Germany takes seriously intel it could go up as soon as next month. Starfish Prime (9 Jul 1962, 400 km, 1.4 Mt) turned Hawaii's sky into a 'new sun', killed ~300 streetlights 1,450 km away, cut Kauai phone link, and its radiation belt killed 6+ satellites incl. Telstar 1. Today: 11,000+ Starlink sats + GPS."
TEXT_HOOK = "WHAT IF A NUKE WENT OFF IN SPACE?"
HYPOTHESIS = "Reference-logic script (claim + familiar contrast + irony thesis + picture sentences + turn + mirrored ending) with a new glow-lit look (procedural lit Earth, aurora, silhouettes, bloom/grain)."
PURPOSE = "Viewer learns what a nuclear blast in orbit does (EMP, artificial aurora, radiation belt killing satellites) from the real 1962 Starfish Prime test, and why it matters now."
L=[("hype","What would happen if someone set off a nuke... in space?",0.1),
("punchline","Not on a city. Two hundred and fifty miles over your head.",0.15),
("story","Because right now, US intelligence says Russia is building a satellite that can carry one. And Germany says it could go up as soon as next month.",0.2),
("tease","Here's the crazy part. It wouldn't hurt a single person on the ground... and that's exactly why it's so dangerous.",0.45),
("story","We know, because America already did it. July, nineteen sixty-two.",0.05),
("story","In Hawaii, people threw parties on their rooftops to watch.",0.1),
("reveal","At eleven p.m., the sky lit up like a brand new sun... then turned blood red.",0.35),
("fast","Nine hundred miles away, three hundred streetlights went dark. Burglar alarms went off. Phone calls between islands just... cut out.",0.4),
("excited","But the real damage was invisible.",0.2),
("story","The blast left a belt of radiation around Earth for years. Within months, at least six satellites were dead. Including Telstar, the first satellite to beam live TV.",0.35),
("story","That was nineteen sixty-two. Today, Starlink alone has over eleven thousand satellites up there. Plus the GPS in your phone.",0.2),
("punchline","So a nuke in space wouldn't hurt a single person...",0.5),
("punchline","it would just turn off the sky your phone talks to.",0.0)]
SR=48000; parts=[]; lines=[]; t=0.0
for i,(tag,text,extra) in enumerate(L):
    v,sp,g,pa=TAGS[tag]; a,sr=k.create(text,voice=VO[v],speed=sp*0.92,lang="en-us")
    idx=np.where(np.abs(a)>0.008)[0]; a=a[max(0,idx[0]-480):idx[-1]+960].astype(np.float32)
    fi,fo=int(.012*sr),int(.03*sr); a[:fi]*=np.linspace(0,1,fi); a[-fo:]*=np.linspace(1,0,fo); a*=10**(g/20)
    sf.write("/tmp/n.wav",a,sr); subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/tmp/n.wav","-af","aresample=48000:resampler=soxr,"+CHAIN,"-ar","48000","-ac","1","/tmp/n2.wav"],check=True)
    b=sf.read("/tmp/n2.wav",dtype="float32")[0]; lines.append(dict(i=i,tag=tag,text=text,start=round(t,3),dur=round(len(b)/SR,3)))
    pa=pa*0.5+extra; parts+=[b,np.zeros(int(pa*SR),np.float32)]; t+=len(b)/SR+pa
sf.write("/home/claude/nuke/vo_raw.wav",np.concatenate(parts),SR)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/home/claude/nuke/vo_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","/home/claude/nuke/vo.wav"],check=True)
json.dump(lines,open("/home/claude/nuke/lines.json","w"),indent=1); print("dur",round(t,2))
