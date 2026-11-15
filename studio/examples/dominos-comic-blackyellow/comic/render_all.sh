cd /home/claude/studio/projects/dominos-comic/comic
for P in ig yt; do
  OMB_PLAT=$P python3 render_dc.py range 0 1042 dc/${P}_1.mp4 > dc/r_${P}1.log 2>&1 &
  OMB_PLAT=$P python3 render_dc.py range 1042 2084 dc/${P}_2.mp4 > dc/r_${P}2.log 2>&1
  wait
  printf "file '${P}_1.mp4'\nfile '${P}_2.mp4'\n" > dc/parts_$P.txt
  ffmpeg -v error -y -f concat -safe 0 -i dc/parts_$P.txt -i dc/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart dc/dominos_$P.mp4
  ls -la dc/dominos_$P.mp4
done
grep -c Traceback dc/r_*.log; echo DONE
