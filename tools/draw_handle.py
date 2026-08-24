#!/usr/bin/env python3
"""Sinh hinh ve thiet ke quai xach hop Mahjong (SVG). python3 tools/draw_handle.py"""
import math, os

C30, S30, YMAX = math.cos(math.radians(30)), 0.5, 350.0

def iso(p, sc):
    x, y, z = p; yp = YMAX - y
    return ((x - yp) * C30 * sc, ((x + yp) * S30 - z) * sc)

def cen(pts): return sum(x + (YMAX-y) + z for x,y,z in pts)/len(pts)

FACES = {
 'top': lambda a,b,c,d,e,f: [(a,c,f),(b,c,f),(b,d,f),(a,d,f)],
 'bot': lambda a,b,c,d,e,f: [(a,c,e),(b,c,e),(b,d,e),(a,d,e)],
 'x+':  lambda a,b,c,d,e,f: [(b,c,e),(b,d,e),(b,d,f),(b,c,f)],
 'x-':  lambda a,b,c,d,e,f: [(a,c,e),(a,d,e),(a,d,f),(a,c,f)],
 'y-':  lambda a,b,c,d,e,f: [(a,c,e),(b,c,e),(b,c,f),(a,c,f)],
 'y+':  lambda a,b,c,d,e,f: [(a,d,e),(b,d,e),(b,d,f),(a,d,f)],
}
SHADE = {'top':1.00,'y-':0.78,'x+':0.58,'x-':0.58,'y+':0.78,'bot':0.42}

def tint(h, f):
    r,g,b = (int(h[i:i+2],16) for i in (1,3,5))
    return '#%02x%02x%02x' % tuple(min(255,int(v*f)) for v in (r,g,b))

class Scene:
    """Painter theo LOP tuong minh; trong cung lop moi sap theo do sau."""
    def __init__(self, sc): self.it, self.sc = [], sc
    def solid(self, layer, x0,x1,y0,y1,z0,z1, col, only=('top','y-','x+'), sw=0.8):
        for w in only:
            p = FACES[w](x0,x1,y0,y1,z0,z1)
            self.it.append((layer, cen(p), p, tint(col,SHADE[w]), '#2a241c', sw))
    def face(self, layer, pts, col, stroke='#2a241c', sw=0.8):
        self.it.append((layer, cen(pts), pts, col, stroke, sw))
    def raw(self, layer, svg): self.it.append((layer, 0, None, svg, None, None))
    def render(self):
        o=[]
        for L,d,pts,col,stroke,sw in sorted(self.it, key=lambda r:(r[0], r[1])):
            if pts is None: o.append(col); continue
            pd=' '.join('%.2f,%.2f'%iso(p,self.sc) for p in pts)
            o.append(f'<polygon points="{pd}" fill="{col}" stroke="{stroke}" '
                     f'stroke-width="{sw}" stroke-linejoin="round"/>')
        return '\n'.join(o)

# --------------------------------------------------------------- kich thuoc
W,D = 354.0, 350.0
Z_FOOT, Z_RIM_H, Z_RIM_S, Z_LID = 2.0, 49.0, 55.0, 67.0
SEAM, SP_X0, SP_X1 = 177.0, 155.0, 199.0
SP_Y0, SP_Y1, SP_Z0, SP_Z1 = -6.0, 356.0, 63.0, 83.0
KEY_Y, SLOT_Y = (4.0, 346.0), (117.0, 237.0)
REC_X0, REC_X1, PIL = 161.0, 193.0, 6.0
CO,CO_D,LID,BODY,LEA,KEY = '#8a5a32','#6b4526','#a9754a','#7a4f2c','#b8823f','#3a2818'

def strap(sc, lift, w=34.0):
    def arc(xoff):
        p=[]
        for i in range(41):
            t=i/40
            y=SLOT_Y[0]+(SLOT_Y[1]-SLOT_Y[0])*t
            p.append(iso((SEAM+xoff, y, SP_Z1+lift+68*math.sin(math.pi*t)**0.66), sc))
        return p
    a,b = arc(-w/2), arc(w/2)
    d='M '+' L '.join('%.2f,%.2f'%q for q in a)+' L '+' L '.join('%.2f,%.2f'%q for q in reversed(b))+' Z'
    return f'<path d="{d}" fill="{LEA}" stroke="#6d4a1c" stroke-width="1" stroke-linejoin="round"/>'

