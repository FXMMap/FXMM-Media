from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
import os
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':2560,'height':1440})
    pg.goto('file://'+os.path.abspath('b.html')); pg.wait_for_timeout(800)
    for o in 'ABC':
        pg.locator('#'+o).screenshot(path=f'banner_{o}.png')
    b.close()
for o in 'ABC':
    im=Image.open(f'banner_{o}.png').convert('RGB')
    desk=im.crop((0,508,2560,931))           # what desktop shows
    mob=im.crop((507,508,2053,931))          # safe area (all devices)
    W=2000; pad=40
    d=desk.resize((W,int(desk.height*W/2560)))
    m=mob.resize((int(mob.width*0.75),int(mob.height*0.75)))
    full=im.resize((W, int(1440*W/2560))); g=ImageDraw.Draw(full); k=W/2560
    g.rectangle([507*k,508*k,2053*k,931*k],outline=(255,59,107),width=4)
    H=pad+50+d.height+pad+50+m.height+pad+50+full.height+pad
    sh=Image.new('RGB',(W+2*pad,H),'white'); dr=ImageDraw.Draw(sh)
    from PIL import ImageFont
    f=ImageFont.truetype('Poppins-Bold.ttf',30)
    y=pad; dr.text((pad,y),f'Opcion {o} · Asi se ve en computadora',fill=(13,24,46),font=f); y+=50
    sh.paste(d,(pad,y)); y+=d.height+pad
    dr.text((pad,y),'Asi se ve en celular',fill=(13,24,46),font=f); y+=50
    sh.paste(m,(pad,y)); y+=m.height+pad
    dr.text((pad,y),'Imagen completa (TV) · en rojo, la zona que se ve en todos los dispositivos',fill=(13,24,46),font=f); y+=50
    sh.paste(full,(pad,y))
    sh.save(f'preview_{o}.png')
print('ok')
