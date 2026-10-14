// FXMM education video engine (canvas). Larger labels for mobile.
const C=document.getElementById('c'),X=C.getContext('2d');
const IM={};function load(n,src){return new Promise(r=>{const i=new Image();i.onload=()=>{IM[n]=i;r()};i.onerror=()=>r();i.src=src})}
window.ready=Promise.all([load('plate','plate.png'),load('card','card01.png'),load('logo','logo_big.png'),load('plate0','plate0.png'),
 ...['300','400','500','600','700'].map(w=>document.fonts.load(w+' 20px P')),document.fonts.load('500 20px M'),document.fonts.load('700 20px M')]);
const cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)), ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
const ramp=(t,a,d=.35)=>ease(cl((t-a)/d));
function lerpK(t,K){for(let i=1;i<K.length;i++){if(t<K[i][0]){const A=K[i-1],B=K[i],u=ease(cl((t-A[0])/(B[0]-A[0])));const r=A.slice(1).map((v,j)=>v+(B[j+1]-v)*u);return r.length>1?r:r[0]}}const r=K[K.length-1].slice(1);return r.length>1?r:r[0]}
const BEAR='rgb(124,138,163)',BULLB='rgb(232,237,246)',BULLF='rgb(11,19,37)',BLUE='rgb(88,152,225)',TAG='rgb(91,165,252)',BLUE_T='rgb(98,165,244)';
const PX0=120,PX1=1600,PY0=150,PY1=900;
let PMIN=1.085,PMAX=1.101;const Y=p=>PY0+(PMAX-p)/(PMAX-PMIN)*(PY1-PY0);
function view(a,b){PMIN=a;PMAX=b}
function rr(x,y,w,h,r){X.beginPath();X.moveTo(x+r,y);X.arcTo(x+w,y,x+w,y+h,r);X.arcTo(x+w,y+h,x,y+h,r);X.arcTo(x,y+h,x,y,r);X.arcTo(x,y,x+w,y,r);X.closePath()}
function background(tf){X.drawImage(IM.plate,0,0);if(tf){X.font='300 26px P';X.fillStyle='rgb(160,170,190)';X.textBaseline='middle';X.textAlign='left';X.fillText('Illustrative example · EUR/USD · '+tf,120,80)}}
function grid(){const step=(PMAX-PMIN)>0.008?0.002:0.001;X.font='500 21px M';X.textBaseline='middle';X.textAlign='left';
 for(let p=Math.ceil(PMIN/step)*step;p<=PMAX+1e-9;p+=step){const y=Y(p);if(y<PY0-5||y>PY1+5)continue;X.strokeStyle='rgba(255,255,255,.045)';X.lineWidth=1;X.beginPath();X.moveTo(PX0,y);X.lineTo(PX1,y);X.stroke();X.fillStyle='rgb(100,112,136)';X.fillText(p.toFixed(4),1625,y)}}
function seeded(s){return()=>{s=(s*9301+49297)%233280;return s/233280}}
function series(K,seed){const r=seeded(seed);const N=K[K.length-1][0];const out=[];let o=K[0][1];
 for(let i=0;i<=N;i++){let j=1;while(K[j][0]<i)j++;const A=K[j-1],B=K[j],u=(i-A[0])/Math.max(1,B[0]-A[0]);const base=A[1]+(B[1]-A[1])*u;
  const c=base+(r()-.5)*0.00055;const h=Math.max(o,c)+r()*0.00022,l=Math.min(o,c)-r()*0.00022;out.push({o,c,h,l});o=c}return out}
function candle(x,k,w){const up=k.c>=k.o,top=Y(Math.max(k.o,k.c)),bot=Y(Math.min(k.o,k.c)),hh=Math.max(2,bot-top);
 X.strokeStyle=up?BULLB:BEAR;X.lineWidth=Math.max(1.5,w/6);X.beginPath();X.moveTo(x,Y(k.h));X.lineTo(x,top);X.moveTo(x,top+hh);X.lineTo(x,Y(k.l));X.stroke();
 if(up){X.fillStyle=BULLF;X.fillRect(x-w/2,top,w,hh);X.lineWidth=1.6;X.strokeRect(x-w/2+.8,top+.8,w-1.6,hh-1.6)}else{X.fillStyle=BEAR;X.fillRect(x-w/2,top,w,hh)}}
