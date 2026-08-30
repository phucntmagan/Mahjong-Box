#!/usr/bin/env python3
"""
Dac ta VAT LIEU va HINH HOC da chot cua hop Mahjong 152 quan (BURLORA).
NGUON SU THAT DUY NHAT - moi script khac import tu day, khong script nao
duoc viet lai mot con so hinh hoc.

CHOT:
  Than, khay, khung nap, song khoa, chot xoay : COCOBOLO (Dalbergia retusa)
  Tam nap                                      : NU GO DO (Afzelia xylocarpa, burl)
  Nap = khung go dac om tam Nu THA trong ranh (khong phai tam lien)
  Be rong  : chuoi X = 370          (CHOT 29-08-2026, tools/width_options.py)
  Xach     : PHUONG AN C, hoc am hai tay  (CHOT 29-08-2026, tools/handle_option_c.py)
             -> phu bi Y = 374, khong con song khoa, khong con quai da
  Day hop  : 8 -> 6                 (CHOT 29-08-2026, giam can)
  Tam Nu   : 10 -> 8                (CHOT 29-08-2026, giam can VA de lay du lip
             cho ranh om tam o do doc canh khe giua - xem selfcheck)

Hai phuong an xach:
  A  song khoa cocobolo 44 x 20 doc khe rap giua + quai da, 2 chot xoay 1/4 vong
     -> xach MOT tay, giai luon khoa nap va do mep tu do cua nap
  C  hai hoc am long ban tay phay vao vach truoc/sau, khong co co cau nao
     -> xach HAI tay, khong giai khoa nap, khong do mep nap (phai them song
        noi giua tren AC-01)

Toan bo the tich duoi day SINH RA tu chuoi kich thuoc, khong go cung.
Doi mot tri so trong phan "CHUOI KICH THUOC" la moi thu tinh lai.
"""
import math

# ============================================================== VAT LIEU
# Tri so cocobolo cong bo thuong 1,05-1,10 (go chim trong nuoc). Chot 1,00 theo
# lo hang thuc te. Do nhay: sai 10 % ty trong -> tai thiet ke doi 6 %, he so an
# toan thap nhat 10x -> 9x. Bien du rong, khong can thiet ke theo dau nang.
RHO = {                       # g/cm3
    'cocobolo'     : 1.00,   # CHOT 24-08-2026 theo lo go thuc te
    'Nu go do'     : 0.90,
    'go do dac'    : 0.82,
    'loi on dinh'  : 0.58,
    'brass'        : 8.50,
}
# he so gian no tuyen tinh, phan tram tren moi 1 % thay doi do am
K = {'doc tho': 0.0001, 'cocobolo ngang tho': 0.0016,
     'go do ngang tho': 0.0015, 'Nu moi phuong': 0.0022, 'loi on dinh': 0.0005}

# tri so co ly cocobolo dung cho kiem ben (MPa)
MOR, E_W, C_PERP, SHEAR = 110.0, 13000.0, 14.0, 13.0
# Keo NGANG THO — tri so yeu nhat cua go, chi phoi viec xe doc thanh go quanh lo
# chot mat mong. Lay ~1/15 MOR, la muc thong dung cho go cung nhiet doi.
T_PERP = 7.0

# derive_mode(): tra ve dac ta o mot ho nghiem ban le khac ma KHONG doi bien toan
# cuc — dung de so sanh hai ho trong hinge_kinematics.py muc 2.
def derive_mode(mode, **kw):
    global HG_MODE
    old = HG_MODE
    try:
        HG_MODE = mode
        return derive(**kw)
    finally:
        HG_MODE = old

M_TILE_G, N_TILES = 16.0, 152
TILE_MAX = (25.7, 36.8, 11.4)     # quan lon nhat theo Rev B

# ============================================================== CHUOI KICH THUOC
# --- X (be rong) : vach | khay | ngan | phu kien | ngan | khay | vach
# Vach ban le 18 la do HOC AM HAI TAY: sau 12 + thanh sau 6. Ban le brass chi an
# Ban le mong go chiem 2*R_KN theo X, van lot trong 18 — xem handle_option_c.py.
# Vach trai/phai KHONG phai so tu chon: no dung bang chieu sau hoc am cong thanh
# sau hoc. Dinh nghia sau khoi hoc am (xem GRIP_D / GRIP_BACK) de khong bao gio lech.
WALL_HINGE = None        # -> gan lai ngay sau khoi HOC AM
BAY        = 126.0       # khoang khay quan
DIV        =   6.0       # vach ngan
AC_BAY     =  70.0       # khoang khay phu kien

# --- Y (chieu sau)
WALL_FB    = 10.0        # vach truoc/sau
INNER_Y    = 330.0       # long hop theo Y

# --- phuong an xach
HANDLE     = 'C'         # CHOT: 'C' hoc am hai tay ('A' song khoa + quai da)
POST_W     =  44.0       # (A) be rong tru quai, bang be rong song khoa
POST_OUT   =   6.0       # (A) tru nho ra ngoai
POST_IN    =   4.0       # (A) tru an vao trong
# Hoc am nay o VACH TRAI/PHAI (vach ban le, day 18) chu khong o vach truoc/sau.
# Ly do: vach truoc/sau chi day 10 nen hoc am 16 sau + khe luon ngon 6 sau an
# thung vach; va vach truoc/sau con phai mang ca ba khe luon ngon lan nam cham.
# Vach 18 nuot duoc hoc sau 12 + thanh sau 6 ma KHONG phai noi go ra ngoai.
GRIP_W, GRIP_D = 120.0, 16.0     # (C) hoc am: rong (theo Y) x sau (theo X)
GRIP_BACK  =   6.0       # (C) go con lai phia sau hoc
WALL_HINGE = GRIP_D + GRIP_BACK    # vach ban le suy ra tu hoc am — 16 + 6 = 22
# CHIEU CAO hoc am KHONG con la so tu chon. Ha bac ban le lay het go o
# x < REBATE_D tu Z(Z_RIM - REBATE_H) len vanh; tran hoc phai nam DUOI dai do,
# neu khong thi doan tran o phia mat ngoai bi rong va ngon tay khong bau vao dau
# duoc. Vay khe ho vao tay tai mat ngoai la mot HE QUA:
#     GRIP_APER = Z_RIM - REBATE_H - GRIP_LIP - Z_FLOOR
# Xem tools/grip_hook.py — moi tri so duoi day deu duoc suy o do.
GRIP_LIP_REQ =  4.0      # go dac toi thieu con lai TREN tran hoc, o moi diem x
GRIP_SLOPE =  10.0       # tran hoc doc len phia trong (do). Chan tren = atan(MU_SKIN)
GRIP_R     =   8.0       # bo tron mep ngoai tran hoc — tools/grip_hook.py muc 3
                         # Rev C2 phai lay R4 vi ha bac ban le khoa tran hoc xuong.
                         # Rev C3 bo ha bac -> chon lai theo ap luc: R >= 6,86 cho
                         # muc tieu 200 kPa, lam tron LEN dao R8 co san.
MU_SKIN    =   0.40      # ma sat da tay tren go danh bong (tra bang, lay can duoi)
FING_T_DIP =  16.0       # be day ngon tay o khop DIP (nam giua)
FING_T_TIP =  11.0       # be day ngon tay o dau mut
FING_W     =  16.0       # be rong mot ngon
N_FING     =   4         # so ngon chiu luc moi tay
L_DISTAL   =  15.0       # chieu dai dot ngon ngoai cung
FING_MAR   =   0.5       # khe toi thieu giua lung ngon tay va day hoc
WRAP_SKIN  =  60.0       # goc da dau ngon boc quanh mep bo (do)
P_COMFORT  =   0.40      # CAN CUNG: tren muc nay la dau, khong xach duoc (MPa)
P_TARGET   =   0.20      # MUC TIEU thiet ke: xach lau khong kho chiu (MPa)
# (C) song noi giua tren AC-01: DA BO. tools/detail_features.py muc 3 tinh lai do
# vong mep tu do cua nap o be day 12 (khong phai 8 nhu Rev B) va cho 0,6 mm duoi
# 50 N — khong can do. Bo song lai giai luon xung dot song-vs-ranh Joker.
FELT     = 0.8           # ni lot khay
FELT_PAD = 0.8           # (C) dem ni duoi nap de ep khay, thay cho song noi

