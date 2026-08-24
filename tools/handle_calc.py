#!/usr/bin/env python3
"""
Tinh toan thiet ke quai xach cho hop Mahjong 152 quan.
Chay: python3 tools/handle_calc.py
"""
import math

def hr(t): print("\n"+"="*76+"\n"+t+"\n"+"="*76)

# --------------------------------------------------------------- 1. KHOI LUONG
hr("1. KHOI LUONG - con so quyet dinh toan bo thiet ke quai")

# the tich go (mm3), hinh hoc Rev C: 354 x 350 x 67, vach 10, day 8, vach ngan 6
V = {}
V['day']        = 354*350*8
V['vach truoc/sau'] = 2*(354*10*44)           # cao trung binh 44 tren day
V['vach trai/phai'] = 2*(330*10*39)
V['vach ngan']  = 2*(330*6*44)
V['canh nap']   = 2*(176.7*350*13 - 100*330*6)  # nem 18->8, tru long lom lot da
V['khay quan']  = 4*(325*124*19 - 315*114*15)
V['khay phu kien'] = 325*68*38 - (28*152*24.5 + 58*75*18.5 + 58*78*18.5)
Vtot = sum(V.values())
print(f"  {'chi tiet':22s}{'cm3':>10s}")
for k,v in V.items(): print(f"  {k:22s}{v/1000:10.0f}")
print(f"  {'TONG GO':22s}{Vtot/1000:10.0f} cm3")

RHO = {'cocobolo':1.10, 'go trac':1.05, 'loi on dinh + veneer':0.58, 'oc cho/walnut':0.65}
M_TILE = 16.0   # g/quan, quan premium ure/melamine ~1,5 g/cm3
m_tiles = 152*M_TILE/1000
print(f"\n  152 quan x {M_TILE:.0f} g = {m_tiles:.2f} kg   (+ 4 xuc xac ~8 g)")

print(f"\n  {'Cau tao':34s}{'go kg':>9s}{'+quan':>9s}{'TONG kg':>10s}")
SC = [
 ("Toan bo cocobolo dac", {'all':'cocobolo'}),
 ("Than+khay cocobolo, nap loi on dinh", {'canh nap':'loi on dinh + veneer','all':'cocobolo'}),
 ("Than cocobolo, nap+khay loi on dinh", {'canh nap':'loi on dinh + veneer',
                                          'khay quan':'loi on dinh + veneer',
                                          'khay phu kien':'loi on dinh + veneer','all':'cocobolo'}),
]
res={}
for name,mix in SC:
    m=0
    for k,v in V.items():
        rho = RHO[mix.get(k, mix['all'])]
        m += v/1000*rho/1000
    res[name]=m
    print(f"  {name:34s}{m:9.2f}{m_tiles:9.2f}{m+m_tiles:10.2f}")

M_LOW  = min(res.values())+m_tiles
M_HIGH = max(res.values())+m_tiles
print(f"\n  => DAI KHOI LUONG THIET KE: {M_LOW:.1f} - {M_HIGH:.1f} kg")

# --------------------------------------------------------------- 2. TAI THIET KE
hr("2. TAI TRONG THIET KE")
g=9.81
P_static = M_HIGH*g
for k,lbl in [(1,"tinh (dung yen)"),(2,"dong (di bo, lac tay)"),(3,"thiet ke - he so 3"),
              (4,"kiem chung roi/giat manh")]:
    print(f"  he so {k}  {lbl:26s} {M_HIGH*k:6.1f} kg = {P_static*k:7.0f} N")
P_DES = P_static*3
print(f"\n  => TAI THIET KE P = {P_DES:.0f} N  (chia deu 2 diem neo: {P_DES/2:.0f} N/diem)")
print(f"  => Yeu cau kiem chung: treo {M_HIGH*4:.0f} kg trong 60 s + 5.000 chu ky nhac")

# --------------------------------------------------------------- 3. ECGONOMI
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
CGx, CGy = 354/2, 350/2
print(f"  Trong tam hop (doi xung 2 truc): X = {CGx:.0f} , Y = {CGy:.0f}")
print(f"  => Tam nam tay PHAI o X=177, Y=175  (dung khe rap giua nap, giua chieu sau)")
print(f"  Neu dat quai tren vach truoc (Y=0): lech {CGy:.0f} mm -> hop treo doc (dang cap ta-i)")
print(f"     => nap o phuong thang dung, canh nap tu bung ra, xuc xac roi khoi o.")
print(f"  Neu dat quai tai X=177,Y=175       : hop treo NGANG, khay nam yen trong khoang.")

