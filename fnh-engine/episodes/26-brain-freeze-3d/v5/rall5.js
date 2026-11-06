const {chromium}=require('playwright'); const fs=require('fs');
(async()=>{const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('http://127.0.0.1:8766/v5.html'); await p.waitForFunction('window.ready===true',{timeout:60000});
await p.evaluate(`window.setTL(${fs.readFileSync('tl4.json','utf8')})`);
const N=+process.argv[2]; fs.mkdirSync('frames5',{recursive:true});
for(let i=0;i<N;i++){await p.evaluate(`window.renderAt(${i/30})`); await p.screenshot({path:`frames5/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:93});}
await b.close();})();