def scene_iso(sc, exploded=False):
    s = Scene(sc); lift = 105.0 if exploded else 0.0
    s.solid(-2, SP_X0,SP_X1, D,D+PIL, Z_FOOT,Z_RIM_S, CO_D, only=('top','x+','y+'))   # tru sau
    s.solid( 0, 4,W-4, 4,D-4, 0,Z_FOOT, '#241d15', only=('y-','x+'))                  # chan
    s.solid( 1, 0,W, 0,D, Z_FOOT,Z_RIM_H, BODY, only=('y-','x+'))                     # than
    s.solid( 2, SP_X0,SP_X1, -PIL,0.0, Z_FOOT,Z_RIM_S, CO_D, only=('top','y-','x+','x-'))
    for i in range(7):                                                                 # mat mong
        a=(i*45)/D
        s.raw(3, '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#4a2f1a" stroke-width="1.3"/>'
              % (*iso((W, i*45, Z_FOOT),sc), *iso((W, i*45, Z_RIM_H),sc)))
    for x0,x1,thin_at in ((0.0,SEAM-0.3,'r'), (SEAM+0.3,W,'l')):                       # canh nap
        s.face(4, FACES['top'](x0,x1,0,D,0,Z_LID), tint(LID,1.0))
        zi,zo = (Z_LID-12,Z_LID-18) if thin_at=='r' else (Z_LID-18,Z_LID-12)
        s.face(4, [(x0,0,zi),(x1,0,zo),(x1,0,Z_LID),(x0,0,Z_LID)], tint(LID,SHADE['y-']))
        if x1==W: s.face(4, FACES['x+'](x0,W,0,D,Z_LID-18,Z_LID), tint(LID,SHADE['x+']))
    s.face(5, FACES['top'](SP_X0,SP_X1,0,D,0,Z_LID), '#5a3d24')                        # ranh am
    if exploded:
        for ky in KEY_Y:                                                               # hoc chot tren nap
            c=iso((SEAM,ky,Z_LID),sc)
            s.raw(6,f'<ellipse cx="{c[0]:.1f}" cy="{c[1]:.1f}" rx="{8.5*C30*sc:.1f}" '
                    f'ry="{8.5*S30*sc:.1f}" fill="#241811" stroke="#0f0a06" stroke-width="1"/>')
    s.solid(7, SP_X0,SP_X1, SP_Y0,SP_Y1, SP_Z0+lift,SP_Z1+lift, CO,
            only=('top','y-','x+','x-')+(('bot',) if exploded else ()))
    s.face(8, FACES['top'](REC_X0,REC_X1,105,249,0,SP_Z1+lift-0.3), '#5a3d24')         # hoc quai
    for ky in KEY_Y:                                                                   # chot
        c=iso((SEAM,ky,SP_Z1+lift),sc)
        s.raw(9, f'<ellipse cx="{c[0]:.1f}" cy="{c[1]:.1f}" rx="{16*C30*sc:.1f}" '
                 f'ry="{16*S30*sc:.1f}" fill="{KEY}" stroke="#1a1208" stroke-width="0.9"/>'
                 f'<line x1="{c[0]-11*C30*sc:.1f}" y1="{c[1]-11*S30*sc:.1f}" '
                 f'x2="{c[0]+11*C30*sc:.1f}" y2="{c[1]+11*S30*sc:.1f}" '
                 f'stroke="#cbb68b" stroke-width="1.8" stroke-linecap="round"/>')
        if exploded:
            s.solid(6.5, SEAM-8,SEAM+8, ky-8,ky+8, SP_Z0+lift-30, SP_Z0+lift, KEY,
                    only=('y-','x+'))
            s.solid(6.6, SEAM-13,SEAM+13, ky-4,ky+4, SP_Z0+lift-38, SP_Z0+lift-30, KEY,
                    only=('top','y-','x+'))
            t=iso((SEAM,ky,Z_LID),sc)
            s.raw(6.7, f'<line x1="{c[0]:.1f}" y1="{c[1]+14:.1f}" x2="{t[0]:.1f}" y2="{t[1]-6:.1f}" '
                       f'stroke="#a8332a" stroke-width="1.1" stroke-dasharray="5,4"/>')
    for sy_ in SLOT_Y:
        c=iso((SEAM,sy_,SP_Z1+lift),sc)
        s.raw(9.5, f'<ellipse cx="{c[0]:.1f}" cy="{c[1]:.1f}" rx="{17*C30*sc:.1f}" '
                   f'ry="{5*S30*sc+2:.1f}" fill="#4a3220"/>')
    s.raw(10, strap(sc, lift))
    return s.render()

