#!/usr/bin/env python3
"""
So sanh ba phuong an be rong hop, dung CHINH bo cong thuc cua box_spec.derive().
Chay: python3 tools/width_options.py

Nen tang: vach ban le buoc phai 18 (hoc am hai tay: sau 12 + thanh sau 6), nen
chuoi X 354 cu khong dung duoc nua. Ba cach dong lai chuoi X:
   370  giu nguyen bo tri long hop
   366  vach ngan mong con 4
   362  khoang phu kien con 62
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B

TILE_MAX = (25.7, 36.8, 11.4)     # quan lon nhat theo Rev B
CITES_LIMIT = 10.0                # kg go loai liet ke moi lo (annotation #15 - PHAI xac minh)
SCALLOP_D, SCALLOP_DEPTH = 25.0, 12.0   # hom ngon ranh Joker

OPTS = [
    ("370", dict(div=6.0, ac_bay=70.0), "giu nguyen bo tri long hop"),
    ("366", dict(div=4.0, ac_bay=70.0), "vach ngan mong con 4"),
    ("362", dict(div=6.0, ac_bay=62.0), "khoang phu kien con 62"),
]

def summarise(kw):
    d = B.derive(**kw)
    V = d['V']
    # dung dung ham cua box_spec — de khong bo sot nhom nao (vd. ban le brass)
    m_c = B.mass_of(d, 'cocobolo')[2]
    m_s = B.mass_of(d, 'loi on dinh')[2]
    tiles = B.N_TILES*B.M_TILE_G/1000
    dal_c = B.dalbergia_of(d, 'cocobolo')
    dal_s = B.dalbergia_of(d, 'loi on dinh')
    ac_in = (d['AC_BAY'] - 2.0) - 2*B.AC_WALL
    return dict(d=d, W=d['W'], LW=d['LW'], OP_W=d['OP_W'], ANG=d['ANG'],
                m_c=m_c, m_s=m_s,
                dal_c=dal_c, dal_s=dal_s, ac_in=ac_in,
                strip=(ac_in - B.AC_JOKER[0])/2, div=d['DIV'])

def hr(t): print("\n" + "="*78 + "\n" + t + "\n" + "="*78)

R = [(lbl, summarise(kw), note) for lbl, kw, note in OPTS]

hr("1. KHOI LUONG VA TAI THIET KE")
print(f"  {'X':>5s}{'canh nap':>10s}{'long khung':>12s}{'goc vat':>9s}"
      f"{'kg (khay coco)':>16s}{'tai TK':>9s}{'kg (loi o.d.)':>15s}")
for lbl, s, _ in R:
    print(f"  {lbl:>5s}{s['LW']:10.2f}{s['OP_W']:12.2f}{s['ANG']:8.2f}°"
          f"{s['m_c']:16.2f}{s['m_c']*9.81*B.DYN:8.0f} N{s['m_s']:15.2f}")
base = R[0][1]['m_c']
print(f"\n  Chenh khoi luong giua 370 va 362: {base - R[2][1]['m_c']:.3f} kg "
      f"({(base-R[2][1]['m_c'])/base*100:.1f} %) — duoi nguong cam nhan khi xach.")

hr("2. NGUONG MIEN TRU CITES (10 kg Dalbergia moi lo — PHAI xac minh)")
print(f"  {'X':>5s}{'Dalb/hop':>11s}{'2 hop':>8s}{'3 hop':>8s}{'so hop/lo':>11s}"
      f"{'bien con lai':>14s}   (khay cocobolo)")
for lbl, s, _ in R:
    n = int(CITES_LIMIT // s['dal_c'])
    print(f"  {lbl:>5s}{s['dal_c']:11.2f}{2*s['dal_c']:8.2f}{3*s['dal_c']:8.2f}"
          f"{n:11d}{(CITES_LIMIT - n*s['dal_c'])/CITES_LIMIT*100:13.1f} %")
print()
print(f"  {'X':>5s}{'Dalb/hop':>11s}{'3 hop':>8s}{'so hop/lo':>11s}"
      f"{'bien con lai':>14s}   (khay loi on dinh)")
for lbl, s, _ in R:
    n = int(CITES_LIMIT // s['dal_s'])
    print(f"  {lbl:>5s}{s['dal_s']:11.2f}{3*s['dal_s']:8.2f}{n:11d}"
          f"{(CITES_LIMIT - n*s['dal_s'])/CITES_LIMIT*100:13.1f} %")
print("\n  => Be rong KHONG lat duoc so hop/lo o ca hai cau tao khay.")
print("     Don bay that su la khay (2 hop -> 3 hop), khong phai be rong.")

hr("3. HE QUA CONG NANG — cho nao gay")
print(f"  {'X':>5s}{'vach ngan':>11s}{'long AC-01':>12s}{'dai ben ranh Joker':>21s}"
      f"{'4 quan du phong 2x2':>22s}")
for lbl, s, _ in R:
    fit = "duoc" if s['ac_in'] >= 2*TILE_MAX[0] else f"KHONG ({2*TILE_MAX[0]:.1f} can)"
    print(f"  {lbl:>5s}{s['div']:11.0f}{s['ac_in']:12.0f}{s['strip']:21.0f}{fit:>22s}")
print()
print(f"  Hom ngon ranh Joker: ban nguyet Ø{SCALLOP_D:.0f} sau {SCALLOP_DEPTH:.0f}"
      f" khoet vao dai ben canh ranh.")
for lbl, s, _ in R:
    left = s['strip'] - SCALLOP_DEPTH
    verdict = (f"con {left:.0f} mm go" if left >= 3.0
               else f"CON {left:.0f} mm — khong khoet duoc")
    print(f"    X={lbl}: dai {s['strip']:.0f} - sau {SCALLOP_DEPTH:.0f} -> {verdict}")
print()
print("  Vach ngan 4 mm (X=366): cocobolo 4 x 43 x 330, khe dan vao day sau 4 mm.")
print("    Ty le manh 330/4 = 82:1. Lam duoc, nhung day la chi tiet duy nhat trong")
print("    hop KHONG co bien du — va no la thanh cua khoang khay, khay co xat vao.")

hr("4. KET LUAN")
print("  370  khoi luong +0,06 kg so voi 362, khong doi bat ky chi tiet nao da chot,")
print("       ty le 370 x 362 gan vuong. So hop/lo CITES khong doi.")
print("  366  tiet kiem 4 mm bang cach lam mong chi tiet mong nhat cua hop. Doi khong dang.")
print("  362  pha ca hai chi tiet cong nang cua AC-01: hoc 4 quan du phong 2x2 va")
print("       hom ngon ranh Joker. Phai bo tri lai, va van khong doi duoc so hop/lo.")
print("\n  => KHUYEN NGHI: 370.")
