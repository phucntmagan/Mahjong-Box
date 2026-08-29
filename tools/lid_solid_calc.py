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
print(f"   - Ban le brass an mortise sau {B.HG_MORT:.1f} mm vao mat duoi do doc, giu bang")
print(f"     vit brass. Vit bat vao Nu: tho xoan loan, hay co loi vo va lo rong,")
print(f"     khong co huong nao dam bao -> luc nho vit khong the dam bao duoc.")
print(f"   - Khi mo 180 do, TOAN BO tai cua canh doi qua mat chan {SS['STOP_H']:.2f} x")
LWx = SS['LW']
m_lf = (SS['V']['khung nap']/2/1e6*B.RHO['cocobolo']
        + SS['V']['tam Nu']/2/1e6*B.RHO['Nu go do'])
M_ty = m_lf*9.81*(LWx/2)/1000 + 5.0*9.81*LWx/1000
print(f"     {B.LID_L:.0f} mm — chinh la mat canh cua do doc ban le. Nguoi choi ty 5 kg")
print(f"     o mep ngoai cho {M_ty:.2f} N.m. Ep mat ngang tho co tri so cho phep")
print(f"     ({B.C_PERP:.0f} MPa cho cocobolo); Nu KHONG co tri so nao on dinh.")
print(f"   - Bo luon arris R{B.HG_R:.2f} chay suot {B.LID_L:.0f} mm nam dung tren canh do")
print(f"     doc: canh mong nhat cua chi tiet, cho de vo nhat neu go co lo rong.")
print(f"  ==> Do doc ban le BAT BUOC la go dac thang tho. Tuc la KHUNG + TAM THA.")
