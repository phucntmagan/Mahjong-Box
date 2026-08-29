#!/usr/bin/env python3
"""
Dong hoc ban le canh nap.
Chay: python3 tools/hinge_kinematics.py
He toa do: Z=0 mat ban, X=0 mat ngoai vach trai. Mat cat trong mat phang X-Z.
Moi tri so hinh hoc lay tu tools/box_spec.py.

BAN NAY THAY HOAN TOAN BAN TRUOC. Ban truoc dat truc xoay o GIUA BE DAY nap va
suy ra ong go ban kinh bang nua be day nap. Rang buoc do la TU DAT RA, khong
phai hinh hoc — xem muc 1.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B
def hr(t): print("\n"+"="*78+"\n"+t+"\n"+"="*78)

S = B.derive()
Z_RIM, Z_LID = S['Z_RIM'], S['Z_LID']
Z_FLOOR, Z_TRAY_TOP = S['Z_FLOOR'], S['Z_TRAY_TOP']
LW, W, T = S['LW'], S['W'], B.T_LID
PX, PZ = S['PIN_X'], S['PIN_Z']

def rot(p, th):
    x, z = p[0]-PX, p[1]-PZ
    c, s = math.cos(th), math.sin(th)
    return (PX + x*c - z*s, PZ + x*s + z*c)
def ang(p):
    return math.degrees(math.atan2(p[1]-PZ, p[0]-PX))

# ==========================================================================
hr("1. TRUC XOAY O DAU — VA VI SAO BAN TRUOC SAI")
print("  Rang buoc THAT SU chi co mot: trong ca hanh trinh 0-180 do, vat lieu")
print("  canh nap khong duoc cat vao vat lieu than hop.\n")
print("  KHONG lap luan bang 'cung goc' — cung goc cua hai khoi CO THE chong nhau")
print("  ma van khong dung nhau, vi con phu thuoc BAN KINH. Nen tinh thang:\n")

EPS = 0.02
def in_body(q):
    """Diem q co nam TRONG long vat lieu than hop khong (khong ke mat bien)."""
    return (EPS < q[0] < W - EPS) and (EPS < q[1] < Z_RIM - EPS)

def nose_radius(px, pz, nx=160, nz=40, dth=0.5):
    """Bo tron DAU CANH nap thanh mui tron ban kinh R quanh truc — R lon nhat con
    quay duoc het 0-180 do. Tra ve (R, so diem khong the cuu bang cach bo tron).
    R = 0 nghia la khong phai bo gi; R > 0 chinh la ban kinh ONG GO bat buoc."""
    def rot2(q, th):
        x, z = q[0]-px, q[1]-pz
        c, s = math.cos(th), math.sin(th)
        return (px + x*c - z*s, pz + x*s + z*c)
    rmin, stuck = math.inf, 0
    for i in range(nx+1):
        x = LW*i/nx
        for j in range(nz+1):
            z = Z_RIM + T*j/nz
            th = 0.0
            while th <= 180.0 + 1e-9:
                if in_body(rot2((x, z), math.radians(th))):
                    if x >= px - 1e-9: stuck += 1      # mui tron khong voi toi
                    rmin = min(rmin, math.hypot(x-px, z-pz))
                    break
                th += dth
    return (0.0 if rmin is math.inf else rmin), stuck

print(f"  Bo tron dau canh nap thanh mui tron ban kinh R quanh truc — R lon nhat")
print(f"  ma canh van quay het 0-180 do khong cham than hop:\n")
print(f"  {'dat truc o':36s}{'toa do':>14s}{'mui tron R':>13s}{'suy ra':>21s}")
res = {}
for lbl, px, pz in [("GIUA BE DAY nap (ban truoc)", T/2, Z_RIM + T/2),
                    ("CANH NGOAI TREN cua than (arris)", 0.0, Z_RIM)]:
    r, st = nose_radius(px, pz)
    res[lbl] = r
    sug = f"ONG GO O{2*r:.1f}" if r > 0.05 else "KHONG PHAI BO GI"
    print(f"  {lbl:36s}{f'({px:.1f} , {pz:.1f})':>14s}{r:10.2f} mm{sug:>21s}"
          + ("   (+{} diem khong cuu duoc)".format(st) if st else ""))
r_mid, r_arr = res["GIUA BE DAY nap (ban truoc)"], res["CANH NGOAI TREN cua than (arris)"]
print()
print(f"  Doc bang tren. Hang mot: truc o giua be day nap thi hai goc dau canh nam")
print(f"  ngoai truc, vong tron chung quet ra DI XUYEN qua vanh than; phai bo tron")
print(f"  dau canh xuong R{r_mid:.1f} moi quay duoc. Va R{r_mid:.1f} = {T:.0f}/2 dung bang")
print(f"  NUA BE DAY NAP — khong phai tinh co: mui tron phai tiep tuyen ca mat tren")
print(f"  lan mat duoi cua nap, ma hai mat do cach nhau {T:.0f} mm.")
print(f"  Cai mui tron do CHINH LA 'ong go O{2*r_mid:.0f}' cua ban truoc.")
print(f"  Nghia la: 'R = nua be day nap' khong phai mot lua chon thiet ke — no la")
print(f"  HE QUA bat buoc, mot khi da tro lo dat truc vao GIUA vat lieu.\n")
print(f"  Dat truc o ARRIS thi hai goc dau canh nap TRUNG VOI truc: ban kinh 0,")
print(f"  chung khong quet ra cai gi ca. Boc = 0. Khong ong go, khong mat mong.\n")
print(f"  QUY TAC RUT RA: truc xoay phai nam o GOC CHUNG cua hai chi tiet.")
print(f"  Truc dat sau vao trong vat lieu bao nhieu thi phai boc di bay nhieu.\n")
print(f"  Vi sao ban truoc chon giua be day nap: de canh mo nam DUNG DAI CAO DO cua")
print(f"  nap khi dong (Z{Z_RIM:.0f}..{Z_LID:.0f}). Do la mot lua chon THAM MY tu dat ra,")
print(f"  chua he duoc dat cau hoi — va chinh no ep ong go phai bang nua be day nap.")
print(f"\n  Dat truc o arris thi canh mo nam thap hon dung mot be day nap:")
print(f"    Z{Z_RIM-T:.0f}..{Z_RIM:.0f} thay vi Z{Z_RIM:.0f}..{Z_LID:.0f}.")
print(f"  Do la cai gia duy nhat, va no khong phai gia: mat TREN cua canh mo nam")
print(f"  dung Z{Z_RIM:.0f} — bang phang voi vanh than, dung cai ta can de bo bai.\n")
print(f"  CON LAI: khop brass O{B.HG_KN:.1f} van can cho. Nhung do la cho cho PHAN CUNG,")
print(f"  R{B.HG_R:.2f} — khong phai cho hinh hoc, R{T/2:.1f}. Chenh {T/2/B.HG_R:.1f} lan.")

# ==========================================================================
hr("2. CANH NAP NAM O DAU KHI MO 180 DO")
pts = {'mep ban le, mat duoi': (0.0, Z_RIM), 'mep ban le, mat tren': (0.0, Z_LID),
       'mep khe giua, mat duoi': (LW, Z_RIM), 'mep khe giua, mat tren': (LW, Z_LID)}
print(f"  {'diem':26s}{'dong X':>9s}{'dong Z':>9s}   {'mo 180: X':>10s}{'Z':>9s}")
op = {}
for k, p in pts.items():
    q = rot(p, math.pi); op[k] = q
    print(f"  {k:26s}{p[0]:9.1f}{p[1]:9.1f}   {q[0]:10.1f}{q[1]:9.1f}")
print(f"\n  Canh mo nam NGANG, mat tren phang tai Z{Z_RIM:.0f} — dung cao do VANH THAN.")
print(f"  Vuon ra {LW:.2f} mm. Mat tren canh mo chinh la mat duoi nap khi dong,")
print(f"  tuc long lom om tam Nu — khay bo bai sau {T - B.S_TOP - B.PAN_T:.1f} mm.")

# ==========================================================================
hr("3. CHAN 180 DO — TU NHIEN, KHONG PHAI PHAY THEM")
R = B.HG_R
SH, A_stop = S['STOP_H'], S['STOP_A']
print(f"  Truc khop nam DUNG tren arris nen khop O{B.HG_KN:.1f} an vao go ca hai ben.")
print(f"  Phai BO LUON hai canh arris dung R{R:.2f}: canh ngoai tren cua vach than va")
print(f"  canh ngoai duoi cua nap. Dong lai, hai duong luon khep thanh lo O{B.HG_KN:.1f} om")
print(f"  tron khop — khop chim trong duong chi goc, chi con mot soi brass manh.\n")
print(f"  O 180 do, mat canh ban le cua nap (mat phang X=0, tu Z{Z_RIM-R:.2f} xuong")
print(f"  Z{Z_RIM-T:.0f}) ap DUNG vao mat ngoai vach than (cung mat phang X=0).")
print(f"  Hai mat dong phang va cham nhau -> canh khong quay tiep duoc.\n")
m_leaf = (S['V']['khung nap']/2/1e6*B.RHO['cocobolo']
          + S['V']['tam Nu']/2/1e6*B.RHO['Nu go do'])
print(f"  Dien tich tiep xuc: {SH:.2f} x {B.LID_L:.0f} = {A_stop:.0f} mm2 — ca chieu dai canh.")
print(f"  (be day nap {T:.0f} tru {R:.2f} bo luon; bo luon lay mat {100*R/T:.0f} % mat chan)")
print(f"  {'truong hop tai':36s}{'M (N.m)':>10s}{'F (N)':>9s}{'MPa':>8s}{'he so':>8s}")
arm_r = 2*SH/3         # hop luc ap suat tren mat chan, xap xi 2/3 chieu cao chan
for lbl, extra, ex_arm in [("chi trong luong canh", 0.0, 0.0),
                           ("+ 2 kg quan bo tren khay", 2.0, LW/2),
                           ("+ nguoi choi ty 5 kg o mep ngoai", 5.0, LW)]:
    M = m_leaf*9.81*(LW/2)/1000 + extra*9.81*ex_arm/1000
    F = M/(arm_r/1000)
    sig = F/A_stop
    print(f"  {lbl:36s}{M:10.2f}{F:9.0f}{sig:8.3f}{B.C_PERP/sig:7.0f}x")
print(f"\n  Ban truoc phai phay mat chan phang trong long mat mong, he so 10x.")
print(f"  Nay chan la ca mat canh nap ap vao ca mat vach than: he so hang tram lan.")

# ==========================================================================
hr("4. QUET 0-180 DO — KIEM VA CHAM")
def leaf_pts(th):
    o = []
    for X in [0.0, LW/4, LW/2, 3*LW/4, LW]:
        o += [rot((X, Z_RIM), th), rot((X, Z_LID), th)]
    return o
EPS = 0.05
def inside(x, z, x0, x1, z0, z1):
    return x0 + EPS < x < x1 - EPS and z0 + EPS < z < z1 - EPS
def hits_body(p):
    x, z = p
    if z < -EPS:                                                  return "MAT BAN"
    if inside(x, z, 0, S['WALL_HINGE'], Z_FLOOR, Z_RIM):          return "VACH THAN"
    if inside(x, z, 0, W, B.FOOT, Z_FLOOR):                       return "DAY HOP"
    if inside(x, z, S['WALL_HINGE'], S['WALL_HINGE']+S['BAY'], Z_FLOOR, Z_TRAY_TOP):
        return "KHAY"
    return None
bad = [(i, h, p) for i in range(181) for p in leaf_pts(math.radians(i))
       if (h := hits_body(p))]
print(f"  Quet 1 do mot buoc, {len(leaf_pts(0))} diem bien tren canh.")
if bad:
    print(f"  VA CHAM: {len(bad)} truong hop, vi du {bad[:3]}")
else:
    zmin = min(min(p[1] for p in leaf_pts(math.radians(i))) for i in range(181))
    print(f"  Khong va cham o bat ky goc nao. Diem thap nhat: Z = {zmin:.1f} mm")
    print(f"  (= vanh than tru be day nap — dung vi tri canh mo).")

# ==========================================================================
hr("5. PHAN CUNG BAN LE")
for a, b in [("Kieu", f"ban le la brass (butt hinge), khop nam DUNG tren arris"),
             ("So luong", f"{B.HG_N} chiec moi canh, tong {2*B.HG_N} chiec"),
             ("Kich thuoc", f"{B.HG_L:.0f} dai x {B.HG_W:.0f} rong moi canh x {B.HG_T} day,"
                            f" khop O{B.HG_KN}"),
             ("Vi tri theo Y", ", ".join(f"{y:.0f}" for y in S['HG_Y'])),
             ("Mortise", f"{B.HG_MORT} mm vao vanh than va {B.HG_MORT} mm vao mat duoi nap"
                         f" -> khep kin khong ho khe"),
             ("Bo luon arris", f"R{B.HG_R:.2f} tren canh ngoai TREN cua vach than va canh"
                               f" ngoai DUOI cua nap; dong lai thanh lo O{B.HG_KN:.1f} om khop"),
             ("Khop lo ra", f"khong lo ra ngoai mat vach — chim trong duong chi goc,"
                            f" nhin nghieng chi thay soi brass rong {B.HG_KN:.1f} mm"),
             ("Gia phai tra", f"mat chan 180 do con {S['STOP_H']:.2f} thay vi {B.T_LID:.0f} mm"
                              f" ({100*B.HG_R/B.T_LID:.0f} %), he so an toan van 55x"),
             ("Vit", "brass, 2 con moi canh moi chiec"),
             ("Vat lieu", B.HG_MAT)]:
    print(f"   {a:20s}: {b}")
m_hg = S['V']['ban le brass']/1e6*B.RHO['brass']
print(f"\n  Khoi luong ban le: {m_hg*1000:.0f} g ca bo.")
print(f"  Ban truoc dung mat mong go + chot: 0 g kim loai nhung ONG O18 tren hop cao 65.")

# ==========================================================================
hr("6. DO VONG DAU CANH KHI MO")
F = 5.0*9.81
bw = 100.0                       # be rong chiu tai gia dinh
I = bw*T**3/12
d = F*LW**3/(3*B.E_W*I)
sig = (F*LW)/(bw*T**2/6)
print(f"  Canh mo la dam console dai {LW:.0f} mm, ngam doc mat chan 180 do.")
print(f"  Nguoi choi ty {F/9.81:.0f} kg o mep ngoai, tai trai deu tren {bw:.0f} mm be rong:")
print(f"    vong dau canh {d:.2f} mm | uon {sig:.1f} MPa (MOR {B.MOR:.0f}) -> he so {B.MOR/sig:.0f}x")
print(f"  Cong them ro cua ban le (~0,05 mm huong kinh) -> tong ~{d+0.05:.2f} mm.")
print(f"  DAC TINH KIEM: vong dau canh mo <= 1,5 mm duoi tai 5 kg tai mep ngoai.")

# ==========================================================================
hr("7. CHOT LAI CAC TRI SO CHO HD-01")
go, t_, tot = B.mass_of(S, 'loi on dinh')
for a, b in [("Truc xoay", f"X = {PX:.0f} (mat ngoai vach), Z = {PZ:.0f} (= vanh than)"),
             ("Suy ra tu", "truc phai o GOC CHUNG cua hai chi tiet -> ban kinh quet = 0"),
             ("Ban le", f"{2*B.HG_N} ban le brass {B.HG_L:.0f} x {B.HG_W:.0f} x {B.HG_T},"
                        f" khop O{B.HG_KN}"),
             ("Ong go / mat mong", "KHONG CON"),
             ("Bo luon arris", f"R{B.HG_R:.2f} hai canh — khep thanh lo O{B.HG_KN:.1f} om khop"),
             ("Chan 180 do", "mat canh nap ap vao mat ngoai vach than — tu nhien"),
             ("Goc mo", "180 do +0/-1 do"),
             ("Vi tri canh khi mo", f"nam ngang, mat tren Z{Z_RIM:.0f} (= vanh than),"
                                    f" vuon ra {LW:.0f}"),
             ("Day nap", f"{T:.0f} deu, khong vat"),
             ("Phu bi", f"{W:.0f} x {S['Y_OA']:.0f} x {S['Z_OA']:.0f}"),
             ("Khoi luong", f"{tot:.2f} kg (khay loi on dinh) / "
                            f"{B.mass_of(S,'cocobolo')[2]:.2f} kg (khay cocobolo)")]:
    print(f"   {a:20s}: {b}")
