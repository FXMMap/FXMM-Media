import os,sys,subprocess
from playwright.sync_api import sync_playwright
html,dur,audio,en,es,out=sys.argv[1],float(sys.argv[2]),sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6]
N=int(round(dur*30)); tmp=out.replace('.mp4','_v.mp4')
ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','image2pipe','-framerate','30','-i','-','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p',tmp],stdin=subprocess.PIPE)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080})
    pg.goto('file://'+os.getcwd()+'/'+html); pg.evaluate('window.ready')
    for i in range(N):
        pg.evaluate(f'draw({i/30})'); ff.stdin.write(pg.screenshot(type='jpeg',quality=94))
        if i%300==0: print(i,flush=True)
    b.close()
ff.stdin.close(); ff.wait()
subprocess.run(['ffmpeg','-v','error','-y','-i',tmp,'-i',audio,'-i',en,'-i',es,'-map','0:v','-map','1:a','-map','2','-map','3','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-c:s','mov_text','-metadata:s:s:0','language=eng','-metadata:s:s:1','language=spa',out],check=True)
os.remove(tmp); print('done',out)
