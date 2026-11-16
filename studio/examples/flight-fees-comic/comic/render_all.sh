cd /home/claude/studio/projects/flight-fees/comic
for P in ig yt; do
  OMB_PLAT=$P python3 render_ff.py range 0 1016 ff/${P}_1.mp4 > ff/r_${P}1.log 2>&1 &
  OMB_PLAT=$P python3 render_ff.py range 1016 2033 ff/${P}_2.mp4 > ff/r_${P}2.log 2>&1
  wait
  printf "file '${P}_1.mp4'\nfile '${P}_2.mp4'\n" > ff/parts_$P.txt
  ffmpeg -v error -y -f concat -safe 0 -i ff/parts_$P.txt -i ff/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart ff/flight_fees_$P.mp4
  ls -la ff/flight_fees_$P.mp4
done
grep -c Traceback ff/r_*.log; echo DONE
