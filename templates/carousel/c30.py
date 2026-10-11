exec(open('lib.py').read())
def book():
    rows=[(1.0920,0,30),(1.0915,0,44),(1.0910,0,180),(1.0905,0,52),(1.0900,40,0),(1.0895,36,0),(1.0890,170,0),(1.0885,48,0)]
    g=''
    for k,(p,b,a) in enumerate(rows):
        y=12+k*36
        g+=f'<text x="410" y="{y+19}" text-anchor="middle" font-family="M" font-size="20" fill="#B9C3D6">{p:.4f}</text>'
        if a: g+=f'<rect x="490" y="{y}" width="{a*1.9}" height="24" rx="3" fill="{"#D0453B" if a>100 else "#4A2A36"}"/>'
        if b: g+=f'<rect x="{330-b*1.9}" y="{y}" width="{b*1.9}" height="24" rx="3" fill="{"#0A9B5A" if b>100 else "#1E4036"}"/>'
    g+='<text x="0" y="300" font-family="P" font-size="19" fill="#7D8AA3">Buy orders</text><text x="840" y="300" text-anchor="end" font-family="P" font-size="19" fill="#7D8AA3">Sell orders</text>'
    return f'<svg width="840" height="310" viewBox="0 0 840 310">{g}</svg>'
def opts():
    st=[(1.0800,30),(1.0850,55),(1.0900,120),(1.0950,48),(1.1000,95),(1.1050,26)]
    g='<line x1="20" y1="150" x2="820" y2="150" stroke="#2A3955" stroke-width="2"/>'
    for k,(p,v) in enumerate(st):
        x=70+k*140; big=v>90
        g+=f'<circle cx="{x}" cy="150" r="{v*0.55}" fill="{"#62A5F4" if big else "#2A3955"}" fill-opacity="{0.9 if big else 1}"/><text x="{x}" y="280" text-anchor="middle" font-family="M" font-size="20" fill="#B9C3D6">{p:.4f}</text>'
    g+='<text x="20" y="30" font-family="P" font-size="19" fill="#7D8AA3">Open options by strike</text>'
    return f'<svg width="840" height="300" viewBox="0 0 840 300">{g}</svg>'
def delta():
    v=[12,-8,20,26,-6,34,40,-10,46,52]
    g='<line x1="0" y1="160" x2="840" y2="160" stroke="#2A3955" stroke-width="2"/>'
    for k,d in enumerate(v):
        x=20+k*82; h=abs(d)*2.6; col='#0A9B5A' if d>0 else '#D0453B'
        g+=f'<rect x="{x}" y="{160-h if d>0 else 160}" width="56" height="{h}" rx="3" fill="{col}"/>'
    g+='<text x="0" y="30" font-family="P" font-size="19" fill="#7D8AA3">Aggressive buyers minus sellers, per bar</text>'
    return f'<svg width="840" height="300" viewBox="0 0 840 300">{g}</svg>'
