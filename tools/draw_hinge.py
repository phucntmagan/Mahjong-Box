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

X0, X1 = S['LEAF_X0'], S['LEAF_X0'] + LW      # mep ngoai va mep khe giua cua canh
def leaf_outline(th):
    """Canh nap: chu nhat LW x TL; goc ngoai duoi do ong go chiem cho."""
    p = ([(X0, Z_RIM+RK)] + arcp(PX, Z_RIM, RK, 90, 0)
         + [(X1, Z_RIM), (X1, Z_LID), (X0, Z_LID)])
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
b.append(v.rect(0, B.WALL_HINGE, 10, Z_RIM - S['REBATE_H'], BODY, sw=1.1))
b.append(v.rect(S['REBATE_D'], B.WALL_HINGE, Z_RIM - S['REBATE_H'], Z_RIM, BODY, sw=1.1))
b.append(v.rect(B.WALL_HINGE, 200, 10, 48, '#c2ab84', sw=0.8))
b.append(T(v.X(112), v.Z(Z_TRAY/2), 'khay', text_anchor='middle', font_size=9, fill='#5a4a32'))
for pt, col in [((X1, Z_LID), '#a8332a'), ((X1, Z_RIM), '#c07a12')]:
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
b.append(v.dim(-S['REACH'], 0, 0, f'cánh mở vươn ra {S["REACH"]:.2f}', dy=20))

# ============================================================ PANEL B: ba ho nghiem
b.append(panel(484, 92, 416, 274, 'B · Ba họ nghiệm — cái nào ép ống, cái nào nhô ra  TL 4:1'))
b.append('<g clip-path="url(#cb)">')
SB, Z0 = 4.0, 27.0
RA = TL/2                        # ho A: ong bi be day nap ep cung
# Ho C duoc ve o hinh hoc CUA RIENG NO de so sanh, khong lay tri so dang chot.
DC = B.derive_mode('C')
PXX, RB_D, RB_H = DC['PIN_X'], DC['REBATE_D'], DC['REBATE_H']
WH = B.WALL_HINGE

def det(ox, px, rr, rebate, label, sub, col):
    """Ve mot chi tiet goc: (px, Z_RIM) la truc, rr ban kinh ong."""
    w = V(ox, 158 + Z_LID*SB, SB)
    o = []
    if rebate:                                   # ho C: ha bac RB_D x RB_H
        o.append(w.poly([(0, Z0), (0, Z_RIM-RB_H), (RB_D, Z_RIM-RB_H), (RB_D, Z_RIM-rr)]
                        + arcp(px, Z_RIM, rr, 270, 360) + [(WH, Z_RIM), (WH, Z0)],
                        BODY, sw=1.2))
        o.append(w.poly([(px, Z_RIM+rr)] + arcp(px, Z_RIM, rr, 90, 0)
                        + [(WH, Z_RIM), (WH, Z_LID), (px, Z_LID)], LEAF, sw=1.2))
    elif px == 0:                                # ho B: truc tren mat ngoai
        o.append(w.poly([(0, Z0), (0, Z_RIM-rr)] + arcp(0, Z_RIM, rr, 270, 360)
                        + [(WH, Z_RIM), (WH, Z0)], BODY, sw=1.2))
        o.append(w.poly([(0, Z_RIM+rr)] + arcp(0, Z_RIM, rr, 90, 0)
                        + [(WH, Z_RIM), (WH, Z_LID), (0, Z_LID)], LEAF, sw=1.2))
    else:                                        # ho A: truc giua be day nap
        o.append(w.rect(0, WH, Z0, Z_RIM, BODY, sw=1.2))
        o.append(w.poly(arcp(rr, Z_RIM+rr, rr, 90, 270) + [(WH, Z_RIM), (WH, Z_LID)],
                        LEAF, sw=1.2))
        o.append(w.circ((rr, Z_RIM+rr), rr, 'none', '#a8332a', 1.6))
    if rebate or px == 0:                        # ho B/C: ve ro ong go
        o.append(w.circ((px, Z_RIM), rr, LEAF, '#2a241c', 1.3))
        cx_, cz_ = px, Z_RIM
    else:                                        # ho A: ong la dau canh bo tron
        cx_, cz_ = rr, Z_RIM + rr
    o.append(w.circ((cx_, cz_), KH/2, '#1a1208', '#1a1208', 0.6))
    o.append(w.path([(-rr-3, Z_RIM), (WH+2, Z_RIM)], '#2f7a3c', 0.8, '4,3'))
    o.append(w.path([(0, Z0-2), (0, Z_LID+3)], '#8a857c', 0.8, '6,3,2,3'))
    o.append(T(ox + WH*SB/2 - 4, 300, label, text_anchor='middle',
               font_size=10, font_weight='bold'))
    for k, t in enumerate(sub):
        o.append(T(ox + WH*SB/2 - 4, 314 + k*12, t, text_anchor='middle',
                   font_size=8.5, fill=col))
    return ''.join(o)

