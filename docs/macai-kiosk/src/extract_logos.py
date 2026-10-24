import sys,base64,io,json
from PIL import Image
import numpy as np
d=sys.argv[1]
p1=Image.open(d+'/hi-01.png').convert('RGB'); p6=Image.open(d+'/hi-06.png').convert('RGB')
def crop(im,box):
    s=im.size[0]/1063
    return np.asarray(im.crop(tuple(int(v*s) for v in box))).astype(float)
def mask_from_purple(a):  # coral on purple: use red channel
    return np.clip((a[...,0]-55)/(244-55),0,1)
def mask_from_white(a):   # purple on white
    return np.clip((255-a[...,1])/(255-28),0,1)
def tight(m,pad=4):
    ys,xs=np.where(m>0.05); return m[max(ys.min()-pad,0):ys.max()+pad,max(xs.min()-pad,0):xs.max()+pad]
out={}
specs={'primary':(p1,(255,330,810,735),mask_from_purple),'symbol':(p1,(420,335,640,535),mask_from_purple),
 'horizontal':(p6,(195,222,870,400),mask_from_white),'badge':(p6,(185,490,465,795),mask_from_white),'stacked':(p6,(570,500,900,770),mask_from_white)}
for k,(im,box,f) in specs.items():
    m=tight(f(crop(im,box)))
    h,w=m.shape; sc=min(1.0,1400/w)
    img=Image.new('LA',(w,h)); img.putdata([(255,int(v*255)) for v in m.flatten()])
    if sc<1: img=img.resize((int(w*sc),int(h*sc)),Image.LANCZOS)
    b=io.BytesIO(); img.save(b,'PNG',optimize=True)
    out[k]={'w':img.size[0],'h':img.size[1],'src':'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()}
    img.save(d+f'/logo_{k}.png'); print(k,img.size,len(b.getvalue()))
json.dump(out,open(d+'/logos.json','w'))
