#!/usr/bin/env python3
"""
Phuong an nap go dac: khung go do + tam Nu go do (thay cho nap boc da / veneer.)
Chay: python3 tools/lid_solid_calc.py
"""
import math
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

hr("5. KHOI LUONG")
V = {'day':354*350*8, 'vach truoc/sau':2*(354*10*44), 'vach trai/phai':2*(330*10*39),
     'vach ngan':2*(330*6*44), 'khay quan':4*(325*124*19-315*114*15),
     'khay phu kien':325*68*38-(28*152*24.5+58*75*18.5+58*78*18.5)}
V_frame = 2*((LW*LL - op_w*op_l)*15)            # khung, day trung binh 15
V_panel = 2*(pan_w*pan_l*PAN_T)                  # tam Nu
V_lid = V_frame + V_panel
print(f"  Khung 2 canh : {V_frame/1000:7.0f} cm3      Tam Nu 2 canh: {V_panel/1000:7.0f} cm3")
print(f"  Nap tong     : {V_lid/1000:7.0f} cm3      Than+khay    : {sum(V.values())/1000:7.0f} cm3")
m_tiles = 152*16/1000
SC = [("Than+khay cocobolo | nap go do dac", 'cocobolo','go do dac','Nu go do'),
      ("Than cocobolo, khay loi on dinh | nap go do dac", 'cocobolo','go do dac','Nu go do'),
      ("Than+khay cocobolo | nap loi on dinh + veneer Nu", 'cocobolo','loi on dinh','loi on dinh')]
print(f"\n  {'Cau tao':50s}{'go':>7s}{'+quan':>8s}{'TONG':>8s}")
out={}
for i,(name,rb,rf,rp) in enumerate(SC):
    vb = sum(V.values())
    if i==1:
        m = (V['day']+V['vach truoc/sau']+V['vach trai/phai']+V['vach ngan'])/1e6*RHO['cocobolo'] \
          + (V['khay quan']+V['khay phu kien'])/1e6*RHO['loi on dinh']
    else:
        m = vb/1e6*RHO[rb]
    m += V_frame/1e6*RHO[rf] + V_panel/1e6*RHO[rp]
    out[name]=m
    print(f"  {name:50s}{m:7.2f}{m_tiles:8.2f}{m+m_tiles:8.2f}")
M = max(out.values())+m_tiles
print(f"\n  Truoc day (nap loi on dinh, khay cocobolo): 6,67 kg")
print(f"  => Nap go do dac cong them ~{M-6.67:.2f} kg. Tai thiet ke P = {M*9.81*3:.0f} N")
print(f"     (truoc la 215 N -> quai da tinh o buoc truoc VAN DU, khong phai tinh lai)")

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
print("     Cong voi cocobolo (Dalbergia, Phu luc II) - hop nay co HAI loai can kiem tra.")
