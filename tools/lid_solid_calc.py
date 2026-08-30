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
K_TANG  = B.k_stile()                 # do doc khung cocobolo, theo cach xe da chon
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

# ==========================================================================
hr("2. TAM NU NGANG BANG MAT KHUNG — tam NANG (raised panel)")
print(f"  Yeu cau: mat nap la MOT MAT PHANG lien, tam Nu khong thut xuong duoi")
print(f"  mat khung {B.S_TOP:.0f} mm nhu ban truoc.\n")
print(f"  Khong the chi nang tam len roi dan: tam Nu {S['PAN_W']:.0f} x {S['PAN_L']:.0f} no")
print(f"  {B.K['Nu moi phuong']*100:.2f} %/1%MC MOI PHUONG. Dan cung thi hoac tam nut hoac")
print(f"  mong khung bung. Nen tam VAN PHAI THA — chi doi hinh cat cua no:\n")
for a, b_ in [("Be day toan bo tam", f"{S['PAN_TH']:.0f} = mong {B.PAN_T:.0f} + phan dang len"
                                     f" {B.S_TOP:.0f}"),
              ("Bac phay quanh mep TREN", f"sau {B.S_TOP:.0f} x rong {S['PAN_REB']:.0f}"
                                          f" (= an vao ranh {B.TON:.0f} + khe {B.PAN_REV:.1f})"),
              ("Mong con lai", f"day {B.PAN_T:.0f}, an vao ranh {B.TON:.0f} tren tong sau"
                               f" {B.GRV:.0f} -> tha {S['PAN_FLOAT']:.0f} mm moi phia"),
              ("Long tam (phan dang len)", f"{S['FIELD_W']:.2f} x {S['FIELD_L']:.2f}, mat tren"
                                           f" o Z{S['Z_LID']:.0f} — ngang bang mat khung"),
              ("Khe quanh long tam", f"{B.PAN_REV:.1f} mm moi phia")]:
    print(f"   {a:26s}: {b_}")
print(f"\n  Cai khe {B.PAN_REV:.1f} mm KHONG phai trang tri: no la cho cho tam no ra.")
print(f"  Tam tha giua nen moi phia dich mot NUA tong bien thien.\n")
print(f"  {'phuong':>10s}{'kich thuoc tam':>17s}{'dich moi phia':>16s}{'khe con lai':>14s}")
for lbl, dim, mv in (("theo X", S['PAN_W'], S['PAN_MOVE_W']),
                     ("theo Y", S['PAN_L'], S['PAN_MOVE_L'])):
    print(f"  {lbl:>10s}{dim:17.1f}{mv:16.2f}{B.PAN_REV - mv:14.2f}")
print(f"\n  Muc 1 da dat: xuong lam ~9 % MC, mua nong am len ~13 % -> bien do 4 %.")
print(f"  Tam PHAI duoc on dinh ve giua dai ({(9+13)/2:.0f} %) TRUOC khi lap, luc do bien")
print(f"  thien chi con +/- {B.DMC_DES:.1f} %. Neu lap thang o 9 % thi ca {B.DMC_DRY:.0f} %")
print(f"  doi ve MOT phia — do la truong hop kiem thu hai.\n")
print(f"  {'truong hop':>34s}{'dich moi phia':>15s}{'khe hep nhat':>14s}{'khe rong nhat':>15s}")
for lbl, mv in ((f"da on dinh 11 %, +/-{B.DMC_DES:.0f} %", S['PAN_MOVE']),
                (f"lap thang o 9 %, +{B.DMC_DRY:.0f} % mot chieu", S['PAN_MOVE_DRY'])):
    print(f"  {lbl:>34s}{mv:15.2f}{B.PAN_REV-mv:14.2f}{B.PAN_REV+mv:15.2f}")
print(f"\n  Ca hai truong hop khe VAN CON HO — {B.PAN_REV:.1f} mm chon dung de nuot duoc ca")
print(f"  truong hop xau. Do la ly do khe la {B.PAN_REV:.1f} chu khong phai 1,0.\n")
print(f"  {'bien thien am':>15s}{'khe hep nhat':>15s}{'khe rong nhat':>16s}   ghi chu")
for dm in (2.0, B.DMC_DRY, 6.0, 8.0):
    mv = max(S['PAN_W'], S['PAN_L'])*B.K['Nu moi phuong']*dm/2
    note = ("lap kho, truong hop kiem" if abs(dm - B.DMC_DRY) < 1e-9 else
            "long tam dap vao khung" if mv > B.PAN_REV else "")
    print(f"  {dm:14.1f} %{B.PAN_REV-mv:15.2f}{B.PAN_REV+mv:16.2f}   {note}")
print(f"\n  Neu muon khe NHO hon {B.PAN_REV:.1f} mm thi chi con mot duong: bo Nu dac, dung")
print(f"  veneer Nu tren loi on dinh ({B.K['loi on dinh']*100:.2f} %/1%MC thay vi"
      f" {B.K['Nu moi phuong']*100:.2f} %).")
mv_core = max(S['PAN_W'], S['PAN_L'])*B.K['loi on dinh']*B.DMC_DRY/2
print(f"  Luc do dich moi phia chi {mv_core:.2f} mm, khe {mv_core*1.5:.1f} mm la du — hoac dan")
print(f"  cung luon, khong con khe. Doi lai: mat cat canh tam khong con la go that.")
print(f"\n  ==> Chot: tam Nu DAC, tha, khe {B.PAN_REV:.1f} mm quanh long tam. Khe do la mot")
print(f"      duong bong deu, doc theo ca bon canh — doc duoc nhu chi tiet, khong phai")
print(f"      nhu khe ho. Mat tren tam va mat khung DONG PHANG o Z{S['Z_LID']:.0f}.")
