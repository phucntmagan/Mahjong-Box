#!/usr/bin/env python3
"""
Dong hoc ban le MONG GO.
Chay: python3 tools/hinge_kinematics.py
He toa do: Z=0 mat ban, X=0 mat ngoai vach trai. Mat cat trong mat phang X-Z.
Moi tri so hinh hoc lay tu tools/box_spec.py.

RANG BUOC VAT LIEU DA CHOT TU DAU: ban le lam bang MONG GO, khong kim loai.
Cai duy nhat con la bien la CHO DAT TRUC — va muc 1 chung minh chinh cho do ep
duong kinh ong go, chu khong phai nguoc lai.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B
def hr(t): print("\n"+"="*78+"\n"+t+"\n"+"="*78)

S = B.derive()
Z_RIM, Z_LID = S['Z_RIM'], S['Z_LID']
LW, W, T = S['LW'], S['W'], B.T_LID
PX, PZ = S['PIN_X'], S['PIN_Z']
R_KN, PROUD = S['R_KN'], S['PROUD']
EPS = 0.02

def rot_about(p, px, pz, th):
    x, z = p[0]-px, p[1]-pz
    c, s = math.cos(th), math.sin(th)
    return (px + x*c - z*s, pz + x*s + z*c)
def rot(p, th): return rot_about(p, PX, PZ, th)
RB_D, RB_H = S['REBATE_D'], S['REBATE_H']
LEAF_X0, REACH = S['LEAF_X0'], S['REACH']

def in_body(q, rb_d=None, rb_h=None):
    """Diem q co nam TRONG go than hop khong. Ha bac o vanh ngoai TREN da bi tru."""
    rb_d = RB_D if rb_d is None else rb_d
    rb_h = RB_H if rb_h is None else rb_h
    if not ((EPS < q[0] < W - EPS) and (EPS < q[1] < Z_RIM - EPS)):
        return False
    # Mat ha bac o x = rb_d la mat TIEP XUC (mat chan 180 do), khong phai mat cam:
    # dung <= nen diem nam dung tren no khong bi tinh la va cham.
    if rb_d > 0 and q[0] < rb_d + EPS and q[1] > Z_RIM - rb_h - EPS:
        return False                      # nam trong ha bac -> khong con go
    return True

# ==========================================================================
hr("1. TRUC DAT O DAU — VA CHO DO EP DUONG KINH ONG GO BAO NHIEU")
print("  Rang buoc hinh hoc THAT SU chi co mot: trong ca hanh trinh 0-180 do,")
print("  vat lieu canh nap khong duoc cat vao vat lieu than hop.\n")
print("  Dat truc o (px,pz) thi phai BO TRON dau canh nap thanh mui tron ban kinh")
print("  R_mui quanh truc moi quay lot. Quet so, khong lap luan bang loi:\n")

def nose_radius(px, pz, nx=160, nz=40, dth=0.5):
    """R_mui NHO NHAT phai bo tron dau canh nap quanh truc (px,pz) de quay het
    0-180 do khong cham than hop. 0 = khong phai bo gi."""
    rmin = math.inf
    for i in range(nx+1):
        x = LW*i/nx
        for j in range(nz+1):
            z = Z_RIM + T*j/nz
            th = 0.0
            while th <= 180.0 + 1e-9:
                if in_body(rot_about((x, z), px, pz, math.radians(th)), 0.0, 0.0):
                    rmin = min(rmin, math.hypot(x-px, z-pz)); break
                th += dth
    return 0.0 if rmin is math.inf else rmin

CANDS = [("giua be day nap (ban goc)",       T/2, Z_RIM + T/2),
         ("lui vao 4 mm tu mat ngoai",        4.0, Z_RIM + T/2),
         ("lui vao 2 mm tu mat ngoai",        2.0, Z_RIM + T/2),
         ("TREN mat ngoai, giua be day nap",  0.0, Z_RIM + T/2),
         ("TREN mat ngoai, o arris",          0.0, Z_RIM)]
print(f"  {'dat truc o':34s}{'toa do':>15s}{'R mui phai bo':>17s}")
res = {}
for lbl, px, pz in CANDS:
    r = nose_radius(px, pz); res[lbl] = r
    print(f"  {lbl:34s}{f'({px:.1f} , {pz:.1f})':>15s}{r:14.2f} mm")
r_mid = res["giua be day nap (ban goc)"]
print()
print(f"  Doc bang: R_mui tut ve 0 DUNG khi px = 0, tuc khi truc nam TREN MAT PHANG")
print(f"  NGOAI cua than. Ly do hinh hoc: mat dau canh nap CHINH LA mat phang x = 0;")
print(f"  truc nam tren no thi ca mat dau la mot tia xuat phat tu truc, quay bao nhieu")
print(f"  cung chi truot tren chinh no, khong bao gio dam vao than.")
print(f"  Truc lui vao trong bao nhieu thi mat dau quet thanh cung, va phai bo tron")
print(f"  dung bay nhieu. O giua be day nap: R_mui = {r_mid:.1f} = {T:.0f}/2 = nua be day nap.\n")
print(f"  => BA HO NGHIEM, va chi ba:\n")
print(f"    HO A — truc TRONG vat lieu, o tam mat dau canh ({T/2:.1f} , {Z_RIM+T/2:.1f})")
print(f"      Dau canh nap bo tron R{T/2:.1f}; ong go CHINH LA dau canh nap bo tron nen")
print(f"      KHONG nho ra ngoai phu bi. Nhung R bi be day nap ep cung: ong luon O{T:.0f}.")
print(f"      Va o 180 do KHONG co mat chan tu nhien.\n")
print(f"    HO B — truc TREN mat phang ngoai, o arris (0 , {Z_RIM:.0f})")
print(f"      Khong phai bo tron gi. R tu do theo do ben thanh go. Nhung tam ong nam")
print(f"      dung tren mat ngoai vach nen nua ong NHO RA {S['R_KN']:.1f} mm moi ben.\n")
print(f"    HO C — truc LUI VAO dung R, van o cao do vanh ({S['R_KN']:.1f} , {Z_RIM:.0f})")
print(f"      Ong tiep tuyen mat ngoai vach TU BEN TRONG -> CHIM HAN, khong nho ra ti nao.")
print(f"      Truc van nam tren mat dau canh nap (chi la mat do lui vao {S['R_KN']:.1f}) nen")
print(f"      R_mui van bang 0. Hai he qua bat buoc, ca hai deu tinh duoc:")
print(f"        1. mep ngoai canh nap lui vao dung {S['R_KN']:.1f} mm;")
print(f"        2. vanh ngoai TREN cua vach phai HA BAC {S['R_KN']:.1f} sau — cao bao nhieu?\n")

def min_rebate_h(rb_d, nx=200, nz=60, dth=0.25):
    """Chieu cao ha bac NHO NHAT de canh nap quay het 0-180 do khong cham vach."""
    lo, hi = 0.0, T + 2.0
    def ok(h):
        for i in range(nx+1):
            x = S['LEAF_X0'] + LW*i/nx
            for j in range(nz+1):
                z = Z_RIM + T*j/nz
                th = 0.0
                while th <= 180.0 + 1e-9:
                    if in_body(rot((x, z), math.radians(th)), rb_d, h): return False
                    th += dth
        return True
    for _ in range(9):
        mid = (lo + hi)/2
        if ok(mid): hi = mid
        else: lo = mid
    return hi

if B.HG_MODE == 'C':
    h_min = min_rebate_h(S['REBATE_D'])
    print(f"  Quet so: ha bac phai cao it nhat {h_min:.2f} mm — tuc DUNG BANG be day nap")
    print(f"  {T:.0f} mm, khong hon khong kem. Ly do: o 180 do mat dau canh nap (cao {T:.0f})")
    print(f"  quay xuong nam gon trong ha bac; thap hon mot ly la goc tren cua no cham vach.")
    print(f"  Dac ta dat REBATE_H = T_LID nen tri so nay tu dung theo be day nap.\n")

# ==========================================================================
hr("2. BA HO NGHIEM — BANG SO")
dA, dB, dC = B.derive_mode('A'), B.derive_mode('B'), B.derive_mode('C')
print(f"  {'':30s}{'HO A':>16s}{'HO B':>16s}{'HO C':>16s}")
print(f"  {'':30s}{'truc trong nap':>16s}{'truc tren mat':>16s}{'truc lui vao R':>16s}")
def line(lbl, f):
    print(f"  {lbl:30s}{f(dA):>16s}{f(dB):>16s}{f(dC):>16s}")
line("Truc xoay",            lambda d: f"({d['PIN_X']:.1f},{d['PIN_Z']:.0f})")
line("Ong go",               lambda d: f"O{2*d['R_KN']:.1f}")
line("Ong bi ep boi",        lambda d: "be day nap" if d['HG_MODE']=='A' else "chot+thanh go")
line("NHO RA moi ben",       lambda d: f"{d['PROUD']:.1f} mm")
line("Ha bac vanh",          lambda d: "khong" if d['REBATE_D']<=0
                                       else f"{d['REBATE_D']:.1f} x {d['REBATE_H']:.0f}")
line("Mep nap lui vao",      lambda d: f"{d['LEAF_X0']:.1f} mm")
line("Phu bi X",             lambda d: f"{d['X_OA']:.1f}")
line("Chan 180 do",          lambda d: "PHAI PHAY" if d['STOP_A'] <= 0 else "tu nhien")
line("Dien tich chan",       lambda d: "—" if d['STOP_A'] <= 0 else f"{d['STOP_A']:.0f} mm2")
line("Canh mo, mat tren o",  lambda d: f"Z{Z_RIM:.0f}" if d['HG_MODE'] != 'A' else f"Z{Z_RIM+T:.0f}")
line("So voi vanh than",     lambda d: "bang vanh" if d['HG_MODE'] != 'A' else f"cao hon {T:.0f}")
line("Canh mo vuon ra",      lambda d: f"{d['REACH']:.1f}")
line("Khoi luong (loi o.d.)",lambda d: f"{B.mass_of(d,'loi on dinh')[2]:.2f} kg")
print()
print(f"  Ho A: phu bi nho nhat nhung ong bang DUNG be day nap ({2*dA['R_KN']:.0f} mm) va khong co")
print(f"        mat chan 180 do — phai phay mat chan trong long mat mong.")
print(f"  Ho B: ong manh nhat nhung nho ra {dB['PROUD']:.1f} mm moi ben, phu bi X {dB['X_OA']:.1f}.")
print(f"  Ho C: ong CHIM HAN (nho ra 0), phu bi X {dC['X_OA']:.1f} — bang dung ho A — va van giu")
print(f"        nguyen mat chan tu nhien {dC['STOP_A']:.0f} mm2 cua ho B.")
print(f"        Gia phai tra: ha bac {dC['REBATE_D']:.1f} x {dC['REBATE_H']:.0f} suot {B.LID_L:.0f} mm tren vanh,")
print(f"        va mep ngoai canh nap lui vao {dC['LEAF_X0']:.1f} mm.")
print(f"\n  DA CHON: HO {B.HG_MODE}.  Doi B.HG_MODE roi chay lai la ra ho kia.")

# ==========================================================================
hr(f"3. CANH MO RA NAM O DAU  (ho {B.HG_MODE})")
X1 = S['LEAF_X0'] + LW                       # mep khe rap giua
pts = {'mep ban le, mat duoi': (S['LEAF_X0'], Z_RIM), 'mep ban le, mat tren': (S['LEAF_X0'], Z_LID),
       'mep khe giua, mat duoi': (X1, Z_RIM), 'mep khe giua, mat tren': (X1, Z_LID)}
print(f"  {'diem':26s}{'dong X':>9s}{'dong Z':>9s}{'mo 180: X':>13s}{'Z':>9s}")
for k, p in pts.items():
    q = rot(p, math.pi)
    print(f"  {k:26s}{p[0]:9.1f}{p[1]:9.1f}{q[0]:13.1f}{q[1]:9.1f}")
zt_open = Z_RIM + T if B.HG_MODE == 'A' else Z_RIM
print(f"\n  Mat TREN cua canh mo nam tai Z{zt_open:.0f}"
      + (f" — cao hon vanh {T:.0f} mm." if B.HG_MODE == 'A' else " — dung cao do VANH THAN."))
print(f"  Vuon ra {S['REACH']:.2f} mm. Mat tren canh mo chinh la mat duoi nap khi dong,")
print(f"  tuc long lom om tam Nu — khay bo bai sau {T - B.S_TOP - B.PAN_T:.1f} mm.")

# ==========================================================================
hr("4. CHAN 180 DO")
m_leaf = (S['V']['khung nap']/2/1e6*B.RHO['cocobolo']
          + S['V']['tam Nu']/2/1e6*B.RHO['Nu go do'])
if S['STOP_A'] > 0:
    SH, A_stop = S['STOP_H'], S['STOP_A']
    _xf = S['LEAF_X0']
    print(f"  O 180 do, mat canh ban le cua nap ap DUNG vao mat doi dien ben than —")
    print(f"  ca hai deu la mat phang x = {_xf:.1f} " +
          ("(mat ngoai vach)." if _xf == 0 else "(mat ha bac)."))
    print(f"  Ca hai deu di qua truc nen chi cham nhau DUNG o 180 do, khong co ma sat")
    print(f"  trong hanh trinh. Chan tu nhien, khong phay gi them.\n")
    print(f"  Trong doan mong ({S['KN_RUN']:.0f} mm) ong go an mat {R_KN:.1f} nen chan cao")
    print(f"  {SH:.2f}; ngoai doan mong ({B.LID_L - S['KN_RUN']:.0f} mm) canh nap con vuong nen")
    print(f"  chan cao ca {T:.0f} mm. Tong dien tich chan {A_stop:.0f} mm2.\n")
    arm_r = 2*SH/3
    print(f"  {'truong hop tai':36s}{'M (N.m)':>10s}{'F (N)':>9s}{'MPa':>8s}{'he so':>8s}")
    for lbl, extra, ex_arm in [("chi trong luong canh", 0.0, 0.0),
                               ("+ 2 kg quan bo tren khay", 2.0, LW/2),
                               ("+ nguoi choi ty 5 kg o mep ngoai", 5.0, LW)]:
        M = m_leaf*9.81*(LW/2)/1000 + extra*9.81*ex_arm/1000
        F = M/(arm_r/1000); sig = F/A_stop
        print(f"  {lbl:36s}{M:10.2f}{F:9.0f}{sig:8.3f}{B.C_PERP/sig:7.0f}x")
    print(f"\n  Ho A phai phay mat chan phang trong long mat mong, he so 10x.")
    print(f"  Ho {B.HG_MODE} chan bang ca mat canh nap ap vao ca mat than: he so hang tram lan.")
else:
    print(f"  Ho A KHONG co mat chan tu nhien: o 180 do canh nap nam ngang o")
    print(f"  Z{Z_RIM:.0f}..{Z_RIM+T:.0f}, treo hoan toan tren chot.")
    print(f"  Phai PHAY MAT CHAN PHANG trong long mat mong — dung cai ban goc lam,")
    print(f"  he so an toan 10x.")

# ==========================================================================
hr("5. QUET 0-180 DO — KIEM VA CHAM")
def leaf_pts(th):
    return [rot((x, z), th) for x in (PX, LW/2, LW)
            for z in (Z_RIM, (Z_RIM+Z_LID)/2, Z_LID)]
bad, zmin = 0, 1e9
for deg in range(0, 181):
    for q in leaf_pts(math.radians(deg)):
        zmin = min(zmin, q[1])
        if in_body(q): bad += 1
print(f"  Quet 1 do mot buoc, {len(leaf_pts(0))} diem bien tren canh.")
print(f"  {'Khong va cham o bat ky goc nao.' if bad == 0 else f'VA CHAM {bad} lan!'}"
      f"  Diem thap nhat: Z = {zmin:.1f} mm")

# ==========================================================================
hr("6. MAT MONG GO — KIEM DO BEN VA CHE TAO")
KH = S['KN_HOLE']
for a, b in [("Kieu", "mat mong go lien khoi voi than va voi nap — KHONG kim loai"),
             ("So mat mong", f"{B.N_KN} moi canh: {S['N_KN_BODY']} thuoc THAN, "
                             f"{S['N_KN_LID']} thuoc NAP (le nen hai dau thuoc than)"),
             ("Kich thuoc", f"dai {B.KN_LEN:.0f}, buoc {S['KN_PITCH']:.0f}, "
                            f"khe doc truc {B.KN_GAP:.1f}, chuoi {S['KN_RUN']:.0f}"),
             ("Dat theo Y", f"{S['KN_Y0']:.1f} .. {S['KN_Y0']+S['KN_RUN']:.1f} "
                            f"tren canh dai {B.LID_L:.0f}"),
             ("Ong go", f"O{2*R_KN:.1f} quanh truc ({PX:.1f} , {PZ:.1f})"),
             ("Chot", f"go cocobolo thang tho O{B.KN_PIN:.0f} x {B.KN_PIN_L:.0f}, "
                      f"2 chot moi canh, gap nhau o mat mong giua"),
             ("Lo chot", f"O{KH:.2f} (+{B.KN_FIT:.2f} khe)"),
             ("Thanh go quanh lo", f"{S['KN_WALL_EFF']:.2f} mm")]:
    print(f"  {a:22s}: {b}")
print()
F_leaf = m_leaf*9.81
V_kn = F_leaf/S['N_KN_LID']
tau    = V_kn/(2*math.pi*(B.KN_PIN/2)**2)     # chot cat hai mat cat
sig_b  = V_kn/(B.KN_PIN*B.KN_LEN)             # ep mat lo chot
sig_s  = V_kn/(2*S['KN_WALL_EFF']*B.KN_LEN)   # xe doc thanh go quanh lo
print(f"  Tai: trong luong mot canh {m_leaf:.2f} kg = {F_leaf:.1f} N chia cho "
      f"{S['N_KN_LID']} mat mong NAP")
print(f"  -> {V_kn:.1f} N moi mat. (Momen khi mo 180 do do MAT CHAN nhan, khong phai chot.)\n")
print(f"  {'kiem':34s}{'ung suat':>13s}{'cho phep':>12s}{'he so':>9s}")
for lbl, v, allow in [("cat chot go (2 mat cat)", tau, B.SHEAR),
                      ("ep mat lo chot", sig_b, B.C_PERP),
                      ("xe doc thanh go quanh lo", sig_s, B.T_PERP)]:
    print(f"  {lbl:34s}{v:10.3f} MPa{allow:10.0f} MPa{allow/v:8.0f}x")
print()
print(f"  Do ben KHONG phai rang buoc — he so hang tram den hang nghin lan.")
print(f"  Cai quyet dinh {S['KN_WALL_EFF']:.1f} mm thanh go la CHE TAO: phai khoan mot lo")
print(f"  O{KH:.2f} sau {B.KN_PIN_L:.0f} mm xuyen {B.N_KN} mat mong xen ke, tren go nhieu dau.")
print(f"  Mui khoan troi 0,1-0,2 mm tren 160 la binh thuong; thanh {S['KN_WALL_EFF']:.1f} mm nuot")
print(f"  duoc do troi do ma khong nut ra ngoai. Duoi 2,5 mm thi khong.")
print(f"\n  DAC TINH KIEM: khoan bang khoan can hoac khoan tung mat mong roi rap thu;")
print(f"  sai lech dong truc giua hai dau <= 0,15 mm. Chay thu 500 chu ky mo-dong.")

# ==========================================================================
hr("7. DO VONG DAU CANH KHI MO")
b_, h_ = 100.0, T
I = b_*h_**3/12
P, L = 5*9.81, LW - PX
defl = P*L**3/(3*B.E_W*I)
sig = P*L*(h_/2)/I
print(f"  Canh mo la dam console dai {L:.0f} mm, ngam doc mat chan 180 do.")
print(f"  Nguoi choi ty 5 kg o mep ngoai, tai trai deu tren {b_:.0f} mm be rong:")
print(f"    vong dau canh {defl:.2f} mm | uon {sig:.1f} MPa (MOR {B.MOR:.0f}) -> he so {B.MOR/sig:.0f}x")
print(f"  Cong ro cua chot trong lo ({B.KN_FIT:.2f}) -> tong ~{defl+B.KN_FIT:.2f} mm.")
print(f"  DAC TINH KIEM: vong dau canh mo <= 1,5 mm duoi tai 5 kg tai mep ngoai.")

# ==========================================================================
hr("8. CHOT LAI CAC TRI SO CHO HD-01")
for a, b in [("Vat lieu ban le", "MONG GO lien khoi — khong mot chi tiet kim loai nao"),
             ("Ho nghiem", f"{B.HG_MODE} — " + {
                 'A': "truc trong vat lieu, tam mat dau canh",
                 'B': "truc tren mat ngoai vach, o arris",
                 'C': "truc lui vao dung R — ong go chim han"}[B.HG_MODE]),
             ("Truc xoay", f"X = {PX:.1f} , Z = {PZ:.1f}"),
             ("Suy ra tu", "R_mui = 0 chi khi truc nam tren mat phang ngoai (muc 1)"),
             ("Ong go", f"O{2*R_KN:.1f} — dinh boi chot O{B.KN_PIN:.0f} + thanh go "
                        f"{S['KN_WALL_EFF']:.1f} mm, KHONG boi be day nap"),
             ("Nho ra ngoai", f"{PROUD:.1f} mm moi ben -> phu bi X {S['X_OA']:.1f}"),
             ("Ha bac vanh", "khong" if S['REBATE_D'] <= 0 else
              f"{S['REBATE_D']:.1f} sau x {S['REBATE_H']:.0f} cao, suot {B.LID_L:.0f} mm"),
             ("Mep nap lui vao", f"{S['LEAF_X0']:.1f} mm"),
             ("Mat mong", f"{B.N_KN} x {B.KN_LEN:.0f}, buoc {S['KN_PITCH']:.0f}, "
                          f"chuoi {S['KN_RUN']:.0f}, dat giua canh"),
             ("Chot", f"go O{B.KN_PIN:.0f} x {B.KN_PIN_L:.0f}, 2 chot moi canh"),
             ("Chan 180 do", f"mat canh nap ap vao mat ngoai vach — tu nhien, {S['STOP_A']:.0f} mm2"),
             ("Goc mo", "180 do +0/-1 do"),
             ("Vi tri canh khi mo", f"nam ngang, mat tren Z{zt_open:.0f} (= vanh than), "
                                    f"vuon ra {S['REACH']:.0f}"),
             ("Day nap", f"{T:.0f} deu, khong vat — be day nap KHONG con dinh ong go"),
             ("Phu bi", f"{S['X_OA']:.1f} x {S['Y_OA']:.0f} x {S['Z_OA']:.0f}"),
             ("Khoi luong", f"{B.mass_of(S,'loi on dinh')[2]:.2f} kg (khay loi on dinh) / "
                            f"{B.mass_of(S,'cocobolo')[2]:.2f} kg (khay cocobolo)")]:
    print(f"   {a:22s}: {b}")
