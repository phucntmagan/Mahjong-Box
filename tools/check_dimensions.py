#!/usr/bin/env python3
"""
Kiem tra doc lap toan bo chuoi kich thuoc cua ban ve
"Ban ve san xuat hop Mahjong 152 quan - Rev B" (BURLORA).

Script nay kiem BAN VE DA NHAN, nen cac tri so Rev B duoi day CO CHU DINH go
cung — chung la doi tuong duoc kiem, khong phai dac ta. Dac ta hien hanh nam
o tools/box_spec.py; muc 9 o cuoi doi chieu Rev B voi dac ta do.

Chay:  python3 tools/check_dimensions.py
Khong phu thuoc thu vien ngoai.

Quy uoc: don vi mm. Z=0 la mat ban. Truc X chay theo canh 354,
X=0 tai canh co mong trai, X=177 tai khe rap giua nap.
"""

import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as BS
S = BS.derive()

IN = 25.4

# ---------------------------------------------------------------- quan co
TILE_NOM = (1.0 * IN, 1.4375 * IN, 0.4375 * IN)   # 1 x 1-7/16 x 7/16 inch
TILE_REVB_MAX = (25.7, 36.8, 11.4)                 # gioi han lo hang cua Rev B
TILE_LOT_P05 = tuple(round(d + 0.5, 3) for d in TILE_NOM)  # lo thuc te +0.5

# ---------------------------------------------------------------- Rev B
REVB = dict(
    overall=(354, 350, 80),
    body_wall_outer=10, body_divider=6, body_bottom=8, foot=2,
    body_h_hinge=60, body_h_seam=70,
    lid_leaf=(176.7, 350), lid_t_hinge=18, lid_t_seam=8, seam_gap=0.6,
    tray_outer=(325, 124, 19), tray_inner=(315, 114), tray_floor=4.0, felt=0.8,
    ac_outer=(325, 68, 38), ac_wall=5.0,
    ac_joker=(28, 150, 24.5), ac_dice=(58, 75, 18.5), ac_aux=(58, 80, 18.5),
    knuckles=7, knuckle_len=44, knuckle_gap=1.0,
    pin_d=6.00, pin_hole_d=6.35, pin_len=322,
)

FAILS, WARNS = [], []

def check(label, got, want, tol=0.01):
    ok = abs(got - want) <= tol
    print(f"  [{'OK ' if ok else 'FAIL'}] {label:52s} = {got:9.3f}  (ky vong {want})")
    if not ok:
        FAILS.append(label)
    return ok

def note(cond, msg):
    print(f"  [{'OK ' if cond else 'CANH BAO'}] {msg}")
    if not cond:
        WARNS.append(msg)


print("=" * 78)
print("1. QUAN CO")
print("=" * 78)
print(f"  Danh nghia 1 x 1-7/16 x 7/16 in = "
      f"{TILE_NOM[0]:.3f} x {TILE_NOM[1]:.3f} x {TILE_NOM[2]:.3f} mm")
check("Rev B ghi 25,4 x 36,51 x 11,11 (chieu dai)", TILE_NOM[1], 36.51, 0.01)
check("Rev B ghi 25,4 x 36,51 x 11,11 (chieu day)", TILE_NOM[2], 11.11, 0.01)
print(f"  Truong hop lon nhat Rev B  : {TILE_REVB_MAX}   (=nom +0,30/+0,29/+0,29)")
print(f"  Lo mua thuc te +0,5 mm     : {TILE_LOT_P05}")


print()
print("=" * 78)
print("2. CHUOI KICH THUOC THAN HOP (GA-02)")
print("=" * 78)
xchain = [REVB['body_wall_outer'], 126, REVB['body_divider'], 70,
          REVB['body_divider'], 126, REVB['body_wall_outer']]
