// ===== Kid v2: appealing cartoon character with hands, shading, real expressions =====
const SK='#ffd6b0', SKD='#f0b27f', HAIR='#3a2418', HAIRH='#6e4630', HOOD='#2ec4a6', HOODD='#1f9a83', OUT='#1a1530';
function hand(x,y,s,rot,k,pose='grip'){G(`translate(${x} ${y}) rotate(${rot}) scale(${s})`,()=>{
  if(pose=='grip'){ // fingers wrapped (seen from front)
    shape('M-50 -30 Q-58 30 -20 46 L40 46 Q62 30 56 -20 Q40 -50 0 -48 Q-36 -50 -50 -30Z',SK,k,OUT,8);
    for(const fx of [-28,-6,16,36]) S(`M${fx} -40 q4 30 0 70`,k,SKD,6);
    shape('M-56 -20 Q-86 -30 -82 4 Q-74 22 -46 12Z',SK,k,OUT,8);}
  else { // palm flat (on forehead)
    shape('M-60 -10 Q-70 50 -20 60 L50 54 Q80 40 70 0 L66 -70 Q60 -86 50 -70 L46 -20 L40 -88 Q32 -104 22 -88 L20 -24 L10 -92 Q0 -106 -10 -90 L-8 -20 L-24 -76 Q-34 -90 -42 -74 Z',SK,k,OUT,8);}
});}
function sleeve(x1,y1,x2,y2,k,w=70){const a=Math.atan2(y2-y1,x2-x1),n=[-Math.sin(a),Math.cos(a)];
  const d=`M${x1+n[0]*w/2} ${y1+n[1]*w/2} L${x2+n[0]*w*0.36} ${y2+n[1]*w*0.36} L${x2-n[0]*w*0.36} ${y2-n[1]*w*0.36} L${x1-n[0]*w/2} ${y1-n[1]*w/2}Z`;shape(d,HOOD,k,OUT,8);
  Fi(`M${x2+n[0]*w*0.4} ${y2+n[1]*w*0.4} L${x2-n[0]*w*0.4} ${y2-n[1]*w*0.4}`,'none',1);S(`M${x2+n[0]*w*0.4} ${y2+n[1]*w*0.4} L${x2-n[0]*w*0.4} ${y2-n[1]*w*0.4}`,k,OUT,12);}
