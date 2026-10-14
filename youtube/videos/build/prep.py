# Group subtitle cues into voice lines, generate af_heart audio per line, map EN/ES cues proportionally.
import os,soundfile as sf,numpy as np
from kokoro_onnx import Kokoro
K=None
def ts(t):h,m,s=t.replace(',','.').split(':');return int(h)*3600+int(m)*60+float(s)
def parse(p):
    out=[]
    for b in open(p).read().strip().split('\n\n'):
        l=b.split('\n');a,c=l[1].split(' --> ');out.append([ts(a),ts(c),'\n'.join(l[2:])])
    return out
def groups(en):
    g=[]
    for s,e,t in en:
        if g and s-g[-1]['e']<0.05: g[-1]['cues'].append((s,e,t));g[-1]['e']=e
        else: g.append({'s':s,'e':e,'cues':[(s,e,t)]})
    return g
def prep(n,voice='af_heart'):
    global K
    if K is None: K=Kokoro("/home/claude/tts/kokoro-v1.0.onnx","/home/claude/tts/voices-v1.0.bin")
    en=parse(f'en{n}.srt');es=parse(f'es{n}.srt');G=groups(en);os.makedirs('gv',exist_ok=True);lines=[]
    for k,g in enumerate(G):
        span=g['e']-g['s']
        txt=' '.join(c[2].replace('\n',' ') for c in g['cues'])
        fn=f'gv/{n}_{k:02d}.wav'
        if not os.path.exists(fn):
            a,r=K.create(txt,voice=voice,speed=1.0,lang='en-us');sf.write(fn,a,r)
        enc=[((c[0]-g['s'])/span,c[2]) for c in g['cues']]
        esc=[((c[0]-g['s'])/span,c[2]) for c in es if g['s']-0.15<=c[0]<g['e']-0.05]
        if not esc: esc=[(0,'')]
        esc=[(max(0,f),t) for f,t in esc]
        lines.append((fn,enc,esc,txt))
    return lines