def card(svg,cap='Illustrative example'): return f'<div class=card style="margin-top:40px;padding:30px 36px 20px">{svg}</div><div class=cap>{cap}</div>'
S=[
 '{LOGO}<div class=cnt>1 / {N}</div><div class=main style="top:400px"><div class=lab>Institutional context</div><div class=h style="font-size:88px;line-height:94px;letter-spacing:-3px">What your chart<br><b>doesn\'t show you.</b></div><div class=p style="font-size:34px;line-height:50px">Three layers trading desks work from every day. We read them, so you don\'t have to.</div></div>',
 f'<div class=cnt>2 / {{N}}</div><div class=main style="top:220px">{num("01","Order flow")}<div class=h>Who is <b>pushing price.</b></div><div class=p>Order flow shows whether buyers or sellers are in control, and whether that pressure is building or fading as price gets close to a level.</div><div class=card style="margin-top:40px;padding:0;overflow:hidden"><div style="padding:26px 34px"><div class=lab style="font-size:19px;color:#8A98B3">What we analyze</div><div style="font-size:27px;line-height:40px;margin-top:10px;color:#B9C3D6">Order-flow delta over 6 hours, 24 hours and 5 days, from institutional market data.</div></div><div style="padding:26px 34px;background:#13284A;border-top:3px solid #62A5F4"><div class=lab style="font-size:19px">What you read in the report</div><div style="font-size:31px;line-height:44px;margin-top:10px;color:#FFFFFF;font-weight:500">&ldquo;Over the last six hours, that selling has almost dried up.&rdquo;</div></div></div><div class=cap>Illustrative example</div></div>',
 f'<div class=cnt>3 / {{N}}</div><div class=main style="top:220px">{num("02","Volume")}<div class=h>Where heavy volume <b>has traded.</b></div><div class=p>Some prices attract far more trading than others, and the market tends to remember them.</div><div class=card style="margin-top:40px;padding:0;overflow:hidden"><div style="padding:26px 34px"><div class=lab style="font-size:19px;color:#8A98B3">What we analyze</div><div style="font-size:27px;line-height:40px;margin-top:10px;color:#B9C3D6">Futures volume by price over recent weeks, and session volume versus the 30-day average.</div></div><div style="padding:26px 34px;background:#13284A;border-top:3px solid #62A5F4"><div class=lab style="font-size:19px">What you read in the report</div><div style="font-size:31px;line-height:44px;margin-top:10px;color:#FFFFFF;font-weight:500">&ldquo;A Volume Node sits inside the zone, where the market often slows down or turns.&rdquo;</div></div></div><div class=cap>Illustrative example</div></div>',
 f'<div class=cnt>4 / {{N}}</div><div class=main style="top:220px">{num("03","Positioning")}<div class=h>Where large traders <b>are positioned.</b></div><div class=p>How large institutional traders are positioned in each currency, and which way the interest-rate gap is pulling the pair.</div><div class=card style="margin-top:40px;padding:0;overflow:hidden"><div style="padding:26px 34px"><div class=lab style="font-size:19px;color:#8A98B3">What we analyze</div><div style="font-size:27px;line-height:40px;margin-top:10px;color:#B9C3D6">Large traders\' weekly positioning, the open interest trend and the policy-rate gap.</div></div><div style="padding:26px 34px;background:#13284A;border-top:3px solid #62A5F4"><div class=lab style="font-size:19px">What you read in the report</div><div style="font-size:31px;line-height:44px;margin-top:10px;color:#FFFFFF;font-weight:500">&ldquo;Large institutional traders have held a steady net short position in the Swiss franc all month.&rdquo;</div></div></div><div class=cap>Illustrative example</div></div>',
 f'<div class=cnt>5 / {{N}}</div><div class=main style="top:250px">{num("04","The real gap")}<div class=h>The basics are public. <b>The depth isn\'t.</b></div><div class=p>Weekly positioning reports and central bank rates are free, if scattered. Order flow and futures volume data is restricted and expensive. That is the real gap between retail and institutional traders.</div><div class=card style="margin-top:40px;padding:0;display:flex;overflow:hidden"><div style="flex:1;padding:30px 32px"><div class=lab style="font-size:19px;color:#8A98B3">Public</div><div style="font-size:28px;line-height:44px;margin-top:16px;color:#B9C3D6">Weekly positioning<br>Central bank rates<br>Economic calendar</div></div><div style="flex:1;padding:30px 32px;background:#13284A;border-left:3px solid #62A5F4"><div class=lab style="font-size:19px">Restricted and expensive</div><div style="font-size:28px;line-height:44px;margin-top:16px;color:#FFFFFF">Order flow<br>Futures volume by price<br>Session volume vs. normal</div></div></div></div>',
 '{LOGO}<div class=cnt>6 / {N}</div><div class=main style="top:235px"><div class=lab>The waitlist is open</div><div class=h style="font-size:84px;line-height:90px;letter-spacing:-2.6px">We analyze and process the data.<br><b>You get a clear report.</b></div><div class=card style="margin-top:46px;border-top:4px solid #62A5F4"><div class=chk><span>&#10003;</span>Zones of interest on the 7 major FX pairs.</div><div class=chk><span>&#10003;</span>Institutional data, in plain language.</div><div class=chk><span>&#10003;</span>Notified by Telegram or email.</div></div><div class=btn><div>Link in bio</div><span>fxmarketmap.com</span></div></div>',
]
build(S,'P30','en',navy=True)
