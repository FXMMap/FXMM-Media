import os, sys, subprocess, json, numpy as np, soundfile as sf
from playwright.sync_api import sync_playwright
import scipy.signal as ss
os.chdir('/home/claude/edu_ext')
U='/root/.claude/uploads/cbb6d3c3-4810-58c4-9f88-c47f5c3a912f/'
SRC={'01':U+'10262d3c-FXMM_Education_01_Prepare_your_chart.mp4','03':U+'1e98e5a4-FXMM_Education_03_Rejection_at_the_zone.mp4'}
FPS=30
which=sys.argv[1]
CFG={
 '01':dict(cut=728,resume=728,ins=726,fn='draw01',tag='n01',
           starts=[0.3,3.0,6.1,9.5,15.6,21.15],drop=[]),
 '03':dict(cut=1717,resume=1923,ins=912,fn='draw03',tag='n03',
           starts=[0.15,5.25,10.95,15.17,19.2,21.1,26.1],drop=[19]),  # index 19 = original line 20 (0-based)
}[which]
NEW_ES={'n01':["Cada nivel de tu gráfico está ahí por una razón.",
 "Los dos bordes muestran dónde empieza\ny dónde termina la zona.",
 "Los niveles clave muestran dónde es más\nprobable que empiece una reacción.",
 "Salen de datos institucionales: un CME Volume Node,\nun options cluster o el gamma flip.",
 "Así, cuando suena la alerta, no empiezas de cero.\nTodo ya está en tu gráfico.",
 "Solo queda esperar un rechazo."],
 'n03':["Un doble piso: el precio prueba la zona, rebota\ny vuelve para una segunda prueba.",
 "El segundo mínimo aguanta en el primero o más arriba.\nLos vendedores lo intentaron dos veces y no pudieron bajarlo.",
 "Una morning star: una vela bajista fuerte,\ndespués una chica que duda,",
 "y luego una vela alcista fuerte que cierra\npor encima de la mitad de la primera.",
 "El impulso acaba de cambiar.",
 "Una ruptura de estructura en M5: en la bajada,\nel precio va marcando máximos cada vez más bajos.",
 "Cuando rompe por encima del último,\nla caída en esa temporalidad terminó."]}
def wrap(t,n=46):
    if len(t)<=n: return t
    w=t.split(' ');best=None
    for i in range(1,len(w)):
        a,b=' '.join(w[:i]),' '.join(w[i:]);d=abs(len(a)-len(b))
        if best is None or d<best[0]: best=(d,a+'\n'+b)
    return best[1]