# --------------------------------------------------------------------- xuat
def svg(w,h,body): return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
    f'viewBox="0 0 {w} {h}" font-family="DejaVu Sans" font-size="11.5">'
    f'<rect width="100%" height="100%" fill="#faf9f6"/>{body}</svg>')
def T(x,y,t,**k):
    a=' '.join(f'{kk.replace("_","-")}="{v}"' for kk,v in k.items())
    return f'<text x="{x}" y="{y}" {a}>{t}</text>'
def lead(x,y,px,py,anchor):
    dx = -8 if anchor=='end' else 8
    return (f'<polyline points="{x+dx},{y-4} {(x+dx+px)/2},{y-4} {px},{py}" fill="none" '
            f'stroke="#6b6862" stroke-width="0.9"/><circle cx="{px}" cy="{py}" r="2.2" fill="#6b6862"/>')
def annot(items):
    o=[]
    for x,y,px,py,txt in items:
        a='end' if x>470 else 'start'
        o.append(lead(x,y,px,py,a)); o.append(T(x,y,txt,text_anchor=a))
    return ''.join(o)

os.makedirs('figs',exist_ok=True)
SC, OX, OY = 0.70, 470, 248

hdr = lambda t,s1,s2: (T(28,32,t,font_size=15.5,font_weight='bold')
                     + T(28,52,s1,fill='#55524b') + T(28,68,s2,fill='#55524b'))

open('figs/fig1-tong-the.svg','w').write(svg(940,548,
  hdr('HÌNH 1 — Hộp đóng: sống khóa và quai da tại chính giữa',
      'Tâm nắm tay trùng trọng tâm hộp (X 177, Y 175) → hộp treo NGANG, khay nằm yên trong khoang.',
      'Toàn bộ bằng gỗ và da, không một chi tiết kim loại. Phủ bì 354 × 362 × 83 mm.')
  + f'<g transform="translate({OX},{OY})">{scene_iso(SC)}</g>'
  + annot([
      (706,140, 500,186, 'Quai da bò bridle 30 × 4, gấp đôi'),
      (706,157, 470,206, 'thông tay 120 · lọt ngón 55'),
      (150,236, 318,258, 'Sống khóa cocobolo 44 × 20'),
      (150,253, 330,272, 'đè lên cả hai cánh nắp → chính là khóa'),
      (792,236, 578,252, 'Chốt xoay 1/4 vòng, gỗ cứng'),
      (792,253, 590,268, 'Ø16, cắm xuống trụ vách sau'),
      (126,414, 356,420, 'Trụ gia cố: vách 10 → 20 mm'),
      (126,431, 350,434, 'tại băng X 155–199'),
      (846,368, 606,404, 'Mặt mộng bản lề — không'),
      (846,385, 596,412, 'thể neo quai vào vách này'),
  ])))

open('figs/fig2-thao-roi.svg','w').write(svg(940,596,
  hdr('HÌNH 2 — Tháo rời: xoay chốt 90°, nhấc sống khóa ra',
      'Lưỡi ngang 26 × 8 nhả khỏi ngàm trong trụ → hai cánh nắp tự do mở.',
      'Sống được bắt cứng vào cánh trái nên không thành chi tiết rời — mở cánh trái là sống đi theo.')
  + f'<g transform="translate({OX},{OY+40})">{scene_iso(SC,True)}</g>'
  + annot([
      (700,182, 556,230, 'Thân chốt Ø16 × 46'),
      (700,199, 548,258, 'Lưỡi ngang 26 × 8 ở chân chốt'),
      (140,300, 322,322, 'Rãnh âm 44 × sâu 4 trên mặt nắp'),
      (140,317, 340,342, '(nắp dày 12 tại khe → còn 8 mm)'),
      (770,404, 620,372, 'Hốc bán nguyệt R8,5 khoét vào'),
      (770,421, 606,390, 'đầu mỗi cánh → thành lỗ Ø17'),
      (140,470, 366,432, 'Ngàm trong trụ: khe 26 × 9'),
      (140,487, 372,446, 'mở vào hốc 30 × 18 sâu 18'),
  ])))
