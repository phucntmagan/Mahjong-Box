"""Khung ban ve san xuat kho A3 ngang. Dung chung boi tools/drawings.py.

Kho giay A3 = 420 x 297 mm. Canvas tinh bang px o 96 dpi: 1 mm = 3.7795 px.
Moi sheet co khung, khung ten, o ghi chu chung va o sua doi.
"""
import math
from drawlib import T, esc, arrow

MM = 3.779528
PW, PH = round(420*MM), round(297*MM)          # 1587 x 1123
M = round(8*MM)                                # le giay
FR = (M, M, PW - 2*M, PH - 2*M)                # khung ve
TB_W, TB_H = round(150*MM), round(46*MM)       # khung ten
INK, DIM, ACC, GRN, RED = '#1a1a1a', '#55524b', '#a8332a', '#2f7a3c', '#a8332a'
THIN, MED, THICK = 0.7, 1.1, 1.8

# ------------------------------------------------------------------ toa do
class V:
    """He toa do 2D cho mot hinh chieu: (ox,oz) la goc (0,0); s = px/mm; z len."""
    def __init__(self, ox, oz, s): self.ox, self.oz, self.s = ox, oz, s
    def X(self, v): return self.ox + v*self.s
    def Z(self, v): return self.oz - v*self.s
    def P(self, p): return (self.X(p[0]), self.Z(p[1]))
    def rect(self, x0, x1, z0, z1, fill='none', st=INK, sw=MED, extra=''):
        return (f'<rect x="{self.X(x0):.2f}" y="{self.Z(z1):.2f}" '
                f'width="{(x1-x0)*self.s:.2f}" height="{(z1-z0)*self.s:.2f}" '
                f'fill="{fill}" stroke="{st}" stroke-width="{sw}" {extra}/>')
    def poly(self, pts, fill='none', st=INK, sw=MED, extra=''):
        d = ' '.join(f'{self.X(a):.2f},{self.Z(b):.2f}' for a, b in pts)
        return (f'<polygon points="{d}" fill="{fill}" stroke="{st}" stroke-width="{sw}" '
                f'stroke-linejoin="round" {extra}/>')
    def path(self, pts, st=INK, sw=MED, dash=None, fill='none'):
        d = 'M ' + ' L '.join(f'{self.X(a):.2f},{self.Z(b):.2f}' for a, b in pts)
        da = f' stroke-dasharray="{dash}"' if dash else ''
        return f'<path d="{d}" fill="{fill}" stroke="{st}" stroke-width="{sw}"{da}/>'
    def circ(self, c, r, fill='none', st=INK, sw=MED):
        return (f'<circle cx="{self.X(c[0]):.2f}" cy="{self.Z(c[1]):.2f}" r="{r*self.s:.2f}" '
                f'fill="{fill}" stroke="{st}" stroke-width="{sw}"/>')
    def cross(self, c, r=3.2, col=ACC):
        x, y = self.P(c)
        return (f'<path d="M {x-r:.1f},{y} L {x+r:.1f},{y} M {x},{y-r:.1f} L {x},{y+r:.1f}" '
                f'stroke="{col}" stroke-width="{THIN}"/>')

# ------------------------------------------------------------------ kich thuoc
def _ar(x, y, a, L=7.0):
    """Mui ten dac tai (x,y), huong a (radian)."""
    p = [(x - L*math.cos(a - 0.30), y - L*math.sin(a - 0.30)),
         (x - L*math.cos(a + 0.30), y - L*math.sin(a + 0.30))]
    return (f'<polygon points="{x:.1f},{y:.1f} {p[0][0]:.1f},{p[0][1]:.1f} '
            f'{p[1][0]:.1f},{p[1][1]:.1f}" fill="{DIM}"/>')

def dim_h(v, x0, x1, z, txt, off=26, col=DIM, fs=10.5, ext=True):
    """Kich thuoc ngang giua x0..x1, duong ghi cach cao do z mot doan off px (xuong)."""
    a, b, y = v.X(x0), v.X(x1), v.Z(z) + off
    o = []
    if ext:
        for xx, zz in ((a, v.Z(z)), (b, v.Z(z))):
            o.append(f'<line x1="{xx:.1f}" y1="{zz:.1f}" x2="{xx:.1f}" y2="{y + 5*(1 if off>0 else -1):.1f}" '
                     f'stroke="{col}" stroke-width="{THIN}"/>')
    o.append(f'<line x1="{a:.1f}" y1="{y:.1f}" x2="{b:.1f}" y2="{y:.1f}" '
             f'stroke="{col}" stroke-width="{THIN}"/>')
    if abs(b - a) > 26:
        o += [_ar(a, y, math.pi), _ar(b, y, 0.0)]
    else:
        o.append(f'<line x1="{a-11:.1f}" y1="{y:.1f}" x2="{b+11:.1f}" y2="{y:.1f}" '
                 f'stroke="{col}" stroke-width="{THIN}"/>')
        o += [_ar(a, y, 0.0), _ar(b, y, math.pi)]
    o.append(T((a+b)/2, y - 5, txt, text_anchor='middle', font_size=fs, fill=col))
    return ''.join(o)