function drawSeries(S,L,o){const sp=o.sp,w=o.w,xr=o.xr||1450;const n=Math.floor(L),f=L-n;
 const cx0=o.x0||PX0;X.save();X.beginPath();X.rect(cx0,PY0-40,PX1-cx0,PY1-PY0+80);X.clip();
 for(let i=Math.max(0,n-Math.ceil((xr-PX0)/sp)-2);i<=Math.min(n,S.length-1);i++){let k=S[i];const x=xr-(L-i)*sp;
  if(i===n){const ff=ease(cl(f*1.15));const wob=Math.sin(L*23)*0.00006*(1-ff);const c=k.o+(k.c-k.o)*ff+wob;k={o:k.o,c,h:Math.max(k.o,c)+(k.h-Math.max(k.o,k.c))*ff,l:Math.min(k.o,c)-(Math.min(k.o,k.c)-k.l)*ff}}
  candle(x,k,w)}
 X.restore();return xr}
function zoneBand(t,b,o){const yt=Y(t),yb=Y(b);
 if(o.fill>0){X.globalAlpha=o.fill;X.fillStyle='rgba(60,120,210,.14)';X.fillRect(PX0,yt,PX1-PX0,yb-yt);X.globalAlpha=1;
  X.globalAlpha=o.fill;X.font='600 22px P';X.fillStyle='rgb(96,160,236)';X.textBaseline='middle';X.textAlign='left';X.fillText('ZONE OF INTEREST',136,yb-22);X.globalAlpha=1}
 if(o.glow>0){X.globalAlpha=o.glow;X.shadowColor='rgba(91,165,252,.95)';X.shadowBlur=16;X.strokeStyle='rgb(130,190,255)';X.lineWidth=4;[yt,yb].forEach(y=>{X.beginPath();X.moveTo(PX0,y);X.lineTo(PX1,y);X.stroke()});X.shadowBlur=0;X.globalAlpha=1}
 X.strokeStyle=BLUE;X.lineWidth=2.5;[[yt,o.top],[yb,o.bot]].forEach(([y,a])=>{if(a>0){X.beginPath();X.moveTo(PX0,y);X.lineTo(PX0+(PX1-PX0)*a,y);X.stroke()}});
 if(o.tags>0){X.globalAlpha=o.tags;[[t,yt],[b,yb]].forEach(([p,y])=>{X.fillStyle=TAG;rr(1606,y-18,124,36,4);X.fill();X.fillStyle='rgb(8,18,40)';X.font='700 22px M';X.textAlign='center';X.fillText(p.toFixed(5),1668,y+1);X.textAlign='left'});X.globalAlpha=1}}
function level(p,name,a,hl=0){const y=Y(p);X.setLineDash([9,7]);X.strokeStyle=`rgba(${170+80*hl},${180+60*hl},${200+55*hl},${.4+.5*hl})`;X.lineWidth=1.5+hl;
 if(hl>0){X.shadowColor='rgba(91,165,252,.9)';X.shadowBlur=12*hl}X.beginPath();X.moveTo(PX0,y);X.lineTo(PX0+(PX1-PX0)*a,y);X.stroke();X.setLineDash([]);X.shadowBlur=0;
 const txt=name+'  '+p.toFixed(5);X.font=(hl>0.5?'500':'400')+' 27px P';X.textAlign='right';X.textBaseline='middle';const w=X.measureText(txt).width;
 X.globalAlpha=a;if(hl>0){X.globalAlpha=a*hl;X.fillStyle='rgba(9,16,32,.92)';X.fillRect(PX1-12-w-12,y-38,w+24,34);X.globalAlpha=a}
 X.fillStyle=hl>0?`rgb(${150+105*hl},${160+95*hl},${180+75*hl})`:'rgb(150,160,180)';X.fillText(txt,PX1-12,y-20);X.textAlign='left';X.globalAlpha=1}
