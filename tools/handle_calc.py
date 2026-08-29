#!/usr/bin/env python3
"""
Thiet ke quai xach — PHUONG AN A (song khoa cocobolo + quai da, xach mot tay).

  A DA BI LOAI ngay 29-08-2026, thay bang phuong an C (hoc am hai tay).
  Giu lai script nay lam ho so: no la co so cua cac tri so tung duoc chot
  (song 44 x 20, chot xoay O16, tru vach, vat nap 18 -> 12, khe rap giua 1,5)
  va mot so trong do van song sang C. So sanh A <-> C: tools/handle_option_c.py

Chay: python3 tools/handle_calc.py
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B

A = B.derive(handle='A')      # moi hinh hoc duoi day la cua phuong an A
VA = A['V']

def hr(t): print("\n"+"="*76+"\n"+t+"\n"+"="*76)

# --------------------------------------------------------------- 1. KHOI LUONG
hr("1. KHOI LUONG - con so quyet dinh toan bo thiet ke quai")
print("  Cau hinh da chot: than + khay + khung nap + song khoa = COCOBOLO,")
print("  tam nap = NU GO DO tha trong ranh. Xem tools/box_spec.py.\n")
print(f"  {'chi tiet':18s}{'cm3':>9s}{'kg':>8s}   vat lieu")
mat={'tam Nu':'Nu go do'}
for k,v in VA.items():
    r = B.RHO[mat.get(k,'cocobolo')]
    print(f"  {k:18s}{v/1000:9.0f}{v/1e6*r:8.2f}   {mat.get(k,'cocobolo')}")
print(f"\n  {'Cau tao khay':16s}{'go kg':>8s}{'+quan':>8s}{'TONG kg':>9s}{'Dalbergia/hop':>15s}")
for khay in ('cocobolo','loi on dinh'):
    go,t,tot = B.mass_of(A, khay)
    print(f"  {khay:16s}{go:8.2f}{t:8.2f}{tot:9.2f}{B.dalbergia_of(A, khay):15.2f}")
M_HIGH = B.mass_of(A,'cocobolo')[2]
M_LOW  = B.mass_of(A,'loi on dinh')[2]
print(f"\n  => DAI KHOI LUONG THIET KE: {M_LOW:.2f} - {M_HIGH:.2f} kg")

hr("2. TAI TRONG THIET KE")
g=9.81
P_static = M_HIGH*g
for k,lbl in [(1,"tinh (dung yen)"),(2,"dong (di bo, lac tay)"),(3,"thiet ke - he so 3"),
              (4,"kiem chung roi/giat manh")]:
    print(f"  he so {k}  {lbl:26s} {M_HIGH*k:6.1f} kg = {P_static*k:7.0f} N")
P_DES = M_HIGH*9.81*B.DYN
print(f"\n  => TAI THIET KE P = {P_DES:.0f} N  (chia deu 2 diem neo: {P_DES/2:.0f} N/diem)")
print(f"  => Yeu cau kiem chung: treo {M_HIGH*4:.0f} kg trong 60 s + 5.000 chu ky nhac")

hr("3. EC-GO-NO-MI TAY NAM  (tai >4,5 kg => quy dinh khac han tui nhe)")
E = [("Chieu dai nam tay thong (clear)", "110 - 130 mm", "ban tay nam 95-100 mm + du 15"),
     ("Tiet dien nam",                   "30 x 18 mm oval", "tai nang can BE MAT RONG, khong tron nho"),
     ("Ban kinh canh nam",               "R >= 8 mm",       "canh sac cat tay o 7 kg"),
     ("Khe long ngon tay duoi nam",      ">= 45 mm",        "du 4 ngon luon vao"),
     ("Do lech tam cho phep",            "<= 15 mm",        "lech hon la hop nghieng khi xach")]
print(f"  {'Thong so':34s}{'Gia tri':20s}Ly do")
for a,b,c in E: print(f"  {a:34s}{b:20s}{c}")

# --------------------------------------------------------------- 4. CAN BANG
hr("4. VI TRI QUAI - DIEU KIEN HOP TREO THANG BANG")
CGx, CGy = A['W']/2, A['Y_BODY']/2
print(f"  Trong tam hop (doi xung 2 truc): X = {CGx:.0f} , Y = {CGy:.0f}")
print(f"  => Tam nam tay PHAI o X={CGx:.0f} , Y={CGy:.0f}  (dung khe rap giua nap, giua chieu sau)")
print(f"  Neu dat quai tren vach truoc (Y=0): lech {CGy:.0f} mm -> hop treo doc")
print(f"     => nap o phuong thang dung, canh nap tu bung ra, xuc xac roi khoi o.")
print(f"  Neu dat quai tai X=177,Y=175       : hop treo NGANG, khay nam yen trong khoang.")

# --------------------------------------------------------------- 5. DUONG TRUYEN LUC
hr("5. DUONG TRUYEN LUC - vi sao khong treo vao ban le")
print("  Cac diem CO THE neo tren mat tren cua hop:")
x_d0 = A["WALL_HINGE"] + A["BAY"]
anchors = [(f"Vach trai/phai (X=0-{A['WALL_HINGE']:.0f}, {A['W']-A['WALL_HINGE']:.0f}-{A['W']:.0f})", f"KHONG - vach nay mang hoc am hai tay va mortise ban le"),
           (f"Vach truoc/sau (Y=0-{B.WALL_FB:.0f}, {A['Y_BODY']-B.WALL_FB:.0f}-{A['Y_BODY']:.0f})", "CO   - lien khoi voi day, chiu luc tot"),
           (f"2 vach ngan (X={x_d0:.0f}-{x_d0+A['DIV']:.0f}, {A['W']-x_d0-A['DIV']:.0f}-{A['W']-x_d0:.0f})", f"CO nhung chi cach nhau {A['AC_BAY']:.0f} mm - qua hep de nam"),
           ("Canh nap", "KHONG truc tiep - canh xoay tu do, se bung ra")]
for a,b in anchors: print(f"   - {a:36s} {b}")
print(f"\n  => Hai diem neo duy nhat dung tam la dinh vach TRUOC va SAU tai X=177.")
print(f"     Khoang cach 2 diem neo: {A['Y_OA']-2*4:.0f} mm (tam neo Y=4 va Y={A['Y_OA']-4:.0f})")

# --------------------------------------------------------------- 6. SONG KHOA
hr("6. SONG KHOA (spine) - kiem ben")
L_span, a_load = A['Y_OA']-2*4, 117.0   # 2 toggle cach ca chieu sau tru 2 x 4
b, h = B.SPINE_W, B.SPINE_T       # tiet dien song
rec_w, rec_t = B.SPINE_REC[1], B.SPINE_REC[2]   # hoc chua quai: rong, con day
P = P_DES
# tiet dien tai hoc: 2 gon ben (b-rec_w)/2 x h  +  day rec_w x rec_t
def I_rec():
    bs = (b-rec_w)/2
    I_sides = 2*(bs*h**3/12)
    yc_floor = h - rec_t/2          # truc trung hoa xap xi giua tiet dien
    # tinh chinh xac: truc trung hoa cua tiet dien chu U nguoc
    A1 = 2*bs*h; y1 = h/2
    A2 = rec_w*rec_t; y2 = rec_t/2
    yb = (A1*y1+A2*y2)/(A1+A2)
    I = 2*(bs*h**3/12 + bs*h*(y1-yb)**2) + (rec_w*rec_t**3/12 + rec_w*rec_t*(y2-yb)**2)
    return I, yb
I_u, yb = I_rec()
c = max(yb, h-yb)
Z_u = I_u/c
Z_full = b*h**2/6
M = (P/2)*((L_span-120)/2)        # 2 tai P/2 tai +-60 quanh tam, goi 2 dau
print(f"  Song {b:.0f} x {h:.0f}, nhip 2 toggle {L_span:.0f}, 2 diem treo cach 120")
print(f"  Momen lon nhat M = (P/2) x {(L_span-120)/2:.0f} = {M:.0f} N.mm")
print(f"  Tiet dien dac      Z = {Z_full:7.0f} mm3  ->  sigma = {M/Z_full:5.1f} MPa")
print(f"  Tiet dien tai hoc  Z = {Z_u:7.0f} mm3  ->  sigma = {M/Z_u:5.1f} MPa   (truc trung hoa yb={yb:.1f})")
MOR = B.MOR
print(f"  MOR cocobolo ~{MOR:.0f} MPa  ->  he so an toan = {MOR/(M/Z_u):.0f}")
E_w = B.E_W
delta = (P/2)*a_load*(3*L_span**2-4*a_load**2)/(24*E_w*I_u)
print(f"  Vong o giua: {delta:.2f} mm  (yeu cau < L/300 = {L_span/300:.2f} mm)  "
      f"{'OK' if delta < L_span/300 else 'KHONG DAT - tang h'}")

# --------------------------------------------------------------- 7. CHOT XOAY 1/4
hr("7. CHOT XOAY 1/4 VONG (turn-key) - kiem ben")
Pk = P_DES/2
d_key, t_tongue, w_tongue = 16.0, 8.0, 26.0
eng = (w_tongue - 10.0)/2          # moi ben tongue an vao go bao nhieu
A_shear = 2*(t_tongue*eng)
A_bear  = 2*(eng*10.0)
print(f"  Moi chot chiu {Pk:.0f} N")
print(f"  Luoi ngang {w_tongue:.0f} x {t_tongue:.0f}, an moi ben {eng:.0f} mm")
print(f"  Cat qua luoi   : A={A_shear:5.0f} mm2 -> {Pk/A_shear:4.2f} MPa  (cho phep ~14 MPa go cung)")
print(f"  Ep mat go dai  : A={A_bear:5.0f} mm2 -> {Pk/A_bear:4.2f} MPa  (cho phep ~10 MPa ngang tho)")
print(f"  Than chot Ø{d_key:.0f} cat: A={math.pi*d_key**2/4:5.0f} mm2 -> {Pk/(math.pi*d_key**2/4):4.2f} MPa")
print(f"  => He so an toan thap nhat ~ {min(14/(Pk/A_shear), 10/(Pk/A_bear)):.0f}x. Go du suc.")
print(f"  Diem yeu THUC SU: mon lo sau 5.000 chu ky, khong phai ben tuc thoi.")
print(f"     -> lot o chot bang go rat cung (grenadille/lignum) hoac sung/xa cu, boi sap.")

# --------------------------------------------------------------- 8. QUAI DA
hr("8. QUAI DA (phuong an A) - kiem ben")
w_s, t_s = 30.0, 4.0
A_s = 2*(w_s*t_s)
print(f"  Da bo bridle {w_s:.0f} x {t_s:.0f}, gap doi -> A = {A_s:.0f} mm2")
print(f"  Ung suat keo = {P_DES/A_s:.2f} MPa   (da bo ~20-25 MPa)  -> he so {20/(P_DES/A_s):.0f}x")
n_st, F_st = 8, 90.0
print(f"  Duong chi khoa: {n_st} mui x {F_st:.0f} N/mui = {n_st*F_st:.0f} N  vs {P_DES:.0f} N  "
      f"-> he so {n_st*F_st/P_DES:.1f}x")
print(f"  Khe luon da qua song: {w_s+2:.0f} x {t_s+2:.0f}, bo tron R3 (canh sac se cat da)")

# --------------------------------------------------------------- 9. TAC DONG DAY CHUYEN
hr("9. TAC DONG DAY CHUYEN - nhung gi phai doi theo")
boss_out, boss_in = 6.0, 4.0
ac_new = B.TRAY[0] - 2*boss_in
print(f"  a) Vach truoc/sau day len {B.WALL_FB:.0f} -> {B.WALL_FB+boss_out+boss_in:.0f} tai bang "
      f"X={A['X_SEAM']-B.POST_W/2:.0f}..{A['X_SEAM']+B.POST_W/2:.0f} (+{boss_out:.0f} ra ngoai, +{boss_in:.0f} vao trong)")
print(f"     Phu bi Y qua 2 tru: {A['Y_BODY']:.0f} + 2 x {boss_out:.0f} = {A['Y_OA']:.0f} mm")
print(f"  b) Khay phu kien AC-01: {325:.0f} -> {ac_new:.0f} mm")
for jl,dice,aux in [(152, A['AC_DICE_L'], B.AC_AUX_L),(152, A['AC_DICE_L']-5, B.AC_AUX_L+5)]:
    tot = 5+jl+5+dice+5+aux+5
    ok = "OK " if abs(tot-A["AC_Y"])<0.01 else "khong khop"
    print(f"     5+{jl}+5+{dice:.0f}+5+{aux:.0f}+5 = {tot:.0f}  {ok}  (phai khep ve {A['AC_Y']:.0f})")
print(f"     (o xuc xac 2x2 can ~51 ; hoc quan du phong 2x2 can ~74)")
print(f"  c) Nap: doi vat {B.T_HINGE:.0f}->8 thanh {B.T_HINGE:.0f}->{B.T_SEAM:.0f}  "
      f"(goc {A['ANG']:.3f} do, tinh tren doan vat that {A['TAPER']:.2f})")
print(f"     -> phay duoc hoc song 4 sau ; dong thoi bo duoc canh dao 8 mm de sut")
print(f"  d) Chieu cao: {A['Z_LID']:.0f} + song noi {A['Z_PROUD']:.0f} "
      f"(am {B.SPINE_INSET:.0f} vao nap) = {A['Z_OA']:.0f} mm phu bi")
print(f"  e) O xuc xac phai co NAP TRUOT - khi xach xuc xac se roi khoi o")

# --------------------------------------------------------------- 10. KET LUAN
hr("10. KET LUAN VE KHOI LUONG")
print(f"  {M_HIGH:.2f} kg mot tay la NANG. Moc so sanh:")
for m,lbl in [(5.0,"gioi han hanh ly xach tay thoai mai"),
              (7.0,"cap laptop day - xach duoc 2-3 phut"),
              (10.0,"nguong khuyen cao xach mot tay lien tuc")]:
    print(f"    {m:4.1f} kg  {lbl}")
print(f"\n  Chot khung nap bang cocobolo (dong mau than) day khoi luong len {M_HIGH:.2f} kg.")
print(f"  Don bay duy nhat con lai la KHAY:")
for khay in ('cocobolo','loi on dinh'):
    print(f"    khay {khay:12s} -> {B.mass_of(A, khay)[2]:.2f} kg")
print(f"  => Chenh {M_HIGH-M_LOW:.2f} kg. Khong con don bay nao khac ma khong doi vat lieu vo.")
print(f"\n  O {M_HIGH:.1f} kg, phuong an C (hoc am hai tay) dang gia can nhac lai:")
print(f"  {M_HIGH/2:.2f} kg moi tay thay vi {M_HIGH:.2f} kg mot tay.")

hr("11. NGUONG MIEN TRU CITES - so hop moi lo hang")
print("  Annotation #15 (theo tri nho, PHAI xac minh): thanh pham <= 10 kg go loai")
print("  liet ke moi lo hang thi duoc mien tru.\n")
print(f"  {'Cau tao khay':16s}{'Dalbergia/hop':>15s}{'2 hop':>9s}{'3 hop':>9s}{'so hop toi da':>15s}")
for khay in ('cocobolo','loi on dinh'):
    d = B.dalbergia_of(A, khay)
    print(f"  {khay:16s}{d:15.2f}{2*d:9.2f}{3*d:9.2f}{int(10//d):15d}")
print("\n  => Khung nap cocobolo day Dalbergia/hop len cao. Neu khay cung cocobolo thi")
print("     mot lo hang chi duoc 2 hop. Khay loi on dinh thi duoc 3.")
print("     Day la ly do THUONG MAI de chon khay loi on dinh, ngoai ly do khoi luong.")
