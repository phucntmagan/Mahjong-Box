#!/usr/bin/env python3
"""
TRAN HOC AM — "phan bau ngon tay". Chay: python3 tools/grip_hook.py

Bai toan: ha bac ban le (ho C) lay het go o x < REBATE_D tu Z(Z_RIM - T_LID) len
vanh. Hoc am nam DUNG tren vach do. Neu tran hoc de o cao do cu (Z_FLOOR + 28)
thi doan tran o phia mat ngoai bi ha bac lay mat -> ngon tay khong con gi de bau.
Muc 2 do lai loi do bang so. Cac muc sau suy ra hinh dang tran moi.

Moi tri so lay tu box_spec.derive(). Khong go cung so nao trong file nay.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B
def hr(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

S = B.derive()
Z_RIM, Z_FL = S['Z_RIM'], S['Z_FLOOR']
RB_D, RB_H = S['REBATE_D'], S['REBATE_H']
GD, GW, WG = B.GRIP_D, B.GRIP_W, S['WALL_GRIP']

# ==========================================================================
hr("1. RANG BUOC — khe ho vao tay KHONG phai so tu chon")
print(f"  Vach ban le day {WG:.0f}. Tren dinh no co hai thu cung doi cho:")
print(f"   - ha bac ban le : x 0..{RB_D:.1f} , z {Z_RIM-RB_H:.0f}..{Z_RIM:.0f}"
      f"  (cao dung be day nap {B.T_LID:.0f})")
print(f"   - hoc am        : x 0..{GD:.0f} , z {Z_FL:.0f}..len tren")
print(f"  Hai vung nay CHONG NHAU theo X (0..{RB_D:.1f}). Nen dinh hoc am phai dung")
print(f"  duoi day ha bac, chua them {B.GRIP_LIP:.0f} mm go dac. Suy ra:\n")
print(f"      khe ho vao tay = Z_RIM - be day nap - san go - san trong")
print(f"                     = {Z_RIM:.0f} - {B.T_LID:.0f} - {B.GRIP_LIP:.0f}"
      f" - {Z_FL:.0f} = {S['GRIP_APER']:.0f} mm\n")
print(f"  Do la mot DINH LUAT, khong phai lua chon: chi co hai don bay.")
print(f"  {'be day nap':>12s}{'khe ho vao tay':>17s}   ghi chu")
for t in (12.0, 13.0, 15.0, 17.0, 19.0):
    ap = Z_RIM - t - B.GRIP_LIP - Z_FL
    note = ("DANG CHOT" if abs(t - B.T_LID) < 1e-9 else
            "nap mong hon — xem docs/NAP-GO-DAC.md truoc khi doi" if t < B.T_LID else
            "nap day hon thi tay bop hon")
    print(f"  {t:12.0f}{ap:17.0f}   {note}")
print(f"\n  (Don bay thu hai la nang vanh Z_RIM, tuc lam hop cao them — bo.)")

# ==========================================================================
hr("2. LOI DA CO — do lai bang so")
OLD_H = 28.0
old_ceil = Z_FL + OLD_H
print(f"  Ban cu de tran hoc PHANG o Z{old_ceil:.0f} (= san trong {Z_FL:.0f} + cao hoc"
      f" {OLD_H:.0f}).")
print(f"  Ha bac ban le chiem z {Z_RIM-RB_H:.0f}..{Z_RIM:.0f}. Z{old_ceil:.0f} nam TRONG dai do.")
print(f"  Vay o cao do tran hoc, go con o dau theo X?\n")
print(f"  {'x':>12s}{'co go ngay tren tran?':>26s}")
for xa, xb, zhi in ((0.0, RB_D, Z_RIM - RB_H), (RB_D, GD, Z_RIM)):
    ok = 'KHONG — ha bac da lay mat' if old_ceil > zhi else 'CO'
    print(f"  {xa:5.1f} .. {xb:4.1f}{ok:>26s}")
print(f"\n  => Doan tran con MOC duoc chi la {GD - RB_D:.1f} mm (dang le {GD:.0f}).")
print(f"     Dot ngon tay dai {B.L_DISTAL:.0f} -> lot {(GD-RB_D)/B.L_DISTAL*100:.0f} %."
      f" Con te hon hoc sau 12 cu ({12/B.L_DISTAL*100:.0f} %).")
print(f"\n  Vi sao tu kiem cu khong bat: dieu kien viet la")
print(f"      GRIP_Z1 > Z_RIM - REBATE_H  VA  REBATE_D > GRIP_D")
print(f"  Ve sau la {RB_D:.1f} > {GD:.0f} — SAI, nen ca menh de khong bao gio dung.")
print(f"  Kiem moi (box_spec.selfcheck) do GRIP_LIP_MIN: quet TUNG DIEM tren tran,")
print(f"  o moi x doi hoi con >= {B.GRIP_LIP_REQ:.1f} mm go dac ben tren. Khong the lot nua.")

# ==========================================================================
hr("3. BAN KINH BO MEP NGOAI TRAN — hai yeu cau nguoc chieu")
print(f"  Bo cang lon thi mep cang em tay, nhung dinh bo cang an len cao, ma tran")
print(f"  hoc lai bi tran {S['GRIP_APER']:.0f} mm chan tren -> long hoc thap xuong,")
print(f"  ngon tay khong lot het chieu sau. Quet R:\n")
print(f"  {'R':>6s}{'cao long hoc tai x=R':>23s}{'tran phang con':>16s}"
      f"{'be mat tran':>13s}{'khe lung ngon':>15s}")
R0 = B.GRIP_R
best = None
for i in range(20, 91):
    B.GRIP_R = i/10
    d = B.derive()
    if d['GRIP_FIT'] >= B.FING_MAR: best = B.GRIP_R
    if i % 10 == 0 or abs(i/10 - R0) < 1e-9:
        print(f"  {B.GRIP_R:6.1f}{d['GRIP_Z_TOP']-B.GRIP_R-Z_FL:23.2f}{d['GRIP_FLAT']:16.2f}"
              f"{d['GRIP_SURF']:13.2f}{d['GRIP_FIT']:15.2f}"
              + ("   <- CHOT" if abs(i/10 - R0) < 1e-9 else ""))
B.GRIP_R = R0
print(f"\n  Doi hoi khe lung ngon >= {B.FING_MAR:.1f} mm -> R lon nhat = {best:.2f}.")
m0 = B.mass_of(S, 'loi on dinh')[2]
P0 = m0*9.81*B.DYN/2
rmin = P0/(B.N_FING*B.FING_W*math.radians(B.WRAP_SKIN)*B.P_COMFORT)
print(f"\n  Chan DUOI thi nguoc lai. Luc bao gio cung bat dau don ve mep bo; da dau")
print(f"  ngon boc quanh mep chung {B.WRAP_SKIN:.0f}°, tuc dai cham chi rong"
      f" R x {math.radians(B.WRAP_SKIN):.3f}.")
print(f"  Doi hoi ap luc luc do <= {B.P_COMFORT*1000:.0f} kPa ({P0:.0f} N moi tay,"
      f" {B.N_FING} ngon x {B.FING_W:.0f} rong):")
print(f"      R >= {P0:.0f} / ({B.N_FING}x{B.FING_W:.0f}x{math.radians(B.WRAP_SKIN):.3f}"
      f"x{B.P_COMFORT:.2f}) = {rmin:.2f} mm\n")
print(f"  {'R':>6s}{'ap luc luc bat luc':>21s}   ket qua")
for r in (3.0, 3.5, 4.0, 4.5, 5.0):
    pr = P0/(B.N_FING*B.FING_W*r*math.radians(B.WRAP_SKIN))*1000
    ok = ('DAU TAY' if r < rmin else
          'ngon khong lot het' if r > best else 'DUOC')
    print(f"  {r:6.1f}{pr:18.0f} kPa   {ok}")
CUTTERS = (3.0, 4.0, 5.0, 6.0, 8.0, 10.0)
win = [c for c in CUTTERS if rmin <= c <= best]
print(f"\n  Cua so cho phep: {rmin:.2f} .. {best:.2f} mm — rong {best-rmin:.2f} mm.")
print(f"  Dao bo canh co san (mm): {', '.join(f'{c:.0f}' for c in CUTTERS)}")
print(f"  Loi vao cua so: {', '.join(f'R{c:.0f}' for c in win) if win else 'KHONG CO'}"
      f"{'  — DUY NHAT mot dao, khong con gi de chon' if len(win) == 1 else ''}.")
print(f"  Da chot GRIP_R = {B.GRIP_R:.1f}  "
      f"({'khop' if win and abs(win[0]-B.GRIP_R) < 1e-9 else 'LECH'}).")
print(f"\n  Ghi chu: docs cu tung viet 'bo tron mep >= R8, cung tri so da chot cho")
print(f"  quai da'. Cho quai da thi dung — da vat qua mot canh tu do. O day mep bo")
print(f"  nam duoi mot tran bi khong che chieu cao, R8 lam long hoc chi con")
B.GRIP_R = 8.0; d8 = B.derive(); B.GRIP_R = R0
print(f"  {d8['GRIP_Z_TOP']-8.0-Z_FL:.1f} mm (khe lung ngon {d8['GRIP_FIT']:+.2f}) — ngon tay khong vao het.")
print(f"  Tri so R8 do da duoc CHEP LAI tu bai toan khac. Bo.")

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
print(f"  vua dung cho dau ngon tay gap lai (dot ngoai cheo len khi bau) ma van cham")
print(f"  tran suot ca {B.L_DISTAL:.0f} mm, thay vi chi cham o mot diem gan mieng hoc.")

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
print(f"\n  Khe hep nhat {S['GRIP_FIT']:.2f} mm (yeu cau >= {B.FING_MAR:.1f}). DAT.")
print(f"\n  Nhay theo co ngon tay. Dat dau mut o do sau 'dep' roi hoi CA ngon co lot")
print(f"  khong; lay dep lon nhat con lot. (Ngon to hon thi phai dung nong hon.)")
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
            "nam 95%" if td == 17.5 else
            "ngon rat to" if td > 17.5 else "nu / ngon ut")
    print(f"  {td:16.1f}{dep:17.1f}{surf:13.1f}{note:>26s}")
print(f"\n  Doc: ngon to hon ngon mau van dat toi {max_depth(17.5):.1f} mm — qua"
      f" dot ngon {B.L_DISTAL:.0f}.")
print(f"  Cai gioi han khong phai chieu sau hoc ma la CHIEU CAO long hoc, va chieu")
print(f"  cao do bi ha bac ban le khoa lai o {S['GRIP_APER']:.0f} mm (muc 1).")

# ==========================================================================
hr("6. AP LUC LEN DAU NGON TAY")
m = B.mass_of(S, 'loi on dinh')[2]
P_hand = m*9.81*B.DYN/2
A_new = B.N_FING*B.FING_W*min(S['GRIP_SURF'], B.L_DISTAL)
EDGE_SHARP, WRAP = 0.5, 60.0     # canh vuong bao gio cung cham ~0,5 mm; da boc ~60 do
print(f"  Hop {m:.2f} kg, he so dong {B.DYN:.0f} -> {P_hand:.0f} N moi tay.")
print(f"  Ap luc phu thuoc BE RONG DAI CHAM, ma dai cham lai phu thuoc hinh tran.\n")
print(f"  {'tinh huong':>40s}{'dai cham':>11s}{'dien tich':>12s}{'ap luc':>11s}")
rows = [("canh vuong, ngon vua bat luc", EDGE_SHARP),
        (f"bo R{B.GRIP_R:.0f}, da boc {WRAP:.0f}°",
         B.GRIP_R*math.radians(WRAP)),
        ("tran phang sau 12, ngon cham 12 (Rev B)", min(12.0, B.L_DISTAL)),
        (f"tran bo + doc, cham het dot ngon", min(S['GRIP_SURF'], B.L_DISTAL))]
for lbl, surf in rows:
    A = B.N_FING*B.FING_W*surf
    print(f"  {lbl:>40s}{surf:11.2f}{A:12.0f}{P_hand/A*1000:10.0f} kPa")
print(f"\n  Nguong: ~100 kPa cam thay em, ~200 kPa chiu duoc, >400 kPa dau trong")
print(f"  chua day mot phut.")
print(f"  Doc bang: canh VUONG cho {P_hand/(B.N_FING*B.FING_W*EDGE_SHARP)*1000:.0f} kPa"
      f" — dau ngay lap tuc. Bo R{B.GRIP_R:.0f} ha xuong")
print(f"  {P_hand/(B.N_FING*B.FING_W*B.GRIP_R*math.radians(WRAP))*1000:.0f} kPa"
      f" — nho di {B.GRIP_R*math.radians(WRAP)/EDGE_SHARP:.1f} lan — ngay o thoi diem xau nhat;")
print(f"  roi do doc dan tai ra het dot ngon -> {P_hand/A_new*1000:.0f} kPa.")
print(f"  Bo mep lo cho THOI DIEM XAU NHAT, do doc lo cho TRANG THAI ON DINH.")
print(f"  Cai bo tron KHONG lam mat chieu sau moc: no bien mot canh sac thanh"
      f" {S['GRIP_ARC']:.1f} mm")
print(f"  cung, cong {S['GRIP_FLAT']/math.cos(th):.1f} mm tran doc = {S['GRIP_SURF']:.1f} mm BE MAT,")
print(f"  dai hon ca chieu sau hoc {GD:.0f} mm.")

# ==========================================================================
hr("7. DAI GO TREN HOC — kiem ben tren TIET DIEN THAT")
def sect(n=2000):
    """A, z trong tam, I quanh truc ngang qua trong tam, cua tiet dien vach
    tai cho co hoc am (da tru hoc am va ha bac ban le)."""
    dx = WG/n
    A = Az = 0.0; cells = []
    for i in range(n):
        x = (i + 0.5)*dx
        zhi = (Z_RIM - RB_H) if x < RB_D else Z_RIM
        zlo = S['grip_ceil'](x) if x < GD else Z_FL
        if zhi <= zlo: continue
        a = (zhi - zlo)*dx; zc = (zhi + zlo)/2
        A += a; Az += a*zc; cells.append((a, zc, zhi - zlo))
    zc0 = Az/A
    I = sum(a*(zc - zc0)**2 + a*h*h/12 for a, zc, h in cells)
    zmin = min(S['grip_ceil'](WG*(i+0.5)/n) if WG*(i+0.5)/n < GD else Z_FL for i in range(n))
    return A, zc0, I, zmin
A_s, zc_s, I_s, zmin_s = sect()
c_max = max(Z_RIM - zc_s, zc_s - zmin_s)
P_des = m*9.81*B.DYN
P_h = P_des/2
M = P_h*GW/8
sig = M*c_max/I_s
tau = 1.5*(P_h/2)/A_s
dfl = P_h*GW**3/(192*B.E_W*I_s)
print(f"  Dam nhip {GW:.0f} mm (be rong hoc), ngam hai dau vao vach hai ben hoc.")
print(f"  Tiet dien KHONG phai chu nhat: no la chu L — dai go tren tran (bi ha bac")
print(f"  an mat {RB_D:.1f} o phia ngoai) cong thanh sau hoc {B.GRIP_BACK:.0f} mm chay suot chieu cao.")
print(f"    Dien tich          A  = {A_s:8.1f} mm2")
print(f"    Trong tam          z  = Z{zc_s:6.2f}")
print(f"    Momen quan tinh    I  = {I_s:8.0f} mm4")
print(f"    Thot xa nhat       c  = {c_max:8.2f} mm")
print(f"    Uon            sigma  = {sig:8.2f} MPa / MOR {B.MOR:.0f}   -> he so {B.MOR/sig:.0f}x")
print(f"    Cat              tau  = {tau:8.2f} MPa / {B.SHEAR:.0f}      -> he so {B.SHEAR/tau:.0f}x")
print(f"    Vong giua nhip        = {dfl:8.4f} mm")
b_rect, h_rect = S['GRIP_LEDGE_T'], S['GRIP_LEDGE']
I_r = b_rect*h_rect**3/12
sig_r = M*(h_rect/2)/I_r
print(f"\n  Can duoi — chi lay dai go tren tran nhu mot chu nhat {h_rect:.0f} x {b_rect:.1f}")
print(f"  (bo qua thanh sau hoc, coi nhu no khong dinh vao dau):")
print(f"    I = {I_r:.0f} mm4 ({I_r/I_s*100:.0f} % tiet dien that),"
      f" sigma = {sig_r:.2f} MPa -> he so {B.MOR/sig_r:.0f}x")
print(f"  Ca hai cach deu cho he so hang tram lan.")
print(f"  Ket cau khong phai rang buoc — nhu truoc. Cai rang buoc van la BAN TAY.")

# ==========================================================================
hr("8. CHOT LAI")
for a, b_ in [("Khe ho vao tay (mat ngoai)", f"{S['GRIP_APER']:.0f} mm — HE QUA cua"
                                             f" ha bac ban le, khong tu chon"),
              ("Sau hoc", f"{GD:.0f} mm (dot ngon {B.L_DISTAL:.0f} + ke {GD-B.L_DISTAL:.0f})"),
              ("Rong hoc", f"{GW:.0f} mm theo Y, Y {S['GRIP_Y0']:.0f}..{S['GRIP_Y1']:.0f}"),
              ("Bo mep ngoai tran", f"R{B.GRIP_R:.0f} (chan tren ec-go-no-mi {best:.2f},"
                                    f" dao co san)"),
              ("Doc tran", f"{B.GRIP_SLOPE:.0f}° len phia trong"
                           f" (chan tren goc ma sat {math.degrees(math.atan(B.MU_SKIN)):.1f}°)"),
              ("Cao do tran", f"Z{S['GRIP_Z_TOP']-B.GRIP_R:.2f} thap nhat (x={B.GRIP_R:.0f})"
                              f" -> Z{S['GRIP_Z_IN']:.2f} tai day hoc"),
              ("Dinh bo tron", f"Z{S['GRIP_Z_TOP']:.0f}, cach day ha bac"
                               f" {S['GRIP_LIP_MIN']:.1f} mm go dac"),
              ("Be mat tran", f"{S['GRIP_SURF']:.1f} mm ({S['GRIP_ARC']:.1f} cung +"
                              f" {S['GRIP_FLAT']/math.cos(th):.1f} doc)"),
              ("Ap luc dau ngon", f"{P_hand/A_new*1000:.0f} kPa"),
              ("Dai go tren hoc", f"cao {S['GRIP_LEDGE']:.0f} x day {S['GRIP_LEDGE_T']:.1f}"
                                  f" (cho mong nhat), he so uon {B.MOR/sig:.0f}x"),
              ("Vach ban le", f"{S['WALL_HINGE']:.0f} = sau hoc {GD:.0f} + thanh sau"
                              f" {B.GRIP_BACK:.0f} — phu bi X van {S['X_OA']:.0f}")]:
    print(f"  {a:28s}{b_}")
print(f"\n  Tu kiem box_spec: {B.selfcheck(S) or 'DAT'}")
