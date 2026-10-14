# Build a paced timeline: voice lines with pauses, music bed, EN/ES subtitles, and a JSON of line start times.
import json,sys,numpy as np,soundfile as sf,scipy.signal as ss
def build(name,lines,gap=0.9,extra=None,lead=0.6,tail=1.2,endcard=3.4):
    """lines: list of (wav, en, es). extra: {index: extra_pause_before}"""
    extra=extra or {}
    SR=24000;t=lead;starts=[];durs=[];clips=[]
    for i,(w,en,es) in enumerate(lines):
        a,r=sf.read(w);a=a if a.ndim==1 else a.mean(1)
        if r!=SR:a=ss.resample_poly(a,SR,r)
        nz=np.where(np.abs(a)>0.004)[0];a=a[max(0,nz[0]-int(.03*SR)):nz[-1]+int(.08*SR)]
        t+=extra.get(i,0);starts.append(round(t,3));durs.append(round(len(a)/SR,3));clips.append(a);t+=len(a)/SR+gap
    t=t-gap+tail;body=t;total=t+endcard
    N=int(total*SR);voice=np.zeros(N)
    for s,a in zip(starts,clips):i=int(s*SR);voice[i:i+len(a)]+=a
    voice*=(10**(-18/20))/np.sqrt((voice[np.abs(voice)>0.01]**2).mean())
    m,mr=sf.read('/home/claude/post11/m4_loop.wav');m=m.mean(1) if m.ndim>1 else m;m=ss.resample_poly(m,SR,mr)
    xf=int(1.5*SR);bed=m.copy()
    while len(bed)<N:
        u=np.linspace(0,1,xf);bed=np.concatenate([bed[:-xf],bed[-xf:]*(1-u)+m[:xf]*u,m[xf:]])
    bed=bed[:N];bed*=(10**(-29/20))/np.sqrt((bed**2).mean())
    fo=int(2.5*SR);bed[N-fo:]*=np.linspace(1,0,fo);bed[:int(.5*SR)]*=np.linspace(0,1,int(.5*SR))
    mix=voice+bed;mix/=max(1,np.abs(mix).max()/0.97);sf.write(f'{name}.wav',mix,SR)
    def fmt(x):h=int(x//3600);mi=int(x%3600//60);s=x%60;return f'{h:02d}:{mi:02d}:{s:06.3f}'.replace('.',',')
    def wrap(t,n=46):
        if len(t)<=n or '\n' in t:return t
        w=t.split(' ');best=None
        for i in range(1,len(w)):
            a_,b_=' '.join(w[:i]),' '.join(w[i:]);d=abs(len(a_)-len(b_))
            if best is None or d<best[0]:best=(d,a_+'\n'+b_)
        return best[1]
    for k,lang in ((1,'en'),(2,'es')):
        with open(f'{name}_{lang}.srt','w') as f:
            for i,(s,d) in enumerate(zip(starts,durs)):
                f.write(f"{i+1}\n{fmt(s)} --> {fmt(s+d+0.25)}\n{wrap(lines[i][k])}\n\n")
    json.dump({'L':starts,'D':durs,'body':round(body,3),'total':round(total,3)},open(f'{name}.json','w'))
    return starts,durs,body,total
