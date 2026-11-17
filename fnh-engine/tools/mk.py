import sys,numpy as np
from PIL import Image,ImageFilter,ImageEnhance
from rembg import remove,new_session
from scipy import ndimage
S=new_session('isnet-general-use')
def mk(src,out,crop=None,sat=1.25,keep=1.0,fill=True):
    im=Image.open(src).convert('RGB')
    if crop: im=im.crop(crop)
    a=remove(im,session=S); al=np.array(a)[:,:,3]>128
    lab,n=ndimage.label(al)
    if n>1:
        sz=ndimage.sum(al,lab,range(1,n+1)); ks=[i+1 for i,v in enumerate(sz) if v>=keep*max(sz)]; al=np.isin(lab,ks)
    if fill: al=ndimage.binary_fill_holes(al)
    rgb=ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(sat)).enhance(1.1)
    A=Image.fromarray((al*255).astype(np.uint8))
    bb=A.getbbox(); rgb=rgb.crop(bb); A=A.crop(bb)
    pad=40; W,H=rgb.size
    o=Image.new('RGBA',(W+2*pad,H+2*pad),(0,0,0,0))
    bp=Image.new('L',o.size,0); bp.paste(A.filter(ImageFilter.MaxFilter(25)),(pad,pad)); ol=bp.filter(ImageFilter.MaxFilter(7))
    o.paste((28,22,20,255),(0,0),ol); o.paste((255,248,231,255),(0,0),bp)
    s=Image.new('RGBA',(W,H)); s.paste(rgb.convert('RGBA'),(0,0)); s.putalpha(A); o.alpha_composite(s,(pad,pad))
    e=Image.new('L',o.size,0); e.paste(A.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3)),(pad,pad)); o.paste((28,22,20,255),(0,0),e)
    o.save(out); print(out,o.size)
if __name__=='__main__':
    mk(sys.argv[1],sys.argv[2],keep=float(sys.argv[3]) if len(sys.argv)>3 else 1.0)
