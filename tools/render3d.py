#!/usr/bin/env python3
"""
Dung hinh 3D cua hop tu chinh dac ta. python3 tools/render3d.py
Sinh figs/fig12a..e.svg ; render PNG bang ./tools/render_figs.sh

Khong dung thu vien ngoai. Bo dung hinh toi gian:
  - hinh khoi = danh sach mat tu giac trong khong gian
  - chieu phoi canh pinhole
  - thuat toan tho son (painter): sap xep mat theo do sau tam mat, ve xa truoc
  - chieu sang phang mot nguon + anh sang moi truong
Khong cull mat sau: hop co long rong, ta CAN nhin thay mat trong.
Moi kich thuoc lay tu box_spec.derive() — khong go cung so nao.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B

S = B.derive()
W, YB, GO = S['W'], S['Y_BODY'], S['GRIP_OUT']
WH, BAY, DIV, ACB = S['WALL_HINGE'], S['BAY'], S['DIV'], S['AC_BAY']
FB, IY = B.WALL_FB, B.INNER_Y
Z_FL, Z_RIM, Z_SEAM, Z_LID = S['Z_FLOOR'], S['Z_RIM'], S['Z_SEAM'], S['Z_LID']
XS, LW = S['X_SEAM'], S['LW']
PIN = (S['PIN_X'], S['PIN_Z'])          # truc xoay ban le

# --------------------------------------------------------------- mau sac
COL = dict(
    coco   = (0x7a, 0x45, 0x23),   # cocobolo
    coco_d = (0x5e, 0x33, 0x1a),   # cocobolo trong bong / mat cat
    burl   = (0xb8, 0x77, 0x33),   # Nu go do
    burl_d = (0x96, 0x5e, 0x28),
    tray   = (0x8a, 0x52, 0x2c),
    felt   = (0x6e, 0x2b, 0x2b),
    tile   = (0xf0, 0xe7, 0xd4),
    tile_e = (0xd8, 0xcb, 0xb0),
    mag    = (0x35, 0x48, 0x60),
    brass  = (0xc4, 0xa2, 0x4a),
    foot   = (0x2e, 0x22, 0x1a),
    cut    = (0xdd, 0xba, 0x8a),   # mat cat — sang han de doc duoc tung lop
    cov    = (0x94, 0x5f, 0x33),   # nap che o xuc xac — chi tiet roi, to khac de nhan ra
    cov_c  = (0xc2, 0x93, 0x59),   # mat cat cua nap che
)

# --------------------------------------------------------------- vector
def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def dot(a, b): return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def norm(a):
    n = math.sqrt(dot(a, a)) or 1.0
    return (a[0]/n, a[1]/n, a[2]/n)

LIGHT = norm((-0.45, -0.75, 0.85))

class Scene:
    """Mot mat = (dinh, mau, mat_na_canh).

    MAT NA CANH la thu quyet dinh hinh nhin ra khoi go hay khoi giay ke o. Mot
    mat lon phai chia nho de thuat toan tho son sap dung, nhung neu ve vien cho
    TUNG O thi ca khoi go hien nguyen luoi chia. Nen moi o mang mot mat na noi
    ro canh nao cua no nam tren BIEN cua mat goc; chi nhung canh do moi duoc ve
    vien. Vien di cung o nen thu tu chieu sau van dung — khong can luot ve rieng.
    """
    def __init__(self, clip_y=None):
        self.faces = []          # (verts, colour, edge_mask)
        self.clip_y = clip_y     # (y0, y1) — cat bo phan ngoai khoang
    # ---- nguyen thuy
    MAXCELL = 13.0     # canh o luoi toi da khi chia nho mat
    def quad(self, v, col, split=True):
        """Them mot tu giac. Chia nho neu no lon.

        Thuat toan tho son sap xep theo TAM mat, nen mot mat lon co tam gan
        camera hon se ve de len cac vat nho nam tren no o phia xa. Chia nho mat
        lon la cach re nhat de het hien tuong do.
        """
        if not split:
            self.faces.append((v, col, 0b1111)); return
        a, b, c, d = v
        e1 = math.sqrt(sum((b[i]-a[i])**2 for i in range(3)))
        e2 = math.sqrt(sum((d[i]-a[i])**2 for i in range(3)))
        nu = max(1, min(16, int(e1/self.MAXCELL) + 1))
        nv = max(1, min(16, int(e2/self.MAXCELL) + 1))
        if nu == 1 and nv == 1:
            self.faces.append((v, col, 0b1111)); return
        def P(u, w):   # noi suy song tuyen tinh
            return tuple(a[i]*(1-u)*(1-w) + b[i]*u*(1-w) + c[i]*u*w + d[i]*(1-u)*w
                         for i in range(3))
        for i in range(nu):
            for j in range(nv):
                u0, u1 = i/nu, (i+1)/nu
                w0, w1 = j/nv, (j+1)/nv
                # canh 0 = P(u0,w0)->P(u1,w0) ... theo thu tu dinh ben duoi
                m = ((1 if j == 0 else 0)
                     | (2 if i == nu-1 else 0)
                     | (4 if j == nv-1 else 0)
                     | (8 if i == 0 else 0))
                self.faces.append(([P(u0, w0), P(u1, w0), P(u1, w1), P(u0, w1)], col, m))
    def poly(self, v, col):
        """Da giac n dinh. n>4 duoc chia quat quanh trong tam: thuat toan tho son
        sap xep theo TAM mat, ma trong tam cua mot da giac co cung bo luon bi keo
        lech ve phia chum dinh -> sap sai. Chia quat lam moi manh co tam rieng."""
        if len(v) == 4: self.quad(v, col); return
        if len(v) < 4: self.faces.append((v, col, 0b111)); return
        n = len(v)
        c = tuple(sum(p[i] for p in v)/n for i in range(3))
        for i in range(n):
            # tam giac quat [c, v_i, v_i+1]: chi canh v_i->v_i+1 la bien that
            self.faces.append(([c, v[i], v[(i+1) % n]], col, 0b010))
    def _cy(self, y0, y1):
        """Cat theo mat phang Y. Tra ve (y0, y1, bi_cat_dau, bi_cat_cuoi)."""
        if self.clip_y is None: return y0, y1, False, False
        a, b = self.clip_y
        n0, n1 = max(y0, a), min(y1, b)
        if n1 <= n0 + 1e-9: return None, None, False, False
        return n0, n1, n0 > y0 + 1e-9, n1 < y1 - 1e-9
    def prism_y(self, poly_xz, y0, y1, col, col_cut=None):
        """Da giac trong mat phang X-Z, keo dai theo truc Y."""
        y0, y1, c0, c1 = self._cy(y0, y1)
        if y0 is None: return
        cc = col_cut or col
        n = len(poly_xz)
        self.poly([(x, y0, z) for x, z in poly_xz], cc if c0 else col)
        self.poly([(x, y1, z) for x, z in poly_xz], cc if c1 else col)
        for i in range(n):
            x0, z0 = poly_xz[i]; x1, z1 = poly_xz[(i+1) % n]
            self.quad([(x0, y0, z0), (x1, y0, z1), (x1, y1, z1), (x0, y1, z0)], col)
    def box(self, x0, x1, y0, y1, z0, z1, col, col_cut=None):
        self.prism_y([(x0, z0), (x1, z0), (x1, z1), (x0, z1)], y0, y1, col, col_cut)

# --------------------------------------------------------------- hinh hoc
def z_rim(x): return S['z_rim_at'](x)
def t_lid(x): return S['t_lid'](x)
def circle_xz(cx, cz, r, n=20):
    return [(cx + r*math.cos(2*math.pi*i/n), cz + r*math.sin(2*math.pi*i/n)) for i in range(n)]
def rot_xz(p, c, th):
    x, z = p[0]-c[0], p[1]-c[1]
    cs, sn = math.cos(th), math.sin(th)
    return (c[0] + x*cs - z*sn, c[1] + x*sn + z*cs)

RK, KH = S['R_KN'], S['KN_HOLE']
PXX, RB_D, RB_H = S['PIN_X'], S['REBATE_D'], S['REBATE_H']
LX0 = S['LEAF_X0']
KN = [(FB + S['KN_Y0'] + i*S['KN_PITCH'], i % 2 == 0)   # (y bat dau, la mong THAN?)
      for i in range(B.N_KN)]
X_BAY = [(WH, WH+BAY), (W-WH-BAY, W-WH)]
X_DIV = [(WH+BAY, WH+BAY+DIV), (W-WH-BAY-DIV, W-WH-BAY)]
X_AC = (WH+BAY+DIV, WH+BAY+DIV+ACB)
WELLS = [WH+BAY/2, XS, W-WH-BAY/2]

def gp(x0, prof):
    """Tiet dien vach ban le: x do tu MAT NGOAI vao. Vach trai giu nguyen,
    vach phai lat guong qua giua hop. Tra ve dung chieu quay cho prism_y."""
    if x0 == 0: return list(prof)
    return [(W - x, z) for x, z in prof][::-1]

def add_body(sc, show_mag=True):
    C, D = COL['coco'], COL['cut']
    sc.box(0, W, 0, YB, 0, B.FOOT, COL['foot'])                       # chan dem
    # ĐÁY: chia theo ĐÚNG các đường mà vách đứng lên trên nó. Một mặt đáy chạy
    # suốt 378 mm sẽ vắt qua chân vách, và thuật toán thợ sơn sắp theo tâm mặt
    # nên vài ô của nó vẽ đè lên vách — hiện ra thành răng cưa trong lòng hốc âm.
    # Cắt trước thì không ô nào còn vắt qua ranh giới, hết răng cưa.
    _gy0, _gy1 = S['GRIP_Y0'], S['GRIP_Y1']
    _xc = sorted({0.0, WH, W - WH, W})
    _yc = sorted({0.0, FB, _gy0, _gy1, YB - FB, YB})
    for _xa, _xb in zip(_xc, _xc[1:]):
        for _ya, _yb in zip(_yc, _yc[1:]):
            sc.box(_xa, _xb, _ya, _yb, B.FOOT, Z_FL, C, D)            # day

    # vach trai/phai (dinh phang Z_RIM), khoet hoc am hai tay o giua chieu sau.
    # Chia theo Z lam hai dai:
    #   duoi Z_TOPBAND : go day du, tru hoc am o bang Y cua hoc
    #   tren           : ho C bi ha bac; ho B bi HOM mat mong NAP khoet mot phan tu
    #                    dia o goc tren-ngoai, va chi o nhung bang Y co mong NAP
    gy0, gy1 = S['GRIP_Y0'], S['GRIP_Y1']
    Z_TB = Z_RIM - (RB_H if RB_H > 0 else RK)          # day cua dai tren
    prof = S['grip_profile']()                         # (0,Z_TOP) -> (GRIP_D,Z_IN)
    for x0, x1 in [(0, WH), (W-WH, W)]:
        for ya, yb_ in [(FB, gy0), (gy1, YB-FB)]:
            sc.box(x0, x1, ya, yb_, Z_FL, Z_TB, C, D)
        # doan co hoc am: thanh sau + dai go tren tran (tran bo tron roi doc)
        sc.prism_y(gp(x0, [(B.GRIP_D, Z_FL), (WH, Z_FL), (WH, Z_TB), (B.GRIP_D, Z_TB)]),
                   gy0, gy1, C, D)
        sc.prism_y(gp(x0, prof + [(B.GRIP_D, Z_TB), (0.0, Z_TB)]), gy0, gy1, C, D)
        # dai tren: cat theo tung bang mat mong
        if RB_H > 0:                                   # ho C — ha bac suot chieu dai
            sc.box(x0 + RB_D if x0 == 0 else x0, x1 if x0 == 0 else x1 - RB_D,
                   FB, YB-FB, Z_TB, Z_RIM, C, D)
        else:                                          # ho B — chi khoet o bang mong NAP
            cuts = [FB]
            for y0k, is_body in KN:
                if is_body: continue
                cuts += [y0k, y0k + B.KN_LEN]
            cuts.append(YB-FB)
            for ya, yb_ in zip(cuts, cuts[1:]):
                if yb_ - ya < 1e-6: continue
                lid_band = any(abs(ya - y0k) < 1e-6 for y0k, ib in KN if not ib)
                xin = RK if lid_band else 0.0
                sc.box(x0 + xin if x0 == 0 else x0, x1 if x0 == 0 else x1 - xin,
                       ya, yb_, Z_TB, Z_RIM, C, D)
    # vach truoc/sau. Chia theo X vi hai le: dinh vach doc (gay tai X=185) va
    # khe luon ngon an 6 mm vao mat trong -> tai bang khe, vach chi con 4 mm.
    cuts = sorted({0.0, XS, W}
                  | {w + s_*B.WELL_W/2 for w in S['WELL_X'] for s_ in (-1, 1)})
    for y0, y1, front in [(0, FB, True), (YB-FB, YB, False)]:
        for xa, xb in zip(cuts, cuts[1:]):
            xm = (xa + xb)/2
            in_well = any(abs(xm - w) < B.WELL_W/2 for w in S['WELL_X'])
            d_ = (B.WALL_FB - B.WELL_D) if in_well else B.WALL_FB
            ya, yb_ = (y0, y0 + d_) if front else (y1 - d_, y1)
            sc.prism_y([(xa, Z_FL), (xb, Z_FL), (xb, z_rim(xb)), (xa, z_rim(xa))],
                       ya, yb_, C, D)
    # vach ngan
    for x0, x1 in X_DIV:
        sc.prism_y([(x0, Z_FL), (x1, Z_FL), (x1, z_rim(x1)), (x0, z_rim(x0))],
                   FB, YB-FB, C, D)
    # mat mong go ben THAN: ong go O2R, tam LUI VAO PXX -> chim han
    for xk in (PXX, W - PXX):
        for y0, is_body in KN:
            if not is_body: continue
            sc.prism_y(circle_xz(xk, Z_RIM, RK), y0, y0 + B.KN_LEN, C, D)
    # nam cham tren vanh than (chi ve khi thuc su nhin thay duoc)
    for xc in (list(B.MAG_X) + [W-x for x in B.MAG_X]) if show_mag else []:
        for yc in (B.MAG_Y, YB-B.MAG_Y):
            sc.box(xc-B.MAG[0]/2, xc+B.MAG[0]/2, yc-B.MAG[1]/2, yc+B.MAG[1]/2,
                   z_rim(xc)-B.MAG_REC, z_rim(xc)-0.1, COL['mag'])

def add_tray(sc, x0, y0, z0, tiles=True):
    """Mot khay quan: 4 vach + day + ni + quan."""
    C, F = COL['tray'], COL['felt']
    w, l, h = B.TRAY[1], B.TRAY[0], B.TRAY[2]
    fl = h - B.TRAY_IN[2]
    sc.box(x0, x0+w, y0, y0+l, z0, z0+fl, C, COL['cut'])              # day khay
    sc.box(x0, x0+5, y0, y0+l, z0+fl, z0+h, C, COL['cut'])
    sc.box(x0+w-5, x0+w, y0, y0+l, z0+fl, z0+h, C, COL['cut'])
    sc.box(x0+5, x0+w-5, y0, y0+5, z0+fl, z0+h, C, COL['cut'])
    sc.box(x0+5, x0+w-5, y0+l-5, y0+l, z0+fl, z0+h, C, COL['cut'])
    sc.box(x0+5, x0+w-5, y0+5, y0+l-5, z0+fl, z0+fl+B.FELT, F)        # ni
    if not tiles: return
    tw, tl, th = B.TILE_MAX[1], B.TILE_MAX[0], B.TILE_MAX[2]
    bx = x0 + 5 + (B.TRAY_IN[1] - 3*tw)/2
    by = y0 + 5 + 1.0
    for r in range(3):
        for c in range(12):
            X = bx + r*tw; Y = by + c*(tl + 0.418)
            sc.box(X+0.4, X+tw-0.4, Y, Y+tl, z0+fl+B.FELT, z0+fl+B.FELT+th,
                   COL['tile'], COL['tile_e'])

def add_ac(sc, tiles=True, cover=False):
    C = COL['ac'] if 'ac' in COL else COL['tray']
    x0 = X_AC[0] + 1; w = S['AC_W_OUT']; y0 = FB + B.AC_CLR; l = S['AC_L']
    z0, h = Z_FL, B.AC_H
    xi0, xi1 = x0 + B.AC_WALL, x0 + w - B.AC_WALL
    sc.box(x0, x0+w, y0, y0+l, z0, z0+h - B.AC_JOKER[2], C, COL['cut'])   # khoi day
    # vach bao quanh
    sc.box(x0, xi0, y0, y0+l, z0, z0+h, C, COL['cut'])
    sc.box(xi1, x0+w, y0, y0+l, z0, z0+h, C, COL['cut'])
    sc.box(xi0, xi1, y0, y0+B.AC_WALL, z0, z0+h, C, COL['cut'])
    sc.box(xi0, xi1, y0+l-B.AC_WALL, y0+l, z0, z0+h, C, COL['cut'])
    zt = z0 + h
    # ranh Joker: hai dai go hai ben
    jy0 = y0 + B.AC_WALL; jy1 = jy0 + B.AC_JOKER[1]
    jx0, jx1 = XS - B.AC_JOKER[0]/2, XS + B.AC_JOKER[0]/2
    for a, b in [(xi0, jx0), (jx1, xi1)]:
        sc.box(a, b, jy0, jy1, zt - B.AC_JOKER[2], zt, C, COL['cut'])
    sc.box(jx0, jx1, jy0, jy1, zt-B.AC_JOKER[2], zt-B.AC_JOKER[2]+B.FELT, COL['felt'])
    if tiles:   # 8 quan Joker, 2 lop x 4
        tl_, tw_, th_ = B.TILE_MAX[1], B.TILE_MAX[0], B.TILE_MAX[2]
        for lay in range(2):
            for c in range(4):
                Y = jy0 + 2 + c*(tl_ + 0.6)
                sc.box(XS-tw_/2, XS+tw_/2, Y, Y+tl_,
                       zt-B.AC_JOKER[2]+B.FELT+lay*(th_+0.4),
                       zt-B.AC_JOKER[2]+B.FELT+lay*(th_+0.4)+th_, COL['tile'], COL['tile_e'])
    # --- o xuc xac (to AC-02). Ba cao do: san dat nap che, khe luon ngon, o.
    # Dung box_spec.dice_layout() de hinh 3D, to AC-01/AC-02 va hinh BX-01 khong
    # bao gio lech nhau. He (u,w) cua o: u chay theo Y, w chay theo X.
    dy0 = jy1 + B.AC_WALL; dy1 = dy0 + S['AC_DICE_L']
    DL = B.dice_layout(S)
    U = lambda u: dy0 + u
    Wx = lambda w: xi0 + w
    z_flr = zt - DL['sock_d']                 # san o (cao do thap nhat)
    z_rec = zt - B.COVER_T                    # san dat nap che
    z_slt = zt - DL['slot_d']                 # san khe luon ngon
    # tam go duoi day o
    sc.box(xi0, xi1, dy0, dy1, zt - B.AC_JOKER[2], z_flr, C, COL['cut'])
    mw, ml = S['DICE_MARG_W'], S['DICE_MARG_L']
    # hai dai go doc hai ben (w) — nguyen khoi tu san o len san dat nap
    sc.box(xi0, Wx(mw), dy0, dy1, z_flr, z_rec, C, COL['cut'])
    sc.box(Wx(S['AC_W_IN'] - mw), xi1, dy0, dy1, z_flr, z_rec, C, COL['cut'])
    # vach giua hai cot o
    w_mid0 = S['DICE_W'][0] + B.DICE_SOCK
    sc.box(Wx(w_mid0), Wx(w_mid0 + B.DICE_RIB), dy0, dy1, z_flr, z_rec, C, COL['cut'])
    for w0 in S['DICE_W']:                    # trong moi cot o
        a, b = Wx(w0), Wx(w0 + B.DICE_SOCK)
        sc.box(a, b, dy0, U(ml), z_flr, z_rec, C, COL['cut'])                 # vanh dau
        sc.box(a, b, U(S['AC_DICE_L'] - ml), dy1, z_flr, z_rec, C, COL['cut'])# vanh cuoi
        u_mid = S['DICE_U'][0] + B.DICE_SOCK
        sc.box(a, b, U(u_mid), U(u_mid + B.DICE_RIB), z_flr, z_rec, C, COL['cut'])
        for su, su1, _, _ in [x for x in DL['slots'] if abs(x[2] - w0) < 1e-9]:
            sc.box(a, b, U(su), U(su1), z_flr, z_slt, C, COL['cut'])          # bac khe
    if tiles:                                  # 4 quan xuc xac nam trong o
        for u0, u1, w0, w1 in DL['socks']:
            c_u, c_w = (u0+u1)/2, (w0+w1)/2
            sc.box(Wx(c_w - B.DIE/2), Wx(c_w + B.DIE/2), U(c_u - B.DIE/2), U(c_u + B.DIE/2),
                   z_flr, z_flr + B.DIE, COL['tile'], COL['tile_e'])
    # hoc 4 quan du phong
    ay0 = dy1 + B.AC_WALL; ay1 = ay0 + B.AC_AUX_L
    sc.box(xi0, xi1, ay0, ay1, zt-B.AC_AUX_D, zt-B.AC_AUX_D+B.FELT, COL['felt'])
    if tiles:
        tl_, tw_, th_ = B.TILE_MAX[1], B.TILE_MAX[0], B.TILE_MAX[2]
        for i in range(2):
            for j in range(2):
                sc.box(XS-tw_-0.5+i*(tw_+1), XS-tw_-0.5+i*(tw_+1)+tw_,
                       ay0+3+j*(tl_+1), ay0+3+j*(tl_+1)+tl_,
                       zt-B.AC_AUX_D+B.FELT, zt-B.AC_AUX_D+B.FELT+th_,
                       COL['tile'], COL['tile_e'])
    # --- nap che o xuc xac. MAC DINH KHONG ve: no che het bon o, hinh noi that
    # se khong con gi de xem. Bat cover=True cho hinh 12g.
    if cover:
        cu0, cu1 = B.COVER_CLR/2, S['AC_DICE_L'] - B.COVER_CLR/2
        cw0, cw1 = B.COVER_CLR/2, S['AC_W_IN'] - B.COVER_CLR/2
        r = B.COVER_NOTCH/2
        wc = S['COVER_NOTCH_W']                    # tam hai hom, he toa do cua hoc
        CV, CVC = COL['cov'], COL['cov_c']
        sc.box(Wx(cw0), Wx(cw1), U(cu0 + r), U(cu1), z_rec, zt, CV, CVC)
        # dai mang hom ngon: cat lat theo u, moi lat mot be rong khac nhau ->
        # nua tron thanh bac thang 0,75 mm, du min o ti le hinh nay.
        n = 12
        for i in range(n):
            ua, ub = cu0 + r*i/n, cu0 + r*(i+1)/n
            dmid = (ua + ub)/2 - cu0
            hw = math.sqrt(max(0.0, r*r - dmid*dmid))
            edges = [cw0]
            for c_ in wc:
                edges += [c_ - hw, c_ + hw]
            edges.append(cw1)
            for wa, wb in zip(edges[0::2], edges[1::2]):
                if wb - wa < 1e-6: continue
                sc.box(Wx(wa), Wx(wb), U(ua), U(ub), z_rec, zt, CV, CVC)
    return (xi0, xi1, dy0, dy1)

def leaf_polys(th, right):
    """Tra ve (do doc mong, do doc khe, do ngang, tam Nu) — da giac XZ + khoang Y."""
    def m(p): return (W - p[0], p[1]) if right else p
    def r(p):
        c = (W - PIN[0], PIN[1]) if right else PIN
        return rot_xz(m(p), c, -th if right else th)
    st, RR = B.STILE, RK
    x0 = LX0                      # mep ngoai canh nap — lui vao PIN_X o ho C
    x1 = LX0 + LW                 # mep khe rap giua
    def arc(a0, a1, n=8):        # goc ngoai duoi cua nap, ong go chiem cho, tam tai truc
        return [(PXX + RR*math.cos(math.radians(a0 + (a1-a0)*i/n)),
                 Z_RIM + RR*math.sin(math.radians(a0 + (a1-a0)*i/n))) for i in range(n+1)]
    out = []
    # do doc ban le
    out.append(([r(p) for p in [(x0, Z_RIM+RR)] + arc(90, 0)
                 + [(x0+st, Z_RIM), (x0+st, Z_LID), (x0, Z_LID)]], 0.0, B.LID_L, 'coco'))
    # do doc khe giua
    out.append(([r((x1-st, Z_RIM)), r((x1, Z_RIM)), r((x1, Z_LID)), r((x1-st, Z_LID))],
                0.0, B.LID_L, 'coco'))
    for y0, y1 in [(0.0, B.RAIL), (B.LID_L-B.RAIL, B.LID_L)]:
        out.append(([r((x0+st, Z_RIM)), r((x1-st, Z_RIM)), r((x1-st, Z_LID)), r((x0+st, Z_LID))],
                    y0, y1, 'coco'))
    # tam Nu NANG: mat tren ngang bang mat khung (Z_LID), long tam thut vao
    # PAN_REV moi phia de con cho cho go no.
    zp0 = Z_LID - S['PAN_TH']; rv = B.PAN_REV
    out.append(([r((x0+st+rv, zp0)), r((x1-st-rv, zp0)),
                 r((x1-st-rv, Z_LID)), r((x0+st+rv, Z_LID))],
                B.RAIL + rv, B.LID_L - B.RAIL - rv, 'burl'))
    return out

def add_lid(sc, th=0.0, leaves=(True, True), show_mag=True, felt=False):
    for right in (False, True):
        if not leaves[1 if right else 0]: continue
        for poly, y0, y1, ck in leaf_polys(th, right):
            sc.prism_y(poly, y0, y1, COL[ck], COL['cut'])
        # mat mong go ben NAP — ong go quay theo canh
        c = (W - PIN[0], PIN[1]) if right else PIN
        for y0, is_body in KN:
            if is_body: continue
            sc.prism_y(circle_xz(c[0], c[1], RK), y0, y0 + B.KN_LEN,
                       COL['coco'], COL['cut'])
        # dem ni duoi nap: MIENG ROI, khong phai tam trai kin. Trai kin thi luc nen
        # ni vuot luc hut nam cham va nap khong dong duoc — xem box_spec muc DEM NI.
        if abs(th) < 1e-9 and felt:
            pw, pl = B.FELT_PAD_SZ
            for xc in B.FELT_PAD_X:
                if (xc < XS) != (not right): continue
                for yc in B.FELT_PAD_Y:
                    # ve o trang thai DA NEN: ni day B.FELT_PAD tu do, lap vao thi
                    # bi ep xuong dung khe B.CLR_Z. Ve be day tu do se dam vao vanh
                    # khay va hinh thanh vo nghia.
                    sc.box(xc - pw/2, xc + pw/2, yc - pl/2, yc + pl/2,
                           Z_RIM - B.CLR_Z, Z_RIM, COL['felt'])
        # nam cham duoi nap
        if abs(th) < 1e-9 and show_mag:
            for xc in (B.MAG_X if not right else [W-x for x in B.MAG_X]):
                for yc in (B.MAG_Y, YB-B.MAG_Y):
                    zr = z_rim(xc)
                    sc.box(xc-B.MAG[0]/2, xc+B.MAG[0]/2, yc-B.MAG[1]/2, yc+B.MAG[1]/2,
                           zr+0.1, zr+B.MAG_REC, COL['mag'])

# --------------------------------------------------------------- ve
def _wrap(txt, budget):
    """Cat chu thanh nhieu dong theo so ky tu — de phu de khong tran ra ngoai."""
    out, line = [], ''
    for word in txt.split():
        if line and len(line) + 1 + len(word) > budget:
            out.append(line); line = word
        else:
            line = (line + ' ' + word) if line else word
    if line: out.append(line)
    return out

def render(sc, eye, target, w, h, title, sub_, zoom=1.0, fit=None, pan=(0.0, 0.0)):
    """Chieu phoi canh + KHUNG HINH TU DONG.

    Truoc day moi hinh phai chinh tay mot tri so `focal`, va vi the hinh nao
    cung thua mot mang trong o duoi. Nay chieu hai luot: luot dau lay toa do
    chuan hoa de biet vat the chiem cho nao, luot sau chon he so phong sao cho
    no vua khit khung con lai duoi dai tieu de. `fit` cho phep dong khung theo
    MOT KHOI quan tam thay vi ca canh — dung cho hinh can nhin.
    """
    ex, ey, ez = eye
    f = norm(sub(target, eye))
    r = norm(cross(f, (0, 0, 1)))
    u = cross(r, f)

    def proj(p):
        d = sub(p, eye)
        zc = dot(d, f)
        if zc < 1.0: return None
        return (dot(d, r)/zc, -dot(d, u)/zc, zc)

    # ---- luot 1: toa do chuan hoa
    prepped = []
    for verts, col, mask in sc.faces:
        q = [proj(p) for p in verts]
        if any(t is None for t in q) or len(q) < 3: continue
        n = norm(cross(sub(verts[1], verts[0]), sub(verts[2], verts[0])))
        if dot(n, sub(eye, verts[0])) < 0: n = (-n[0], -n[1], -n[2])
        sh = 0.34 + 0.66*max(0.0, dot(n, LIGHT))
        prepped.append((sum(t[2] for t in q)/len(q), q, col, sh, mask))
    if not prepped:
        raise SystemExit('khong con mat nao trong khung nhin')

    # ---- khung hinh
    if fit is None:
        pts = [(t[0], t[1]) for _, q, _, _, _ in prepped for t in q]
    else:
        x0, x1, y0, y1, z0, z1 = fit
        pts = []
        for X in (x0, x1):
            for Y in (y0, y1):
                for Z in (z0, z1):
                    t = proj((X, Y, Z))
                    if t: pts.append((t[0], t[1]))
    bx0 = min(p[0] for p in pts); bx1 = max(p[0] for p in pts)
    by0 = min(p[1] for p in pts); by1 = max(p[1] for p in pts)
    hdr = 44 + 16*len(_wrap(sub_, int((w - 48)/5.35)))
    M = 16.0
    focal = min((w - 2*M)/max(bx1 - bx0, 1e-6),
                (h - hdr - 2*M)/max(by1 - by0, 1e-6))*zoom
    ox = w/2 - focal*(bx0 + bx1)/2 + pan[0]*w
    oy = hdr + (h - hdr)/2 - focal*(by0 + by1)/2 + pan[1]*h

    out = []
    for zc, q, col, sh, mask in prepped:
        pts_s = [(ox + focal*t[0], oy + focal*t[1]) for t in q]
        c = '#%02x%02x%02x' % tuple(min(255, int(v*sh)) for v in col)
        k = '#%02x%02x%02x' % tuple(min(255, int(v*sh*0.58)) for v in col)
        out.append((zc, pts_s, c, k, mask))
    out.sort(key=lambda t: -t[0])

    body = [f'<rect width="100%" height="100%" fill="#f7f5f1"/>']
    for _, pts_s, c, k, mask in out:
        d = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts_s)
        # vien trung mau nen de khong lo duong chia o
        body.append(f'<polygon points="{d}" fill="{c}" stroke="{c}" stroke-width="0.7"/>')
        if mask:
            n = len(pts_s)
            seg = []
            for i in range(n):
                if mask & (1 << i):
                    a, b = pts_s[i], pts_s[(i+1) % n]
                    if abs(a[0]-b[0]) + abs(a[1]-b[1]) < 1.6: continue
                    seg.append(f'M {a[0]:.1f},{a[1]:.1f} L {b[0]:.1f},{b[1]:.1f}')
            if seg:
                body.append(f'<path d="{" ".join(seg)}" fill="none" stroke="{k}" '
                            f'stroke-width="0.55" stroke-linecap="round"/>')
    body.append(f'<rect x="0" y="0" width="{w}" height="{hdr - 8}" fill="#f7f5f1" '
                f'fill-opacity="0.94"/>')
    body.append(f'<text x="24" y="30" font-size="15" font-weight="bold" '
                f'font-family="DejaVu Sans" fill="#1a1a1a">{title}</text>')
    for i, ln in enumerate(_wrap(sub_, int((w - 48)/5.35))):
        body.append(f'<text x="24" y="{48 + i*15}" font-size="10.5" '
                    f'font-family="DejaVu Sans" fill="#55524b">{ln}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">' + ''.join(body) + '</svg>')

os.makedirs('figs', exist_ok=True)
CX, CY, CZ = W/2, YB/2, 30
def shot(name, title, sub_, build, eye, target=None, w=1000, h=620,
         zoom=1.0, fit=None, pan=(0.0, 0.0)):
    sc = Scene()
    build(sc)
    open(f'figs/{name}.svg', 'w').write(
        render(sc, eye, target or (CX, CY, CZ), w, h, title, sub_,
               zoom=zoom, fit=fit, pan=pan))
    print(f'  {name}  ({len(sc.faces)} mat)')

# 1 — tong the, nap dong
def v1(sc): add_body(sc, show_mag=False); add_lid(sc, show_mag=False)
shot('fig12a-tong-the-nap-dong', 'HÌNH 12a — Tổng thể, nắp đóng',
     f'{S["X_OA"]:.1f} × {S["Y_OA"]:.0f} × {S["Z_OA"]:.0f} mm · {B.mass_of(S,"loi on dinh")[2]:.2f} kg. '
     f'Bản lề mắt mộng gỗ Ø{2*RK:.1f}, trục trên arris, nhô ra {S["PROUD"]:.1f} mm mỗi bên — '
     f'không hạ bậc, không một chi tiết kim loại. Hốc âm hai tay khe hở {S["GRIP_APER"]:.1f} × '
     f'sâu {B.GRIP_D:.0f}. Tấm Nu ngang bằng mặt khung.',
     v1, eye=(-250, -430, 260), target=(CX, CY, 22))

# 2 — nap mo 180 do
def v2(sc):
    add_body(sc)
    for x0, y0 in [(X_BAY[0][0]+1, FB+B.AC_CLR), (X_BAY[1][0]+1, FB+B.AC_CLR)]:
        for k in (0, 1):
            add_tray(sc, x0, y0, Z_FL + k*B.TRAY_H + 0.02, tiles=(k == 1))
    add_ac(sc)
    add_lid(sc, math.pi)
shot('fig12b-nap-mo-180', 'HÌNH 12b — Nắp mở 180°',
     f'Hai cánh nằm ngang, mặt trên phẳng đúng cao độ vành thân Z{Z_RIM:.0f}, vươn ra {LW:.0f} mm mỗi bên. '
     f'Lòng lõm của khung nắp chính là khay bỏ bài.',
     v2, eye=(-90, -600, 430), target=(CX, CY, 18), w=1180, h=620)

# 3 — noi that nhin tu tren
def v3(sc):
    add_body(sc)
    for x0 in (X_BAY[0][0]+1, X_BAY[1][0]+1):
        for k in (0, 1):
            add_tray(sc, x0, FB+B.AC_CLR, Z_FL + k*B.TRAY_H + 0.02, tiles=(k == 1))
    add_ac(sc)
shot('fig12c-noi-that', 'HÌNH 12c — Lòng hộp, tháo nắp',
     f'4 khay quân 3 × 12 (2 chồng mỗi khoang) + AC-01: rãnh Joker 8 quân, '
     f'4 ổ xúc xắc {B.DICE_SOCK:.0f} × {B.DICE_SOCK:.0f} (nắp che tháo ra), '
     f'hốc 4 quân dự phòng.',
     v3, eye=(-70, -360, 520), target=(CX, CY, 20))

# 4 — mat cat doc
def v4(sc):
    sc.clip_y = (140.0, YB+GO+1)
    add_body(sc)
    for x0 in (X_BAY[0][0]+1, X_BAY[1][0]+1):
        for k in (0, 1):
            add_tray(sc, x0, FB+B.AC_CLR, Z_FL + k*B.TRAY_H + 0.02, tiles=True)
    add_ac(sc)
    add_lid(sc)
shot('fig12d-mat-cat', 'HÌNH 12d — Cắt dọc giữa hộp',
     f'Cắt tại Y = 140. Chuỗi Z: chân {B.FOOT:.0f} + đáy {B.BOT:.0f} + 2 × khay {B.TRAY_H:.0f} '
     f'+ khe {B.CLR_Z:.0f} = vành Z{Z_RIM:.0f}; nắp dày {B.T_LID:.0f} đều → Z{Z_LID:.0f}. '
     f'Mặt cắt tô sáng.',
     v4, eye=(-150, -520, 215), target=(CX, 215, 28))

# 5 — chi tiet goc: ban le + hoc am
def v5(sc):
    sc.clip_y = (-1.0, 260.0)
    add_body(sc)
    for k in (0, 1):
        add_tray(sc, X_BAY[0][0]+1, FB+B.AC_CLR, Z_FL + k*B.TRAY_H + 0.02, tiles=(k == 1))
    add_lid(sc, math.radians(50), leaves=(True, False))
    add_lid(sc, 0.0, leaves=(False, True))
shot('fig12e-chi-tiet-goc', 'HÌNH 12e — Vách trái: hốc âm hai tay và bản lề',
     f'Hốc âm {B.GRIP_W:.0f} rộng, khe hở vào tay {S["GRIP_APER"]:.1f}, sâu {B.GRIP_D:.0f} trong vách '
     f'{S["WALL_GRIP"]:.0f}; dải gỗ trên hốc {S["GRIP_LEDGE"]:.1f} cao × {S["GRIP_LEDGE_T"]:.0f} dày '
     f'(dày hết bề dày vách). {B.N_KN} mắt mộng gỗ Ø{2*RK:.1f} trên arris.',
     v5, eye=(-470, -330, 205), target=(60, 150, 26),
     fit=(-S['PROUD'] - 8, 96.0, 12.0, 250.0, 0.0, Z_RIM + 20))

# 6 — CAT NGANG QUA HOC AM: cho thay dung cai "phan bau ngon tay"
def v6(sc):
    sc.clip_y = (YB/2, YB + 1)
    add_body(sc, show_mag=False)
    add_lid(sc, 0.0, show_mag=False)
shot('fig12f-hoc-am-cat', 'HÌNH 12f — Cắt ngang hốc âm: phần bấu ngón tay',
     f'Cắt tại Y{YB/2:.0f}, giữa hốc. Trần hốc KHÔNG phẳng: bo R{B.GRIP_R:.0f} ở mép ngoài rồi '
     f'dốc lên {B.GRIP_SLOPE:.0f}° vào trong, kết thúc ở Z{S["GRIP_Z_IN"]:.1f}. '
     f'Khe hở vào tay {S["GRIP_APER"]:.1f} mm; bề mặt trần {S["GRIP_SURF"]:.1f} mm > đốt ngón {B.L_DISTAL:.0f}.',
     v6, eye=(-95, -330, 118), target=(46, YB/2, 24), w=1000, h=560,
     fit=(-S['PROUD'] - 10, 150.0, YB/2, YB, 0.0, Z_LID))

# 7 — AC-01 CO NAP CHE DAY VAO: rang buoc chieu cao chat nhat cua khay
AC_DY0 = B.WALL_FB + B.AC_CLR + B.AC_WALL + B.AC_JOKER[1] + B.AC_WALL
Y_CUT  = AC_DY0 + S['DICE_U'][0] + B.DICE_SOCK/2      # cat qua TAM mot hang o
def v7(sc):
    sc.clip_y = (Y_CUT, Y_CUT + 62)      # lat cat day 62 mm, khong keo ca hop ra sau
    add_body(sc, show_mag=False)
    for x0 in (X_BAY[0][0]+1, X_BAY[1][0]+1):
        for k in (0, 1):
            add_tray(sc, x0, B.WALL_FB + B.AC_CLR, Z_FL + k*B.TRAY_H + 0.02, tiles=True)
    add_ac(sc, cover=True)
    add_lid(sc, 0.0, show_mag=False, felt=True)
shot('fig12g-nap-che-xuc-xac', 'HÌNH 12g — Nắp che ổ xúc xắc đậy vào, cắt qua tâm ổ',
     f'Cắt tại Y{Y_CUT:.0f}. Nắp che dày {B.COVER_T:.0f} nằm trong sàn phay sâu {B.COVER_T:.0f}, '
     f'mặt trên NGANG BẰNG vành AC-01 (Z{Z_FL+B.AC_H:.0f}). Dưới nắp: xúc xắc {B.DIE:.0f} hở '
     f'{S["DIE_HEAD"]:.0f} mm; ổ sâu {B.DICE_SOCK_D:.0f} kể từ sàn nắp = {Z_FL+B.AC_H-B.dice_layout(S)["sock_d"]:.0f} '
     f'tính từ đáy. Trên nắp che: khe {S["AC_GAP"]:.0f} mm tới vành thân Z{Z_RIM:.0f}, '
     f'trong đó nỉ đệm dày {B.FELT_PAD:.1f} tự do, lắp vào bị NÉN xuống {B.CLR_Z:.1f} — '
     f'{S["FELT_PRELOAD"]:.1f} mm nén đó là thứ ép khay và nắp che xuống. Nỉ là {S["FELT_PAD_N"]:.0f} miếng rời '
     f'{B.FELT_PAD_SZ[0]:.0f} × {B.FELT_PAD_SZ[1]:.0f}, KHÔNG trải kín: trải kín thì lực nén vượt lực hút nam châm.',
     v7, eye=(XS - 210, Y_CUT - 330, 122), target=(XS, Y_CUT + 20, 30), w=1000, h=620,
     fit=(X_AC[0] - 34, X_AC[1] + 34, Y_CUT, Y_CUT + 62, 0.0, Z_LID), zoom=0.93)