# --------------------------------------------------------------- 5. DUONG TRUYEN LUC
hr("5. DUONG TRUYEN LUC - vi sao khong treo vao ban le")
print("  Cac diem CO THE neo tren mat tren cua hop:")
anchors = [("Vach trai/phai (X=0-10, 344-354)", "KHONG - 314/350 mm da la mat mong ban le"),
           ("Vach truoc/sau (Y=0-10, 340-350)", "CO   - lien khoi voi day, chiu luc tot"),
           ("2 vach ngan (X=136-142, 212-218)", "CO nhung chi cach nhau 76 mm - qua hep de nam"),
           ("Canh nap", "KHONG truc tiep - canh xoay tu do, se bung ra")]
for a,b in anchors: print(f"   - {a:36s} {b}")
print(f"\n  => Hai diem neo duy nhat dung tam la dinh vach TRUOC va SAU tai X=177.")
print(f"     Khoang cach 2 diem neo: {350-2*4:.0f} mm (tam neo Y=4 va Y=346)")

# --------------------------------------------------------------- 6. SONG KHOA
hr("6. SONG KHOA (spine) - kiem ben")
L_span, a_load = 342.0, 117.0     # 2 toggle cach 342 ; 2 diem treo strap cach 120
b, h = 44.0, 20.0                 # tiet dien song
rec_w, rec_t = 32.0, 10.0         # hoc chua quai: rong 32, con day 10
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
MOR = 110.0
print(f"  MOR cocobolo ~{MOR:.0f} MPa  ->  he so an toan = {MOR/(M/Z_u):.0f}")
E_w = 13000.0
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
ac_new = 325 - 2*boss_in
print(f"  a) Vach truoc/sau day len 10 -> 20 tai bang X=155..199 (+{boss_out:.0f} ra ngoai, +{boss_in:.0f} vao trong)")
print(f"     Phu bi Y qua 2 tru: 350 + 2 x {boss_out:.0f} = {350+2*boss_out:.0f} mm")
print(f"  b) Khay phu kien AC-01: {325:.0f} -> {ac_new:.0f} mm")
for jl,dice,aux in [(152,65,80),(152,60,85)]:
    tot = 5+jl+5+dice+5+aux+5
    ok = "OK " if abs(tot-ac_new)<0.01 else "khong khop"
    print(f"     5+{jl}+5+{dice}+5+{aux}+5 = {tot}  {ok}")
print(f"     (o xuc xac 2x2 can ~51 ; hoc quan du phong 2x2 can ~74)")
print(f"  c) Nap: doi vat 18->8 thanh 18->12  (goc {math.degrees(math.atan(6/176.7)):.3f} do)")
print(f"     -> phay duoc hoc song 4 sau ; dong thoi bo duoc canh dao 8 mm de sut")
print(f"  d) Chieu cao: 67 + song noi {h-4:.0f} (am 4 vao nap) = {67+h-4:.0f} mm phu bi")
print(f"  e) O xuc xac phai co NAP TRUOT - khi xach xuc xac se roi khoi o")

# --------------------------------------------------------------- 10. KET LUAN
hr("10. KET LUAN VE KHOI LUONG")
print(f"  {M_HIGH:.1f} kg mot tay la NANG. Moc so sanh:")
for m,lbl in [(5.0,"gioi han hanh ly xach tay thoai mai"),
              (7.0,"cap laptop day - xach duoc 2-3 phut"),
              (10.0,"nguong khuyen cao xach mot tay lien tuc")]:
    print(f"    {m:4.1f} kg  {lbl}")
print(f"\n  Giam can bang VAT LIEU, khong phai bang thiet ke quai:")
for name,m in res.items():
    print(f"    {m+m_tiles:5.2f} kg  {name}")
print(f"  => Chenh {M_HIGH-M_LOW:.1f} kg giua cau tao dac va cau tao loi on dinh.")
print(f"     Loi on dinh dang nao cung BAT BUOC cho canh nap (xem review Rev B, muc 5).")