b.append(det(524, RA, RA, False, 'HỌ A',
             [f'ống Ø{TL:.0f} = bề dày nắp', 'nhô 0 · KHÔNG có chặn'], '#a8332a'))
b.append(det(672, 0.0, RK, False, 'HỌ B',
             [f'ống Ø{2*RK:.1f}', f'NHÔ RA {RK:.1f} mỗi bên'],
             '#2f7a3c' if B.HG_MODE == 'B' else '#c07a12'))
b.append(det(820, PXX, RK, True, 'HỌ C',
             [f'ống Ø{2*RK:.1f} · nhô 0', f'hạ bậc {RB_D:.1f}×{RB_H:.0f}'],
             '#2f7a3c' if B.HG_MODE == 'C' else '#8a857c'))
b.append('</g>')

ann = [(60, 396, v.X(PX), v.Z(PZ),
        f'Trục chốt gỗ Ø{B.KN_PIN:.0f} tại ({PX:.1f} , {PZ:.0f}) — trên arris; ống Ø{2*RK:.1f} '
        f'nhô ra {S["PROUD"]:.1f} mỗi bên'),
       (60, 413, v.X(60), v.Z(Z_RIM+TL/2),
        f'{B.N_KN} mắt mộng gỗ × {B.KN_LEN:.0f}, bước {S["KN_PITCH"]:.0f}, chuỗi {S["KN_RUN"]:.0f} — không kim loại'),
       (60, 430, v.X(-92), v.Z(Z_RIM-TL/2),
        f'Cánh mở nằm ngang, mặt trên phẳng tại Z{Z_RIM:.0f} = đúng vành thân'),
       (60, 447, v.X(-4), v.Z(Z_RIM-TL/2),
        f'Chặn 180° = mặt cạnh nắp áp vào mặt ngoài vách, {S["STOP_A"]:.0f} mm²'),
       (908, 396, 856, 210,
        f'Họ C chìm hẳn nhưng phải hạ bậc {RB_D:.1f}×{RB_H:.0f} suốt vách — nó khoá trần hốc âm '
        f'(HÌNH 14)'),
       (908, 413, 560, 210,
        f'Họ A: ống Ø{TL:.0f} = bề dày nắp, là HỆ QUẢ bắt buộc của chỗ đặt trục')]

open('figs/fig8-dong-hoc-ban-le.svg', 'w').write(svg(940, 486, hdr(
    'HÌNH 8 — Bản lề mắt mộng gỗ: chỗ đặt trục quyết định đường kính ống',
    f'Trục cắm vào trong vật liệu thì mặt đầu cánh nắp quét thành cung, buộc phải bo tròn — R = ½ bề dày nắp. Ống Ø{TL:.0f} là hệ quả, không phải lựa chọn.',
    f'Đưa trục ra mặt phẳng mép đầu cánh (họ B) thì bán kính quét = 0, ống còn Ø{2*RK:.1f} và KHÔNG cần hạ bậc — đổi lại ống nhô ra {RK:.1f} mm mỗi bên.')
    + ''.join(b) + annot(ann, 470)))
print('fig8 xong')
