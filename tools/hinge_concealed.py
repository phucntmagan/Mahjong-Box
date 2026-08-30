#!/usr/bin/env python3
"""
BAN LE CHIM HAN — nhin tu ngoai khong thay gi. CO LAM DUOC KHONG?
Chay: python3 tools/hinge_concealed.py

Y tuong duoc de xuat: day truc SAU vao trong vach, de lai mot lop DA GO phu
ngoai, thi nhin tu ngoai se khong thay ban le.

Ket qua: KHONG. Va ly do khong phai tay nghe ma la hinh hoc — muc 2 quet so,
muc 3 rut ra dinh luat. Muc 5 chi ra don bay THAT SU con lai.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B
def hr(t): print("\n"+"="*78+"\n"+t+"\n"+"="*78)

S = B.derive()
Z_RIM, Z_LID, T = S['Z_RIM'], S['Z_LID'], B.T_LID
W, WALL = S['W'], S['WALL_HINGE']
R = S['R_KN']
X1 = S['LEAF_X0'] + S['LW']
EPS = 0.02

def rot(p, px, pz, th):
    x, z = p[0]-px, p[1]-pz
    c, s = math.cos(th), math.sin(th)
    return (px + x*c - z*s, pz + x*s + z*c)

# ==========================================================================
hr("1. MO HINH")
print(f"  Truc dat o (a , {Z_RIM:.0f} - b): LUI VAO a tu mat ngoai vach, va SAU b duoi")
print(f"  vanh. Ong go O{2*R:.1f} quanh truc. De ong khong lo ra mat ngoai thi phai con")
print(f"      DA GO ngoai  s = a - {R:.1f}")
print(f"  'Chim han' nghia la s > 0: con mot lop go lien lac phu kin ban le.\n")
print(f"  Vach ban le {WALL:.0f} mm, nap day {T:.0f} mm, vanh o Z{Z_RIM:.0f}.")
print(f"  Canh nap khi dong: la nap x tu 0 den {X1:.0f}, z tu {Z_RIM:.0f} den {Z_LID:.0f};")
print(f"  cong mot luoi go thoc tu nap xuong toi truc.")

# ==========================================================================
hr("2. QUET SO — truc chim quay duoc bao nhieu do")

def first_collision(a, b, s, dth=0.25, nx=120, nz=20):
    """Goc dau tien canh nap an vao DA GO ngoai (x < s, z < Z_RIM). Tra ve
    (goc, diem ban dau, vi tri luc cham)."""
    px, pz = a, Z_RIM - b
    pts = [(X1*i/nx, Z_RIM + T*j/nz) for i in range(nx+1) for j in range(nz+1)]
    th = dth
    while th <= 180.0:
        for p in pts:
            q = rot(p, px, pz, math.radians(th))
            if EPS < q[0] < s - EPS and EPS < q[1] < Z_RIM - EPS:
                return th, p, q
        th += dth
    return None, None, None

S_SKIN = 2.0
print(f"  Lay da go s = {S_SKIN:.1f} mm (mong hon thi khong con la go, la vo).")
print(f"  Quet {0.25}° mot buoc.\n")
print(f"  {'a':>6s}{'b':>6s}{'da go s':>9s}{'cham o goc':>12s}   diem tren nap -> cho cham")
for a, b in [(8.1, 6.1), (9.0, 7.0), (11.0, 9.0), (13.0, 11.0), (8.1, 0.0)]:
    if a - R < S_SKIN - 1e-9: continue
    th, p, q = first_collision(a, b, S_SKIN)
    if th is None:
        print(f"  {a:6.1f}{b:6.1f}{a-R:9.1f}{'khong cham':>12s}")
    else:
        print(f"  {a:6.1f}{b:6.1f}{a-R:9.1f}{th:11.2f}°   "
              f"({p[0]:.1f},{p[1]:.0f}) -> ({q[0]:.2f},{q[1]:.2f})")
print()
print(f"  Moi cau hinh chim deu chet o duoi 1 do. Va diem pham loi LUON LA MOT:")
print(f"  mot diem tren MAT DUOI cua nap, nam PHIA NGOAI truc.")

# ==========================================================================
hr("3. VI SAO — dinh luat")
a, b = 11.0, 9.0
px, pz = a, Z_RIM - b
print(f"  Lay truc ({a:.0f} , {pz:.0f}). Quay canh nap thi diem nao cua nap di xuong?")
print(f"  Van toc mot diem cach truc (dx,dz) la (-dz, dx). Diem NGOAI truc (dx < 0)")
print(f"  co van toc z am -> DI XUONG. Ca dai mat duoi nap tu x = 0 den x = {a:.0f} deu")
print(f"  nam ngoai truc, nen ca dai do CAY XUONG duoi vanh ngay tu do dau tien.\n")
print(f"  {'diem mat duoi':>15s}{'thut sau nhat toi':>20s}{'o goc':>9s}")
for x0 in (0.0, 2.0, 5.0, 8.0, a-0.1):
    lo = None
    for deg in range(0, 181):
        q = rot((x0, Z_RIM), px, pz, math.radians(deg))
        if EPS < q[0] < WALL and q[1] < Z_RIM - EPS:
            if lo is None or q[1] < lo[0]: lo = (q[1], deg)
    print(f"  {x0:15.1f}{'Z'+format(lo[0],'.1f'):>20s}{lo[1]:8d}°")
print()
print(f"  Vach phai duoc khoet rong TOAN BO dai do. Ma dai do bat dau tu x = 0,")
print(f"  tuc no MO THANG RA MAT NGOAI. Da go bi cay thung ngay lap tuc.\n")
print(f"  ==> DINH LUAT: be rong khe ho BAT BUOC tren mat ngoai = DO LUI VAO cua truc.")
print(f"      Va phan ong nho ra ngoai = max(0 , R - do lui vao).")
print(f"      Day khong phai hai bai toan, no la MOT: day truc vao trong bao nhieu thi")
print(f"      ong bot nho ra bay nhieu VA khe ho rong ra dung bay nhieu.")

# ==========================================================================
hr("4. BANG DANH DOI — day truc vao sau bao nhieu thi duoc gi")
print(f"  {'truc lui vao':>14s}{'ong nho ra':>13s}{'khe ho mat ngoai':>19s}"
      f"{'tong nhin thay':>16s}   ghi chu")
for aa in (0.0, 2.0, 4.0, R, 8.0, 11.0):
    proud = max(0.0, R - aa)
    gap = aa
    note = ("ho B — vach & nap phang liet" if aa == 0 else
            "HO C — dang dung, khe nho nhat ma khong nho ra" if abs(aa-R) < 1e-9 else
            "ong khong con lap day khe — khe rong hon ong" if aa > R else
            "vua nho ra vua co khe")
    print(f"  {aa:14.1f}{proud:13.1f}{gap:19.1f}{proud+gap:16.1f}   {note}")
print()
print(f"  Doc bang: cot 'tong nhin thay' KHONG BAO GIO nho hon {R:.1f} — bang dung ban")
print(f"  kinh ong. Day truc vao chi DOI CHO cai nhin thay tu 'nho ra' sang 'khe ho'.")
print(f"  Va day qua {R:.1f} thi khe con rong hon ca ong: te hon han.\n")
print(f"  ==> Cau hinh dang dung (truc lui vao dung R = {R:.1f}) DA LA toi uu cua")
print(f"      'khong nho ra ti nao'. Khong co cau hinh nao vua khong nho ra vua khong khe.")

# ==========================================================================
hr("5. DON BAY THAT SU CON LAI — lam ONG NHO DI")
print(f"  Vi 'tong nhin thay' = R, muon nhin thay it hon thi chi con mot cach:")
print(f"  lam ban kinh ong nho lai. R = (chot + khe)/2 + thanh go quanh lo.\n")
print(f"  {'chot':>7s}{'thanh go':>10s}{'ong go':>9s}{'khe ho':>9s}{'cat chot':>11s}"
      f"{'xe doc':>10s}   rui ro khoan lo sau {B.KN_PIN_L:.0f}")
m_leaf = (S['V']['khung nap']/2/1e6*B.RHO['cocobolo']
          + S['V']['tam Nu']/2/1e6*B.RHO['Nu go do'])
V_kn = m_leaf*9.81/S['N_KN_LID']
for pin, wl in ((6.0, 3.0), (5.0, 3.0), (5.0, 2.5), (4.0, 2.5), (4.0, 2.0), (3.0, 2.0)):
    r = (pin + B.KN_FIT)/2 + wl
    tau = V_kn/(2*math.pi*(pin/2)**2)
    sig_s = V_kn/(2*wl*B.KN_LEN)
    risk = ("an toan" if wl >= 3.0 else
            "chap nhan duoc" if wl >= 2.5 else
            "NGUY — mui khoan troi 0,1-0,2 se nut ra ngoai")
    print(f"  O{pin:<6.0f}{wl:10.1f}{'O'+format(2*r,'.1f'):>9s}{2*r:8.1f}"
          f"{B.SHEAR/tau:10.0f}x{B.T_PERP/sig_s:9.0f}x   {risk}")
print()
print(f"  Do ben khong phai rang buoc o bat ky dong nao — he so hang tram lan.")
print(f"  Rang buoc la KHOAN: lo O(chot+{B.KN_FIT:.1f}) sau {B.KN_PIN_L:.0f} mm xuyen "
      f"{B.N_KN} mat mong")
print(f"  xen ke tren cocobolo nhieu dau. Mui khoan troi 0,1-0,2 mm tren {B.KN_PIN_L:.0f} la")
print(f"  binh thuong; thanh go phai nuot duoc do troi do.")
print(f"\n  === DON BAY NAY DA DUOC LAY (Rev C3) ===")
print(f"  Ban truoc dung chot O6 + thanh 3,0 -> ong O{2*((6.0+B.KN_FIT)/2+3.0):.1f}.")
print(f"  Nay ha xuong chot O{B.KN_PIN:.0f} + thanh {B.KN_WALL:.1f} -> ong O{2*R:.1f}:")
print(f"  duong kinh bot {2*((6.0+B.KN_FIT)/2+3.0) - 2*R:.1f} mm, dai nhin thay bot"
      f" {((6.0+B.KN_FIT)/2+3.0) - R:.1f} mm.")
print(f"  Doi lai: thanh go quanh lo chot chi con {B.KN_WALL:.1f} mm. DAC TINH KIEM bat buoc")
print(f"  TRUOC khi chot — do do troi mui khoan tren 160 mm phai <= 0,10 mm. Neu do")
print(f"  duoc lon hon thi phai tra thanh go ve 3,0 va ong ve O{2*((B.KN_PIN+B.KN_FIT)/2+3.0):.1f}.")

# ==========================================================================
hr("6. KET LUAN")
print(f"  Cai hinh ve — ong go nam gon trong long vach, co da go phu ngoai — KHONG")
print(f"  QUAY DUOC. Khong phai 'kho lam', ma la ngay do dau tien mat duoi cua nap da")
print(f"  cay thung lop da go do (muc 2: cham o duoi 1 do).")
print(f"\n  Ly do goc: canh nap la vat ran quay quanh MOT truc. Moi diem cua nap nam")
print(f"  PHIA NGOAI truc deu di xuong khi mo. Truc cang lui vao trong thi dai 'di")
print(f"  xuong' cang rong, va dai do luon bat dau tu mat ngoai vach.")
print(f"\n  Vay nen:")
print(f"   - Muon KHONG NHO RA  -> phai chap nhan khe ho rong bang ban kinh ong.")
print(f"   - Muon KHONG KHE HO  -> phai chap nhan ong nho ra bang ban kinh ong.")
print(f"   - Muon CA HAI        -> phai bo mo phang 180 do (xem docs/DONG-HOC-BAN-LE.md);")
print(f"     va bo 180 do la bo luon khay bo bai tren mat duoi nap.")
print(f"\n  Rev C3 da CHON dau kia cua dinh luat: ho B — chap nhan ong nho ra {R:.1f} mm")
print(f"  moi ben de KHONG phai ha bac. Ly do khong nam o ban le ma nam o HOC AM:")
print(f"  ha bac {R:.1f} x {B.T_LID:.0f} chay suot vach ban le, ma hoc am hai tay nam dung")
print(f"  tren vach do — ha bac khoa tran hoc xuong va lam dai go tren hoc mong di")
print(f"  {R:.1f} mm. Bo ha bac thi khe ho vao tay va ban kinh bo mep deu rong ra")
print(f"  (xem tools/grip_hook.py). Gia phai tra la {2*R:.1f} mm phu bi X.")
print(f"  Don bay con lai van la ha duong kinh ong — muc 5 da lay mot phan.")
