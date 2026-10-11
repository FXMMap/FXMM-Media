import asyncio,os
from playwright.async_api import async_playwright
CSS='''@font-face{font-family:P;font-weight:400;src:url(poppins-latin-400-normal.woff2)}@font-face{font-family:P;font-weight:600;src:url(poppins-latin-600-normal.woff2)}@font-face{font-family:P;font-weight:700;src:url(poppins-latin-700-normal.woff2)}@font-face{font-family:L;font-style:italic;src:url(/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf)}@font-face{font-family:M;font-weight:500;src:url(jetbrains-mono-latin-500-normal.woff2)}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1920px;background:#0D182E;font-family:P;color:#fff;position:relative;overflow:hidden}
.wm{position:absolute;right:-200px;bottom:-140px;width:900px;opacity:1}
.logo{position:absolute;left:90px;top:230px;height:52px}
.k{position:absolute;left:90px;top:350px;font-size:26px;font-weight:600;letter-spacing:5px;color:#62A5F4}
h1{position:absolute;left:88px;right:88px;top:420px;font-size:76px;line-height:1.1;font-weight:700;letter-spacing:-1.6px}
.es{position:absolute;left:90px;right:90px;font-size:34px;line-height:1.4;color:#B9C3D6}
.img{position:absolute;left:90px;right:90px;height:500px;border-radius:24px;background-size:cover;background-position:center;border:1px solid #22304A}
.mm{font-family:L;font-style:italic;font-weight:600;font-size:38px;letter-spacing:0;color:#fff;text-transform:none;margin-left:6px}.k{display:flex;align-items:baseline}.free{position:absolute;left:94px;font-size:28px;color:#B9C3D6}.pill{position:absolute;left:90px;height:96px;display:flex;align-items:center;gap:14px;background:#fff;border-radius:48px;padding:0 34px 0 8px}.pill img{height:84px}.pill span{color:#121821;font-weight:600;font-size:30px}
.tap{position:absolute;left:90px;right:90px;text-align:center;font-family:M;font-size:28px;color:#C9D3E3;letter-spacing:1px}'''
S=[('st_a1','The Retail Trading Industry <span style="color:#62A5F4">Has an Incentive Problem</span>','La industria del trading retail tiene un problema de incentivos.','a01_cover.jpg',800,920),
   ('st_a2','What Weekly Positioning Data <span style="color:#62A5F4">Actually Tells You</span>','Lo que de verdad te dicen los datos semanales de posicionamiento.','a02_cover_B.jpg',800,920)]
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1080,'height':1920})
    for n,t,es,img,ey,iy in S:
      h=f'<!doctype html><meta charset=utf-8><style>{CSS}</style><img class=wm src=wmN.png><img class=logo src=logoW.png><div class=k>NEW ON <span class=mm>The Market Map</span></div><h1>{t}</h1><div class=es style="top:{ey}px">{es}</div><div class=img style="top:{iy+60}px;background-image:url({img})"></div><div class=pill style="top:{iy+610}px"><img src=ss_icon.png><span>Read on Substack · Léelo en Substack</span></div><div class=free style="top:{iy+728}px">Free newsletter, twice a week · Gratis, dos veces por semana</div><div class=tap style="top:{iy+800}px">&darr;</div>'
      open('t.html','w').write(h);await pg.goto('file://'+os.path.abspath('t.html'));await pg.wait_for_timeout(500);await pg.screenshot(path=n+'_v3.png')
    await b.close()
asyncio.run(m())