function kid2(x,y,s,k,st){ // st: eyes, mouth, pose('cone'|'pain'|'none'|'lick'), pain, t, look
  const t=st.t||0, br=Math.sin(t*3)*4;
  G(`translate(${x} ${y+br}) scale(${s})`,()=>{
    // body / hoodie
    shape('M-230 470 Q-240 330 -150 300 Q0 270 150 300 Q240 330 230 470Z',HOOD,k,OUT,9);
    Fi('M60 300 Q170 310 230 470 L120 470 Q120 360 60 300Z',HOODD,cl(k*2-1));
    S('M-40 300 q-6 60 -14 90 M40 300 q6 60 14 90',k,'#e8fff8',7); o+=`<circle cx="-54" cy="392" r="8" fill="#e8fff8" opacity="${k}"/><circle cx="54" cy="392" r="8" fill="#e8fff8" opacity="${k}"/>`;
    shape('M-70 230 L-62 300 Q0 324 62 300 L70 230Z',SK,k,OUT,8); Fi('M20 240 L62 300 L70 236Z',SKD,cl(k*2-1));
    // ears
    shape(circ(-196,10,34,46,10),SK,k,OUT,8); shape(circ(196,10,34,46,10),SK,k,OUT,8); S('M-200 -6 q-14 16 0 34 M200 -6 q14 16 0 34',k,SKD,6);
    // head with jaw
    const hd=cr([[0,-230],[140,-200],[205,-90],[208,40],[170,150],[90,225],[0,245],[-90,225],[-170,150],[-208,40],[-205,-90],[-140,-200]],true);
    shape(hd,SK,k,OUT,9);
    Fi(cr([[150,-160],[205,-70],[208,40],[172,148],[100,218],[150,120],[178,10],[172,-90]],true),SKD,cl(k*2-1)*0.75);
    // pain glow on forehead
    if(st.pain>0){const pd=circ(0,-120,150,62,18);Fi(pd,'#ff4d4d',st.pain*(0.35+0.25*Math.sin(t*16)));
      S('M-70 -170 l22 26 l-12 18 l26 20 M50 -175 l-18 24 l16 18 l-12 22',st.pain,'#c1121f',9);}
    // hair: big swoosh with spikes + highlight
    shape('M-214 -40 Q-236 -200 -110 -262 Q10 -310 140 -258 Q228 -214 214 -60 Q196 -130 150 -150 Q170 -200 110 -214 Q120 -170 70 -170 Q60 -230 0 -226 Q10 -180 -40 -176 Q-60 -220 -110 -212 Q-90 -170 -140 -150 Q-190 -120 -214 -40Z',HAIR,k,OUT,9);
    S('M-120 -230 Q-40 -270 60 -250',k,HAIRH,10); S('M100 -232 q40 10 60 40',k,HAIRH,8);
    // cheeks
    Fi(circ(-120,90,44,26,10),'#ff8fa3',cl(k*2-1)*0.75); Fi(circ(120,90,44,26,10),'#ff8fa3',cl(k*2-1)*0.75);
    // brows
    const e=st.eyes;
    const bro=e=='squeeze'?[[-150,-80,-40,-50],[40,-50,150,-80]]:e=='wide'||e=='shock'?[[-150,-118,-50,-128],[50,-128,150,-118]]:e=='happy'?[[-150,-98,-50,-108],[50,-108,150,-98]]:[[-150,-92,-50,-100],[50,-100,150,-92]];
    for(const[a,b,c,d] of bro) S(`M${a} ${b} Q${(a+c)/2} ${Math.min(b,d)-14} ${c} ${d}`,k,HAIR,18);
    // eyes
    for(const ex of [-90,90]){
      if(e=='squeeze'){S(`M${ex-46} -48 L${ex+ (ex<0?14:-14)} -20 L${ex-46+92-0} 8`.replace(/L\S+ -20 L\S+ 8/, (ex<0?`L${ex+30} -22 L${ex-46} 4`:`L${ex-30} -22 L${ex+46} 4`)).replace(`M${ex-46}`,ex<0?`M${ex-46}`:`M${ex+46}`),k,OUT,12);}
      else if(e=='happy'||(e=='wink'&&ex>0)){S(`M${ex-44} -14 Q${ex} -62 ${ex+44} -14`,k,OUT,12);}
      else{const rx=e=='wide'||e=='shock'?54:48, ry=e=='wide'||e=='shock'?62:54;
        shape(circ(ex,-30,rx,ry,16),'#fff',k,OUT,8);
        if(k>0.6){const lx=(st.look||0)*12;const ir=e=='shock'?14:30;
          o+=`<circle cx="${ex+lx}" cy="-24" r="${ir}" fill="#7a4a22"/><circle cx="${ex+lx}" cy="-24" r="${ir*0.55}" fill="#140c08"/><circle cx="${ex+lx+ir*0.35}" cy="${-24-ir*0.4}" r="${ir*0.32}" fill="#fff"/><circle cx="${ex+lx-ir*0.35}" cy="${-24+ir*0.35}" r="${ir*0.14}" fill="#fff"/>`;
          if(e!='wide'&&e!='shock') S(`M${ex-rx} -48 Q${ex} ${-30-ry-10} ${ex+rx} -48`,1,OUT,10);}}}
    // nose
    S('M-8 34 Q-26 66 4 74',k,'#c98a5e',9);
    // mouth
    const m=st.mouth;
    if(m=='bite'){shape(cr([[-90,120],[0,100],[90,120],[70,200],[0,226],[-70,200]],true),'#5c1325',k,OUT,9);Fi('M-80 118 Q0 98 80 118 L76 140 Q0 122 -76 140Z','#fff',cl(k*2-1));Fi(cr([[-46,196],[0,170],[46,196],[0,222]],true),'#ff6b81',cl(k*2-1));}
    else if(m=='grimace'){shape('M-96 140 Q0 118 96 140 L90 196 Q0 214 -90 196Z','#fff',k,OUT,9);for(const gx of [-60,-30,0,30,60])S(`M${gx} 128 V204`,k,'#c9c3d6',5);S('M-94 168 Q0 158 94 168',k,'#c9c3d6',5);}
    else if(m=='o'){shape(circ(0,170,38,48,12),'#5c1325',k,OUT,9);}
    else if(m=='lick'){S('M-70 140 Q0 196 70 140',k,OUT,11);shape('M-22 166 Q0 236 34 168Z','#ff6b81',k,OUT,7);}
    else {shape('M-84 128 Q0 230 84 128 Q0 158 -84 128Z','#5c1325',k,OUT,9);Fi('M-70 134 Q0 156 70 134 L64 146 Q0 166 -64 146Z','#fff',cl(k*2-1));}
    // arms + hands by pose
    if(st.pose=='cone'){sleeve(150,320,250,170,k);hand(250,150,1,-10,k,'grip');}
    else if(st.pose=='pain'){sleeve(-150,320,-150,-60,k);sleeve(150,320,150,-60,k);hand(-110,-150,1,-20,k,'palm');hand(110,-150,1,20,k,'palm');}
    else if(st.pose=='lick'){sleeve(150,320,200,200,k);hand(200,180,1,-6,k,'grip');}
  });}
