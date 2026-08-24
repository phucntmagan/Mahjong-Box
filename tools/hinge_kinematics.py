#!/usr/bin/env python3
"""
Dong hoc ban le canh nap — giai diem con treo tu review Rev B §2.5.
HD-01 ghi "goc mo 180 do" nhung khong dinh nghia CAO DO TRUC XOAY, nen khong
biet canh mo ra nam o dau. Script nay suy ra vi tri truc tu rang buoc, quet
0-180 do kiem va cham, roi tinh he qua.

Chay: python3 tools/hinge_kinematics.py
He toa do: Z=0 mat ban, X=0 mat ngoai vach trai. Mat cat trong mat phang X-Z.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B
def hr(t): print("\n"+"="*78+"\n"+t+"\n"+"="*78)

# ---------------------------------------------------------------- hinh hoc
Z_FOOT, Z_FLOOR, Z_RIM, Z_LID = 2.0, 10.0, 49.0, 67.0
T_HINGE, T_SEAM = 18.0, 12.0          # day nap tai mong / tai khe giua
LW = 176.7                            # be rong canh nap (truoc khi doi)
SPINE_PROUD = 16.0                    # song khoa noi tren mat nap
Z_TRAY_TOP = 48.0

hr("1. SUY RA VI TRI TRUC XOAY TU RANG BUOC")
print("  Rang buoc:")
C = [("R1", "Chot phai NAM TRONG go ca canh nap lan than - khong duoc lo ra ngoai"),
     ("R2", "Mat mong la ong go quanh lo Ø6,2; ban kinh ong = nua be day nap = 9"),
     ("R3", "Ong go phai tiep tuyen ca mat tren (Z67) lan mat duoi (Z49) cua nap"),
     ("R4", "Khi mo 180 do, SONG KHOA (noi 16) chuc xuong - khong duoc cham mat ban"),
     ("R5", "Trong hanh trinh 0-180 do, canh khong duoc va vao than hop")]
for a,b in C: print(f"   {a}  {b}")

R_KN = T_HINGE/2
PZ = Z_RIM + R_KN
PX = R_KN
print(f"\n  R2+R3 => tam ong o giua be day nap: Pz = {Z_RIM:.0f} + {R_KN:.0f} = {PZ:.0f}")
print(f"          va cach mat ngoai than dung mot ban kinh: Px = {PX:.0f}")
print(f"  => TRUC XOAY P = ({PX:.0f} , {PZ:.0f})   (mm tinh tu mat ngoai vach trai / mat ban)")

def rot(p, th):
    """Quay diem p quanh P mot goc th (do), chieu mo canh."""
    x, z = p[0]-PX, p[1]-PZ
    c, s = math.cos(math.radians(th)), math.sin(math.radians(th))
    return (PX + x*c - z*s, PZ + x*s + z*c)

hr("2. CANH NAP NAM O DAU KHI MO 180 DO")
pts = {'mep mong, mat tren' : (2*R_KN, Z_LID),
       'mep mong, mat duoi' : (2*R_KN, Z_RIM),
       'mep khe giua, mat tren' : (LW, Z_LID),
       'mep khe giua, mat duoi' : (LW, Z_LID-T_SEAM),
       'day song khoa'      : (LW-22, Z_LID+SPINE_PROUD)}
print(f"  {'diem':26s}{'dong X':>9s}{'dong Z':>9s}   {'mo 180: X':>10s}{'Z':>9s}")
op={}
for k,p in pts.items():
    q = rot(p, 180); op[k]=q
    print(f"  {k:26s}{p[0]:9.1f}{p[1]:9.1f}   {q[0]:10.1f}{q[1]:9.1f}")

z_bot = min(q[1] for k,q in op.items() if 'song' not in k)
z_spine = op['day song khoa'][1]
print(f"\n  => Canh mo ra nam NGANG, mat duoi phang tai Z = {z_bot:.0f}")
print(f"     dung bang cao do VANH THAN ({Z_RIM:.0f}) -> canh nhu hai canh chim")
print(f"     chia ra tu mep tren hop. Vuon ra {abs(op['mep khe giua, mat tren'][0]):.1f} mm.")
print(f"     Mat tren canh mo doc tu Z{op['mep mong, mat duoi'][1]:.0f} (sat hop) xuong "
      f"Z{op['mep khe giua, mat duoi'][1]:.0f} (dau ngoai)")
print(f"     = doc {math.degrees(math.atan((T_HINGE-T_SEAM)/LW)):.2f} do NGHIENG VE PHIA NGUOI CHOI. Tot cho khay bo bai.")
print(f"\n  R4: day song khoa o Z = {z_spine:.0f} -> ho mat ban {z_spine:.0f} mm. DAT.")
print(f"      (neu ha truc de canh nam han xuong ban thi song khoa dam xuong mat ban - BAT KHA)")

hr("3. QUET 0-180 DO — KIEM VA CHAM")
def leaf_pts(th):
    o=[]
    for X in [2*R_KN, 40, 80, 120, LW]:
        zl = Z_RIM + (Z_LID-T_SEAM-Z_RIM)*(X-2*R_KN)/(LW-2*R_KN)
        o += [rot((X, zl), th), rot((X, Z_LID), th)]
    o.append(rot((LW-22, Z_LID+SPINE_PROUD), th))
    return o
def hits_body(p):
    x,z = p
    if z < 0: return "MAT BAN"
    if 0 <= x <= 10 and Z_FLOOR <= z <= Z_RIM: return "VACH THAN"
    if 0 <= x <= 354 and Z_FOOT <= z <= Z_FLOOR: return "DAY HOP"
    if 10 <= x <= 136 and Z_FLOOR <= z <= Z_TRAY_TOP: return "KHAY"
    return None
bad=[]
for i in range(0,181):
    for p in leaf_pts(i):
        h = hits_body(p)
        if h: bad.append((i,h,p))
print(f"  Quet 1 do mot buoc, 11 diem bien tren canh + day song khoa.")
if bad:
    print(f"  VA CHAM: {len(bad)} truong hop, vi du {bad[:3]}")
else:
    print(f"  Khong va cham o bat ky goc nao.  Khoang cach nho nhat toi mat ban:")
    zmin = min(min(p[1] for p in leaf_pts(i)) for i in range(181))
    print(f"    Z_min = {zmin:.1f} mm (tai day song khoa khi mo het)")

hr("4. VAN CHUA GIAI: KHONG CO MAT CHAN 180 DO TU NHIEN")
print("  O 180 do khong co be mat nao cua canh gap be mat nao cua than.")
print("  Khop chot khong chiu duoc momen quanh chinh truc no -> canh se quay tiep")
print("  va rot xuong neu khong co CHAN.")
print("\n  Giai: phay MOT MAT PHANG tren ong go cua ca hai ben (chan trong long mong,")
print("  hoan toan khuat). Khi mo het, hai mat phang ap vao nhau.")
r_flat, w_flat, l_flat, n_kn = 6.0, 8.0, 44.0, 3
A = w_flat*l_flat*n_kn
m_leaf = (B.V['khung nap']/2/1e6*B.RHO['cocobolo'] + B.V['tam Nu']/2/1e6*B.RHO['Nu go do'])
arm = ((2*R_KN)+LW)/2 - PX
M_self = m_leaf*9.81*arm/1000
print(f"\n  Mat chan: rong {w_flat:.0f} x dai {l_flat:.0f} x {n_kn} mat mong = {A:.0f} mm2, ban kinh {r_flat:.0f}")
print(f"  Khoi luong 1 canh {m_leaf:.2f} kg, canh tay don toi trong tam {arm:.0f} mm")
for lbl, extra, ex_arm in [("chi trong luong canh", 0, 0),
                           ("+ 2 kg quan bo tren khay", 2.0, LW/2),
                           ("+ nguoi choi ty 5 kg o mep ngoai", 5.0, LW-PX)]:
    M = M_self + extra*9.81*ex_arm/1000
    F = M/(r_flat/1000)
    print(f"   {lbl:34s} M={M:5.2f} N.m -> F={F:6.0f} N -> {F/A:5.2f} MPa")
print(f"  Cho phep nen ngang tho cocobolo ~14 MPa -> he so an toan >= {14/((M_self+5*9.81*(LW-PX)/1000)/(r_flat/1000)/A):.0f}x")

hr("5. DO VONG DAU CANH KHI MO")
clr, kn_len = 0.25, 44.0
slop = clr/kn_len
tip = LW - PX
print(f"  Khe chot 0,20-0,25 mm duong kinh trong ong dai {kn_len:.0f} mm")
print(f"  -> goc ro = {clr:.2f}/{kn_len:.0f} = {slop*1000:.2f} mrad")
print(f"  -> vong dau canh = {slop*tip:.2f} mm o mut {tip:.0f} mm")
print(f"  Sut mat chan duoi tai 5 kg: {(M_self+5*9.81*(LW-PX)/1000)/(r_flat/1000)/A/1000*3:.3f} mm (bo qua)")
print(f"  => DAC TINH KIEM: vong dau canh mo <= 1,5 mm duoi tai 5 kg tai mep ngoai.")
print(f"     Muon chat hon thi siet khe chot, khong phai tang tiet dien.")

hr("6. HE QUA BAT BUOC: VACH BAN LE PHAI DAY 18, KHONG PHAI 10")
print(f"  Ong go ban kinh {R_KN:.0f} -> mat mong ben THAN cung phai day {2*R_KN:.0f} mm.")
print(f"  Vach hien tai 10 mm: lo Ø6,2 chi con {(10-6.2)/2:.1f} mm thanh moi ben. Khong duoc.")
print(f"\n  Chuoi X hien tai : 10 + 126 + 6 + 70 + 6 + 126 + 10 = 354")
opts = [(18,126,6,70,"khong doi gi khac"),
        (18,126,6,62,"AC-01 con 60 ngoai / 50 long - phai bo tri lai o xuc xac va hoc quan du"),
        (18,126,4,70,"vach ngan mong con 4 mm")]
print(f"\n  {'vach':>6s}{'khay':>7s}{'ngan':>7s}{'ph.kien':>9s}{'TONG':>7s}   ghi chu")
for w,t,d,a,note in opts:
    tot = 2*w+2*t+2*d+a
    print(f"  {w:6d}{t:7d}{d:7d}{a:9d}{tot:7d}   {note}")
print(f"\n  => Khuyen nghi 370 x 350: khong dong toi bo tri long hop da chot.")
print(f"     370 x 350 gan vuong, ty le nhin con dep hon 354 x 350.")
NEWW = 370.0
print(f"\n  Keo theo: canh nap {(NEWW-1.5)/2:.1f} moi ben (khe rap giua 1,5)")
print(f"            khe rap giua van o X = {NEWW/2:.0f}; song khoa X {NEWW/2-22:.0f}..{NEWW/2+22:.0f}")
dV = ((NEWW-354)*350*8                      # day rong them
      + 2*(2*R_KN-10)*39*330                # vach ban le day them
      + 2*(NEWW-354)*10*44)                 # vach truoc/sau dai them
dm = dV/1e6*B.RHO['cocobolo']
print(f"            the tich go +{dV/1000:.0f} cm3 -> +{dm:.2f} kg -> tong "
      f"{B.mass('cocobolo')[2]+dm:.2f} kg, tai TK {(B.mass('cocobolo')[2]+dm)*9.81*3:.0f} N")
print(f"            Dalbergia/hop {B.dalbergia_kg('cocobolo')+dm:.2f} kg -> van 2 hop/lo")

hr("7. CHOT LAI CAC TRI SO CHO HD-01")
for a,b in [("Truc xoay", f"X = {PX:.0f} tu mat ngoai vach, Z = {PZ:.0f} tu mat ban"),
            ("Ban kinh ong go", f"R{R_KN:.0f}, tiep tuyen mat tren va mat duoi nap"),
            ("Day vach ban le", f"{2*R_KN:.0f} mm (tu 10) - thanh quanh lo {R_KN-3.1:.1f} mm"),
            ("Lo chot", "Ø6,20 +0,05/0 ; chot Ø6,00 -0,05 (khe 0,20-0,25)"),
            ("Mat chan 180 do", f"phay phang rong {w_flat:.0f}, ban kinh {r_flat:.0f}, tren ca hai ben, khuat trong mong"),
            ("Goc mo", "180 do +0/-2 do, chan bang mat phang trong mong"),
            ("Vi tri canh khi mo", f"nam ngang, mat duoi Z{z_bot:.0f} (= vanh than), vuon ra {abs(op['mep khe giua, mat tren'][0]):.0f}"),
            ("Do vong cho phep", "<= 1,5 mm tai mep ngoai duoi tai 5 kg"),
            ("Phu bi moi", f"{NEWW:.0f} x 350 x 83")]:
    print(f"   {a:22s}: {b}")
