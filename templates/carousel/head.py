import asyncio,os
from playwright.async_api import async_playwright
N=6
CSS='''@font-face{font-family:P;font-weight:300;src:url(poppins-latin-300-normal.woff2)}@font-face{font-family:P;font-weight:400;src:url(poppins-latin-400-normal.woff2)}@font-face{font-family:P;font-weight:500;src:url(poppins-latin-500-normal.woff2)}@font-face{font-family:P;font-weight:600;src:url(poppins-latin-600-normal.woff2)}@font-face{font-family:M;font-weight:500;src:url(jetbrains-mono-latin-500-normal.woff2)}@font-face{font-family:M;font-weight:700;src:url(jetbrains-mono-latin-700-normal.woff2)}
body{margin:0;width:1080px;height:1350px;background:#F7F6F2;font-family:P;position:relative;overflow:hidden;color:#121821}
.wm{position:absolute;right:-170px;bottom:-190px;width:800px}
.logo{position:absolute;left:84px;top:88px;height:44px}
.cnt{position:absolute;right:84px;top:92px;font-family:M;font-size:22px;color:#5A6270;letter-spacing:6px}
.lab{font-size:23px;font-weight:600;letter-spacing:5px;color:#0060C7;text-transform:uppercase}
.num{font-family:M;font-weight:700;font-size:110px;color:#0060C7;line-height:1;margin-right:26px}
.h{font-size:76px;font-weight:600;line-height:82px;letter-spacing:-2.4px;margin-top:22px}.h b{font-weight:600;color:#0060C7}
.p{font-size:31px;font-weight:300;line-height:46px;color:#3F4754;margin-top:26px}
.main{position:absolute;left:84px;right:84px;top:200px}
.foot{position:absolute;left:84px;right:84px;bottom:52px;border-top:1px solid #E1E2E0;padding-top:48px;display:flex;justify-content:space-between;align-items:center}
.dots{display:flex;gap:8px}.dots i{width:26px;height:4px;border-radius:2px;background:#DCDDDA}.dots i.on{width:26px;background:#0060C7}
.sw{font-size:22px;font-weight:500;color:#3F4754}
.card{background:#fff;border:1px solid #E6E7E4;border-radius:12px;box-shadow:0 12px 30px rgba(18,24,33,.06);padding:34px 36px}
.chk{display:flex;gap:22px;align-items:center;font-size:31px;font-weight:400;margin:14px 0}.chk span{width:38px;height:38px;border-radius:50%;background:#E6EFFC;color:#0060C7;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:600;flex:none}
.btn{display:flex;align-items:center;gap:26px;margin-top:40px}.btn div{background:#007DFF;color:#fff;font-weight:600;font-size:33px;padding:26px 46px}.btn span{font-family:M;font-size:30px}
'''
WM='<img class=wm src=wmI.png>'
def foot(i,last=False):
  d=''.join(f'<i class="{"on" if k==i else ""}"></i>' for k in range(N))
  return f'<div class=foot><div class=dots>{d}</div><div class=sw>{"Guárdalo para después" if last else "Desliza &rarr;"}</div></div>'

CSS+='''
.cap{font-family:M;font-size:19px;color:#6B7280;margin-top:14px}
.bar{display:flex;align-items:center;gap:20px;font-size:26px;font-weight:500;margin:16px 0}.bar .t{width:150px;color:#3F4754}.bar .b{height:34px;border-radius:4px}.bar .v{font-family:M;font-size:24px;color:#121821}
.rate{flex:1;text-align:center;padding:26px 10px}.rate .n{font-family:M;font-weight:700;font-size:58px;color:#121821}.rate .l{font-size:22px;color:#5A6270;margin-top:6px}
'''
