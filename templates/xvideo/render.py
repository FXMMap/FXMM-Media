import os,asyncio,sys
from playwright.async_api import async_playwright
V=sys.argv[1];N=15*30;W=4;D=f'fr{V}';os.makedirs(D,exist_ok=True)
async def worker(p,k):
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1920,'height':1080})
    await pg.goto('file://'+os.path.abspath('v.html')+'?v='+V);await pg.wait_for_timeout(1000)
    for i in range(k,N,W):
        await pg.evaluate(f'R({i/30})');await pg.screenshot(path=f'{D}/{i:05d}.jpg',type='jpeg',quality=92)
    await b.close()
async def main():
    async with async_playwright() as p: await asyncio.gather(*[worker(p,k) for k in range(W)])
asyncio.run(main())