cut_t=CFG['cut']/FPS; res_t=CFG['resume']/FPS; ins_t=CFG['ins']/FPS
shift=cut_t+ins_t-res_t
def ts(t):h,m,s=t.replace(',','.').split(':');return int(h)*3600+int(m)*60+float(s)
def fmt(t):t=max(0,t);h=int(t//3600);m=int(t%3600//60);s=t%60;return f'{h:02d}:{m:02d}:{s:06.3f}'.replace('.',',')
def parse(p):
    out=[]
    for b in open(p).read().strip().split('\n\n'):
        l=b.split('\n'); a,c=l[1].split(' --> '); out.append([ts(a),ts(c),'\n'.join(l[2:])])
    return out
nl=json.load(open('newlines.json'))[CFG['tag']]
# ---------- 1) render insert ----------
ins_mp4=f'ins{which}.mp4'
if not os.path.exists(ins_mp4):
    ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','image2pipe','-framerate',str(FPS),'-i','-','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p',ins_mp4],stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080})
        pg.goto('file://'+os.getcwd()+'/r.html'); pg.evaluate('window.ready')
        for i in range(CFG['ins']):
            pg.evaluate(f"{CFG['fn']}({i/FPS})")
            ff.stdin.write(pg.screenshot(type='jpeg',quality=95))
            if i%150==0: print('frame',i,flush=True)
        b.close()
    ff.stdin.close(); ff.wait()
# ---------- 2) video assembly ----------
src=SRC[which]
vid=f'v{which}.mp4'
fc=(f"[0:v]trim=start_frame=0:end_frame={CFG['cut']},setpts=PTS-STARTPTS[a];"
    f"[0:v]trim=start_frame={CFG['resume']},setpts=PTS-STARTPTS[c];"
    f"[1:v]setpts=PTS-STARTPTS[b];[a][b][c]concat=n=3:v=1:a=0,format=yuv420p[v]")
subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-i',ins_mp4,'-filter_complex',fc,'-map','[v]','-r','30','-c:v','libx264','-preset','medium','-crf','17',vid],check=True)
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',vid]))
# ---------- 3) subtitles + voice timeline ----------
en=parse(f'en{which}.srt'); es=parse(f'es{which}.srt')
def remap(lst,drop_idx):
    out=[]
    for i,(s,e,t) in enumerate(lst):
        if i in drop_idx: continue
        if s<cut_t-0.001: out.append([s,min(e,cut_t),t,i])
        else:
            s2=max(s+shift,cut_t+ins_t); out.append([s2,e+shift,t,i])
    return out
en2=remap(en,CFG['drop'])
# es drop: entries whose start falls inside the removed window [cut_t,res_t) except those that continue past resume
es_drop=[i for i,(s,e,t) in enumerate(es) if (cut_t-0.6)<=s<res_t-1.5] if which=='03' else []
es2=remap(es,es_drop)
newen=[[cut_t+st,cut_t+st+nl[k][1],wrap(nl[k][0]),'new'] for k,st in enumerate(CFG['starts'])]
newes=[[cut_t+st,cut_t+st+nl[k][1],NEW_ES[CFG['tag']][k],'new'] for k,st in enumerate(CFG['starts'])]
def write(lst,fn):
    lst=sorted(lst,key=lambda x:x[0])
    with open(fn,'w') as f:
        for i,(s,e,t,_) in enumerate(lst,1): f.write(f"{i}\n{fmt(s)} --> {fmt(e)}\n{t}\n\n")
write(en2+newen,f'en{which}_long.srt'); write(es2+newes,f'es{which}_long.srt')
# ---------- 4) audio ----------
SR=24000; N=int(dur*SR)+SR; voice=np.zeros(N)
def put(wav,t):
    a,r=sf.read(wav); a=a if a.ndim==1 else a.mean(1)
    if r!=SR: a=ss.resample_poly(a,SR,r)
    i=int(t*SR); voice[i:i+len(a)]+=a[:max(0,N-i)]
for k,(s,e,t) in enumerate(en):
    if k in CFG['drop']: continue
    pass
# original lines (o-files generated from en srt with same indexing, untrimmed)
from kokoro_onnx import Kokoro
K=Kokoro("/home/claude/tts/kokoro-v1.0.onnx","/home/claude/tts/voices-v1.0.bin")
os.makedirs('raw',exist_ok=True)
for k,(s,e,t) in enumerate(en):
    if k in CFG['drop']: continue
    fn=f'raw/o{which}_{k:02d}.wav'
    if not os.path.exists(fn):
        a,r=K.create(t.replace('\n',' '),voice='af_heart',speed=1.0,lang='en-us'); sf.write(fn,a,r)
    put(fn, s if s<cut_t else s+shift)
for k,st in enumerate(CFG['starts']):
    put(f"{CFG['tag']}_{k:02d}.wav",cut_t+st)
rms=lambda x:np.sqrt((x[np.abs(x)>0.01]**2).mean())
voice*= (10**(-18/20))/rms(voice)
m,mr=sf.read('/home/claude/post11/m4_loop.wav'); m=m.mean(1) if m.ndim>1 else m; m=ss.resample_poly(m,SR,mr)
xf=int(1.5*SR); bed=m.copy()
while len(bed)<N:
    t=np.linspace(0,1,xf); bed=np.concatenate([bed[:-xf],bed[-xf:]*(1-t)+m[:xf]*t,m[xf:]])
bed=bed[:N]; bed*=(10**(-29/20))/np.sqrt((bed**2).mean())
fo=int(2.5*SR); end=int(dur*SR); bed[end-fo:end]*=np.linspace(1,0,fo); bed[end:]=0
bed[:int(.5*SR)]*=np.linspace(0,1,int(.5*SR))
mix=(voice+bed)[:end]; mix/=max(1,np.abs(mix).max()/0.97)
sf.write(f'a{which}.wav',mix,SR)
# ---------- 5) mux ----------
names={'01':'FXMM_Education_01_Prepare_your_chart_LONG.mp4','03':'FXMM_Education_03_Rejection_at_the_zone_LONG.mp4'}
subprocess.run(['ffmpeg','-v','error','-y','-i',vid,'-i',f'a{which}.wav','-i',f'en{which}_long.srt','-i',f'es{which}_long.srt',
 '-map','0:v','-map','1:a','-map','2','-map','3','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-c:s','mov_text',
 '-metadata:s:s:0','language=eng','-metadata:s:s:1','language=spa',names[which]],check=True)
print('done',names[which],dur)
