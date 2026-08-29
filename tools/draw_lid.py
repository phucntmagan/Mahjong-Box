#!/usr/bin/env python3
"""Hinh ve phuong an nap go dac (khung + tam Nu tha). python3 tools/draw_lid.py"""
import math, os

class V:
    def __init__(self, ox, oz, s): self.ox, self.oz, self.s = ox, oz, s
    def X(self, v): return self.ox + v*self.s
    def Z(self, v): return self.oz - v*self.s
    def rect(self, x0,x1,z0,z1, fill, st='#2a241c', sw=0.9, extra=''):
        return (f'<rect x="{self.X(x0):.1f}" y="{self.Z(z1):.1f}" width="{(x1-x0)*self.s:.1f}" '
                f'height="{(z1-z0)*self.s:.1f}" fill="{fill}" stroke="{st}" stroke-width="{sw}" {extra}/>')
    def poly(self, pts, fill, st='#2a241c', sw=0.9):
        d=' '.join(f'{self.X(a):.1f},{self.Z(b):.1f}' for a,b in pts)
        return f'<polygon points="{d}" fill="{fill}" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"/>'
    def dim(self, x0,x1,z, label, dy=0, col='#55524b', fs=9.5):
        a,b,y=self.X(x0),self.X(x1),self.Z(z)+dy
        return (f'<line x1="{a:.1f}" y1="{y:.1f}" x2="{b:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="0.8"/>'
                f'<line x1="{a:.1f}" y1="{y-3:.1f}" x2="{a:.1f}" y2="{y+3:.1f}" stroke="{col}" stroke-width="0.8"/>'
                f'<line x1="{b:.1f}" y1="{y-3:.1f}" x2="{b:.1f}" y2="{y+3:.1f}" stroke="{col}" stroke-width="0.8"/>'
                f'<text x="{(a+b)/2:.1f}" y="{y-4:.1f}" text-anchor="middle" font-size="{fs}" fill="{col}">{label}</text>')

def arrow(x1,y1,x2,y2,col,w=2.0,head=6):
    a=math.atan2(y2-y1,x2-x1)
    p=[(x2-head*math.cos(a-0.42), y2-head*math.sin(a-0.42)),
       (x2-head*math.cos(a+0.42), y2-head*math.sin(a+0.42))]
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" '
            f'stroke-width="{w}" stroke-linecap="round"/><polygon points="{x2:.1f},{y2:.1f} '
            f'{p[0][0]:.1f},{p[0][1]:.1f} {p[1][0]:.1f},{p[1][1]:.1f}" fill="{col}"/>')
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
def annot(items, mid=470):
    o=[]
    for x,y,px,py,txt in items:
        a='end' if x>mid else 'start'
        o.append(lead(x,y,px,py,a)); o.append(T(x,y,txt,text_anchor=a))
    return ''.join(o)
def panel(x,y,w,h,label):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#b8b5ae" '
            f'stroke-width="1" stroke-dasharray="5,4"/>'
            f'<text x="{x+6}" y="{y+15}" font-size="11" font-weight="bold" fill="#55524b">{label}</text>')
def hdr(t,s1,s2=''):
    return (T(28,32,t,font_size=15.5,font_weight='bold')+T(28,52,s1,fill='#55524b')
            +(T(28,68,s2,fill='#55524b') if s2 else ''))

FR, NU, SP, BODY = '#7a3f28', '#c8873f', '#6b3520', '#7a4f2c'
import box_spec as B
S = B.derive()
LW, LL = S['LW'], B.LID_L
ST_H = ST_S = B.STILE
RAIL = B.RAIL
op_w, op_l = S['OP_W'], S['OP_L']
GRV, TON, PAN_T = B.GRV, B.TON, B.PAN_T
T_H, T_S, S_TOP = B.T_HINGE, B.T_SEAM, B.S_TOP
os.makedirs('figs', exist_ok=True)

