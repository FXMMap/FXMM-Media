import asyncio,os,sys
from playwright.async_api import async_playwright
V=sys.argv[1];T=[float(x) for x in sys.argv[2].split(',')]
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1080,'height':1920})
    await pg.goto('file://'+os.path.abspath('vv.html')+'?v='+V);await pg.wait_for_timeout(800)
    for t in T: await pg.evaluate(f'R({t})');await pg.screenshot(path=f'k_{V}_{t}.png')
    await b.close()
asyncio.run(m())
