# Redraws the chart panel of IG slide p26_03: price still ~28 pips above the zone when the report goes out.
import asyncio,os,sys,random
from playwright.async_api import async_playwright
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))
src,out,lang=sys.argv[1],sys.argv[2],sys.argv[3]
L={'es':('ZONA DE INTERÉS','PRECIO AL ENVIAR EL INFORME','≈ 28 pips'),
   'en':('ZONE OF INTEREST','PRICE WHEN THE REPORT GOES OUT','≈ 28 pips')}[lang]
random.seed(11)
# candles: gentle descent from y=800 to close ~880
cs=[];prev=808
N=15
for i in range(N):
  tgt=808+(878-808)*(i+1)/N
  c=tgt+random.uniform(-14,12) if i<N-1 else 878
  o=prev
  hi=min(o,c)-random.uniform(4,10); lo=max(o,c)+random.uniform(4,10)
  cs.append((o,c,hi,lo)); prev=c
svg=[]
for i,(o,c,hi,lo) in enumerate(cs):
  x=34+i*34; col='#DD3D3D' if c>o else '#19965C'
  top=min(o,c); h=max(abs(c-o),3)
  svg.append(f'<line x1={x} x2={x} y1={hi-750} y2={lo-750} stroke="{col}" stroke-width=2 />')
  svg.append(f'<rect x={x-11} y={top-750} width=22 height={h} fill="{col}" />')
html=f'''<!doctype html><meta charset=utf-8><style>
@font-face{{font-family:P6;src:url({D}/poppins-latin-600-normal.woff2)}}@font-face{{font-family:J;src:url({D}/jetbrains-mono-latin-700-normal.woff2)}}
*{{margin:0}}body{{width:913px;height:339px;background:#0D182E}}
.p{{position:absolute;left:0;top:0;width:911px;height:337px;border:1px solid #25314A;border-radius:10px;background:#15213B;overflow:hidden}}
.z{{position:absolute;left:0;right:0;top:235px;height:50px;background:#1C3257;border-top:2px solid #62A5F4;border-bottom:2px solid #62A5F4}}
.zl{{position:absolute;left:16px;top:252px;font-family:P6;font-size:17px;letter-spacing:2px;color:#62A5F4}}
.pl{{position:absolute;left:560px;top:96px;font-family:J;font-size:14px;letter-spacing:1px;color:#C9D3E3}}
.pip{{position:absolute;left:712px;top:162px;font-family:P6;font-size:26px;color:#FFFFFF}}
</style><div class=p><div class=z></div><div class=zl>{L[0]}</div>
<svg width=913 height=339 style="position:absolute;left:0;top:0">{''.join(svg)}
<line x1=530 x2=905 y1=128 y2=128 stroke="#C9D3E3" stroke-width=1.5 stroke-dasharray="6 5"/>
<line x1=690 x2=690 y1=132 y2=231 stroke="#FFFFFF" stroke-width=2/>
<line x1=680 x2=700 y1=132 y2=132 stroke="#FFFFFF" stroke-width=2/><line x1=680 x2=700 y1=231 y2=231 stroke="#FFFFFF" stroke-width=2/>
<circle cx=510 cy=128 r=5 fill="#FFFFFF"/></svg>
<div class=pl>{L[1]}</div><div class=pip>{L[2]}</div></div>'''
open('/tmp/pp.html','w').write(html)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':913,'height':339})
    await pg.goto('file:///tmp/pp.html');await pg.wait_for_timeout(400);await pg.screenshot(path='/tmp/pp.png');await b.close()
asyncio.run(m())
im=Image.open(src).convert('RGB');im.paste(Image.open('/tmp/pp.png').convert('RGB'),(84,750));im.save(out,quality=93)