# ================================================================== HINH 6
p = V(96, 452, 0.86)                      # mat bang 1 canh: X = ngang 176,7 ; "Z" = doc 350
b=[panel(80,92,220,380,'A · Mặt bằng một cánh  TL 1:1,16'),
   p.rect(0,LW,0,LL,FR,sw=1.2),
   p.rect(ST_H,ST_H+op_w,RAIL,RAIL+op_l,NU,sw=1.0),
   p.rect(ST_H-TON,ST_H+op_w+TON,RAIL-TON,RAIL+op_l+TON,'none','#a8332a',1.0,
          'stroke-dasharray="4,3"')]
for i in range(B.N_KN):
    a = i*B.KN_PITCH
    if i % 2 == 1: b.append(p.rect(-4,0,a,a+B.KN_LEN,SP,sw=0.9))
b += [p.dim(0,ST_H,0,f'{ST_H:.0f}',dy=16), p.dim(ST_H,ST_H+op_w,0,f'lòng {op_w:.2f}',dy=16),
      p.dim(ST_H+op_w,LW,0,f'{ST_S:.0f}',dy=16), p.dim(0,LW,0,f'{LW:.2f}',dy=38),
      T(p.X(LW/2), p.Z(LL)-10,f'{LL:.0f} dọc',text_anchor='middle',font_size=9.5,fill='#55524b')]

s2 = V(403, 252, 2.50)                    # mat cat ngang 2,5x
b.append(panel(336,92,576,190,'B · Mặt cắt ngang cánh nắp  TL 2,5:1'))
b += [s2.poly([(0,0),(ST_H,0),(ST_H,T_H),(0,T_H)],FR,sw=1.1),
      s2.poly([(LW-ST_S,0),(LW,0),(LW,T_S),(LW-ST_S,T_S)],FR,sw=1.1),
      s2.poly([(ST_H,T_H),(LW-ST_S,T_S),(LW-ST_S,T_S-8),(ST_H,T_H-10)],'#faf9f6','#faf9f6',0),
      s2.rect(ST_H-GRV,LW-ST_S+GRV,T_H-S_TOP-PAN_T,T_H-S_TOP,NU,sw=1.1)]
cx,cy = s2.X(10), s2.Z(9)
b.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{3.1*2.50:.1f}" fill="#faf9f6" stroke="#2a241c" stroke-width="1"/>')
b += [s2.rect(LW-22,LW+22,18,38,SP,sw=1.2),
      s2.rect(LW-22,LW,14,18,'#faf9f6','#faf9f6',0),
      s2.poly([(LW-22,14),(LW,14)],'none','#2a241c',1.0),
      s2.dim(ST_H,LW-ST_S,42,f'lòng khung {op_w:.2f}',dy=-2),
      s2.dim(0,ST_H,-6,'đố 34'), s2.dim(LW-ST_S,LW,-6,'đố 34'),
      arrow(s2.X(76),s2.Z(21),s2.X(76),s2.Z(14.5),'#a8332a',1.6,5),
      arrow(s2.X(76),s2.Z(2),s2.X(76),s2.Z(7.5),'#a8332a',1.6,5),
      T(s2.X(76),s2.Z(25),'khay bỏ bài hình thành miễn phí',text_anchor='middle',font_size=10,fill='#a8332a')]

s3 = V(400-(ST_H-14)*7.4, 462, 7.4)       # chi tiet ranh 7,4x
b.append(panel(336,300,300,190,'C · Chi tiết mộng–rãnh  TL 7,4:1'))
b += [s3.poly([(ST_H-14,0),(ST_H,0),(ST_H,18),(ST_H-14,18)],FR,sw=1.1),
      s3.rect(ST_H-GRV,ST_H,18-PAN_T,18,'#faf9f6',sw=1.0),
      s3.rect(ST_H-GRV+3,ST_H+8,18-PAN_T,18,NU,sw=1.1),
      s3.dim(ST_H-GRV,ST_H,19,'rãnh 9',dy=-3),
      s3.dim(ST_H-GRV+3,ST_H,-1,'mộng 6'),
      arrow(s3.X(ST_H-GRV+3),s3.Z(13),s3.X(ST_H-GRV),s3.Z(13),'#a8332a',1.8,5),
      T(s3.X(ST_H-GRV+1.4),s3.Z(15.6),'thả 3',text_anchor='middle',font_size=9.5,fill='#a8332a')]