print('ok')

# =====================================================================
#  HINH 3/4/5 — ban ve 2D
# =====================================================================
class V:
    """He toa do 2D: goc (ox,oz) la diem (x=0,z=0), s = px/mm, z huong len."""
    def __init__(self, ox, oz, s): self.ox, self.oz, self.s = ox, oz, s
    def X(self, v): return self.ox + v*self.s
    def Z(self, v): return self.oz - v*self.s
    def rect(self, x0,x1,z0,z1, fill, st='#2a241c', sw=0.9):
        return (f'<rect x="{self.X(x0):.1f}" y="{self.Z(z1):.1f}" width="{(x1-x0)*self.s:.1f}" '
                f'height="{(z1-z0)*self.s:.1f}" fill="{fill}" stroke="{st}" stroke-width="{sw}"/>')
    def poly(self, pts, fill, st='#2a241c', sw=0.9):
        d=' '.join(f'{self.X(a):.1f},{self.Z(b):.1f}' for a,b in pts)
        return f'<polygon points="{d}" fill="{fill}" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"/>'
    def dim(self, x0,x1,z, label, dy=0, col='#55524b'):
        a,b,y=self.X(x0),self.X(x1),self.Z(z)+dy
        return (f'<line x1="{a:.1f}" y1="{y:.1f}" x2="{b:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="0.8"/>'
                f'<line x1="{a:.1f}" y1="{y-3:.1f}" x2="{a:.1f}" y2="{y+3:.1f}" stroke="{col}" stroke-width="0.8"/>'
                f'<line x1="{b:.1f}" y1="{y-3:.1f}" x2="{b:.1f}" y2="{y+3:.1f}" stroke="{col}" stroke-width="0.8"/>'
                f'<text x="{(a+b)/2:.1f}" y="{y-4:.1f}" text-anchor="middle" font-size="10" fill="{col}">{label}</text>')

def arrow(x1,y1,x2,y2,col,w=2.0,head=6):
    a=math.atan2(y2-y1,x2-x1)
    p=[(x2-head*math.cos(a-0.42), y2-head*math.sin(a-0.42)),
       (x2-head*math.cos(a+0.42), y2-head*math.sin(a+0.42))]
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" '
            f'stroke-width="{w}" stroke-linecap="round"/><polygon points="{x2:.1f},{y2:.1f} '
            f'{p[0][0]:.1f},{p[0][1]:.1f} {p[1][0]:.1f},{p[1][1]:.1f}" fill="{col}"/>')

def rim(x): return 49 + 6*(1 - abs(x-177)/177)

def sec_body(v, tiles=True):
    o=[v.rect(4,350,0,2,'#241d15'), v.rect(0,354,2,10,'#6b4526')]
    for x0,x1 in ((0,10),(136,142),(212,218),(344,354)):
        o.append(v.poly([(x0,10),(x1,10),(x1,rim(x1)),(x0,rim(x0))],'#7a4f2c'))
    for x0,x1 in ((10,136),(218,344)):
        for k in (0,1):
            z0=10+19*k
            o.append(v.rect(x0+1,x1-1,z0,z0+19,'#c2ab84',sw=0.8))
            if tiles:
                for i in range(3):
                    tx=x0+7+i*40
                    o.append(v.rect(tx,tx+33,z0+4.8,z0+16,'#e6dcc4','#9a8a68',0.6))
    o.append(v.rect(143,211,10,48,'#b39a72'))
    o.append(f'<text x="{v.X(177):.1f}" y="{v.Z(26):.1f}" text-anchor="middle" font-size="9" fill="#4a3c28">AC-01</text>')
    return ''.join(o)

