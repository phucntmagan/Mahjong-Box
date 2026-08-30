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
REV, PAN_TH = B.PAN_REV, S['PAN_TH']
T_H, T_S, S_TOP = B.T_HINGE, B.T_SEAM, B.S_TOP
os.makedirs('figs', exist_ok=True)

# ================================================================== HINH 6
p = V(96, 452, 0.86)                      # mat bang 1 canh: X = ngang 176,7 ; "Z" = doc 350
b=[panel(80,92,220,380,'A · Mặt bằng một cánh  TL 1:1,16'),
   p.rect(0,LW,0,LL,FR,sw=1.2),
   p.rect(ST_H,ST_H+op_w,RAIL,RAIL+op_l,NU,sw=1.0),
   p.rect(ST_H-TON,ST_H+op_w+TON,RAIL-TON,RAIL+op_l+TON,'none','#a8332a',1.0,
          'stroke-dasharray="4,3"')]
_S = B.derive()
for i in range(B.N_KN):                            # chuoi mat mong go tren do doc
    y0 = _S['KN_Y0'] + i*_S['KN_PITCH']
    b.append(p.rect(0, 2*_S['R_KN'], y0, y0+B.KN_LEN,
                    SP if i % 2 == 0 else FR, sw=0.9))
b += [p.dim(0,ST_H,0,f'{ST_H:.0f}',dy=16), p.dim(ST_H,ST_H+op_w,0,f'lòng {op_w:.2f}',dy=16),
      p.dim(ST_H+op_w,LW,0,f'{ST_S:.0f}',dy=16), p.dim(0,LW,0,f'{LW:.2f}',dy=38),
      T(p.X(LW/2), p.Z(LL)-10,f'{LL:.0f} dọc',text_anchor='middle',font_size=9.5,fill='#55524b')]

s2 = V(403, 252, 2.50)                    # mat cat ngang 2,5x
b.append(panel(336,92,576,190,'B · Mặt cắt ngang cánh nắp  TL 2,5:1'))
b += [s2.poly([(0,0),(ST_H,0),(ST_H,T_H),(0,T_H)],FR,sw=1.1),
      s2.poly([(LW-ST_S,0),(LW,0),(LW,T_S),(LW-ST_S,T_S)],FR,sw=1.1),
      s2.poly([(ST_H,T_H),(LW-ST_S,T_S),(LW-ST_S,T_S-8),(ST_H,T_H-10)],'#faf9f6','#faf9f6',0),
      # tam NANG: mong day PAN_T chay trong ranh, long tam day len ngang mat khung
      s2.rect(ST_H-GRV,LW-ST_S+GRV,T_H-S_TOP-PAN_T,T_H-S_TOP,NU,sw=1.1),
      s2.rect(ST_H+REV,LW-ST_S-REV,T_H-S_TOP,T_H,NU,sw=1.1)]
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
      s3.rect(ST_H-GRV,ST_H,18-PAN_T-S_TOP,18-S_TOP,'#faf9f6',sw=1.0),
      s3.rect(ST_H-GRV+3,ST_H+8,18-PAN_T-S_TOP,18-S_TOP,NU,sw=1.1),
      s3.rect(ST_H+REV,ST_H+8,18-S_TOP,18,NU,sw=1.1),
      s3.dim(ST_H-GRV,ST_H,19,'rãnh 9',dy=-3),
      arrow(s3.X(ST_H),s3.Z(18-S_TOP/2),s3.X(ST_H+REV),s3.Z(18-S_TOP/2),'#a8332a',1.4,4),
      T(s3.X(ST_H+REV+1.6),s3.Z(18-S_TOP/2)+3.5,f'khe {REV:.1f}',font_size=9,fill='#a8332a'),
      s3.dim(ST_H-GRV+3,ST_H,-1,'mộng 6'),
      arrow(s3.X(ST_H-GRV+3),s3.Z(13),s3.X(ST_H-GRV),s3.Z(13),'#a8332a',1.8,5),
      T(s3.X(ST_H-GRV+1.4),s3.Z(15.6),'thả 3',text_anchor='middle',font_size=9.5,fill='#a8332a')]

