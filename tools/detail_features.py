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
          f"  mot ben la vach ban le go dac day {S['WALL_HINGE']:.0f} mm,",
          f"  ben kia la vach ngan day {S['DIV']:.0f} mm."]:
    print(f"   - {t}")

print(f"\n  --- LOI GIAI: KHE LUON NGON + MO MOC, o hai DAU khoang ---")
print(f"  Nhac hai tay, moi tay mot dau — dung tinh than cua phuong an C.")
print(f"  Lam cho CA BA khoang (X = {' va '.join(f'{w:.0f}' for w in S['WELL_X'])}).")
print(f"  Ban truoc phai bo khe o khoang phu kien vi hoc am hai tay nam tren cung")
print(f"  vach truoc; nay hoc am da chuyen sang vach trai/phai nen xung dot bien mat,")
print(f"  va AC-01 duoc nhac dung nhu khay quan — khong con phai kep hai dai go")
print(f"  qua hom ngon ranh Joker nua.\n")

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
print(f"     Chong xoc khay thay bang dem ni {B.FELT_PAD:.1f} mm dan duoi nap.")
print(f"     KHONG trai kin: {S['FELT_PAD_N']:.0f} mieng roi {B.FELT_PAD_SZ[0]:.0f} x {B.FELT_PAD_SZ[1]:.0f}.")
print(f"     Khe tren vanh khay {B.CLR_Z:.1f} < ni {B.FELT_PAD:.1f} nen ni bi NEN "
      f"{S['FELT_PRELOAD']:.1f} mm ({S['FELT_STRAIN']*100:.0f} %) va that su ep xuong.")
print(f"     Luc day nguoc len nap: {S['FELT_FORCE']:.0f} N tren {S['FELT_PAD_N']:.0f} mieng, "
      f"= {S['FELT_FORCE']/S['MAG_TOTAL']*100:.0f} % luc hut {S['MAG_TOTAL']:.0f} N cua 8 cap nam cham.")
print(f"     Neu trai ni KIN ca ba khoang ({(2*S['BAY']+S['AC_BAY'])*B.INNER_Y/1e2:.0f} cm2) thi luc do")
print(f"     thanh {(2*S['BAY']+S['AC_BAY'])*B.INNER_Y*B.FELT_SIGMA:.0f} N — nap khong the dong. "
      f"Do la ly do ni phai la mieng roi.")
print(f"     Rut AC-01 ra: khe luon ngon nhu khay quan (muc 1).")

# ==========================================================================
hr("4. O XUC XAC VA NAP CHE  (to AC-02)")
DL = B.dice_layout(S)
sock, rib = B.DICE_SOCK, B.DICE_RIB
field_l, field_w = S['DICE_FIELD_L'], S['DICE_FIELD_W']
print(f"  Mieng hoc: {S['AC_DICE_L']:.0f} (dai) x {S['AC_W_IN']:.0f} (rong), tren khoi dac AC-01.\n")

print("  4.1  BA LOI CUA HINH HOC CU — bat duoc khi ngoi ve to AC-02")
old_cov_l = 2*sock + 3*rib
print(f"   (1) Nap che cu dai {old_cov_l:.0f} = TRUONG O, khong phai MIENG HOC "
      f"{S['AC_DICE_L']:.0f}.")
print(f"       Hai dau nap cach thanh hoc {(S['AC_DICE_L']-old_cov_l)/2:.0f} mm — "
      f"khong tua vao gi, nap roi tot xuong.")
print(f"   (2) O cu sau {B.DICE_SOCK_D:.0f} do TU VANH AC-01, ma nap che an mat "
      f"{B.COVER_T:.0f} tu tren:")
print(f"       cho con lai duoi nap = {B.DICE_SOCK_D - B.COVER_T:.0f} < xuc xac "
      f"{B.DIE:.0f}. Dong nap la ep len xuc xac.")
print(f"   (3) Khong co chi tiet nao lay xuc xac ra. O {sock:.0f} x {sock:.0f} sau "
      f"{B.DICE_SOCK_D:.0f}, quan {B.DIE:.0f},")
print(f"       khe {(sock-B.DIE)/2:.1f} mm moi ben — ngon tay khong luon vao duoc, "
      f"khong co gi de bau.\n")

print("  4.2  GIAI LAI: BA CAO DO PHAY TU MOT MAT CHUAN LA VANH AC-01")
for a, b_ in [("San dat nap che",
               f"sau {B.COVER_T:.0f}, phu HET {S['AC_DICE_L']:.0f} x {S['AC_W_IN']:.0f}"
               f" — khong ha bac vao thanh vach nao"),
              ("Khe luon dau ngon",
               f"sau {DL['slot_d']:.0f} tu vanh, {B.DICE_SLOT:.0f} x {sock:.0f}, "
               f"mot khe canh moi o"),
              ("O xuc xac",
               f"sau {DL['sock_d']:.0f} tu vanh (= {B.DICE_SOCK_D:.0f} ke tu san nap), "
               f"4 o {sock:.0f} x {sock:.0f}")]:
    print(f"   {a:20s}: {b_}")
print(f"   Chuoi dai : {S['DICE_MARG_L']:.0f} + {B.DICE_SLOT:.0f} + {sock:.0f} + {rib:.0f}"
      f" + {sock:.0f} + {B.DICE_SLOT:.0f} + {S['DICE_MARG_L']:.0f} = {S['AC_DICE_L']:.0f}")
print(f"   Chuoi ngang: {S['DICE_MARG_W']:.1f} + {sock:.0f} + {rib:.0f} + {sock:.0f}"
      f" + {S['DICE_MARG_W']:.1f} = {S['AC_W_IN']:.0f}")
