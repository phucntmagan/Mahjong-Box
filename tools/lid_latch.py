#!/usr/bin/env python3
"""
Khoa nap — bai toan con treo sau khi phuong an C bo song khoa.
Chay: python3 tools/lid_latch.py

Thu tu lap luan:
  1. Khoa phai chan huong nao? (dong hoc — cho phan truc giac nhat)
  2. Do am an mon them bao nhieu re? (giet not ho khoa canh-canh)
  3. Can bao nhieu luc giu? (tai trong that su)
  4. Nam cham: chon co, kiem he so
  5. Khoa gai brass: phuong an nhin thay duoc, cung dimension day du
  6. So sanh va khuyen nghi
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B
S = B.derive()
LATCH_DZ = 7.0     # truc luoi gai dat duoi vanh bao nhieu (rieng cua khoa nap)
def hr(t): print("\n" + "="*78 + "\n" + t + "\n" + "="*78)

PX, PZ = S['PIN_X'], S['PIN_Z']
XA, ZT = S['LW'], S['Z_LID']              # mep khe rap giua cua canh trai, mat tren
DX, DZ = XA - PX, ZT - PZ
Rs = math.hypot(DX, DZ)

# Phep quay DUNG, khong tuyen tinh hoa: o goc lon so hang cos chiem uu the va
# tuyen tinh hoa cho ket qua qua lac quan (sai toi 2,4 lan o 20 do).
# Do tach phu thuoc CAO DO cua diem xet: diem tren truc chot (Z56) thi he ra,
# diem duoi truc thi ban dau lai khep vao. Nen phai tinh o dung cao do cua chot.
Z_BOLT = (S['Z_SEAM'] + S['Z_LID'])/2       # chot nam giua be day do doc canh khe
def seam_dx(th, z=Z_BOLT):
    """Mep khe rap giua tut ra ngoai bao nhieu khi canh mo goc th (rad)."""
    return DX*(1 - math.cos(th)) + (z - PZ)*math.sin(th)
def seam_dz(th):
    """Mep khe rap giua nang len bao nhieu."""
    return DX*math.sin(th) - DZ*(1 - math.cos(th))
def theta_for_gap(g, z=Z_BOLT):
    """Goc mo cua MOI canh de hai mep khe tach nhau them g mm."""
    lo, hi = 0.0, math.pi/2
    for _ in range(90):
        mid = (lo + hi)/2
        if 2*seam_dx(mid, z) < g: lo = mid
        else: hi = mid
    return (lo + hi)/2

# ==========================================================================
hr("1. KHOA PHAI CHAN HUONG NAO — dong hoc")
print(f"  Truc chot P = ({PX:.1f} , {PZ:.0f}) — lui vao {PX:.1f} tu mat ngoai vach, o cao do")
print(f"  vanh. KHONG phai giua be day nap (xem hinge_kinematics.py muc 1).")
print(f"  Mep khe rap giua = ({XA:.2f} , {ZT:.0f}),")
print(f"  cach truc {Rs:.2f} mm.\n")
print(f"  Quay canh mot goc nho theta, mep khe di chuyen:")
print(f"    dX = -{DZ:.2f}*theta     dZ = +{DX:.2f}*theta     -> ty le {DX/DZ:.1f} : 1")
print(f"  Nghia la mep khe di gan nhu THANG DUNG len, chi he ra ngoai mot chut.\n")
print(f"  Hai kieu mo, hai chuyen dong tuong doi khac han nhau:")
print(f"   (a) MOT canh mo    : mep khe canh do nang {DX:.2f}*theta so voi canh kia")
print(f"                        -> can chan phuong Z")
print(f"   (b) HAI canh cung mo: hai mep khe nang BANG NHAU, chi TACH NHAU "
      f"{2*DZ:.0f}*theta")
print(f"                        -> chan Z vo dung, phai chan phuong X")
print(f"\n  Kieu (b) khong phai truong hop hiem: lat up hop la trong luong hai canh")
print(f"  deu keo chung mo cung luc. Do la truong hop THUONG GAP nhat.\n")
print(f"  He qua: mot cai chot truot ngang xuyen tu canh nay sang canh kia — thu")
print(f"  ai cung nghi toi dau tien — KHONG khoa duoc, vi kieu (b) rut no ra theo")
print(f"  dung truc cua no:")
print(f"  (tinh o cao do chot, Z{Z_BOLT:.0f} — giua be day do doc canh khe giua)")
print(f"  {'chot an sau':>14s}{'tuot khi moi canh mo':>22s}{'khe da venh len':>18s}")
for e in (5.0, 6.5, 8.0, 12.0):
    th = theta_for_gap(e)
    print(f"  {e:14.1f}{math.degrees(th):20.1f}°{seam_dz(th):15.0f} mm")
print(f"\n  Dat chot cao hay thap cung khong cuu duoc: voi chot an sau {6.5}, khe venh")
zb_lo, zb_hi = S['Z_SEAM'], S['Z_LID']
for z, lbl in [(zb_hi, 'sat mat tren nap'), (Z_BOLT, 'giua be day'), (zb_lo, 'sat mat duoi')]:
    th = theta_for_gap(6.5, z)
    print(f"    {lbl:20s} (Z{z:.0f}): {seam_dz(th):5.0f} mm")
print(f"\n  => Khoa noi CANH voi CANH khong dung duoc, du chot to den may.")

# ==========================================================================
hr("2. DO AM — giet not ho khoa canh-canh")
mv1 = 2*B.STILE*B.k_stile()*5          # do doc xe XUYEN TAM (P7)
mv1_t = 2*B.STILE*B.K['cocobolo ngang tho']*5   # neu P7 truot: xe tiep tuyen
mv = 2*mv1
print(f"  Moi canh nap co {2*B.STILE:.0f} mm go ngang be rong nam trong chuoi")
print(f"  (hai do doc {B.STILE:.0f}, xe {B.STILE_GRAIN}); tam Nu tha nen khong dong gop.")
print(f"  O dMC 5 %: moi canh no {mv1:.2f} mm -> khe rap giua dong lai {mv:.2f} mm.\n")
th_mv = theta_for_gap(mv)
print(f"  Bat ky khoa nao noi hai canh voi nhau deu phai co {mv:.2f} mm re theo X")
print(f"  de con lap duoc quanh nam. Ma {mv:.2f} mm re do, theo muc 1, cho moi canh")
print(f"  mo {math.degrees(th_mv):.1f}° va khe venh len {seam_dz(th_mv):.1f} mm.")
_thT = theta_for_gap(2*mv1_t)
print(f"  Neu P7 truot va do doc hoa ra xe tiep tuyen: {2*mv1_t:.2f} mm re -> "
      f"{math.degrees(_thT):.1f}° va {seam_dz(_thT):.1f} mm venh.")
print(f"  Ket luan khong doi theo huong nao — no chi manh hon o truong hop xau.")
print(f"\n  => KET LUAN CUA HAI MUC DAU:")
print(f"     Khoa phai noi NAP voi THAN, khong phai canh voi canh.")
print(f"     Va no chi duoc chan phuong Z — de tu do theo X — neu khong no se")
print(f"     chong lai {mv:.2f} mm gian no theo mua va tu pha go.")

# ==========================================================================
hr("3. CAN BAO NHIEU LUC GIU")
V = S['V']
m_leaf = (V['khung nap']/2/1e6*B.RHO['cocobolo']
          + V['tam Nu']/2/1e6*B.RHO['Nu go do'])
# Truc xoay nam DUNG tai canh ngoai tren cua than (arris): canh nap trai roi tu
# x=PIN_X den x=LW, nen tay don trong tam = nua be rong canh.
arm_leaf = (S['LW'] - PX)/2
m_tray = V['khay quan']/4/1e6*B.RHO['cocobolo'] + 36*B.M_TILE_G/1000
m_bay = 2*m_tray
arm_bay = S['WALL_HINGE'] + S['BAY']/2 - PX
m_ac = (V['khay phu kien']/1e6*B.RHO['cocobolo']
        + (8+4)*B.M_TILE_G/1000 + 4*0.005)          # AC-01 + Joker + du phong + xuc xac
arm_ac = S['X_SEAM'] - PX
print("  Truong hop thiet ke: LAT UP HOP. Luc do trong luong canh nap va toan bo")
print("  ruot hop deu de len mat trong cua nap va co xoay no ra.\n")
rows = [("Trong luong mot canh nap", m_leaf, arm_leaf),
        ("2 khay quan day trong mot khoang", m_bay, arm_bay),
        ("Nua khay phu kien + quan Joker", m_ac/2, arm_ac)]
M = 0.0
print(f"  {'thanh phan':36s}{'kg':>7s}{'tay don':>9s}{'N.mm':>9s}")
for lbl, m, a in rows:
    mm = m*9.81*a; M += mm
    print(f"  {lbl:36s}{m:7.2f}{a:9.0f}{mm:9.0f}")
print(f"  {'TONG momen quanh truc chot':36s}{'':7s}{'':9s}{M:9.0f}")
print(f"\n  Bo tri {S['MAG_N_LEAF']} diem giu moi canh: tay don "
      f"{' va '.join(f'{r:.0f}' for r in S['MAG_R'])} mm, o ca hai dau hop,")
print(f"  tong tay don {S['MAG_SUM_R']:.0f} mm. Neu moi diem gop luc F:")
F1 = M/S['MAG_SUM_R']
print(f"    F x {S['MAG_SUM_R']:.0f} = {M:.0f}  ->  F = {F1:.2f} N moi diem (tinh)")
for k in (1, 3):
    print(f"    he so dong {k}  ->  {F1*k:5.2f} N moi diem")
print(f"\n  Chot DAC TINH: giu duoc hop LAT UP hoan toan voi he so dong 3.")
print(f"  => moi diem giu phai chiu >= {F1*3:.1f} N.")

# ==========================================================================
hr("4. NAM CHAM — phuong an chinh")
mw, md, mt = B.MAG
print(f"  Chan Z, tu do hoan toan theo X — dung cai muc 2 doi hoi.")
print(f"  Nam cham keo theo phuong THANG DUNG, tuc dung huong manh nhat cua no;")
print(f"  {mv:.2f} mm truot ngang theo mua chi lam lech {mv/mw*100:.0f} % be mat, gan nhu")
print(f"  khong doi luc.\n")
for a, bb in [("Nam cham", f"khoi {mw:.0f} x {md:.0f} x {mt:.0f}, {B.MAG_GRADE}"),
              ("So luong", f"{S['MAG_N_LEAF']} moi canh x 2 canh = {2*S['MAG_N_LEAF']} cap"),
              ("Vi tri X", f"{B.MAG_X[0]:.0f} va {B.MAG_X[1]:.0f} tren canh trai;"
                           f" doi xung tren canh phai"),
              ("Vi tri Y", f"{B.MAG_Y:.1f} (hai dau hop) — nam trong dai {B.WALL_FB:.0f} mm"
                           f" ma nap va vanh than con chong len nhau"),
              ("Go con lai", f"{S['MAG_MAR_OUT']:.1f} mm ra mep nap, {S['MAG_MAR_IN']:.1f} mm"
                             f" vao long hop"),
              ("Hoc am", f"{mw+0.2:.1f} x {md+0.2:.1f} x sau {B.MAG_REC:.1f}, dan epoxy,"
                         f" mat nam cham THUT 0,1 duoi be mat"),
              ("Doi ung", "nam cham thu hai (khong dung dia thep — thep se ri trong"
                          " khi hau am, va cocobolo nhieu dau lam kho phat hien)"),
              ("Day nap con lai", f"{S['t_lid'](max(B.MAG_X)) - B.MAG_REC:.1f} mm o cho"
                                  f" mong nhat")]:
    print(f"   {a:18s}: {bb}")
print(f"\n  Kiem:")
P_eff = B.MAG_PULL*(1-B.MAG_DERATE)
print(f"   {'yeu cau moi diem (he so dong 3)':44s}{F1*3:7.1f} N")
print(f"   {'luc keo mot cap, tiep xuc truc tiep':44s}{B.MAG_PULL:7.1f} N")
print(f"   {'sau khi tut do lop hoan thien (-25 %)':44s}{P_eff:7.1f} N")
print(f"   {'HE SO AN TOAN':44s}{P_eff/(F1*3):7.1f} x")
print(f"   {'tong luc giu mot canh':44s}{P_eff*S['MAG_N_LEAF']:7.1f} N")
m_mag = 2*S['MAG_N_LEAF']*2*mw*md*mt/1e6*B.RHO_MAG
print(f"   {'khoi luong them vao (8 cap)':44s}{m_mag*1000:7.0f} g")
print(f"\n  > CANH BAO: {B.MAG_PULL:.0f} N moi cap la tri so CATALOGUE o tiep xuc truc tiep.")
print(f"  > Phai do lai tren mau that: lop hoan thien day 0,1-0,2 mm giua hai mat")
print(f"  > lam tut luc 15-25 %, va tri so cong bo cua hang Trung Quoc thuong lac quan.")
print(f"  > DAC TINH KIEM (dua vao QA, khong phai vao BOM): moi cap nam cham lap")
print(f"  > tren mau da hoan thien phai do duoc >= {F1*3:.1f} N. Chon nam cham theo")
print(f"  > ket qua do, khong theo catalogue. Khoi {mw:.0f} x {md:.0f} x {mt:.0f} N45 la diem xuat phat.")
print(f"\n  > HE SO 1,6 do la NAM TREN he so dong 3 roi. So voi tai TINH khi lat up")
print(f"  > hoan toan, bien la {P_eff/F1:.1f} lan. Nhung 1,6 khong con cho de sai neu")
print(f"  > mau do khong dat: tay don nam cham bi CHAN TREN boi ba khe luon ngon")
print(f"  > (dai {B.WELL_W:.0f} mm quanh X = {', '.join(f'{x:.0f}' for x in S['WELL_X'])}), nen KHONG the")
print(f"  > day nam cham ra xa hon {max(B.MAG_X):.0f} de an gian bang tay don.")
_t_hi = 8.0
_rec_hi = _t_hi + 0.2
_left = S['t_lid'](max(B.MAG_X)) - _rec_hi
print(f"\n  DU PHONG neu mau do khong dat {F1*3:.1f} N: TANG BE DAY nam cham, khong")
print(f"  tang chieu dai (chieu dai bi chan boi khoang ho {B.MAG_X[1]-B.MAG_X[0]:.0f} mm giua hai hoc).")
print(f"   {mw:.0f} x {md:.0f} x {_t_hi:.0f} , hoc am sau {_rec_hi:.1f}"
      f" -> nap con {_left:.1f} mm (toi thieu 6,0) : {'DU CHO' if _left >= 6.0 else 'KHONG DU CHO'}")
print(f"   Vach truoc day {B.WALL_FB:.0f} mm, hoc khoet THANG DUNG tu vanh Z{S['Z_SEAM']:.0f}"
      f" xuong, con {S['Z_SEAM']-B.BOT-_rec_hi:.1f} mm than vach: du cho.")
print(f"   => co san mot buoc tang luc ma khong doi bat ky kich thuoc phu bi nao.")
print(f"\n  Cai nam cham KHONG lam duoc:")
print(f"   - Khong khoa. Ai cung mo duoc nap bang cach nhac len. Do la nap hop, khong")
print(f"     phai ket sat — nhung phai noi ro voi khach de khong ai ky vong sai.")
print(f"   - Khong chong duoc cu roi tu do. O 3 g thi dat; roi tu 1 m thi khong.")
print(f"   - Nam cham gan quan co: quan Mahjong khong tu tinh, khong van de. Nhung")
print(f"     canh bao trong so tay: giu the tin dung va dong ho co cach hop 20 cm.")

# ==========================================================================
hr("5. KHOA GAI BRASS — phuong an nhin thay duoc")
print(f"  Cung phai noi NAP voi THAN va chi chan Z, y nhu nam cham. Hinh thuc kha thi")
print(f"  duy nhat la LUOI GAI LAT QUA MEP NAP: xoay len de len mat nap, xoay xuong thi")
print(f"  nam ap vao mat vach.\n")
z_rim_at = S['z_rim_at']
LX = (100.0, S['W']-100.0)          # mot khoa moi canh, tranh dai hoc am 125..245
for a, bb in [("Vi tri", f"X = {LX[0]:.0f} (canh trai) va {LX[1]:.0f} (canh phai),"
                         f" tren mat ngoai vach truoc"),
              ("Vi sao khong o giua", f"khe rap giua X={S['X_SEAM']:.0f} nam giua ba khe luon"
                                      f" ngon nhac khay tren vanh vach truoc; de o do thi luoi"
                                      f" gai va khe khoet vao nhau"),
              ("Du mot cai moi canh", "giu bat ky mot diem nao cua canh la canh do khong"
                                      " xoay duoc nua — dong hoc chi co mot bac tu do"),
              ("De ban ma", f"vach truoc day {B.WALL_FB:.0f}, vanh o Z{z_rim_at(LX[0]):.0f};"
                            f" hoc am nay o vach trai/phai nen mat truoc con trong"),
              ("De", f"brass 40 x 12 x 3, ha bac 3 mm vao mat vach"),
              ("Truc xoay", f"chot brass O3, truc chay theo X, o Z{S['Z_RIM']-LATCH_DZ:.0f}"
                            f" (lui {LATCH_DZ:.0f} mm duoi vanh — de de brass 40x12 nam tron"
                            f" tren mat vach ma khong cham vanh)"),
              ("Luoi gai", f"brass 3 mm day, voi ra {B.WALL_FB+10:.0f}, dau luoi de len"
                           f" mat nap {10:.0f} mm"),
              ("Ha bac tren nap", f"10 (Y) x 34 (X) x sau 3,2 -> luoi phang voi mat nap"),
              ("Giu vi tri", "vong ep song (wave washer) o truc cho ma sat ~0,3 N.m;"
                             " luoi dung yen o ca hai vi tri, khong can lo xo")]:
    print(f"   {a:20s}: {bb}")
F_catch = M/(LX[0]-PX)
print(f"\n  Kiem: mot khoa moi canh, tay don {LX[0]-PX:.0f} mm tu truc chot")
print(f"   luc tren luoi gai, he so dong 3 : {F_catch*3:.0f} N")
w_t, t_t = 34.0, 3.0
sig = 6*(F_catch*3)*10/(w_t*t_t**2)
print(f"   uon luoi (34 x 3, voi 10)       : {sig:.0f} MPa"
      f"  / brass ~250 -> he so {250/sig:.0f}x")
print(f"   ep mat go duoi luoi (34 x 10)   : {F_catch*3/(w_t*10):.2f} MPa"
      f"  / cocobolo {B.C_PERP:.0f} -> he so {B.C_PERP/(F_catch*3/(w_t*10)):.0f}x")
print(f"\n  Doi lai: hai chi tiet chuyen dong quay lai vao thiet ke, dung cai ma phuong")
print(f"  an C vua bo di. Va phai thao tac moi lan mo hop.")

# ==========================================================================
hr("6. SO SANH VA KHUYEN NGHI")
print(f"  {'':32s}{'nam cham':>18s}{'khoa gai brass':>24s}")
for a, x, y in [
    ("Chi tiet chuyen dong", "0", "2"),
    ("Chi tiet mon", "khong", "truc xoay"),
    ("Phai thao tac khi mo", "khong", "co"),
    ("Nhin thay", "khong", "co"),
    ("He so an toan khi lat up", f"{P_eff/(F1*3):.1f}x (luc hut)", f"{250/sig:.0f}x (ben luoi gai)"),
    ("Khoa chong mo khong", "KHONG", "KHONG - khong co chot"),
    ("Chong xoc/lach cach", "co", "co, va ep chat hon"),
    ("Chiu duoc gian no theo mua", "co", "co"),
    ("Khoi luong them", f"{m_mag*1000:.0f} g", "~60 g"),
    ("Rui ro che tao", "thap", "trung binh"),
]:
    print(f"  {a:32s}{x:>18s}{y:>24s}")
print(f"\n  => KHUYEN NGHI: NAM CHAM.")
print(f"     Phuong an C duoc chon vi 'khong co cau, khong chi tiet mon'. Gan lai hai")
print(f"     cai khoa gai la pha chinh ly do da chon no. Nam cham giu du {P_eff/(F1*3):.1f} lan")
print(f"     yeu cau, khong nhin thay, khong phai thao tac, khong mon.")
print(f"\n     Chon khoa gai brass NEU khach doi mot khoa NHIN THAY duoc — day la")
print(f"     quyet dinh ve san pham, khong phai ve ky thuat. Luc do lam ca hai:")
print(f"     nam cham giu hang ngay, khoa gai lam chi tiet trang tri va chot van chuyen.")