print("  Chuoi X: " + " + ".join(map(str, xchain)))
check("Tong chuoi X", sum(xchain), REVB['overall'][0])
ychain = [10, 330, 10]
print("  Chuoi Y: " + " + ".join(map(str, ychain)))
check("Tong chuoi Y", sum(ychain), REVB['overall'][1])
check("Khe khay quan moi ben (126 - 124)/2", (126 - REVB['tray_outer'][1]) / 2, 1.0)
check("Khe khay phu kien moi ben (70 - 68)/2", (70 - REVB['ac_outer'][1]) / 2, 1.0)
check("Khe khay moi dau (330 - 325)/2", (330 - REVB['tray_outer'][0]) / 2, 2.5)
note(False, "Kich thuoc khoang 126 / 70 / 330 KHONG co dung sai tren bat ky sheet nao; "
            "QA-01 lai yeu cau khe 1,0 +/-0,3 -> khong truy nguyen duoc.")
note(False, "Khong co sheet ban ve rieng cho than hop BX-01.")


print()
print("=" * 78)
print("3. KHAY QUAN TR-01 - long 315 x 114, sau 15,0, ni 0,8")
print("=" * 78)
inner_l, inner_w = REVB['tray_inner']
depth = REVB['tray_outer'][2] - REVB['tray_floor']
edge = 1.0
print(f"  Vach khay = (325-315)/2 = {(325-inner_l)/2:.1f} ; (124-114)/2 = {(124-inner_w)/2:.1f}")
print(f"  Sau long  = 19 - 4,0 = {depth:.1f}   ; sau huu dung = {depth-REVB['felt']:.1f}")
print(f"  {'':10s}{'khe 12 cot':>12s}{'khe 3 hang':>12s}{'mep tren quan':>16s}")
for lbl, (w, h, t) in [("danh nghia", TILE_NOM),
                       ("Rev B max ", TILE_REVB_MAX),
                       ("lo +0,5   ", TILE_LOT_P05)]:
    gx = (inner_l - 2 * edge - 12 * w) / 11
    gy = (inner_w - 2 * edge - 3 * h) / 2
    head = depth - REVB['felt'] - t
    print(f"  {lbl:10s}{gx:12.3f}{gy:12.3f}{head:16.3f}")
    if lbl.strip() == "Rev B max":
        check("Rev B ghi khe 12 cot >= 0,42", gx, 0.42, 0.005)
        check("Rev B ghi khe 3 hang >= 0,80", gy, 0.80, 0.005)
        check("Rev B ghi mep cao hon quan 2,8", head, 2.80, 0.005)
note(True, "Lo +0,5 van con khe duong o khay quan (0,200 / 0,481).")
note(False, "Hoc nhac tay 70 x 7 nam tren khay, nhung khay chi ho 1,0/ben - "
            "khong luon duoc ngon tay. Can hoc lom doi ung tren vanh khoang cua than.")


print()
print("=" * 78)
print("4. KHAY PHU KIEN AC-01")
print("=" * 78)
w_ac, wall = REVB['ac_outer'][1], REVB['ac_wall']
print(f"  Long ngang = 68 - 2 x 5 = {w_ac - 2*wall:.0f}  -> hoc xuc xac 58 dung het be rong")
print(f"  Dai rong con lai canh ranh Joker = (58 - 28)/2 = {(58-28)/2:.0f} moi ben (dang bo trong)")
for jl, aux in [(150, 80), (152, 78)]:
    tot = wall + jl + wall + REVB['ac_dice'][1] + wall + aux + wall
    tag = "Rev B" if jl == 150 else "de xuat"
    print(f"\n  [{tag}] 5 + {jl} + 5 + 75 + 5 + {aux} + 5 = {tot:.0f}")
    check(f"  chuoi dai AC-01 khep ve 325 ({tag})", tot, REVB['ac_outer'][0])
    for lbl, h in [("danh nghia", TILE_NOM[1]), ("Rev B max ", TILE_REVB_MAX[1]),
                   ("lo +0,5   ", TILE_LOT_P05[1])]:
        g = (jl - 2 * 1.0 - 4 * h) / 3
        flag = "  <-- AM, KHONG NHET DUOC" if g < 0 else ""
        print(f"      khe giua 4 Joker, bien 1,0 - {lbl}: {g:7.3f}{flag}")
# cong thuc goc cua Rev B cho 150
check("Rev B: 4x36,8 + 3x0,4 + 2x0,8", 4*36.8 + 3*0.4 + 2*0.8, 150.0)
print()
for lbl, t in [("danh nghia", TILE_NOM[2]), ("Rev B max ", TILE_REVB_MAX[2]),
               ("lo +0,5   ", TILE_LOT_P05[2])]:
    used = 2 * t + REVB['felt']
    print(f"  Sau Joker 2 lop {lbl}: 2 x {t:.3f} + ni 0,8 = {used:6.3f} "
          f"/ hoc 24,5 -> du {24.5-used:+.3f}")