def dim_v(v, z0, z1, x, txt, off=26, col=DIM, fs=10.5, ext=True):
    """Kich thuoc dung giua z0..z1, duong ghi cach x mot doan off px (sang trai am)."""
    a, b, xx = v.Z(z0), v.Z(z1), v.X(x) + off
    o = []
    if ext:
        for yy, x_ in ((a, v.X(x)), (b, v.X(x))):
            o.append(f'<line x1="{x_:.1f}" y1="{yy:.1f}" x2="{xx + 5*(1 if off>0 else -1):.1f}" '
                     f'y2="{yy:.1f}" stroke="{col}" stroke-width="{THIN}"/>')
    o.append(f'<line x1="{xx:.1f}" y1="{a:.1f}" x2="{xx:.1f}" y2="{b:.1f}" '
             f'stroke="{col}" stroke-width="{THIN}"/>')
    if abs(b - a) > 26:
        o += [_ar(xx, a, math.pi/2), _ar(xx, b, -math.pi/2)]
    else:
        o.append(f'<line x1="{xx:.1f}" y1="{a+11:.1f}" x2="{xx:.1f}" y2="{b-11:.1f}" '
                 f'stroke="{col}" stroke-width="{THIN}"/>')
        o += [_ar(xx, a, -math.pi/2), _ar(xx, b, math.pi/2)]
    o.append(f'<g transform="translate({xx-5:.1f},{(a+b)/2:.1f}) rotate(-90)">'
             + T(0, 0, txt, text_anchor='middle', font_size=fs, fill=col) + '</g>')
    return ''.join(o)

def lead(px, py, tx, ty, txt, col=DIM, fs=10, anchor=None):
    """Duong dan tu diem (px,py) toi nhan chu tai (tx,ty)."""
    anchor = anchor or ('end' if tx < px else 'start')
    dx = -6 if anchor == 'end' else 6
    return (f'<polyline points="{px:.1f},{py:.1f} {tx+dx:.1f},{ty-4:.1f} {tx+dx*3:.1f},{ty-4:.1f}" '
            f'fill="none" stroke="{col}" stroke-width="{THIN}"/>'
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.4" fill="{col}"/>'
            + T(tx, ty, txt, text_anchor=anchor, font_size=fs, fill=col))

def balloon(px, py, tx, ty, n, col=ACC):
    return (f'<polyline points="{px:.1f},{py:.1f} {tx:.1f},{ty:.1f}" fill="none" '
            f'stroke="{col}" stroke-width="{THIN}"/>'
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.4" fill="{col}"/>'
            f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="10" fill="#fff" stroke="{col}" '
            f'stroke-width="{MED}"/>'
            + T(tx, ty + 4, str(n), text_anchor='middle', font_size=11,
                font_weight='bold', fill=col))

def viewbox(x, y, w, h, label, sub='', tl=''):
    """Khung mot hinh chieu tren sheet."""
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#c9c5bd" '
         f'stroke-width="{THIN}" stroke-dasharray="6,4"/>',
         T(x + 8, y + 18, label, font_size=13, font_weight='bold', fill=INK)]
    if sub: o.append(T(x + 8, y + 33, sub, font_size=10, fill=DIM))
    if tl:  o.append(T(x + w - 8, y + 18, tl, text_anchor='end', font_size=11,
                       font_weight='bold', fill=DIM))
    return ''.join(o)

def table(x, y, cols, rows, w, rh=17, fs=9.5, head=True, zebra=True, colw=None):
    """Bang. cols = danh sach tieu de; rows = danh sach hang (list chu)."""
    n = len(cols)
    colw = colw or [w/n]*n
    o = []
    yy = y
    if head:
        o.append(f'<rect x="{x}" y="{yy}" width="{w}" height="{rh}" fill="#ece8e0" '
                 f'stroke="#b8b5ae" stroke-width="{THIN}"/>')
        cx = x
        for c, cw in zip(cols, colw):
            o.append(T(cx + 5, yy + rh - 5, c, font_size=fs, font_weight='bold', fill=INK))
            cx += cw
        yy += rh
    for i, r in enumerate(rows):
        if zebra and i % 2:
            o.append(f'<rect x="{x}" y="{yy}" width="{w}" height="{rh}" fill="#f4f2ee"/>')
        cx = x
        for j, (c, cw) in enumerate(zip(r, colw)):
            al = 'end' if (j and str(c) and str(c)[0].isdigit()) else 'start'
            o.append(T(cx + (cw - 6 if al == 'end' else 5), yy + rh - 5, c,
                       text_anchor=al, font_size=fs, fill=INK))
            cx += cw
        o.append(f'<line x1="{x}" y1="{yy+rh:.1f}" x2="{x+w}" y2="{yy+rh:.1f}" '
                 f'stroke="#dcd8d0" stroke-width="{THIN}"/>')
        yy += rh
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{yy-y}" fill="none" '
             f'stroke="#b8b5ae" stroke-width="{THIN}"/>')
    cx = x
    for cw in colw[:-1]:
        cx += cw
        o.append(f'<line x1="{cx:.1f}" y1="{y}" x2="{cx:.1f}" y2="{yy}" '
                 f'stroke="#dcd8d0" stroke-width="{THIN}"/>')
    return ''.join(o), yy

