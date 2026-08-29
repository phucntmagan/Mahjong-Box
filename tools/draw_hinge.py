#!/usr/bin/env python3
"""Hinh dong hoc ban le MONG GO. python3 tools/draw_hinge.py
Moi tri so lay tu box_spec.derive() — khong go cung."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drawlib import *
import box_spec as B

S = B.derive()
Z_RIM, Z_LID, TL = S['Z_RIM'], S['Z_LID'], B.T_LID
LW, W = S['LW'], S['W']
PX, PZ = S['PIN_X'], S['PIN_Z']
RK, KH = S['R_KN'], S['KN_HOLE']
Z_TRAY = S['Z_TRAY_TOP']
BODY, LEAF, LEAFO, PIN = '#7a4f2c', '#a9754a', '#cbb08c', '#3a2818'

def rot(p, th):
    x, z = p[0]-PX, p[1]-PZ
    c, s = math.cos(math.radians(th)), math.sin(math.radians(th))
    return (PX + x*c - z*s, PZ + x*s + z*c)

def arcp(cx, cz, r, a0, a1, n=20):
    return [(cx + r*math.cos(math.radians(a0 + (a1-a0)*i/n)),
             cz + r*math.sin(math.radians(a0 + (a1-a0)*i/n))) for i in range(n+1)]

def leaf_outline(th):
    """Canh nap: chu nhat LW x TL, goc arris ngoai duoi do ong go chiem cho."""
    p = ([(0, Z_RIM+RK)] + arcp(0, Z_RIM, RK, 90, 0)
         + [(LW, Z_RIM), (LW, Z_LID), (0, Z_LID)])
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
b.append(f'<line x1="{v.X(-180):.1f}" y1="{v.Z(0):.1f}" x2="{v.X(200):.1f}" y2="{v.Z(0):.1f}" '
         f'stroke="#1a1a1a" stroke-width="2"/>')
b.append(T(v.X(-178), v.Z(0)-5, 'mặt bàn', font_size=9.5, fill='#8a857c'))
b.append(v.rect(0, 200, 2, 10, '#5c3d24'))
b.append(v.rect(0, B.WALL_HINGE, 10, Z_RIM, BODY, sw=1.1))
b.append(v.rect(B.WALL_HINGE, 200, 10, 48, '#c2ab84', sw=0.8))
b.append(T(v.X(112), v.Z(Z_TRAY/2), 'khay', text_anchor='middle', font_size=9, fill='#5a4a32'))
for pt, col in [((LW, Z_LID), '#a8332a'), ((LW, Z_RIM), '#c07a12')]:
    b.append(v.path([rot(pt, t) for t in range(0, 181, 3)], col, 1.0, '4,3'))
for th, fill in ((0, LEAF), (60, 'none'), (120, 'none'), (180, LEAFO)):
    b.append(v.poly(leaf_outline(th), fill, '#6b4326' if fill == 'none' else '#2a241c',
                    0.9 if fill == 'none' else 1.3,
                    'stroke-dasharray="5,4"' if fill == 'none' else ''))
b.append(v.circ((PX, PZ), RK, LEAF, '#2a241c', 1.2))
b.append(v.circ((PX, PZ), KH/2, '#1a1208', '#1a1208', 0.6))
b += [f'<line x1="{v.X(-180):.1f}" y1="{v.Z(Z_RIM):.1f}" x2="{v.X(200):.1f}" y2="{v.Z(Z_RIM):.1f}" '
      f'stroke="#2f7a3c" stroke-width="1" stroke-dasharray="6,4"/>',
      T(v.X(196), v.Z(Z_RIM)-5, f'Z{Z_RIM:.0f} — vành thân', text_anchor='end',
        font_size=9.5, fill='#2f7a3c'),
      arrow(v.X(-62), v.Z(0)-4, v.X(-62), v.Z(Z_RIM)+4, '#55524b', 1.2, 5),
      T(v.X(-58), v.Z(Z_RIM/2), f'{Z_RIM:.0f}', font_size=9.5, fill='#55524b')]
b.append('</g>')
b.append(v.dim(-LW, 0, 0, f'cánh mở vươn ra {LW:.2f}', dy=20))

# ============================================================ PANEL B: hai ho nghiem
b.append(panel(484, 92, 416, 274, 'B · Hai họ nghiệm — và cái nào ép ống to  TL 6:1'))
b.append('<g clip-path="url(#cb)">')
SB, Z0 = 6.0, 30.0
RA = TL/2                        # ho A: ong bi be day nap ep cung

wA = V(520, 485, SB)
b.append(wA.rect(0, 20, Z0, Z_RIM, BODY, sw=1.3))
b.append(wA.poly(arcp(RA, Z_RIM+RA, RA, 90, 270) + [(20, Z_RIM), (20, Z_LID)], LEAF, sw=1.3))
b.append(wA.circ((RA, Z_RIM+RA), RA, 'none', '#a8332a', 1.8))
b.append(wA.circ((RA, Z_RIM+RA), KH/2, '#1a1208', '#1a1208', 0.6))
b.append(wA.path([(-3, Z_RIM), (20, Z_RIM)], '#2f7a3c', 0.9, '4,3'))

wB = V(720, 485, SB)
b.append(wB.poly([(0, Z0), (0, Z_RIM-RK)] + arcp(0, Z_RIM, RK, 270, 360)
                 + [(20, Z_RIM), (20, Z0)], BODY, sw=1.3))
b.append(wB.poly([(0, Z_RIM+RK)] + arcp(0, Z_RIM, RK, 90, 0)
                 + [(20, Z_RIM), (20, Z_LID), (0, Z_LID)], LEAF, sw=1.3))
b.append(wB.circ((0, Z_RIM), RA, 'none', '#c0bcb2', 1.2))       # cai da tranh duoc
b.append(wB.circ((0, Z_RIM), RK, LEAF, '#2a241c', 1.4))
b.append(wB.circ((0, Z_RIM), KH/2, '#1a1208', '#1a1208', 0.6))
b.append(wB.path([(-RK-4, Z_RIM), (20, Z_RIM)], '#2f7a3c', 0.9, '4,3'))
b.append(wB.path([(0, Z0), (0, Z_LID+2)], '#8a857c', 0.9, '7,3,2,3'))

for cx, ttl, sub, col in [
        (580, 'HỌ A · trục TRONG vật liệu',
         f'đầu cánh phải bo tròn R{RA:.1f} → ống Ø{TL:.0f}', '#a8332a'),
        (790, 'HỌ B · trục TRÊN mặt phẳng ngoài',
         f'không bo gì → ống Ø{2*RK:.1f}, nhô ra {RK:.1f}', '#2f7a3c')]:
    b.append(T(cx, 326, ttl, text_anchor='middle', font_size=10.5, font_weight='bold'))
    b.append(T(cx, 342, sub, text_anchor='middle', font_size=10, fill=col))
b.append('</g>')

ann = [(60, 396, v.X(PX), v.Z(PZ),
        f'Trục chốt gỗ Ø{B.KN_PIN:.0f} tại ({PX:.0f} , {PZ:.0f}) — đúng trên arris'),
       (60, 413, v.X(60), v.Z(Z_RIM+TL/2),
        f'{B.N_KN} mắt mộng gỗ × {B.KN_LEN:.0f}, bước {S["KN_PITCH"]:.0f}, chuỗi {S["KN_RUN"]:.0f} — không kim loại'),
       (60, 430, v.X(-92), v.Z(Z_RIM-TL/2),
        f'Cánh mở nằm ngang, mặt trên phẳng tại Z{Z_RIM:.0f} = đúng vành thân'),
       (60, 447, v.X(-4), v.Z(Z_RIM-TL/2),
        f'Chặn 180° = mặt cạnh nắp áp vào mặt ngoài vách, {S["STOP_A"]:.0f} mm²'),
       (908, 396, 726, 215,
        f'Ống Ø{2*RK:.1f} do chốt Ø{B.KN_PIN:.0f} + thành gỗ {S["KN_WALL_EFF"]:.1f} quyết định, KHÔNG do bề dày nắp'),
       (908, 413, 566, 215,
        f'Ống Ø{TL:.0f} của họ A là HỆ QUẢ bắt buộc của chỗ đặt trục')]

open('figs/fig8-dong-hoc-ban-le.svg', 'w').write(svg(940, 486, hdr(
    'HÌNH 8 — Bản lề mắt mộng gỗ: chỗ đặt trục quyết định đường kính ống',
    f'Trục cắm vào trong vật liệu thì mặt đầu cánh nắp quét thành cung, buộc phải bo tròn — R = ½ bề dày nắp. Ống Ø{TL:.0f} là hệ quả, không phải lựa chọn.',
    f'Đưa trục lên mặt phẳng ngoài (x = 0) thì mặt đầu là tia xuất phát từ trục, bán kính quét = 0. Ống còn Ø{2*RK:.1f}, đổi lại nhô ra {RK:.1f} mm mỗi bên.')
    + ''.join(b) + annot(ann, 470)))
print('fig8 xong')
