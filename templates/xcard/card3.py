import asyncio,os,json,sys
from playwright.async_api import async_playwright
src=open('card.py').read()
F=src.split("F='''")[1].split("'''")[0].replace("svg{position:absolute;right:-120px;bottom:-230px}","")
VAR={
 'A':'.wm{position:absolute;right:-140px;bottom:-260px;width:820px;height:595px;background:url(wmA.png) center/contain no-repeat}',
 'B':'.wm{position:absolute;right:-140px;bottom:-260px;width:820px;height:595px;background:url(wmB.png) center/contain no-repeat}',
 'C':'.wm{position:absolute;right:-140px;bottom:-260px;width:820px;height:595px;background:url(wmC.png) center/contain no-repeat}',
}
VAR['D']=VAR['A'].replace('wmA.png','wmD.png')
VAR['N']=VAR['A'].replace('wmA.png','wmN.png')
NAVY='body{background:#0D182E}h1{color:#FFFFFF}h1 b{color:#62A5F4}.k{color:#62A5F4}.line{background:#22304A}.url{color:#C9D3E3}.logo{height:33px;top:812px}'
LOGO={'A':'logoD.png','B':'logoD.png','C':'logoD.png','D':'logoD.png','N':'logoW.png'}
C=json.load(open(sys.argv[1])); vs=sys.argv[2].split(','); out=sys.argv[3]
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1600,'height':900})
    for v in vs:
     for k,(kick,t) in C.items():
      extra=NAVY if v=='N' else ''
      html=f'<!doctype html><meta charset=utf-8><style>{F}h1 b{{font-weight:700;color:#0060C7}}{VAR[v]}{extra}</style><div class=wm></div><div class=k>{kick}</div><h1>{t}</h1><div class=line></div><img class=logo src={LOGO[v]}><div class=url>fxmarketmap.com</div>'
      open('c2.html','w').write(html);await pg.goto('file://'+os.path.abspath('c2.html'));await pg.wait_for_timeout(300)
      await pg.evaluate("""()=>{const h=document.querySelector('h1'),k=document.querySelector('.k');const H=h.offsetHeight;const top=(770-H)/2+10;h.style.top=top+'px';k.style.top=(top-42)+'px';}""")
      await pg.screenshot(path=f'{out}/{v}_{k}')
    await b.close()
asyncio.run(m())