ann=[(908,330, s3.X(ST_H-2), s3.Z(13), f'Tấm Nu {PAN_T:.0f}, thụt {S_TOP:.0f} dưới mặt trên khung'),
     (908,347, s3.X(ST_H-7.5), s3.Z(4),  'Đáy rãnh — 3 mm trống để tấm nở'),
     (908,412, s3.X(ST_H-6.2), s3.Z(11), 'KHÔNG keo quanh rãnh —'),
     (908,429, s3.X(ST_H-3), s3.Z(6),  'chỉ chốt 1 điểm ở đúng tâm tấm'),
     (84,494, p.X(17), p.Z(60), 'Đố dọc 34 gỗ đặc thẳng thớ mang mặt mộng;'),
     (84,510, p.X(90), p.Z(90), 'tấm Nu THẢ — không nằm trong chuỗi kích thước'),
     (908,150, s2.X(LW-ST_S/2), s2.Z(T_S+6), 'Đố khe giữa — không còn rãnh sống khóa'),
     (908,167, s2.X(172), s2.Z(15), '(gỗ đặc) — không bao giờ vào tấm Nu'),
     (908,246, s2.X(10),  s2.Z(9),  'Lỗ chốt bản lề Ø6,2 nằm trong đố gỗ đặc')]
open('figs/fig6-khung-tam-tha.svg','w').write(svg(940,528,
  hdr('HÌNH 6 — Nắp gỗ đặc: khung cocobolo ôm tấm Nu thả trong rãnh',
      'Chỉ hai thanh đố 34 mm nằm trong chuỗi kích thước bề rộng cánh. Tấm Nu thả tự do trong rãnh nên nở bao nhiêu cũng không đẩy khe ráp giữa.',
      f'Khung dày {T_H:.0f} tại mộng → {T_S:.0f} tại khe giữa; tấm Nu dày đều {PAN_T:.0f} thụt {S_TOP:.0f} dưới mặt khung: mặt dưới tự thành khay bỏ bài.')
  + ''.join(b) + annot(ann, 620)))
print('fig6 xong')

# ================================================================== HINH 7
K_BURL, K_LONG, K_CORE = 0.0022, 0.0001, 0.0005
PITCH, KLEN, GAP = 45.0, 44.0, 1.0
KN=[((n-1)*PITCH,(n-1)*PITCH+KLEN,'THAN' if n%2 else 'NAP') for n in range(1,8)]
CTR=(6*PITCH+KLEN)/2
def mingap(e):
    return min((KN[i+1][0] if KN[i+1][2]=='THAN' else CTR+(KN[i+1][0]-CTR)*(1+e))
             - (KN[i][1]   if KN[i][2]  =='THAN' else CTR+(KN[i][1]  -CTR)*(1+e)) for i in range(6))

def junction(v, e, lbl, col, y_lbl, y_names):
    o=[v.rect(28,44,0,18,BODY,sw=1.1)]
    a = CTR+(45-CTR)*(1+e)
    o.append(v.rect(a,a+16,0,18,NU,sw=1.1))
    o += [v.dim(44,a,20,f'khe {a-44:.2f}',dy=-2,col=col,fs=11),
          T(v.X(36),y_names,'mắt mộng THÂN',text_anchor='middle',font_size=9.5,fill='#55524b'),
          T(v.X(a+8),y_names,'mắt mộng NẮP',text_anchor='middle',font_size=9.5,fill='#55524b'),
          T(v.X(44.5),y_lbl,lbl,text_anchor='middle',font_size=11.5,font_weight='bold',fill=col)]
    return ''.join(o)

vA, vB = V(306-44.5*5.5, 246, 5.5), V(306-44.5*5.5, 452, 5.5)
b=[panel(96,92,420,178,'A · Khe giữa mắt mộng 1 và 2  TL 5,5:1'),
   panel(96,286,420,214,'B · Cùng chỗ đó sau khi hút ẩm  ΔMC 4 %'),
   junction(vA,0,'Lúc làm — 9 % MC','#2f7a3c',120,264),
   junction(vB,K_BURL*4,'Mùa nồm — 13 % MC','#a8332a',324,470),
   T(306,492,'nắp Nu ĐẶC: khe đóng — bản lề kẹt cứng',text_anchor='middle',
     font_size=11.5,font_weight='bold',fill='#a8332a')]
