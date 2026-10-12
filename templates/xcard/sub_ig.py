import asyncio,os,sys
from playwright.async_api import async_playwright
D=os.path.dirname(os.path.abspath(__file__))
ITEMS=[('a04_cover.jpg','Why Price Reacts Where Volume Has Traded','FRIDAY · OCT 23','50% 50%','sub_oct23.jpg'),
       ('a05_cover.jpg','Patience Isn\'t a Personality Trait. It\'s a Plan.','TUESDAY · OCT 27','38% 50%','sub_oct27.jpg')]
CSS='''@font-face{font-family:P;src:url(%s/poppins-latin-500-normal.woff2)}@font-face{font-family:P6;src:url(%s/poppins-latin-600-normal.woff2)}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;background:#0D182E;overflow:hidden;position:relative}
.ph{position:absolute;top:0;left:0;width:1080px;height:780px;background-size:cover}
.fade{position:absolute;top:620px;left:0;width:1080px;height:160px;background:linear-gradient(rgba(13,24,46,0),#0D182E)}
.pn{position:absolute;top:780px;left:0;width:1080px;height:570px;padding:20px 84px}
.k{font-family:P6;font-size:24px;letter-spacing:6px;color:#62A5F4}
.m{font-family:Georgia,serif;font-style:italic;color:#fff;font-size:34px;margin-top:26px}.m b{font-family:P6;font-style:normal;font-size:24px;color:#62A5F4;margin-left:8px}
h1{font-family:P6;font-weight:600;color:#fff;font-size:62px;line-height:76px;margin-top:22px}
.u{position:absolute;left:84px;bottom:70px;font-family:P;font-size:26px;color:#C9D3E3}.u span{color:#62A5F4}
.bar{position:absolute;left:84px;top:-4px;width:90px;height:6px;background:#007DFF}'''%(D,D)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1080,'height':1350})
    for img,t,day,pos,out in ITEMS:
      src='file://'+os.path.abspath('substack/'+img)
      html=f'<!doctype html><meta charset=utf-8><style>{CSS}</style><div class=ph style="background-image:url({src});background-position:{pos}"></div><div class=fade></div><div class=pn><div class=bar></div><div class=k>NEW · {day}</div><div class=m>The Market Map <b>by FXMM</b></div><h1>{t}</h1><div class=u>Free, twice a week · <span>fxmarketmap.substack.com</span></div></div>'
      open('/tmp/sub.html','w').write(html);await pg.goto('file:///tmp/sub.html');await pg.wait_for_timeout(500)
      await pg.screenshot(path='feed/ig-substack/'+out,type='jpeg',quality=92)
    await b.close()
asyncio.run(m())
