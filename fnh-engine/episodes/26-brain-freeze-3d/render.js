const {chromium}=require('playwright'); const fs=require('fs');
const [off,step,N,out]=[+process.argv[2],+process.argv[3],+process.argv[4],process.argv[5]];
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1080,height:1920}}); p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('http://127.0.0.1:8765/scene.html'); await p.waitForFunction('window.ready===true',{timeout:120000});
await p.evaluate(`window.setTL(${fs.readFileSync('tl.json','utf8')})`);
for(let i=off;i<N;i+=step){const f=`${out}/f${String(i).padStart(5,'0')}.jpg`; if(fs.existsSync(f)) continue;
 await p.evaluate(`window.renderAt(${i/30})`); await p.screenshot({path:f+'.tmp.jpg',type:'jpeg',quality:93}); fs.renameSync(f+'.tmp.jpg',f);
 if(i%60<step) console.log('frame',i,new Date().toISOString());}
await b.close();})();