ann=[(908,330, s3.X(ST_H+3), s3.Z(17), f'Tấm NÂNG dày {PAN_TH:.0f}: lòng tấm NGANG BẰNG mặt khung'),
     (908,347, s3.X(ST_H-7.5), s3.Z(4),  'Đáy rãnh — 3 mm trống để tấm nở'),
     (908,412, s3.X(ST_H-6.2), s3.Z(11), 'KHÔNG keo quanh rãnh —'),
     (908,429, s3.X(ST_H-3), s3.Z(6),  'chỉ chốt 1 điểm ở đúng tâm tấm'),
     (84,494, p.X(17), p.Z(60), 'Đố dọc 34 gỗ đặc thẳng thớ mang mặt mộng;'),
     (84,510, p.X(90), p.Z(90), 'tấm Nu THẢ — không nằm trong chuỗi kích thước'),
     (908,150, s2.X(LW-ST_S/2), s2.Z(T_S+6), 'Đố khe giữa — không còn rãnh sống khóa'),
     (908,167, s2.X(172), s2.Z(15), '(gỗ đặc) — không bao giờ vào tấm Nu'),
     (908,246, s2.X(2), s2.Z(0),
      f'Mắt mộng gỗ Ø{2*_S["R_KN"]:.1f} phay thẳng từ đố gỗ đặc, lỗ chốt Ø{_S["KN_HOLE"]:.2f}')]
open('figs/fig6-khung-tam-tha.svg','w').write(svg(940,528,
  hdr('HÌNH 6 — Nắp gỗ đặc: khung cocobolo ôm tấm Nu thả trong rãnh',
      'Chỉ hai thanh đố 34 mm nằm trong chuỗi kích thước bề rộng cánh. Tấm Nu thả tự do trong rãnh nên nở bao nhiêu cũng không đẩy khe ráp giữa.',
      f'Tấm Nu là tấm NÂNG dày {PAN_TH:.0f}: mộng {PAN_T:.0f} thả trong rãnh, lòng tấm ngang bằng mặt khung, khe {REV:.1f} mm quanh lòng tấm để nở.')
  + ''.join(b) + annot(ann, 620)))
print('fig6 xong')

# ================================================================== HINH 7
# Vi sao KHONG lam nap bang mot tam Nu DAC: khe rap giua dong lai theo mua.
# (Ban truoc lap luan bang mat mong go — mat mong da bi bo, nhung ket luan
#  khung + tam tha van dung, chi doi cho lap luan sang KHE RAP GIUA.)
K_BURL, K_LONG, K_CORE = B.K['Nu moi phuong'], B.K['doc tho'], B.K['loi on dinh']
K_XG = B.K['cocobolo ngang tho']
SEAM = B.SEAM

seam_left = B.seam_left          # dung chung voi lid_solid_calc.py — khong tinh lai

DMC_MAX = 6.0
def junction(v, dmc, kind, lbl, col, y_lbl, y_names):
    g = seam_left(dmc, kind)
    o = [v.rect(-30, -max(g, 0)/2, 0, 15, FR, sw=1.1),
         v.rect(max(g, 0)/2, 30, 0, 15, FR, sw=1.1)]
    o += [v.dim(-max(g, 0)/2, max(g, 0)/2, 17, f'khe {max(g,0):.2f}', dy=-2, col=col, fs=11),
          T(v.X(-16), y_names, 'cánh TRÁI', text_anchor='middle', font_size=9.5, fill='#55524b'),
          T(v.X(16), y_names, 'cánh PHẢI', text_anchor='middle', font_size=9.5, fill='#55524b'),
          T(v.X(0), y_lbl, lbl, text_anchor='middle', font_size=11.5, font_weight='bold', fill=col)]
    if g <= 0:
        o.append(T(v.X(0), y_names+16, f'ĐÃ CHẠM NHAU — thừa {-g:.2f} mm',
                   text_anchor='middle', font_size=10, font_weight='bold', fill='#a8332a'))
    return ''.join(o)

vA, vB = V(306, 250, 5.5), V(306, 456, 5.5)
b = [panel(96, 92, 420, 178, 'A · Khe ráp giữa hai cánh nắp  TL 5,5:1'),
     panel(96, 286, 420, 214, 'B · Cùng chỗ đó sau khi hút ẩm  ΔMC 4 %'),
     junction(vA, 0, 'nu', 'Lúc làm — 9 % MC', '#2f7a3c', 120, 264),
     junction(vB, 4.0, 'nu', 'Mùa nồm — 13 % MC', '#a8332a', 324, 470),
     T(306, 496, 'nắp Nu ĐẶC: khe đóng — hai cánh chống nhau, tự phá gỗ',
       text_anchor='middle', font_size=11.5, font_weight='bold', fill='#a8332a')]
