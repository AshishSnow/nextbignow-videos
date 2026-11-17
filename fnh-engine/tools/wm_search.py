import json,subprocess,time,urllib.parse,re,sys
from PIL import Image,ImageDraw
UA='FreshNestHubBot/1.0 (https://freshnesthub.com)'
out_dir=sys.argv[1]; pairs=[p.split('=',1) for p in sys.argv[2:]]
def get(u):
    for i in range(6):
        r=subprocess.run(['curl','-s','-m','30','-A',UA,u],capture_output=True)
        try: return json.loads(r.stdout)
        except: time.sleep(20)
out={}
for key,q in pairs:
    u='https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrnamespace=6&gsrlimit=8&gsrsearch='+urllib.parse.quote(q+' filetype:bitmap')+'&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=960'
    d=get(u); res=[]
    for p in (d or {}).get('query',{}).get('pages',{}).values():
        ii=p['imageinfo'][0]; m=ii.get('extmetadata',{})
        res.append(dict(t=p['title'],u=re.sub(r'\?.*$','',ii.get('thumburl') or '').replace('thumb.wikimedia.org','upload.wikimedia.org'),a=re.sub('<[^>]+>','',m.get('Artist',{}).get('value',''))[:60],l=m.get('LicenseShortName',{}).get('value','')))
    out[key]=res; print(key,len(res),flush=True); time.sleep(8)
    json.dump(out,open(out_dir+'/cands.json','w'),indent=1)
for k,v in out.items():
    for i,c in enumerate(v[:8]):
        f=f'{out_dir}/{k}_{i}.jpg'
        for t in range(3):
            r=subprocess.run(['curl','-s','-m','30','-A',UA,'-o',f,'-w','%{http_code}',c['u']],capture_output=True,text=True)
            if r.stdout=='200': break
            time.sleep(10)
        time.sleep(3)
    print('dl',k,flush=True)
ks=list(out); S=Image.new('RGB',(2000,260*len(ks)),'white'); dr=ImageDraw.Draw(S)
for r,k in enumerate(ks):
    for i in range(8):
        try: im=Image.open(f'{out_dir}/{k}_{i}.jpg').convert('RGB'); im.thumbnail((240,240)); S.paste(im,(i*250,r*260))
        except: pass
        dr.text((i*250+4,r*260+244),f'{k}{i}',fill='red')
S.save(out_dir+'/all.jpg'); print('ALLDONE',flush=True)
