cd /home/claude/studio/projects/lego-comeback/comic
for P in ig yt; do
  OMB_PLAT=$P python3 render_lg.py range 0 844 lg/${P}_1.mp4 > lg/r_${P}1.log 2>&1 &
  OMB_PLAT=$P python3 render_lg.py range 844 1688 lg/${P}_2.mp4 > lg/r_${P}2.log 2>&1
  wait
  printf "file '${P}_1.mp4'\nfile '${P}_2.mp4'\n" > lg/parts_$P.txt
  ffmpeg -v error -y -f concat -safe 0 -i lg/parts_$P.txt -i lg/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart lg/lego_comeback_$P.mp4
  ls -la lg/lego_comeback_$P.mp4
done
grep -c Traceback lg/r_*.log; echo DONE
