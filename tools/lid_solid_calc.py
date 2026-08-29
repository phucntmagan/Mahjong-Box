#!/usr/bin/env python3
"""
Phuong an nap go dac: khung cocobolo + tam Nu go do THA trong ranh.
Moi tri so hinh hoc lay tu tools/box_spec.py.
Chay: python3 tools/lid_solid_calc.py
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B
def hr(t): print("\n"+"="*78+"\n"+t+"\n"+"="*78)

S = B.derive()

# --------------------------------------------------- he so gian no (%/1% MC)
K_LONG  = B.K['doc tho']              # doc tho - gan nhu bang 0
K_TANG  = B.K['cocobolo ngang tho']   # ngang tho, do doc khung cocobolo
K_BURL  = B.K['Nu moi phuong']        # NU: tho xoan loan, khong huong -> deu moi phuong
K_CORE  = B.K['loi on dinh']          # loi on dinh (ply/MDF) + veneer

hr("1. TAI SAO NAP KHONG THE LA MOT TAM NU DAC — chuoi mat mong")
PITCH, KLEN = B.KN_PITCH, B.KN_LEN
GAP = PITCH - KLEN
K = [((n-1)*PITCH, (n-1)*PITCH+KLEN, 'THAN' if n%2 else 'NAP')
     for n in range(1, B.N_KN+1)]
RUN = (B.N_KN-1)*PITCH + KLEN
CTR = RUN/2
print(f"  7 mat mong xen ke, buoc {PITCH:.0f}, dai {KLEN:.0f}, khe doc truc {GAP:.1f}. Chuoi {RUN:.0f} mm.")
print(f"  Than = go dac thang tho, tho chay doc canh {B.LID_L:.0f} -> mat mong THAN dung yen.")
print(f"  Canh nap no deu quanh tam chuoi ({CTR:.0f} mm). Mat mong NAP truot doc truc.\n")

def min_gap(k_mat):
    """Khe doc truc nho nhat con lai khi vat lieu canh nap gian he so k_mat"""
    best=None
    for i in range(B.N_KN-1):
        a0,b0,t0 = K[i]; a1,b1,t1 = K[i+1]
        e0 = b0 if t0=='THAN' else CTR + (b0-CTR)*(1+k_mat)
        e1 = a1 if t1=='THAN' else CTR + (a1-CTR)*(1+k_mat)
        g = e1 - e0
        best = g if best is None or g < best else best
    return best

print(f"  {'Cau tao canh nap':24s}{'he so':>8s}{'dMC 2%':>9s}{'dMC 3%':>9s}{'dMC 4%':>9s}{'dMC 5%':>9s}")
for lbl,k in [("Tam Nu dac", K_BURL), ("Khung go dac (doc tho)", K_LONG), ("Loi on dinh + veneer", K_CORE)]:
    row = "".join(f"{min_gap(k*m):9.2f}" for m in (2,3,4,5))
    print(f"  {lbl:24s}{k*100:7.2f}%{row}")
print(f"  (gia tri = khe con lai, mm. Am = mat mong CHONG NHAU -> ban le ket cung)")

# nguong dMC lam khe = 0
half = CTR - K[1][0]     # khoang cach tu tam den mep ngoai cung cua mat mong NAP
eps_crit = GAP/half
print(f"\n  Khe dong hoan toan khi vat lieu gian eps = {GAP:.1f}/{half:.0f} = {eps_crit*100:.3f}%")
print(f"    Nu dac      : dMC nguong = {eps_crit/K_BURL:.1f} %   <- xuong ket cung")
print(f"    Khung go dac: dMC nguong = {eps_crit/K_LONG:.0f} %   <- khong bao gio toi")
print(f"\n  Xuong lam o 9% MC, mua nong am mien Bac/Nam len 13% -> dMC = 4%.")
print(f"  => Nap Nu DAC ket ban le dung o dieu kien su dung binh thuong.")
print(f"  Truoc khi ket, khe tut tu 1,00 xuong {min_gap(K_BURL*3):.2f} mm o dMC 3% -> ma sat, ket rit, mon son.")

print(f"\n  Van de thu hai, khong tinh duoc bang so:")
print(f"   - Mat mong la ong go thanh {B.R_KN-B.D_PIN/2:.1f} mm quanh lo O{B.D_PIN}, dai {KLEN:.0f}.")
print(f"   - Go thang tho: tho chay doc truc mong -> ben. Nu: tho xoan loan, khong co")
print(f"     huong nao dam bao, lai hay co loi vo/lo rong -> mat mong co the tach.")
print(f"   - Khong the thiet ke chi tiet 5,8 mm thanh mong theo mot ung suat cho phep")
print(f"     nao ca, vi Nu khong co tri so cho phep on dinh.")
print(f"  ==> Canh ban le BAT BUOC la go dac thang tho. Tuc la KHUNG + TAM THA.")

hr("2. KHUNG + TAM THA (frame & panel) — dung nhu anh mau")
LW, LL = S['LW'], B.LID_L
ST_H = ST_S = B.STILE
RAIL = B.RAIL
op_w, op_l = S['OP_W'], S['OP_L']
GRV, TON = B.GRV, B.TON
pan_w, pan_l = S['PAN_W'], S['PAN_L']
print(f"  Do doc canh mong {ST_H:.0f} | Do doc canh khe giua {ST_S:.0f} | Do ngang {RAIL:.0f}")
print(f"  Long khung        : {op_w:.1f} x {op_l:.1f}")
print(f"  Tam Nu            : {pan_w:.1f} x {pan_l:.1f} x day {B.PAN_T:.0f}   (canh an {TON:.0f} vao ranh sau {GRV:.0f})")
print(f"  Khong gian tha    : {GRV-TON:.0f} mm moi phia\n")
print(f"  {'Chuyen vi can nuot':28s}{'dMC 2%':>9s}{'dMC 3%':>9s}{'dMC 5%':>9s}{'cho phep':>10s}")
for lbl, dim in [("Tam Nu theo be rong", pan_w), ("Tam Nu theo chieu dai", pan_l)]:
    d=[dim*K_BURL*m/2 for m in (2,3,5)]
    ok = "OK" if d[2] <= (GRV-TON) else "THIEU"
    print(f"  {lbl:28s}{d[0]:9.2f}{d[1]:9.2f}{d[2]:9.2f}{GRV-TON:9.1f}  {ok}")
print(f"  (chia 2 vi tam tha deu ve hai phia - CHI dan/chot tam o DUNG TAM)")

print(f"\n  --- DAY TAM Nu KHONG PHAI TU DO CHON ---")
print(f"  Khung VAT, nen cho mong nhat cua no la mep trong do doc canh khe giua")
print(f"  (x = {S['LW']-B.STILE:.2f}), day chi con {S['t_lid'](S['LW']-B.STILE):.2f} mm.")
print(f"  Ranh om tam an vao do: lip TREN {B.S_TOP:.0f} + ranh {B.GRV_W:.0f} + lip DUOI.\n")
print(f"  {'day tam':>9s}{'lip tren':>10s}{'ranh':>7s}{'lip DUOI':>10s}   ket qua")
for pt in (10.0, 9.0, 8.0, 7.0):
    lip = S['t_lid'](S['LW']-B.STILE) - B.S_TOP - pt
    print(f"  {pt:9.0f}{B.S_TOP:10.1f}{pt:7.0f}{lip:10.2f}   "
          f"{'KHONG LAM DUOC' if lip < 2.0 else 'dat'}")
print(f"\n  Ban truoc chot tam {10:.0f} mm: lip duoi con "
      f"{S['t_lid'](S['LW']-B.STILE)-B.S_TOP-10:.2f} mm — mot loi tiem an, khong phay duoc.")
print(f"  Tam {B.PAN_T:.0f} mm cho lip duoi {S['LIP_BOT']:.2f} mm. Do la ly do KY THUAT de")
print(f"  chot {B.PAN_T:.0f}, khong phai ly do giam can (giam can chi la phan thuong).")
print(f"  He qua: canh tam KHONG bi phay bac — ranh rong dung bang day tam ({B.GRV_W:.0f}).")
print(f"  Tot cho Nu: mot bac 1,5 mm tren canh tam tho xoan loan la cho nut.")

hr("3. KHE RAP GIUA NAP")
print(f"  Be rong canh nap = do {ST_H:.0f} + long {op_w:.1f} (THA) + do {ST_S:.0f}")
print(f"  Chi hai thanh do nam trong chuoi kich thuoc -> tam Nu khong dong gop gi.\n")
print(f"  {'Cau tao':26s}{'dMC 2%':>9s}{'dMC 3%':>9s}{'dMC 5%':>9s}")
for lbl,k,dim in [("Nu dac ca tam", K_BURL, LW),
                  ("Khung + tam tha", K_TANG, ST_H+ST_S),
                  ("Loi on dinh + veneer", K_CORE, LW)]:
    d=[2*dim*k*m for m in (2,3,5)]     # x2 vi hai canh cung no vao khe
    print(f"  {lbl:26s}{d[0]:9.2f}{d[1]:9.2f}{d[2]:9.2f}")
print(f"\n  Khe Rev B 0,6 mm. Voi khung+tam: can >= {2*(ST_H+ST_S)*K_TANG*5:.2f} mm o dMC 5%.")
print(f"  => CHOT khe rap giua {B.SEAM} +/-0,3.")
if S['HANDLE'] == 'A':
    print(f"     Song khoa {B.SPINE_W:.0f} rong phu kin khe nen KHONG lo.")
else:
    print(f"     Phuong an C bo song khoa -> khe {B.SEAM} mm LO RA tren mat nap, chay suot")
    print(f"     {LL:.0f} mm. Day la mot khe co chu dinh, phai vat canh deu hai ben va ghi")
    print(f"     vao QA nhu mot dac tinh nhin thay, khong phai dung sai lap ghep.")

hr("4. KHAY BO BAI HINH THANH MIEN PHI")
t_h, t_s, PAN_T = B.T_HINGE, B.T_SEAM, B.PAN_T
print(f"  Khung day {t_h:.0f} tai mong -> {t_s:.0f} tai khe giua; tam Nu day {PAN_T:.0f},")
print(f"  dat thut {B.S_TOP:.0f} mm duoi mat tren khung (lip {B.S_TOP:.0f} la be mat nhin thay).")
print(f"  => Mat duoi tam Nu cao hon mat duoi khung:")
print(f"     tai canh mong    : {t_h-B.S_TOP-PAN_T:.0f} mm sau")
print(f"     tai canh khe giua: {t_s-B.S_TOP-PAN_T:.0f} mm sau")
print(f"  Long lom {op_w:.1f} x {op_l:.0f} nay CHINH LA khay bo bai trong anh mau -")
print(f"  khong phai phay them, khong dinh toi van de 'khong phay duoc long o mep 8 mm'.")

hr("5. KHOI LUONG — cau hinh da chot")
print("  Khung nap = COCOBOLO (dong mau than). Chi tam nap la Nu go do.\n")
print(f"  {'Cau tao khay':16s}{'go kg':>8s}{'+quan':>8s}{'TONG kg':>9s}{'tai TK':>9s}")
for khay in ('cocobolo','loi on dinh'):
    go,t,tot = B.mass_of(S, khay)
    print(f"  {khay:16s}{go:8.2f}{t:8.2f}{tot:9.2f}{tot*9.81*B.DYN:8.0f} N")

hr("5b. MONG KHUNG BANG COCOBOLO — rui ro lon nhat cua phuong an nay")
print("  Khung nap la ket cau 4 mong moi canh, 8 mong ca bo, giu tam Nu va mang mat mong.")
print("  Cocobolo la mot trong nhung loai KHO DAN NHAT: chat chiet xuat (quinone) thoi")
print("  len be mat vua gia cong trong vong vai phut va chan ket dinh.\n")
for a_,b_ in [("Keo","EPOXY, khong dung PVA. PVA tren cocobolo la kieu hong da biet."),
              ("Lau dau","Acetone hoac cong nghiep, lau NGAY truoc khi ep - trong vong 15 phut"),
              ("",  "ke tu khi phay xong ma mong. Lau xong khong cham tay vao mat dan."),
              ("Chot khoa","Chot go Ø5 XUYEN mong, khoan lech 0,8 mm (draw-bore)."),
              ("",  "Muc dich KHONG phai chiu tai - moi mong chi chiu ~20 N - ma la"),
              ("",  "de khung khong bung neu duong keo hong sau vai mua."),
              ("Kiem tra","Ep thu 1 mong mau, de 7 ngay roi pha huy. Duong pha phai di qua"),
              ("",  "THO GO, khong duoc di doc duong keo.")]:
    print(f"   {a_:11s} {b_}" if a_ else f"   {'':11s} {b_}")
print("\n  Neu khong lam duoc quy trinh nay o xuong: chuyen khung nap sang go do")
print("  (de dan hon nhieu) va chap nhan lech mau o mep nap.")

hr("6. TAM NU - YEU CAU MUA VA XU LY")
print(f"  Can 2 tam da lang {pan_w:.0f} x {pan_l:.0f} x 12 (de bao {PAN_T:.0f}), lat sach book-match")
print(f"  => khoi Nu tho toi thieu ~{pan_w+40:.0f} x {pan_l+40:.0f} x 40 de xe duoc 2 lat lien tiep")
for a,b in [("On dinh hoa","ngam nhua chan khong (vacuum stabilise) truoc khi gia cong tinh"),
            ("Mat/loi vo","tram epoxy trong hoac epoxy + bot chinh go, tram TRUOC khi cha tinh"),
            ("Chieu day",f"{B.PAN_T:.0f} mm — chot theo lip ranh (muc 2), khong phai chon tuy y"),
            ("Dan tam","CHI dan/chot mot diem o DUNG TAM moi canh; tuyet doi khong dan quanh ranh"),
            ("Hoan thien","Nu hut khong deu -> phai bit lo (grain filler) roi moi phu")]:
    print(f"   - {a:12s}: {b}")

hr("7. NAP TRONG PHUONG AN C — CAI GI GIU, CAI GI BO")
print("  GIU:")
for t in [f"Khung go dac om tam Nu tha — ly do (muc 1) khong dinh gi toi phuong an xach",
          f"Vat nap {B.T_HINGE:.0f} -> {B.T_SEAM:.0f}, goc {S['ANG']:.3f} do tren doan vat {S['TAPER']:.2f}",
          f"Khe rap giua {B.SEAM} +/-0,3",
          f"Khay bo bai sinh ra mien phi tu chenh day khung va tam",
          f"Quy trinh epoxy + acetone 15 phut + chot draw-bore O5 cho 8 mong khung"]:
    print(f"   - {t}")
print("\n  BO (theo phuong an C):")
for t in ["Ranh am 4 x 21,25 tren do doc canh khe giua cho song khoa",
          "Hoc ban nguyet R8,5 o dau moi canh cho chot xoay O16",
          "Song khoa 44 x 20 va quai da"]:
    print(f"   - {t}")
print("\n  HE QUA phai xu ly o cho khac:")
print(f"   ! Khe rap giua {B.SEAM} mm nay LO RA, khong con song khoa che.")
print(f"   ! Mep tu do cua nap khong con song khoa do -> song noi giua tren AC-01")
print(f"     (rong {B.RIB_W:.0f}, cao {S['Z_SEAM']-(S['Z_FLOOR']+B.AC_H):.0f} tu dinh khay len mat duoi nap).")
print(f"   ! Khoa nap chua co loi giai. Xem tools/handle_option_c.py muc 5.")
print(f"\n  Phu bi {S['W']:.0f} x {S['Y_OA']:.0f} x {S['Z_OA']:.0f}")

hr("8. PHAP LY - PHAI TU XAC MINH")
print("  Go do = Afzelia xylocarpa. IUCN: Endangered.")
print("  CoP18 (2019) dua Afzelia spp. QUAN THE CHAU PHI vao Phu luc II CITES.")
print("  Loai chau A (A. xylocarpa) va quy dinh Nhom IIA trong nuoc cua Viet Nam la hai")
print("  chuyen KHAC NHAU va co the da thay doi. Tao viet theo tri nho.")
print("  => BAT BUOC xac minh voi Co quan quan ly CITES VN + Chi cuc Kiem lam truoc khi mua.")
print("     Cong voi cocobolo (Dalbergia, Phu luc II) - hop nay co HAI loai can kiem tra.\n")
print("  Khung nap cocobolo lam TANG go Dalbergia moi hop:")
print(f"  {'Cau tao khay':16s}{'Dalbergia/hop':>15s}{'so hop toi da / lo':>21s}")
for khay in ('cocobolo','loi on dinh'):
    d=B.dalbergia_of(S, khay)
    print(f"  {khay:16s}{d:15.2f}{int(B.CITES_LIMIT//d):21d}")
print("  (theo nguong mien tru 10 kg cua annotation #15 - PHAI xac minh lai)")