function bellIcon(cx,cy,s){X.fillStyle='rgb(10,20,40)';X.beginPath();X.moveTo(cx-9*s,cy+6*s);X.quadraticCurveTo(cx-9*s,cy-10*s,cx,cy-11*s);X.quadraticCurveTo(cx+9*s,cy-10*s,cx+9*s,cy+6*s);X.lineTo(cx+11*s,cy+8*s);X.lineTo(cx-11*s,cy+8*s);X.closePath();X.fill();X.beginPath();X.arc(cx,cy+11*s,3*s,0,7);X.fill()}
function bell(p,a,T){if(a<=0)return;const x=900,y=Y(p)-(1-a)*80;X.globalAlpha=a;X.fillStyle=TAG;X.beginPath();X.arc(x,y,30,0,7);X.fill();bellIcon(x,y,1.25);
 X.font='600 26px P';const txt='Alert · '+p.toFixed(5),w=X.measureText(txt).width+36;X.fillStyle='rgba(9,16,32,.95)';rr(x+44,y-24,w,48,6);X.fill();X.strokeStyle='rgba(120,180,250,.8)';X.lineWidth=1.5;X.stroke();X.fillStyle='#fff';X.textBaseline='middle';X.fillText(txt,x+62,y+1);X.globalAlpha=1}
function pulse(p,a,tt){if(a<=0)return;for(let k=0;k<2;k++){const ph=((tt*0.8+k*0.5)%1+1)%1;X.globalAlpha=a*(1-ph)*.85;X.strokeStyle=TAG;X.lineWidth=3;X.beginPath();X.arc(900,Y(p),32+ph*56,0,7);X.stroke()}X.globalAlpha=1}
function notif(x,y,a,T,l1,l2,l3){if(a<=0)return;const dx=(1-a)*120;X.globalAlpha=a;X.shadowColor='rgba(0,0,0,.45)';X.shadowBlur=30;X.fillStyle='#fff';rr(x+dx,y,620,170,18);X.fill();X.shadowBlur=0;
 X.fillStyle='rgb(14,26,52)';rr(x+dx+28,y+30,78,78,14);X.fill();X.fillStyle=TAG;bellIconL(x+dx+67,y+68);
 X.textBaseline='middle';X.font='400 24px P';X.fillStyle='rgb(110,118,135)';X.fillText(l1,x+dx+130,y+46);X.font='700 31px P';X.fillStyle='rgb(14,20,34)';X.fillText(l2,x+dx+130,y+90);X.font='500 25px M';X.fillStyle='rgb(30,110,220)';X.fillText(l3,x+dx+130,y+134);X.font='400 22px P';X.fillStyle='rgb(110,118,135)';X.textAlign='right';X.fillText('now',x+dx+596,y+46);X.textAlign='left';X.globalAlpha=1}
function bellIconL(cx,cy){X.fillStyle=TAG;X.beginPath();X.moveTo(cx-14,cy+9);X.quadraticCurveTo(cx-14,cy-16,cx,cy-17);X.quadraticCurveTo(cx+14,cy-16,cx+14,cy+9);X.lineTo(cx+17,cy+12);X.lineTo(cx-17,cy+12);X.closePath();X.fill();X.beginPath();X.arc(cx,cy+17,4.5,0,7);X.fill()}
function callout(x,y,txt,a,o={}){if(a<=0)return;X.globalAlpha=a;X.font=o.f||'500 28px P';const w=X.measureText(txt).width+36,h=54;const bx=o.align==='right'?x-w:o.align==='center'?x-w/2:x;
 X.fillStyle=o.bg||'rgba(9,16,32,.94)';rr(bx,y-h/2,w,h,8);X.fill();X.strokeStyle=o.bd||'rgba(255,255,255,.3)';X.lineWidth=1.2;X.stroke();X.fillStyle=o.c||'#fff';X.textBaseline='middle';X.textAlign='left';X.fillText(txt,bx+18,y+1);X.globalAlpha=1}
