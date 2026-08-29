#!/usr/bin/env python3
"""
Dong hoc ban le canh nap — giai diem con treo tu review Rev B §2.5.
HD-01 ghi "goc mo 180 do" nhung khong dinh nghia CAO DO TRUC XOAY, nen khong
biet canh mo ra nam o dau. Script nay suy ra vi tri truc tu rang buoc, quet
0-180 do kiem va cham, roi tinh he qua.

Chay: python3 tools/hinge_kinematics.py
He toa do: Z=0 mat ban, X=0 mat ngoai vach trai. Mat cat trong mat phang X-Z.
Moi tri so hinh hoc lay tu tools/box_spec.py — script nay khong go cung so nao.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B
def hr(t): print("\n"+"="*78+"\n"+t+"\n"+"="*78)

S = B.derive()
Z_RIM, Z_LID, Z_SEAM = S['Z_RIM'], S['Z_LID'], S['Z_SEAM']
Z_FLOOR, Z_TRAY_TOP  = S['Z_FLOOR'], S['Z_TRAY_TOP']
LW, W = S['LW'], S['W']
R_KN, PX, PZ = B.R_KN, B.R_KN, Z_RIM + B.R_KN
HAS_SPINE = (S['HANDLE'] == 'A')
SPINE_PROUD = S['Z_PROUD']

hr("1. SUY RA VI TRI TRUC XOAY TU RANG BUOC")
print(f"  Phuong an xach da chot: {S['HANDLE']}"
      f"  ({'song khoa + quai da' if HAS_SPINE else 'hoc am hai tay, KHONG co song khoa'})")
print("  Rang buoc:")
C = [("R1", "Chot phai NAM TRONG go ca canh nap lan than - khong duoc lo ra ngoai"),
     ("R2", f"Mat mong la ong go quanh lo O{B.D_PIN}; ban kinh ong = nua be day nap = {R_KN:.0f}"),
     ("R3", f"Ong go phai tiep tuyen ca mat tren (Z{Z_LID:.0f}) lan mat duoi "
            f"(Z{Z_RIM:.0f}) cua nap"),
     ("R4", "Trong hanh trinh 0-180 do, canh khong duoc va vao than hop hay mat ban")]
for a, b in C: print(f"   {a}  {b}")
print(f"\n  R2+R3 => tam ong o giua be day nap: Pz = {Z_RIM:.0f} + {R_KN:.0f} = {PZ:.0f}")
print(f"          va cach mat ngoai than dung mot ban kinh: Px = {PX:.0f}")
print(f"  => TRUC XOAY P = ({PX:.0f} , {PZ:.0f})   (mm tinh tu mat ngoai vach trai / mat ban)")
print(f"\n  Chi R2+R3 da khoa het bac tu do. Trong ban truoc, rang buoc 'song khoa khong")
print(f"  duoc cham mat ban' duoc dung de bac bo ho nghiem 'canh nam phang tren ban'.")
print(f"  Phuong an C bo song khoa, nen lap luan do khong con — nhung KET LUAN khong doi:")
print(f"  muon ha truc thi phai pha R2 hoac R3, tuc la de ong go loi ra khoi be day nap.")

def rot(p, th):
    x, z = p[0]-PX, p[1]-PZ
    c, s = math.cos(math.radians(th)), math.sin(math.radians(th))
    return (PX + x*c - z*s, PZ + x*s + z*c)

hr("2. CANH NAP NAM O DAU KHI MO 180 DO")
pts = {'mep mong, mat tren'     : (2*R_KN, Z_LID),
       'mep mong, mat duoi'     : (2*R_KN, Z_RIM),
       'mep khe giua, mat tren' : (LW, Z_LID),
       'mep khe giua, mat duoi' : (LW, Z_SEAM)}
if HAS_SPINE:
    pts['day song khoa'] = (LW - B.SPINE_W/2, Z_LID + SPINE_PROUD)
print(f"  {'diem':26s}{'dong X':>9s}{'dong Z':>9s}   {'mo 180: X':>10s}{'Z':>9s}")
op = {}
for k, p in pts.items():
    q = rot(p, 180); op[k] = q
    print(f"  {k:26s}{p[0]:9.1f}{p[1]:9.1f}   {q[0]:10.1f}{q[1]:9.1f}")
z_bot  = min(q[1] for q in op.values())
reach  = abs(op['mep khe giua, mat tren'][0])
print(f"\n  => Canh mo ra nam NGANG, mat duoi phang tai Z = {z_bot:.0f}")
print(f"     dung bang cao do VANH THAN ({Z_RIM:.0f}) -> canh nhu hai canh chim")
print(f"     chia ra tu mep tren hop. Vuon ra {reach:.2f} mm.")
print(f"     Mat tren canh mo doc tu Z{op['mep mong, mat duoi'][1]:.0f} (sat hop) xuong "
      f"Z{op['mep khe giua, mat duoi'][1]:.0f} (dau ngoai)")
print(f"     = doc {S['ANG']:.3f} do NGHIENG VE PHIA NGUOI CHOI. Tot cho khay bo bai.")
print(f"     (Do doc nay = dung goc vat nap, tinh tren doan vat that {S['TAPER']:.2f} mm")
print(f"      chu khong tren ca be rong canh {LW:.2f} — day la cho ban truoc tinh nham.)")

hr("3. QUET 0-180 DO — KIEM VA CHAM")
def leaf_pts(th):
    o = []
    for X in [2*R_KN, 40, 80, 120, LW]:
        zl = Z_RIM + (Z_SEAM - Z_RIM)*(X - 2*R_KN)/(LW - 2*R_KN)
        o += [rot((X, zl), th), rot((X, Z_LID), th)]
    if HAS_SPINE:
        o.append(rot((LW - B.SPINE_W/2, Z_LID + SPINE_PROUD), th))
    return o
EPS = 0.05      # canh dong TI len vanh than la tiep xuc chu y, khong phai va cham;
                # chi bao loi khi diem bien XUYEN vao khoi dac qua EPS.
def inside(x, z, x0, x1, z0, z1):
    return x0 + EPS < x < x1 - EPS and z0 + EPS < z < z1 - EPS
def hits_body(p):
    x, z = p
    if z < -EPS:                                                       return "MAT BAN"
    if inside(x, z, 0, S['WALL_HINGE'], Z_FLOOR, Z_RIM):               return "VACH THAN"
    if inside(x, z, 0, W, B.FOOT, Z_FLOOR):                            return "DAY HOP"
    if inside(x, z, S['WALL_HINGE'], S['WALL_HINGE'] + S['BAY'],
              Z_FLOOR, Z_TRAY_TOP):                                    return "KHAY"
    return None
bad = [(i, h, p) for i in range(181) for p in leaf_pts(i) if (h := hits_body(p))]
n_pts = len(leaf_pts(0))
print(f"  Quet 1 do mot buoc, {n_pts} diem bien tren canh"
      f"{' + day song khoa' if HAS_SPINE else ''}.")
if bad:
    print(f"  VA CHAM: {len(bad)} truong hop, vi du {bad[:3]}")
else:
    zmin = min(min(p[1] for p in leaf_pts(i)) for i in range(181))
    print(f"  Khong va cham o bat ky goc nao.")
    print(f"  Diem thap nhat cua canh trong ca hanh trinh: Z = {zmin:.1f} mm")
    if not HAS_SPINE:
        print(f"  Bo song khoa nen canh KHONG BAO GIO xuong duoi vanh than. Ho mat ban")
        print(f"  luon >= {zmin:.0f} mm — rang buoc mat ban bien mat hoan toan.")

hr("4. KHONG CO MAT CHAN 180 DO TU NHIEN")
print("  O 180 do khong be mat nao cua canh gap be mat nao cua than. Khop chot khong")
print("  chiu duoc momen quanh chinh truc no -> canh se quay tiep va rot xuong neu")
print("  khong co CHAN.\n")
print("  Giai: phay MOT MAT PHANG tren ong go cua ca hai ben (chan trong long mong,")
print("  hoan toan khuat). Khi mo het, hai mat phang ap vao nhau.")
r_flat, w_flat = 6.0, 8.0
A_flat = w_flat*B.KN_LEN*B.KN_LID
m_leaf = ((S['V']['khung nap'] + S['V']['mat mong nap'])/2/1e6*B.RHO['cocobolo']
          + S['V']['tam Nu']/2/1e6*B.RHO['Nu go do'])
arm = (2*R_KN + LW)/2 - PX
M_self = m_leaf*9.81*arm/1000
print(f"\n  Mat chan: rong {w_flat:.0f} x dai {B.KN_LEN:.0f} x {B.KN_LID} mat mong"
      f" = {A_flat:.0f} mm2, ban kinh {r_flat:.0f}")
print(f"  Khoi luong 1 canh {m_leaf:.2f} kg, canh tay don toi trong tam {arm:.0f} mm")
worst = None
for lbl, extra, ex_arm in [("chi trong luong canh", 0, 0),
                           ("+ 2 kg quan bo tren khay", 2.0, LW/2),
                           ("+ nguoi choi ty 5 kg o mep ngoai", 5.0, LW - PX)]:
    M = M_self + extra*9.81*ex_arm/1000
    F = M/(r_flat/1000)
    worst = F/A_flat
    print(f"   {lbl:34s} M={M:5.2f} N.m -> F={F:6.0f} N -> {F/A_flat:5.2f} MPa")
print(f"  Cho phep nen ngang tho cocobolo ~{B.C_PERP:.0f} MPa -> he so an toan "
      f">= {B.C_PERP/worst:.0f}x")

hr("5. DO VONG DAU CANH KHI MO")
clr = 0.25
slop = clr/B.KN_LEN
tip = LW - PX
print(f"  Khe chot 0,20-0,25 mm duong kinh trong ong dai {B.KN_LEN:.0f} mm")
print(f"  -> goc ro = {clr:.2f}/{B.KN_LEN:.0f} = {slop*1000:.2f} mrad")
print(f"  -> vong dau canh = {slop*tip:.2f} mm o mut {tip:.0f} mm")
print(f"  Sut mat chan duoi tai 5 kg: {worst/1000*3:.3f} mm (bo qua)")
print(f"  => DAC TINH KIEM: vong dau canh mo <= 1,5 mm duoi tai 5 kg tai mep ngoai.")
print(f"     Muon chat hon thi siet khe chot, khong phai tang tiet dien.")

hr("6. VACH BAN LE 18 — CHUOI X DA CHOT 370")
print(f"  Ong go ban kinh {R_KN:.0f} -> mat mong ben THAN cung phai day {2*R_KN:.0f} mm.")
print(f"  Vach 10 mm cua Rev B: lo O{B.D_PIN} chi con {(10-B.D_PIN)/2:.1f} mm thanh moi ben."
      f" Khong dung duoc.")
print(f"  Vach {S['WALL_HINGE']:.0f} mm: thanh quanh lo {R_KN - B.D_PIN/2:.1f} mm moi ben.\n")
print(f"  Chuoi X Rev B  : 10 + 126 + 6 + 70 + 6 + 126 + 10 = 354  (khong dung duoc)")
print(f"  Chuoi X DA CHOT: {S['WALL_HINGE']:.0f} + {S['BAY']:.0f} + {S['DIV']:.0f}"
      f" + {S['AC_BAY']:.0f} + {S['DIV']:.0f} + {S['BAY']:.0f} + {S['WALL_HINGE']:.0f}"
      f" = {W:.0f}")
print(f"  So sanh ba phuong an be rong: tools/width_options.py")

hr("7. CHOT LAI CAC TRI SO CHO HD-01")
go, t, tot = B.mass_of(S, 'loi on dinh')
for a, b in [("Truc xoay", f"X = {PX:.0f} tu mat ngoai vach, Z = {PZ:.0f} tu mat ban"),
             ("Ban kinh ong go", f"R{R_KN:.0f}, tiep tuyen mat tren va mat duoi nap"),
             ("Day vach ban le", f"{S['WALL_HINGE']:.0f} mm (tu 10) - thanh quanh lo "
                                 f"{R_KN - B.D_PIN/2:.1f} mm"),
             ("Lo chot", f"O{B.D_PIN:.2f} +0,05/0 ; chot O6,00 -0,05 (khe 0,20-0,25)"),
             ("Chuoi mat mong", f"{B.N_KN} mat x {B.KN_LEN:.0f}, buoc {B.KN_PITCH:.0f},"
                                f" chuoi {S['KN_RUN']:.0f} mm giua long {B.INNER_Y:.0f}"),
             ("Mat chan 180 do", f"phay phang rong {w_flat:.0f}, ban kinh {r_flat:.0f},"
                                 f" hai ben, khuat trong mong"),
             ("Goc mo", "180 do +0/-2 do, chan bang mat phang trong mong"),
             ("Vi tri canh khi mo", f"nam ngang, mat duoi Z{z_bot:.0f} (= vanh than),"
                                    f" vuon ra {reach:.0f}"),
             ("Do vong cho phep", "<= 1,5 mm tai mep ngoai duoi tai 5 kg"),
             ("Phu bi", f"{W:.0f} x {S['Y_OA']:.0f} x {S['Z_OA']:.0f}"),
             ("Khoi luong", f"{tot:.2f} kg (khay loi on dinh) / "
                            f"{B.mass_of(S,'cocobolo')[2]:.2f} kg (khay cocobolo)")]:
    print(f"   {a:20s}: {b}")
