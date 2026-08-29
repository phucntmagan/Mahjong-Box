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
hr("1. HOC SAU 16 KHONG NAM DUOC TRONG VACH DAY 10")
print(f"  Hoc am yeu cau  : rong {B.GRIP_W:.0f} x cao {B.GRIP_H:.0f} x SAU {B.GRIP_D:.0f}")
print(f"  Vach truoc/sau  : day {B.WALL_FB:.0f}")
print(f"  Can be day vach : {B.GRIP_D:.0f} (hoc) + {B.GRIP_BACK:.0f} (thanh sau) "
      f"= {B.GRIP_D+B.GRIP_BACK:.0f} mm")
print(f"  Thieu           : {B.GRIP_D+B.GRIP_BACK-B.WALL_FB:.0f} mm\n")
print("  Ba cach dong khoang thieu:")
tray_end_gap = (B.INNER_Y - B.TRAY[0])/2
opts = [
  ("day RA NGOAI", f"vach 10 -> {B.WALL_FB+C['GRIP_OUT']:.0f} tren bang {B.GRIP_W:.0f} mm",
   f"phu bi Y 350 -> {C['Y_OA']:.0f}  (+{C['Y_OA']-A['Y_BODY']:.0f})", "KHA THI"),
  ("day VAO TRONG", f"long hop {B.INNER_Y:.0f} -> {B.INNER_Y-2*(B.GRIP_D+B.GRIP_BACK-B.WALL_FB):.0f}",
   f"khay quan {B.TRAY[0]:.0f} chi con khe {tray_end_gap:.1f} moi dau; "
   f"long khay {B.TRAY_IN[0]:.0f} phai tut xuong "
   f"{B.TRAY_IN[0]-2*(B.GRIP_D+B.GRIP_BACK-B.WALL_FB):.0f} < "
   f"{12*B.TILE_MAX[0]+2*1.0:.1f} can cho 12 cot", "BAT KHA"),
  ("giam do SAU hoc", f"sau toi da = {B.WALL_FB-B.GRIP_BACK:.0f} mm",
   "ngon tay chi an duoc 4 mm - khong moc duoc 3,7 kg", "BAT KHA"),
]
for a, b, c, v in opts:
    print(f"   [{v:8s}] {a:16s} {b}")
    print(f"   {'':11s}{'':16s} -> {c}")
print(f"\n  => C KHONG PHAI 'khong doi phu bi'. No doi {C['Y_OA']-A['Y_BODY']:.0f} mm theo Y.")
print(f"     Nhung no BO 16 mm theo Z (khong con song khoa noi tren nap).")
volA = A['W']*A['Y_OA']*A['Z_OA']/1e6
volC = C['W']*C['Y_OA']*C['Z_OA']/1e6
print(f"     The tich bao: A {volA:.2f} L  ->  C {volC:.2f} L  "
      f"({(volC-volA)/volA*100:+.0f} %)  — C van la hop NHO HON.")

# ============================================================================
hr("2. HINH HOC HOC AM — vi tri suy ra tu chuoi Z, khong chon tay")
print(f"  Dat DAY hoc ngang san trong (Z{C['Z_FLOOR']:.0f}) — moc go day nhat cua vach")
print(f"  vi duoi cao do do la day hop {B.BOT:.0f} mm do lung phia sau.\n")
for a, b in [("Bang X", f"{C['GRIP_X0']:.0f} .. {C['GRIP_X1']:.0f}  (giua hop, doi xung "
                        f"quanh khe rap giua X={C['X_SEAM']:.0f})"),
             ("Bang Z", f"{C['GRIP_Z0']:.0f} .. {C['GRIP_Z1']:.0f}"),
             ("Be day vach tai hoc", f"{C['WALL_GRIP']:.0f} = {B.WALL_FB:.0f} goc "
                                     f"+ {C['GRIP_OUT']:.0f} noi ra ngoai"),
             ("Thanh sau hoc", f"{B.GRIP_BACK:.0f} mm — ngan cach ngon tay voi long khoang"),
             ("Dai go TREN hoc", f"{C['GRIP_LEDGE']:.2f} mm (toi vanh than tai X={C['GRIP_X0']:.0f})"),
             ("Dai go DUOI hoc", f"{C['GRIP_SKIRT']:.0f} mm, lai duoc day hop {B.BOT:.0f} do lung"),
             ("Va cham ben trong", "khong — toan bo phan them nam NGOAI mat vach goc")]:
    print(f"   {a:22s}: {b}")