print(f"   Vanh do nap che hep nhat: {S['COVER_LEDGE']:.1f} mm (bon canh deu co cho tua)\n")

print("  4.3  VI SAO CO KHE LUON NGON — va vi sao xuc xac khong tut sang do")
print(f"   Dau ngon tay day {B.FING_T_TIP:.0f} mm (cung tri so dung cho hoc am hai tay).")
print(f"   Khe {B.DICE_SLOT:.0f} mm nuot duoc dau ngon; ngon ap vao suon quan roi "
      f"nhac len.")
print(f"   San khe cao hon san o {B.DICE_STEP:.0f} mm. Quan {B.DIE:.0f} chi ho tren dau "
      f"{S['DIE_HEAD']:.0f} mm duoi nap che,")
print(f"   nen no khong the leo qua bac {B.DICE_STEP:.0f} de tut sang khe. Va khe "
      f"{B.DICE_SLOT:.0f} < canh quan {B.DIE:.0f}:")
print(f"   du co bo nap ra lac manh, quan cung khong nam gon trong khe duoc.")
print(f"   Ngon tay cham duoc {S['DIE_GRIP']:.0f} mm chieu cao suon quan.\n")

print("  4.4  'NAP TRUOT' VAN KHONG LAM DUOC — ly do bang so, giu nguyen")
slide_room = S['AC_DICE_L'] - field_l
print(f"   Nap phai truot {field_l:.0f} mm moi lo het hai hang o; cho de nap truot "
      f"vao chi {slide_room:.0f} mm.")
print(f"   Truot ngang can {field_w:.0f} mm ma chi con {S['AC_W_IN']-field_w:.0f} mm.")
print(f"   => NAP THA, {S['COVER_L']:.1f} x {S['COVER_W']:.1f} x {B.COVER_T:.0f} cocobolo.\n")

print("  4.5  NAP THA — kich thuoc, khe lap, hom ngon")
for a, b_ in [("Kich thuoc",
               f"{S['COVER_L']:.1f} x {S['COVER_W']:.1f} x {B.COVER_T:.0f}"
               f"  (mieng hoc tru khe lap {B.COVER_CLR:.1f})"),
              ("Mat tren", "ngang bang vanh AC-01; san phay sau dung be day nap"),
              ("Hom ngon", f"2 hom nua tron O{B.COVER_NOTCH:.0f} tren MOT canh ngan, "
                           f"dat dung tren hai khe luon ngon"),
              ("  voi qua vanh", f"{S['COVER_REACH']:.0f} mm — dau ngon xuong toi khe roi "
                                 f"moc nguoc len mep nap"),
              ("  go con lai", f"giua hai hom {S['COVER_LIG_MID']:.0f}, hai goc "
                               f"{S['COVER_LIG_END']:.2f}"),
              ("Tho go", f"chay theo canh {S['COVER_L']:.1f} — CUNG chieu tho AC-01")]:
    print(f"   {a:16s}: {b_}")
print()
print(f"   Khe lap {B.COVER_CLR:.1f} mm khong phai de gian no o trang thai can bang:")
print(f"   nap che va AC-01 cung loai go, cung chieu tho, nen o can bang hai ben no")
print(f"   bang nhau va khe khong doi. Khe la de chiu QUA DO — mieng go day "
      f"{B.COVER_T:.0f} mm can bang")
print(f"   truoc khoi {B.AC_H:.0f} mm. Bien do qua do: {S['COVER_MOVE']:.2f} mm o "
      f"{B.DMC_DES:.0f} %, {S['COVER_MOVE_DRY']:.2f} mm o {B.DMC_DRY:.0f} %.")
print(f"   Neu xe nap NGANG THO (tho chay theo canh {S['COVER_W']:.1f}) thi bien do "
      f"thanh {S['COVER_L']*B.K['cocobolo ngang tho']*B.DMC_DRY:.2f} mm > khe.\n")

print("  4.6  DAO PHAY — rang buoc it ai nghi toi")
print(f"   O vuong {sock:.0f} phay bang dao tru thi bon goc bo ban kinh = ban kinh dao.")
print(f"   Quan xuc xac canh {B.DIE:.0f} tha vao o {sock:.0f}: goc quan cach vach o "
      f"{(sock-B.DIE)/2:.1f} mm.")
print(f"   Ban kinh bo LON NHAT ma goc quan van lot: R{S['DICE_R_MAX']:.2f}.")
print(f"   => dao O{B.DICE_MILL:.0f} (bo R{S['DICE_R']:.1f}) DUOC; dao O8 (bo R4) thi "
      f"quan kenh goc, khong nam phang.\n")

print("  4.7  KIEM CHIEU CAO — nap che khong duoc nho len")
print(f"   Vanh AC-01 o Z{S['Z_FLOOR']+B.AC_H:.0f}; vanh than o Z{S['Z_RIM']:.0f}; "
      f"khe {S['AC_GAP']:.0f} mm.")
print(f"   Ni dem duoi nap hop day {B.FELT_PAD:.1f} -> nap che duoc phep nho toi da "
      f"{S['COVER_PROUD']:.1f} mm.")
print(f"   Vay dung sai phai MOT CHIEU: san phay sau {B.COVER_T:.0f} +0,15/0 va nap che "
      f"day {B.COVER_T:.0f} 0/-0,10")
print(f"   -> nap luon nam THAP hon vanh 0..0,25 mm, khong bao gio nho len.")
print(f"   Day AC-01 con lai duoi o: {S['AC_DICE_FLR']:.0f} mm.")