def sec_lid(v, spine=True, x_lo=0.0, x_hi=354.0):
    o=[]
    for x0,x1,ti,to in ((0,176.7,49,55),(177.3,354,55,49)):
        a,b=max(x0,x_lo),min(x1,x_hi)
        if b<=a: continue
        f=lambda xx: ti+(to-ti)*(xx-x0)/(x1-x0)
        o.append(v.poly([(a,f(a)),(b,f(b)),(b,67),(a,67)],'#a9754a'))
    if spine:
        for x0,x1 in ((155,176.7),(177.3,199)):
            o.append(v.rect(x0,x1,63,67,'#faf9f6','#faf9f6',0))
            o.append(f'<line x1="{v.X(x0):.1f}" y1="{v.Z(63):.1f}" x2="{v.X(x1):.1f}" '
                     f'y2="{v.Z(63):.1f}" stroke="#2a241c" stroke-width="0.9"/>')
        o.append(v.rect(155,199,63,83,'#8a5a32',sw=1.1))
        o.append(v.rect(161,193,73,83,'#5a3d24',sw=0.9))
    return ''.join(o)

def hdr2(t,s1,s2=''):
    return (T(28,32,t,font_size=15.5,font_weight='bold')+T(28,52,s1,fill='#55524b')
            +(T(28,68,s2,fill='#55524b') if s2 else ''))
def panel(x,y,w,h,label):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#b8b5ae" '
            f'stroke-width="1" stroke-dasharray="5,4"/>'
            f'<text x="{x+6}" y="{y+15}" font-size="11" font-weight="bold" fill="#55524b">{label}</text>')

# ---------------------------------------------------------------- HINH 3
v1 = V(112, 258, 1.10)
BX0,BX1,BY0,BY1 = 100, 378, 296, 548          # khung chi tiet B
v2 = V(BX0+8-138*3.30, BY1-6+30*3.30, 3.30)   # 3,3x vung X 138..216, Z 30..106
clip=(f'<defs><clipPath id="cb"><rect x="{BX0+1}" y="{BY0+1}" width="{BX1-BX0-2}" '
      f'height="{BY1-BY0-2}"/></clipPath></defs>')
b=[clip, panel(96,92,440,190,'A · Mặt cắt toàn bộ  TL 1:0,91'),
   panel(BX0-4,BY0-4,BX1-BX0+8,BY1-BY0+8,'B · Chi tiết khe ráp giữa  TL 3,3:1'),
   sec_body(v1), sec_lid(v1),
   f'<rect x="{v1.X(138):.1f}" y="{v1.Z(92):.1f}" width="{78*1.10:.1f}" height="{54*1.10:.1f}" '
   f'fill="none" stroke="#a8332a" stroke-width="1.4" stroke-dasharray="4,3"/>',
   v1.dim(0,354,0,'354',dy=20),
   arrow(v1.X(177), v1.Z(38)+8, v1.X(177), BY0-12,'#a8332a',1.3,6),
   f'<g clip-path="url(#cb)">{sec_body(v2)}{sec_lid(v2)}</g>']
g=[f'<line x1="{v2.X(177):.1f}" y1="{v2.Z(55):.1f}" x2="{v2.X(177):.1f}" y2="{v2.Z(63):.1f}" stroke="#a8332a" stroke-width="1.6"/>']
for xx in (166,188):
    g.append(arrow(v2.X(xx),v2.Z(62.5),v2.X(xx),v2.Z(56.4),'#a8332a',2.4,7))
b.append(f'<g clip-path="url(#cb)">{"".join(g)}</g>')
b += [arrow(v2.X(150),v2.Z(102),v2.X(150),v2.Z(86),'#2f7a3c',2.8,9),
      T(v2.X(150),v2.Z(105),'NHẤC',text_anchor='middle',font_size=12.5,font_weight='bold',fill='#2f7a3c'),
      v2.dim(155,199,88,'sống 44',dy=-3), v2.dim(177,199,85,'vấu 22',dy=30),
      f'<line x1="{v2.X(177):.1f}" y1="{v2.Z(55):.1f}" x2="{v2.X(177):.1f}" '
      f'y2="{v2.Z(63):.1f}" stroke="#2a241c" stroke-width="1.6"/>',
      f'<text x="{v2.X(177):.1f}" y="{v2.Z(50):.1f}" text-anchor="middle" font-size="9.5" '
      f'fill="#2a241c">khe ráp 0,6</text>']