# --- Z (chieu cao), Z=0 la mat ban
FOOT   =  2.0            # chan dem
BOT    =  6.0            # day hop (8 -> 6)
BOT_TON=  4.0            # mong day chay vao ranh trong vach
TRAY_H = 19.0            # chieu cao mot khay quan
N_STACK = 2              # so khay chong trong mot khoang
CLR_Z  =  1.0            # khe tren dinh khay
# Nap DEU, khong vat. Be day nap KHONG con rang buoc ban le (xem phan BAN LE).
# Nay la lua chon TU DO: doi 1 mm be day nap = 0,06 kg va 1 mm khay bo bai.
#   12 -> khay 4,0  cao 59  6,11 kg      15 -> khay 5,0  cao 62  6,29 kg
#   18 -> khay 8,0  cao 65  6,53 kg
T_LID   = 15.0           # day nap
T_HINGE = T_LID          # giu ten cu cho cac script da viet
T_SEAM  = T_LID
SPINE_T, SPINE_INSET = 20.0, 4.0   # (A) song khoa day 20, am 4 vao nap

# --- nap
SEAM    = 1.5            # khe rap giua (0,6 -> 1,5 vi gian no khung go dac)
STILE   = 34.0           # be rong do doc (ca hai canh)
RAIL    = 30.0           # be rong do ngang
PAN_T   =  7.0           # day tam Nu
GRV     =  9.0           # ranh om tam: sau 9
TON     =  6.0           # canh tam an vao ranh 6 -> tam THA 3 mm moi phia
GRV_W   = PAN_T          # ranh rong dung bang day tam: tam KHONG bi phay bac.
                         # Nu tho xoan loan, mot bac 1,5 mm tren canh tam la cho nut.
S_TOP   =  3.0           # lip khung phia TREN ranh om tam.
# CHOT Rev C3: tam Nu NGANG BANG mat khung — mat nap la mot mat phang lien.
# Cach lam: tam NANG (raised panel). Tam la mot vong go day PAN_T + S_TOP, phay
# mot bac sau S_TOP rong (TON + PAN_REV) quanh mep TREN -> con lai mot mong day
# PAN_T tha trong ranh khung nhu cu, con LONG tam dang len ngang mat khung.
# Tam van THA (khong dan), nen giua canh long tam va mep trong khung phai chua
# mot khe PAN_REV de tam no ra khong dap vao khung.
PAN_REV =  1.5           # khe ho quanh long tam (reveal). Suy o tools/lid_solid_calc.py
DMC_DES =  2.0           # bien thien am go, +/- % quanh do am LAP RAP (da on dinh 11 %)
DMC_DRY =  4.0           # neu lap thang o do am xuong 9 % ma khong on dinh truoc:
                         # go chi no MOT CHIEU, ca 4 % doi ve mot phia
LID_L   = 350.0          # chieu dai canh nap (theo Y, khong ke tru/hoc am)

# ============================================================== BAN LE — MONG GO
# RANG BUOC DA CHOT TU DAU: ban le lam bang MONG GO, khong dung kim loai.
# (Kim loai chi duoc chap nhan cho KHOA NAP — xem docs/KHOA-NAP.md.)
#
# Cai duy nhat con la BIEN la CHO DAT TRUC. hinge_kinematics.py muc 1 chung minh
# chi co DUNG HAI ho nghiem hinh hoc, khong co ho thu ba:
#
#   A. Truc nam TRONG vat lieu, tai TAM mat dau canh nap -> (T_LID/2 , Z_RIM+T_LID/2)
#      Dau canh nap buoc phai bo tron ban kinh R = T_LID/2 (tiep tuyen ca hai mat
#      nap). Ong go = chinh dau canh nap, KHONG nho ra ngoai phu bi. Nhung R bi
#      be day nap ep cung, va o 180 do KHONG co mat chan tu nhien.
#
#   B. Truc nam TREN MAT PHANG NGOAI cua than (x = 0), tai arris (0 , Z_RIM)
#      Hai goc dau canh nap trung voi truc -> ban kinh quet 0, khong phai bo tron
#      gi ca. R cua ong go duoc TU DO chon theo do ben chu khong theo be day nap.
#      Gia: ong nho ra ngoai dung R moi ben. Duoc: o 180 do mat canh nap ap thang
#      vao mat ngoai vach -> mat chan tu nhien, va canh mo nam PHANG voi vanh than.
#
#   C. Truc LUI VAO dung R, van o cao do vanh -> (R , Z_RIM)
#      Ong go tiep tuyen mat ngoai vach TU BEN TRONG: KHONG nho ra ti nao.
#      Doi lai hai thu, ca hai deu suy ra duoc bang so:
#        - mat dau canh nap phai lui vao dung R (neu khong no quet vao vach);
#        - vanh ngoai TREN cua vach phai ha bac R sau x T_LID cao de mat dau
#          canh nap co cho quet qua.
#      Dong hoc va mat chan 180 do giong het ho B.
#
# Doi HG_MODE thi moi tri so duoi day tu suy lai.
# CHOT Rev C3 — BO HA BAC, quay ve ho B.
# Ha bac 6,1 x 15 chay suot vach ban le la thu KHOA tran hoc am xuong Z28, va
# lam dai go tren hoc chi con 15,9 day thay vi 22. Bo no thi vach ban le lien
# khoi tu san toi vanh; tran hoc am duoc tha len va ban kinh bo mep di tu R4
# len R8 (ap luc luc bat luc 343 -> 171 kPa). Gia phai tra: ong go nho ra dung
# R moi ben. Bu lai bang cach HA ONG: chot O5 + thanh 2,5 -> ong O10,2.
HG_MODE  = 'B'           # 'A' truc giua be day nap | 'B' truc tren mat ngoai (nho ra)
                         # 'C' truc lui vao dung R -> ong go AM HOAN TOAN, khong nho ra
KN_PIN   =  5.0          # duong kinh chot go (cocobolo thang tho)
KN_FIT   =  0.20         # khe lo chot: lo O(KN_PIN + KN_FIT)
KN_WALL  =  2.5          # thanh go quanh lo chot — CHI dung o mode B (mode A: R bi ep)
                         # 2,5 la CAN DUOI: phai do do troi mui khoan <= 0,10 mm
                         # tren 160 mm TRUOC khi chot (xem CHOT-REV-C.md muc 8/7)
N_KN     =  7            # so mat mong; le -> hai dau thuoc THAN
KN_LEN   = 44.0          # dai mot mat mong
KN_GAP   =  1.0          # khe doc truc giua hai mat mong (cho go no theo mua)
KN_PIN_L = 160.0         # dai mot chot; 2 chot moi canh, gap nhau o mat mong giua
RHO_BRASS = 8.5          # g/cm3

# --- song khoa + quai (phuong an A)
SPINE_W = 44.0
SPINE_REC = (144.0, 32.0, 10.0)   # hoc chua quai tren song

