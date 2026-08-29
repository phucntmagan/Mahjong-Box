#!/usr/bin/env python3
"""
Bon chi tiet cong nang con treo tu review Rev B, giai bang so.
Chay: python3 tools/detail_features.py

  1. Nhac khay quan ra khoi khoang        (review §2.3 — de xuat cu KHONG dong duoc)
  2. Hom ngon ranh Joker                  (review §2.3)
  3. Do mep tu do cua nap                 (review §3.2 — kiem lai, khong con la van de)
  4. Nap che o xuc xac                    (QUAI-XACH muc 5 cua bang tac dong day chuyen)
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B
S = B.derive()
def hr(t): print("\n" + "="*78 + "\n" + t + "\n" + "="*78)

TILE = B.TILE_MAX
FINGER_W, FINGER_T = 20.0, 12.0    # dau ngon tro nguoi lon: rong ~20, day ~12

# ==========================================================================
hr("1. NHAC KHAY QUAN — vi sao de xuat cu khong dong duoc")
gap_end  = (S['BAY'] - B.TRAY[1])/2          # khe ben khay theo X
gap_side = (B.INNER_Y - B.TRAY[0])/2         # khe dau khay theo Y
field_l  = 12*TILE[0] + 2*1.0                # chieu dai toi thieu long khay
field_w  = 3*TILE[1] + 2*1.0
print(f"  Khoang khay {S['BAY']:.0f} x {B.INNER_Y:.0f} ; khay {B.TRAY[1]:.0f} x {B.TRAY[0]:.0f}")
print(f"  Khe quanh khay: {gap_end:.1f} mm hai ben (X), {gap_side:.1f} mm hai dau (Y)")
print(f"  Truong quan toi thieu: {field_l:.1f} x {field_w:.1f} ; long khay "
      f"{B.TRAY_IN[0]:.0f} x {B.TRAY_IN[1]:.0f}")
print(f"  Du dia con lai trong long khay: {B.TRAY_IN[0]-field_l:.1f} theo dai, "
      f"{B.TRAY_IN[1]-field_w:.1f} theo rong\n")
print(f"  => Khong co cho nao quanh khay lot duoc ngon tay ({FINGER_T:.0f} mm day).")
print(f"     Truong quan chiem gan het khoang theo CA HAI phuong, nen KHONG THE")
print(f"     lay cho bang cach thu nho khay.")
print(f"\n  De xuat cu (review §2.3): 'hoc lom {B.WELL_W:.0f} x 10 tren vanh khoang,")
print(f"  trung vi tri hoc tren khay -> mo duoc ~17 mm de kep'. KHONG DONG DUOC:")
for t in [f"khoet vanh than chi lam lo MAT NGOAI cua khay, van khong co gi de moc;",
          f"khoet vanh khay thi ngay sau vanh la truong quan — dinh quan chi thap hon",
          f"  vanh khay {S['HEADROOM']:.1f} mm, nen hoc sau hon {S['HEADROOM']:.1f} la ho vao o quan;",
          f"'kep' can hai diem doi dien, ma hai ben doi dien cua khay deu bi chan:",
          f"  mot ben la vach ban le (mat mong chiem {S['KN_RUN']:.0f}/{B.LID_L:.0f} mm),",
          f"  ben kia la vach ngan day {S['DIV']:.0f} mm."]:
    print(f"   - {t}")

print(f"\n  --- LOI GIAI: KHE LUON NGON + MO MOC, o hai DAU khoang ---")
print(f"  Nhac hai tay, moi tay mot dau — dung tinh than cua phuong an C.")
print(f"  CHI lam cho hai khoang KHAY QUAN (X = {' va '.join(f'{w:.0f}' for w in S['WELL_X'])}).")
print(f"  KHONG lam cho khoang phu kien: hoc am hai tay chiem bang X "
      f"{S['GRIP_X0']:.0f}..{S['GRIP_X1']:.0f} va an sau {B.GRIP_D:.0f} tu mat ngoai; khe luon")
print(f"  ngon an {B.WELL_D:.0f} tu mat trong. Cong lai vua het be day vach {B.WALL_FB:.0f} — thung vach.")
print(f"  AC-01 duoc nhac bang cach kep hai dai go qua hai hom ngon ranh Joker (muc 2).\n")
for a, b in [
  ("Hoc tren vach truoc/sau",
   f"{B.WELL_W:.0f} rong x sau {B.WELL_D:.0f} vao vach {B.WALL_FB:.0f}, chay tu vanh"
   f" xuong san Z{S['Z_FLOOR']:.0f}"),
  ("Da ngoai con lai",  f"{B.WALL_FB - B.WELL_D:.0f} mm — mat ngoai hop KHONG bi thung"),
  ("Khoet mat dau khay", f"{B.WELL_W:.0f} rong x cao {B.NOTCH_H:.0f} tu vanh khay xuong,"
                         f" XUYEN het be day vach khay {B.NOTCH_D:.0f}"),
  ("Khe luon ngon (Y)",  f"{B.WELL_D:.0f} + {B.AC_CLR:.1f} + {B.NOTCH_D:.0f}"
                         f" - ni {B.WELL_FELT:.0f} = {S['LIFT_CHANNEL']:.1f} mm"),
  ("Mo de moc ngon",     f"sau {S['LIFT_LEDGE']:.0f} x rong {B.WELL_W:.0f},"
                         f" cao {S['LIFT_LIP']:.0f} mm con lai duoi cho khoet"),
  ("Cao do mo, khay tren", f"Z{S['Z_LIFT_LEDGE']:.0f}"),
]:
    print(f"   {a:24s}: {b}")
m_tray = (S['V']['khay quan']/4/1e6*B.RHO['cocobolo'] + 36*B.M_TILE_G/1000)
P = m_tray*9.81
print(f"\n  Kiem mo: khay day {m_tray:.2f} kg -> {P:.0f} N, chia hai tay {P/2:.0f} N moi ben.")
A_led = B.WELL_W*S['LIFT_LEDGE']
print(f"   ep mat go tren mo : {P/2:.0f} N / {A_led:.0f} mm2 = {P/2/A_led:.3f} MPa"
      f"  (cho phep ~{B.C_PERP:.0f}) -> he so {B.C_PERP/(P/2/A_led):.0f}x")
sig = 6*(P/2)*S['LIFT_LEDGE']/(B.WELL_W*S['LIFT_LIP']**2)
print(f"   uon chan mo       : {sig:.3f} MPa  (MOR {B.MOR:.0f}) -> he so {B.MOR/sig:.0f}x")
print(f"   => Ket cau thua. Rang buoc la khe {S['LIFT_CHANNEL']:.1f} mm so voi"
      f" dau ngon {FINGER_T:.0f} mm day: vua du.")
print(f"\n  Doi lai: cho khoet ho ra {S['TILE_OPEN']:.1f} mm tren be day quan"
      f" {TILE[2]:.1f} mm.")
travel = B.WELL_D + B.AC_CLR + B.NOTCH_D
print(f"   Quan dau moi hang co the truot ra toi da {travel:.1f} mm roi cham day hoc —")
print(f"   khong roi ra duoc (quan dai {TILE[1]:.1f}), nhung se ken khi tra khay vao.")
print(f"   Chan bang dai NI {B.WELL_FELT:.0f} mm dan vao day hoc: vua chan quan, vua lam dem.")

# ==========================================================================
hr("2. HOM NGON RANH JOKER")
strip = (S['AC_W_IN'] - B.AC_JOKER[0])/2
lat = B.AC_JOKER[0] - TILE[0]
print(f"  Ranh Joker {B.AC_JOKER[0]:.0f} rong x {B.AC_JOKER[1]:.0f} dai x"
      f" {B.AC_JOKER[2]:.1f} sau, chua 8 quan xep 2 lop x 4.")
print(f"  Quan ho ngang chi {lat:.1f} mm, ma ranh sau {B.AC_JOKER[2]:.1f} —"
      f" khong nhat ra duoc.")
print(f"  Dai go moi ben ranh: ({S['AC_W_IN']:.0f} - {B.AC_JOKER[0]:.0f})/2 = {strip:.0f} mm\n")
print(f"  Hom ban nguyet O{B.SCAL_D:.0f} sau {B.SCAL_DEP:.0f}, khoet vao dai go tu phia ranh,")
print(f"  o GIUA chieu dai ranh, tren CA HAI dai -> kep duoc hai mat ben cua quan.")
print(f"  Hai hom doi nhau nay lam LUON viec thu hai: kep hai dai go de RUT AC-01 ra")
print(f"  khoi khoang — AC-01 khong the co khe luon ngon nhu khay quan (muc 1).")
print(f"   Dai go con lai : {strip:.0f} - {B.SCAL_DEP:.0f} = {S['SCAL_LEFT']:.0f} mm")
print(f"   Cong vach AC-01: + {B.AC_WALL:.0f} = {S['SCAL_LEFT']+B.AC_WALL:.0f} mm go tong cong")
F_side = 20.0
Zs = B.AC_JOKER[2]*S['SCAL_LEFT']**2/6
Ms = F_side*B.SCAL_D/8
print(f"   Kiem web con lai duoi luc ngang {F_side:.0f} N:")
print(f"     tiet dien {S['SCAL_LEFT']:.0f} x {B.AC_JOKER[2]:.1f}, nhip {B.SCAL_D:.0f}"
      f" -> {Ms/Zs:.2f} MPa, he so {B.MOR/(Ms/Zs):.0f}x")
print(f"   Hom khoet SUOT chieu sau ranh ({B.AC_JOKER[2]:.1f}) de lay duoc ca lop duoi.")
print(f"\n  Luu y bo tri: hom nam giua chieu dai ranh Joker. Ranh Joker nam o giua")
print(f"  be rong AC-01, tuc dung duoi khe rap giua nap. Xem muc 3 — day tung la")
print(f"  cho xung dot voi 'song noi giua', va xung dot do da bien mat.")

# ==========================================================================
hr("3. DO MEP TU DO CUA NAP — kiem lai review §3.2")
span = B.INNER_Y
print(f"  Review Rev B §3.2: hai canh nap gap nhau tren khoang phu kien rong")
print(f"  {S['AC_BAY']:.0f} mm hoan toan rong; nhip ho {span:.0f} mm; 'an tay vao giua")
print(f"  nap la hai dau canh vong xuong va cao vao nhau'.")
print(f"  Luc do mep tu do day 8 mm. Da doi thanh {B.T_SEAM:.0f} mm.\n")
F = 50.0
print(f"  Do doc canh khe giua {B.STILE:.0f} x t, nhip {span:.0f}, tai giua nhip {F:.0f} N")
print(f"  {'day mep':>9s}{'I (mm4)':>11s}{'vong (mm)':>11s}{'uon (MPa)':>11s}{'he so':>8s}")
for t in (8.0, B.T_SEAM):
    I = B.STILE*t**3/12
    dfl = F*span**3/(48*B.E_W*I)
    sig = (F*span/4)/(B.STILE*t**2/6)
    tag = "  <- Rev B" if t == 8.0 else "  <- da chot"
    print(f"  {t:9.0f}{I:11.0f}{dfl:11.2f}{sig:11.1f}{B.MOR/sig:8.0f}{tag}")
print(f"\n  Va khe rap giua da tu {0.6} len {B.SEAM}: hai canh vong XUONG cung chieu,")
print(f"  khe lai nam NGANG — vong khong lam hai canh cao vao nhau.")
print(f"  => Mep tu do KHONG con can chi tiet do. Bo 'song noi giua tren AC-01'.")
print(f"     Chong xoc khay thay bang dem ni {B.FELT_PAD} mm dan duoi nap tren moi khoang.")
print(f"     Rut AC-01 ra: xem muc 2 — kep hai dai go qua hai hom ngon ranh Joker.")

# ==========================================================================
hr("4. NAP CHE O XUC XAC")
n, sock, rib = 2, B.DICE_SOCK, B.DICE_RIB
field = n*sock + (n+1)*rib
print(f"  O xuc xac: {n}x{n} o vuong {sock:.0f} x {sock:.0f} sau {B.DICE_SOCK_D:.0f},"
      f" vach {rib:.0f}")
print(f"  Truong o: {field:.0f} x {field:.0f}  trong hoc {S['AC_DICE_L']:.0f} (dai)"
      f" x {S['AC_W_IN']:.0f} (rong)")
slide_room = S['AC_DICE_L'] - field
print(f"  Cho trong con lai theo chieu dai hoc: {slide_room:.0f} mm\n")
print(f"  'Nap TRUOT' khong lam duoc, va day la ly do bang so:")
print(f"   - Nap phai truot di it nhat {field:.0f} mm de lo het hai hang o.")
print(f"   - Cho de nap truot vao chi co {slide_room:.0f} mm.")
print(f"   - Muon du cho thi hoc xuc xac phai dai {field*2:.0f}, tuc chuoi AC-01 phai")
print(f"     dai them {field*2-S['AC_DICE_L']:.0f} mm — khong con cho, chuoi da khep"
      f" ve {S['AC_L']:.0f}.")
print(f"   - Truot ngang cung khong duoc: cung can {field:.0f} mm hanh trinh, ma theo")
print(f"     phuong ngang chi con {S['AC_W_IN']-field:.0f} mm cho trong.")
cov_w, cov_l = S['AC_W_IN'] + 2*B.COVER_LIP, field
print(f"\n  => NAP THA (drop-in), khong truot:")
for a, b in [("Kich thuoc", f"{cov_w:.0f} x {cov_l:.0f} x {B.COVER_T:.0f} cocobolo"),
             ("Ha bac", f"{B.COVER_LIP:.0f} mm quanh mieng hoc, sau {B.COVER_T:.0f}"
                        f" -> mat nap PHANG voi vanh AC-01"),
             ("Nhac nap", f"hom ban nguyet O20 o mot dau, khoet suot be day"),
             ("Chong xe dich", f"nap tua bon canh vao bac; dem ni {B.FELT_PAD} duoi nap hop"
                               f" ep xuong"),
             ("Tho go", f"chay theo canh {cov_l:.0f} — mieng go {cov_w:.0f} x {cov_l:.0f}"
                        f" x {B.COVER_T:.0f} la mieng nho, phai xe theo tho dai")]:
    print(f"   {a:16s}: {b}")
print(f"\n  Voi phuong an C hop luon duoc be NGANG, nen nap tha la du:")
print(f"  xuc xac chi roi khoi o khi hop bi lat nghieng — luc do ca hai canh nap")
print(f"  cung bung ra (xem tools/handle_option_c.py muc 5), nen nap che khong phai")
print(f"  la tuyen phong thu cuoi cung. No la de xuc xac khong nhay lach cach khi di.")
d_die = 16.0
print(f"\n  Kiem o: xuc xac canh {d_die:.0f} trong o {sock:.0f} sau {B.DICE_SOCK_D:.0f}")
print(f"   khe {sock-d_die:.0f} mm moi chieu; xuc xac nho len {d_die-B.DICE_SOCK_D:.0f} mm")
print(f"   -> nap tha o tren giu lai. Moi o co hom ngon O10 sau 3 de lay xuc xac.")
