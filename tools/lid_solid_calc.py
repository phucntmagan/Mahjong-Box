#!/usr/bin/env python3
"""
Phuong an nap go dac: khung go do + tam Nu go do (thay cho nap boc da / veneer.)
Chay: python3 tools/lid_solid_calc.py
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B
def hr(t): print("\n"+"="*78+"\n"+t+"\n"+"="*78)

# --------------------------------------------------- he so gian no (%/1% MC)
K_LONG  = 0.0001   # doc tho - gan nhu bang 0
K_TANG  = 0.0015   # ngang tho, go do (Afzelia xylocarpa la loai ON DINH: co ngot thap)
K_BURL  = 0.0022   # NU: tho xoan loan, khong co huong -> lay cao va deu moi phuong
K_CORE  = 0.0005   # loi on dinh (ply/MDF) + veneer

RHO = {'cocobolo':1.10, 'go do dac':0.82, 'Nu go do':0.90, 'loi on dinh':0.58}

hr("1. TAI SAO NAP KHONG THE LA MOT TAM NU DAC — chuoi mat mong")
PITCH, KLEN, GAP = 45.0, 44.0, 1.0
K = [((n-1)*PITCH, (n-1)*PITCH+KLEN, 'THAN' if n%2 else 'NAP') for n in range(1,8)]
RUN = 6*PITCH + KLEN
CTR = RUN/2
print(f"  7 mat mong xen ke, buoc {PITCH:.0f}, dai {KLEN:.0f}, khe doc truc {GAP:.1f}. Chuoi {RUN:.0f} mm.")
print(f"  Than = go dac thang tho, tho chay doc canh 350 -> mat mong THAN dung yen.")
print(f"  Canh nap no deu quanh tam chuoi ({CTR:.0f} mm). Mat mong NAP truot doc truc.\n")

def min_gap(k_mat):
    """Khe doc truc nho nhat con lai khi vat lieu canh nap gian he so k_mat"""
    best=None
    for i in range(6):
        a0,b0,t0 = K[i]; a1,b1,t1 = K[i+1]
        A = b0 if t0=='THAN' else CTR + (b0-CTR)*(1+k_mat)
        B = a1 if t1=='THAN' else CTR + (a1-CTR)*(1+k_mat)
        g = B - A
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
print(f"   - Mat mong la ong go thanh 5,8 mm quanh lo Ø6,2, dai 44.")
print(f"   - Go thang tho: tho chay doc truc mong -> ben. Nu: tho xoan loan, khong co")
print(f"     huong nao dam bao, lai hay co loi vo/lo rong -> mat mong co the tach.")
print(f"   - Khong the thiet ke chi tiet 5,8 mm thanh mong theo mot ung suat cho phep")
print(f"     nao ca, vi Nu khong co tri so cho phep on dinh.")
print(f"  ==> Canh ban le BAT BUOC la go dac thang tho. Tuc la KHUNG + TAM THA.")

hr("2. KHUNG + TAM THA (frame & panel) — dung nhu anh mau")
LW, LL = 176.7, 350.0        # canh nap
ST_H, ST_S, RAIL = 34.0, 34.0, 30.0    # do dai canh mong / canh khe giua / do ngang
op_w = LW - ST_H - ST_S
op_l = LL - 2*RAIL
GRV, TON = 9.0, 6.0          # ranh sau 9, mong tam dai 6 -> tha 3 mm moi phia
pan_w, pan_l = op_w + 2*TON, op_l + 2*TON
print(f"  Do doc canh mong {ST_H:.0f} | Do doc canh khe giua {ST_S:.0f} | Do ngang {RAIL:.0f}")
print(f"  Long khung        : {op_w:.1f} x {op_l:.1f}")
print(f"  Tam Nu            : {pan_w:.1f} x {op_l+2*TON:.1f} x day 10   (mong {TON:.0f} vao ranh sau {GRV:.0f})")
print(f"  Khong gian tha    : {GRV-TON:.0f} mm moi phia\n")
print(f"  {'Chuyen vi can nuot':28s}{'dMC 2%':>9s}{'dMC 3%':>9s}{'dMC 5%':>9s}{'cho phep':>10s}")
for lbl, dim in [("Tam Nu theo be rong", pan_w), ("Tam Nu theo chieu dai", pan_l)]:
    d=[dim*K_BURL*m/2 for m in (2,3,5)]
    ok = "OK" if d[2] <= (GRV-TON) else "THIEU"
    print(f"  {lbl:28s}{d[0]:9.2f}{d[1]:9.2f}{d[2]:9.2f}{GRV-TON:9.1f}  {ok}")
print(f"  (chia 2 vi tam tha deu ve hai phia - CHI dan/chot tam o DUNG TAM)")

hr("3. KHE RAP GIUA NAP")
print(f"  Be rong canh nap = do {ST_H:.0f} + long {op_w:.1f} (THA) + do {ST_S:.0f}")
print(f"  Chi hai thanh do nam trong chuoi kich thuoc -> tam Nu khong dong gop gi.\n")
print(f"  {'Cau tao':26s}{'dMC 2%':>9s}{'dMC 3%':>9s}{'dMC 5%':>9s}")
for lbl,k,dim in [("Nu dac ca tam", K_BURL, LW),
                  ("Khung + tam tha", K_TANG, ST_H+ST_S),
                  ("Loi on dinh + veneer", K_CORE, LW)]:
    d=[2*dim*k*m for m in (2,3,5)]     # x2 vi hai canh cung no vao khe
    print(f"  {lbl:26s}{d[0]:9.2f}{d[1]:9.2f}{d[2]:9.2f}")
print(f"\n  Khe hien tai 0,6 mm. Voi khung+tam: can >= {2*(ST_H+ST_S)*K_TANG*5:.2f} mm o dMC 5%.")
print(f"  => De xuat khe rap giua 1,5 +/-0,3. Song khoa 44 rong phu kin khe nen KHONG lo.")

hr("4. KHAY BO BAI HINH THANH MIEN PHI")
t_h, t_s, PAN_T = 18.0, 12.0, 10.0
print(f"  Khung day {t_h:.0f} tai mong -> {t_s:.0f} tai khe giua; tam Nu day {PAN_T:.0f}, phang voi mat tren.")
print(f"  => Mat duoi tam Nu cao hon mat duoi khung:")
print(f"     tai canh mong    : {t_h-PAN_T:.0f} mm sau")
print(f"     tai canh khe giua: {t_s-PAN_T:.0f} mm sau")
print(f"  Long lom {op_w:.1f} x {op_l:.0f} nay CHINH LA khay bo bai trong anh mau -")
print(f"  khong phai phay them, khong dinh toi van de 'khong phay duoc long o mep 8 mm'.")

hr("5. KHOI LUONG — cau hinh da chot")
print("  Khung nap = COCOBOLO (dong mau than). Chi tam nap la Nu go do.\n")
print(f"  {'Cau tao khay':16s}{'go kg':>8s}{'+quan':>8s}{'TONG kg':>9s}{'tai TK':>9s}")
for khay in ('cocobolo','loi on dinh'):
    go,t,tot = B.mass(khay)
    print(f"  {khay:16s}{go:8.2f}{t:8.2f}{tot:9.2f}{B.design_load(khay):8.0f} N")
print(f"\n  Tai thiet ke {B.design_load('cocobolo'):.0f} N so voi 215 N o buoc truoc (+8 %).")
print("  Kiem lai toan bo kiem ben quai: he so an toan thap nhat tut tu 10x xuong 9x.")
print("  => Kich thuoc song khoa, chot xoay va quai GIU NGUYEN, khong phai sua.")

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
            ("Chieu day","10 mm la diem can - mong hon thi de nut khi thao tac, day hon thi kho san"),
            ("Dan tam","CHI dan/chot mot diem o DUNG TAM moi canh; tuyet doi khong dan quanh ranh"),
            ("Hoan thien","Nu hut khong deu -> phai bit lo (grain filler) roi moi phu")]:
    print(f"   - {a:12s}: {b}")

hr("7. NHUNG GI KHONG DOI")
for t in ["Song khoa 44 x 20, chot xoay Ø16, quai - tai thiet ke gan nhu y nguyen",
          "Song bat cung vao DO DOC CANH KHE GIUA (go dac), khong bao gio bat vao tam Nu tha",
          "Vat nap 18 -> 12 van giu (khung vat, tam Nu day deu 10)",
          "Hoc ban nguyet R8,5 cho chot: khoet vao DO DOC canh khe giua - go dac, khoet duoc",
          "Phu bi 354 x 362 x 83"]:
    print(f"   - {t}")

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
    d=B.dalbergia_kg(khay)
    print(f"  {khay:16s}{d:15.2f}{int(10//d):21d}")
print("  (theo nguong mien tru 10 kg cua annotation #15 - PHAI xac minh lai)")