print()
print(f"  Hoc phu 58 x 78..80 : 4 quan du phong xep 2x2 nam ngang can "
      f"{2*TILE_REVB_MAX[0]:.1f} x {2*TILE_REVB_MAX[1]:.1f} (quan max) "
      f"/ {2*TILE_LOT_P05[0]:.1f} x {2*TILE_LOT_P05[1]:.1f} (lo +0,5)")
note(True, "Hoc phu chua duoc 4 quan du phong -> bo 156 quan chuan thi truong My.")
note(False, "Ranh Joker sau 24,5 chi ho 2,3 mm be ngang - khong nhat duoc quan ra.")
note(False, "Hoc xuc xac 58 x 75 de 4 vien chay tu do; can 4 o 18x18 sau 12 dang 2x2.")


print()
print("=" * 78)
print("5. NAP HAI CANH & MONG XOAY (HD-01)")
print("=" * 78)
leaf_w = REVB['lid_leaf'][0]
check("2 x 176,7 + khe 0,6", 2 * leaf_w + REVB['seam_gap'], REVB['overall'][0])
ang = math.degrees(math.atan((REVB['lid_t_hinge'] - REVB['lid_t_seam']) / leaf_w))
check("Goc vat mat duoi nap (Rev B ghi 3,24 do)", ang, 3.24, 0.005)
stack = 2 * 0.3 + 0.2
print(f"  Stack dung sai: 2 x 176,7 +/-0,3 + 0,6 +/-0,2 = "
      f"{2*leaf_w+REVB['seam_gap']:.1f} +/-{stack:.1f}   (khop QA-01 phu bi X/Y +/-0,8)")
note(False, "Nhung than cung la 354 +/-0,8 -> truong hop xau lech 1,6 mm, "
            "vien nap thut vao 0,8/ben. Nen dung sai QUAN HE (dong mep +/-0,3), "
            "khong phai hai tri tuyet doi doc lap.")

run = REVB['knuckles'] * REVB['knuckle_len'] + (REVB['knuckles'] - 1) * REVB['knuckle_gap']
print()
check("Chieu dai mong hoat dong 7x44 + 6x1", run, 314)
pitch = REVB['knuckle_len'] + REVB['knuckle_gap']
for n in range(1, REVB['knuckles'] + 1):
    a = (n - 1) * pitch
    print(f"  mat mong {n} ({'THAN' if n % 2 else 'NAP '}) : {a:6.1f} - {a+REVB['knuckle_len']:6.1f}")
print(f"  Chieu dai chiu luc cua nap = 3 x 44 = 132 / 350 mm ({132/350*100:.0f}%)")
clr = REVB['pin_hole_d'] - REVB['pin_d']
print(f"\n  Khe chot: lo {REVB['pin_hole_d']} - chot {REVB['pin_d']} = {clr:.2f} mm duong kinh "
      f"(0,30..0,40 voi dung sai) -> ro")
print(f"  Do manh chot: {REVB['pin_len']}/{REVB['pin_d']} = {REVB['pin_len']/REVB['pin_d']:.0f} : 1")
note(False, f"Chot Ø6 x 322 va lo khoan 322 mm khong kha thi; tach thanh 2 chot x 160.")
# kiem tra phuong an 2 chot
pinA = (-4, 156); pinB = (318, 158)
k4 = ((4 - 1) * pitch, (4 - 1) * pitch + REVB['knuckle_len'])
engA = pinA[1] - k4[0]; engB = k4[1] - pinB[1]
print(f"  Phuong an 2 chot x 160: A {pinA[0]}..{pinA[1]}, B {pinB[1]}..{pinB[0]}")
print(f"    mat mong 4 (NAP) {k4[0]:.0f}-{k4[1]:.0f}: chot A an {engA:.0f} mm, chot B an {engB:.0f} mm"
      f"  -> khop lien tuc, khong va nhau (khe {pinB[1]-pinA[1]:.0f} mm)")
