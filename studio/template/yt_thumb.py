"""yt_thumb.py <photo> <line1> <line2> <tag> <out.png>  -- 1280x720 YouTube thumbnail, OMB purple look"""
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
photo,l1,l2,tag,out=sys.argv[1:6]; W,H=1280,720
y,x=np.mgrid[0:H,0:W]; d=np.sqrt(((x-860)/W)**2+((y-330)/H)**2); t=np.clip(d/0.75,0,1)[...,None]
bg=Image.fromarray((np.array([150,70,220])*(1-t)+np.array([28,10,56])*t).astype(np.uint8)).convert('RGBA')
ph=ImageOps.expand(ImageOps.fit(Image.open(photo).convert('RGB'),(520,420)),14,fill=(250,248,242)).convert('RGBA').rotate(-5,expand=True,resample=Image.BICUBIC)
sh=Image.new('RGBA',ph.size,(0,0,0,0)); sh.putalpha(ph.split()[-1].point(lambda a:150 if a else 0)); sh=sh.filter(ImageFilter.GaussianBlur(18))
bg.alpha_composite(sh,(700,190)); bg.alpha_composite(ph,(680,165))
dr=ImageDraw.Draw(bg); FD='/home/claude/studio/fonts/doc/'
def fit(s,maxw,size):
    while ImageFont.truetype(FD+'ArchivoCond-Black.ttf',size).getlength(s)>maxw: size-=4
    return ImageFont.truetype(FD+'ArchivoCond-Black.ttf',size)
F1=fit(l1,660,150); F2=fit(l2,660,150)
dr.text((66,158),l1,font=F1,fill=(20,8,40)); dr.text((60,150),l1,font=F1,fill=(255,248,235))
b=dr.textbbox((60,330),l2,font=F2); dr.rectangle((b[0]-18,b[1]-14,b[2]+18,b[3]+18),fill=(232,70,60)); dr.text((60,330),l2,font=F2,fill=(255,214,64))
g=ImageFont.truetype(FD+'Archivo-Bold.ttf',34); bb=dr.textbbox((80,566),tag,font=g)
dr.rounded_rectangle((60,558,bb[2]+20,614),10,fill=(160,92,240)); dr.text((80,566),tag,font=g,fill=(255,255,255))
dr.ellipse((1150,26,1250,126),fill=(20,16,24),outline=(250,248,242),width=4)
dr.text((1170,38),'O.',font=ImageFont.truetype(FD+'ArchivoCond-Black.ttf',66),fill=(250,248,242))
bg.convert('RGB').save(out)
