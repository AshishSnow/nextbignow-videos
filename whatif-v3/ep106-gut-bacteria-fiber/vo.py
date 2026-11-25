import os, json, subprocess, numpy as np, soundfile as sf
os.chdir("/home/claude/tts")
from kokoro_onnx import Kokoro
k=Kokoro("kokoro.onnx","voices.npz"); VO=np.load("voices.npz")
# tag: voice, speed, gain dB, pause after
TAGS={"story":("mix_michael_puck",1.0,0,0.18),"excited":("hype",1.05,1,0.15),"deadpan":("calm",0.95,-1,0.22),
 "tease":("calm",0.97,-1.5,0.26),"reveal":("hype",1.02,1.5,0.2),"serious":("calm",0.97,0,0.2),"hype":("hype",1.05,1.5,0.18),
 "aside":("calm",1.05,-2.5,0.12),"friend":("mix_michael_puck",1.02,0,0.18),"punchline":("calm",0.93,1,0.3),"question":("mix_michael_puck",1.03,0.5,0.15),"count":("hype",1.0,1.5,0.5)}
CHAIN="highpass=f=80,lowpass=f=9500,equalizer=f=200:t=q:w=1:g=1.5,equalizer=f=6500:t=q:w=1.5:g=-4,deesser=i=0.6:m=0.5:f=0.5,afftdn=nf=-40,agate=threshold=0.012:ratio=6:attack=4:release=180:range=0.02,acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120:knee=4"
SEED = "Skip fiber and your gut bacteria may start eating the slimy shield that lines your gut."
TEXT_HOOK = "YOUR GUT IS ON THE MENU"
HYPOTHESIS = "Length brick: 30-35 s / ~90 words with a mid-video 'tag the friend' line (vs 43-46 s, CTA only at end) -> higher avg watch % and shares > 0 at a similar 3s rate."
PURPOSE = "Viewer learns that in mouse studies, low fiber pushed gut bacteria to eat the protective mucus lining and make harmful compounds, while fiber and indigestible plant proteins helped; early research."
L=[("hype","Skip your veggies, and your gut bacteria might start eating... you."),
("tease","Not your food. Your gut's slimy protective lining."),
("story","Here's why. Bacteria love fiber. It's their favorite meal."),
("serious","But when fiber runs out, they turn to the mucus that guards your gut."),
("reveal","And chewing it up makes chemicals linked to harm."),
("friend","Tag the friend who hasn't eaten a vegetable all week."),
("reveal","Twist: plants also pack proteins you can't digest. Those make bacteria pump out helpful chemicals."),
("serious","This was mostly in mice, so it's early."),
("punchline","But feed your bacteria fiber... or they might feed on you.")]
SR=48000; parts=[]; lines=[]; t=0.0
for i,(tag,text) in enumerate(L):
    v,sp,g,pa=TAGS[tag]; a,sr=k.create(text,voice=VO[v],speed=sp*0.88,lang="en-us")
    idx=np.where(np.abs(a)>0.008)[0]; a=a[max(0,idx[0]-480):idx[-1]+960].astype(np.float32)
    fi,fo=int(.012*sr),int(.03*sr); a[:fi]*=np.linspace(0,1,fi); a[-fo:]*=np.linspace(1,0,fo); a*=10**(g/20)
    sf.write("/tmp/n.wav",a,sr); subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/tmp/n.wav","-af","aresample=48000:resampler=soxr,"+CHAIN,"-ar","48000","-ac","1","/tmp/n2.wav"],check=True)
    b=sf.read("/tmp/n2.wav",dtype="float32")[0]; lines.append(dict(i=i,tag=tag,text=text,start=round(t,3),dur=round(len(b)/SR,3)))
    parts+=[b,np.zeros(int(pa*SR),np.float32)]; t+=len(b)/SR+pa
sf.write("/home/claude/gut/vo_raw.wav",np.concatenate(parts),SR)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/home/claude/gut/vo_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","/home/claude/gut/vo.wav"],check=True)
json.dump(lines,open("/home/claude/gut/lines.json","w"),indent=1); print("dur",round(t,2))