function pill(txt,x,y,a){callout(x,y,txt,a,{f:'600 32px P',bg:'rgba(40,90,170,.35)',bd:'rgba(120,180,250,.95)',align:'center'})}
function kicker(t,x,y,a){if(a<=0)return;X.globalAlpha=a;X.font='700 26px M';X.fillStyle=BLUE_T;X.textBaseline='middle';X.letterSpacing='4px';X.fillText(t,x,y);X.letterSpacing='0px';X.globalAlpha=1}
function bigLine(t,x,y,size,col,a,dy,out=1){if(a<=0||out<=0)return;X.globalAlpha=a*out;X.font=`700 ${size}px P`;X.fillStyle=col;X.textBaseline='middle';X.textAlign='left';X.fillText(t,x,y+dy);X.globalAlpha=1}
function fadeTo(t,a,b){const k=cl((t-a)/(b-a));X.globalAlpha=k;X.drawImage(IM.plate,0,0);X.globalAlpha=1}
function fadeFrom(t,a,b){const k=1-cl((t-a)/(b-a));X.globalAlpha=k;X.drawImage(IM.plate,0,0);X.globalAlpha=1}
function copyPanel(x,y,a,clicks,t){if(a<=0)return;X.globalAlpha=a;X.shadowColor='rgba(0,0,0,.4)';X.shadowBlur=30;X.fillStyle='#fff';rr(x,y,820,697,14);X.fill();X.shadowBlur=0;
 X.textBaseline='middle';X.textAlign='left';X.fillStyle='rgb(14,20,34)';X.font='500 48px P';X.fillText('Levels to copy',x+44,y+76);X.font='300 30px P';X.fillStyle='rgb(110,118,135)';X.fillText('EUR/USD · Buying interest',x+44,y+128);
 X.fillStyle='rgb(225,228,234)';X.fillRect(x+44,y+168,732,2);
 const rows=[['Zone of interest','1.09024 – 1.08724',''],['CME Volume Node','1.08870',''],['Put Cluster','1.08738','above $1B'],['Gamma Flip','1.09051','']];
 rows.forEach((r,i)=>{const ry=y+190+i*126;X.fillStyle='rgb(90,98,115)';X.font='400 28px P';X.fillText(r[0],x+44,ry+30);X.fillStyle='rgb(14,20,34)';X.font='700 38px M';X.fillText(r[1],x+44,ry+78);
  if(r[2]){const w=X.measureText(r[1]).width;X.font='400 24px P';X.fillStyle='rgb(110,118,135)';X.fillText(r[2],x+44+w+18,ry+80)}
  const done=t>=clicks[i][0];const bx=x+590,by=ry+28,bw=186,bh=58;
  if(done){X.fillStyle='rgb(14,26,52)';rr(bx,by,bw,bh,6);X.fill();X.fillStyle='#fff'}else{X.strokeStyle='rgb(14,20,34)';X.lineWidth=2;rr(bx,by,bw,bh,6);X.stroke();X.fillStyle='rgb(14,20,34)'}
  X.font='500 26px P';X.textAlign='center';X.fillText(done?'Copied':'Copy',bx+bw/2,by+bh/2+1);X.textAlign='left';
  if(i<3){X.fillStyle='rgb(232,234,239)';X.fillRect(x+44,ry+120,732,2)}});
 // cursor travelling between buttons
 let cx=x+700,cy=y+260;for(let i=0;i<clicks.length;i++){const ct=clicks[i][0],tx=x+690,ty=y+190+i*126+60;if(t>=ct-0.35){const u=ease(cl((t-(ct-0.35))/0.3));cx=cx+(tx-cx)*u;cy=cy+(ty-cy)*u}}
 if(t>clicks[0][0]-0.6){X.fillStyle='#fff';X.strokeStyle='#111';X.lineWidth=2;X.beginPath();X.moveTo(cx,cy);X.lineTo(cx,cy+34);X.lineTo(cx+9,cy+26);X.lineTo(cx+16,cy+40);X.lineTo(cx+22,cy+37);X.lineTo(cx+15,cy+24);X.lineTo(cx+26,cy+24);X.closePath();X.fill();X.stroke()}
 X.globalAlpha=1}
