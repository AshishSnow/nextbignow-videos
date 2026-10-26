import sys, cv2, numpy as np, glob
out=sys.argv[1]; files=sys.argv[2:]
ims=[]
for fn in files:
    im=cv2.imread(fn); h,w=im.shape[:2]
    ov=im.copy()
    cv2.rectangle(ov,(60,250),(w-120,h-420),(0,255,255),4)
    im=cv2.addWeighted(ov,0.7,im,0.3,0)
    cv2.putText(im,fn.split('/')[-1],(70,240),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),5)
    ims.append(cv2.resize(im,(360,640)))
while len(ims)%4: ims.append(np.zeros_like(ims[0]))
rows=[np.hstack(ims[i:i+4]) for i in range(0,len(ims),4)]
cv2.imwrite(out,np.vstack(rows))
