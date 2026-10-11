import asyncio,os,sys
from playwright.async_api import async_playwright
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1920,'height':1080})
    for v in 'ABC':
      await pg.goto('file://'+os.path.abspath('v.html')+'?v='+v);await pg.wait_for_timeout(800)
      for t in [2.5,7.5,11.5,14.5]:
        await pg.evaluate(f'R({t})');await pg.screenshot(path=f'k_{v}_{t}.png')
    await b.close()
asyncio.run(m())
