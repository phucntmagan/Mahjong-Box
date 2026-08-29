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
}
# he so gian no tuyen tinh, phan tram tren moi 1 % thay doi do am
K = {'doc tho': 0.0001, 'cocobolo ngang tho': 0.0016,
     'go do ngang tho': 0.0015, 'Nu moi phuong': 0.0022, 'loi on dinh': 0.0005}

# tri so co ly cocobolo dung cho kiem ben (MPa)
MOR, E_W, C_PERP, SHEAR = 110.0, 13000.0, 14.0, 13.0

M_TILE_G, N_TILES = 16.0, 152
TILE_MAX = (25.7, 36.8, 11.4)     # quan lon nhat theo Rev B

# ============================================================== CHUOI KICH THUOC
# --- X (be rong) : vach | khay | ngan | phu kien | ngan | khay | vach
# Vach ban le PHAI la 18: tools/hinge_kinematics.py chung minh ong go ban kinh 9
# quanh lo O6,2 khong nam duoc trong vach 10. Day khong phai tuy chon.
WALL_HINGE = 18.0        # vach trai/phai - mang mat mong ban le
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
GRIP_W, GRIP_H, GRIP_D = 120.0, 30.0, 16.0   # (C) hoc am: rong x cao x sau
GRIP_BACK  =   6.0       # (C) go con lai phia sau hoc
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
T_HINGE = 18.0           # day nap tai canh mong
T_SEAM  = 12.0           # day nap tai khe rap giua
SPINE_T, SPINE_INSET = 20.0, 4.0   # (A) song khoa day 20, am 4 vao nap

# --- nap
SEAM    = 1.5            # khe rap giua (0,6 -> 1,5 vi gian no khung go dac)
STILE   = 34.0           # be rong do doc (ca hai canh)
RAIL    = 30.0           # be rong do ngang
PAN_T   =  8.0           # day tam Nu (10 -> 8)
GRV     =  9.0           # ranh om tam: sau 9
TON     =  6.0           # canh tam an vao ranh 6 -> tam THA 3 mm moi phia
GRV_W   = PAN_T          # ranh rong dung bang day tam: tam KHONG bi phay bac.
                         # Nu tho xoan loan, mot bac 1,5 mm tren canh tam la cho nut.
S_TOP   =  3.0           # lip khung phia TREN ranh - do la be mat nhin thay
LID_L   = 350.0          # chieu dai canh nap (theo Y, khong ke tru/hoc am)

# --- ban le
R_KN    = T_HINGE/2      # ban kinh ong go = 9
D_PIN   = 6.2            # lo chot
N_KN, KN_LEN, KN_PITCH = 7, 44.0, 45.0    # 7 mat mong, dai 44, buoc 45
KN_BODY, KN_LID = 4, 3   # 4 mat thuoc THAN, 3 thuoc NAP

# --- song khoa + quai (phuong an A)
SPINE_W = 44.0
SPINE_REC = (144.0, 32.0, 10.0)   # hoc chua quai tren song

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
WELL_W   = 70.0          # be rong hoc ngon tren vach truoc/sau, do tu trong ra
WELL_D   =  6.0          # sau vao vach (vach 10 -> con 4 mm da ngoai)
NOTCH_D  =  5.0          # khoet XUYEN mat dau khay (day vach khay 5)
NOTCH_H  = 12.0          # cao khoet, tinh tu vanh khay xuong
WELL_FELT=  1.0          # ni dan vao day hoc: chan quan truot ra va lam dem

# --- hom ngon ranh Joker
SCAL_D   = 25.0          # duong kinh hom ban nguyet
SCAL_DEP = 12.0          # sau khoet vao dai go ben ranh

