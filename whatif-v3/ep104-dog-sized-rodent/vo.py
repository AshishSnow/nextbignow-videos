import os, json, subprocess, numpy as np, soundfile as sf
os.chdir("/home/claude/tts")
from kokoro_onnx import Kokoro
k=Kokoro("kokoro.onnx","voices.npz"); VO=np.load("voices.npz")
# tag: voice, speed, gain dB, pause after
TAGS={"story":("mix_michael_puck",1.0,0,0.18),"excited":("hype",1.05,1,0.15),"deadpan":("calm",0.95,-1,0.22),
 "tease":("calm",0.97,-1.5,0.26),"reveal":("hype",1.02,1.5,0.2),"serious":("calm",0.97,0,0.2),"hype":("hype",1.05,1.5,0.18),
 "aside":("calm",1.05,-2.5,0.12),"friend":("mix_michael_puck",1.02,0,0.18),"punchline":("calm",0.93,1,0.3),"question":("mix_michael_puck",1.03,0.5,0.15),"count":("hype",1.0,1.5,0.5)}
CHAIN="highpass=f=80,lowpass=f=9500,equalizer=f=200:t=q:w=1:g=1.5,equalizer=f=6500:t=q:w=1.5:g=-4,deesser=i=0.6:m=0.5:f=0.5,afftdn=nf=-40,agate=threshold=0.012:ratio=6:attack=4:release=180:range=0.02,acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120:knee=4"
SEED = "A rodent as heavy as your big dog lived 35 million years ago in Thailand, and we know it from basically one tooth."
TEXT_HOOK = "FROM JUST ONE TOOTH"
HYPOTHESIS = "Text hook brick: a method mystery ('from just one tooth') instead of a number/contradiction -> compare 3s rate with ep100/ep102."
PURPOSE = "Viewer learns about Yakamys, a ~30 kg rodent from 35-million-year-old Thailand, known from one molar, and that the size is a rough estimate."
L=[("hype","Imagine a rodent as heavy as your big dog. That was real."),
("tease","About sixty-six pounds. Living in Thailand thirty-five million years ago."),
("story","Its fossil turned up in a coal mine, inside old swamp clay."),
("tease","But here's the catch. All they found was one tooth."),
("story","Plus a chip of another. That's it."),
("reveal","But that tooth is huge. More than twice the size of its closest Asian cousins."),
("serious","So they worked backward, from the tooth to the whole body."),
("serious","But they admit it's a ballpark. One tooth leaves a lot of guesswork."),
("hype","Still, it means giant rodents showed up way earlier than we thought."),
("friend","So next time a mouse runs by... be glad it's not that size.")]
SR=48000; parts=[]; lines=[]; t=0.0
for i,(tag,text) in enumerate(L):
    v,sp,g,pa=TAGS[tag]; a,sr=k.create(text,voice=VO[v],speed=sp*0.88,lang="en-us")
    idx=np.where(np.abs(a)>0.008)[0]; a=a[max(0,idx[0]-480):idx[-1]+960].astype(np.float32)
    fi,fo=int(.012*sr),int(.03*sr); a[:fi]*=np.linspace(0,1,fi); a[-fo:]*=np.linspace(1,0,fo); a*=10**(g/20)
    sf.write("/tmp/n.wav",a,sr); subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/tmp/n.wav","-af","aresample=48000:resampler=soxr,"+CHAIN,"-ar","48000","-ac","1","/tmp/n2.wav"],check=True)
    b=sf.read("/tmp/n2.wav",dtype="float32")[0]; lines.append(dict(i=i,tag=tag,text=text,start=round(t,3),dur=round(len(b)/SR,3)))
    parts+=[b,np.zeros(int(pa*SR),np.float32)]; t+=len(b)/SR+pa
sf.write("/home/claude/rodent/vo_raw.wav",np.concatenate(parts),SR)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/home/claude/rodent/vo_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","/home/claude/rodent/vo.wav"],check=True)
json.dump(lines,open("/home/claude/rodent/lines.json","w"),indent=1); print("dur",round(t,2))