# --- khoa nap (CHOT 29-08-2026 — xem tools/lid_latch.py)
# Dong hoc buoc khoa phai noi NAP voi THAN va chi chan phuong Z:
#   - hai canh cung mo thi chi tach nhau 18*theta trong khi nang 175*theta, nen
#     moi khoa noi CANH-CANH deu tuot ra sau khi khe da venh hang chuc mm;
#   - khe rap giua con dong/mo 1,09 mm theo mua, nen khoa canh-canh phai co tung
#     ay re theo X, tu no da cho venh 10,6 mm.
# Chan Z, tu do theo X: nam cham. Khong co chi tiet nao chuyen dong.
MAG      = (20.0, 5.0, 5.0)   # nam cham khoi: dai (X) x rong (Y) x day (Z)
MAG_REC  =  5.2               # sau hoc am nam cham
# Vi tri X bi ep giua hai chi tiet khac: khe luon ngon nhac khay an het dai vanh
# than o giua moi khoang, nen nam cham chi con nam duoc trong khoang trong giua
# hai khe. Xem selfcheck() — day la va cham hinh 3D bat duoc.
MAG_X    = (122.0, 144.0)     # tam nam cham tren canh TRAI; canh phai doi xung
MAG_Y    =  5.5               # tam theo Y, tinh tu mat ngoai vach truoc
MAG_EDGE =  2.0               # go toi thieu con lai quanh hoc nam cham
# Be DAY nam cham la bien tu do duy nhat: dai bi khe luon ngon ep, rong bi vach
# 10 mm ep, con day thi nap va vanh than deu con du go. Neu do thuc te thieu luc,
# tang day (va MAG_REC) chu khong doi gi khac.
MAG_PULL = 30.0               # N moi cap, tiep xuc truc tiep — PHAI DO LAI tren mau that
MAG_DERATE = 0.25             # tut luc do lop hoan thien chen giua hai mat
MAG_GRADE= 'N45, ma Ni'
RHO_MAG  = 7.5                # g/cm3

# --- khay
TRAY = (325.0, 124.0, TRAY_H)     # khay quan phu bi
TRAY_IN = (315.0, 114.0, 15.0)    # long khay quan
AC_H = 38.0                       # chieu cao khay phu kien
AC_WALL = 5.0
AC_JOKER = (28.0, 152.0, 24.5)    # ranh Joker (rong, dai, sau)
AC_AUX_L, AC_AUX_D = 80.0, 18.5   # hoc 4 quan du phong (dai, sau)
AC_DICE_D = 18.5                  # o xuc xac (sau); chieu dai = phan con lai
AC_CLR   =  2.5                   # khe moi dau khay trong khoang (bang khay quan)

# --- hoc nhac khay (review Rev B §2.3 giai lai — xem tools/detail_features.py)
WELL_W   = 50.0          # be rong hoc ngon (chua ca nam cham tren cung vanh)
WELL_D   =  6.0          # sau vao vach (vach 10 -> con 4 mm da ngoai)
NOTCH_D  =  5.0          # khoet XUYEN mat dau khay (day vach khay 5)
NOTCH_H  = 12.0          # cao khoet, tinh tu vanh khay xuong
WELL_FELT=  1.0          # ni dan vao day hoc: chan quan truot ra va lam dem

# --- hom ngon ranh Joker
SCAL_D   = 25.0          # duong kinh hom ban nguyet
SCAL_DEP = 12.0          # sau khoet vao dai go ben ranh

# --- o xuc xac + nap che
DICE_SOCK  = 18.0        # canh o vuong
DICE_SOCK_D= 18.0        # sau o (xuc xac 16 phai chim han: khe duoi nap chi 1 mm)
DICE_RIB   =  5.0        # vach giua cac o
COVER_T    =  4.0        # day nap che o xuc xac
COVER_LIP  =  3.0        # bac ha nap che quanh mieng o

