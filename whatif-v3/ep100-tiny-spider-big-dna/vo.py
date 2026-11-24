import os, json, subprocess, numpy as np, soundfile as sf
os.chdir("/home/claude/tts")
from kokoro_onnx import Kokoro
k=Kokoro("kokoro.onnx","voices.npz"); VO=np.load("voices.npz")
# tag: voice, speed, gain dB, pause after
TAGS={"story":("mix_michael_puck",1.0,0,0.18),"excited":("hype",1.05,1,0.15),"deadpan":("calm",0.95,-1,0.22),
 "tease":("calm",0.97,-1.5,0.26),"reveal":("hype",1.02,1.5,0.2),"serious":("calm",0.97,0,0.2),"hype":("hype",1.05,1.5,0.18),
 "aside":("calm",1.05,-2.5,0.12),"friend":("mix_michael_puck",1.02,0,0.18),"punchline":("calm",0.93,1,0.3),"question":("mix_michael_puck",1.03,0.5,0.15),"count":("hype",1.0,1.5,0.5)}
CHAIN="highpass=f=80,lowpass=f=9500,equalizer=f=200:t=q:w=1:g=1.5,equalizer=f=6500:t=q:w=1.5:g=-4,deesser=i=0.6:m=0.5:f=0.5,afftdn=nf=-40,agate=threshold=0.012:ratio=6:attack=4:release=180:range=0.02,acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120:knee=4"
SEED = "A spider that fits on a quarter has 50% more DNA than you, and most of it is copy-paste repeats."
TEXT_HOOK = "IT BEATS YOUR GENOME BY 50%"
HYPOTHESIS = "Text hook brick: a number/stake the voice does not say (vs plain topic label on ep97) -> expect 3s view rate >= 70%."
PURPOSE = "Viewer leaves knowing DNA size does not equal complexity (and that this spider needs protecting)."
L=[("hype","This spider fits on a quarter. But its DNA beats yours."),
("tease","Not a little bigger. About fifty percent bigger."),
("story","It's a trapdoor spider from the sand dunes of California."),
("story","It hides under a tiny trapdoor and waits for dinner."),
("serious","So scientists read its genome. Four point six billion letters."),
("tease","Yours? About three billion."),
("reveal","But here's the twist. Over three quarters of it is repeats, copied again and again."),
("serious","So more DNA doesn't mean more genes. Or a fancier animal."),
("story","And it needs help. Rising seas and fires threaten the only dunes it lives on."),
("friend","So next time you spot a tiny spider... its DNA might beat yours.")]
SR=48000; parts=[]; lines=[]; t=0.0
for i,(tag,text) in enumerate(L):
    v,sp,g,pa=TAGS[tag]; a,sr=k.create(text,voice=VO[v],speed=sp*0.88,lang="en-us")
    idx=np.where(np.abs(a)>0.008)[0]; a=a[max(0,idx[0]-480):idx[-1]+960].astype(np.float32)
    fi,fo=int(.012*sr),int(.03*sr); a[:fi]*=np.linspace(0,1,fi); a[-fo:]*=np.linspace(1,0,fo); a*=10**(g/20)
    sf.write("/tmp/n.wav",a,sr); subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/tmp/n.wav","-af","aresample=48000:resampler=soxr,"+CHAIN,"-ar","48000","-ac","1","/tmp/n2.wav"],check=True)
    b=sf.read("/tmp/n2.wav",dtype="float32")[0]; lines.append(dict(i=i,tag=tag,text=text,start=round(t,3),dur=round(len(b)/SR,3)))
    parts+=[b,np.zeros(int(pa*SR),np.float32)]; t+=len(b)/SR+pa
sf.write("/home/claude/spider/vo_raw.wav",np.concatenate(parts),SR)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/home/claude/spider/vo_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","/home/claude/spider/vo.wav"],check=True)
json.dump(lines,open("/home/claude/spider/lines.json","w"),indent=1); print("dur",round(t,2))