note(engA > 15 and engB > 15 and pinB[1] > pinA[1],
     "Phuong an 2 chot giu duoc lien tuc khop tai mat mong giua.")


print()
print("=" * 78)
print("6. CHUOI Z - KHOANG RONG BEN TRONG")
print("=" * 78)
foot, bot, tray_h = REVB['foot'], REVB['body_bottom'], REVB['tray_outer'][2]
floor = foot + bot
tray_top = floor + 2 * tray_h
print(f"  san trong = chan {foot} + day {bot} = Z{floor}")
print(f"  dinh chong 2 khay = Z{floor} + 2 x {tray_h} = Z{tray_top}")
rim_hinge = foot + REVB['body_h_hinge']
rim_seam = foot + REVB['body_h_seam']
check("Phu bi Z tai mong: 2 + 60 + 18", rim_hinge + REVB['lid_t_hinge'], REVB['overall'][2])
check("Phu bi Z tai khe giua: 2 + 70 + 8", rim_seam + REVB['lid_t_seam'], REVB['overall'][2])
print(f"  RONG tren khay tai mong    : Z{rim_hinge} - Z{tray_top} = {rim_hinge-tray_top:.0f} mm")
print(f"  RONG tren khay tai khe giua: Z{rim_seam} - Z{tray_top} = {rim_seam-tray_top:.0f} mm")
note(False, "14-24 mm rong khong duoc giao nhiem vu, khong co khoa nap, khong co "
            "chi tiet ep khay -> khay va quan se xoc khi van chuyen.")

print()
print("  --- Phuong an ha chieu cao (de xuat luc review; da duoc thay bang dac ta o muc 9) ---")
CLR = 1.0
rimC = tray_top + CLR
bodyC_hinge = rimC - foot
lidC_out = rimC + REVB['lid_t_hinge']
bodyC_seam = lidC_out - REVB['lid_t_seam'] - foot
print(f"  vanh than tai mong Z{rimC:.0f} -> chieu cao than {bodyC_hinge:.0f}")
print(f"  vanh than tai khe giua Z{lidC_out-REVB['lid_t_seam']:.0f} -> chieu cao than {bodyC_seam:.0f}")
print(f"  PHU BI MOI = 354 x 350 x {lidC_out:.0f}   (giam {REVB['overall'][2]-lidC_out:.0f} mm)")
angC = math.degrees(math.atan((bodyC_seam - bodyC_hinge) / leaf_w))
print(f"  goc vat bu tren dinh than = {angC:.3f} do (khop goc nap 3,240 do)")
spine = (lidC_out - REVB['lid_t_seam']) - (floor + REVB['ac_outer'][2])
print(f"  song noi giua tren AC-01 = Z{lidC_out-REVB['lid_t_seam']:.0f} - Z{floor+REVB['ac_outer'][2]:.0f} "
      f"= {spine:.0f} mm  (do dau canh nap + ep khay + lam tay nam)")
print("\n  Khe con lai duoi mat nap (Rev C) tren khoang khay trai:")
for X in [10, 50, 90, 136, 177]:
    z = rimC + (lidC_out - REVB['lid_t_seam'] - rimC) * X / leaf_w
    print(f"    X={X:5.1f}  mat duoi nap Z={z:6.2f}   ho tren dinh khay (Z48) = {z-48:5.2f}")


print()
print("=" * 78)
print("7. GIAN NO DO AM (tiep tuyen ~0,20 % / 1 % MC)")
print("=" * 78)
for dim, label in [(leaf_w, "mot canh nap ngang tho"),
                   (350, "than ngang 350"),
                   (126, "khoang khay rong 126"),
                   (114, "long khay rong 114")]:
    row = "  ".join(f"dMC {d}% -> {dim*0.002*d:5.2f}" for d in (2, 3, 5))
    print(f"  {label:24s} {dim:6.1f} mm : {row}")
print(f"\n  Hai canh nap no ra tai khe giua khi dMC=3%: "
      f"2 x {leaf_w*0.002*3:.2f} = {2*leaf_w*0.002*3:.2f} mm  vs khe {REVB['seam_gap']} mm")
