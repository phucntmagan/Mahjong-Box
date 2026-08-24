#!/usr/bin/env python3
"""Hinh dong hoc ban le. python3 tools/draw_hinge.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drawlib import *

PX, PZ, R = 9.0, 58.0, 9.0
Z_RIM, Z_LID, T_SEAM, LW, SP = 49.0, 67.0, 12.0, 176.7, 16.0
BODY,LEAF,LEAFO,SPN,PIN = '#7a4f2c','#a9754a','#cbb08c','#6b3520','#3a2818'

def rot(p, th):
    x,z = p[0]-PX, p[1]-PZ
    c,s = math.cos(math.radians(th)), math.sin(math.radians(th))
    return (PX+x*c-z*s, PZ+x*s+z*c)

def leaf_outline(th):
    p=[(2*R,Z_RIM),(LW,Z_LID-T_SEAM),(LW,Z_LID),(2*R,Z_LID)]
    return [rot(q,th) for q in p]
def spine_outline(th):
    p=[(LW-44,Z_LID),(LW,Z_LID),(LW,Z_LID+SP),(LW-44,Z_LID+SP)]
    return [rot(q,th) for q in p]

os.makedirs('figs',exist_ok=True)

# ---------------------------------------------------------- PANEL A: quet
v = V(76 + 170*0.95, 352, 0.95)
CLIP=('<defs>'
      '<clipPath id="ca"><rect x="61" y="93" width="402" height="270"/></clipPath>'
      '<clipPath id="cb"><rect x="485" y="93" width="414" height="238"/></clipPath>'
      '</defs>')
b=[CLIP, panel(60,92,404,272,'A · Hành trình 0 → 180°  TL 1:1,05')]
b.append('<g clip-path="url(#ca)">')
b.append(f'<line x1="{v.X(-170):.1f}" y1="{v.Z(0):.1f}" x2="{v.X(200):.1f}" y2="{v.Z(0):.1f}" '
         f'stroke="#1a1a1a" stroke-width="2"/>')
b.append(T(v.X(-160), v.Z(0)+14,'mặt bàn',font_size=9.5,fill='#55524b'))
b.append(v.rect(0,200,2,10,'#5c3d24'))
b.append(v.rect(0,18,10,Z_RIM,BODY,sw=1.1))
b.append(v.rect(18,200,10,48,'#c2ab84',sw=0.8))
b.append(T(v.X(110), v.Z(28),'khay',text_anchor='middle',font_size=9,fill='#5a4a32'))
# cung quet cua 2 goc mep ngoai
for pt,col in [((LW,Z_LID),'#a8332a'), ((LW,Z_LID-T_SEAM),'#c07a12')]:
    arc=[rot(pt,t) for t in range(0,181,3)]
    b.append(v.path(arc, col, 1.0, '4,3'))
b.append(v.poly(leaf_outline(0), LEAF, sw=1.2))
b.append(v.poly(spine_outline(0), SPN, sw=1.1))
b.append(v.poly(leaf_outline(180), LEAFO, sw=1.2))
b.append(v.poly(spine_outline(180), SPN, sw=1.1))
b.append(v.circ((PX,PZ), 3.1, PIN, '#1a1208', 1.1))
b.append(v.circ((PX,PZ), R, 'none', '#a8332a', 1.0))
b += [f'<line x1="{v.X(-170):.1f}" y1="{v.Z(Z_RIM):.1f}" x2="{v.X(200):.1f}" y2="{v.Z(Z_RIM):.1f}" '
      f'stroke="#2f7a3c" stroke-width="1" stroke-dasharray="6,4"/>',
      T(v.X(196), v.Z(Z_RIM)-5,'Z49 — vành thân',text_anchor='end',font_size=9.5,fill='#2f7a3c'),
      arrow(v.X(-60),v.Z(0)-4, v.X(-60),v.Z(33)+4,'#55524b',1.2,5),
      T(v.X(-56),v.Z(15),'33',font_size=9.5,fill='#55524b')]
b.append('</g>')
b.append(v.dim(-158.7,18,0,'cánh mở vươn ra 159 + 18',dy=22))

# ---------------------------------------------------------- PANEL B: mat mong
def knuckle(w, th, lbl, y_lbl):
    o=[w.rect(0,18,20,Z_RIM,BODY,sw=1.1)]
    o.append(w.circ((PX,PZ), R, LEAF, '#2a241c', 1.2))
    lo = leaf_outline(th)
    o.append(w.poly(lo, LEAF, sw=1.2))
    o.append(w.circ((PX,PZ), R, 'none', '#a8332a', 1.6))
    # mat chan: day cung ban kinh 6, huong xuong khi dong / len khi mo
    a0 = -90 if th==0 else 90
    p1 = (PX+6*math.cos(math.radians(a0-28)), PZ+6*math.sin(math.radians(a0-28)))
    p2 = (PX+6*math.cos(math.radians(a0+28)), PZ+6*math.sin(math.radians(a0+28)))
    o.append(w.path([p1,p2], '#2f7a3c', 2.6))
    o.append(w.circ((PX,PZ), 3.1, PIN, '#1a1208', 1.1))
    o.append(T(w.X(PX), y_lbl, lbl, text_anchor='middle', font_size=11.5, font_weight='bold'))
    return ''.join(o)

vb = V(560-PX*4.6, 494, 4.6)
vc = V(790-PX*4.6, 494, 4.6)
b.append(panel(484,92,416,272,'B · Mắt mộng — TL 4,6:1'))
b.append('<g clip-path="url(#cb)">')
b.append(knuckle(vb, 0,   'ĐÓNG 0°', 350))
b.append(knuckle(vc, 180, 'MỞ 180°', 350))
b.append('</g>')
b.append(T(692,368,'mặt chặn phẳng nằm trong lòng mộng — hoàn toàn khuất',
           text_anchor='middle',font_size=10,fill='#2f7a3c'))

ann=[(60,150, v.X(PX), v.Z(PZ), 'Trục xoay P = (9 , 58)'),
     (60,167, v.X(PX+9), v.Z(PZ+7), 'ống gỗ R9 tiếp tuyến hai mặt nắp'),
     (60,404, v.X(-100), v.Z(Z_RIM+9), 'Cánh mở nằm ngang, dốc 1,94° về phía người chơi'),
     (60,421, v.X(-136), v.Z(38), 'Sống khóa chúc xuống Z33 — hở mặt bàn 33 mm,'),
     (60,438, v.X(-130), v.Z(24), 'nên cánh KHÔNG THỂ nằm hẳn xuống bàn'),
     (908,404, vb.X(PX), vb.Z(PZ-6), 'Mặt chặn phẳng rộng 8, bán kính 6 —'),
     (908,421, vc.X(PX), vc.Z(PZ+6), '1,41 MPa dưới người tỳ 5 kg, hệ số 10×'),
     (908,150, vb.X(4), vb.Z(38), 'Vách bản lề phải dày 18 (từ 10)'),
     (908,167, vb.X(15), vb.Z(30), '→ hộp thành 370 × 350')]
open('figs/fig8-dong-hoc-ban-le.svg','w').write(svg(940,468,
  hdr('HÌNH 8 — Động học bản lề: trục xoay suy ra từ ràng buộc, không phải chọn',
      'Ống gỗ bán kính 9 tiếp tuyến cả mặt trên (Z67) lẫn mặt dưới (Z49) của nắp → tâm ống buộc phải ở (9 , 58). Không còn bậc tự do nào.',
      'Quét 1° một bước, 11 điểm biên: không va chạm ở bất kỳ góc nào. Cánh mở ra nằm ngang đúng cao độ vành thân.')
  + ''.join(b) + annot(ann, 470)))
print('fig8 xong')