# --- o xuc xac + nap che
DICE_SOCK  = 18.0        # canh o vuong
DICE_SOCK_D= 12.0        # sau o
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
        # hoc sau GRIP_D can GRIP_D + GRIP_BACK be day vach; vach chi co WALL_FB
        grip_out = GRIP_D + GRIP_BACK - WALL_FB          # phan phai day ra ngoai
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

    LW     = (W - SEAM)/2                                # be rong mot canh nap
    TAPER  = LW - 2*R_KN                                 # doan vat thuc (tu X=18 ra mep)
    SLOPE  = (T_HINGE - T_SEAM)/TAPER
    ANG    = math.degrees(math.atan(SLOPE))
    OP_W   = LW - 2*STILE                                # long khung theo X
    OP_L   = LID_L - 2*RAIL                              # long khung theo Y
    PAN_W, PAN_L = OP_W + 2*TON, OP_L + 2*TON            # tam Nu
    X_SEAM = W/2                                         # tam khe rap giua
    KN_RUN = N_KN*KN_LEN + (N_KN-1)*(KN_PITCH-KN_LEN)    # chieu dai chuoi mong
    A_KN   = math.pi*(R_KN**2 - (D_PIN/2)**2)            # tiet dien ong go tru lo chot

    def z_rim_at(x):
        """Cao do vanh than tai toa do x - vanh doc theo dung goc vat cua nap."""
        return Z_RIM + (Z_SEAM - Z_RIM)*min(x, W-x)/X_SEAM
    def t_lid(x):
        """Day nap tai x tinh tu mat ngoai vach (x=18 la mep trong cua ong go)."""
        return T_HINGE - SLOPE*max(0.0, x - 2*R_KN)
    def _int_t(a, b):
        """Tich phan day nap tu x=a den x=b (a,b >= 18)."""
        return T_HINGE*(b-a) - SLOPE*((b-2*R_KN)**2 - (a-2*R_KN)**2)/2

    # --- lip cua ranh om tam Nu: khung vat nen cho mong nhat la mep trong
    #     cua do doc canh khe giua (x = LW - STILE)
    LIP_BOT = t_lid(LW - STILE) - S_TOP - PAN_T

    # --- hoc am (phuong an C): dat day hoc ngang san trong, dinh cach vanh mot dai go
    GRIP_X0   = X_SEAM - GRIP_W/2
    GRIP_X1   = X_SEAM + GRIP_W/2
    GRIP_Z0   = Z_FLOOR                                  # day hoc ngang san trong
    GRIP_Z1   = GRIP_Z0 + GRIP_H
    WALL_GRIP = WALL_FB + grip_out                       # be day vach tai hoc
    GRIP_LEDGE = min(z_rim_at(GRIP_X0), z_rim_at(GRIP_X1)) - GRIP_Z1  # dai go tren hoc am
    GRIP_SKIRT = GRIP_Z0 - FOOT                                       # dai go duoi hoc am

    # --- khay phu kien: chuoi dai khep ve AC_Y
    AC_W_OUT  = ac_bay - 2.0                             # khe 1,0 moi ben
    AC_W_IN   = AC_W_OUT - 2*AC_WALL
    AC_DICE_L = AC_L - 4*AC_WALL - AC_JOKER[1] - AC_AUX_L

    # --- hoc nhac khay: khe luon ngon tay va mo moc len
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
    v['vach trai/phai'] = 2*(INNER_Y*wall_hinge*(Z_RIM - Z_FLOOR))
    v['mat mong than']  = 2*KN_BODY*KN_LEN*A_KN
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
    st_h   = LID_L*_int_t(2*R_KN, STILE)
    st_s   = LID_L*_int_t(LW-STILE, LW)
    if handle == 'A':
        st_s -= (SPINE_W/2 - SEAM/2)*LID_L*SPINE_INSET   # ranh am cho song khoa
    rails  = 2*RAIL*_int_t(STILE, LW-STILE)
    groove = (2*OP_W + 2*OP_L)*GRV*GRV_W
    v['khung nap']      = 2*(st_h + st_s + rails - groove)
    v['mat mong nap']   = 2*KN_LID*KN_LEN*A_KN
    v['tam Nu']         = 2*(PAN_W*PAN_L*PAN_T)

    if handle == 'A':
        v['tru quai']   = 2*(POST_W*(POST_OUT+POST_IN)*(Z_SEAM - Z_FLOOR))
        v['song khoa']  = (Y_OA*SPINE_W*SPINE_T
                           - SPINE_REC[0]*SPINE_REC[1]*SPINE_REC[2])
        V_THAN = ['day','vach truoc/sau','tru quai','vach trai/phai',
                  'mat mong than','vach ngan']
        V_NAP  = ['khung nap','mat mong nap','song khoa']
    else:
        # go them cua go noi tru di the tich hoc khoet vao
        v['go hoc am']  = 2*(GRIP_W*grip_out*(z_rim_at(X_SEAM) - FOOT)
                             - GRIP_W*GRIP_H*GRIP_D)
        v['nap che o xuc xac'] = (AC_W_IN + 2*COVER_LIP)*(2*DICE_SOCK + 3*DICE_RIB)*COVER_T
        V_THAN = ['day','vach truoc/sau','go hoc am','vach trai/phai',
                  'mat mong than','vach ngan']
        V_NAP  = ['khung nap','mat mong nap']
    V_KHAY = ['khay quan','khay phu kien'] + (['nap che o xuc xac'] if handle=='C' else [])

    d.update({k: val for k, val in locals().items()
              if k.isupper() or k in ('t_lid', '_int_t', 'z_rim_at')})
    d.update(dict(WALL_HINGE=wall_hinge, BAY=bay, DIV=div, AC_BAY=ac_bay,
                  HANDLE=handle, V=v, V_THAN=V_THAN, V_KHAY=V_KHAY, V_NAP=V_NAP))
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