# ------------------------------------------------------------------ khung ten
PROJ = 'HỘP MAHJONG 152 QUÂN — BURLORA'
def titleblock(code, name, scale, mat, mass, rev, date, sheet_no, sheet_n):
    x = FR[0] + FR[2] - TB_W
    y = FR[1] + FR[3] - TB_H
    o = [f'<rect x="{x}" y="{y}" width="{TB_W}" height="{TB_H}" fill="#fff" stroke="{INK}" '
         f'stroke-width="{MED}"/>']
    r1 = y + 22
    o += [f'<line x1="{x}" y1="{r1}" x2="{x+TB_W}" y2="{r1}" stroke="{INK}" stroke-width="{THIN}"/>',
          T(x + 8, y + 16, PROJ, font_size=11, font_weight='bold', fill=INK)]
    o.append(T(x + 8, r1 + 22, name, font_size=15, font_weight='bold', fill=INK))
    r2 = r1 + 32
    o.append(f'<line x1="{x}" y1="{r2}" x2="{x+TB_W}" y2="{r2}" stroke="{INK}" stroke-width="{THIN}"/>')
    cells = [('MÃ', code), ('TỈ LỆ', scale), ('KHỐI LƯỢNG', mass),
             ('VẬT LIỆU', mat), ('REV', rev), ('TỜ', f'{sheet_no}/{sheet_n}')]
    cw = TB_W/3
    for k, (lab, val) in enumerate(cells):
        cx = x + (k % 3)*cw
        cy = r2 + (k//3)*((TB_H - (r2 - y))/2)
        o.append(T(cx + 8, cy + 13, lab, font_size=7.5, fill=DIM))
        o.append(T(cx + 8, cy + 27, val, font_size=11, font_weight='bold', fill=INK))
        if k % 3: o.append(f'<line x1="{cx:.1f}" y1="{r2}" x2="{cx:.1f}" y2="{y+TB_H}" '
                           f'stroke="#dcd8d0" stroke-width="{THIN}"/>')
    o.append(f'<line x1="{x}" y1="{r2+(TB_H-(r2-y))/2:.1f}" x2="{x+TB_W}" '
             f'y2="{r2+(TB_H-(r2-y))/2:.1f}" stroke="#dcd8d0" stroke-width="{THIN}"/>')
    o.append(T(x - 8, y + TB_H - 6, f'Ngày {date} · đơn vị mm · góc chiếu thứ nhất',
               text_anchor='end', font_size=9, fill=DIM))
    return ''.join(o)

def sheet(code, name, scale, mat, mass, sheet_no, sheet_n, body,
          notes=(), rev='C3', date='30-08-2026', head=''):
    o = [f'<rect width="100%" height="100%" fill="#ffffff"/>',
         f'<rect x="{FR[0]}" y="{FR[1]}" width="{FR[2]}" height="{FR[3]}" fill="none" '
         f'stroke="{INK}" stroke-width="{THICK}"/>']
    if head:
        o.append(T(FR[0] + 14, FR[1] + 26, head, font_size=12, fill=DIM))
    if notes:
        nx = FR[0] + FR[2] - TB_W
        ny = FR[1] + FR[3] - TB_H - 12 - 15*len(notes)
        o.append(T(nx, ny - 6, 'GHI CHÚ', font_size=10, font_weight='bold', fill=INK))
        for i, n in enumerate(notes):
            o.append(T(nx, ny + 11 + i*15, f'{i+1}. {n}', font_size=9.5, fill=INK))
    o.append(body)
    o.append(titleblock(code, name, scale, mat, mass, rev, date, sheet_no, sheet_n))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{PW}" height="{PH}" '
            f'viewBox="0 0 {PW} {PH}" font-family="DejaVu Sans" font-size="10">'
            + ''.join(o) + '</svg>')
