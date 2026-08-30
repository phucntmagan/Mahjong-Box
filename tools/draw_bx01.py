#!/usr/bin/env python3
"""Sheet BX-01 — than hop. Sinh figs/fig9 (mat bang) va figs/fig10 (mat cat).
Chay: python3 tools/draw_bx01.py ; roi ./tools/render_figs.sh
Moi toa do lay tu box_spec.derive() — khong go cung so nao."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drawlib import *
import box_spec as B

S = B.derive()
W, YO, YB, ZO = S['W'], S['Y_OA'], S['Y_BODY'], S['Z_OA']
WH, BAY, DIV, ACB = S['WALL_HINGE'], S['BAY'], S['DIV'], S['AC_BAY']
FB, IY, GO = B.WALL_FB, B.INNER_Y, S['GRIP_OUT']
Z_FL, Z_RIM, Z_SEAM, Z_LID = S['Z_FLOOR'], S['Z_RIM'], S['Z_SEAM'], S['Z_LID']
XS, ACL = S['X_SEAM'], B.AC_CLR
BODY, WALL, TRAYC, AC, LID, NU = '#8a5a33', '#7a4f2c', '#c2ab84', '#b39268', '#a9754a', '#cbb08c'
CUT, DIM, ACC, HID, VOID = '#2a241c', '#55524b', '#a8332a', '#2f5d9e', '#f4efe6'
os.makedirs('figs', exist_ok=True)

x_bay = [(WH, WH+BAY), (W-WH-BAY, W-WH)]
x_div = [(WH+BAY, WH+BAY+DIV), (W-WH-BAY-DIV, W-WH-BAY)]
x_ac  = (WH+BAY+DIV, WH+BAY+DIV+ACB)
GY0, GY1 = S['GRIP_Y0'], S['GRIP_Y1']
wells = [WH+BAY/2, XS, W-WH-BAY/2]
kn = [(FB + S['KN_Y0'] + i*S['KN_PITCH'], i % 2 == 0)        # (y bat dau, la mong THAN?)
      for i in range(B.N_KN)]

def balloon(px, py, n, col=ACC):
    return (f'<circle cx="{px:.1f}" cy="{py:.1f}" r="8.5" fill="#fff" stroke="{col}" '
            f'stroke-width="1.3"/><text x="{px:.1f}" y="{py+3.6:.1f}" text-anchor="middle" '
            f'font-size="10" font-weight="bold" fill="{col}">{n}</text>')
def tag(v, fx, fy, bx, by, n):
    """bong so dat tai (bx,by) px, day dan toi diem (fx,fy) mm."""
    px, py = v.X(fx), v.Z(fy)
    return (f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{px:.1f}" y2="{py:.1f}" stroke="{ACC}" '
            f'stroke-width="0.8"/><circle cx="{px:.1f}" cy="{py:.1f}" r="2" fill="{ACC}"/>'
            + balloon(bx, by, n))

# ============================================================ FIG 9 — MAT BANG
v = V(126, 528, 1.0)
BL, BR, BT, BB = 96, 512, 116, 604
b = [panel(56, 92, 500, 520, 'MAT BANG — nhin tu tren, nap thao ra.  TL 1:1')]
for x0, x1 in [(0, WH), (W-WH, W)]:          # hoc am hai tay tren vach trai/phai
    b.append(v.rect(x0, x1, GY0, GY1, '#6b4526', CUT, 1.0))
b.append(v.rect(0, W, 0, YB, BODY, CUT, 1.3))
b.append(v.rect(WH, W-WH, FB, YB-FB, VOID, CUT, 1.0))
for a0, a1 in x_div:
    b.append(v.rect(a0, a1, FB, YB-FB, WALL, CUT, 1.0))
for a0, a1 in x_bay:                                     # khay quan
    b.append(v.rect(a0+1, a1-1, FB+ACL, YB-FB-ACL, TRAYC, CUT, 0.9))
    b.append(v.rect(a0+6, a1-6, FB+ACL+5, YB-FB-ACL-5, '#e8dcc2', CUT, 0.7))
b.append(v.rect(x_ac[0]+1, x_ac[1]-1, FB+ACL, YB-FB-ACL, AC, CUT, 0.9))
acx0, acx1 = x_ac[0]+1+B.AC_WALL, x_ac[1]-1-B.AC_WALL
jy0 = FB+ACL+B.AC_WALL
b.append(v.rect(XS-B.AC_JOKER[0]/2, XS+B.AC_JOKER[0]/2, jy0, jy0+B.AC_JOKER[1], '#8f7449', CUT, 0.8))
dy0 = jy0+B.AC_JOKER[1]+B.AC_WALL
b.append(v.rect(acx0, acx1, dy0, dy0+S['AC_DICE_L'], '#9c8055', CUT, 0.8))
ay0 = dy0+S['AC_DICE_L']+B.AC_WALL
b.append(v.rect(acx0, acx1, ay0, ay0+B.AC_AUX_L, '#9c8055', CUT, 0.8))
f = 2*B.DICE_SOCK+3*B.DICE_RIB
cy = dy0+S['AC_DICE_L']/2
for i in (0, 1):
    for j in (0, 1):
        sx = XS - f/2 + B.DICE_RIB + i*(B.DICE_SOCK+B.DICE_RIB)
        sy = cy - f/2 + B.DICE_RIB + j*(B.DICE_SOCK+B.DICE_RIB)
        b.append(v.rect(sx, sx+B.DICE_SOCK, sy, sy+B.DICE_SOCK, '#6b5638', CUT, 0.7))
jmid = jy0+B.AC_JOKER[1]/2
for sgn in (-1, 1):
    xc = XS + sgn*B.AC_JOKER[0]/2
    b.append(f'<path d="M {v.X(xc):.1f},{v.Z(jmid-B.SCAL_D/2):.1f} '
             f'A {B.SCAL_DEP:.1f},{B.SCAL_D/2:.1f} 0 0 {1 if sgn>0 else 0} '
             f'{v.X(xc):.1f},{v.Z(jmid+B.SCAL_D/2):.1f} Z" fill="{VOID}" stroke="{ACC}" '
             f'stroke-width="1.1"/>')
for c in wells:                                          # khe luon ngon
    w0, w1 = c-B.WELL_W/2, c+B.WELL_W/2
    for y0, y1 in [(FB-B.WELL_D, FB), (YB-FB, YB-FB+B.WELL_D)]:
        b.append(v.rect(w0, w1, y0, y1, VOID, ACC, 1.2))
    for y0, y1 in [(FB+ACL, FB+ACL+B.NOTCH_D), (YB-FB-ACL-B.NOTCH_D, YB-FB-ACL)]:
        b.append(v.rect(w0, w1, y0, y1, VOID, ACC, 1.2))
for xc in list(B.MAG_X) + [W-x for x in B.MAG_X]:         # hoc nam cham khoa nap
    for yc in (B.MAG_Y, YB-B.MAG_Y):
        b.append(v.rect(xc-B.MAG[0]/2, xc+B.MAG[0]/2, yc-B.MAG[1]/2, yc+B.MAG[1]/2,
                        '#2f5d9e', '#1a3a66', 1.0))
RK, RB = S['R_KN'], S['REBATE_D']
for xp in (S['PIN_X'], W - S['PIN_X']):   # truc chot: LUI VAO dung RK -> ong chim han
    lo, hi = min(xp-RK, xp+RK), max(xp-RK, xp+RK)
    b.append(v.rect(lo, hi, kn[0][0]-2, kn[-1][0]+B.KN_LEN+2, VOID, ACC, 0.9,
                    'stroke-dasharray="3,3"'))          # ha bac vanh, suot chuoi mong
    for y0, is_body in kn:
        b.append(v.rect(lo, hi, y0, y0+B.KN_LEN, WALL if is_body else LID, CUT, 0.8))
    b.append(v.path([(xp, kn[0][0]-12), (xp, kn[-1][0]+B.KN_LEN+12)], ACC, 1.4, '10,4'))
# chuoi kich thuoc
xs_ = [0, WH, WH+BAY, x_ac[0], x_ac[1], W-WH-BAY, W-WH, W]
for i in range(len(xs_)-1):
    b.append(v.dim(xs_[i], xs_[i+1], 0, f'{xs_[i+1]-xs_[i]:.0f}', dy=30))
b.append(v.dim(0, W, 0, f'{W:.0f}  THAN', dy=54))
b.append(v.dim(0, W, 0, f"{S['X_OA']:.1f}  PHU BI X (ong ban le chim han, khong nho ra)", dy=104))
for y0, y1, lbl, dx in [(FB, YB-FB, f'{IY:.0f}', 20), (0, YB, f'{YO:.0f}  PHU BI Y', 48)]:
    xx = v.X(W)+dx
    b.append(f'<line x1="{xx:.1f}" y1="{v.Z(y0):.1f}" x2="{xx:.1f}" y2="{v.Z(y1):.1f}" '
             f'stroke="{DIM}" stroke-width="0.8"/>'
             f'<line x1="{xx-3:.1f}" y1="{v.Z(y0):.1f}" x2="{xx+3:.1f}" y2="{v.Z(y0):.1f}" stroke="{DIM}" stroke-width="0.8"/>'
             f'<line x1="{xx-3:.1f}" y1="{v.Z(y1):.1f}" x2="{xx+3:.1f}" y2="{v.Z(y1):.1f}" stroke="{DIM}" stroke-width="0.8"/>'
             f'<text x="{xx-4:.1f}" y="{(v.Z(y0)+v.Z(y1))/2:.1f}" fill="{DIM}" font-size="9.5" '
             f'text-anchor="middle" transform="rotate(-90 {xx-4:.1f} {(v.Z(y0)+v.Z(y1))/2:.1f})">{lbl}</text>')
# chuan A/B/C
for lbl, px, py, lx, ly in [("B", v.X(-30), v.Z(YB*0.30), v.X(0), v.Z(YB*0.30)),
                            ("C", v.X(-30), v.Z(0), v.X(0), v.Z(0))]:
    b.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{lx:.1f}" y2="{ly:.1f}" stroke="{CUT}" stroke-width="1.1"/>'
             f'<rect x="{px-9:.1f}" y="{py-9:.1f}" width="18" height="18" fill="#fff" stroke="{CUT}" stroke-width="1.2"/>'
             f'<text x="{px:.1f}" y="{py+4:.1f}" text-anchor="middle" font-size="11" font-weight="bold">{lbl}</text>')
# duong cat
b.append(v.path([(-52, YB/2), (W+6, YB/2)], HID, 1.1, '12,4,3,4'))
b.append(T(v.X(-58), v.Z(YB/2)+4, 'A', font_size=11, font_weight='bold', fill=HID))
b.append(v.path([(XS-20, -8), (XS-20, YB+8)], HID, 1.1, '12,4,3,4'))
b.append(T(v.X(XS-20), v.Z(YB+14), 'B', font_size=11, font_weight='bold', fill=HID,
           text_anchor='middle'))
# bong so
ITEMS = [
 (1, (S['PIN_X'], kn[0][0]+B.KN_LEN/2), 'L',
  f'Truc chot go O{B.KN_PIN:.0f} LUI VAO {S["PIN_X"]:.1f} tu mat ngoai vach, o Z{S["Z_RIM"]:.0f} '
  f'(vanh than) — ong go chim han, KHONG nho ra ngoai phu bi. Doi xung hai ben.'),
 (2, (W-S['PIN_X'], kn[4][0]+B.KN_LEN/2), 'R',
  f'{B.N_KN} mat mong go x {B.KN_LEN:.0f}, buoc {S["KN_PITCH"]:.0f}, chuoi {S["KN_RUN"]:.0f}. '
  f'Mat sam thuoc THAN, mat sang thuoc NAP. Ong go O{2*S["R_KN"]:.1f}. Ha bac vanh '
  f'{S["REBATE_D"]:.1f} sau x {S["REBATE_H"]:.0f} cao suot {B.LID_L:.0f}.'),
 (3, (WH/2, GY1-14), 'L',
  f'Hoc am hai tay: rong {B.GRIP_W:.0f} (Y {GY0:.0f}..{GY1:.0f}), sau {B.GRIP_D:.0f}, khe ho vao '
  f'tay {S["GRIP_APER"]:.0f} tai mat ngoai. Tran bo R{B.GRIP_R:.0f} roi doc {B.GRIP_SLOPE:.0f}° '
  f'vao trong — HINH 14. Nam gon trong vach {WH:.0f}, khong noi go ra ngoai.'),
 (4, (wells[0], FB-B.WELL_D/2), 'B',
  f'Khe luon ngon nhac khay: hoc {B.WELL_W:.0f} x sau {B.WELL_D:.0f} vao vach truoc/sau.'),
 (5, (wells[2], YB-FB-ACL-B.NOTCH_D/2), 'R',
  f'Khoet xuyen mat dau khay {B.WELL_W:.0f} x cao {B.NOTCH_H:.0f} — mo moc ngon.'),
 (6, (XS+B.AC_JOKER[0]/2-6, jmid), 'T',
  f'Hom ngon O{B.SCAL_D:.0f} sau {B.SCAL_DEP:.0f}, hai ben ranh Joker, khoet suot chieu sau.'),
 (7, (XS+f/2, cy), 'B',
  f'4 o xuc xac {B.DICE_SOCK:.0f} x {B.DICE_SOCK:.0f} sau {B.DICE_SOCK_D:.0f}, vach {B.DICE_RIB:.0f}.'),
 (8, (x_div[0][1], YB*0.78), 'T',
  f'Vach ngan {DIV:.0f}, cao toi vanh tai chinh vi tri no.'),
 (9, (WH/2, kn[-1][0]+30), 'L',
  f'Vach ban le {WH:.0f} — SUY RA tu hoc am: sau {B.GRIP_D:.0f} + thanh sau '
  f'{B.GRIP_BACK:.0f}. Dai go tren hoc: cao {S["GRIP_LEDGE"]:.0f}, cho mong nhat '
  f'{S["GRIP_LEDGE_T"]:.1f} (da tru ha bac) — duong truyen luc khi xach.'),
 (10, (B.MAG_X[1], B.MAG_Y), 'B',
  f'Hoc nam cham khoa nap {B.MAG[0]+0.2:.1f} x {B.MAG[1]+0.2:.1f} x sau {B.MAG_REC:.1f}, '
  f'8 cai tren than (va 8 doi ung tren nap). Vi tri +/-0,2.'),
]
for n, (fx, fy), side, _ in ITEMS:
    bx, by = {'L': (BL, v.Z(fy)), 'R': (BR, v.Z(fy)),
              'T': (v.X(fx), BT), 'B': (v.X(fx), BB)}[side]
    b.append(tag(v, fx, fy, bx, by, n))
# chu giai
b.append(panel(572, 92, 588, 520, 'CHU GIAI'))
y = 122
for n, _, _, txt in ITEMS:
    b.append(balloon(590, y, n))
    for ln in _wrap(txt, 62) if (_wrap := (lambda s, n_: [s[i:i+n_] for i in range(0, len(s), n_)])) else []:
        pass
    words, line, out = txt.split(' '), '', []
    for wd in words:
        if len(line)+len(wd)+1 > 68: out.append(line); line = wd
        else: line = (line+' '+wd).strip()
    out.append(line)
    for k, ln in enumerate(out):
        b.append(T(608, y+4+k*14, ln, font_size=10.5))
    y += 14*len(out) + 12
y += 6
b.append(T(590, y, 'CHUAN', font_size=11, font_weight='bold'))
y += 16
for lbl, txt in B.DATUM:
    b.append(f'<rect x="{590-9}" y="{y-9}" width="18" height="18" fill="#fff" stroke="{CUT}" '
             f'stroke-width="1.2"/><text x="590" y="{y+4}" text-anchor="middle" font-size="11" '
             f'font-weight="bold">{lbl}</text>')
    words, line, out = txt.split(' '), '', []
    for wd in words:
        if len(line)+len(wd)+1 > 68: out.append(line); line = wd
        else: line = (line+' '+wd).strip()
    out.append(line)
    for k, ln in enumerate(out):
        b.append(T(608, y+4+k*14, ln, font_size=10.5, fill=DIM))
    y += 14*len(out) + 10

open('figs/fig9-bx01-mat-bang.svg', 'w').write(svg(1180, 668,
  hdr('BX-01 — THAN HOP, MAT BANG',
      f'Hop Mahjong 152 quan, BURLORA. Than {W:.0f} x {YO:.0f} x {ZO:.0f}; phu bi X {S["X_OA"]:.1f} ke ca ong ban le nho ra {S["R_KN"]:.1f} moi ben.',
      'Sheet nay truoc day KHONG TON TAI — than hop chi co mat trong mot chuoi kich thuoc tren GA-02 (review Rev B §2.2).')
  + ''.join(b)))
print('fig9 xong')

# ============================================================ FIG 10 — MAT CAT
SC = 1.62
b = []
va = V(84, 284, SC)
b.append(panel(56, 92, 664, 214, 'MAT CAT A-A — cat ngang giua hop.  TL 1,62:1'))
b.append(va.rect(0, W, 0, B.FOOT, '#4a3423', CUT, 0.9))
b.append(va.rect(0, W, B.FOOT, Z_FL, BODY, CUT, 1.2))
for x0, x1, zt in [(a0, a1, S['z_rim_at']((a0+a1)/2)) for a0, a1 in x_div]:
    b.append(va.rect(x0, x1, Z_FL, zt, WALL, CUT, 1.1))
# vach ban le: A-A cat DUNG qua giua hoc am, nen phai ve bien that —
# hoc am (bo tron + doc) o duoi, ha bac ban le o tren.
prof = S['grip_profile'](20)
wall_prof = ([(0.0, S['GRIP_Z_TOP']), (0.0, Z_RIM - S['REBATE_H']),
              (S['REBATE_D'], Z_RIM - S['REBATE_H']), (S['REBATE_D'], Z_RIM),
              (WH, Z_RIM), (WH, Z_FL), (B.GRIP_D, Z_FL)] + list(prof)[::-1])
for left in (True, False):
    b.append(va.poly([(x if left else W - x, z) for x, z in wall_prof], WALL, CUT, 1.1))
for a0, a1 in x_bay:
    for k in (0, 1):
        b.append(va.rect(a0+1, a1-1, Z_FL+k*B.TRAY_H, Z_FL+(k+1)*B.TRAY_H, TRAYC, CUT, 0.9))
        b.append(va.rect(a0+6, a1-6, Z_FL+k*B.TRAY_H+4, Z_FL+(k+1)*B.TRAY_H, '#e8dcc2', CUT, 0.7))
b.append(va.rect(x_ac[0]+1, x_ac[1]-1, Z_FL, Z_FL+B.AC_H, AC, CUT, 0.9))
for left in (True, False):
    xa = WH if left else XS+B.SEAM/2
    xb_ = XS-B.SEAM/2 if left else W-WH
    za, zb = (Z_RIM, Z_SEAM) if left else (Z_SEAM, Z_RIM)
    b.append(va.poly([(xa, za), (xb_, zb), (xb_, Z_LID), (xa, Z_LID)], LID, CUT, 1.1))
    b.append(va.rect(xa+(B.STILE if left else 0), xb_-(0 if left else B.STILE),
                     Z_LID-B.S_TOP-B.PAN_T, Z_LID-B.S_TOP, NU, CUT, 0.8))
for x0 in (S['PIN_X'], W - S['PIN_X']):             # ong go mat mong, chim han
    b.append(va.circ((x0, Z_RIM), S['R_KN'], LID, CUT, 1.2))
b.append(va.path([(-4, Z_RIM), (W+4, Z_RIM)], '#2f7a3c', 0.9, '6,4'))
b.append(va.dim(0, W, 0, f'{W:.0f}', dy=22))
for zz, dy_, lbl in [(B.FOOT, 10, f'chan dem {B.FOOT:.0f}'), (Z_FL, 0, f'day {B.BOT:.0f}'),
                     (Z_RIM, 0, f'vanh Z{Z_RIM:.0f}'), (Z_LID, -2, f'mat nap Z{Z_LID:.0f}')]:
    b.append(T(va.X(W)+8, va.Z(zz)+3+dy_, lbl, font_size=8.5, fill=DIM))
b.append(T(va.X(XS), va.Z(Z_LID)-6, f'khe rap giua {B.SEAM}  (Z{Z_SEAM:.0f})',
           font_size=8.5, fill=ACC, text_anchor='middle'))

vb = V(96, 502, SC)
b.append(panel(56, 326, 664, 238,
               f'MAT CAT B-B — cat doc tai X = {XS-20:.0f}, qua khoang khay quan.  TL 1,62:1'))
b.append(vb.rect(-GO, YB+GO, 0, B.FOOT, '#4a3423', CUT, 0.9))
b.append(vb.rect(-GO, YB+GO, B.FOOT, Z_FL, BODY, CUT, 1.2))
z_at = S['z_rim_at'](XS-20)
for y0, y1 in [(-GO, FB), (YB-FB, YB+GO)]:
    b.append(vb.rect(y0, y1, Z_FL, z_at, WALL, CUT, 1.1))
b.append(vb.rect(FB+ACL, YB-FB-ACL, Z_FL, Z_FL+B.AC_H, AC, CUT, 0.9))
b.append(vb.rect(-GO, YB+GO, z_at, Z_LID, LID, CUT, 1.1))
b.append(vb.rect(FB, YB-FB, Z_LID-B.S_TOP-B.PAN_T, Z_LID-B.S_TOP, NU, CUT, 0.8))
b.append(vb.dim(-GO, YB+GO, 0, f'{YO:.0f}  phu bi Y', dy=22))
b.append(vb.dim(0, YB, 0, f'{YB:.0f}  than, chuan C', dy=44))
for zz, lbl in [(Z_FL, f'san trong Z{Z_FL:.0f}'), (z_at, f'vanh Z{z_at:.1f}')]:
    b.append(T(vb.X(YB+GO)+8, vb.Z(zz)+3, lbl, font_size=8.5, fill=DIM))
b.append(T(vb.X(YB/2), vb.Z(Z_LID)-8,
           f'Hoc am hai tay o VACH TRAI/PHAI, khong nam trong mat cat nay — xem A-A va HINH 14',
           font_size=8.5, fill=ACC, text_anchor='middle'))
# chuan A tren mat cat
b.append(f'<line x1="{vb.X(YB*0.62):.1f}" y1="{vb.Z(0):.1f}" x2="{vb.X(YB*0.62):.1f}" '
         f'y2="{vb.Z(0)+26:.1f}" stroke="{CUT}" stroke-width="1.2"/>'
         f'<rect x="{vb.X(YB*0.62)-9:.1f}" y="{vb.Z(0)+26:.1f}" width="18" height="18" '
         f'fill="#fff" stroke="{CUT}" stroke-width="1.2"/>'
         f'<text x="{vb.X(YB*0.62):.1f}" y="{vb.Z(0)+39:.1f}" text-anchor="middle" '
         f'font-size="11" font-weight="bold">A</text>')

# --- CT 1: mat mong go CHIM HAN (ho C)
SD = 3.5
RH, KH, RB = S['R_KN'], S['KN_HOLE'], S['REBATE_D']
PXX, RBH = S['PIN_X'], S['REBATE_H']
Z_BOT = Z_RIM - 21
def arcd(cx, cz, r, a0, a1, n=20):
    return [(cx+r*math.cos(math.radians(a0+(a1-a0)*i/n)),
             cz+r*math.sin(math.radians(a0+(a1-a0)*i/n))) for i in range(n+1)]
vd = V(812, 118 + Z_LID*SD, SD)
b.append(panel(736, 92, 224, 214, f'CT 1 — mat mong go, chim han.  TL {SD:.1f}:1'))
# THAN: mat ngoai x=0 den Z_RIM-RBH, roi ha bac vao RB, roi ong go
b.append(vd.poly([(0, Z_BOT), (0, Z_RIM-RBH), (RB, Z_RIM-RBH), (RB, Z_RIM-RH)]
                 + arcd(PXX, Z_RIM, RH, 270, 360)
                 + [(WH, Z_RIM), (WH, Z_BOT)], WALL, CUT, 1.2))
# NAP: mep ngoai lui vao dung PIN_X
b.append(vd.poly([(PXX, Z_RIM+RH)] + arcd(PXX, Z_RIM, RH, 90, 0)
                 + [(WH, Z_RIM), (WH, Z_LID), (PXX, Z_LID)], LID, CUT, 1.2))
b.append(vd.circ((PXX, Z_RIM), RH, LID, CUT, 1.4))
b.append(vd.circ((PXX, Z_RIM), KH/2, '#1a1208', CUT, 1.0))
b.append(vd.path([(-3, Z_RIM), (WH+2, Z_RIM)], '#2f7a3c', 1.0, '5,3'))
b.append(vd.path([(0, Z_BOT-3), (0, Z_LID+4)], HID, 1.0, '8,3,2,3'))
b.append(T(vd.X(WH+3), vd.Z(Z_RIM)+3, f'Z{Z_RIM:.0f}', font_size=8, fill='#2f7a3c'))
b.append(T(vd.X(WH+3), vd.Z(Z_LID)+3, f'Z{Z_LID:.0f}', font_size=8, fill='#2f7a3c'))
b.append(vd.dim(0, RB, Z_LID, f'{RB:.1f}', dy=-5, fs=8))
b.append(arrow(vd.X(-6), vd.Z(Z_RIM-RBH/2), vd.X(RB-0.5), vd.Z(Z_RIM-RBH/2), ACC, 1.3, 4))
b.append(T(vd.X(-7), vd.Z(Z_RIM-RBH/2)+3, 'hạ bậc', text_anchor='end', font_size=8, fill=ACC))
for k, t in enumerate([f'trục chốt ({PXX:.1f} , {Z_RIM:.0f}) — lùi vào {PXX:.1f}',
                       f'ống Ø{2*RH:.1f} tiếp tuyến mặt ngoài TỪ TRONG',
                       f'→ nhô ra 0,0 mm',
                       f'hạ bậc {RB:.1f} × {RBH:.0f} = đúng bề dày nắp',
                       f'mép nắp lùi {S["LEAF_X0"]:.1f}',
                       f'chặn 180°: {S["STOP_A"]:.0f} mm²']):
    b.append(T(742, 252 + k*11, t, font_size=8, fill=DIM))

# --- CT 2: khe luon ngon
SE = 5.6
ytr, ztt = FB+ACL, Z_FL+2*B.TRAY_H
ve = V(848-11*SE, 420+36*SE, SE)
b.append(panel(736, 326, 224, 238, 'CT 2 — khe luon ngon.  TL 5,6:1'))
b.append(ve.rect(0, FB, 26, Z_RIM, WALL, CUT, 1.2))
b.append(ve.rect(FB-B.WELL_D, FB, 26, Z_RIM, VOID, ACC, 1.2))
b.append(ve.rect(ytr, ytr+12, 26, ztt, TRAYC, CUT, 1.0))
b.append(ve.rect(ytr, ytr+B.NOTCH_D, ztt-B.NOTCH_H, ztt, VOID, ACC, 1.2))
b.append(ve.path([(FB-B.WELL_D, S['Z_LIFT_LEDGE']), (ytr+B.NOTCH_D, S['Z_LIFT_LEDGE'])], ACC, 2.2))
b.append(arrow(ve.X(FB-B.WELL_D/2), ve.Z(S['Z_LIFT_LEDGE']-12),
               ve.X(FB-B.WELL_D/2), ve.Z(S['Z_LIFT_LEDGE']-1.5), ACC, 1.6, 5))
for k, t in enumerate([f'khe luon ngon {S["LIFT_CHANNEL"]:.1f} mm',
                       f'mo moc: sau {S["LIFT_LEDGE"]:.0f}, cao {S["LIFT_LIP"]:.0f}, o Z{S["Z_LIFT_LEDGE"]:.0f}',
                       f'da ngoai vach con {B.WALL_FB-B.WELL_D:.0f} mm — mat ngoai khong thung',
                       f'ni {B.WELL_FELT:.0f} mm dan day hoc: chan quan truot ra']):
    b.append(T(748, 512+k*13, t, font_size=9, fill=ACC if k < 2 else DIM))

open('figs/fig10-bx01-mat-cat.svg', 'w').write(svg(985, 620,
  hdr('BX-01 — THAN HOP, MAT CAT',
      f'Chuoi Z: chan {B.FOOT:.0f} + day {B.BOT:.0f} + 2 x khay {B.TRAY_H:.0f} + khe '
      f'{B.CLR_Z:.0f} = vanh Z{Z_RIM:.0f}; nap {B.T_HINGE:.0f} -> Z{Z_LID:.0f}.',
      f'Vanh than doc {S["ANG"]:.3f} do tu Z{Z_RIM:.0f} o canh mong len Z{Z_SEAM:.0f} o khe rap giua — dung goc vat cua nap.')
  + ''.join(b)))
print('fig10 xong')