# ============================================================== SUY RA
# Toan bo hinh hoc suy ra tu chuoi X va phuong an xach. Tach thanh ham de so
# sanh duoc cac phuong an bang CHINH bo cong thuc nay, khong uoc luong bang tay.
def derive(wall_hinge=WALL_HINGE, bay=BAY, div=DIV, ac_bay=AC_BAY, handle=HANDLE):
    d = {}
    W       = 2*wall_hinge + 2*bay + 2*div + ac_bay      # phu bi X
    Y_BODY  = 2*WALL_FB + INNER_Y                        # phu bi Y khong ke nho ra

    # --- phuong an xach quyet dinh phu bi Y va Z
    if handle == 'A':
        post_out, post_in = POST_OUT, POST_IN
        grip_out = 0.0
        Z_PROUD = SPINE_T - SPINE_INSET                  # song khoa noi tren nap
    else:
        post_out, post_in = 0.0, 0.0
        # Hoc am o VACH TRAI/PHAI (day wall_hinge). Hoc sau GRIP_D can
        # GRIP_D + GRIP_BACK be day vach — vach 18 nuot duoc 12 + 6 nen KHONG
        # phai noi go ra ngoai: phu bi khong doi.
        grip_out = max(0.0, GRIP_D + GRIP_BACK - wall_hinge)
        Z_PROUD = 0.0
    GRIP_OUT = grip_out
    NHO_RA  = max(post_out, grip_out)
    Y_OA    = Y_BODY + 2*NHO_RA                          # phu bi Y
    AC_Y    = INNER_Y - 2*post_in                        # LONG khoang phu kien theo Y
    AC_L    = AC_Y - 2*AC_CLR                            # DAI khay AC-01 (khe moi dau)

    Z_FLOOR    = FOOT + BOT                              # san trong
    Z_TRAY_TOP = Z_FLOOR + N_STACK*TRAY_H
    Z_RIM      = Z_TRAY_TOP + CLR_Z                      # vanh than tai canh mong
    Z_LID      = Z_RIM + T_HINGE                         # mat tren nap
    Z_SEAM     = Z_LID - T_SEAM                          # vanh than tai khe giua
    Z_OA       = Z_LID + Z_PROUD                         # phu bi Z
    Z_RIM_AVG  = (Z_RIM + Z_SEAM)/2                      # vanh doc deu 49 -> 55 -> 49

    # ---------------------------------------------------- ban le mong go
    KN_HOLE = KN_PIN + KN_FIT
    if HG_MODE == 'A':
        # Truc o TAM mat dau canh nap. Ong go = dau canh nap bo tron, tiep tuyen
        # ca mat tren lan mat duoi -> R BI EP bang nua be day nap.
        R_KN  = T_LID/2
        PIN_X, PIN_Z = R_KN, Z_RIM + R_KN
        LEAF_X0 = 0.0                            # mep ngoai canh nap (mui tron toi x=0)
        REBATE_D = REBATE_H = 0.0
        STOP_H = 0.0                             # KHONG co mat chan tu nhien
    elif HG_MODE == 'B':
        # Truc TREN mat phang ngoai, o arris. Khong phai bo tron gi.
        R_KN  = KN_HOLE/2 + KN_WALL
        PIN_X, PIN_Z = 0.0, Z_RIM
        LEAF_X0 = 0.0
        REBATE_D = REBATE_H = 0.0
        STOP_H = T_LID - R_KN
    else:
        # Truc LUI VAO dung R: ong tiep tuyen mat ngoai vach TU BEN TRONG.
        # Ong chim han, khong nho ra ti nao. Hai he qua bat buoc:
        #   - mep ngoai canh nap phai lui vao dung R (LEAF_X0), neu khong mat dau
        #     canh se quet vao vach khi mo;
        #   - vanh ngoai TREN cua vach phai ha bac REBATE_D sau x REBATE_H cao,
        #     lay cho cho mat dau canh nap quet qua.
        R_KN  = KN_HOLE/2 + KN_WALL
        REBATE_D, REBATE_H = R_KN, T_LID        # ha bac PHAI bang ban kinh ong
        PIN_X, PIN_Z = REBATE_D, Z_RIM          # truc nam dung tren mat ha bac
        LEAF_X0 = PIN_X
        STOP_H = T_LID - R_KN
    # Nho ra ngoai KHONG duoc gan bang tay: suy tu chinh hinh hoc. Ong go tam
    # (PIN_X, Z_RIM) ban kinh R_KN chiem x tu PIN_X-R_KN; am thi nho ra ngoai.
    PROUD = max(0.0, R_KN - PIN_X)
    LW    = (W - SEAM)/2 - LEAF_X0               # be rong VAT LY mot canh nap
    REACH = (W - SEAM)/2 - PIN_X                 # canh mo vuon ra bao nhieu tu truc
    KN_WALL_EFF = R_KN - KN_HOLE/2               # thanh go that quanh lo chot
    KN_PITCH = KN_LEN + KN_GAP
    KN_RUN   = N_KN*KN_LEN + (N_KN - 1)*KN_GAP
    KN_Y0    = (LID_L - KN_RUN)/2                # chuoi mong dat giua chieu dai canh
    N_KN_BODY = (N_KN + 1)//2                    # mong le thuoc THAN
    N_KN_LID  = N_KN//2                          # mong chan thuoc NAP
    if HG_MODE == 'A':
        STOP_A = 0.0
    else:
        # trong doan mong, ong go an mat R nen chan chi cao STOP_H; ngoai doan
        # mong mat dau canh nap con vuong nen chan cao ca be day nap.
        STOP_A = KN_RUN*STOP_H + (LID_L - KN_RUN)*T_LID
    X_OA   = W + 2*PROUD                         # phu bi X ke ca ong go nho ra
    TAPER  = LW
    SLOPE  = 0.0
    ANG    = 0.0
    OP_W   = LW - 2*STILE                                # long khung theo X
    OP_L   = LID_L - 2*RAIL                              # long khung theo Y
    PAN_W, PAN_L = OP_W + 2*TON, OP_L + 2*TON            # tam Nu (do ca mong)
    # --- tam NANG: long tam dang len ngang mat khung, chua khe PAN_REV moi phia
    PAN_TH   = PAN_T + S_TOP                             # be day toan bo tam
    FIELD_W  = OP_W - 2*PAN_REV                          # long tam (phan dang len)
    FIELD_L  = OP_L - 2*PAN_REV
    PAN_REB  = TON + PAN_REV                             # be rong bac phay quanh mep tren
    PAN_FLOAT = GRV - TON                                # tam tha bao nhieu trong ranh
    # go no theo mua: tam Nu no deu moi phuong. Moi phia dich mot NUA tong.
    PAN_MOVE_W = PAN_W*K['Nu moi phuong']*DMC_DES/2      # dich moi phia theo X
    PAN_MOVE_L = PAN_L*K['Nu moi phuong']*DMC_DES/2      # dich moi phia theo Y
    PAN_MOVE   = max(PAN_MOVE_W, PAN_MOVE_L)
    PAN_MOVE_DRY = max(PAN_W, PAN_L)*K['Nu moi phuong']*DMC_DRY/2   # lap kho, no mot chieu
    X_SEAM = W/2                                         # tam khe rap giua

    def z_rim_at(x):
        """Cao do vanh than tai toa do x.

        Nap deu, khong vat -> vanh phang suot.
        """
        return Z_RIM
    def t_lid(x):
        """Day nap tai x. Nap deu nen hang so."""
        return T_LID
    def _int_t(a, b):
        return T_LID*(b - a)

    # --- lip cua ranh om tam Nu: khung vat nen cho mong nhat la mep trong
    #     cua do doc canh khe giua (x = LW - STILE)
    LIP_BOT = t_lid(LW - STILE) - S_TOP - PAN_T

    # --- khoa nap bang nam cham: ban kinh tay don tinh tu truc chot ban le
    pass
    MAG_R = tuple(x - PIN_X for x in MAG_X)          # tay don moi nam cham
    MAG_N_LEAF = 2*len(MAG_X)                        # 2 dau hop x so vi tri
    MAG_SUM_R = 2*sum(MAG_R)                         # tong tay don mot canh
    MAG_MAR_OUT = MAG_Y - MAG[1]/2                   # go tu mep nap toi hoc
    MAG_MAR_IN  = WALL_FB - (MAG_Y + MAG[1]/2)       # go tu hoc toi mat trong vach

    # --- hoc am (phuong an C) tren VACH TRAI/PHAI, giua chieu sau hop
    GRIP_Y0   = Y_BODY/2 - GRIP_W/2
    GRIP_Y1   = Y_BODY/2 + GRIP_W/2
    GRIP_Z0   = Z_FLOOR                                  # day hoc ngang san trong
    WALL_GRIP = wall_hinge + grip_out                    # be day vach tai hoc
    GRIP_SKIRT = GRIP_Z0 - FOOT                          # dai go duoi hoc am

    # --- TRAN HOC AM: bo tron mep ngoai + doc len phia trong.
    # Cao do tran KHONG con lay tu chan tren cua vach (Rev C2 lay tu day ha bac,
    # va do la mot su tinh co: ha bac bien mat thi tri so do vo nghia). Nay tran
    # duoc suy tu CHINH BAN TAY: nang tran vua du de khe hep nhat giua lung ngon
    # tay va san hoc bang dung FING_MAR. Vach con du go hay khong la mot cau hoi
    # RIENG, kiem doc lap o GRIP_LIP_MIN.
    _th       = math.radians(GRIP_SLOPE)
    GRIP_TANG = GRIP_R/math.tan(math.radians((90.0 - GRIP_SLOPE)/2))  # dinh -> tiep diem
    GRIP_XT   = GRIP_R*(1.0 + math.sin(_th))             # x tiep diem cung/tran
    GRIP_FLAT = GRIP_D - GRIP_XT                         # doan tran phang con lai
    GRIP_ARC  = GRIP_R*math.radians(90.0 + GRIP_SLOPE)   # do dai cung bo tron
    GRIP_SURF = GRIP_ARC + GRIP_FLAT/math.cos(_th)       # CHIEU DAI BE MAT tran hoc

    def fing_t(x):
        """Be day ngon tay tai x, gia thiet dau mut cham day hoc (x = GRIP_D)."""
        u = min(max(GRIP_D - x, 0.0), L_DISTAL)
        return FING_T_TIP + (FING_T_DIP - FING_T_TIP)*u/L_DISTAL

    def _ceil_at(z1, x):
        """Tran hoc neu dinh ao dat o z1: cung bo tron roi mat doc."""
        cz = z1 + GRIP_TANG
        if x <= GRIP_XT:
            return cz - math.sqrt(max(0.0, GRIP_R*GRIP_R - (x - GRIP_R)**2))
        return z1 + x*math.tan(_th)

    _n = 128
    def _fit_at(z1):
        return min(_ceil_at(z1, GRIP_D*i/_n) - GRIP_Z0 - fing_t(GRIP_D*i/_n)
                   for i in range(_n + 1))
    # _fit_at tang tuyen tinh theo z1 (cong them mot hang so), nen giai truc tiep
    GRIP_Z1   = GRIP_Z0 + FING_MAR - _fit_at(GRIP_Z0)    # DINH ao cua tran (tai x=0)
    GRIP_H    = GRIP_Z1 - GRIP_Z0                        # chieu cao doan tran phang keo ve x=0
    GRIP_Z_TOP = GRIP_Z1 + GRIP_TANG                     # dinh bo tron, tai mat ngoai
    GRIP_APER = GRIP_Z_TOP - GRIP_Z0                     # khe ho vao tay tai mat ngoai
    GRIP_CX, GRIP_CZ = GRIP_R, GRIP_Z_TOP                # tam cung bo tron
    GRIP_ZT   = GRIP_CZ - GRIP_R*math.cos(_th)
    GRIP_Z_IN = GRIP_Z1 + GRIP_D*math.tan(_th)           # tran tai day hoc (x = GRIP_D)

    def grip_ceil(x):
        """Cao do TRAN hoc tai x (0 = mat ngoai vach). Cung bo tron roi mat doc."""
        return _ceil_at(GRIP_Z1, min(max(x, 0.0), GRIP_D))

    def grip_top(x):
        """Cao do THAP NHAT cua thu nam tren dau vach tai x — tran hoc phai o duoi.
        Ho C: ha bac ban le. Ho B: hom cua mat mong NAP khoet vao goc tren-ngoai
        cua than, ban kinh R_KN quanh (0 , Z_RIM)."""
        if REBATE_H > 0 and x < REBATE_D: return Z_RIM - REBATE_H
        if x < R_KN:                      return Z_RIM - R_KN
        return Z_RIM

    def grip_profile(n=14):
        """Bien duoi cua dai go tren hoc: cung bo tron roi mat doc. Tu mat ngoai
        (0 , GRIP_Z_TOP) vao toi day hoc (GRIP_D , GRIP_Z_IN)."""
        sw = 90.0 + GRIP_SLOPE                           # cung quet 100 do
        pts = [(GRIP_CX + GRIP_R*math.cos(math.radians(180.0 + sw*i/n)),
                GRIP_CZ + GRIP_R*math.sin(math.radians(180.0 + sw*i/n)))
               for i in range(n + 1)]
        return pts + [(GRIP_D, GRIP_Z_IN)]

    # dien tich TIET DIEN hoc am (chu nhat + net doc + phan bo tron) — tich phan so
    _m = 256
    GRIP_A = sum((grip_ceil(GRIP_D*i/_m) + grip_ceil(GRIP_D*(i+1)/_m))/2 - GRIP_Z0
                 for i in range(_m))*GRIP_D/_m

    # dai go tren hoc — duong truyen luc khi xach. Ho C bi ha bac an mat REBATE_D
    # o mat ngoai; ho B khong bi gi, dai go day het be day vach.
    GRIP_LEDGE_T = WALL_GRIP - REBATE_D
    GRIP_LEDGE   = Z_RIM - GRIP_Z_TOP                    # CHIEU CAO dai go, do tu dinh bo tron

    GRIP_FIT = _fit_at(GRIP_Z1)                          # khe hep nhat lung ngon/day hoc
    GRIP_LIP_MIN = min(grip_top(GRIP_D*i/_n) - grip_ceil(GRIP_D*i/_n)
                       for i in range(_n + 1))           # go dac mong nhat TREN tran
    GRIP_EJECT = math.tan(_th)                           # he so day ngon tay ra

    # --- khay phu kien: chuoi dai khep ve AC_Y
    AC_W_OUT  = ac_bay - 2.0                             # khe 1,0 moi ben
    AC_W_IN   = AC_W_OUT - 2*AC_WALL
    AC_DICE_L = AC_L - 4*AC_WALL - AC_JOKER[1] - AC_AUX_L

    # --- hoc nhac khay: khe luon ngon tay va mo moc len
    # Khe luon ngon CHI o hai khoang khay. Khoang phu kien KHONG co khe: hoc am
    # hai tay chiem bang X {GRIP_X0}..{GRIP_X1} va an sau 16 tu mat ngoai, con khe
    # luon ngon an 6 tu mat trong — cong lai vua dung het be day vach 10, tuc thung
    # vach. AC-01 duoc nhac bang hai hom ngon ranh Joker doi nhau (kep hai dai go).
    # Ca BA khoang deu co khe luon ngon. Truoc day khoang phu kien khong the co
    # vi hoc am hai tay nam tren cung vach truoc; nay hoc am da chuyen sang vach
    # trai/phai nen xung dot do bien mat, va AC-01 duoc nhac dung nhu khay quan.
    WELL_X = (wall_hinge + bay/2, X_SEAM, W - wall_hinge - bay/2)
    LIFT_CHANNEL = WELL_D + AC_CLR + NOTCH_D - WELL_FELT  # be rong khe luon ngon (Y)
    LIFT_LEDGE   = NOTCH_D                                # be sau mo de moc ngon
    Z_LIFT_LEDGE = Z_FLOOR + 2*TRAY_H - NOTCH_H           # cao do mo cua khay TREN
    TILE_TOP  = (TRAY_H - TRAY_IN[2]) + FELT + TILE_MAX[2]  # dinh quan so voi day khay
    HEADROOM  = TRAY_H - TILE_TOP                        # vanh khay cao hon quan
    TILE_OPEN = NOTCH_H - HEADROOM                       # quan bi ho ra ben hong khoet
    LIFT_LIP  = TRAY_H - NOTCH_H                         # chieu cao mo con lai duoi khoet
    SCAL_LEFT = (AC_W_IN - AC_JOKER[0])/2 - SCAL_DEP     # dai go con lai ben ranh Joker


    # ---------------------------------------------------- the tich (mm3)
    v = {}
    v['day']            = W*Y_BODY*BOT
    v['vach truoc/sau'] = (2*(W*WALL_FB*(Z_RIM_AVG - Z_FLOOR))
                           - 4*(WELL_W*WELL_D*(z_rim_at(wall_hinge + bay/2) - Z_FLOOR)))
    # --- go them/bot vi mat mong (tinh tren TIET DIEN, mm2, roi nhan chieu dai)
    A_DISC = math.pi*R_KN**2                             # tiet dien ong go
    A_HOLE = math.pi*(KN_HOLE/2)**2                      # lo chot
    if HG_MODE == 'A':
        # than: moi mat mong THAN la mot tru moc len tren vanh (ca dia nam tren Z_RIM)
        dV_body = N_KN_BODY*KN_LEN*(A_DISC - A_HOLE)
        # nap: cho mat mong THAN thi canh nap bi khoet lui het o vuong 2R x T_LID;
        #      cho mat mong NAP thi dau canh bo tron (bot hai mieng goc)
        A_NOSE  = R_KN*T_LID - A_DISC/2                  # phan bo di khi bo tron dau canh
        dV_lid  = -(N_KN_BODY*KN_LEN*(2*R_KN*T_LID)
                    + N_KN_LID*KN_LEN*(A_NOSE + A_HOLE))
    elif HG_MODE == 'B':
        # arris: trong doan mong, phan them = nua dia nam ngoai mat phang x=0
        # Ho B: truc nam DUNG tren arris. Mot dia tam (0 , Z_RIM) chia lam bon
        # phan tu: goc tren-trong da nam trong canh nap, goc duoi-trong da nam
        # trong khoi vach. Nen mot mat mong chi THEM 3/4 dia (tru ca lo chot),
        # va o cho mat mong CUA BEN KIA thi ben nay phai KHOET di 1/4 dia.
        dV_body = (N_KN_BODY*KN_LEN*(3*A_DISC/4 - A_HOLE)
                   - N_KN_LID*KN_LEN*A_DISC/4)
        dV_lid  = (N_KN_LID*KN_LEN*(3*A_DISC/4 - A_HOLE)
                   - N_KN_BODY*KN_LEN*A_DISC/4)
    else:
        # Mode C. Ha bac lay di REBATE_D x REBATE_H suot chieu dai canh khoi vanh.
        # Ong go nam gon trong x 0..2R: mot phan tu dia (x>R, z<Z_RIM) von da la go
        # vach nen khong tinh them; ba phan tu con lai la go them.
        dV_body = (-REBATE_D*REBATE_H*LID_L
                   + N_KN_BODY*KN_LEN*(3*A_DISC/4 - A_HOLE)
                   - N_KN_LID*KN_LEN*A_DISC/4)
        dV_lid  = (N_KN_LID*KN_LEN*(3*A_DISC/4 - A_HOLE)
                   - N_KN_BODY*KN_LEN*A_DISC/4)
    v['vach trai/phai'] = 2*(INNER_Y*wall_hinge*(Z_RIM - Z_FLOOR)) + 2*dV_body
    x_div = wall_hinge + bay + div/2                     # vach ngan cao toi vanh tai chinh no
    v['vach ngan']      = 2*(INNER_Y*div*(z_rim_at(x_div) - Z_FLOOR))
    v['khay quan']      = 4*(TRAY[0]*TRAY[1]*TRAY[2]
                             - TRAY_IN[0]*TRAY_IN[1]*TRAY_IN[2]
                             - 2*WELL_W*NOTCH_D*NOTCH_H)
    v['khay phu kien']  = (AC_L*AC_W_OUT*AC_H
                           - AC_JOKER[0]*AC_JOKER[1]*AC_JOKER[2]
                           - AC_W_IN*AC_DICE_L*AC_DICE_D
                           - AC_W_IN*AC_AUX_L*AC_AUX_D)
    # khung nap: do doc canh mong (phan dac x 18..34) + do doc canh khe giua
    # + 2 do ngang ; tru ranh am song khoa va ranh om tam Nu
    st_h   = LID_L*_int_t(0.0, STILE) + dV_lid           # do doc ban le, da ke mat mong
    st_s   = LID_L*_int_t(LW-STILE, LW)
    if handle == 'A':
        st_s -= (SPINE_W/2 - SEAM/2)*LID_L*SPINE_INSET   # ranh am cho song khoa
    rails  = 2*RAIL*_int_t(STILE, LW-STILE)
    groove = (2*OP_W + 2*OP_L)*GRV*GRV_W
    v['khung nap']      = 2*(st_h + st_s + rails - groove)
    v['tam Nu']         = 2*(PAN_W*PAN_L*PAN_T + FIELD_W*FIELD_L*S_TOP)

    if handle == 'A':
        v['tru quai']   = 2*(POST_W*(POST_OUT+POST_IN)*(Z_SEAM - Z_FLOOR))
        v['song khoa']  = (Y_OA*SPINE_W*SPINE_T
                           - SPINE_REC[0]*SPINE_REC[1]*SPINE_REC[2])
        V_THAN = ['day','vach truoc/sau','tru quai','vach trai/phai','vach ngan']
        V_NAP  = ['khung nap','song khoa']
    else:
        # hoc am khoet vao vach trai/phai (khong con go noi ra ngoai)
        v['vach trai/phai'] -= 2*GRIP_W*GRIP_A
        v['nap che o xuc xac'] = (AC_W_IN + 2*COVER_LIP)*(2*DICE_SOCK + 3*DICE_RIB)*COVER_T
        # hoc am nam cham khoet vao nap va vao vanh than (4 moi canh + 4 doi ung)
        n_mag = 2*MAG_N_LEAF
        v['khung nap'] -= n_mag*MAG[0]*MAG[1]*MAG_REC
        v['vach truoc/sau'] -= n_mag*MAG[0]*MAG[1]*MAG_REC
        V_THAN = ['day','vach truoc/sau','vach trai/phai','vach ngan']
        V_NAP  = ['khung nap']
    V_KHAY = ['khay quan','khay phu kien'] + (['nap che o xuc xac'] if handle=='C' else [])
    V_KIM  = []                      # KHONG co chi tiet kim loai nao trong ban le

    d.update({k: val for k, val in locals().items()
              if k.isupper() or k in ('t_lid', '_int_t', 'z_rim_at',
                                      'grip_ceil', 'grip_profile', 'grip_top', 'fing_t')})
    d.update(dict(HG_MODE=HG_MODE, WALL_HINGE=wall_hinge, BAY=bay, DIV=div, AC_BAY=ac_bay,
                  HANDLE=handle, V=v, V_THAN=V_THAN, V_KHAY=V_KHAY, V_NAP=V_NAP,
                  V_KIM=V_KIM))
    return d

