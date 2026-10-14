import json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
k=Kokoro("/home/claude/tts/kokoro-v1.0.onnx","/home/claude/tts/voices-v1.0.bin")
L={
'n03':["A double bottom: price tests the zone, bounces, and comes back for a second test.",
 "The second low holds at or above the first. Sellers tried twice and couldn't push lower.",
 "A morning star: a strong bearish candle, then a small one that hesitates,",
 "then a strong bullish candle that closes past the middle of the first.",
 "Momentum just turned.",
 "A break of structure on M5: on the way down, price keeps making lower highs.",
 "When it breaks above the last one, the drop on that timeframe is over."],
'n01':["Each level on your chart is there for a reason.",
 "The two edges show where the zone starts and where it ends.",
 "The key levels show where a reaction is more likely to start.",
 "They come from institutional data: a CME volume node, an options cluster, or the gamma flip.",
 "So when the alert goes off, you're not starting from zero. Everything is already on your chart.",
 "All that's left is to wait for a rejection."]}
out={}
for tag,lines in L.items():
    out[tag]=[]
    for i,t in enumerate(lines):
        a,r=k.create(t,voice='af_heart',speed=1.0,lang='en-us')
        sf.write(f'{tag}_{i:02d}.wav',a,r); out[tag].append([t,len(a)/r])
        print(tag,i,round(len(a)/r,2),t)
json.dump(out,open('newlines.json','w'),indent=1)
