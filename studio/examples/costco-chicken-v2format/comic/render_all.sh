cd /home/claude/studio/projects/costco-chicken/comic
for P in ig yt; do
  OMB_PLAT=$P python3 render_cc.py range 0 896 cc/${P}_1.mp4 > cc/r_${P}1.log 2>&1 &
  OMB_PLAT=$P python3 render_cc.py range 896 1793 cc/${P}_2.mp4 > cc/r_${P}2.log 2>&1
  wait
  printf "file '${P}_1.mp4'\nfile '${P}_2.mp4'\n" > cc/parts_$P.txt
  ffmpeg -v error -y -f concat -safe 0 -i cc/parts_$P.txt -i cc/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart cc/costco_chicken_$P.mp4
  ls -la cc/costco_chicken_$P.mp4
done
grep -c Traceback cc/r_*.log; echo DONE
