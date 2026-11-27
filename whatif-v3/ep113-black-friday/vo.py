import os, json, subprocess, numpy as np, soundfile as sf
os.chdir("/home/claude/tts")
from kokoro_onnx import Kokoro
k=Kokoro("kokoro.onnx","voices.npz"); VO=np.load("voices.npz")
# tag: voice, speed, gain dB, pause after
TAGS={"fast":("mix_michael_puck",1.1,0.5,0.1),"story":("mix_michael_puck",1.0,0,0.18),"excited":("hype",1.05,1,0.15),"deadpan":("calm",0.95,-1,0.22),
 "tease":("calm",0.97,-1.5,0.26),"reveal":("hype",1.02,1.5,0.2),"serious":("calm",0.97,0,0.2),"hype":("hype",1.05,1.5,0.18),
 "aside":("calm",1.05,-2.5,0.12),"friend":("mix_michael_puck",1.02,0,0.18),"punchline":("calm",0.93,1,0.3),"question":("mix_michael_puck",1.03,0.5,0.15),"count":("hype",1.0,1.5,0.5)}
CHAIN="highpass=f=80,lowpass=f=9500,equalizer=f=200:t=q:w=1:g=1.5,equalizer=f=6500:t=q:w=1.5:g=-4,deesser=i=0.6:m=0.5:f=0.5,afftdn=nf=-40,agate=threshold=0.012:ratio=6:attack=4:release=180:range=0.02,acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120:knee=4"
# PACKAGING (decided first): type = quip + tip (saves) | title "This Black Friday 'Deal' Cost $78 MORE" | cover "THIS 'DEAL' COST $78 MORE" = first line
SEED = "Groundwork Collaborative (16 Nov 2026, Keepa data, 351 Amazon BF/CM deals 2024-25): 29.1% same or higher than the month before, ~1 in 10 higher. Apple Watch S10 $602 -> $679.99 'sale' (BF 2025); UGG boots $98.40 -> $179.98 CM deal. Amazon: 'deeply flawed', its check 98% same/lower vs 30 days. EU requires lowest 30-day price; US no federal rule."
TEXT_HOOK = "THIS 'DEAL' COST $78 MORE"
HYPOTHESIS = "Packaging-first + reward in 0-4 s + a TIP (saves) on the day itself (Black Friday); new black/electric-yellow sale world with a price-history chart as hero visual."
PURPOSE = "Viewer learns that many Black Friday 'deals' aren't lower than last month and how to check price history in 30 seconds before buying."
L=[("hype","Last Black Friday, this deal cost seventy-eight dollars more than it did a month earlier.",0.1),
("story","A smartwatch. Six hundred and two dollars in October... then six seventy-nine on Black Friday, with a sale badge on it.",0.25),
("reveal","A watchdog group checked three hundred fifty Amazon deals. Almost one in three were no cheaper than the month before. Nearly one in ten cost more.",0.15),
("story","One pair of boots went from ninety-eight dollars... to a hundred and eighty, as a Cyber Monday deal.",0.2),
("story","Amazon says that study is flawed, and that its own check found almost every deal was a real low.",0.3),
("tease","So how do you know?",0.2),
("story","In Europe, stores have to show the lowest price from the last thirty days. In the US, they don't.",0.15),
("excited","So before you buy, paste the link into a free price tracker like Keepa or CamelCamelCamel, and look at the last thirty days.",0.25),
("punchline","If the line didn't drop... the deal is just a sticker.",0.3),
("punchline","Save this, and check before you tap buy.",0.0)]
SR=48000; parts=[]; lines=[]; t=0.0
for i,(tag,text,extra) in enumerate(L):
    v,sp,g,pa=TAGS[tag]; a,sr=k.create(text,voice=VO[v],speed=sp*0.92,lang="en-us")
    idx=np.where(np.abs(a)>0.008)[0]; a=a[max(0,idx[0]-480):idx[-1]+960].astype(np.float32)
    fi,fo=int(.012*sr),int(.03*sr); a[:fi]*=np.linspace(0,1,fi); a[-fo:]*=np.linspace(1,0,fo); a*=10**(g/20)
    sf.write("/tmp/n.wav",a,sr); subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/tmp/n.wav","-af","aresample=48000:resampler=soxr,"+CHAIN,"-ar","48000","-ac","1","/tmp/n2.wav"],check=True)
    b=sf.read("/tmp/n2.wav",dtype="float32")[0]; lines.append(dict(i=i,tag=tag,text=text,start=round(t,3),dur=round(len(b)/SR,3)))
    pa=pa*0.5+extra; parts+=[b,np.zeros(int(pa*SR),np.float32)]; t+=len(b)/SR+pa
sf.write("/home/claude/bf/vo_raw.wav",np.concatenate(parts),SR)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/home/claude/bf/vo_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","/home/claude/bf/vo.wav"],check=True)
json.dump(lines,open("/home/claude/bf/lines.json","w"),indent=1); print("dur",round(t,2))