note(2 * leaf_w * 0.002 * 3 < REVB['seam_gap'],
     "Khe rap giua 0,6 mm khong hap thu noi gian no cua nap go dac -> "
     "BAT BUOC veneer tren loi on dinh, hoac mo khe >= 2,5 mm.")


print()
print("=" * 78)
print("8. KIEM TOAN SUC CHUA")
print("=" * 78)
check("4 khay x (3 hang x 12 quan)", 4 * 3 * 12, 144)
check("Joker 4/lop x 2 lop", 4 * 2, 8)
check("TONG", 4 * 3 * 12 + 4 * 2, 152)
print(f"  + 4 quan du phong o hoc phu (de xuat) -> {152+4} quan")


print()
print("=" * 78)
print("9. DOI CHIEU Rev B  <->  DAC TA DA CHOT (tools/box_spec.py)")
print("=" * 78)
print(f"  {'hang muc':24s}{'Rev B':>22s}{'da chot':>26s}   nguyen nhan doi")
CMP = [
  ("Chuoi X (be rong)", "10+126+6+70+6+126+10",
   f"{S['WALL_HINGE']:.0f}+{S['BAY']:.0f}+{S['DIV']:.0f}+{S['AC_BAY']:.0f}+"
   f"{S['DIV']:.0f}+{S['BAY']:.0f}+{S['WALL_HINGE']:.0f}",
   "hoc am hai tay: sau 12 + thanh sau 6"),
  ("Phu bi X", "354", f"{S['W']:.0f}", ""),
  ("Phu bi Y", "350", f"{S['Y_OA']:.0f}", "hoc am chuyen sang vach trai/phai -> Y khong doi"),
  ("Phu bi Z", "80", f"{S['Z_OA']:.0f}", "ha chieu cao + bo song khoa + day 6"),
  ("Day hop", "8", f"{BS.BOT:.0f}", "giam can; kiem uon he so 864x"),
  ("Day nap", "18 tai mong / 8 tai khe giua", f"{BS.T_LID:.0f} deu, khong vat",
   "truc ra arris -> be day nap khong con rang buoc ban le"),
  ("Goc vat mat duoi nap", "3,24 do", f"{S['ANG']:.3f} do (khong vat)",
   "vat chi de canh mo nam ngang; nay canh mo da nam ngang san"),
  ("Khe rap giua", "0,6", f"{BS.SEAM}", "gian no khung go dac o dMC 5 %"),
  ("Canh nap", "176,7 tam lien", f"{S['LW']:.2f} khung + tam tha",
   f"Nu dac dong khe rap giua o dMC {BS.seam_close_dmc('nu'):.2f} %"),
  ("Ban le", "mat mong go + chot O6 x 322",
   f"{BS.N_KN} mat mong go x {BS.KN_LEN:.0f}, ong O{2*S['R_KN']:.1f}, chot go O{BS.KN_PIN:.0f}",
   "truc dua ra arris -> khong con ong go"),
  ("Truc xoay", "giua be day nap", f"({S['PIN_X']:.0f} , {S['PIN_Z']:.0f}) tren arris",
   "hinge_kinematics.py muc 1"),
  ("Ranh Joker", "150", f"{BS.AC_JOKER[1]:.0f}", "lo quan +0,5 thi khe am"),
  ("Khay phu kien AC-01", "325 x 68 x 38",
   f"{S['AC_L']:.0f} x {S['AC_W_OUT']:.0f} x {BS.AC_H:.0f}", ""),
]
for a, x, y, why in CMP:
    print(f"  {a:24s}{x:>22s}{y:>26s}   {why}")
print()
print(f"  Khoi luong: {BS.mass_of(S,'cocobolo')[2]:.2f} kg (khay cocobolo) / "
      f"{BS.mass_of(S,'loi on dinh')[2]:.2f} kg (khay loi on dinh)")
print(f"  Rev B khong tinh khoi luong o bat ky sheet nao.")

print()
print("=" * 78)
print(f"KET LUAN: {len(FAILS)} loi so hoc, {len(WARNS)} canh bao thiet ke")
print("=" * 78)
for f in FAILS:
    print(f"  LOI  : {f}")
for w in WARNS:
    print(f"  CANH BAO: {w}")
raise SystemExit(1 if FAILS else 0)