globals().update(derive())
MAT = {'tam Nu': 'Nu go do'}

# ============================================================== KHOI LUONG
def mass_of(d, khay='cocobolo'):
    """Khoi luong (kg): (go, quan, tong) cua mot phuong an d tra ve tu derive()."""
    V = d['V']
    m  = sum(V[k] for k in d['V_THAN'] + d['V_NAP'])/1e6*RHO['cocobolo']
    m += sum(V[k] for k in d['V_KHAY'])/1e6*RHO[khay]
    m += V['tam Nu']/1e6*RHO['Nu go do']
    m += sum(V[k] for k in d['V_KIM'])/1e6*RHO['brass']
    t = N_TILES*M_TILE_G/1000
    return m, t, m + t

def dalbergia_of(d, khay='cocobolo'):
    """Go Dalbergia moi hop - dung cho nguong mien tru CITES."""
    V = d['V']
    m = sum(V[k] for k in d['V_THAN'] + d['V_NAP'])/1e6*RHO['cocobolo']
    if khay == 'cocobolo':
        m += sum(V[k] for k in d['V_KHAY'])/1e6*RHO['cocobolo']
    return m

_SELF = derive()
def mass(khay='cocobolo'):        return mass_of(_SELF, khay)
def dalbergia_kg(khay='cocobolo'): return dalbergia_of(_SELF, khay)

