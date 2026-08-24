#!/usr/bin/env python3
"""
Dac ta VAT LIEU va HINH HOC da chot cua hop Mahjong 152 quan.
Nguon su that duy nhat cho khoi luong va tai thiet ke - moi script khac import tu day.

CHOT (24-08-2026):
  Than hop, khay, khung nap, song khoa, chot xoay : COCOBOLO (Dalbergia retusa)
  Tam nap                                          : NU GO DO (Afzelia xylocarpa, burl)
  Quai                                             : DA BO BRIDLE
  Nap = khung go dac om tam Nu THA trong ranh (khong phai tam lien, khong boc da)
"""
import math

# ------------------------------------------------------------------ vat lieu
RHO = {                       # g/cm3
    'cocobolo'     : 1.10,
    'Nu go do'     : 0.90,
    'go do dac'    : 0.82,
    'loi on dinh'  : 0.58,
}
# he so gian no tuyen tinh, phan tram tren moi 1 % thay doi do am
K = {'doc tho': 0.0001, 'cocobolo ngang tho': 0.0016,
     'go do ngang tho': 0.0015, 'Nu moi phuong': 0.0022, 'loi on dinh': 0.0005}

M_TILE_G, N_TILES = 16.0, 152

# ------------------------------------------------------------------ hinh hoc
LW, LL = 176.7, 350.0                    # canh nap
ST_H, ST_S, RAIL = 34.0, 34.0, 30.0      # do doc canh mong / canh khe giua / do ngang
OP_W, OP_L = LW-ST_H-ST_S, LL-2*RAIL     # long khung
GRV, TON, PAN_T = 9.0, 6.0, 10.0         # ranh 9, mong 6 -> tha 3 ; tam day 10
PAN_W, PAN_L = OP_W+2*TON, OP_L+2*TON

SPINE = (362.0, 44.0, 20.0)              # song khoa
SPINE_REC = (144.0, 32.0, 10.0)          # hoc chua quai tren song

V = {   # mm3
    'day'            : 354*350*8,
    'vach truoc/sau' : 2*(354*10*44),
    'vach trai/phai' : 2*(330*10*39),
    'vach ngan'      : 2*(330*6*44),
    'khay quan'      : 4*(325*124*19 - 315*114*15),
    'khay phu kien'  : 325*68*38 - (28*152*24.5 + 58*75*18.5 + 58*78*18.5),
    'khung nap'      : 2*((LW*LL - OP_W*OP_L)*15),
    'tam Nu'         : 2*(PAN_W*PAN_L*PAN_T),
    'song khoa'      : SPINE[0]*SPINE[1]*SPINE[2] - SPINE_REC[0]*SPINE_REC[1]*SPINE_REC[2],
}
V_THAN  = ['day','vach truoc/sau','vach trai/phai','vach ngan']
V_KHAY  = ['khay quan','khay phu kien']

def mass(khay='cocobolo'):
    """Khoi luong (kg): (go, quan, tong). khay = 'cocobolo' hoac 'loi on dinh'."""
    m  = sum(V[k] for k in V_THAN)/1e6*RHO['cocobolo']
    m += sum(V[k] for k in V_KHAY)/1e6*RHO[khay]
    m += V['khung nap']/1e6*RHO['cocobolo']
    m += V['song khoa']/1e6*RHO['cocobolo']
    m += V['tam Nu']/1e6*RHO['Nu go do']
    t = N_TILES*M_TILE_G/1000
    return m, t, m+t

def dalbergia_kg(khay='cocobolo'):
    """Khoi luong go Dalbergia moi hop - dung cho nguong mien tru CITES."""
    m = sum(V[k] for k in V_THAN)/1e6*RHO['cocobolo']
    m += V['khung nap']/1e6*RHO['cocobolo'] + V['song khoa']/1e6*RHO['cocobolo']
    if khay == 'cocobolo':
        m += sum(V[k] for k in V_KHAY)/1e6*RHO['cocobolo']
    return m

DYN = 3.0          # he so dong
def design_load(khay='cocobolo'):
    return mass(khay)[2]*9.81*DYN

if __name__ == '__main__':
    print("="*72); print("DAC TA DA CHOT — khung va than COCOBOLO, tam nap NU GO DO"); print("="*72)
    print(f"  {'chi tiet':18s}{'cm3':>9s}   vat lieu")
    mat = {'tam Nu':'Nu go do'}
    for k,v in V.items():
        print(f"  {k:18s}{v/1000:9.0f}   {mat.get(k,'cocobolo')}")
    print()
    for khay in ('cocobolo','loi on dinh'):
        go,t,tot = mass(khay)
        print(f"  Khay {khay:12s}: go {go:5.2f} + quan {t:.2f} = {tot:5.2f} kg"
              f"   | tai thiet ke {design_load(khay):.0f} N"
              f"   | Dalbergia {dalbergia_kg(khay):.2f} kg/hop")
