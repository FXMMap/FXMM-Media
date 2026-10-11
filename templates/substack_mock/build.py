import json,markdown,asyncio,os
from playwright.async_api import async_playwright
a1=json.load(open('/home/claude/substack/a1.json'))
a2=markdown.markdown(open('a2.md').read())
A=[('a1','The Retail Trading Industry Has an Incentive Problem',"Most products built for retail traders make money when you're active, not when you're right.",'Oct 13, 2026','a01_cover.jpg',a1),
   ('a2',"What Weekly Positioning Data Actually Tells You (And What It Doesn't)","The Commitments of Traders report is free, public and widely misread. Here's how to read it the way a desk does.",'Oct 16, 2026','a02_cover_B.jpg',a2)]
CSS='''@font-face{font-family:P;font-weight:600;src:url(poppins-latin-600-normal.woff2)}@font-face{font-family:P;font-weight:700;src:url(poppins-latin-700-normal.woff2)}@font-face{font-family:P;font-weight:400;src:url(poppins-latin-400-normal.woff2)}
@font-face{font-family:L;src:url(/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf)}
body{margin:0;background:#fff;font-family:L,Georgia,serif;color:#363737}
.nav{height:64px;border-bottom:1px solid #e6e6e6;display:flex;align-items:center;justify-content:space-between;padding:0 32px;font-family:P}
.nav .l{display:flex;align-items:center;gap:12px;font-weight:700;font-size:18px;color:#121821}.nav .l span{width:36px;height:36px;border-radius:8px;background:#0D182E;display:flex;align-items:center;justify-content:center}
.nav .b{background:#0060C7;color:#fff;font-weight:600;font-size:14px;padding:10px 18px;border-radius:8px}
.w{max-width:728px;margin:0 auto;padding:40px 24px 80px}
h1{font-family:P;font-weight:700;font-size:40px;line-height:1.15;color:#121821;margin:0 0 12px;letter-spacing:-.5px}
.sub{font-size:21px;color:#6b6b6b;line-height:1.45;margin-bottom:24px}
.au{display:flex;align-items:center;gap:12px;font-family:P;font-size:14px;color:#121821;border-top:1px solid #eee;border-bottom:1px solid #eee;padding:14px 0;margin-bottom:28px}
.au .av{width:40px;height:40px;border-radius:50%;background:#0D182E;display:flex;align-items:center;justify-content:center}.au small{display:block;color:#777;font-size:13px}
.cover{width:100%;border-radius:4px;margin-bottom:28px}
.body p,.body li{font-size:19px;line-height:1.65;margin:0 0 22px}.body h2{font-family:P;font-weight:700;font-size:26px;color:#121821;margin:40px 0 16px}
.body a{color:#0060C7}
.cta{margin-top:40px;border:1px solid #e6e6e6;border-radius:8px;padding:28px;text-align:center;font-family:P}.cta b{display:block;font-size:20px;color:#121821;margin-bottom:6px}.cta i{font-style:normal;color:#777;font-size:14px}
.cta div{margin:16px auto 0;display:inline-block;background:#0060C7;color:#fff;font-weight:600;padding:12px 26px;border-radius:8px}'''
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1100,'height':900})
    for k,t,s,d,c,h in A:
      html=f'''<!doctype html><meta charset=utf-8><style>{CSS}</style><div class=nav><div class=l><span><img src=mark.png style="width:24px"></span>The Market Map by FXMM</div><div class=b>Subscribe</div></div>
<div class=w><h1>{t}</h1><div class=sub>{s}</div><div class=au><div class=av><img src=mark.png style="width:24px"></div><div>Roberto Di Ciero<small>{d}</small></div></div><img class=cover src={c}><div class=body>{h}</div>
<div class=cta><b>The Market Map by FXMM</b><i>For retail traders who want to trade with context, not hope.</i><br><div>Subscribe</div></div></div>'''
      open(f'{k}.html','w').write(html)
      await pg.goto('file://'+os.path.abspath(f'{k}.html'));await pg.wait_for_timeout(600)
      await pg.screenshot(path=f'mock_{k}.png',full_page=True)
    await b.close()
asyncio.run(m())
