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

hr("1. TAI SAO NAP KHONG THE LA MOT TAM NU DAC — khe rap giua")
LW = B.derive()['LW']
print(f"  Nap gap doi: hai canh {LW:.2f} mm, khe rap giua {B.SEAM} mm.")
print(f"  Ca hai canh cung hut am va cung lon ra, moi ben an vao khe mot nua.")
print(f"  Nu khong co huong tho -> no DEU moi phuong, ca be rong canh nam trong")
print(f"  chuoi kich thuoc. Khung go dac chi dua {2*B.STILE:.0f} mm go ngang tho vao chuoi.\n")
print(f"  {'Cau tao canh nap':26s}{'he so':>8s}" + "".join(f"{'dMC '+str(m)+'%':>9s}" for m in (2,3,4,5)))
for lbl, kind, kk in [("Tam Nu dac", 'nu', K_BURL),
                      ("Loi on dinh + veneer", 'core', K_CORE),
                      ("Khung go dac + tam tha", 'frame', K_TANG)]:
    row = "".join(f"{B.seam_left(m, kind):9.2f}" for m in (2, 3, 4, 5))
    print(f"  {lbl:26s}{kk*100:7.2f}%{row}")
print(f"  (gia tri = khe con lai, mm. Am = hai canh CHONG NHAU -> tu pha go)\n")
for lbl, kind in [("Tam Nu dac", 'nu'), ("Loi on dinh + veneer", 'core'),
                  ("Khung go dac + tam tha", 'frame')]:
    d = B.seam_close_dmc(kind)
    print(f"    {lbl:26s}: khe dong o dMC {d:5.2f} %")
print(f"\n  Xuong lam o 9 % MC, mua nong am mien Bac/Nam len 13 % -> dMC = 4 %.")
print(f"  => Nap Nu DAC dong khe o dMC {B.seam_close_dmc('nu'):.2f} % — chua het mot mua.")
print(f"     Hai canh chong nhau roi tu pha go hoac day bung ban le.")

print(f"\n  Van de thu hai — do doc canh ban le phai chiu duoc gi:")
SS = B.derive()
LWx = SS['LW']
m_lf = (SS['V']['khung nap']/2/1e6*B.RHO['cocobolo']
        + SS['V']['tam Nu']/2/1e6*B.RHO['Nu go do'])
M_ty = m_lf*9.81*(LWx/2)/1000 + 5.0*9.81*LWx/1000
print(f"   - Mat mong ban le duoc PHAY THANG TU do doc: ong go O{2*SS['R_KN']:.1f} lien khoi")
print(f"     voi do, va mot lo chot O{SS['KN_HOLE']:.2f} khoan doc {B.KN_PIN_L:.0f} mm xuyen trong")
print(f"     long do. Nu tho xoan loan, hay co loi vo va lo rong: mot lo sau {B.KN_PIN_L:.0f} mm")
print(f"     trong Nu gan nhu chac chan gap lo rong, va ong go se tach.")
print(f"   - Thanh go quanh lo chot chi {SS['KN_WALL_EFF']:.1f} mm, chay suot chuoi mong")
print(f"     {SS['KN_RUN']:.0f} mm tren canh do doc: chi tiet mong nhat cua ca cai hop.")
print(f"   - Khi mo 180 do, TOAN BO tai cua canh doi qua mat chan {SS['STOP_A']:.0f} mm2 —")
print(f"     chinh la mat canh cua do doc ban le. Nguoi choi ty 5 kg o mep ngoai cho")
print(f"     {M_ty:.2f} N.m. Ep mat ngang tho co tri so cho phep ({B.C_PERP:.0f} MPa cho")
print(f"     cocobolo); Nu KHONG co tri so nao on dinh.")
print(f"  ==> Do doc ban le BAT BUOC la go dac thang tho. Tuc la KHUNG + TAM THA.")