print(f"\n  Go noi {C['GRIP_OUT']:.0f} mm chay HET chieu cao vach (Z{B.FOOT:.0f}..vanh) chu khong")
print(f"  chi quanh hoc: nap dai {B.LID_L:.0f} nen tu thut vao {C['GRIP_OUT']:.0f} mm moi ben,")
print(f"  go noi doc thanh hai dai dung tren mat truoc/sau. Chu y, khong phai vet phay.")

# ============================================================================
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
hr("4. EC-GO-NO-MI — 3,7 kg hai tay so voi 7,4 kg mot tay")
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
m_leaf = ((C['V']['khung nap'] + C['V']['mat mong nap'])/2/1e6*B.RHO['cocobolo']
          + C['V']['tam Nu']/2/1e6*B.RHO['Nu go do'])
arm_leaf = (2*B.R_KN + C['LW'])/2 - B.R_KN          # tu truc chot toi trong tam canh
M_shut = m_leaf*9.81*arm_leaf/1000
F_lift = M_shut/((C['LW'] - B.R_KN)/1000)
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
hr("6. NEU MUC TIEU LA DUOI 6 kg")
base = B.mass_of(C, 'loi on dinh')[2]
print(f"  Diem xuat phat: C + khay loi on dinh = {base:.2f} kg\n")
def dm_bot(t):    return C['W']*C['Y_BODY']*(B.BOT-t)/1e6*B.RHO['cocobolo']
def dm_pan(t):    return C['V']['tam Nu']*(1-t/B.PAN_T)/1e6*B.RHO['Nu go do']
def dm_frame():   return C['V']['khung nap']/1e6*(B.RHO['cocobolo']-B.RHO['go do dac'])
body_keys = ['day','vach truoc/sau','go hoc am','vach ngan']
def dm_body():    return sum(C['V'][k] for k in body_keys)/1e6*(B.RHO['cocobolo']-B.RHO['loi on dinh'])
LEV = [("Day hop 8 -> 6", dm_bot(6.0), "day khong chiu tai gi ngoai khay; van du cho ranh vach"),
       ("Tam Nu 10 -> 8", dm_pan(8.0), "mong hon thi de nut khi thao tac tam tha"),
       ("Khung nap sang go do dac", dm_frame(), "MAT dong mau voi than — doi tham my lay 0,1 kg"),
       ("Than sang loi on dinh + veneer", dm_body(),
        "vach TRAI/PHAI phai giu go dac (mang mat mong) nen khong tinh vao day")]
run = base
print(f"  {'don bay':34s}{'-kg':>7s}{'con lai':>9s}   ghi chu")
for lbl, dm, note in LEV:
    run -= dm
    print(f"  {lbl:34s}{dm:7.2f}{run:9.2f}   {note}")
print(f"\n  Quan co {B.N_TILES*B.M_TILE_G/1000:.2f} kg la san cung — khong don bay nao cham toi.")
tiles = B.N_TILES*B.M_TILE_G/1000
print(f"  Ba don bay dau ({sum(x[1] for x in LEV[:3]):.2f} kg) giu nguyen san pham la go dac:")
print(f"    -> {base - sum(x[1] for x in LEV[:3]):.2f} kg. VAN TREN 6.")
print(f"  Chi khi doi THAN sang loi on dinh + veneer moi qua nguong: "
      f"{run:.2f} kg.")
print(f"  Nhung luc do hop khong con la hop go dac nua — va do la mot quyet dinh")
print(f"  ve san pham, khong phai ve ky thuat.")
print(f"\n  => KET LUAN: voi cau tao go dac da chot, san duoi cung la "
      f"~{base - sum(x[1] for x in LEV[:3]):.1f} kg.")
print(f"     6 kg KHONG voi toi duoc. Nen theo dung logic cua chinh may:")
print(f"     khong keo duoc xuong duoi 6 -> chon C.")

# ============================================================================
hr("7. BANG CHOT A ↔ C")
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
    ("Giai khoa nap", "co", "KHONG"),
    ("Do mep tu do cua nap", "co", "them song noi AC-01"),
    ("Rui ro che tao", "trung binh", "thap"),
]:
    print(f"  {a:32s}{x:>26s}{y:>28s}")