# bieu do
gx0,gy0,gw,gh = 588, 140, 300, 250
b.append(panel(552,92,360,398,'C · Khe nhỏ nhất còn lại theo ΔMC'))
b.append(f'<rect x="{gx0}" y="{gy0}" width="{gw}" height="{gh}" fill="#fdf6f4" stroke="none"/>')
def gY(v): return gy0+gh-(v+0.62)/1.85*gh
def gX(m): return gx0+m/6*gw
b.append(f'<rect x="{gx0}" y="{gY(0)}" width="{gw}" height="{gy0+gh-gY(0):.1f}" fill="#f4dcd8"/>')
b.append(f'<line x1="{gx0}" y1="{gY(0):.1f}" x2="{gx0+gw}" y2="{gY(0):.1f}" stroke="#a8332a" stroke-width="1.4"/>')
b.append(T(gx0+gw-4, gY(0)+14,'khe = 0 · mắt mộng chạm nhau',text_anchor='end',font_size=9.5,fill='#a8332a'))
for v in (0,0.5,1.0):
    b.append(f'<line x1="{gx0-4}" y1="{gY(v):.1f}" x2="{gx0}" y2="{gY(v):.1f}" stroke="#55524b" stroke-width="0.8"/>')
    b.append(T(gx0-8,gY(v)+3.5,f'{v:.1f}',text_anchor='end',font_size=9.5,fill='#55524b'))
for m in range(7):
    b.append(f'<line x1="{gX(m):.1f}" y1="{gy0+gh}" x2="{gX(m):.1f}" y2="{gy0+gh+4}" stroke="#55524b" stroke-width="0.8"/>')
    b.append(T(gX(m),gy0+gh+16,str(m),text_anchor='middle',font_size=9.5,fill='#55524b'))
b.append(T(gx0+gw/2,gy0+gh+34,'ΔMC (%)',text_anchor='middle',font_size=10,fill='#55524b'))
b.append(T(gx0+4,gy0-8,'khe còn lại (mm)',font_size=10,fill='#55524b'))
for k,col,lbl,ly in [(K_BURL,'#a8332a','Nu ĐẶC',0),(K_CORE,'#c07a12','lõi ổn định',1),
                     (K_LONG,'#2f7a3c','khung gỗ đặc',2)]:
    pts=' '.join(f'{gX(m/4):.1f},{gY(mingap(k*m/4)):.1f}' for m in range(0,25))
    b.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.4"/>')
    b.append(T(gx0+gw+4, gY(mingap(k*6))+4+ (0 if k!=K_LONG else -10), lbl, font_size=10,
               font_weight='bold', fill=col, text_anchor='end'))
xc = GAP/(CTR-45)/K_BURL
b.append(f'<line x1="{gX(xc):.1f}" y1="{gy0}" x2="{gX(xc):.1f}" y2="{gY(0):.1f}" stroke="#a8332a" '
         f'stroke-width="1.2" stroke-dasharray="4,3"/>')
b.append(T(gX(xc)-6,gy0+16,f'ΔMC {xc:.1f} %',text_anchor='end',font_size=10,font_weight='bold',fill='#a8332a'))
b.append(T(gX(xc)-6,gy0+30,'xưởng 9 % → nồm 13 %',text_anchor='end',font_size=9.5,fill='#a8332a'))
open('figs/fig7-ket-ban-le.svg','w').write(svg(940,540,
  hdr('HÌNH 7 — Vì sao tấm Nu ĐẶC không phay mặt mộng trực tiếp được',
      'Thân hộp thẳng thớ, thớ chạy dọc cạnh 350 → mặt mộng thân đứng yên. Nu không có hướng thớ, nở đều mọi phương, kéo mặt mộng nắp trượt dọc trục.',
      'Khe dọc trục 1,0 mm đóng hoàn toàn ở ΔMC 4,1 % — đúng bằng chênh lệch xưởng ↔ mùa nồm.')
  + ''.join(b)))
print('fig7 xong')