ann3=[(900,132, v1.X(177), v1.Z(76), 'Sống khóa nằm đúng khe ráp giữa —'),
      (900,149, v1.X(177), v1.Z(58), 'trùng trọng tâm hộp theo phương X'),
      (900,196, v1.X(290), v1.Z(32), 'Khay nằm nguyên trong khoang'),
      (900,213, v1.X(300), v1.Z(20), 'khi hộp treo ngang'),
      (900,252, v1.X(60),  v1.Z(6),  'Đáy 8 — nơi tải kết thúc'),
      (900,352, v2.X(196), v2.Z(78), 'Sống 44 × 20 cocobolo,'),
      (900,369, v2.X(190), v2.Z(65), 'ngập 4 mm trong rãnh âm'),
      (900,424, v2.X(194), v2.Z(58), 'Vấu đè 22 mm lên MỖI cánh'),
      (900,441, v2.X(186), v2.Z(53), '→ hai cánh bị khóa xuống'),
      (900,496, v2.X(150), v2.Z(58), 'Nắp vát 18 → 12: hết cạnh dao 8 mm,'),
      (900,513, v2.X(148), v2.Z(51), 'mép tự do được đỡ suốt chiều dài')]
open('figs/fig3-mat-cat.svg','w').write(svg(940,566,
  hdr2('HÌNH 3 — Mặt cắt tại giữa chiều sâu (Y 175): sống khóa đè hai cánh',
       'Sống bắt cứng vào cánh trái, vấu đè 22 mm lên cánh phải. Nhấc quai là cả hai cánh bị ép xuống — không cánh nào bung được.',
       'Chi tiết này đồng thời đỡ mép tự do của nắp: giải luôn vấn đề §3.2 trong review Rev B.')
  + ''.join(b) + annot(ann3)))

# ---------------------------------------------------------------- HINH 4
def key_sec(v, locked):
    o=[v.rect(120,234,2,10,'#6b4526'), v.poly([(120,10),(234,10),(234,55),(120,55)],'#7a4f2c')]
    o.append(v.rect(162,192,37,47,'#faf9f6'))
    o.append(v.rect(168.5,185.5,47,55,'#faf9f6'))
    for x0,x1,ti,to in ((120,176.7,53.1,55),(177.3,234,55,53.1)):
        o.append(v.poly([(x0,ti),(x1,to),(x1,67),(x0,67)],'#a9754a'))
    o.append(v.rect(168.5,185.5,55,67,'#faf9f6'))
    o.append(v.rect(155,199,63,83,'#8a5a32',sw=1.1))
    zk = 39 if locked else 53
    o.append(v.rect(169,185,zk+8,81,'#3a2818','#1a1208',0.9))
    tw = 13 if locked else 4.5
    o.append(v.rect(177-tw,177+tw,zk,zk+8,'#3a2818','#1a1208',0.9))
    o.append(v.rect(170,184,81,84,'#c8b48a','#1a1208',0.9))
    if locked:
        for xx in (165.5,188.5):
            o.append(arrow(v.X(xx),v.Z(42),v.X(xx),v.Z(46.6),'#2f7a3c',1.8,5))
    return ''.join(o)

def key_plan(cx,cy,rot,s=2.15):
    o=[f'<rect x="{cx-23*s:.1f}" y="{cy-23*s:.1f}" width="{46*s:.1f}" height="{46*s:.1f}" rx="3" '
       f'fill="#7a4f2c" stroke="#2a241c" stroke-width="1"/>',
       f'<circle cx="{cx}" cy="{cy}" r="{8.5*s:.1f}" fill="#faf9f6" stroke="#2a241c" stroke-width="1"/>',
       f'<rect x="{cx-13*s:.1f}" y="{cy-4.5*s:.1f}" width="{26*s:.1f}" height="{9*s:.1f}" '
       f'fill="#faf9f6" stroke="#2a241c" stroke-width="1"/>',
       f'<g transform="rotate({rot} {cx} {cy})"><rect x="{cx-13*s:.1f}" y="{cy-4*s:.1f}" '
       f'width="{26*s:.1f}" height="{8*s:.1f}" fill="#3a2818" opacity="0.9"/></g>',
       f'<circle cx="{cx}" cy="{cy}" r="{5*s:.1f}" fill="#c8b48a" stroke="#1a1208" stroke-width="1"/>']
    return ''.join(o)

