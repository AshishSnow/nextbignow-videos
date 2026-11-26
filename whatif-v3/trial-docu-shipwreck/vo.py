import os, json, subprocess, numpy as np, soundfile as sf
os.chdir("/home/claude/tts")
from kokoro_onnx import Kokoro
k=Kokoro("kokoro.onnx","voices.npz"); VO=np.load("voices.npz")
# tag: voice, speed, gain dB, pause after
TAGS={"story":("mix_michael_puck",1.0,0,0.18),"excited":("hype",1.05,1,0.15),"deadpan":("calm",0.95,-1,0.22),
 "tease":("calm",0.97,-1.5,0.26),"reveal":("hype",1.02,1.5,0.2),"serious":("calm",0.97,0,0.2),"hype":("hype",1.05,1.5,0.18),
 "aside":("calm",1.05,-2.5,0.12),"friend":("mix_michael_puck",1.02,0,0.18),"punchline":("calm",0.93,1,0.3),"question":("mix_michael_puck",1.03,0.5,0.15),"count":("hype",1.0,1.5,0.5)}
CHAIN="highpass=f=80,lowpass=f=9500,equalizer=f=200:t=q:w=1:g=1.5,equalizer=f=6500:t=q:w=1.5:g=-4,deesser=i=0.6:m=0.5:f=0.5,afftdn=nf=-40,agate=threshold=0.012:ratio=6:attack=4:release=180:range=0.02,acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120:knee=4"
SEED = "A ship that sank 2,200 years ago still carries its 'repair receipts': pollen trapped in each coat of pine tar hints at where it was worked on."
TEXT_HOOK = "WHERE HAS THIS SHIP BEEN?"
HYPOTHESIS = "Docu v6: open loop (receipt with ??? in the hook, filled in at the reveal), one consistent metaphor (receipts) end to end, condensed + serif-italic type system."
PURPOSE = "Viewer learns that pollen trapped in 4-5 batches of pine-tar coating on a 2,200-year-old wreck off Croatia suggests work near Italy and near Croatia; exact spots unknown."
L=[("hype","This ship sank twenty-two hundred years ago... but it never threw out its receipts."),
("story","It's basically a car that kept every service receipt."),
("tease","Except these receipts are glued to the hull."),
("story","Every time it got fixed, workers slapped on hot pine tar."),
("reveal","And while it was sticky, it grabbed whatever was in the air... pollen from the trees nearby."),
("serious","So every coat is a receipt... with an address on it."),
("aside","Twenty-two hundred years later,"),
("story","scientists scraped off ten samples and found four or five coats."),
("reveal","Some from near Italy. Some from the coast of Croatia."),
("punchline","Same ship. Different repair shops."),
("friend","Tag the friend who never services their car."),
("punchline","The ship never made it home... but its receipts did.")]
SR=48000; parts=[]; lines=[]; t=0.0
for i,(tag,text) in enumerate(L):
    v,sp,g,pa=TAGS[tag]; a,sr=k.create(text,voice=VO[v],speed=sp*0.97,lang="en-us")
    idx=np.where(np.abs(a)>0.008)[0]; a=a[max(0,idx[0]-480):idx[-1]+960].astype(np.float32)
    fi,fo=int(.012*sr),int(.03*sr); a[:fi]*=np.linspace(0,1,fi); a[-fo:]*=np.linspace(1,0,fo); a*=10**(g/20)
    sf.write("/tmp/n.wav",a,sr); subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/tmp/n.wav","-af","aresample=48000:resampler=soxr,"+CHAIN,"-ar","48000","-ac","1","/tmp/n2.wav"],check=True)
    b=sf.read("/tmp/n2.wav",dtype="float32")[0]; lines.append(dict(i=i,tag=tag,text=text,start=round(t,3),dur=round(len(b)/SR,3)))
    pa=pa*0.45; parts+=[b,np.zeros(int(pa*SR),np.float32)]; t+=len(b)/SR+pa
sf.write("/home/claude/docu/vo_raw.wav",np.concatenate(parts),SR)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/home/claude/docu/vo_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","/home/claude/docu/vo.wav"],check=True)
json.dump(lines,open("/home/claude/docu/lines.json","w"),indent=1); print("dur",round(t,2))
