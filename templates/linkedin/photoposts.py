from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
B='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
SB='/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
M='/usr/share/fonts/opentype/inter/Inter-Medium.otf'
NAVY=(13,24,46); BLUE='#62A5F4'
logo=Image.open('logo.png').convert('RGBA')

def coeffs(dst, src):
    A=[];b=[]
    for (x,y),(u,v) in zip(dst,src):
        A.append([x,y,1,0,0,0,-u*x,-u*y]); b.append(u)
        A.append([0,0,0,x,y,1,-v*x,-v*y]); b.append(v)
    return np.linalg.solve(np.array(A,float),np.array(b,float)).tolist()

def screen():
    W,H=600,1300
    s=Image.new('RGB',(W,H),(9,20,40)); d=ImageDraw.Draw(s)
    d.text((W//2,150),'9:41',font=ImageFont.truetype(B,120),fill=(230,236,245),anchor='mm')
    d.text((W//2,235),'Tuesday, October 13',font=ImageFont.truetype(M,30),fill=(170,185,210),anchor='mm')
    x0,y0,x1,y1=34,420,W-34,700
    d.rounded_rectangle((x0,y0,x1,y1),36,fill=(236,240,247))
    ic=logo.crop((0,0,int(logo.height*1.45),logo.height)); ic=ic.resize((52,int(52*ic.height/ic.width)))
    d.rounded_rectangle((x0+26,y0+28,x0+92,y0+94),14,fill=NAVY); s.paste(ic,(x0+33,y0+61-ic.height//2),ic)
    d.text((x0+110,y0+36),'FXMM',font=ImageFont.truetype(SB,30),fill=(30,40,60))
    d.text((x1-28,y0+38),'now',font=ImageFont.truetype(M,26),fill=(120,130,150),anchor='ra')
    d.text((x0+110,y0+74),'Telegram',font=ImageFont.truetype(M,22),fill=(120,130,150))
    d.text((x0+28,y0+130),'Zone of interest · EUR/USD',font=ImageFont.truetype(SB,32),fill=(15,25,45))
    d.text((x0+28,y0+178),'Buying interest · 1.0885 – 1.0915',font=ImageFont.truetype(M,27),fill=(60,70,90))
    d.text((x0+28,y0+218),'Confluence grade: Heavy',font=ImageFont.truetype(M,27),fill=(47,95,196))
    return s

def phone_photo():
    ph=Image.open('photos/p2.png').convert('RGB')
    dst=[(752,197),(1028,152),(1318,822),(1012,906)]
    s=screen()
    c=coeffs([(0,0),(600,0),(600,1300),(0,1300)] and dst,[(0,0),(600,0),(600,1300),(0,1300)])
    warped=s.transform(ph.size,Image.PERSPECTIVE,c,Image.BICUBIC)
    mask=Image.new('L',ph.size,0); ImageDraw.Draw(mask).polygon(dst,fill=255)
    mask=mask.filter(ImageFilter.GaussianBlur(1.2))
    # keep a little glass shading
    out=Image.composite(warped,ph,mask)
    return out

def post(photo,box,l1,l2,name):
    cv=Image.new('RGB',(1200,1500),NAVY); d=ImageDraw.Draw(cv)
    f=ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf',58)
    d.text((70,118),l1,font=f,fill='white'); d.text((70,196),l2,font=f,fill=BLUE)
    lg=logo.resize((int(logo.width*36/logo.height),36)); cv.paste(lg,(1200-70-lg.width,48),lg)
    ph=photo.crop(box).resize((1200,1100),Image.LANCZOS)
    cv.paste(ph,(0,400))
    # soft blend line
    g=Image.new('L',(1200,60)); 
    for y in range(60): ImageDraw.Draw(g).line((0,y,1200,y),fill=int(255*(1-y/60)))
    cv.paste(Image.new('RGB',(1200,60),NAVY),(0,400),g)
    cv.save(f'posts/{name}.png',quality=95)

t2=Image.open('photos/t2.png').convert('RGB')
post(t2,(570,0,1827,1152),'Most traders start with a chart.','Institutions start with positioning.','FXMM_LI_photo1')
post(phone_photo(),(412,0,1669,1152),'A level is a line.','A zone is a decision point.','FXMM_LI_photo2')
b2=Image.open('photos/b2.png').convert('RGB')
post(b2,(428,0,1685,1152),'Stop chasing','the home run.','FXMM_LI_photo3')