DYN = 3.0          # he so dong
def design_load(khay='cocobolo'): return mass(khay)[2]*9.81*DYN

# Nguong mien tru cua chu giai #15. DA TRA LAI 29-08-2026 - xem tools/cites_check.py.
# Con so 10 kg dung. Nhung DIEN GIAI nguong nay tinh tren TUNG MON HANG chu khong
# cong don ca lo, nghia la 'so hop moi lo' co the khong con la rang buoc.
# Chua xac nhan duoc bang van ban goc (cites.org bi chan o moi truong nay).
CITES_LIMIT = 10.0   # kg go cua MOT loai duoc chu giai

# ============================================================== CHUAN VA DUNG SAI
# QA-01 cua Rev B tham chieu "chuan A/B/C" ma khong dinh nghia o dau (review §2.2).
# Dinh nghia o day, tren THAN HOP, vi than la chi tiet duoc gia cong truoc va moi
# thu khac lap theo no.
DATUM = [
 ("A", "MAT DAY NGOAI cua than (truoc khi dan chan dem). Chuan Z. Moi cao do"
       " trong ho so deu do tu day, KHONG do tu vanh."),
 ("B", "MAT NGOAI VACH BAN LE TRAI. Chuan X. Chon mat nay vi TRUC XOAY BAN LE"
       " NAM DUNG TREN NO (X = 0): moi sai lech cua mat nay di thang vao vi tri"
       " truc, nen no phai la chuan chu khong phai kich thuoc suy ra."),
 ("C", "MAT NGOAI VACH TRUOC (mat vach goc, KHONG phai mat go noi cua hoc am)."
       " Chuan Y. Go noi hoc am la chi tiet noi len, khong duoc lam chuan."),
]

# Dung sai. Nguyen tac: cai gi lap voi chi tiet khac thi dung sai MOT CHIEU va di
# ve phia LONG HON; cai gi chi de nhin thi dung sai doi xung.
TOL = [
 # (kich thuoc, tri so, dung sai, ly do)
 ("Khoang khay quan (X)",      "BAY",   "+0,40 / 0",   "khay 124 -0,25 -> khe 1,00..1,45 moi ben"),
 ("Khoang phu kien (X)",       "AC_BAY","+0,40 / 0",   "AC-01 68 -0,25 -> khe 1,00..1,45 moi ben"),
 ("Long hop (Y)",              "INNER_Y","+0,50 / 0",  "khay 325 -0,30 -> khe 2,50..3,00 moi dau"),
 ("Be day vach ban le",        "WALL_HINGE","+/-0,15", "quyet dinh vi tri truc xoay X=9"),
 ("Be day vach ngan",          "DIV",   "+/-0,20",     "khong lap voi gi, chi chia khoang"),
 ("Be day day hop",            "BOT",   "+/-0,20",     "vao chuoi Z"),
 ("Cao do vanh tai canh mong", "Z_RIM", "+/-0,30",     "quyet dinh khe 1,0 tren dinh khay"),
 ("Tam lo chot theo B",        None,    "+/-0,10",     "hai ben phai dong truc: sai lech lam ket ban le"),
 ("Tam lo chot theo A",        None,    "+/-0,10",     "nt"),
 ("Mortise ban le tren vanh",  None,    "+0 / -0,05",  "sau hon la nap kenh; nong hon la ho khe"),
 ("Vi tri ban le theo Y",      None,    "+/-0,30",     "ba ban le phai dong truc: lech lam ket"),
 ("Phu bi X, Y",               None,    "+/-0,50",     "KHONG dung doc lap voi nap - xem ghi chu"),
 ("Dong mep nap - than",       None,    "+/-0,30",     "dung sai QUAN HE. Nap cat theo than THUC TE"),
]
TOL_NOTE = ("Phu bi than va phu bi nap KHONG duoc dung sai hoa doc lap: truong hop xau"
            " cua hai tri +/-0,5 cho lech 1,0 mm, vien nap thut vao 0,5 mm moi ben va"
            " nhin thay ro. Canh nap phai duoc CAT THEO THAN da hoan thien (match-fit)"
            " o nguyen cong cuoi, va chi kiem theo dung sai quan he +/-0,30.")

