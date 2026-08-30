#!/usr/bin/env python3
"""
BA DUONG KHE NHIN THAY TREN MAT NAP — chung tu dau ra, va siet duoc toi dau.

Nhin tu tren xuong, mat nap co dung ba duong 1,5 mm:
    2 khe quanh long tam nu (moi canh nap mot khe chay quanh)
    1 khe rap giua hai canh
Hai loai khe nay KHONG cung nguyen nhan, nen khong siet chung bang mot cach.

Chay: python3 tools/gap_options.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B

S = B.derive()
K_BURL = B.K['Nu moi phuong']
K_COCO = B.K['cocobolo ngang tho']
K_CORE = B.K['loi on dinh']
# Ty le co ngot XUYEN TAM / TIEP TUYEN cua go cung nhiet doi. Tra bang (cocobolo
# 2,7 / 4,3). CHUA do tren lo go thuc te — dung de so sanh phuong an, khong dung
# de chot kich thuoc khi chua co so lieu lo hang.
RAD_RATIO = 0.63

def hr(t): print('\n' + '='*78 + f'\n{t}\n' + '='*78)

hr('1. MOI DUONG KHE DANG DO CAI GI')
print(f"""  KHE QUANH LONG TAM  (PAN_REV = {B.PAN_REV:.1f})
    Tam nu {S['PAN_W']:.1f} x {S['PAN_L']:.0f}, THA trong ranh, no {K_BURL*100:.2f} %/1%MC MOI PHUONG.
    Long khung KHONG doi kich thuoc (do doc/do ngang chan nhau theo chieu DOC tho),
    nen ca chuyen vi la cua rieng tam. Canh dai {S['PAN_L']:.0f} chi phoi.
    Can moi phia = {S['PAN_L']:.0f} x {K_BURL:.4f} x dMC / 2 = {S['PAN_L']*K_BURL/2:.3f} x dMC

  KHE RAP GIUA  (SEAM = {B.SEAM:.1f})
    Moi canh nap no theo be RONG bang chuyen vi NGANG THO cua hai do doc:
      2 x {B.STILE:.0f} x {K_COCO:.4f} x dMC = {2*B.STILE*K_COCO:.4f} x dMC
    Ban le o hai mep NGOAI nen ca luong no do doi vao GIUA. Hai canh cung doi:
    khe dong lai = {2*2*B.STILE*K_COCO:.4f} x dMC
    Tam nu KHONG dong gop mot mm nao — no tha, no khong day khung.""")

hr('2. MOT KHE CHO SAN BAO NHIEU %MC')
print(f"  {'khe':>6}{'long tam: dMC chiu duoc':>26}{'khe rap giua: dMC chiu duoc':>30}")
for g in (0.3, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0):
    d_pan = g/(S['PAN_L']*K_BURL/2)
    d_seam = g/(2*2*B.STILE*K_COCO)
    print(f"  {g:6.1f}{d_pan:20.1f} %{d_seam:24.1f} %")
print(f"""
  Doc bang: khe hien tai 1,5 cho long tam {1.5/(S['PAN_L']*K_BURL/2):.1f} %MC va cho khe rap giua
  {1.5/(2*2*B.STILE*K_COCO):.1f} %MC. Hai con so rat khac nhau — CUNG mot be rong khe dang
  mua hai muc an toan khac han nhau. Do la dau hieu no duoc chon bang mat chu
  khong bang tinh.""")

hr('3. KHE QUANH LONG TAM: 1,5 DANG BAO HIEM CHO MOT RUI RO DA BI P5 CAM')
need_des = S['PAN_L']*K_BURL*B.DMC_DES/2
need_dry = S['PAN_L']*K_BURL*B.DMC_DRY/2
print(f"""  box_spec kiem tam nu bang HAI truong hop:
    on dinh ve 11 % roi bien thien +/-{B.DMC_DES:.0f} %  -> can {need_des:.2f} mm
    lap thang o 9 %, ca {B.DMC_DRY:.0f} % don mot chieu -> can {need_dry:.2f} mm   <- cai nay chon 1,5
  Ma QA-01 P5 la PHEP THU BAT BUOC: "on dinh tam Nu va moi phoi ve 11 % MC, 11 % +/-1".
  Truong hop thu hai chi xay ra khi P5 bi bo qua. Thiet ke chong lai mot truong hop
  ma mot phep thu bat buoc da cam la DEM RUI RO HAI LAN.

  Neu tin P5: khe can {need_des:.2f} -> chon 0,8 con du he so {0.8/need_des:.2f}x, chiu toi
  {0.8/(S['PAN_L']*K_BURL/2):.1f} %MC bien thien.
  Neu khong tin P5: phai giu 1,5. Khong co duong giua.""")

hr('4. KHE RAP GIUA: SIET DUOC BA CACH, DEU CO GIA')
rows = []
rows.append(('giu nguyen', B.STILE, K_COCO, B.SEAM))
rows.append(('do doc xe XUYEN TAM (quartersawn)', B.STILE, K_COCO*RAD_RATIO, None))
rows.append(('do doc 34 -> 24', 24.0, K_COCO, None))
rows.append(('ca hai', 24.0, K_COCO*RAD_RATIO, None))
print(f"  {'phuong an':38}{'no/canh o 5%':>14}{'khe toi thieu':>15}{'de xuat':>10}")
for name, st, k, fixed in rows:
    grow5 = 2*st*k*5.0
    need = 2*grow5
    pick = fixed if fixed else math.ceil((need + 0.2)*10)/10
    print(f"  {name:38}{grow5:12.2f} mm{need:13.2f} mm{pick:9.1f}")
print(f"""
  Gia phai tra:
    xe xuyen tam : ty le {RAD_RATIO:.2f} la TRA BANG, chua do tren lo go. Va go xuyen tam
                   khong con van chay uon — cocobolo dep nhat lai la o mat tiep tuyen.
                   Doi van lay on dinh: day la quyet dinh THAM MY, khong phai ky thuat.
    do doc 34->24: khung yeu di. Do doc mang MAT MONG BAN LE (ong go O{2*S['R_KN']:.1f}
                   nam tren arris, an vao do doc) — 24 mm van du, nhung nhip mep
                   tu do dai {B.LID_L:.0f} thi do cung uon giam ({(24/B.STILE)**1:.2f} lan theo
                   be rong). Va vien khung mong di la doi ty le nhin thay.""")

hr('5. NEU MUON CA BA DUONG DUOI 0,5 — CHI CON MOT DUONG')
need_core = S['PAN_L']*K_CORE*B.DMC_DRY/2
print(f"""  Khe quanh long tam bi TAM NU DAC ep. Doi tam sang VENEER NU tren loi on dinh:
    no {K_CORE*100:.2f} %/1%MC thay vi {K_BURL*100:.2f} -> can {need_core:.2f} mm o ca truong hop kho {B.DMC_DRY:.0f} %.
    Tuc khe 0,4 la du, va neu dan cung thi KHONG CON KHE NAO — long khung on dinh
    nen tam loi on dinh dan chet duoc, duong khe bien thanh duong keo.
  Nhung khe RAP GIUA thi veneer khong giup gi: no do hai do doc COCOBOLO DAC sinh ra.
  Muon no duoi 0,5 thi phai xe xuyen tam VA thu do doc, hoac chap nhan khe dong han
  o {0.5/(2*2*B.STILE*K_COCO):.1f} %MC.

  => Ket luan: "mat nap phang lien, ba duong khe sat" va "tam nu GO DAC" la hai
     yeu cau chong nhau. Chon mot.""")

hr('6. MOT LOI THOAT KHAC: GIAU KHE THAY VI THU KHE')
print(f"""  Khe quanh long tam lo ra la vi Rev C3 chot TAM NANG, long tam NGANG BANG mat
  khung. Neu tam THUT XUONG duoi mat khung (nhu Rev C2) thi mep khung phu len canh
  tam, va khe gian no nam KHUAT duoi mep phu — nhin tu tren khong thay duong nao ca,
  du khe thuc te van {B.PAN_REV:.1f} mm.
  Doi lai: mat nap khong con la mot mat phang lien. Do dung la thu Rev C3 danh doi
  de lay. Ghi ra day de quyet dinh duoc nhin thay ca hai chieu.""")
