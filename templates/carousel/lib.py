exec(open('head.py').read())
NAVY='''body{background:#0D182E;color:#EEF1F6}.h{color:#FFFFFF}.h b{color:#62A5F4}.lab{color:#62A5F4}.num{color:#62A5F4}.cnt{color:#8A98B3}
.p{color:#B9C3D6}.foot{border-top:1px solid #22304A}.dots i{background:#2A3955}.dots i.on{background:#62A5F4}.sw{color:#B9C3D6}
.card{background:#15213A;border:1px solid #22304A;box-shadow:none}.chk{color:#EEF1F6}.chk span{background:#1E3254;color:#62A5F4}.btn span{color:#EEF1F6}.cap{color:#7D8AA3}
.logo{height:33px}'''
def candles(W=912,H=280,label='ZONA DE INTERÉS',navy=False):
    import random
    random.seed(7); out=[]; zt,zb=205,255
    zf,zl,zt_c=('#1B3358','#62A5F4','#62A5F4') if navy else ('#E3EEFC','#2F6FE6','#0060C7')
    out.append(f'<rect x="0" y="{zt}" width="{W}" height="{zb-zt}" fill="{zf}"/><line x1="0" y1="{zt}" x2="{W}" y2="{zt}" stroke="{zl}" stroke-width="2"/><line x1="0" y1="{zb}" x2="{W}" y2="{zb}" stroke="{zl}" stroke-width="2"/>')
    out.append(f'<text x="16" y="{zb-14}" font-family="P" font-size="18" font-weight="600" letter-spacing="2" fill="{zt_c}">{label}</text>')
    path=[60,75,70,95,88,110,105,130,122,150,145,170,165,190,200,225,232,215,190,170,150,135,118,100,90,78]
    n=len(path); step=W/(n+1)
    for k in range(n-1):
        o,c=path[k],path[k+1]; x=step*(k+1)
        hi=min(o,c)-random.randint(6,16); lo=max(o,c)+random.randint(6,16)
        if k==15: lo=246
        col='#0A9B5A' if c<o else '#D0453B'
        out.append(f'<line x1="{x}" y1="{hi}" x2="{x}" y2="{lo}" stroke="{col}" stroke-width="2"/><rect x="{x-11}" y="{min(o,c)}" width="22" height="{max(abs(c-o),3)}" fill="{col}"/>')
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">'+''.join(out)+'</svg>'
def num(n,lab): return f'<div style="display:flex;align-items:flex-end"><div class=num>{n}</div><div class=lab style="margin-bottom:14px">{lab}</div></div>'
def build(S,prefix,lang='es',navy=False):
    N=len(S)
    def ft(i,last):
        d=''.join(f'<i class="{"on" if k==i else ""}"></i>' for k in range(N))
        sw=("Guárdalo para después" if last else "Desliza &rarr;") if lang=='es' else ("Save this for later" if last else "Swipe &rarr;")
        return f'<div class=foot><div class=dots>{d}</div><div class=sw>{sw}</div></div>'
    css=CSS+(NAVY if navy else '')
    wm=f'<img class=wm src={"wmN.png" if navy else "wmI.png"}>'
    lg=f'<img class=logo src={"logoW.png" if navy else "logo.png"}>'
    async def m():
      async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1080,'height':1350})
        for i,h in enumerate(S):
          h=h.replace('{LOGO}',lg).replace('{N}',str(N))
          open('t.html','w').write(f'<!doctype html><meta charset=utf-8><style>{css}</style><body>{wm}{h}{ft(i,i==N-1)}</body>')
          await pg.goto('file://'+os.path.abspath('t.html'));await pg.wait_for_timeout(400);await pg.screenshot(path=f'{prefix}_{i+1:02d}.png')
        await b.close()
    asyncio.run(m())
    from PIL import Image
    ims=[Image.open(f'{prefix}_{i:02d}.png') for i in range(1,N+1)]
    rows=(N+2)//3
    s=Image.new('RGB',(3*540+40,rows*685+10),'#888')
    for k,im in enumerate(ims): s.paste(im.resize((540,675)),(10+(k%3)*550,10+(k//3)*685))
    s.save(f'{prefix}_sheet.png')
