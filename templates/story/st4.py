# IG stories for Substack articles (v4 layout: no drawn button, space for native link sticker)
import asyncio,os
from playwright.async_api import async_playwright
CSS=open('st3.py').read().split("CSS='''")[1].split("'''")[0]
CSS+='.sub{position:absolute;left:0;right:0;text-align:center;font-size:30px;line-height:1.35;color:#B9C3D6}.ssi{position:absolute;left:510px;width:60px}'
S=[('story_art03','The Home Run Trade <span style="color:#62A5F4">Is Ruining Your Month</span>','El trade que "arregla el mes" es el que te lo arruina.','a03_cover.jpg'),
   ('story_art04','Why Price Reacts <span style="color:#62A5F4">Where Volume Has Traded</span>','Por qué el precio reacciona donde se operó volumen real.','a04_cover.jpg'),
   ('story_art05','Patience Isn\'t a Personality Trait. <span style="color:#62A5F4">It\'s&nbsp;a&nbsp;Plan.</span>','La paciencia no es un rasgo de personalidad. Es un plan.','a05_cover.jpg'),
   ('story_art06','Why Currencies Move <span style="color:#62A5F4">Before Central Banks Do</span>','Por qué las monedas se mueven antes que los bancos centrales.','a06_cover.jpg')]
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1080,'height':1920})
    for n,t,es,img in S:
      iy=920
      h=f'<!doctype html><meta charset=utf-8><style>{CSS}</style><img class=wm src=wmN.png><img class=logo src=logoW.png><div class=k>NEW ON <span class=mm>The Market Map</span></div><h1 id=h>{t}</h1><div class=es id=es>{es}</div><div class=img style="top:{iy+60}px;background-image:url({img})"></div><div class=tap style="top:{iy+600}px">TAP THE LINK BELOW · TOCA EL LINK &darr;</div><img class=ssi src=ss_icon.png style="top:1725px"><div class=sub style="top:1795px">Free newsletter, twice a week<br>Gratis, dos veces por semana</div>'
      open('t.html','w').write(h);await pg.goto('file://'+os.path.abspath('t.html'));await pg.wait_for_timeout(600)
      await pg.evaluate("()=>{const h=document.getElementById('h');document.getElementById('es').style.top=(h.offsetTop+h.offsetHeight+70)+'px'}")
      await pg.screenshot(path='../../stories/substack-31c88032/'+n+'.png')
    await b.close()
asyncio.run(m())
