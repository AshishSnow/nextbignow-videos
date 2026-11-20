set -e
cd /home/claude/studio/projects/grocery-ads
N=1805; Q=452
for i in 0 1 2 3; do a=$((i*Q)); b=$(( (i+1)*Q )); [ $b -gt $N ] && b=$N; python3 render_grocery.py range $a $b > work/r$i.log 2>&1 & done
wait
for v in ig yt; do ls out/${v}_0*.mp4 | sort | sed "s/^/file '/;s/$/'/" | sed "s#file '#file '$PWD/#" > work/$v.txt
ffmpeg -v error -y -f concat -safe 0 -i work/$v.txt -c copy work/${v}_cat.mp4; done
mkdir -p final
for v in ig yt; do
 if [ $v = yt ]; then IN="-i work/yt_cat.mp4 -loop 1 -t 0.2 -i thumbnail_grocery.png"; FC="[1:v]scale=1080:1920,setsar=1,fps=30[t];[0:v][t]overlay=eof_action=pass:enable='lt(t,0.2)'[v]"; else IN="-i work/ig_cat.mp4"; FC="[0:v]null[v]"; fi
 for p in 1 2; do
  if [ $p = 1 ]; then ffmpeg -v error -y $IN -filter_complex "$FC" -map "[v]" -c:v libx264 -b:v 9000k -preset slow -pass 1 -passlogfile work/p_$v -an -f mp4 /dev/null
  else ffmpeg -v error -y $IN -i mix.wav -filter_complex "$FC" -map "[v]" -map $([ $v = yt ] && echo 2 || echo 1):a -c:v libx264 -b:v 9000k -preset slow -pass 2 -passlogfile work/p_$v -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart final/grocery_$v.mp4; fi
 done
done
ls -la final