# ------------------------------------------------------- CHUYEN DONG THEO MUA
# Khe rap giua hai canh nap con lai bao nhieu khi go hut them dmc % am.
# Dung chung boi tools/lid_solid_calc.py va tools/draw_lid.py (hinh 7).
def seam_left(dmc, kind, lw=None):
    """kind: 'nu' = mot tam Nu dac ; 'core' = loi on dinh + veneer ;
             'frame' = khung go dac + tam tha (chi 2 do ngang tho vao chuoi)."""
    lw = derive()['LW'] if lw is None else lw
    if   kind == 'nu':    grow = lw*K['Nu moi phuong']*dmc
    elif kind == 'core':  grow = lw*K['loi on dinh']*dmc
    elif kind == 'frame': grow = 2*STILE*K['cocobolo ngang tho']*dmc
    else: raise ValueError(kind)
    return SEAM - 2*grow          # hai canh cung no, moi ben an vao khe mot nua

def seam_close_dmc(kind, lw=None):
    """dMC lam khe rap giua dong hoan toan. inf neu khong bao gio dong."""
    lw = derive()['LW'] if lw is None else lw
    k = {'nu': lw*K['Nu moi phuong'], 'core': lw*K['loi on dinh'],
         'frame': 2*STILE*K['cocobolo ngang tho']}[kind]
    return math.inf if k <= 0 else SEAM/(2*k)

# ============================================================== TU KIEM
def selfcheck(d=None):
    d = d or _SELF
    e = []
    if abs(2*(d['LW'] + d['LEAF_X0']) + SEAM - d['W']) > 1e-9:
        e.append("2 canh nap + 2 lui vao + khe != phu bi X")
    if d['REBATE_H'] > 0 and d['REBATE_H'] < T_LID - 1e-9:
        e.append("ha bac vanh thap hon be day nap — mat dau canh se quet vao vach")
    # Ha bac (z T_LID duoi vanh) va hoc am (z GRIP_Z0..GRIP_Z1) chong nhau mot doan.
    # Trong doan chong, hoc am sau hon nen ha bac khong lay them gi; ngoai doan do
    # ha bac lay REBATE_D khoi be day vanh — do la duong truyen luc khi xach.
    if d['REBATE_D'] > 0 and max(d['REBATE_D'], GRIP_D) + GRIP_BACK > d['WALL_HINGE'] + 1e-9:
        e.append("ha bac hoac hoc am an thung vach ban le")
    if d['REBATE_D'] > 0 and d['WALL_HINGE'] - d['REBATE_D'] < 8.0:
        e.append("vanh con lai sau ha bac mong hon 8 mm")
    if HG_MODE == 'C' and d['PROUD'] > 1e-9:
        e.append("ha bac nong hon ban kinh ong -> ong go van nho ra ngoai")
    if abs(d['OP_W'] + 2*STILE - d['LW']) > 1e-9:  e.append("chuoi be rong canh nap khong khep")
    if abs(d['t_lid'](d['LW']) - T_SEAM) > 1e-9:   e.append("vat nap khong ve dung T_SEAM")
    if 2*d['R_KN'] > WALL_HINGE:                  e.append("ong go rong hon be day vach ban le")
    if d['KN_RUN'] > LID_L:                       e.append("chuoi mat mong dai hon canh nap")
    if d['KN_WALL_EFF'] < 2.0:                    e.append("thanh go quanh lo chot mong hon 2,0 mm")
    if N_KN % 2 == 0:                             e.append("so mat mong phai le de hai dau thuoc THAN")
    if KN_PIN_L*2 < d['KN_RUN']:                  e.append("hai chot khong phu het chuoi mat mong")
    if HG_MODE == 'B' and d['STOP_H'] <= 0:       e.append("ong go an het be day nap, mat chan 180 do bien mat")
    if TRAY[1] + 2 > d['BAY']:                     e.append("khay quan khong lot khoang")
    if d['AC_W_IN'] < 2*TILE_MAX[0]:               e.append("long AC-01 khong du 4 quan du phong 2x2")
    if d['AC_DICE_L'] < 2*TILE_MAX[0]:             e.append("o xuc xac ngan hon 2 hang o 18x18")
    if SPINE_W/2 + d['X_SEAM'] > d['W']:           e.append("song khoa vuot ra ngoai hop")
    # ranh om tam nam o mep trong do doc; cho mong nhat la mep trong do doc
    # canh khe giua, vi nap vat mong dan ve phia do.
    lip = d['LIP_BOT']
    if lip < 2.0:
        e.append(f"lip duoi ranh om tam chi con {lip:.2f} mm - tang PAN_T se lam no am")
    if S_TOP < 2.5:                                e.append("lip tren ranh om tam mong hon 2,5")
    # --- tam nang ngang mat khung: khe quanh long tam phai nuot duoc go no
    if PAN_REV < d['PAN_MOVE']:
        e.append(f"khe quanh long tam {PAN_REV:.2f} < go no {d['PAN_MOVE']:.2f} mm "
                 f"o dMC {DMC_DES:.1f} % — long tam se dap vao khung")
    if PAN_REV < d['PAN_MOVE_DRY']:
        e.append(f"khe quanh long tam {PAN_REV:.2f} < go no mot chieu "
                 f"{d['PAN_MOVE_DRY']:.2f} mm neu lap o do am xuong {DMC_DRY:.0f} %")
    if d['PAN_MOVE'] > d['PAN_FLOAT']:
        e.append(f"tam no {d['PAN_MOVE']:.2f} > khoang tha trong ranh {d['PAN_FLOAT']:.1f} mm")
    if d['PAN_REB'] > GRV:
        e.append("bac phay quanh mep tren rong hon ca ranh om tam")
    if d['PAN_TH'] + d['LIP_BOT'] > T_LID + 1e-9:
        e.append("tam nang day hon cho con lai trong be day nap")
    if (WALL_FB - BOT_TON)/2 < 2.5:                e.append("ranh om day lam vach truoc/sau qua mong")
    if d['HANDLE'] == 'C':
        if d['MAG_MAR_OUT'] < MAG_EDGE:
            e.append(f"nam cham cach mep nap {d['MAG_MAR_OUT']:.1f} < {MAG_EDGE:.1f} mm")
        if d['MAG_MAR_IN'] < MAG_EDGE:
            e.append(f"nam cham cach mat trong vach {d['MAG_MAR_IN']:.1f} < {MAG_EDGE:.1f} mm")
        if max(MAG_X) + MAG[0]/2 > d['LW'] - MAG_EDGE:
            e.append("nam cham ngoai cung vuot qua khe rap giua")
        # nam cham va khe luon ngon deu an vao vanh vach truoc/sau -> phai roi nhau
        if d['GRIP_OUT'] > 0:
            e.append(f"vach ban le {d['WALL_HINGE']:.0f} khong nuot noi hoc am sau "
                     f"{GRIP_D:.0f} + thanh sau {GRIP_BACK:.0f}")
        for xc in MAG_X:
            for wc in d['WELL_X']:
                if abs(xc - wc) < (MAG[0] + WELL_W)/2 + MAG_EDGE:
                    e.append(f"nam cham X={xc:.0f} cham khe luon ngon X={wc:.0f}")
        for i in range(len(MAG_X)-1):
            if MAG_X[i+1] - MAG_X[i] < MAG[0] + MAG_EDGE:
                e.append("hai nam cham tren cung mot canh qua sat nhau")
        if d['t_lid'](max(MAG_X)) - MAG_REC < 6.0:
            e.append("hoc nam cham lam nap mong hon 6 mm o cho mong nhat")
    if WALL_FB - WELL_D < 3.5:  e.append("da ngoai vach truoc/sau tai hoc ngon mong hon 3,5")
    if NOTCH_D > (TRAY[0]-TRAY_IN[0])/2 + 0.001:
        e.append("khoet mat dau khay sau hon be day vach khay")
    if d['SCAL_LEFT'] < 3.0:    e.append("dai go ben ranh Joker sau khi khoet hom con < 3 mm")
    if d['LIFT_CHANNEL'] < 11.0: e.append("khe luon ngon tay khi nhac khay hep hon 11 mm")
    if d['TILE_OPEN'] > TILE_MAX[2] - 2.0:
        e.append("khoet mat dau khay ho gan het be day quan - quan tuot ra duoc")
    if d['LIFT_LIP'] < 5.0:     e.append("mo nhac khay thap hon 5 mm")
    if d['HANDLE'] == 'C':
        if d['GRIP_LEDGE'] < 8.0:  e.append("dai go tren hoc am thap hon 8 mm")
        if d['GRIP_LEDGE_T'] < 8.0: e.append("dai go tren hoc am mong hon 8 mm sau khi ha bac")
        # HA BAC BAN LE AN VAO TRAN HOC — loi da tung lot luoi mot lan (Rev C1):
        # kiem cu chi bat khi REBATE_D > GRIP_D nen khong bao gio no. Nay kiem
        # tung diem mot: o MOI x tren tran hoc phai con GRIP_LIP go dac ben tren.
        if d['GRIP_LIP_MIN'] < GRIP_LIP_REQ:
            e.append(f"tran hoc am thoc len sat thu nam tren no: con {d['GRIP_LIP_MIN']:.2f} "
                     f"< {GRIP_LIP_REQ:.1f} mm go dac")
        if d['GRIP_FIT'] < FING_MAR - 1e-9:
            e.append(f"ngon tay khong lot het chieu sau hoc: khe hep nhat {d['GRIP_FIT']:.2f} mm")
        if d['GRIP_APER'] < FING_T_DIP + 2.0:
            e.append(f"khe ho vao tay {d['GRIP_APER']:.1f} hep hon ngon tay {FING_T_DIP:.0f} + 2")
        if d['GRIP_SURF'] < L_DISTAL:
            e.append("be mat tran hoc ngan hon dot ngon tay — chi bam duoc mep")
        if d['GRIP_FLAT'] < 3.0:
            e.append("bo tron mep an het doan tran phang")
        # chan DUOI cua ban kinh bo: luc luon bat dau don ve mep, da tay boc
        # duoc chung WRAP_SKIN do quanh no. Bo cang nho, dai cham cang hep.
        _P = mass_of(d, 'loi on dinh')[2]*9.81*DYN/2
        _p = _P/(N_FING*FING_W*GRIP_R*math.radians(WRAP_SKIN))
        if _p > P_COMFORT:
            e.append(f"bo mep tran qua nho: ap luc luc bat luc {_p*1000:.0f} kPa "
                     f"> {P_COMFORT*1000:.0f} (can R >= "
                     f"{_P/(N_FING*FING_W*math.radians(WRAP_SKIN)*P_COMFORT):.2f})")
        if d['GRIP_EJECT'] > MU_SKIN:
            e.append("tran hoc doc hon goc ma sat — ngon tay bi day tuot ra")
        if d['GRIP_SKIRT'] < 4.0:  e.append("dai go duoi hoc am mong hon 4 mm")
        if d['GRIP_Y0'] < WALL_FB + 10:            e.append("hoc am cham vach truoc/sau")
    return e

