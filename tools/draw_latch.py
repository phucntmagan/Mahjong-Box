#!/usr/bin/env python3
"""Hinh khoa nap. python3 tools/draw_latch.py ; roi ./tools/render_figs.sh
Moi toa do tu box_spec.derive()."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drawlib import *
import box_spec as B

S = B.derive()
W, YB, GO = S['W'], S['Y_BODY'], S['GRIP_OUT']
Z_FL, Z_RIM, Z_SEAM, Z_LID = S['Z_FLOOR'], S['Z_RIM'], S['Z_SEAM'], S['Z_LID']
XS, LW = S['X_SEAM'], S['LW']
PX, PZ = S['PIN_X'], S['PIN_Z']
DX, DZ = LW - PX, Z_LID - PZ
BODY, WALL, LID, LIDO, NU = '#8a5a33', '#7a4f2c', '#a9754a', '#d8c3a5', '#cbb08c'
CUT, DIM, ACC, GRN, MAGC = '#2a241c', '#55524b', '#a8332a', '#2f7a3c', '#2f5d9e'
os.makedirs('figs', exist_ok=True)

def rot_about(p, c, th):
    x, z = p[0]-c[0], p[1]-c[1]
    cs, sn = math.cos(th), math.sin(th)
    return (c[0] + x*cs - z*sn, c[1] + x*sn + z*cs)
PIN_L, PIN_R = (PX, PZ), (W-PX, PZ)
def leaf(th, right=False):
    p = [(2*B.R_KN, Z_RIM), (LW, Z_SEAM), (LW, Z_LID), (2*B.R_KN, Z_LID)]
    if right:
        p = [(W-x, z) for x, z in p]
        return [rot_about(q, PIN_R, -th) for q in p]
    return [rot_about(q, PIN_L, th) for q in p]
def seam_pt(th, right=False):
    p = (W-LW, (Z_SEAM+Z_LID)/2) if right else (LW, (Z_SEAM+Z_LID)/2)
    return rot_about(p, PIN_R if right else PIN_L, -th if right else th)
Z_BOLT = (Z_SEAM + Z_LID)/2      # chot nam giua be day do doc canh khe giua
def seam_dx(th): return DX*(1-math.cos(th)) + (Z_BOLT-PZ)*math.sin(th)
def theta_for_gap(g):
    lo, hi = 0.0, math.pi/2
    for _ in range(80):
        m = (lo+hi)/2
        if 2*seam_dx(m) < g: lo = m
        else: hi = m
    return (lo+hi)/2

E_BOLT = 6.5
TH = theta_for_gap(E_BOLT)

# ============================================================ PANEL A
v = V(80, 320, 1.5)
b = [panel(56, 92, 600, 250,
           'A · Vi sao khoa noi CANH voi CANH khong dung duoc  —  TL 1,5:1')]
b.append(v.rect(0, W, Z_FL, Z_RIM, BODY, CUT, 1.1))
for x0, x1 in [(0, S['WALL_HINGE']), (W-S['WALL_HINGE'], W)]:
    b.append(v.rect(x0, x1, Z_FL, Z_RIM, WALL, CUT, 1.1))
for right in (False, True):                       # canh mo (nhat, dut net)
    b.append(v.poly(leaf(TH, right), LIDO, ACC, 1.1, 'stroke-dasharray="5,3"'))
for right in (False, True):                       # canh dong
    b.append(v.poly(leaf(0.0, right), LID, CUT, 1.1))
for x0 in (PX, W-PX):
    b.append(v.circ((x0, PZ), B.R_KN, 'none', GRN, 1.0))
    b.append(v.circ((x0, PZ), B.D_PIN/2, '#1a1208', CUT, 0.9))
zb = (Z_SEAM + Z_LID)/2
b.append(v.rect(XS-14, XS+14, zb-1.6, zb+1.6, '#c9a227', CUT, 0.9))   # chot khi dong
sA, sB = seam_pt(TH), seam_pt(TH, True)                                # chot khi tach
b.append(v.rect(sA[0]-14, sA[0], sA[1]-1.6, sA[1]+1.6, '#c9a227', ACC, 1.0))
b.append(v.rect(sB[0], sB[0]+14, sB[1]-1.6, sB[1]+1.6, '#c9a227', ACC, 1.0))
b.append(v.dim(sA[0], sB[0], sA[1], f'tach {sB[0]-sA[0]:.1f} — chot {E_BOLT} da tuot',
               dy=-10, col=ACC))
ztop = leaf(TH)[2][1]
b.append(arrow(v.X(XS-84), v.Z(Z_LID), v.X(XS-84), v.Z(ztop), ACC, 1.6, 6))
b.append(T(v.X(XS-88), (v.Z(Z_LID)+v.Z(ztop))/2 + 3, f'venh len {ztop-Z_LID:.0f}',
           font_size=9.5, fill=ACC, text_anchor='end'))
b.append(T(356, 330, f'ca HAI canh cung mo {math.degrees(TH):.1f}° — day la truong hop'
           f' lat up hop', font_size=9.5, fill=ACC, text_anchor='middle'))
b.append(T(v.X(2*B.R_KN+4), v.Z(Z_LID)-6, 'canh nap khi DONG', font_size=9, fill=DIM))
b.append(T(v.X(PX)+16, v.Z(PZ)+4, f'P = ({PX:.0f} , {PZ:.0f})', font_size=9, fill=GRN))

# ============================================================ PANEL C
sc = 4.6
q = V(755, 230 + S['z_rim_at'](B.MAG_X[1])*sc, sc)
zr = S['z_rim_at'](B.MAG_X[1]); tl = S['t_lid'](B.MAG_X[1])
mw, md = B.MAG[0], B.MAG[1]
b.append(panel(672, 92, 284, 250, ''))
b.append(T(684, 110, 'C · Mat cat qua mot cap nam cham', font_size=11,
           font_weight='bold', fill='#55524b'))
b.append(T(684, 124, f'TL {sc}:1', font_size=9.5, fill='#55524b'))
b.append(q.rect(-GO, B.WALL_FB, zr-10, zr, WALL, CUT, 1.3))
b.append(q.rect(-GO, 26, zr, zr+tl, LID, CUT, 1.3))
b.append(q.rect(B.MAG_Y-md/2, B.MAG_Y+md/2, zr-B.MAG_REC, zr, MAGC, '#1a3a66', 1.2))
b.append(q.rect(B.MAG_Y-md/2, B.MAG_Y+md/2, zr, zr+B.MAG_REC, MAGC, '#1a3a66', 1.2))
b.append(q.path([(-GO-2, zr), (28, zr)], GRN, 1.1, '5,3'))
b.append(T(q.X(28)+4, q.Z(zr+tl/2)+3, f'nap {tl:.1f}', font_size=9, fill=DIM))
b.append(T(q.X(28)+4, q.Z(zr-5)+3, f'vanh Z{zr:.1f}', font_size=9, fill=GRN))
b.append(arrow(q.X(B.MAG_Y), q.Z(zr+B.MAG_REC+5), q.X(B.MAG_Y), q.Z(zr+0.5), MAGC, 1.8, 5))
b.append(arrow(q.X(B.MAG_Y), q.Z(zr-B.MAG_REC-5), q.X(B.MAG_Y), q.Z(zr-0.5), MAGC, 1.8, 5))
mv = 2*2*B.STILE*B.K['cocobolo ngang tho']*5
for k, t_ in enumerate([f'hut theo phuong Z — huong manh nhat cua nam cham',
                        f'go con {S["MAG_MAR_OUT"]:.1f} ra mep nap, {S["MAG_MAR_IN"]:.1f} vao long hop',
                        f'tu do theo X: gian no theo mua {mv:.2f} mm chi lam',
                        f'lech {mv/mw*100:.0f} % be mat, gan nhu khong doi luc hut']):
    b.append(T(684, 296+k*13, t_, font_size=9, fill=MAGC if k != 1 else DIM))

# ============================================================ PANEL B
p = V(80, 500, 1.5)
b.append(panel(56, 362, 900, 190,
               'B · Bo tri nam cham — nhin tu tren, dai mep truoc.  TL 1,5:1'))
b.append(p.rect(0, W, 0, 34, '#efe9dd', '#cfccc5', 0.8))
b.append(p.rect(0, W, -GO, 0, '#e2d7c4', '#cfccc5', 0.8))

b.append(p.rect(0, W, 0, B.WALL_FB, WALL, CUT, 1.1))
b.append(p.path([(XS, -GO-5), (XS, 38)], CUT, 1.0, '7,4'))
b.append(T(p.X(XS), p.Z(38)-4, 'khe rap giua', font_size=9, fill=DIM, text_anchor='middle'))
for xc in list(B.MAG_X) + [W-x for x in B.MAG_X]:
    b.append(p.rect(xc-mw/2, xc+mw/2, B.MAG_Y-md/2, B.MAG_Y+md/2, MAGC, '#1a3a66', 1.1))
    b.append(T(p.X(xc), p.Z(B.MAG_Y+9), f'{xc:.0f}', font_size=8.5, fill=MAGC,
               text_anchor='middle'))
b.append(p.dim(0, W, -GO, f'{W:.0f}', dy=26))
b.append(T(p.X(W)+10, p.Z(B.MAG_Y)-4, f'nam cham {mw:.0f} x {md:.0f} x {B.MAG[2]:.0f}',
           font_size=9, fill=MAGC))
b.append(T(p.X(W)+10, p.Z(B.MAG_Y)+10,
           f'dai chong nhau nap/vanh {B.WALL_FB:.0f} mm', font_size=9, fill=DIM))

b.append(T(p.X(4), p.Z(24)+3, 'long hop', font_size=8.5, fill=DIM))

open('figs/fig11-khoa-nap.svg', 'w').write(svg(980, 572,
  hdr('HÌNH 11 — Khóa nắp: vì sao phải nối NẮP với THÂN, và chặn đúng một phương',
      f'Trục chốt P = ({PX:.0f} , {PZ:.0f}), mép khe ráp giữa cách trục {math.hypot(DX,DZ):.1f} mm. '
      f'Mép khe đi gần như thẳng đứng lên: tỉ lệ dọc/ngang {DX/DZ:.1f} : 1.',
      'Hai cánh cùng mở thì hai mép khe nâng bằng nhau và chỉ tách nhau — mọi khóa nối cánh với cánh đều tuột ra.')
  + ''.join(b)))
print('fig11 xong')