SK = 2.55
va, vb = V(96-120*SK, 452, SK), V(410-120*SK, 452, SK)
b=[panel(88,96,300,392,'A · THẢ — lưỡi trùng khe, rút chốt được'),
   panel(402,96,300,392,'B · KHÓA — xoay 90°, lưỡi tì dưới bản mặt'),
   panel(716,96,196,362,'C · Nhìn từ trên'),
   key_sec(va,False), key_sec(vb,True),
   key_plan(814,192,0), key_plan(814,364,90),
   T(814,272,'0° — cắm vào / rút ra',text_anchor='middle',font_size=11),
   T(814,444,'90° — khóa',text_anchor='middle',font_size=11,font_weight='bold',fill='#2f7a3c'),
   arrow(814,288,814,316,'#a8332a',2.2,7),
   T(840,306,'xoay 90°',font_size=10.5,fill='#a8332a')]
ann4=[(300,150, va.X(177), va.Z(82), 'Núm gỗ cứng, phẳng với mặt sống'),
      (300,167, va.X(186), va.Z(72), 'Thân Ø16 × 46'),
      (300,300, va.X(182), va.Z(57), 'Lưỡi 26 × 8 đang lọt qua khe'),
      (300,317, va.X(186), va.Z(50), 'Lỗ Ø17 xuyên khe nắp'),
      (690,150, vb.X(199), vb.Z(72), 'Sống khóa 44 × 20'),
      (690,300, vb.X(193), vb.Z(51), 'Bản mặt trụ dày 8'),
      (690,317, vb.X(160), vb.Z(42), 'Hốc 30 × 16 sâu 10'),
      (690,420, vb.X(190), vb.Z(43), 'Lưỡi ăn 8,5 mm mỗi bên')]
open('figs/fig4-chot-xoay.svg','w').write(svg(940,520,
  hdr2('HÌNH 4 — Chốt xoay 1/4 vòng: chi tiết duy nhất chuyển động',
       'Không lò xo, không ren, không kim loại. Lưỡi ngang tì lên mặt dưới bản mặt trụ: ứng suất cắt 0,84 MPa trên giới hạn ~14 MPa — hệ số 15×.',
       'Điểm yếu thật là MÒN sau 5.000 chu kỳ, không phải bền tức thời → lót ổ bằng gỗ cực cứng (grenadille/lignum) và bôi sáp vi tinh thể.')
  + ''.join(b) + annot(ann4)))
print('fig3, fig4 xong')

# ---------------------------------------------------------------- HINH 5
def hand(cx, cy, col='#3a2818'):
    return (f'<path d="M{cx-26},{cy} q0,-16 9,-16 q5,0 6,7 l1,8 M{cx-11},{cy-1} '
            f'l-1,-13 q0,-8 6,-8 q6,0 6,8 l1,13 M{cx+1},{cy-2} l0,-12 q0,-7 6,-7 '
            f'q6,0 6,7 l0,13 M{cx+13},{cy-1} l1,-9 q1,-6 6,-5 q5,1 5,7 l-1,9" '
            f'fill="none" stroke="{col}" stroke-width="2.6" stroke-linecap="round"/>'
            f'<path d="M{cx-26},{cy} q0,20 26,20 q26,0 26,-20 z" fill="#e8d9c0" '
            f'stroke="{col}" stroke-width="2"/>')

def elev_level(v):
    """Nhin chinh dien, hop treo NGANG"""
    o=[v.rect(0,354,2,10,'#6b4526'), v.poly([(0,10),(354,10),(354,49),(0,49)],'#7a4f2c')]
    for x0,x1 in ((10,136),(218,344)):
        for k in (0,1):
            z0=10+19*k; o.append(v.rect(x0+1,x1-1,z0,z0+19,'#c2ab84',sw=0.7))
    o.append(v.rect(143,211,10,48,'#b39a72'))
    for x0,x1,ti,to in ((0,176.7,49,55),(177.3,354,55,49)):
        o.append(v.poly([(x0,ti),(x1,to),(x1,67),(x0,67)],'#a9754a'))
    o.append(v.rect(155,199,63,83,'#8a5a32',sw=1.1))
    a=[iso for iso in []]
    pts=[(v.X(155+ (199-155)*0 ),0)]
    # quai
    d=[]
    for i in range(41):
        t=i/40; x=155+44*0.5; z=83+58*math.sin(math.pi*t)**0.66
        d.append((v.X(146+62*t), v.Z(z)))
    o.append('<path d="M '+' L '.join(f'{a:.1f},{b:.1f}' for a,b in d)+
             '" fill="none" stroke="#b8823f" stroke-width="9" stroke-linecap="round"/>')
    return ''.join(o), d[20]