# ============================================================== TU KIEM
def selfcheck(d=None):
    d = d or _SELF
    e = []
    if abs(2*d['LW'] + SEAM - d['W']) > 1e-9:      e.append("2 canh nap + khe != phu bi X")
    if abs(d['OP_W'] + 2*STILE - d['LW']) > 1e-9:  e.append("chuoi be rong canh nap khong khep")
    if abs(d['t_lid'](d['LW']) - T_SEAM) > 1e-9:   e.append("vat nap khong ve dung T_SEAM")
    if abs(d['t_lid'](2*R_KN) - T_HINGE) > 1e-9:   e.append("vat nap khong bat dau tu T_HINGE")
    if d['KN_RUN'] > INNER_Y:                      e.append("chuoi mat mong dai hon long hop")
    if TRAY[1] + 2 > d['BAY']:                     e.append("khay quan khong lot khoang")
    if d['AC_W_IN'] < 2*TILE_MAX[0]:               e.append("long AC-01 khong du 4 quan du phong 2x2")
    if d['AC_DICE_L'] < 2*TILE_MAX[0]:             e.append("o xuc xac ngan hon 2 hang o 18x18")
    if SPINE_W/2 + d['X_SEAM'] > d['W']:           e.append("song khoa vuot ra ngoai hop")
    if R_KN > d['WALL_HINGE']/2:                   e.append("ong go khong nam trong vach ban le")
    # ranh om tam nam o mep trong do doc; cho mong nhat la mep trong do doc
    # canh khe giua, vi nap vat mong dan ve phia do.
    lip = d['LIP_BOT']
    if lip < 2.0:
        e.append(f"lip duoi ranh om tam chi con {lip:.2f} mm - tang PAN_T se lam no am")
    if S_TOP < 2.5:                                e.append("lip tren ranh om tam mong hon 2,5")
    if (WALL_FB - BOT_TON)/2 < 2.5:                e.append("ranh om day lam vach truoc/sau qua mong")
    if WALL_FB - WELL_D < 3.5:  e.append("da ngoai vach truoc/sau tai hoc ngon mong hon 3,5")
    if NOTCH_D > (TRAY[0]-TRAY_IN[0])/2 + 0.001:
        e.append("khoet mat dau khay sau hon be day vach khay")
    if d['SCAL_LEFT'] < 3.0:    e.append("dai go ben ranh Joker sau khi khoet hom con < 3 mm")
    if d['LIFT_CHANNEL'] < 11.0: e.append("khe luon ngon tay khi nhac khay hep hon 11 mm")
    if d['TILE_OPEN'] > TILE_MAX[2] - 2.0:
        e.append("khoet mat dau khay ho gan het be day quan - quan tuot ra duoc")
    if d['LIFT_LIP'] < 5.0:     e.append("mo nhac khay thap hon 5 mm")
    if d['HANDLE'] == 'C':
        if d['GRIP_LEDGE'] < 8.0:  e.append("dai go tren hoc am mong hon 8 mm")
        if d['GRIP_SKIRT'] < 4.0:  e.append("dai go duoi hoc am mong hon 4 mm")
        if d['GRIP_X0'] < d['WALL_HINGE']:         e.append("hoc am cham vach ban le")
    return e

if __name__ == '__main__':
    for h in ('A', 'C'):
        d = derive(handle=h)
        V = d['V']
        print("="*76)
        print(f"PHUONG AN {h} — phu bi {d['W']:.0f} x {d['Y_OA']:.0f} x {d['Z_OA']:.0f}"
              f"   ({'song khoa + quai da, mot tay' if h=='A' else 'hoc am hai dau, hai tay'})")
        print("="*76)
        print(f"  Chuoi X : {d['WALL_HINGE']:.0f} + {d['BAY']:.0f} + {d['DIV']:.0f} + "
              f"{d['AC_BAY']:.0f} + {d['DIV']:.0f} + {d['BAY']:.0f} + {d['WALL_HINGE']:.0f}"
              f" = {d['W']:.0f}")
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
