#!/usr/bin/env python3
"""
Phuong an C — hoc am long ban tay, xach hai tay. Khong quai, khong co cau.
Chay: python3 tools/handle_option_c.py

Cau hoi phai tra loi:
  1. Hoc 120 x 30 sau 16 co nam duoc trong vach truoc/sau khong?
  2. Dai go con lai tren hoc co chiu duoc ca hop khong?
  3. 3,7 kg moi tay co that su de hon 7,4 kg mot tay khong - do bang gi?
  4. Bo cai gi khi bo quai, va cai gi phai them lai?
  5. Neu muc tieu la duoi 6 kg thi con duong nao?
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B

def hr(t): print("\n" + "="*78 + "\n" + t + "\n" + "="*78)

A = B.derive(handle='A')
C = B.derive(handle='C')

# ============================================================================
hr("1. HOC AM PHAI NAM O VACH NAO")
print(f"  Hoc am can be day vach = sau hoc {B.GRIP_D:.0f} + thanh sau {B.GRIP_BACK:.0f}"
      f" = {B.GRIP_D+B.GRIP_BACK:.0f} mm.\n")
print(f"  {'vach':22s}{'day':>6s}{'du/thieu':>10s}   ket qua")
for lbl, t in [("truoc/sau", B.WALL_FB), ("trai/phai (ban le)", C['WALL_HINGE'])]:
    d = t - (B.GRIP_D + B.GRIP_BACK)
    print(f"  {lbl:22s}{t:6.0f}{d:+10.0f}   "
          f"{'DU — khong phai noi go ra ngoai' if d >= 0 else 'THIEU — phai noi go ra ngoai'}")
print(f"\n  Vach truoc/sau chi {B.WALL_FB:.0f} mm. Dat hoc am o do thi phai noi go ra ngoai,")
print(f"  va con hai he qua nang hon:")
print(f"   - Vach truoc/sau la cho DUY NHAT nap va vanh than con chong len nhau")
print(f"     ({B.WALL_FB:.0f} mm), tuc la cho duy nhat dat duoc nam cham khoa nap.")
print(f"   - No cung la cho duy nhat khoet duoc khe luon ngon nhac khay. Hoc am sau")
print(f"     {B.GRIP_D:.0f} tu ngoai + khe luon ngon {B.WELL_D:.0f} tu trong = an het be day vach.")
print(f"  Ba chi tiet tranh nhau mot bo phan day {B.WALL_FB:.0f} mm.\n")
print(f"  Vach TRAI/PHAI day {C['WALL_HINGE']:.0f} mm, va tren no KHONG co gi khac tranh cho:")
print(f"  ong go ban le O{2*C['R_KN']:.1f} nam o ARRIS (0 , Z{C['Z_RIM']:.0f}), chiem {C['R_KN']:.1f} mm")
print(f"  be day vach tinh tu mat ngoai,")
print(f"  con hoc am o Z{C['GRIP_Z0']:.0f}..{C['GRIP_Z1']:.0f} — hai vung roi nhau hoan toan.")
print(f"  (Chinh hoc am dinh ra be day {C['WALL_HINGE']:.0f}: sau {B.GRIP_D:.0f} + thanh sau"
      f" {B.GRIP_BACK:.0f} = {C['WALL_HINGE']:.0f}.")
print(f"   Ong go chi an {C['R_KN']:.1f} mm vao vach {C['WALL_HINGE']:.0f}, con {C['WALL_HINGE']-C['R_KN']:.1f} mm;")
print(f"   hoc am moi la thu dinh ra be day vach.)")
print(f"\n  => Hoc am dat o VACH TRAI/PHAI. Phu bi KHONG doi: {C['W']:.0f} x {C['Y_OA']:.0f}"
      f" x {C['Z_OA']:.0f}.")
print(f"     (Ban truoc dat hoc am o vach truoc/sau va ket luan C phai noi phu bi Y")
print(f"      350 -> 374. Ket luan do SAI vi chon nham vach.)")

hr("2. HINH HOC HOC AM")
for a, bb in [("Kich thuoc", f"{B.GRIP_W:.0f} rong (theo Y) x {B.GRIP_H:.0f} cao x"
                             f" {B.GRIP_D:.0f} sau"),
              ("Bang Y", f"{C['GRIP_Y0']:.0f} .. {C['GRIP_Y1']:.0f}  (giua chieu sau hop,"
                         f" doi xung quanh Y={C['Y_BODY']/2:.0f})"),
              ("Bang Z", f"{C['GRIP_Z0']:.0f} .. {C['GRIP_Z1']:.0f} — day hoc ngang san trong"),
              ("Be day vach tai hoc", f"{C['WALL_GRIP']:.0f} mm, KHONG noi go ra ngoai"),
              ("Thanh sau hoc", f"{B.GRIP_BACK:.0f} mm"),
              ("Dai go TREN hoc", f"{C['GRIP_LEDGE']:.2f} mm (toi vanh than Z{C['Z_RIM']:.0f})"),
              ("Dai go DUOI hoc", f"{C['GRIP_SKIRT']:.0f} mm, lai duoc day hop {B.BOT:.0f} do lung"),
              ("Va cham", f"khong — ban le brass nam tren vanh Z{C['Z_RIM']:.0f},"
                          f" hoc am o Z{C['GRIP_Z1']:.0f} tro xuong")]:
    print(f"   {a:22s}: {bb}")
print(f"\n  Hai tay dat o hai vach trai/phai, cach nhau {C['W']:.0f} mm — hop gan vuong")
print(f"  ({C['W']:.0f} x {C['Y_OA']:.0f}) nen dat o vach nao cung cho khoang cach hai tay nhu nhau.")

hr("3. KIEM BEN — dai go tren hoc la duong truyen luc duy nhat")
m_C = B.mass_of(C, 'cocobolo')[2]
P_des = m_C*9.81*B.DYN
P_hand = P_des/2
L, h, b = B.GRIP_W, C['GRIP_LEDGE'], C['WALL_GRIP']
print(f"  Khoi luong {m_C:.2f} kg -> tai thiet ke {P_des:.0f} N (he so dong {B.DYN:.0f})"
      f" -> {P_hand:.0f} N moi tay\n")
print(f"  Dai go tren hoc = dam nhip {L:.0f}, tiet dien {h:.2f} (cao) x {b:.0f} (day),")
print(f"  ngam hai dau vao chinh vach hai ben hoc. Tho go chay DOC nhip. Tot.")
M = P_hand*L/8                      # ngam hai dau, tai phan bo giua nhip
Zs = b*h**2/6
I = b*h**3/12
sig = M/Zs
tau = 1.5*(P_hand/2)/(b*h)
dfl = P_hand*L**3/(192*B.E_W*I)
print(f"    Momen        M = P.L/8      = {M:7.0f} N.mm")
print(f"    Uon          sigma          = {sig:7.2f} MPa  / MOR {B.MOR:.0f}"
      f"   -> he so {B.MOR/sig:4.0f}x")
print(f"    Cat          tau            = {tau:7.2f} MPa  / {B.SHEAR:.0f}"
      f"      -> he so {B.SHEAR/tau:4.0f}x")
print(f"    Vong giua nhip              = {dfl:7.3f} mm   (khong cam thay duoc)")
A_back = B.GRIP_W*B.GRIP_H
print(f"\n  Thanh sau {B.GRIP_BACK:.0f} mm: khong nam tren duong truyen luc, chi chan ngon tay.")
print(f"    Tua vao ca bon canh; day duoi lai duoc day hop {B.BOT:.0f} mm do.")
print(f"    Neu an manh 200 N deu tren {A_back:.0f} mm2 -> {200/A_back*1000:.0f} kPa. Khong van de.")
print(f"\n  => Ket cau KHONG phai rang buoc cua C. He so an toan thap nhat "
      f"{min(B.MOR/sig, B.SHEAR/tau):.0f}x.")
print(f"     Rang buoc cua C nam o BAN TAY, khong o go.")

# ============================================================================
hr("4. EC-GO-NO-MI — chia doi tai, nhung tang ap luc cuc bo")
m_A = B.mass_of(A, 'cocobolo')[2]
N_FING, W_FING, L_DISTAL, EDGE_STRIP = 4, 16.0, 15.0, 5.0
A_flat = N_FING*W_FING*min(B.GRIP_D, L_DISTAL)     # ngon tay ap deu tran hoc
A_edge = N_FING*W_FING*EDGE_STRIP                  # truong hop xau: don ve mep truoc
strapA = 30.0*100.0                                # phan nam quai da phuong an A
print(f"  {'':30s}{'phuong an A':>20s}{'phuong an C':>20s}")
rows = [("So tay", "mot", "hai"),
        ("Khoi luong hop (kg)", f"{m_A:.2f}", f"{m_C:.2f}"),
        ("Tai tinh moi tay (N)", f"{m_A*9.81:.0f}", f"{m_C*9.81/2:.0f}"),
        ("Tai thiet ke moi tay (N)", f"{m_A*9.81*B.DYN:.0f}", f"{m_C*9.81*B.DYN/2:.0f}"),
        ("Dien tich tiep xuc (mm2)", f"{strapA:.0f}", f"{A_flat:.0f}"),
        ("Ap luc tinh (kPa)", f"{m_A*9.81/strapA*1000:.0f}",
                              f"{m_C*9.81/2/A_flat*1000:.0f}"),
        ("Ap luc tinh, don mep (kPa)", "—", f"{m_C*9.81/2/A_edge*1000:.0f}"),
        ("Khoang cach hai diem nam", "0 (mot diem)", f"{C['Y_OA']:.0f} mm"),
        ("Tu the", "tay buong doc than", "hai tay truoc bung"),
        ("Con tay ranh de mo cua", "co", "khong")]
for a, x, y in rows:
    print(f"  {a:30s}{x:>20s}{y:>20s}")
print(f"\n  Doc bang nay cho dung:")
print(f"   - C chia doi TAI (mot tay {m_A*9.81:.0f} N -> {m_C*9.81/2:.0f} N) — day la cai loi that.")
print(f"   - Nhung C lai TANG AP LUC cuc bo: quai da co {strapA:.0f} mm2 be mat nam,")
print(f"     hoc am chi co {A_flat:.0f} mm2 dau ngon tay: ap luc tinh "
      f"{m_C*9.81/2/A_flat*1000:.0f} kPa so voi {m_A*9.81/strapA*1000:.0f} kPa cua quai da.")
print(f"   - Neu tran hoc phang va mep sac, luc don het ve mep truoc: "
      f"{m_C*9.81/2/A_edge*1000:.0f} kPa. Do la luc hoc am tro thanh kho chiu.")
print(f"\n  => Hai yeu cau bat buoc cho tran hoc, neu khong C mat het cai loi cua no:")
print(f"     a) Tran hoc PHAI doc vao trong ~10 do de dau ngon tay ap deu ca "
      f"{min(B.GRIP_D,L_DISTAL):.0f} mm sau,")
print(f"        khong phai chi bam mep.")
print(f"     b) Mep ngoai tran hoc bo tron R >= 8 (cung tri so da chot cho quai da).")
print(f"        Canh vuong o {m_C*9.81/2:.0f} N moi tay se hang tay sau ~30 giay.")

# ============================================================================
hr("5. BO GI VA PHAI THEM LAI GI")
only_A = [k for k in A['V'] if k not in C['V']]
only_C = [k for k in C['V'] if k not in A['V']]
print("  Bo di:")
for k in only_A:
    print(f"   - {k:18s} {A['V'][k]/1000:7.0f} cm3  "
          f"{A['V'][k]/1e6*B.RHO['cocobolo']:5.2f} kg")
print("  Them vao:")
for k in only_C:
    print(f"   + {k:18s} {C['V'][k]/1000:7.0f} cm3  "
          f"{C['V'][k]/1e6*B.RHO['cocobolo']:5.2f} kg")
print(f"\n  Song khoa cua phuong an A lam BA viec: quai, khoa nap, va do mep tu do")
print(f"  cua nap. Bo no thi mat ca ba. Nhung viec thu ba hoa ra KHONG con la van de:")
print(f"  review Rev B §3.2 neu no khi mep nap day 8; vat nap da doi thanh 12, va")
print(f"  tools/detail_features.py muc 3 tinh lai cho vong 0,59 mm duoi 50 N, he so 21x.")
print(f"  => Khong can song noi tren AC-01. Chi can dem ni duoi nap de ep khay.")
print(f"     Bo song con giai luon xung dot 'song nam dung tren ranh Joker'.")
print(f"\n  CON TREO — C khong giai:")
# canh nap dong duoc giu bang chinh trong luong no de len vanh than.
# Momen giu = m.g.arm.cos(nghieng) quanh truc chot -> ve 0 khi hop nam nghieng 90 do.
m_leaf = (C['V']['khung nap']/2/1e6*B.RHO['cocobolo']
          + C['V']['tam Nu']/2/1e6*B.RHO['Nu go do'])
# truc xoay o canh ngoai tren cua than: canh nap roi tu x=PIN_X den x=LW
arm_leaf = (C['LW'] - C['PIN_X'])/2                 # tu truc chot toi trong tam canh
M_shut = m_leaf*9.81*arm_leaf/1000
F_lift = M_shut/((C['LW'] - C['PIN_X'])/1000)
print(f"   ! KHOA NAP. Canh nap chi duoc giu dong bang chinh trong luong no de len vanh:")
print(f"     canh {m_leaf:.2f} kg, canh tay don {arm_leaf:.0f} mm -> momen giu {M_shut:.2f} N.m.")
print(f"     Momen do bien thien theo cos(goc nghieng), ve 0 khi hop nam nghieng 90 do.")
print(f"     Nghia la: xach ngang thi KHONG bung — dung nhu may noi. Nhung")
print(f"       a) chi can {F_lift:.0f} N (~{F_lift/9.81*1000:.0f} g) day len o mep tu do la canh mo,")
print(f"       b) dat hop nam nghieng len canh la canh tren do xuong het hanh trinh.")
print(f"     Phuong an A giai ca hai bang chinh chi tiet quai.")
print(f"   ! Rang buoc 'khong kim loai' van con, va bo song khoa nghia la tren nap")
print(f"     KHONG con chi tiet nao de gan khoa vao. Khe rap giua {B.SEAM} mm lai nam")
print(f"     ngay tren khoang phu kien rong. Bai toan khoa nap phai giai rieng.")

# ============================================================================
hr("6. KHOI LUONG — DA QUA NGUONG 6 kg")
base_c = B.mass_of(C, 'cocobolo')[2]
base_s = B.mass_of(C, 'loi on dinh')[2]
print(f"  Muc tieu may dat ra tu dau: duoi 6 kg.\n")
print(f"  {'cau tao khay':22s}{'kg':>8s}{'tai TK':>10s}")
print(f"  {'cocobolo':22s}{base_c:8.2f}{base_c*9.81*B.DYN:9.0f} N")
print(f"  {'loi on dinh':22s}{base_s:8.2f}{base_s*9.81*B.DYN:9.0f} N"
      f"   <- DUOI 6 kg")
print(f"\n  Duong di tu 7,48 kg (ban dau) xuong {base_s:.2f} kg:")
for lbl, d in [("chot ty trong cocobolo 1,00", 0.44), ("bo song khoa + quai (phuong an C)", 0.31),
               ("day hop 8 -> 6", 0.26), ("tam Nu 10 -> 8", 0.14),
               ("khay loi on dinh thay cocobolo", 0.62),
               ("nap 18 -> 12 va tam Nu 8 -> 6 (ban le thanh hon)", 0.62)]:
    print(f"    - {lbl:48s} {d:5.2f} kg")
print(f"\n  Cai keo duoc xuong duoi 6 kg khong phai mot don bay giam can nao ca — ma la")
print(f"  viec lam ban le thanh hon. Nap tu 18 xuong 12 lay di 0,62 kg, va do la he")
print(f"  qua PHU cua mot thay doi tham my.")
print(f"\n  Con lai neu can:")
for lbl, dm, note in [("Khung nap sang go do dac", C['V']['khung nap']/1e6*(B.RHO['cocobolo']-B.RHO['go do dac']),
                       "MAT dong mau voi than"),
                      ("Than sang loi on dinh + veneer",
                       sum(C['V'][k] for k in ('day','vach truoc/sau','vach ngan'))/1e6
                       *(B.RHO['cocobolo']-B.RHO['loi on dinh']),
                       "vach trai/phai phai giu go dac (mang ban le va hoc am)")]:
    print(f"    - {lbl:34s}{dm:5.2f} kg   {note}")
print(f"\n  Quan co {B.N_TILES*B.M_TILE_G/1000:.2f} kg la san cung — chiem "
      f"{B.N_TILES*B.M_TILE_G/1000/base_s*100:.0f} % ca hop.")

hr("7. BANG CHOT A ↔ C")
volA = A['W']*A['Y_OA']*A['Z_OA']/1e6
volC = C['W']*C['Y_OA']*C['Z_OA']/1e6
print(f"  {'':32s}{'A · song khoa + quai da':>26s}{'C · hoc am hai tay':>28s}")
for a, x, y in [
    ("Phu bi", f"{A['W']:.0f} x {A['Y_OA']:.0f} x {A['Z_OA']:.0f}",
               f"{C['W']:.0f} x {C['Y_OA']:.0f} x {C['Z_OA']:.0f}"),
    ("The tich bao (L)", f"{volA:.2f}", f"{volC:.2f}"),
    ("Khoi luong khay cocobolo", f"{m_A:.2f} kg", f"{m_C:.2f} kg"),
    ("Khoi luong khay loi o.d.", f"{B.mass_of(A,'loi on dinh')[2]:.2f} kg",
                                 f"{B.mass_of(C,'loi on dinh')[2]:.2f} kg"),
    ("Tai thiet ke", f"{m_A*9.81*B.DYN:.0f} N", f"{m_C*9.81*B.DYN:.0f} N"),
    ("Dalbergia/hop (khay coco)", f"{B.dalbergia_of(A):.2f} kg", f"{B.dalbergia_of(C):.2f} kg"),
    ("Hop moi lo CITES", f"{int(B.CITES_LIMIT//B.dalbergia_of(A))}",
                         f"{int(B.CITES_LIMIT//B.dalbergia_of(C))}"),
    ("Chi tiet chuyen dong", "2 chot xoay", "0"),
    ("Chi tiet mon", "lo chot + da", "khong co"),
    ("Vat lieu ngoai go", "da bo bridle", "khong"),
    ("Khoa nap", "song khoa lam luon", "8 cap nam cham"),
    ("Do mep tu do cua nap", "co", "khong can — xem detail_features"),
    ("Rui ro che tao", "trung binh", "thap"),
]:
    print(f"  {a:32s}{x:>26s}{y:>28s}")
