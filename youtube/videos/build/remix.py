import os,sys,subprocess,numpy as np,soundfile as sf,scipy.signal as ss
from kokoro_onnx import Kokoro
U='/root/.claude/uploads/cbb6d3c3-4810-58c4-9f88-c47f5c3a912f/'
K=Kokoro("/home/claude/tts/kokoro-v1.0.onnx","/home/claude/tts/voices-v1.0.bin")
def ts(t):h,m,s=t.replace(',','.').split(':');return int(h)*3600+int(m)*60+float(s)
n=sys.argv[1]; src=[U+f for f in os.listdir(U) if f'Education_{n}' in f][0]
subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-map','0:2',f'en{n}.srt'],check=True)
bl=open(f'en{n}.srt').read().strip().split('\n\n')
raw=[(ts(b.split('\n')[1].split(' --> ')[0]),ts(b.split('\n')[1].split(' --> ')[1]),' '.join(b.split('\n')[2:])) for b in bl]
segs=[]
for s0,e0,t0 in raw:
    if segs and s0-segs[-1][2]<0.05: segs[-1]=(segs[-1][0],segs[-1][1]+' '+t0,e0)
    else: segs.append((s0,t0,e0))
LASTEND=segs[-1][2]+0.3
segs=[(a,b) for a,b,c in segs]
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]))
SR=24000;N=int(dur*SR)+SR;voice=np.zeros(N);os.makedirs('raw',exist_ok=True)
for k,(s,t) in enumerate(segs):
    fn=f'raw/o{n}_{k:02d}.wav'
    a,r=K.create(t,voice='af_heart',speed=1.0,lang='en-us')
    nxt=segs[k+1][0] if k+1<len(segs) else LASTEND
    nz=np.where(np.abs(a)>0.01)[0]; end=nz[-1]/r
    room=nxt-s-0.08
    if end>room:
        f=min(1.25,end/room); sf.write('/tmp/x.wav',a,r)
        subprocess.run(['ffmpeg','-v','error','-y','-i','/tmp/x.wav','-af',f'atempo={f:.3f}',fn],check=True); a,r=sf.read(fn)
        print('stretched',k,round(f,3))
    sf.write(fn,a,r)
    i=int(s*SR); voice[i:i+len(a)]+=a[:max(0,N-i)]
rms=lambda x:np.sqrt((x[np.abs(x)>0.01]**2).mean())
voice*=(10**(-18/20))/rms(voice)
m,mr=sf.read('/home/claude/post11/m4_loop.wav'); m=m.mean(1) if m.ndim>1 else m; m=ss.resample_poly(m,SR,mr)
xf=int(1.5*SR); bed=m.copy()
while len(bed)<N:
    t=np.linspace(0,1,xf); bed=np.concatenate([bed[:-xf],bed[-xf:]*(1-t)+m[:xf]*t,m[xf:]])
bed=bed[:N]; bed*=(10**(-29/20))/np.sqrt((bed**2).mean())
end=int(dur*SR); fo=int(2.5*SR); bed[end-fo:end]*=np.linspace(1,0,fo); bed[end:]=0; bed[:int(.5*SR)]*=np.linspace(0,1,int(.5*SR))
mix=(voice+bed)[:end]; mix/=max(1,np.abs(mix).max()/0.97); sf.write(f'a{n}.wav',mix,SR)
out=os.path.basename(src).split('-',1)[1].replace('.mp4','_v2.mp4')
subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-i',f'a{n}.wav','-map','0:v','-map','1:a','-map','0:s','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-c:s','copy',out],check=True)
print('done',out,dur)
