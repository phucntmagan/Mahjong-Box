#!/usr/bin/env python3
"""
TRAN HOC AM — "phan bau ngon tay". Chay: python3 tools/grip_hook.py

Rev C2: ha bac ban le (ho C) lay het go o x < REBATE_D tu Z(Z_RIM - T_LID) len
vanh. Hoc am nam DUNG tren vach do, nen tran hoc bi khoa xuong Z28 va ban kinh
bo mep chi con R4.

Rev C3: BO ha bac (ve ho B). Vach ban le lien khoi tu san toi vanh. Cao do tran
hoc thoi lay tu chan tren cua vach — no duoc suy tu CHINH BAN TAY, con vach du
go hay khong la mot cau hoi RIENG, kiem doc lap.

Moi tri so lay tu box_spec.derive(). Khong go cung so nao trong file nay.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B
def hr(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

S = B.derive()
Z_RIM, Z_FL = S['Z_RIM'], S['Z_FLOOR']
RB_D, RB_H, RK = S['REBATE_D'], S['REBATE_H'], S['R_KN']
GD, GW, WG = B.GRIP_D, B.GRIP_W, S['WALL_GRIP']
m = B.mass_of(S, 'loi on dinh')[2]
P_hand = m*9.81*B.DYN/2

# ==========================================================================
hr("1. CAI GI NAM TREN DAU HOC AM")
print(f"  Vach ban le day {WG:.0f}, cao tu san Z{Z_FL:.0f} toi vanh Z{Z_RIM:.0f}.")
print(f"  Hoc am an sau {GD:.0f} tu mat ngoai. Cai gi chiem cho o phia tren?\n")
print(f"  {'ho ban le':>10s}{'ha bac':>16s}{'hom mat mong nap':>19s}"
      f"{'tran hoc cao nhat':>20s}")
for mode in ('C', 'B'):
    d = B.derive_mode(mode)
    lim = min(d['grip_top'](GD*i/64) for i in range(65))
    print(f"  {mode:>10s}{d['REBATE_D']:8.1f} x{d['REBATE_H']:5.0f}"
          f"{'Z' + format(Z_RIM - d['R_KN'], '.1f'):>19s}{'Z' + format(lim, '.1f'):>20s}"
          + ("   <- DANG CHOT" if mode == B.HG_MODE else ""))
print()
_C = B.derive_mode('C')
_R0 = B.GRIP_R
def _rmax(mode):
    """Ban kinh bo mep lon nhat con dung duoc o mot ho ban le."""
    best = None
    for i in range(20, 141):
        B.GRIP_R = i/10
        d = B.derive_mode(mode)
        if d['GRIP_FLAT'] >= 3.0 and d['GRIP_LIP_MIN'] >= B.GRIP_LIP_REQ: best = B.GRIP_R
    B.GRIP_R = _R0
    return best
print(f"  Ho C: ha bac {_C['REBATE_D']:.1f} x {_C['REBATE_H']:.0f} chay SUOT chieu dai vach,")
print(f"        lay het go o dai ngoai cung tu Z{Z_RIM-_C['REBATE_H']:.0f} len vanh. O R"
      f"{B.GRIP_R:.0f} thi go dac con lai tren tran chi")
print(f"        {_C['GRIP_LIP_MIN']:.2f} mm — tu kiem no. Ban kinh bo mep lon nhat ho C"
      f" chiu duoc: R{_rmax('C'):.1f}.")
print(f"  Ho B: khong ha bac. Thu duy nhat con nam tren dau vach la HOM cua mat")
print(f"        mong NAP: mot phan tu dia ban kinh {RK:.1f} khoet vao goc tren-ngoai,")
print(f"        tuc go chi mat tu Z{Z_RIM-RK:.1f} tro len, va chi o {RK:.1f} mm ngoai cung.")
print(f"        Ban kinh bo mep lon nhat ho B chiu duoc: R{_rmax('B'):.1f}.")
print(f"\n  => Bo ha bac tra lai {_C['REBATE_H']-RK:.1f} mm chieu cao vach cho hoc am,")
print(f"     va noi rong cua so ban kinh bo mep tu R{_rmax('C'):.1f} len R{_rmax('B'):.1f}.")

# ==========================================================================
hr("2. LOI DA CO — giu lai lam ho so")
# hai so LICH SU cua ban Rev C1/C2, giu de doi chieu:
OLD_H  = 28.0                                # chieu cao hoc tu chon luc do
OLD_RB = (6.0 + B.KN_FIT)/2 + 3.0            # R ong go luc do: chot O6 + thanh 3,0
print(f"  Rev C1 de tran hoc PHANG o Z{Z_FL+OLD_H:.0f} (= san {Z_FL:.0f} + cao hoc {OLD_H:.0f}")
print(f"  — mot so TU CHON). Z{Z_FL+OLD_H:.0f} nam trong dai ha bac"
      f" Z{Z_RIM-B.T_LID:.0f}..{Z_RIM:.0f}, nen o")
print(f"  {OLD_RB:.1f} mm ngoai cung khong con go ngay tren tran: doan moc duoc chi con")
print(f"  {GD-OLD_RB:.1f} mm thay vi {GD:.0f} — {(GD-OLD_RB)/B.L_DISTAL*100:.0f} % dot ngon,"
      f" te hon ca hoc sau 12 da bi loai.\n")
print(f"  Tu kiem luc do viet:  GRIP_Z1 > Z_RIM - REBATE_H  VA  REBATE_D > GRIP_D")
print(f"  Ve sau la {OLD_RB:.1f} > {GD:.0f} — luon SAI, nen ca menh de khong bao gio no.")
print(f"  Mot dieu kien VA co mot ve luon sai la mot cai luoi trang tri.\n")
print(f"  Kiem moi khong so hai so nua: no quet TUNG DIEM tren tran, o moi x doi")
print(f"  hoi con >= {B.GRIP_LIP_REQ:.1f} mm go dac ben tren (GRIP_LIP_MIN). Rev C3 bo ha")
print(f"  bac roi nhung kiem do VAN GIU — chinh no la thu chung minh tran moi thoat:")
print(f"  go dac mong nhat tren tran nay = {S['GRIP_LIP_MIN']:.1f} mm.")

# ==========================================================================
hr("3. CAO DO TRAN — suy tu ngon tay, khong tu vach")
print(f"  Rev C2 lay tran = day ha bac tru san go. Do la mot su TINH CO: ha bac")
print(f"  bien mat thi tri so do vo nghia. Nay tran duoc dinh nghia lai:")
print(f"      nang tran vua du de khe hep nhat giua LUNG ngon tay va SAN hoc")
print(f"      bang dung FING_MAR = {B.FING_MAR:.1f} mm.")
print(f"  Roi hoi rieng: vach con du go tren tran khong? (muc 2 — con"
      f" {S['GRIP_LIP_MIN']:.1f} mm.)\n")
print(f"  Ket qua: dinh ao tran Z{S['GRIP_Z1']:.2f}, dinh bo tron Z{S['GRIP_Z_TOP']:.2f},")
print(f"  khe ho vao tay {S['GRIP_APER']:.2f} mm (Rev C2 la 20,0).")

hr("3b. BAN KINH BO MEP — nay bi chan hai dau, va cua so rong ra")
print(f"  {'R':>6s}{'khe ho vao tay':>17s}{'tran phang con':>16s}{'be mat tran':>13s}"
      f"{'go dac tren tran':>18s}")
R0 = B.GRIP_R
best_hi = None
for i in range(20, 141):
    B.GRIP_R = i/10
    d = B.derive()
    if d['GRIP_FLAT'] >= 3.0 and d['GRIP_LIP_MIN'] >= B.GRIP_LIP_REQ: best_hi = B.GRIP_R
    if i % 20 == 0 or abs(i/10 - R0) < 1e-9:
        print(f"  {B.GRIP_R:6.1f}{d['GRIP_APER']:17.2f}{d['GRIP_FLAT']:16.2f}"
              f"{d['GRIP_SURF']:13.2f}{d['GRIP_LIP_MIN']:18.2f}"
              + ("   <- CHOT" if abs(i/10 - R0) < 1e-9 else ""))
B.GRIP_R = R0
print(f"\n  Chan TREN: doan tran phang phai con >= 3,0 mm -> R <= {best_hi:.1f}.")
print(f"  (Rev C2 chan tren la 4,30 vi khe ho bi ha bac khoa o 20 mm. Nay khong con.)\n")
rmin_hard = P_hand/(B.N_FING*B.FING_W*math.radians(B.WRAP_SKIN)*B.P_COMFORT)
rmin_soft = P_hand/(B.N_FING*B.FING_W*math.radians(B.WRAP_SKIN)*B.P_TARGET)
print(f"  Chan DUOI la ap luc. Luc bao gio cung bat dau don ve mep bo; da dau ngon")
print(f"  boc quanh mep chung {B.WRAP_SKIN:.0f}°, dai cham rong R x"
      f" {math.radians(B.WRAP_SKIN):.3f}. Voi {P_hand:.0f} N moi tay,")
print(f"  {B.N_FING} ngon x {B.FING_W:.0f} rong:")
print(f"      khong DAU   (<= {B.P_COMFORT*1000:.0f} kPa) -> R >= {rmin_hard:.2f}")
print(f"      xach LAU du (<= {B.P_TARGET*1000:.0f} kPa) -> R >= {rmin_soft:.2f}\n")
print(f"  {'R':>6s}{'ap luc luc bat luc':>21s}   ket qua")
for r in (3.0, 4.0, 6.0, 7.0, 8.0, 10.0, 12.0):
    pr = P_hand/(B.N_FING*B.FING_W*r*math.radians(B.WRAP_SKIN))*1000
    ok = ('DAU' if r < rmin_hard else 'chiu duoc, chua em' if r < rmin_soft else
          'tran phang con < 3' if r > best_hi else 'DUOC')
    print(f"  {r:6.1f}{pr:18.0f} kPa   {ok}")
CUTTERS = (3.0, 4.0, 5.0, 6.0, 8.0, 10.0)
win = [c for c in CUTTERS if rmin_soft <= c <= best_hi]
print(f"\n  Cua so theo muc tieu {B.P_TARGET*1000:.0f} kPa: {rmin_soft:.2f} .. {best_hi:.1f} mm.")
print(f"  Dao bo canh co san (mm): {', '.join(f'{c:.0f}' for c in CUTTERS)}"
      f" -> loi vao: {', '.join(f'R{c:.0f}' for c in win)}")
print(f"  Lay dao NHO NHAT loi vao cua so (bo cang to thi cang an vao tran phang):"
      f" R{min(win):.0f}.")
print(f"  Da chot GRIP_R = {B.GRIP_R:.1f}  "
      f"({'khop' if abs(min(win)-B.GRIP_R) < 1e-9 else 'LECH'}).")
print(f"\n  Ghi lai: Rev C2 phai lay R4 (343 kPa) vi ha bac khoa khe ho o 20 mm. Bo")
print(f"  ha bac di thi R8 vao duoc, ap luc luc bat luc con"
      f" {P_hand/(B.N_FING*B.FING_W*8.0*math.radians(B.WRAP_SKIN))*1000:.0f} kPa.")

# ==========================================================================
hr("4. DO DOC TRAN — chan tren la goc ma sat")
th = math.radians(B.GRIP_SLOPE)
print(f"  Tran doc len phia trong thi phan luc co thanh phan NGANG day ngon tay ra.")
print(f"  Ngon khong tuot chi khi  tan(doc) <= mu  (ma sat da tay / go danh bong).")
print(f"  mu tra bang = {B.MU_SKIN:.2f} (lay can duoi) -> doc toi da"
      f" {math.degrees(math.atan(B.MU_SKIN)):.1f}°.")
print(f"  Chot {B.GRIP_SLOPE:.0f}°: tan = {math.tan(th):.3f} / {B.MU_SKIN:.2f}"
      f" -> he so {B.MU_SKIN/math.tan(th):.2f}x.\n")
print(f"  Cai doc dung de lam gi: no nang tran len {GD*math.tan(th):.2f} mm o day hoc,")
print(f"  vua dung cho dau ngon tay gap lai ma van cham tran suot ca {B.L_DISTAL:.0f} mm.")

# ==========================================================================
hr("5. NGON TAY CO LOT HET CHIEU SAU KHONG")
print(f"  Ngon mau: day {B.FING_T_DIP:.0f} o khop DIP, {B.FING_T_TIP:.0f} o dau mut,")
print(f"  dot ngoai dai {B.L_DISTAL:.0f}, rong {B.FING_W:.0f}. Dat dau mut cham day hoc.\n")
print(f"  {'x (tu mat ngoai)':>18s}{'cao long hoc':>15s}{'day ngon tai do':>18s}{'khe lung':>11s}")
for i in range(9):
    x = GD*i/8
    c = S['grip_ceil'](x) - Z_FL
    t = S['fing_t'](x)
    print(f"  {x:18.1f}{c:15.2f}{t:18.2f}{c-t:11.2f}")
print(f"\n  Khe hep nhat {S['GRIP_FIT']:.2f} mm — bang dung FING_MAR vi tran duoc suy")
print(f"  tu chinh dieu kien nay (muc 3).")
print(f"\n  Nhay theo co ngon tay. Dat dau mut o do sau 'dep' roi hoi CA ngon co lot")
print(f"  khong; lay dep lon nhat con lot.")
print(f"  {'day ngon o DIP':>16s}{'dat dau mut sau':>17s}{'be mat cham':>13s}{'ghi chu':>26s}")
def max_depth(td, n=200):
    ok_dep = 0.0
    for k in range(n + 1):
        dep = GD*k/n
        good = True
        for i in range(n + 1):
            x = dep*i/n
            u = min(max(dep - x, 0.0), B.L_DISTAL)
            t = B.FING_T_TIP + (td - B.FING_T_TIP)*u/B.L_DISTAL
            if S['grip_ceil'](x) - Z_FL - t < 0.0: good = False; break
        if good: ok_dep = dep
    return ok_dep
for td in (14.0, 16.0, 17.5, 19.0):
    dep = max_depth(td)
    surf = min(dep + (S['GRIP_SURF'] - GD), S['GRIP_SURF']) if dep > 0 else 0.0
    note = ("ngon mau (nam, 50%)" if abs(td - B.FING_T_DIP) < 1e-9 else
            "nam 95%" if td == 17.5 else "ngon rat to" if td > 17.5 else "nu / ngon ut")
    print(f"  {td:16.1f}{dep:17.1f}{surf:13.1f}{note:>26s}")

# ==========================================================================
hr("6. AP LUC LEN DAU NGON TAY")
A_new = B.N_FING*B.FING_W*min(S['GRIP_SURF'], B.L_DISTAL)
EDGE_SHARP = 0.5
print(f"  Hop {m:.2f} kg, he so dong {B.DYN:.0f} -> {P_hand:.0f} N moi tay.")
print(f"  Ap luc phu thuoc BE RONG DAI CHAM, ma dai cham lai phu thuoc hinh tran.\n")
print(f"  {'tinh huong':>42s}{'dai cham':>11s}{'dien tich':>12s}{'ap luc':>11s}")
rows = [("canh vuong, ngon vua bat luc", EDGE_SHARP),
        (f"bo R4 (Rev C2), da boc {B.WRAP_SKIN:.0f}°", 4.0*math.radians(B.WRAP_SKIN)),
        (f"bo R{B.GRIP_R:.0f} (Rev C3), da boc {B.WRAP_SKIN:.0f}°",
         B.GRIP_R*math.radians(B.WRAP_SKIN)),
        ("tran phang sau 12, ngon cham 12 (Rev B)", min(12.0, B.L_DISTAL)),
        ("tran bo + doc, cham het dot ngon", min(S['GRIP_SURF'], B.L_DISTAL))]
for lbl, surf in rows:
    A = B.N_FING*B.FING_W*surf
    print(f"  {lbl:>42s}{surf:11.2f}{A:12.0f}{P_hand/A*1000:10.0f} kPa")
print(f"\n  Nguong: ~100 kPa em, ~200 kPa chiu duoc lau, >400 kPa dau trong mot phut.")
print(f"  Bo mep lo cho THOI DIEM XAU NHAT, do doc lo cho TRANG THAI ON DINH.")

# ==========================================================================
hr("7. DAI GO TREN HOC — kiem ben tren TIET DIEN THAT")
def sect(n=2000):
    dx = WG/n
    A = Az = 0.0; cells = []
    for i in range(n):
        x = (i + 0.5)*dx
        zhi = S['grip_top'](x)
        zlo = S['grip_ceil'](x) if x < GD else Z_FL
        if zhi <= zlo: continue
        a = (zhi - zlo)*dx; zc = (zhi + zlo)/2
        A += a; Az += a*zc; cells.append((a, zc, zhi - zlo))
    zc0 = Az/A
    I = sum(a*(zc - zc0)**2 + a*h*h/12 for a, zc, h in cells)
    return A, zc0, I
A_s, zc_s, I_s = sect()
c_max = max(Z_RIM - zc_s, zc_s - Z_FL)
M = P_hand*GW/8
sig = M*c_max/I_s
tau = 1.5*(P_hand/2)/A_s
dfl = P_hand*GW**3/(192*B.E_W*I_s)
print(f"  Dam nhip {GW:.0f} mm (be rong hoc), ngam hai dau vao vach hai ben hoc.")
print(f"  Tiet dien la chu L: dai go tren tran cong thanh sau hoc {B.GRIP_BACK:.0f} mm.")
print(f"  Ho B khong ha bac nen dai go tren tran day HET {S['GRIP_LEDGE_T']:.1f} mm"
      f" (ho C chi con 15,9).")
print(f"    Dien tich          A  = {A_s:8.1f} mm2")
print(f"    Trong tam          z  = Z{zc_s:7.2f}")
print(f"    Momen quan tinh    I  = {I_s:8.0f} mm4")
print(f"    Uon            sigma  = {sig:8.2f} MPa / MOR {B.MOR:.0f}   -> he so {B.MOR/sig:.0f}x")
print(f"    Cat              tau  = {tau:8.2f} MPa / {B.SHEAR:.0f}      -> he so {B.SHEAR/tau:.0f}x")
print(f"    Vong giua nhip        = {dfl:8.4f} mm")
b_r, h_r = S['GRIP_LEDGE_T'], S['GRIP_LEDGE']
I_r = b_r*h_r**3/12
sig_r = M*(h_r/2)/I_r
print(f"\n  Can duoi — chi lay dai go tren tran nhu chu nhat {h_r:.1f} x {b_r:.1f}:")
print(f"    I = {I_r:.0f} mm4 ({I_r/I_s*100:.0f} % tiet dien that),"
      f" sigma = {sig_r:.2f} MPa -> he so {B.MOR/sig_r:.0f}x")
print(f"  Ket cau khong phai rang buoc. Rang buoc van la BAN TAY.")

# ==========================================================================
hr("8. CHOT LAI")
for a, b_ in [("Khe ho vao tay (mat ngoai)", f"{S['GRIP_APER']:.2f} mm — suy tu ngon tay,"
                                             f" khong tu vach"),
              ("Sau hoc", f"{GD:.0f} mm (dot ngon {B.L_DISTAL:.0f} + ke {GD-B.L_DISTAL:.0f})"),
              ("Rong hoc", f"{GW:.0f} mm theo Y, Y {S['GRIP_Y0']:.0f}..{S['GRIP_Y1']:.0f}"),
              ("Bo mep ngoai tran", f"R{B.GRIP_R:.0f} — cua so {rmin_soft:.2f}..{best_hi:.1f},"
                                    f" dao co san loi vao: R{min(win):.0f}"),
              ("Doc tran", f"{B.GRIP_SLOPE:.0f}° len phia trong"
                           f" (chan tren goc ma sat {math.degrees(math.atan(B.MU_SKIN)):.1f}°)"),
              ("Cao do tran", f"Z{S['GRIP_Z_TOP']-B.GRIP_R:.2f} thap nhat (x={B.GRIP_R:.0f})"
                              f" -> Z{S['GRIP_Z_IN']:.2f} tai day hoc"),
              ("Go dac tren tran", f"mong nhat {S['GRIP_LIP_MIN']:.2f} mm"
                                   f" (yeu cau >= {B.GRIP_LIP_REQ:.1f})"),
              ("Be mat tran", f"{S['GRIP_SURF']:.2f} mm ({S['GRIP_ARC']:.2f} cung +"
                              f" {S['GRIP_FLAT']/math.cos(th):.2f} doc)"),
              ("Ap luc dau ngon", f"{P_hand/A_new*1000:.0f} kPa on dinh /"
                                  f" {P_hand/(B.N_FING*B.FING_W*B.GRIP_R*math.radians(B.WRAP_SKIN))*1000:.0f}"
                                  f" kPa luc bat luc"),
              ("Dai go tren hoc", f"cao {S['GRIP_LEDGE']:.2f} x day {S['GRIP_LEDGE_T']:.1f}"
                                  f" (day HET be day vach), he so uon {B.MOR/sig:.0f}x"),
              ("Vach ban le", f"{S['WALL_HINGE']:.0f} = sau hoc {GD:.0f} + thanh sau"
                              f" {B.GRIP_BACK:.0f}")]:
    print(f"  {a:28s}{b_}")
print(f"\n  Tu kiem box_spec: {B.selfcheck(S) or 'DAT'}")
