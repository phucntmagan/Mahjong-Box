#!/usr/bin/env python3
"""Hinh 14 — tran hoc am va phan bau ngon tay. python3 tools/draw_grip.py
Moi tri so lay tu box_spec.derive(); xem tools/grip_hook.py de biet cach suy."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drawlib import *
import box_spec as B

S = B.derive()
Z_RIM, Z_LID, Z_FL = S['Z_RIM'], S['Z_LID'], S['Z_FLOOR']
RK = S['R_KN']
GD, WG, GR = B.GRIP_D, S['WALL_GRIP'], B.GRIP_R
APER, LIP = S['GRIP_APER'], S['GRIP_LIP_MIN']
ceil_, fing = S['grip_ceil'], S['fing_t']
BODY, LEAF, VOID, SKIN = '#7a4f2c', '#a9754a', '#efe7d8', '#d8a97e'
GRN, RED, AMB = '#2f7a3c', '#a8332a', '#c07a12'
P_HAND = B.mass_of(S, 'loi on dinh')[2]*9.81*B.DYN/2
WRAP = math.radians(B.WRAP_SKIN)
def pres(r): return P_HAND/(B.N_FING*B.FING_W*r*WRAP)*1000.0     # kPa
os.makedirs('figs', exist_ok=True)
b = ['<defs><clipPath id="cg"><rect x="61" y="93" width="372" height="440"/></clipPath></defs>']

def arcp(cx, cz, r, a0, a1, n=16):
    return [(cx + r*math.cos(math.radians(a0 + (a1-a0)*i/n)),
             cz + r*math.sin(math.radians(a0 + (a1-a0)*i/n))) for i in range(n+1)]

# ==================================================== PANEL A: mat cat hoc am
SC = 6.4
v = V(168, 505, SC)
b.append(panel(60, 92, 374, 442,
               f'A · Mặt cắt hốc âm, tại một mắt mộng NẮP  TL {SC:.1f}:1'))
b.append('<g clip-path="url(#cg)">')
prof = S['grip_profile'](28)
# than: goc tren-ngoai bi HOM mat mong nap khoet mat mot phan tu dia
wall = ([(0.0, S['GRIP_Z_TOP']), (0.0, Z_RIM - RK)] + arcp(0.0, Z_RIM, RK, 270, 360)
        + [(WG, Z_RIM), (WG, Z_FL), (GD, Z_FL)] + list(prof)[::-1])
b.append(v.rect(-RK - 2, WG + 6, B.FOOT, Z_FL, BODY, sw=1.1))     # day hop
b.append(v.rect(-RK - 2, 2, 0, B.FOOT, '#2e221a', sw=0.8))        # chan dem
b.append(v.poly([(0.0, Z_FL), (GD, Z_FL)] + list(prof)[::-1], VOID, '#c9c3b6', 0.8))
b.append(v.poly(wall, BODY, sw=1.3))
b.append(v.rect(0.0, WG + 6, Z_RIM, Z_LID, LEAF, sw=1.2))         # canh nap dong
b.append(v.circ((0.0, Z_RIM), RK, LEAF, '#2a241c', 1.3))          # ong go, nho ra
b.append(v.circ((0.0, Z_RIM), S['KN_HOLE']/2, '#1a1208', '#1a1208', 0.6))

# ngon tay
top = [(-11.0, ceil_(0.0))] + list(prof)
bot = [(x, ceil_(x) - fing(x)) for x in [GD*i/24 for i in range(25)]][::-1]
b.append(v.poly(top + [(GD, ceil_(GD) - fing(GD))] + bot
                + [(-11.0, ceil_(0.0) - fing(0.0))], SKIN, '#9a6a44', 1.1,
                'fill-opacity="0.80"'))
b.append(T(v.X(2.4), v.Z(15.0), 'đốt ngón tay', font_size=9.5, fill='#7a4a28'))
b.append(v.path([(GD - B.L_DISTAL, Z_FL + 2.2), (GD, Z_FL + 2.2)], '#7a4a28', 1.4))
b.append(T(v.X(GD - B.L_DISTAL/2), v.Z(Z_FL + 2.2) + 12, f'{B.L_DISTAL:.0f}',
           text_anchor='middle', font_size=9, fill='#7a4a28'))
# tran hoc to dam
b.append(v.path(list(prof), GRN, 2.2))
b.append(v.path([(GD, Z_FL), (GD, ceil_(GD))], '#6b4326', 1.0, '4,3'))
b.append(v.circ((GR, S['GRIP_Z_TOP']), 0.35, GRN, GRN, 0.6))
b.append(v.path([(GR, S['GRIP_Z_TOP']), (GR + GR*math.cos(math.radians(212)),
                 S['GRIP_Z_TOP'] + GR*math.sin(math.radians(212)))], GRN, 0.9, '3,2'))
b.append(T(v.X(GR + 1.2), v.Z(S['GRIP_Z_TOP'] + 1.6), f'R{GR:.0f}', font_size=10,
           fill=GRN, font_weight='bold'))
b.append(T(v.X(GD + 1), v.Z(S['GRIP_Z_IN'] - 1.4), f'{B.GRIP_SLOPE:.0f}°',
           font_size=9.5, fill=GRN, font_weight='bold'))
_DAT = [(Z_RIM, f'vành Z{Z_RIM:.0f}', '#8a857c'),
        (Z_RIM - RK, f'hõm mắt mộng Z{Z_RIM-RK:.1f}', AMB),
        (S['GRIP_Z_TOP'], f'đỉnh bo Z{S["GRIP_Z_TOP"]:.1f}', RED),
        (Z_FL, f'sàn Z{Z_FL:.0f}', '#8a857c')]
for z, lbl, c in _DAT:
    b.append(v.path([(-13, z), (WG + 3, z)], c, 0.8, '6,4'))
b.append('</g>')
for z, lbl, c in _DAT:
    b.append(T(v.X(WG + 4), v.Z(z) + 3.2, lbl, font_size=8.5, fill=c))
# kich thuoc
b.append(f'<line x1="{v.X(-9):.1f}" y1="{v.Z(Z_FL):.1f}" x2="{v.X(-9):.1f}" '
         f'y2="{v.Z(S["GRIP_Z_TOP"]):.1f}" stroke="{RED}" stroke-width="1.4"/>')
b.append(T(v.X(-10), v.Z((Z_FL + S['GRIP_Z_TOP'])/2), f'{APER:.1f}', text_anchor='end',
           font_size=11, fill=RED, font_weight='bold'))
b.append(T(v.X(-10), v.Z((Z_FL + S['GRIP_Z_TOP'])/2) + 12, 'khe hở', text_anchor='end',
           font_size=8.5, fill=RED))
b.append(f'<line x1="{v.X(-4):.1f}" y1="{v.Z(S["GRIP_Z_TOP"]):.1f}" x2="{v.X(-4):.1f}" '
         f'y2="{v.Z(Z_RIM-RK):.1f}" stroke="{GRN}" stroke-width="1.4"/>')
b.append(T(v.X(-5), v.Z((S['GRIP_Z_TOP'] + Z_RIM - RK)/2) + 3, f'{LIP:.1f}',
           text_anchor='end', font_size=9.5, fill=GRN, font_weight='bold'))
b.append(v.dim(0, GD, Z_FL, f'sâu {GD:.0f}', dy=17))
b.append(v.dim(0, WG, B.FOOT, f'vách {WG:.0f}', dy=32))
b.append(T(v.X(-RK - 1), v.Z(Z_RIM + RK + 2), f'ống Ø{2*RK:.1f} nhô {RK:.1f}',
           text_anchor='end', font_size=9, fill=AMB))

# ==================================================== PANEL B: chuoi Z truoc/sau
b.append(panel(452, 92, 448, 214, 'B · Chuỗi Z của vách bản lề — bỏ hạ bậc thì được gì'))
bx, by, bw = 542, 124, 250
SCB = bw/Z_RIM
sets = [('Rev C2 · có hạ bậc',
         [(0, Z_FL, '#5c3d24'), (Z_FL, Z_FL + 20.0, RED),
          (Z_FL + 20.0, Z_RIM - B.T_LID, '#8a857c'), (Z_RIM - B.T_LID, Z_RIM, AMB)]),
        ('Rev C3 · bỏ hạ bậc',
         [(0, Z_FL, '#5c3d24'), (Z_FL, S['GRIP_Z_TOP'], RED),
          (S['GRIP_Z_TOP'], Z_RIM - RK, '#8a857c'), (Z_RIM - RK, Z_RIM, AMB)])]
for k, (lbl, segs) in enumerate(sets):
    y = by + k*50
    b.append(T(bx - 6, y + 18, lbl, text_anchor='end', font_size=9, fill='#55524b'))
    for z0, z1, c in segs:
        b.append(f'<rect x="{bx + z0*SCB:.1f}" y="{y}" width="{(z1-z0)*SCB:.1f}" height="26" '
                 f'fill="{c}" stroke="#2a241c" stroke-width="0.9"/>')
        if (z1 - z0)*SCB > 22:
            b.append(T(bx + (z0+z1)/2*SCB, y + 18, f'{z1-z0:.1f}',
                       text_anchor='middle', font_size=9.5, fill='#fff', font_weight='bold'))
for i, (c, t) in enumerate((('#5c3d24', 'chân + đáy'), (RED, 'khe hở vào tay'),
                            ('#8a857c', 'gỗ đặc trên trần'), (AMB, 'thứ nằm trên đầu vách'))):
    b.append(f'<rect x="{470 + (i % 2)*216:.0f}" y="{by + 106 + (i//2)*17:.0f}" '
             f'width="11" height="10" fill="{c}"/>')
    b.append(T(485 + (i % 2)*216, by + 115 + (i//2)*17, t, font_size=9, fill='#55524b'))
b.append(T(468, by + 158, 'Hạ bậc bản lề cao đúng bề dày nắp (15) và chạy suốt vách.',
           font_size=9.5, fill='#55524b'))
b.append(T(468, by + 172, f'Bỏ nó thì thứ duy nhất còn trên đầu vách là hõm mắt mộng nắp '
           f'{RK:.1f} mm.', font_size=9.5, fill='#55524b'))
b.append(T(468, by + 186, f'Khe hở vào tay 20,0 → {APER:.1f}, và vẫn dư {LIP:.1f} mm gỗ đặc.',
           font_size=9.5, fill=GRN, font_weight='bold'))

# ==================================================== PANEL C: chon ban kinh bo
b.append(panel(452, 318, 448, 216, 'C · Bỏ hạ bậc mở cửa sổ bán kính bo từ R4 lên R8'))
gx, gy, gw, gh = 512, 356, 336, 112
R0, R1, P0v, P1v = 2.0, 14.0, 0.0, 600.0
def RX(r): return gx + (r - R0)/(R1 - R0)*gw
def PY(p): return gy + gh - (min(max(p, P0v), P1v) - P0v)/(P1v - P0v)*gh
b.append(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" fill="#fff" stroke="#d8d5ce"/>')
r_hard = P_HAND/(B.N_FING*B.FING_W*WRAP*B.P_COMFORT)
r_soft = P_HAND/(B.N_FING*B.FING_W*WRAP*B.P_TARGET)
old = B.GRIP_R; r_hi = None
for i in range(20, 141):
    B.GRIP_R = i/10
    d = B.derive()
    if d['GRIP_FLAT'] >= 3.0 and d['GRIP_LIP_MIN'] >= B.GRIP_LIP_REQ: r_hi = B.GRIP_R
B.GRIP_R = old
b.append(f'<rect x="{gx}" y="{gy}" width="{RX(r_soft)-gx:.1f}" height="{gh}" '
         f'fill="{RED}" fill-opacity="0.08"/>')
b.append(f'<rect x="{RX(r_hi):.1f}" y="{gy}" width="{gx+gw-RX(r_hi):.1f}" height="{gh}" '
         f'fill="{RED}" fill-opacity="0.08"/>')
b.append(f'<rect x="{RX(r_soft):.1f}" y="{gy}" width="{RX(r_hi)-RX(r_soft):.1f}" '
         f'height="{gh}" fill="{GRN}" fill-opacity="0.10"/>')
b.append('<path d="M ' + ' L '.join(f'{RX(R0+(R1-R0)*i/120):.1f},{PY(pres(R0+(R1-R0)*i/120)):.1f}'
                                    for i in range(121)) + f'" fill="none" stroke="{RED}" '
         f'stroke-width="2"/>')
for pv, c, lbl in ((B.P_COMFORT*1000, RED, f'{B.P_COMFORT*1000:.0f} kPa — đau'),
                   (B.P_TARGET*1000, AMB, f'{B.P_TARGET*1000:.0f} kPa — xách lâu được')):
    b.append(f'<line x1="{gx}" y1="{PY(pv):.1f}" x2="{gx+gw}" y2="{PY(pv):.1f}" '
             f'stroke="{c}" stroke-width="1" stroke-dasharray="5,3"/>')
    b.append(T(gx + 4 if pv > 300 else gx + gw - 4, PY(pv) - 4, lbl,
               text_anchor='start' if pv > 300 else 'end', font_size=8.5, fill=c))
for r, c, tag, dy in ((4.0, '#8a857c', 'R4 · Rev C2', 14), (B.GRIP_R, GRN, 'R8 · Rev C3', 30)):
    b.append(f'<line x1="{RX(r):.1f}" y1="{gy}" x2="{RX(r):.1f}" y2="{gy+gh}" '
             f'stroke="{c}" stroke-width="1.6"'
             + ('' if c == GRN else ' stroke-dasharray="4,3"') + '/>')
    b.append(f'<circle cx="{RX(r):.1f}" cy="{PY(pres(r)):.1f}" r="3.4" fill="{c}"/>')
    b.append(T(RX(r) + 5 if c == GRN else RX(r) - 5, gy + dy,
               f'{tag}: {pres(r):.0f} kPa', text_anchor='start' if c == GRN else 'end',
               font_size=9, fill=c, font_weight='bold' if c == GRN else 'normal'))
b.append(f'<path d="M {RX(r_soft):.1f},{gy-6} L {RX(r_soft):.1f},{gy-11} '
         f'L {RX(r_hi):.1f},{gy-11} L {RX(r_hi):.1f},{gy-6}" fill="none" '
         f'stroke="{GRN}" stroke-width="1.4"/>')
b.append(T((RX(r_soft)+RX(r_hi))/2, gy - 15, f'cửa sổ {r_soft:.2f} … {r_hi:.1f}',
           text_anchor='middle', font_size=9.5, fill=GRN, font_weight='bold'))
b.append(T(RX(r_hi) + 5, gy + gh - 8, 'trần phẳng còn dưới 3', font_size=8.5, fill=RED))
b.append(T(gx + 4, gy + gh - 8, 'mép cấn tay', font_size=8.5, fill=RED))
for r in range(2, 15, 2):
    b.append(T(RX(r), gy + gh + 13, f'{r}', text_anchor='middle', font_size=9, fill='#8a857c'))
b.append(T(gx + gw/2, gy + gh + 27, 'bán kính bo mép ngoài trần  R (mm)',
           text_anchor='middle', font_size=9.5, fill='#55524b'))
b.append(T(gx - 2, gy + gh + 44, 'Trục đứng: áp lực đầu ngón lúc lực còn dồn về mép bo.',
           font_size=9.5, fill='#55524b'))
b.append(T(gx - 2, gy + gh + 57, 'Rev C2 chặn trên là 4,30 vì hạ bậc khoá khe hở ở 20 mm.',
           font_size=9.5, fill='#55524b'))

ann = [(60, 556, v.X(11), v.Z(20),
        f'Trần hốc: bo R{GR:.0f} ở mép ngoài rồi dốc {B.GRIP_SLOPE:.0f}° vào trong — bề mặt '
        f'{S["GRIP_SURF"]:.1f} mm, dài hơn cả chiều sâu hốc {GD:.0f}'),
       (60, 573, v.X(-RK/2), v.Z(Z_RIM),
        f'Không còn hạ bậc. Ống gỗ Ø{2*RK:.1f} nhô ra {RK:.1f} mm mỗi bên; hõm của nó chỉ ăn '
        f'{RK:.1f} mm góc trên-ngoài của vách'),
       (60, 590, v.X(GD + 3), v.Z(Z_FL + 4),
        f'Thành sau {B.GRIP_BACK:.0f} chặn đầu ngón; dải gỗ trên hốc {S["GRIP_LEDGE"]:.1f} cao × '
        f'{S["GRIP_LEDGE_T"]:.0f} dày — nay dày HẾT bề dày vách')]

open('figs/fig14-hoc-am-bau-ngon.svg', 'w').write(svg(940, 604, hdr(
    'HÌNH 14 — Trần hốc âm: chỗ ngón tay bấu vào',
    f'Rev C3 bỏ hạ bậc bản lề. Trần hốc thôi lấy cao độ từ vách: nó được nâng vừa đủ để khe hẹp '
    f'nhất giữa lưng ngón tay và sàn hốc bằng {B.FING_MAR:.1f} mm.',
    f'Khe hở vào tay thành {APER:.1f} mm (Rev C2: 20,0) và bo mép đi từ R4 lên R{GR:.0f} — '
    f'áp lực lúc bắt lực {pres(4.0):.0f} → {pres(GR):.0f} kPa. Gỗ đặc trên trần còn {LIP:.1f} mm.')
    + ''.join(b) + annot(ann, 470)))
print('fig14 xong')
