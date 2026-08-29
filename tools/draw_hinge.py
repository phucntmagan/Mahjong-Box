#!/usr/bin/env python3
"""Hinh dong hoc ban le — TRUC XOAY TREN ARRIS. python3 tools/draw_hinge.py
Moi tri so lay tu box_spec.derive() — khong go cung."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drawlib import *
import box_spec as B

S = B.derive()
Z_RIM, Z_LID, TL = S['Z_RIM'], S['Z_LID'], B.T_LID
LW, W = S['LW'], S['W']
PX, PZ = S['PIN_X'], S['PIN_Z']
R, SH = B.HG_R, S['STOP_H']
Z_TRAY = S['Z_TRAY_TOP']
BODY, LEAF, LEAFO, BRASS, PIN = '#7a4f2c', '#a9754a', '#cbb08c', '#c9a227', '#3a2818'

def rot(p, th):
    x, z = p[0]-PX, p[1]-PZ
    c, s = math.cos(math.radians(th)), math.sin(math.radians(th))
    return (PX + x*c - z*s, PZ + x*s + z*c)

def leaf_outline(th):
    """Canh nap: chu nhat LW x T, arris ngoai duoi bo luon R."""
    p = [(0, Z_RIM+R)] + [(R-R*math.cos(math.radians(a)), Z_RIM+R-R*math.sin(math.radians(a)))
                          for a in range(90, -1, -15)] + [(LW, Z_RIM), (LW, Z_LID), (0, Z_LID)]
    return [rot(q, th) for q in p]

os.makedirs('figs', exist_ok=True)

# ============================================================ PANEL A: quet
v = V(78 + 172*0.95, 356, 0.95)
CLIP = ('<defs>'
        '<clipPath id="ca"><rect x="61" y="93" width="402" height="272"/></clipPath>'
        '<clipPath id="cb"><rect x="485" y="93" width="414" height="272"/></clipPath>'
        '</defs>')
b = [CLIP, panel(60, 92, 404, 274, 'A · Hành trình 0 → 180°  TL 1:1,05')]
b.append('<g clip-path="url(#ca)">')
b.append(f'<line x1="{v.X(-175):.1f}" y1="{v.Z(0):.1f}" x2="{v.X(200):.1f}" y2="{v.Z(0):.1f}" '
         f'stroke="#1a1a1a" stroke-width="2"/>')
b.append(T(v.X(-174), v.Z(0)-5, 'mặt bàn', font_size=9.5, fill='#8a857c'))
b.append(v.rect(0, 200, 2, 10, '#5c3d24'))
b.append(v.rect(0, B.WALL_HINGE, 10, Z_RIM, BODY, sw=1.1))
b.append(v.rect(B.WALL_HINGE, 200, 10, 48, '#c2ab84', sw=0.8))
b.append(T(v.X(112), v.Z(Z_TRAY/2), 'khay', text_anchor='middle', font_size=9, fill='#5a4a32'))
# cung quet cua hai goc mep ngoai cua canh
for pt, col in [((LW, Z_LID), '#a8332a'), ((LW, Z_RIM), '#c07a12')]:
    b.append(v.path([rot(pt, t) for t in range(0, 181, 3)], col, 1.0, '4,3'))
for th, fill in ((0, LEAF), (60, 'none'), (120, 'none'), (180, LEAFO)):
    b.append(v.poly(leaf_outline(th), fill, '#6b4326' if fill == 'none' else '#2a241c',
                    0.9 if fill == 'none' else 1.3,
                    'stroke-dasharray="5,4"' if fill == 'none' else ''))
b.append(v.circ((PX, PZ), R, BRASS, '#6b5410', 1.1))
b += [f'<line x1="{v.X(-175):.1f}" y1="{v.Z(Z_RIM):.1f}" x2="{v.X(200):.1f}" y2="{v.Z(Z_RIM):.1f}" '
      f'stroke="#2f7a3c" stroke-width="1" stroke-dasharray="6,4"/>',
      T(v.X(196), v.Z(Z_RIM)-5, f'Z{Z_RIM:.0f} — vành thân', text_anchor='end',
        font_size=9.5, fill='#2f7a3c'),
      arrow(v.X(-62), v.Z(0)-4, v.X(-62), v.Z(Z_RIM)+4, '#55524b', 1.2, 5),
      T(v.X(-58), v.Z(Z_RIM/2), f'{Z_RIM:.0f}', font_size=9.5, fill='#55524b')]
b.append('</g>')
b.append(v.dim(-LW, 0, 0, f'cánh mở vươn ra {LW:.2f}', dy=20))

# ============================================================ PANEL B: goc phong to
# Truc cam sau vao vat lieu bao nhieu thi phai bo di bay nhieu.
b.append(panel(484, 92, 416, 274, 'B · Trục đặt ở đâu thì phải bỏ đi bao nhiêu  TL 6:1'))
b.append('<g clip-path="url(#cb)">')
SB, Z0 = 6.0, 30.0
RM = TL/2                        # mui tron bat buoc khi truc o giua be day nap

def arcp(cx, cz, r, a0, a1, n=18):
    return [(cx + r*math.cos(math.radians(a0 + (a1-a0)*i/n)),
             cz + r*math.sin(math.radians(a0 + (a1-a0)*i/n))) for i in range(n+1)]

# --- chi tiet 1: truc o giua be day nap -> mui tron RM
w1 = V(520, 485, SB)
b.append(w1.rect(0, 20, Z0, Z_RIM, BODY, sw=1.3))
b.append(w1.poly(arcp(RM, Z_RIM+RM, RM, 90, 270) + [(20, Z_RIM), (20, Z_LID)], LEAF, sw=1.3))
b.append(w1.circ((RM, Z_RIM+RM), RM, 'none', '#a8332a', 1.8))
b.append(w1.circ((RM, Z_RIM+RM), 0.5, PIN, PIN, 0.6))
b.append(w1.path([(-3, Z_RIM), (20, Z_RIM)], '#2f7a3c', 0.9, '4,3'))

# --- chi tiet 2: truc o arris -> chi bo luon R cho khop brass
w2 = V(720, 485, SB)
b.append(w2.poly([(0, Z0), (0, Z_RIM-R)] + arcp(0, Z_RIM, R, 270, 360)
                 + [(20, Z_RIM), (20, Z0)], BODY, sw=1.3))
b.append(w2.poly([(0, Z_RIM+R)] + arcp(0, Z_RIM, R, 90, 0)
                 + [(20, Z_RIM), (20, Z_LID), (0, Z_LID)], LEAF, sw=1.3))
b.append(w2.circ((0, Z_RIM), RM, 'none', '#c0bcb2', 1.2))          # cai da tranh duoc
b.append(w2.circ((0, Z_RIM), R, BRASS, '#6b5410', 1.3))
b.append(w2.circ((0, Z_RIM), 0.5, PIN, PIN, 0.6))
b.append(w2.path([(-9, Z_RIM), (20, Z_RIM)], '#2f7a3c', 0.9, '4,3'))

for cx, ttl, sub, col in [
        (580, 'trục ở GIỮA bề dày nắp', f'mũi tròn bắt buộc R{RM:.1f} → ống gỗ Ø{TL:.0f}', '#a8332a'),
        (790, 'trục ở ARRIS (0 , 47)',  f'chỉ bo lượn R{R:.2f} cho khớp brass', '#2f7a3c')]:
    b.append(T(cx, 326, ttl, text_anchor='middle', font_size=10.5, font_weight='bold'))
    b.append(T(cx, 342, sub, text_anchor='middle', font_size=10, fill=col))
b.append('</g>')

ann = [(60, 396, v.X(PX), v.Z(PZ), f'Trục xoay P = ({PX:.0f} , {PZ:.0f}) — arris ngoài trên của thân'),
       (60, 413, v.X(60), v.Z(Z_RIM+TL/2), f'Bản lề lá brass {B.HG_L:.0f}×{B.HG_W:.0f}×{B.HG_T}, khớp Ø{B.HG_KN} — không ống gỗ, không mắt mộng'),
       (60, 430, v.X(-92), v.Z(Z_RIM-TL/2), f'Cánh mở nằm ngang, mặt trên phẳng tại Z{Z_RIM:.0f} = đúng vành thân'),
       (60, 447, v.X(-4), v.Z(Z_RIM-TL/2), f'Chặn 180° = mặt cạnh nắp ({SH:.2f}×{B.LID_L:.0f} mm) áp vào mặt ngoài vách'),
       (908, 396, 726, 203, f'Bo lượn R{R:.2f} hai cạnh arris → khép thành lỗ Ø{B.HG_KN} ôm khớp brass'),
       (908, 413, 566, 203, f'Ống gỗ Ø{TL:.0f} của bản trước là HỆ QUẢ của chỗ đặt trục')]

open('figs/fig8-dong-hoc-ban-le.svg', 'w').write(svg(940, 486, hdr(
    'HÌNH 8 — Bản lề: trục ở ARRIS, không phải ở giữa bề dày nắp',
    f'Trục cắm vào giữa bề dày nắp thì hai góc đầu cánh quét vòng tròn xuyên qua vành thân → buộc phải bo mũi tròn R = ½ bề dày. Ống gỗ Ø{TL:.0f} là hệ quả.',
    f'Đưa trục ra arris — góc chung của cả hai chi tiết — thì bán kính quét bằng 0. Bề dày nắp {TL:.0f} mm không còn ràng buộc gì tới bản lề.')
    + ''.join(b) + annot(ann, 470)))
print('fig8 xong')
