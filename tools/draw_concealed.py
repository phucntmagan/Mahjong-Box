#!/usr/bin/env python3
"""Hinh 13 — vi sao ban le chim han khong quay duoc. python3 tools/draw_concealed.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drawlib import *
import box_spec as B

S = B.derive()
Z_RIM, Z_LID, TL = S['Z_RIM'], S['Z_LID'], B.T_LID
WALL, R = S['WALL_HINGE'], S['R_KN']
BODY, LEAF, VOID, SKIN = '#7a4f2c', '#a9754a', '#efe7d8', '#c9a227'
os.makedirs('figs', exist_ok=True)

def arcp(cx, cz, r, a0, a1, n=24):
    return [(cx + r*math.cos(math.radians(a0 + (a1-a0)*i/n)),
             cz + r*math.sin(math.radians(a0 + (a1-a0)*i/n))) for i in range(n+1)]
def rot(p, px, pz, th):
    x, z = p[0]-px, p[1]-pz
    c, s = math.cos(math.radians(th)), math.sin(math.radians(th))
    return (px + x*c - z*s, pz + x*s + z*c)

b = ['<defs><clipPath id="ca"><rect x="61" y="93" width="402" height="292"/></clipPath></defs>']

# ================================================= PANEL A: truc chim, cay thung da go
A_IN, A_DOWN, S_SKIN = 11.0, 9.0, 2.0
PXA, PZA = A_IN, Z_RIM - A_DOWN
SC = 6.4
Z_BOT = Z_RIM - 20
v = V(168, 118 + Z_LID*SC, SC)
b.append(panel(60, 92, 404, 294,
               f'A · Trục chìm hẳn: lùi vào {A_IN:.0f}, sâu {A_DOWN:.0f} dưới vành  TL {SC:.1f}:1'))
b.append('<g clip-path="url(#ca)">')
b.append(v.rect(0, WALL, Z_BOT, Z_RIM, BODY, sw=1.2))                 # vach
b.append(v.rect(0, S_SKIN, Z_BOT, Z_RIM, SKIN, '#6b5410', 1.1))       # da go phai giu
b.append(v.rect(0, 26, Z_RIM, Z_LID, LEAF, sw=1.3))                   # canh nap (mot doan)
# vung go PHAI BOC: quy dao ca dai mat duoi nap tu x=0 den x=truc
rho, bb = math.hypot(A_IN, A_DOWN), A_DOWN
ph0 = math.degrees(math.atan2(A_DOWN, -A_IN))
poly = (arcp(PXA, PZA, rho, ph0, ph0+180, 40)
        + arcp(PXA, PZA, bb, ph0+180, ph0, 40))
b.append(v.poly(poly, '#a8332a', '#7a2018', 1.0, 'fill-opacity="0.55"'))
b.append(v.circ((PXA, PZA), R, LEAF, '#2a241c', 1.3))                 # ong go
b.append(v.circ((PXA, PZA), S['KN_HOLE']/2, '#1a1208', '#1a1208', 0.6))
b.append(v.path([(-8, Z_RIM), (WALL+3, Z_RIM)], '#2f7a3c', 1.0, '5,3'))
b.append(v.dim(0, S_SKIN, Z_BOT, f'da {S_SKIN:.0f}', dy=16, fs=8.5))
b.append('</g>')
b.append(T(72, 356, 'Vùng đỏ = gỗ PHẢI BỐC đi để cánh quay. Nó cày thẳng qua lớp da gỗ',
           font_size=10, fill='#a8332a'))
b.append(T(72, 370, f'và mở thông ra mặt ngoài. Va chạm ở 0,25° — cánh gần như không nhúc nhích.',
           font_size=10, fill='#a8332a'))

# ================================================= PANEL B: bang danh doi
b.append(panel(484, 92, 416, 294, 'B · Đẩy trục vào sâu bao nhiêu thì được gì'))
gx, gy, gw, bh = 560, 140, 300, 26
SCB = gw/(2*R + 4)
b.append(T(692, 118, f'Tổng "nhìn thấy" luôn = bán kính ống = {R:.1f} mm.',
           text_anchor='middle', font_size=10.5, font_weight='bold', fill='#55524b'))
rows = [(0.0, 'HỌ B'), (2.0, ''), (4.0, ''), (R, 'HỌ C'), (8.0, ''), (11.0, '')]
for k, (a_, tag) in enumerate(rows):
    y = gy + 20 + k*(bh + 12)
    proud, gap = max(0.0, R - a_), a_
    b.append(T(gx - 8, y + 17, f'lùi vào {a_:.1f}', text_anchor='end', font_size=9.5, fill='#55524b'))
    x = gx
    if proud > 0:
        b.append(f'<rect x="{x:.1f}" y="{y}" width="{proud*SCB:.1f}" height="{bh}" '
                 f'fill="#c07a12" stroke="#8a5608" stroke-width="1"/>')
        if proud > 1.5:
            b.append(T(x + proud*SCB/2, y + 17, f'{proud:.1f}', text_anchor='middle',
                       font_size=9.5, fill='#fff'))
        x += proud*SCB
    if gap > 0:
        b.append(f'<rect x="{x:.1f}" y="{y}" width="{gap*SCB:.1f}" height="{bh}" '
                 f'fill="#a8332a" stroke="#7a2018" stroke-width="1"/>')
        if gap > 1.5:
            b.append(T(x + gap*SCB/2, y + 17, f'{gap:.1f}', text_anchor='middle',
                       font_size=9.5, fill='#fff'))
        x += gap*SCB
    if tag:
        b.append(T(x + 8, y + 17, tag, font_size=10, font_weight='bold',
                   fill='#2f7a3c' if tag == 'HỌ C' else '#55524b'))
b.append(f'<line x1="{gx + R*SCB:.1f}" y1="{gy + 8}" x2="{gx + R*SCB:.1f}" '
         f'y2="{gy + 20 + len(rows)*(bh+12):.1f}" stroke="#2f7a3c" stroke-width="1.4" '
         f'stroke-dasharray="5,4"/>')
b.append(T(gx + R*SCB + 4, gy + 4, f'{R:.1f}', font_size=9.5, fill='#2f7a3c'))
for i, (c, t) in enumerate([('#c07a12', 'ống nhô ra ngoài mặt vách'),
                            ('#a8332a', 'khe hở bắt buộc trên mặt vách')]):
    b.append(f'<rect x="{gx - 40 + i*180}" y="374" width="13" height="11" fill="{c}"/>')
    b.append(T(gx - 22 + i*180, 384, t, font_size=9.5, fill='#55524b'))

open('figs/fig13-ban-le-chim.svg', 'w').write(svg(940, 470, hdr(
    'HÌNH 13 — Vì sao bản lề chìm hẳn trong gỗ không quay được',
    'Cánh nắp là vật rắn quay quanh MỘT trục: mọi điểm nằm phía ngoài trục đều đi xuống khi mở. Trục lùi vào bao nhiêu thì dải "đi xuống" rộng bấy nhiêu.',
    f'Dải đó luôn bắt đầu từ mặt ngoài vách, nên nó luôn mở thẳng ra ngoài. Đẩy trục vào trong chỉ ĐỔI CHỖ cái nhìn thấy — tổng vẫn là {R:.1f} mm.')
    + ''.join(b)))
print('fig13 xong')