def elev_portrait(v):
    """Hop treo DOC vi quai o vach truoc: nhin chinh dien, nap thanh 2 tam dung"""
    o=[v.poly([(0,0),(354,0),(354,350),(0,350)],'#7a4f2c')]
    for x0,x1 in ((14,168),(186,340)):
        o.append(v.rect(x0,x1,16,334,'#a9754a',sw=1.0))
    o.append(f'<text x="{v.X(91):.1f}" y="{v.Z(175):.1f}" text-anchor="middle" font-size="11" '
             f'fill="#5c3d24">cánh nắp</text>')
    # canh phai bung ra
    o.append(f'<g opacity="0.9" transform="rotate(-19 {v.X(340):.1f} {v.Z(334):.1f})">'
             f'{v.rect(186,340,16,334,"#c08a5c",sw=1.2)}</g>')
    o.append(arrow(v.X(296),v.Z(232),v.X(252),v.Z(246),'#a8332a',2.4,8))
    for i,(dx,dz) in enumerate(((246,110),(276,78),(226,52),(300,40))):
        o.append(f'<rect x="{v.X(dx):.1f}" y="{v.Z(dz):.1f}" width="9" height="9" rx="1.5" '
                 f'fill="#2a241c" transform="rotate({20*i} {v.X(dx):.1f} {v.Z(dz):.1f})"/>')
    return ''.join(o)

vA = V(112, 330, 0.80)
vB = V(566, 372, 0.62)
bodyA, grip = elev_level(vA)
b5=[panel(80,96,404,336,'A · ĐÚNG — quai tại X 177, Y 175'),
    panel(516,96,400,336,'B · SAI — quai trên vách trước'),
    bodyA, hand(grip[0], grip[1]+4),
    arrow(vA.X(177), vA.Z(30), vA.X(177), vA.Z(-14),'#2f7a3c',2.4,8),
    T(vA.X(177)+8, vA.Z(-4),'trọng tâm rơi thẳng xuống dưới nắm tay',font_size=11,fill='#2f7a3c'),
    f'<circle cx="{vA.X(177):.1f}" cy="{vA.Z(30):.1f}" r="4.5" fill="#2f7a3c"/>',
    elev_portrait(vB), hand(vB.X(177), vB.Z(360)+10),
    arrow(vB.X(177), vB.Z(175), vB.X(177), vB.Z(-16),'#a8332a',2.2,8),
    f'<circle cx="{vB.X(177):.1f}" cy="{vB.Z(175):.1f}" r="4.5" fill="#a8332a"/>',
    T(vB.X(177)+8, vB.Z(-6),'hộp buộc phải xoay 90°',font_size=11,fill='#a8332a')]
ann5=[(452,150, vA.X(199), vA.Z(74), 'Sống khóa ép cả hai cánh nắp'),
      (452,167, vA.X(250), vA.Z(40), 'Khay nằm yên trong khoang'),
      (452,206, vA.X(70),  vA.Z(6),  'Lực đi thẳng vào đáy hộp'),
      (906,150, vB.X(292), vB.Z(300), 'Cánh nắp thành tấm đứng'),
      (906,167, vB.X(316), vB.Z(262), '→ tự bung ra nếu không khóa'),
      (906,244, vB.X(276), vB.Z(78),  'Xúc xắc rời khỏi ổ'),
      (906,300, vB.X(96),  vB.Z(30),  'Khay trượt dồn về vách dưới')]
open('figs/fig5-tu-the-xach.svg','w').write(svg(940,452,
  hdr2('HÌNH 5 — Vì sao quai phải nằm giữa nóc, không phải trên vách',
       'Trọng tâm hộp ở X 177, Y 175. Quai đặt chỗ khác là hộp tự xoay cho tới khi trọng tâm rơi thẳng dưới nắm tay.',
       'Quai trên vách trước lệch 175 mm → hộp treo dọc, nắp thành hai tấm đứng, xúc xắc rời ổ.')
  + ''.join(b5) + annot(ann5)))
print('fig5 xong')
