exec(open('head.py').read())
def candles():
    import random
    random.seed(7)
    W,H=912,330; out=[]
    zt,zb=205,255
    out.append(f'<rect x="0" y="{zt}" width="{W}" height="{zb-zt}" fill="#E3EEFC"/><line x1="0" y1="{zt}" x2="{W}" y2="{zt}" stroke="#2F6FE6" stroke-width="2"/><line x1="0" y1="{zb}" x2="{W}" y2="{zb}" stroke="#2F6FE6" stroke-width="2"/>')
    out.append(f'<text x="16" y="{zb-14}" font-family="P" font-size="18" font-weight="600" letter-spacing="2" fill="#0060C7">ZONA DE INTERÉS</text>')
    path=[60,75,70,95,88,110,105,130,122,150,145,170,165,190,200,225,232,215,190,170,150,135,118,100,90,78]
    n=len(path); step=W/(n+1)
    for k in range(n-1):
        o,c=path[k],path[k+1]
        x=step*(k+1)
        hi=min(o,c)-random.randint(6,16); lo=max(o,c)+random.randint(6,16)
        if k==15: lo=246
        up=c<o
        col='#0A9B5A' if up else '#D0453B'
        out.append(f'<line x1="{x}" y1="{hi}" x2="{x}" y2="{lo}" stroke="{col}" stroke-width="2"/><rect x="{x-11}" y="{min(o,c)}" width="22" height="{max(abs(c-o),3)}" fill="{col}"/>')
    return f'<svg width="{W}" height="280" viewBox="0 0 {W} 280">'+''.join(out)+'</svg>'
def vprof():
    vals=[22,30,38,52,70,96,100,82,58,44,34,26,20]
    r=''
    for k,v in enumerate(vals):
        y=10+k*24; w=v*5.9; hot=k in (5,6)
        r+=f'<rect x="0" y="{y}" width="{w}" height="18" rx="2" fill="{"#0060C7" if hot else "#D5DEEA"}"/>'
    r+='<text x="640" y="150" font-family="P" font-size="22" font-weight="600" fill="#0060C7">Mayor volumen</text><text x="640" y="178" font-family="P" font-size="20" fill="#5A6270">negociado</text>'
    return f'<svg width="840" height="330" viewBox="0 0 840 330">{r}</svg>'
def num(n,lab): return f'<div style="display:flex;align-items:flex-end"><div class=num>{n}</div><div class=lab style="margin-bottom:14px">{lab}</div></div>'
S=[
 f'<img class=logo src=logo.png><div class=cnt>1 / {N}</div><div class=main style="top:380px"><div class=lab>Contexto institucional</div><div class=h style="font-size:88px;line-height:94px;letter-spacing:-3px">3 cosas que mira<br>una mesa <b>antes de operar.</b></div><div class=p style="font-size:34px;line-height:50px">Lo que responde un desk institucional antes de arriesgar capital, y que casi nunca ves junto en tu gráfico.</div></div>',
 f'<div class=cnt>2 / {N}</div><div class=main style="top:250px">{num("01","Posicionamiento")}<div class=h>¿Hacia dónde están <b>los grandes?</b></div><div class=p>Las mesas miran cómo están posicionados los grandes operadores en cada divisa. Operar contra ese flujo sin saberlo es remar contra la corriente.</div><div class=card style="margin-top:40px"><div class=bar><span class=t>Compras</span><span class=b style="width:430px;background:#0060C7"></span><span class=v>68%</span></div><div class=bar><span class=t>Ventas</span><span class=b style="width:200px;background:#D5DEEA"></span><span class=v>32%</span></div></div><div class=cap>Ejemplo ilustrativo</div></div>',
 f'<div class=cnt>3 / {N}</div><div class=main style="top:250px">{num("02","Tasas de interés")}<div class=h>¿Hacia dónde tiran <b>las tasas?</b></div><div class=p>La diferencia de tasas entre dos bancos centrales empuja una moneda sobre la otra durante semanas o meses. Es el viento de fondo del par.</div><div class=card style="margin-top:40px;display:flex;align-items:center;padding:20px 20px"><div class=rate><div class=n>4,50%</div><div class=l>Banco central A</div></div><div style="font-family:M;font-size:40px;color:#9AA3AF">vs</div><div class=rate><div class=n>2,25%</div><div class=l>Banco central B</div></div><div class=rate style="border-left:1px solid #E6E7E4"><div class=n style="color:#0060C7">+2,25</div><div class=l>Favorece a A</div></div></div><div class=cap>Ejemplo ilustrativo</div></div>',
 f'<div class=cnt>4 / {N}</div><div class=main style="top:250px">{num("03","Volumen real")}<div class=h>¿Dónde se negoció <b>dinero de verdad?</b></div><div class=p>Los precios donde cambió de manos mucho volumen suelen volver a importar. Ahí es donde el precio tiene más probabilidad de reaccionar.</div><div class=card style="margin-top:40px;padding:26px 36px 16px">{vprof()}</div><div class=cap>Ejemplo ilustrativo</div></div>',
 f'<div class=cnt>5 / {N}</div><div class=main style="top:250px">{num("04","La regla")}<div class=h>Si se alinean, actúan. <b>Si no, esperan.</b></div><div class=p>Ese contexto casi nunca le llega al trader minorista en un solo lugar. Por eso termina operando solo con el gráfico.</div><div class=card style="margin-top:40px;padding:30px 0 20px">{candles()}</div><div class=cap>Ejemplo ilustrativo</div></div>',
 f'<img class=logo src=logo.png><div class=cnt>6 / {N}</div><div class=main style="top:235px"><div class=lab>La lista de espera está abierta</div><div class=h style="font-size:84px;line-height:90px;letter-spacing:-2.6px">Te mostramos<br><b>dónde se alinean.</b></div><div class=card style="margin-top:46px;border-top:4px solid #007DFF"><div class=chk><span>&#10003;</span>Zonas de interés en los 7 pares principales.</div><div class=chk><span>&#10003;</span>Con su contexto técnico, macro e institucional.</div><div class=chk><span>&#10003;</span>Aviso por Telegram o email.</div></div><div class=btn><div>Link en la bio</div><span>fxmarketmap.com</span></div></div>',
]
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1080,'height':1350})
    for i,h in enumerate(S):
      open('t.html','w').write(f'<!doctype html><meta charset=utf-8><style>{CSS}</style><body>{WM}{h}{foot(i,i==N-1)}</body>')
      await pg.goto('file://'+os.path.abspath('t.html'));await pg.wait_for_timeout(400);await pg.screenshot(path=f'ES_{i+1:02d}.png')
    await b.close()
asyncio.run(m())