if __name__ == '__main__':
    for h in ('A', 'C'):
        d = derive(handle=h)
        V = d['V']
        print("="*76)
        print(f"PHUONG AN {h} — phu bi {d['X_OA']:.1f} x {d['Y_OA']:.0f} x {d['Z_OA']:.0f}"
              f"   ({'song khoa + quai da, mot tay' if h=='A' else 'hoc am hai dau, hai tay'})")
        print("="*76)
        print(f"  Chuoi X : {d['WALL_HINGE']:.0f} + {d['BAY']:.0f} + {d['DIV']:.0f} + "
              f"{d['AC_BAY']:.0f} + {d['DIV']:.0f} + {d['BAY']:.0f} + {d['WALL_HINGE']:.0f}"
              f" = {d['W']:.0f}"
              + (f"  (+2 x {d['PROUD']:.1f} ong go nho ra = {d['X_OA']:.1f})"
                 if d['PROUD'] > 0 else "  (ong go khong nho ra)"))
        print(f"  Ban le : mong go, truc ({d['PIN_X']:.1f} , {d['PIN_Z']:.1f}) "
              f"mode {HG_MODE} ; ong O{2*d['R_KN']:.1f} ; {N_KN} mat mong x {KN_LEN:.0f}"
              f" ; chot go O{KN_PIN:.0f}")
        print(f"  Chuoi Y : {WALL_FB:.0f} + {INNER_Y:.0f} + {WALL_FB:.0f} = {d['Y_BODY']:.0f}"
              f"  (+2 x {d['NHO_RA']:.0f} nho ra = {d['Y_OA']:.0f})")
        print(f"  Chuoi Z : chan {FOOT:.0f} + day {BOT:.0f} + {N_STACK} x khay {TRAY_H:.0f}"
              f" + khe {CLR_Z:.0f} = vanh Z{d['Z_RIM']:.0f} ; nap {T_HINGE:.0f} -> "
              f"Z{d['Z_LID']:.0f} ; noi {d['Z_PROUD']:.0f} -> Z{d['Z_OA']:.0f}")
        print(f"  Canh nap: {d['LW']:.2f} x {LID_L:.0f}, vat {T_HINGE:.0f} -> {T_SEAM:.0f}"
              f" tren {d['TAPER']:.2f} = {d['ANG']:.3f} do")
        print(f"  AC-01   : {d['AC_L']:.0f} x {d['AC_W_OUT']:.0f} x {AC_H:.0f} trong khoang {d['AC_Y']:.0f}, long rong "
              f"{d['AC_W_IN']:.0f} ; chuoi dai {AC_WALL:.0f}+{AC_JOKER[1]:.0f}+{AC_WALL:.0f}+"
              f"{d['AC_DICE_L']:.0f}+{AC_WALL:.0f}+{AC_AUX_L:.0f}+{AC_WALL:.0f}")
        print()
        print(f"  {'chi tiet':20s}{'cm3':>9s}{'kg':>7s}   vat lieu")
        for k, val in V.items():
            m = MAT.get(k, 'cocobolo')
            print(f"  {k:20s}{val/1000:9.0f}{val/1e6*RHO[m]:7.2f}   {m}")
        print()
        for khay in ('cocobolo', 'loi on dinh'):
            go, t, tot = mass_of(d, khay)
            dal = dalbergia_of(d, khay)
            print(f"  Khay {khay:12s}: go {go:5.2f} + quan {t:.2f} = {tot:5.2f} kg"
                  f"   | tai TK {tot*9.81*DYN:3.0f} N"
                  f"   | Dalbergia {dal:.2f} kg/hop -> {int(CITES_LIMIT//dal)} hop/lo")
        err = selfcheck(d)
        print("\n  TU KIEM: " + ("DAT" if not err else "LOI"))
        for x in err:
            print(f"    LOI: {x}")
        print()
    raise SystemExit(1 if selfcheck() else 0)
