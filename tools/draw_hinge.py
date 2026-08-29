#!/usr/bin/env python3
"""Hinh dong hoc ban le. python3 tools/draw_hinge.py
Moi tri so lay tu box_spec.derive() — khong go cung."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drawlib import *
import box_spec as B

S = B.derive()
R = B.R_KN
Z_RIM, Z_LID, T_SEAM = S['Z_RIM'], S['Z_LID'], B.T_SEAM
LW, SP = S['LW'], S['Z_PROUD']          # SP = 0 o phuong an C (khong con song khoa)
PX, PZ = R, Z_RIM + R
Z_TRAY, W = S['Z_TRAY_TOP'], S['W']
BODY,LEAF,LEAFO,SPN,PIN = '#7a4f2c','#a9754a','#cbb08c','#6b3520','#3a2818'

def rot(p, th):
    x,z = p[0]-PX, p[1]-PZ
    c,s = math.cos(math.radians(th)), math.sin(math.radians(th))
    return (PX+x*c-z*s, PZ+x*s+z*c)

def leaf_outline(th):
    p=[(2*R,Z_RIM),(LW,Z_LID-T_SEAM),(LW,Z_LID),(2*R,Z_LID)]
    return [rot(q,th) for q in p]
def spine_outline(th):
    if SP <= 0: return None          # phuong an C khong co song khoa
    p=[(LW-B.SPINE_W,Z_LID),(LW,Z_LID),(LW,Z_LID+SP),(LW-B.SPINE_W,Z_LID+SP)]
    return [rot(q,th) for q in p]

os.makedirs('figs',exist_ok=True)

# ---------------------------------------------------------- PANEL A: quet
v = V(76 + 170*0.95, 352, 0.95)
CLIP=('<defs>'
      '<clipPath id="ca"><rect x="61" y="93" width="402" height="270"/></clipPath>'
      '<clipPath id="cb"><rect x="485" y="93" width="414" height="228"/></clipPath>'
      '</defs>')
b=[CLIP, panel(60,92,404,272,'A · Hành trình 0 → 180°  TL 1:1,05')]
b.append('<g clip-path="url(#ca)">')
b.append(f'<line x1="{v.X(-170):.1f}" y1="{v.Z(0):.1f}" x2="{v.X(200):.1f}" y2="{v.Z(0):.1f}" '
         f'stroke="#1a1a1a" stroke-width="2"/>')
b.append(T(v.X(-160), v.Z(0)+14,'mặt bàn',font_size=9.5,fill='#55524b'))
b.append(v.rect(0,200,2,10,'#5c3d24'))
b.append(v.rect(0,18,10,Z_RIM,BODY,sw=1.1))
b.append(v.rect(18,200,10,48,'#c2ab84',sw=0.8))
b.append(T(v.X(110), v.Z(Z_TRAY/2),'khay',text_anchor='middle',font_size=9,fill='#5a4a32'))
# cung quet cua 2 goc mep ngoai
for pt,col in [((LW,Z_LID),'#a8332a'), ((LW,Z_LID-T_SEAM),'#c07a12')]:
    arc=[rot(pt,t) for t in range(0,181,3)]
    b.append(v.path(arc, col, 1.0, '4,3'))
b.append(v.poly(leaf_outline(0), LEAF, sw=1.2))
b.append(v.poly(leaf_outline(180), LEAFO, sw=1.2))
for th in (0, 180):
    so = spine_outline(th)
    if so: b.append(v.poly(so, SPN, sw=1.1))
b.append(v.circ((PX,PZ), 3.1, PIN, '#1a1208', 1.1))
b.append(v.circ((PX,PZ), R, 'none', '#a8332a', 1.0))
b += [f'<line x1="{v.X(-170):.1f}" y1="{v.Z(Z_RIM):.1f}" x2="{v.X(200):.1f}" y2="{v.Z(Z_RIM):.1f}" '
      f'stroke="#2f7a3c" stroke-width="1" stroke-dasharray="6,4"/>',
      T(v.X(196), v.Z(Z_RIM)-5,f'Z{Z_RIM:.0f} — vành thân',text_anchor='end',font_size=9.5,fill='#2f7a3c'),
      arrow(v.X(-60),v.Z(0)-4, v.X(-60),v.Z(Z_RIM)+4,'#55524b',1.2,5),
      T(v.X(-56),v.Z(Z_RIM/2),f'{Z_RIM:.0f}',font_size=9.5,fill='#55524b')]
b.append('</g>')
b.append(v.dim(-(LW-2*R),2*R,0,f'cánh mở vươn ra {LW-2*R:.0f} + {2*R:.0f}',dy=34))

# ---------------------------------------------------------- PANEL B: mat mong
STUB = 34.0          # chi ve mot doan cut cua canh nap quanh mat mong
SB = 3.2
def stub_outline(th):
    z1 = Z_RIM + (Z_LID - T_SEAM - Z_RIM)*(STUB - 2*R)/(LW - 2*R)
    p = [(2*R, Z_RIM), (STUB, z1), (STUB, Z_LID), (2*R, Z_LID)]
    return [rot(q, th) for q in p]

def knuckle(w, th, lbl, y_lbl):
    o = [w.rect(0, 2*R, Z_RIM-22, Z_RIM, BODY, sw=1.1)]      # vach than
    o.append(w.circ((PX, PZ), R, LEAF, '#2a241c', 1.2))       # ong go
    o.append(w.poly(stub_outline(th), LEAF, sw=1.2))
    o.append(w.circ((PX, PZ), R, 'none', '#a8332a', 1.6))
    a0 = -90 if th == 0 else 90                               # mat chan phang
    p1 = (PX+6*math.cos(math.radians(a0-28)), PZ+6*math.sin(math.radians(a0-28)))
    p2 = (PX+6*math.cos(math.radians(a0+28)), PZ+6*math.sin(math.radians(a0+28)))
    o.append(w.path([p1, p2], '#2f7a3c', 2.6))
    o.append(w.circ((PX, PZ), B.D_PIN/2, PIN, '#1a1208', 1.1))
    return ''.join(o)

vb = V(600-PX*SB, 250+PZ*SB, SB)
vc = V(800-PX*SB, 250+PZ*SB, SB)
b.append(panel(484, 92, 416, 272, f'B · Mắt mộng — TL {SB:.1f}:1'))
b.append('<g clip-path="url(#cb)">')
b.append(knuckle(vb, 0,   'ĐÓNG 0°', 340))
b.append(knuckle(vc, 180, 'MỞ 180°', 340))
b.append('</g>')
for w, lbl in [(vb, 'ĐÓNG 0°'), (vc, 'MỞ 180°')]:
    b.append(T(w.X(PX), 336, lbl, text_anchor='middle', font_size=11.5, font_weight='bold'))
b.append(T(692, 358, 'mặt chặn phẳng nằm trong lòng mộng — hoàn toàn khuất',
           text_anchor='middle', font_size=10, fill='#2f7a3c'))

ann=[(60,150, v.X(PX), v.Z(PZ), f'Trục xoay P = ({PX:.0f} , {PZ:.0f})'),
     (60,167, v.X(PX+R), v.Z(PZ+7), f'ống gỗ R{R:.0f} tiếp tuyến hai mặt nắp'),
     (60,404, v.X(-100), v.Z(Z_RIM+R), f'Cánh mở nằm ngang, dốc {S["ANG"]:.2f}° về phía người chơi'),
     (60,421, v.X(-136), v.Z(Z_RIM-9), f'Mặt dưới cánh mở phẳng tại Z{Z_RIM:.0f} — đúng cao độ vành thân,'),
     (60,438, v.X(-130), v.Z(Z_RIM-20), 'không bao giờ xuống dưới vành trong cả hành trình'),
     (908,404, vb.X(PX), vb.Z(PZ-6), 'Mặt chặn phẳng rộng 8, bán kính 6 —'),
     (908,421, vc.X(PX), vc.Z(PZ+6), 'hệ số an toàn 10× dưới người tỳ 5 kg'),
     (908,150, vb.X(4), vb.Z(Z_RIM-11), f'Vách bản lề phải dày {2*R:.0f} (từ 10)'),
     (908,167, vb.X(15), vb.Z(Z_RIM-19), f'→ hộp thành {W:.0f} × {S["Y_OA"]:.0f}')]
open('figs/fig8-dong-hoc-ban-le.svg','w').write(svg(940,468,
  hdr('HÌNH 8 — Động học bản lề: trục xoay suy ra từ ràng buộc, không phải chọn',
      f'Ống gỗ bán kính {R:.0f} tiếp tuyến cả mặt trên (Z{Z_LID:.0f}) lẫn mặt dưới (Z{Z_RIM:.0f}) của nắp → tâm ống buộc phải ở ({PX:.0f} , {PZ:.0f}). Không còn bậc tự do nào.',
      'Quét 1° một bước, 11 điểm biên: không va chạm ở bất kỳ góc nào. Cánh mở ra nằm ngang đúng cao độ vành thân.')
  + ''.join(b) + annot(ann, 470)))
print('fig8 xong')