function endCard(tt,line){X.drawImage(IM.plate0,0,0);
 const a=ramp(tt,0,.6);X.globalAlpha=a;X.drawImage(IM.logo,776,370);X.font='300 46px P';X.fillStyle='#fff';X.textAlign='center';X.textBaseline='middle';X.fillText(line,960,545);
 X.font='300 26px P';X.fillStyle='rgb(140,150,175)';X.fillText('Educational content. Not investment advice. Trading involves risk.',960,640);X.textAlign='left';X.globalAlpha=1}
function buildC(closes,start,seed,ov={}){const r=seeded(seed);let o=start;const out=[];
 closes.forEach((c,i)=>{let h=Math.max(o,c)+0.00004+r()*0.00008,l=Math.min(o,c)-0.00004-r()*0.00008;const v=ov[i]||{};
  if(v.o!==undefined)o=v.o;if(v.h!==undefined)h=v.h;if(v.l!==undefined)l=v.l;out.push({o,c,h,l});o=c});return out}
function chip(txt,x,y,on){X.font='600 24px P';const w=X.measureText(txt).width+36;X.fillStyle=on?'rgb(80,152,230)':'rgba(255,255,255,.08)';rr(x,y,w,42,6);X.fill();X.fillStyle=on?'rgb(8,18,40)':'rgb(150,160,180)';X.textBaseline='middle';X.textAlign='left';X.fillText(txt,x+18,y+22);return w}
function tfChips(a){/* a: 0 = M15 active, 1 = H1 active */const w1=chip('M15',1390,150,a<0.5);chip('H1',1390+w1+10,150,a>=0.5)}
function boxLabel(x1,p1,x2,p2,txt,a,col){if(a<=0)return;const y1=Y(p1),y2=Y(p2);X.globalAlpha=a;X.fillStyle=col||'rgba(91,165,252,.16)';X.fillRect(x1,Math.min(y1,y2),(x2-x1)*cl(a*1.3),Math.abs(y2-y1));X.strokeStyle=col?'rgba(255,255,255,.45)':'rgba(120,180,250,.85)';X.lineWidth=1.5;X.strokeRect(x1,Math.min(y1,y2),(x2-x1)*cl(a*1.3),Math.abs(y2-y1));
 X.font='500 28px P';X.fillStyle='#fff';X.textAlign='center';X.textBaseline='middle';X.fillText(txt,x1+(x2-x1)/2,(y1+y2)/2);X.textAlign='left';X.globalAlpha=1}
function ring(x,y,a,col='#fff'){if(a<=0)return;X.globalAlpha=a;X.strokeStyle=col;X.lineWidth=2.5;X.beginPath();X.arc(x,y,13,0,7);X.stroke();X.globalAlpha=1}
function label(x,y,txt,a,o={}){if(a<=0)return;X.globalAlpha=a;X.font=o.f||'500 28px P';X.fillStyle=o.c||'#fff';X.textAlign=o.align||'center';X.textBaseline='middle';X.fillText(txt,x,y);X.textAlign='left';X.globalAlpha=1}
function centerText(parts,y,size,a,weight=600){if(a<=0)return;X.globalAlpha=a;X.font=`${weight} ${size}px P`;X.textBaseline='middle';X.textAlign='left';const tw=parts.reduce((s,p)=>s+X.measureText(p[0]).width,0);let x=960-tw/2;parts.forEach(([t,c])=>{X.fillStyle=c;X.fillText(t,x,y);x+=X.measureText(t).width});X.globalAlpha=1}
function panel(x,y,w,h,a){X.globalAlpha=a;X.fillStyle='rgba(12,22,44,.96)';rr(x,y,w,h,12);X.fill();X.strokeStyle='rgba(120,160,220,.35)';X.lineWidth=1.5;X.stroke();X.globalAlpha=1}
function drawFixed(S,x0,sp,w,n){const full=Math.floor(n),f=n-full;
 for(let i=0;i<Math.min(S.length,Math.ceil(n));i++){let k=S[i];if(i===full&&f>0){const ff=ease(f),c=k.o+(k.c-k.o)*ff;k={o:k.o,c,h:Math.max(k.o,c)+(k.h-Math.max(k.o,k.c))*ff,l:Math.min(k.o,c)-(Math.min(k.o,k.c)-k.l)*ff}}candle(x0+i*sp,k,w)}}
