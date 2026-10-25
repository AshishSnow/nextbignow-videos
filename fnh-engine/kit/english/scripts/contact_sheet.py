import sys, subprocess, numpy as np, cv2
src, out, step = sys.argv[1], sys.argv[2], float(sys.argv[3])
d = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src],capture_output=True,text=True).stdout)
ims=[]
t=0.0
while t < d - 0.05:
    p = subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.3f}","-i",src,"-frames:v","1","-f","rawvideo","-pix_fmt","bgr24","-s","216x384","-"],capture_output=True)
    im = np.frombuffer(p.stdout,np.uint8).reshape(384,216,3).copy()
    cv2.putText(im,f"{t:.1f}",(4,18),0,0.55,(0,0,255),2); ims.append(im); t+=step
while len(ims)%10: ims.append(np.zeros_like(ims[0]))
cv2.imwrite(out, np.vstack([np.hstack(ims[i:i+10]) for i in range(0,len(ims),10)]))
