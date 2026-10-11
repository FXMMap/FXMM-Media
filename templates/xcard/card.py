import asyncio,os,json,sys
from playwright.async_api import async_playwright
F='''@font-face{font-family:P;font-weight:600;src:url(poppins-latin-600-normal.woff2)}@font-face{font-family:P;font-weight:700;src:url(poppins-latin-700-normal.woff2)}@font-face{font-family:P;font-weight:400;src:url(poppins-latin-400-normal.woff2)}
body{margin:0;width:1600px;height:900px;background:#F4F6F9;font-family:P;position:relative;overflow:hidden}
.k{position:absolute;left:110px;top:300px;font-size:17px;font-weight:600;letter-spacing:3.5px;color:#0060C7}
h1{position:absolute;left:108px;top:340px;width:1300px;margin:0;font-size:74px;line-height:1.12;font-weight:700;letter-spacing:-1.6px;color:#121821}
.line{position:absolute;left:110px;right:110px;top:770px;height:1px;background:#E1E5EB}
.logo{position:absolute;left:110px;top:808px;height:40px}
.url{position:absolute;right:110px;top:815px;font-size:22px;font-weight:400;color:#121821}
svg{position:absolute;right:-120px;bottom:-230px}'''
SVG='<svg width="760" height="700" viewBox="0 0 760 700"><g fill="none" stroke="#EAEEF4" stroke-width="110" stroke-linejoin="miter"><polyline points="40,140 330,430 720,40"/><polyline points="40,420 330,710 720,320"/></g></svg>'
C=json.load(open(sys.argv[1]))
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1600,'height':900})
    for k,(kick,t) in C.items():
      html=f'<!doctype html><meta charset=utf-8><style>{F}</style>{SVG}<div class=k>{kick}</div><h1>{t}</h1><div class=line></div><img class=logo src=logoD.png><div class=url>fxmarketmap.com</div>'
      open('c.html','w').write(html);await pg.goto('file://'+os.path.abspath('c.html'));await pg.wait_for_timeout(300)
      # vertically center title block between 0 and line
      await pg.evaluate("""()=>{const h=document.querySelector('h1'),k=document.querySelector('.k');const H=h.offsetHeight;const top=(770-H)/2+10;h.style.top=top+'px';k.style.top=(top-42)+'px';}""")
      await pg.screenshot(path=k)
    await b.close()
asyncio.run(m())