# bieu do
gx0, gy0, gw, gh = 588, 140, 300, 250
b.append(panel(552, 92, 360, 398, 'C · Khe ráp giữa còn lại theo ΔMC'))
b.append(f'<rect x="{gx0}" y="{gy0}" width="{gw}" height="{gh}" fill="#fdf6f4" stroke="none"/>')
G_LO, G_HI = -0.9, 1.8
def gY(v): return gy0 + gh - (v - G_LO)/(G_HI - G_LO)*gh
def gX(m): return gx0 + m/DMC_MAX*gw
b.append(f'<rect x="{gx0}" y="{gY(0):.1f}" width="{gw}" height="{gy0+gh-gY(0):.1f}" fill="#f4dcd8"/>')
b.append(f'<line x1="{gx0}" y1="{gY(0):.1f}" x2="{gx0+gw}" y2="{gY(0):.1f}" stroke="#a8332a" stroke-width="1.4"/>')
b.append(T(gx0+gw-4, gY(0)+14, 'khe = 0 · hai cánh chạm nhau', text_anchor='end',
           font_size=9.5, fill='#a8332a'))
for val in (0, 0.5, 1.0, 1.5):
    b.append(f'<line x1="{gx0-4}" y1="{gY(val):.1f}" x2="{gx0}" y2="{gY(val):.1f}" stroke="#55524b" stroke-width="0.8"/>')
    b.append(T(gx0-8, gY(val)+3.5, f'{val:.1f}', text_anchor='end', font_size=9.5, fill='#55524b'))
for m in range(int(DMC_MAX)+1):
    b.append(f'<line x1="{gX(m):.1f}" y1="{gy0+gh}" x2="{gX(m):.1f}" y2="{gy0+gh+4}" stroke="#55524b" stroke-width="0.8"/>')
    b.append(T(gX(m), gy0+gh+16, str(m), text_anchor='middle', font_size=9.5, fill='#55524b'))
b.append(T(gx0+gw/2, gy0+gh+34, 'ΔMC (%)', text_anchor='middle', font_size=10, fill='#55524b'))
b.append(T(gx0+4, gy0-8, 'khe còn lại (mm)', font_size=10, fill='#55524b'))
for kind, col, lbl, dy in [('nu', '#a8332a', 'Nu ĐẶC', 0), ('core', '#c07a12', 'lõi ổn định', -13),
                           ('frame', '#2f7a3c', 'khung + tấm thả', 15)]:
    pts = ' '.join(f'{gX(DMC_MAX*m/40):.1f},{gY(max(seam_left(DMC_MAX*m/40, kind), G_LO)):.1f}'
                   for m in range(41))
    b.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.4"/>')
    b.append(T(gx0+gw-4, gY(max(seam_left(DMC_MAX, kind), G_LO))+4+dy, lbl, font_size=10,
               font_weight='bold', fill=col, text_anchor='end'))
xc = B.seam_close_dmc('nu')
b.append(f'<line x1="{gX(xc):.1f}" y1="{gy0}" x2="{gX(xc):.1f}" y2="{gY(0):.1f}" stroke="#a8332a" '
         f'stroke-width="1.2" stroke-dasharray="4,3"/>')
b.append(T(gX(xc)+6, gy0+16, f'ΔMC {xc:.1f} %', font_size=10, font_weight='bold', fill='#a8332a'))
b.append(T(gX(xc)+6, gy0+30, 'chưa hết một mùa', font_size=9.5, fill='#a8332a'))
open('figs/fig7-khe-rap-giua.svg', 'w').write(svg(940, 540,
  hdr('HÌNH 7 — Vì sao nắp không làm bằng một tấm Nu ĐẶC',
      f'Nu không có hướng thớ, nở đều mọi phương {K_BURL*100:.2f} %/1 % MC. Cả bề rộng cánh {LW:.2f} mm nằm trong chuỗi, nên hai cánh cùng lớn ra ăn vào khe giữa.',
      f'Khe {SEAM} mm đóng hết ở ΔMC {xc:.1f} % — chưa hết một mùa. Khung gỗ đặc chỉ đưa {2*B.STILE:.0f} mm gỗ ngang thớ vào chuỗi: khe còn {seam_left(4.0,"frame"):.2f} mm ở ΔMC 4 %.')
  + ''.join(b)))
print('fig7 xong')
