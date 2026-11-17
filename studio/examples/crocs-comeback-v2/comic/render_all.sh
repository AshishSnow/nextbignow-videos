cd /home/claude/studio/projects/crocs-comeback/comic
for P in ig yt; do
  OMB_PLAT=$P python3 render_cr.py range 0 783 cr/${P}_1.mp4 > cr/r_${P}1.log 2>&1 &
  OMB_PLAT=$P python3 render_cr.py range 783 1566 cr/${P}_2.mp4 > cr/r_${P}2.log 2>&1
  wait
  printf "file '${P}_1.mp4'\nfile '${P}_2.mp4'\n" > cr/parts_$P.txt
  ffmpeg -v error -y -f concat -safe 0 -i cr/parts_$P.txt -i cr/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart cr/crocs_comeback_$P.mp4
  ls -la cr/crocs_comeback_$P.mp4
done
grep -c Traceback cr/r_*.log; echo DONE
