#!/usr/bin/env python3
"""Hinh 14 — tran hoc am va phan bau ngon tay. python3 tools/draw_grip.py
Moi tri so lay tu box_spec.derive(); xem tools/grip_hook.py de biet cach suy."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drawlib import *
import box_spec as B

S = B.derive()
Z_RIM, Z_LID, Z_FL = S['Z_RIM'], S['Z_LID'], S['Z_FLOOR']
RB_D, RB_H, RK = S['REBATE_D'], S['REBATE_H'], S['R_KN']
GD, WG, GR = B.GRIP_D, S['WALL_GRIP'], B.GRIP_R
APER, LIP = S['GRIP_APER'], B.GRIP_LIP
ceil_, fing = S['grip_ceil'], S['fing_t']
BODY, LEAF, VOID, SKIN = '#7a4f2c', '#a9754a', '#efe7d8', '#d8a97e'
GRN, RED, AMB = '#2f7a3c', '#a8332a', '#c07a12'
os.makedirs('figs', exist_ok=True)
b = ['<defs><clipPath id="cg"><rect x="61" y="93" width="372" height="440"/></clipPath></defs>']

# ==================================================== PANEL A: mat cat hoc am
SC = 6.4
v = V(164, 505, SC)
b.append(panel(60, 92, 374, 442, f'A · Mặt cắt hốc âm tại giữa hốc  TL {SC:.1f}:1'))
b.append('<g clip-path="url(#cg)">')

prof = S['grip_profile'](28)
# than hop: vach ban le da tru hoc am va ha bac
wall = ([(0.0, S['GRIP_Z_TOP']), (0.0, Z_RIM - RB_H), (RB_D, Z_RIM - RB_H),
         (RB_D, Z_RIM), (WG, Z_RIM), (WG, Z_FL), (GD, Z_FL)]
        + [(x, z) for x, z in prof][::-1])
b.append(v.rect(-2, WG + 6, B.FOOT, Z_FL, BODY, sw=1.1))            # day hop
b.append(v.rect(-2, 2, 0, B.FOOT, '#2e221a', sw=0.8))           # chan dem
b.append(v.poly([(0.0, Z_FL), (GD, Z_FL)] + [(x, z) for x, z in prof][::-1],
                VOID, '#c9c3b6', 0.8))                            # LONG hoc am
b.append(v.poly(wall, BODY, sw=1.3))
# canh nap dong + ong go
b.append(v.poly([(RB_D, Z_RIM), (WG + 6, Z_RIM), (WG + 6, Z_LID), (RB_D, Z_LID)],
                LEAF, sw=1.2))
b.append(v.circ((RB_D, Z_RIM), RK, LEAF, '#2a241c', 1.2))
b.append(v.circ((RB_D, Z_RIM), S['KN_HOLE']/2, '#1a1208', '#1a1208', 0.6))

# ngon tay
top = [(-11.0, ceil_(0.0))] + [(x, z) for x, z in prof]
bot = [(x, ceil_(x) - fing(x)) for x in [GD*i/24 for i in range(25)]][::-1]
fpoly = top + [(GD, ceil_(GD) - fing(GD))] + bot + [(-11.0, ceil_(0.0) - fing(0.0))]
b.append(v.poly(fpoly, SKIN, '#9a6a44', 1.1, 'fill-opacity="0.80"'))
b.append(T(v.X(3.0), v.Z(16.0), 'đốt ngón tay', font_size=9.5, fill='#7a4a28'))
b.append(v.path([(GD - B.L_DISTAL, Z_FL + 2.4), (GD, Z_FL + 2.4)], '#7a4a28', 1.4))
b.append(T(v.X(GD - B.L_DISTAL/2), v.Z(Z_FL + 2.4) + 12, f'{B.L_DISTAL:.0f}',
           text_anchor='middle', font_size=9, fill='#7a4a28'))
b.append(v.path([(0.0, ceil_(0.0)), (0.0, ceil_(0.0) - fing(0.0))], '#9a6a44', 0.8, '3,3'))

# duong tran hoc to dam + cac ghi chu hinh hoc
b.append(v.path(prof, GRN, 2.2))
b.append(v.path([(GD, Z_FL), (GD, ceil_(GD))], '#6b4326', 1.0, '4,3'))
b.append(v.circ((GR, S['GRIP_Z_TOP']), 0.35, GRN, GRN, 0.6))
b.append(v.path([(GR, S['GRIP_Z_TOP']), (GR + GR*math.cos(math.radians(215)),
                 S['GRIP_Z_TOP'] + GR*math.sin(math.radians(215)))], GRN, 0.9, '3,2'))
b.append(T(v.X(GR + 1.0), v.Z(S['GRIP_Z_TOP'] + 1.4), f'R{GR:.0f}', font_size=10,
           fill=GRN, font_weight='bold'))
b.append(v.path([(S['GRIP_XT'], S['GRIP_ZT']), (GD + 3, S['GRIP_ZT'])], GRN, 0.7, '3,2'))
b.append(T(v.X(GD + 4), v.Z(S['GRIP_Z_IN'] - 1.2), f'{B.GRIP_SLOPE:.0f}°',
           font_size=9.5, fill=GRN, font_weight='bold'))

# duong chuan
for z, lbl, c in [(Z_RIM, f'vành Z{Z_RIM:.0f}', GRN),
                  (Z_RIM - RB_H, f'đáy hạ bậc Z{Z_RIM-RB_H:.0f}', AMB),
                  (S['GRIP_Z_TOP'], f'đỉnh bo Z{S["GRIP_Z_TOP"]:.0f}', RED),
                  (Z_FL, f'sàn Z{Z_FL:.0f}', '#8a857c')]:
    b.append(v.path([(-13, z), (WG + 4, z)], c, 0.8, '6,4'))
    b.append(T(v.X(WG + 5), v.Z(z) + 3.2, lbl, font_size=8.5, fill=c))
b.append('</g>')

# kich thuoc
b.append(v.dim(-11, 0, Z_FL, '', dy=0))
b.append(f'<line x1="{v.X(-9):.1f}" y1="{v.Z(Z_FL):.1f}" x2="{v.X(-9):.1f}" '
         f'y2="{v.Z(S["GRIP_Z_TOP"]):.1f}" stroke="{RED}" stroke-width="1.2"/>')
b.append(T(v.X(-10), v.Z((Z_FL + S['GRIP_Z_TOP'])/2), f'{APER:.0f}', text_anchor='end',
           font_size=11, fill=RED, font_weight='bold'))
b.append(T(v.X(-10), v.Z((Z_FL + S['GRIP_Z_TOP'])/2) + 12, 'khe hở', text_anchor='end',
           font_size=8.5, fill=RED))
b.append(v.dim(0, GD, Z_FL, f'sâu {GD:.0f}', dy=17))
b.append(v.dim(0, WG, B.FOOT, f'vách {WG:.0f}', dy=32))
b.append(f'<line x1="{v.X(-4):.1f}" y1="{v.Z(S["GRIP_Z_TOP"]):.1f}" x2="{v.X(-4):.1f}" '
         f'y2="{v.Z(Z_RIM-RB_H):.1f}" stroke="{RED}" stroke-width="1.2"/>')
b.append(T(v.X(-5), v.Z((S['GRIP_Z_TOP'] + Z_RIM - RB_H)/2) + 3, f'{LIP:.0f}',
           text_anchor='end', font_size=9.5, fill=RED))

# ==================================================== PANEL B: dinh luat chuoi Z
b.append(panel(452, 92, 448, 206, 'B · Khe hở vào tay là phần CÒN LẠI của chuỗi Z'))
bx, by, bw = 486, 128, 300
SCB = bw/Z_RIM
segs = [(0, Z_FL, '#5c3d24', f'chân+đáy {Z_FL:.0f}'),
        (Z_FL, S['GRIP_Z_TOP'], RED, f'khe hở vào tay {APER:.0f}'),
        (S['GRIP_Z_TOP'], Z_RIM - RB_H, '#8a857c', f'sàn {LIP:.0f}'),
        (Z_RIM - RB_H, Z_RIM, AMB, f'hạ bậc = bề dày nắp {RB_H:.0f}')]
for z0, z1, c, lbl in segs:
    b.append(f'<rect x="{bx + z0*SCB:.1f}" y="{by}" width="{(z1-z0)*SCB:.1f}" height="30" '
             f'fill="{c}" stroke="#2a241c" stroke-width="0.9"/>')
    if (z1 - z0)*SCB > 20:
        b.append(T(bx + (z0+z1)/2*SCB, by + 20, f'{z1-z0:.0f}', text_anchor='middle',
                   font_size=10.5, fill='#fff', font_weight='bold'))
for i, (z0, z1, c, lbl) in enumerate(segs):
    b.append(f'<rect x="{bx - 2 + (i % 2)*152:.0f}" y="{by + 44 + (i//2)*17:.0f}" '
             f'width="11" height="10" fill="{c}"/>')
    b.append(T(bx + 12 + (i % 2)*152, by + 53 + (i//2)*17, lbl, font_size=9, fill='#55524b'))
b.append(T(bx - 2, by - 8, f'0', font_size=9, fill='#8a857c'))
b.append(T(bx + Z_RIM*SCB, by - 8, f'Z{Z_RIM:.0f}', text_anchor='end', font_size=9, fill='#8a857c'))
b.append(T(bx - 2, by + 96, f'Chỉ hai đòn bẩy: bề dày nắp và chiều cao vành. Nắp mỏng đi 1 mm',
           font_size=9.5, fill='#55524b'))
b.append(T(bx - 2, by + 110, f'thì khe hở rộng thêm đúng 1 mm — không có cách thứ ba.',
           font_size=9.5, fill='#55524b'))
b.append(T(bx - 2, by + 130, f'Trần hốc cũ đặt phẳng ở Z{Z_FL+28:.0f} — nằm TRONG dải hạ bậc, nên đoạn',
           font_size=9.5, fill=RED))
b.append(T(bx - 2, by + 144, f'trần phía mặt ngoài bị lấy mất: chỉ còn {GD-RB_D:.1f} mm móc được.',
           font_size=9.5, fill=RED))

# ==================================================== PANEL C: chon ban kinh bo
b.append(panel(452, 310, 448, 224, 'C · Cửa sổ cho phép chỉ lọt đúng một dao: R4'))
gx, gy, gw, gh = 512, 362, 336, 110
R0, R1, U0, U1 = 2.0, 9.0, -3.0, 3.0
def RX(r): return gx + (r - R0)/(R1 - R0)*gw
def RY(u): return gy + gh - (u - U0)/(U1 - U0)*gh
b.append(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" fill="#fff" stroke="#d8d5ce"/>')
old, pts = B.GRIP_R, []
for i in range(71):
    B.GRIP_R = R0 + (R1 - R0)*i/70
    pts.append((B.GRIP_R, B.derive()['GRIP_FIT']))
B.GRIP_R = old
RMAX0 = 4.30
m0 = B.mass_of(S, 'loi on dinh')[2]*9.81*B.DYN/2
RMIN = m0/(B.N_FING*B.FING_W*math.radians(B.WRAP_SKIN)*B.P_COMFORT)
b.append(f'<rect x="{gx}" y="{RY(B.FING_MAR):.1f}" width="{gw}" '
         f'height="{gy+gh-RY(B.FING_MAR):.1f}" fill="{RED}" fill-opacity="0.07"/>')
b.append(f'<rect x="{gx}" y="{gy}" width="{RX(RMIN)-gx:.1f}" height="{gh}" '
         f'fill="{RED}" fill-opacity="0.07"/>')
b.append(f'<rect x="{RX(RMIN):.1f}" y="{gy}" width="{RX(RMAX0)-RX(RMIN):.1f}" height="{gh}" '
         f'fill="{GRN}" fill-opacity="0.10"/>')
b.append('<path d="M ' + ' L '.join(f'{RX(r):.1f},{RY(min(max(u,U0),U1)):.1f}' for r, u in pts)
         + f'" fill="none" stroke="{RED}" stroke-width="2"/>')
b.append(f'<line x1="{gx}" y1="{RY(B.FING_MAR):.1f}" x2="{gx+gw}" y2="{RY(B.FING_MAR):.1f}" '
         f'stroke="{RED}" stroke-width="1" stroke-dasharray="5,3"/>')
b.append(T(gx + gw - 4, RY(B.FING_MAR) - 4, f'khe tối thiểu {B.FING_MAR:.1f} mm',
           text_anchor='end', font_size=8.5, fill=RED))
b.append(T(RX(4.9), RY(-2.55), 'ngón tay KHÔNG lọt hết chiều sâu hốc', font_size=9.5, fill=RED))
b.append(f'<line x1="{RX(RMIN):.1f}" y1="{gy}" x2="{RX(RMIN):.1f}" y2="{gy+gh}" '
         f'stroke="#8a857c" stroke-width="1.2" stroke-dasharray="4,3"/>')
b.append(T(gx + 4, gy + 84, 'áp lực', font_size=8.5, fill=RED))
b.append(T(gx + 4, gy + 95, 'đầu ngón', font_size=8.5, fill=RED))
b.append(T(gx + 4, gy + 106, f'> {B.P_COMFORT*1000:.0f} kPa', font_size=8.5, fill=RED))
b.append(f'<path d="M {RX(RMIN):.1f},{gy-6} L {RX(RMIN):.1f},{gy-11} '
         f'L {RX(RMAX0):.1f},{gy-11} L {RX(RMAX0):.1f},{gy-6}" fill="none" '
         f'stroke="{GRN}" stroke-width="1.4"/>')
b.append(T((RX(RMIN)+RX(RMAX0))/2, gy - 15, f'{RMIN:.2f} … {RMAX0:.2f}',
           text_anchor='middle', font_size=9.5, fill=GRN, font_weight='bold'))
RMAX0 = RMAX = 4.30
b.append(f'<line x1="{RX(RMAX):.1f}" y1="{gy}" x2="{RX(RMAX):.1f}" y2="{gy+gh}" '
         f'stroke="#8a857c" stroke-width="1.2" stroke-dasharray="4,3"/>')
b.append(T(RX(RMAX) + 4, gy + 13, f'chặn trên', font_size=9, fill='#8a857c'))
b.append(f'<line x1="{RX(B.GRIP_R):.1f}" y1="{gy}" x2="{RX(B.GRIP_R):.1f}" y2="{gy+gh}" '
         f'stroke="{GRN}" stroke-width="1.6"/>')
b.append(T(RX(B.GRIP_R) - 4, gy + 13, f'chốt R{B.GRIP_R:.0f}', text_anchor='end',
           font_size=10, fill=GRN, font_weight='bold'))
B.GRIP_R = 8.0; f8 = B.derive()['GRIP_FIT']; B.GRIP_R = old
b.append(f'<circle cx="{RX(8.0):.1f}" cy="{RY(max(f8,U0)):.1f}" r="3.4" fill="{RED}"/>')
b.append(T(RX(8.0) - 6, RY(max(f8, U0)) - 24, f'R8 (chép từ quai da): {f8:+.2f}',
           text_anchor='end', font_size=9, fill=RED))
b.append(f'<line x1="{RX(8.0):.1f}" y1="{RY(max(f8,U0))-20:.1f}" x2="{RX(8.0):.1f}" '
         f'y2="{RY(max(f8,U0))-5:.1f}" stroke="{RED}" stroke-width="0.9"/>')
for r in range(2, 10):
    b.append(T(RX(r), gy + gh + 13, f'{r}', text_anchor='middle', font_size=9, fill='#8a857c'))
for u in (-2, 0, 2):
    b.append(T(gx - 5, RY(u) + 3.5, f'{u}', text_anchor='end', font_size=8.5, fill='#8a857c'))
b.append(T(gx + gw/2, gy + gh + 26, 'bán kính bo mép ngoài trần  R (mm)',
           text_anchor='middle', font_size=9.5, fill='#55524b'))
b.append(T(gx - 2, gy + gh + 42, 'Trục đứng: khe hẹp nhất giữa lưng ngón tay và sàn hốc.',
           font_size=9.5, fill='#55524b'))
b.append(T(gx - 2, gy + gh + 55, 'Bo nhỏ thì mép cấn tay; bo lớn thì lòng hốc thấp, ngón không lọt.',
           font_size=9.5, fill='#55524b'))

ann = [(60, 556, v.X(11), v.Z(25),
        f'Trần hốc: bo R{GR:.0f} ở mép ngoài rồi dốc {B.GRIP_SLOPE:.0f}° vào trong — bề mặt '
        f'{S["GRIP_SURF"]:.1f} mm, dài hơn cả chiều sâu hốc {GD:.0f}'),
       (60, 573, v.X(RB_D/2), v.Z(Z_RIM - RB_H/2),
        f'Hạ bậc bản lề {RB_D:.1f} × {RB_H:.0f} — đây là thứ khoá trần hốc xuống, không phải '
        f'chọn cho đẹp'),
       (60, 590, v.X(GD + 3), v.Z(Z_FL + 3),
        f'Thanh sau {B.GRIP_BACK:.0f} chặn đầu ngón; dải gỗ trên hốc {S["GRIP_LEDGE"]:.0f} cao × '
        f'{S["GRIP_LEDGE_T"]:.1f} dày là đường truyền lực khi xách')]

open('figs/fig14-hoc-am-bau-ngon.svg', 'w').write(svg(940, 604, hdr(
    'HÌNH 14 — Trần hốc âm: chỗ ngón tay bấu vào',
    f'Hạ bậc bản lề lấy hết gỗ trong {RB_D:.1f} mm ngoài cùng, từ Z{Z_RIM-RB_H:.0f} lên vành. '
    f'Trần hốc phải nằm dưới dải đó: khe hở vào tay = {Z_RIM:.0f} − {B.T_LID:.0f} − {LIP:.0f} '
    f'− {Z_FL:.0f} = {APER:.0f} mm.',
    f'Trong {APER:.0f} mm đó, bo mép R{GR:.0f} và dốc {B.GRIP_SLOPE:.0f}° chia lại: đốt ngón '
    f'{B.L_DISTAL:.0f} lọt hết chiều sâu {GD:.0f}, tì lên {S["GRIP_SURF"]:.1f} mm bề mặt thay vì '
    f'bấu một cạnh vuông.')
    + ''.join(b) + annot(ann, 470)))
print('fig14 xong')
