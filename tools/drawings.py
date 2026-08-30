#!/usr/bin/env python3
"""
BO BAN VE SAN XUAT — kho A3 ngang, 7 to.
Chay: python3 tools/drawings.py   roi   ./tools/build_drawings.sh

Moi tri so lay tu tools/box_spec.py. Khong go cung so nao.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drawlib import T, esc
from sheetlib import (V, MM, PW, PH, FR, TB_W, TB_H, INK, DIM, ACC, GRN, RED,
                      THIN, MED, THICK, dim_h, dim_v, lead, balloon, viewbox,
                      table, sheet)
import box_spec as B

S   = B.derive()
W, YB, XS = S['W'], S['Y_BODY'], S['X_SEAM']
WH, FB    = S['WALL_HINGE'], B.WALL_FB
BAY, DIV, ACB = S['BAY'], S['DIV'], S['AC_BAY']
Z_FL, Z_RIM, Z_LID = S['Z_FLOOR'], S['Z_RIM'], S['Z_LID']
RK, KH, PXX = S['R_KN'], S['KN_HOLE'], S['PIN_X']
LW, GD, GW = S['LW'], B.GRIP_D, B.GRIP_W
GY0, GY1 = S['GRIP_Y0'], S['GRIP_Y1']
MASS_O = B.mass_of(S, 'loi on dinh')[2]
MASS_C = B.mass_of(S, 'cocobolo')[2]
X_BAY = [(WH, WH+BAY), (W-WH-BAY, W-WH)]
X_DIV = [(WH+BAY, WH+BAY+DIV), (W-WH-BAY-DIV, W-WH-BAY)]
X_AC  = (WH+BAY+DIV, WH+BAY+DIV+ACB)
KN = [(S['KN_Y0'] + i*S['KN_PITCH'], i % 2 == 0) for i in range(B.N_KN)]
HID = '#8a857c'            # net khuat
CEN = '#3a5f8a'            # duong tam
N_SH = 8
SHEETS = []

def hidden(v, pts):  return v.path(pts, HID, THIN, '7,4')
def centre(v, pts):  return v.path(pts, CEN, THIN, '11,3,2,3')

# ==========================================================================
# TO 00 — DANH MUC + BANG KE PHOI
# ==========================================================================
def sheet00():
    o = []
    x0, y0 = FR[0] + 30, FR[1] + 70
    o.append(T(x0, y0 - 26, 'BỘ BẢN VẼ SẢN XUẤT', font_size=22, font_weight='bold', fill=INK))
    o.append(T(x0, y0 - 4, f'Phủ bì {S["X_OA"]:.1f} × {S["Y_OA"]:.0f} × {S["Z_OA"]:.0f} mm · '
               f'{MASS_O:.2f} kg (khay lõi ổn định) / {MASS_C:.2f} kg (khay cocobolo) · '
               f'152 quân {B.TILE_MAX[0]:.1f} × {B.TILE_MAX[1]:.1f} × {B.TILE_MAX[2]:.1f}',
               font_size=11, fill=DIM))
    rows = [['00', 'Danh mục · bảng kê phôi · quy ước chung', '—'],
            ['BX-01', 'Thân hộp — mặt bằng, mặt cắt A-A, B-B', '1:2'],
            ['BX-02', 'Vách bản lề — hốc âm, mắt mộng, toạ độ trần', '4:1 / 1:2'],
            ['HD-01', 'Cánh nắp — khung + tấm Nu nâng', '1:2 / 4:1'],
            ['TR-01', 'Khay quân (4 chiếc)', '1:2 / 2:1'],
            ['AC-01', 'Khay phụ kiện', '1:2 / 2:1'],
            ['AC-02', 'Ổ xúc xắc và nắp che — ba cao độ', '2:1 / 1:1 / 3:1'],
            ['QA-01', 'Dung sai, kiểm, đặc tính bắt buộc', '—']]
    t, yy = table(x0, y0 + 14, ['TỜ', 'NỘI DUNG', 'TỈ LỆ'], rows, 700, rh=21, fs=11,
                  colw=[90, 500, 110])
    o.append(t)

    o.append(T(x0, yy + 42, 'BẢNG KÊ PHÔI — kích thước HOÀN THIỆN',
               font_size=13, font_weight='bold', fill=INK))
    o.append(T(x0, yy + 58, 'Phôi xẻ phải dư 4 mm mỗi chiều dài/rộng và 2 mm bề dày; '
               'hong tối thiểu 4 tuần, đưa về 11 % MC trước khi gia công tinh.',
               font_size=10, fill=DIM))
    P = []
    P.append(['Đáy hộp', '1', f'{S["BOT_L"]:.0f} × {S["BOT_W"]:.0f} × {B.BOT:.0f}',
              'cocobolo', f'thả trong rãnh, mộng {B.BOT_TON:.0f}'])
    P.append(['Vách bản lề', '2', f'{YB:.0f} × {Z_RIM - B.FOOT:.0f} × {WH:.0f}',
              'cocobolo', 'thẳng thớ; mang mắt mộng + hốc âm'])
    P.append(['Vách trước/sau', '2',
              f'{W - 2*WH + 2*B.JOINT_D:.0f} × {Z_RIM - B.FOOT:.0f} × {FB:.0f}',
              'cocobolo', f'kể cả mộng ngậm {B.JOINT_D:.0f} hai đầu'])
    P.append(['Vách ngăn', '2', f'{B.INNER_Y + 2*B.DIV_TON:.0f} × {Z_RIM - Z_FL:.0f} × {DIV:.0f}',
              'cocobolo', f'kể cả mộng ngậm {B.DIV_TON:.0f} hai đầu'])
    P.append(['Đố dọc cánh nắp', '4', f'{B.LID_L:.0f} × {B.STILE:.0f} × {B.T_LID:.0f}',
              'cocobolo', 'XẺ XUYÊN TÂM, góc vòng năm ≥ 60° (P7); 2 chiếc mang mắt mộng'])
    P.append(['Đố ngang cánh nắp', '4', f'{S["OP_W"] + 2*B.TON:.1f} × {B.RAIL:.0f} × {B.T_LID:.0f}',
              'cocobolo', 'kể cả mộng hai đầu'])
    P.append(['Tấm Nu (tấm nâng)', '2', f'{S["PAN_L"]:.0f} × {S["PAN_W"]:.1f} × {S["PAN_TH"]:.0f}',
              'Nu gõ đỏ', f'bậc {B.S_TOP:.0f} × {S["PAN_REB"]:.0f} quanh mép trên'])
    _tw = (B.TRAY[0]-B.TRAY_IN[0])/2
    P.append(['Vách dài khay quân', '8', f'{B.TRAY[0]:.0f} × {B.TRAY_H:.0f} × {_tw:.0f}',
              'cocobolo', '4 khay × 2; xem TR-01'])
    P.append(['Vách đầu khay quân', '8', f'{B.TRAY[1]-2*_tw:.0f} × {B.TRAY_H:.0f} × {_tw:.0f}',
              'cocobolo', '4 khay × 2'])
    P.append(['Đáy khay quân', '4',
              f'{B.TRAY[0]:.0f} × {B.TRAY[1]:.0f} × {B.TRAY_H-B.TRAY_IN[2]:.0f}',
              'cocobolo', 'hoặc lõi ổn định + veneer'])
    P.append(['Khay phụ kiện AC-01', '1', f'{S["AC_L"]:.0f} × {S["AC_W_OUT"]:.0f} × {B.AC_H:.0f}',
              'cocobolo', 'khối đặc, phay lòng'])
    P.append(['Nắp che ổ xúc xắc', '1',
              f'{S["COVER_L"]:.1f} × {S["COVER_W"]:.1f} × {B.COVER_T:.0f}',
              'cocobolo', f'nắp thả; thớ theo cạnh {S["COVER_L"]:.1f}; xem AC-02'])
    P.append(['Chốt bản lề', '4', f'Ø{B.KN_PIN:.2f} −0,05 × {B.KN_PIN_L:.0f}',
              'cocobolo', 'thẳng thớ, không mắt'])
    P.append(['Chốt draw-bore góc thân', f'{4*B.JOINT_NP}', f'Ø{B.JOINT_PIN:.0f} × {WH:.0f}',
              'cocobolo', 'lệch tâm 0,4 mm'])
    P.append(['Nam châm khối', f'{2*S["MAG_N_LEAF"]}',
              f'{B.MAG[0]:.0f} × {B.MAG[1]:.0f} × {B.MAG[2]:.0f}',
              f'NdFeB {B.MAG_GRADE}', 'phân cực theo bề dày'])
    t2, yy2 = table(x0, yy + 70, ['CHI TIẾT', 'SL', 'KÍCH THƯỚC HOÀN THIỆN (mm)', 'VẬT LIỆU', 'GHI CHÚ'],
                    P, 1000, rh=19, fs=10, colw=[210, 55, 260, 150, 325])
    o.append(t2)

    bx = x0 + 1040
    o.append(T(bx, y0 + 14, 'QUY ƯỚC CHUNG', font_size=13, font_weight='bold', fill=INK))
    gen = [f'Đơn vị mm. Góc chiếu thứ nhất.',
           f'Dung sai chung ±0,3 nếu không ghi khác.',
           f'Mọi cao độ Z đo từ MẶT ĐÁY NGOÀI (chuẩn A),',
           f'không đo từ vành.',
           f'Chuẩn X = mặt ngoài vách bản lề trái (B).',
           f'Chuẩn Y = mặt ngoài vách trước (C).',
           f'Cạnh lộ ra bo R0,5 nếu không ghi khác.',
           f'Keo: epoxy 2 thành phần cho mọi mối mộng',
           f'cocobolo; lau acetone và ép trong 15 phút',
           f'kể từ khi phay xong má mộng.',
           f'KHÔNG một chi tiết kim loại nào trong bản lề.',
           f'Nam châm chỉ dùng cho khoá nắp.']
    for i, g in enumerate(gen):
        o.append(T(bx, y0 + 38 + i*17, g, font_size=10.5, fill=INK))
    o.append(T(bx, y0 + 38 + len(gen)*17 + 22, 'NGUỒN SỐ', font_size=13,
               font_weight='bold', fill=INK))
    src = ['tools/box_spec.py — nguồn sự thật duy nhất',
           'tools/grip_hook.py — trần hốc âm',
           'tools/hinge_kinematics.py — bản lề',
           'tools/lid_solid_calc.py — nắp, tấm nâng',
           'tools/lid_latch.py — khoá nam châm',
           'tools/drawings.py — chính bộ bản vẽ này',
           '',
           'Mọi trị số trên các tờ sau đều do script sinh.',
           'Sửa số bằng tay là sai quy trình.']
    for i, g in enumerate(src):
        o.append(T(bx, y0 + 38 + len(gen)*17 + 44 + i*17, g, font_size=10.5,
                   fill=DIM if i > 5 else INK))
    return sheet('00', 'DANH MỤC · BẢNG KÊ PHÔI', '—', 'cocobolo / Nu gõ đỏ',
                 f'{MASS_O:.2f} kg', 1, N_SH, ''.join(o))
SHEETS.append(('00-danh-muc', sheet00))

# ==========================================================================
# TO BX-01 — THAN HOP
# ==========================================================================
def sheetBX01():
    o = []
    SC = MM/2                          # 1:2
    # ---------------- MAT BANG (cot trai, tren)
    v = V(120, 770, SC)
    o.append(viewbox(46, 74, 806, 706, 'MẶT BẰNG — nhìn từ trên, tháo nắp',
                     'nét khuất: rãnh ôm đáy · hốc âm · rãnh ngậm góc', 'TL 1:2'))
    o.append(v.rect(0, W, 0, YB, '#fbfaf8', INK, THICK))
    for x0, x1 in [(0, WH), (W-WH, W)]:
        o.append(v.rect(x0, x1, 0, YB, 'none', INK, MED))
    o.append(v.rect(WH, W-WH, 0, FB, 'none', INK, MED))
    o.append(v.rect(WH, W-WH, YB-FB, YB, 'none', INK, MED))
    for x0, x1 in X_DIV:
        o.append(v.rect(x0, x1, FB, YB-FB, '#efe9df', INK, MED))
    for x0, x1 in [(WH-B.JOINT_D, WH), (W-WH, W-WH+B.JOINT_D)]:
        for y0, y1 in [(0, FB), (YB-FB, YB)]:
            o.append(hidden(v, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]))
    g = B.BOT_GRV
    o.append(hidden(v, [(WH-g, FB-g), (W-WH+g, FB-g), (W-WH+g, YB-FB+g),
                        (WH-g, YB-FB+g), (WH-g, FB-g)]))
    for x0, x1 in [(0, GD), (W-GD, W)]:
        o.append(hidden(v, [(x0, GY0), (x1, GY0), (x1, GY1), (x0, GY1), (x0, GY0)]))
    for xk in (PXX, W - PXX):
        for y0, is_body in KN:
            o.append(v.rect(xk-RK, xk+RK, y0, y0+B.KN_LEN,
                            '#e6d9c4' if is_body else '#ffffff', INK, MED))
        o.append(centre(v, [(xk, -16), (xk, YB+16)]))
        o.append(hidden(v, [(xk-KH/2, 0), (xk-KH/2, YB)]))
        o.append(hidden(v, [(xk+KH/2, 0), (xk+KH/2, YB)]))
    for xc in S['WELL_X']:
        for y0, y1 in [(0, B.WELL_D), (YB-B.WELL_D, YB)]:
            o.append(v.rect(xc-B.WELL_W/2, xc+B.WELL_W/2, y0, y1, '#f7e9e6', ACC, MED))
    for xc in list(B.MAG_X) + [W-x for x in B.MAG_X]:
        for yc in (B.MAG_Y, YB-B.MAG_Y):
            o.append(v.rect(xc-B.MAG[0]/2, xc+B.MAG[0]/2, yc-B.MAG[1]/2, yc+B.MAG[1]/2,
                            '#cfd8e2', '#3a5f8a', MED))
    o.append(centre(v, [(XS, -16), (XS, YB+16)]))
    o.append(T(v.X(XS)+5, v.Z(YB)+14, 'khe ráp giữa', font_size=9, fill=CEN))
    # kich thuoc doc (ben trai)
    o.append(dim_v(v, GY0, GY1, 0, f'{GW:.0f} hốc âm', off=-28))
    o.append(dim_v(v, S['KN_Y0'], S['KN_Y0']+S['KN_RUN'], 0,
                   f'{S["KN_RUN"]:.0f} chuỗi mắt mộng', off=-52))
    o.append(dim_v(v, 0, YB, 0, f'{YB:.0f}', off=-78))
    o.append(dim_h(v, S['WELL_X'][0]-B.WELL_W/2, S['WELL_X'][0]+B.WELL_W/2, YB,
                   f'{B.WELL_W:.0f}', off=-24))
    for n, (px, py), (tx, ty) in [
            (1, v.P((PXX, KN[0][0]+B.KN_LEN/2)), (206, 640)),
            (2, v.P((GD/2, GY0+24)), (212, 500)),
            (3, v.P((S['WELL_X'][1], B.WELL_D/2)), (526, 700)),
            (4, v.P((B.MAG_X[1], YB-B.MAG_Y)), (456, 178)),
            (5, v.P((X_DIV[0][0]+DIV/2, 250)), (362, 268)),
            (6, v.P((WH-B.JOINT_D/2, FB/2)), (206, 722))]:
        o.append(balloon(px, py, tx, ty, n))
    # ---------------- MAT CAT A-A (thang hang duoi mat bang)
    va = V(120, 930, SC)
    o.append(viewbox(46, 786, 806, 246, 'MẶT CẮT A-A — cắt ngang giữa hộp',
                     '', 'TL 1:2'))
    o.append(va.rect(0, W, 0, B.FOOT, '#efe9df', INK, MED))
    o.append(va.rect(WH-B.BOT_TON, W-WH+B.BOT_TON, B.FOOT, Z_FL, '#efe9df', INK, MED))
    for x0, x1 in [(0, WH), (W-WH, W)]:
        o.append(va.rect(x0, x1, B.FOOT, Z_RIM, '#e6d9c4', INK, MED))
    for x0, x1 in X_DIV:
        o.append(va.rect(x0, x1, Z_FL, Z_RIM, '#e6d9c4', INK, MED))
    for a0, a1 in X_BAY:
        for k in (0, 1):
            o.append(va.rect(a0+1, a1-1, Z_FL+k*B.TRAY_H, Z_FL+(k+1)*B.TRAY_H,
                             '#fbfaf8', HID, THIN))
    o.append(va.rect(X_AC[0]+1, X_AC[1]-1, Z_FL, Z_FL+B.AC_H, '#fbfaf8', HID, THIN))
    for left in (True, False):
        xa = 0.0 if left else XS+B.SEAM/2
        xb = XS-B.SEAM/2 if left else W
        o.append(va.rect(xa, xb, Z_RIM, Z_LID, '#e6d9c4', INK, MED))
        za = Z_LID - S['PAN_TH']
        o.append(va.rect((xa+B.STILE+B.PAN_REV) if left else (xa+B.PAN_REV),
                         (xb-B.PAN_REV) if left else (xb-B.STILE-B.PAN_REV),
                         za, Z_LID, '#d9b877', INK, THIN))
    for xk in (PXX, W - PXX):
        o.append(va.circ((xk, Z_RIM), RK, '#ffffff', INK, MED))
        o.append(va.circ((xk, Z_RIM), KH/2, '#efe9df', INK, THIN))
        o.append(centre(va, [(xk-RK-10, Z_RIM), (xk+RK+10, Z_RIM)]))
    o.append(va.path([(-8, Z_RIM), (W+8, Z_RIM)], GRN, THIN, '9,4'))
    o.append(T(va.X(W)+8, va.Z(Z_RIM)-14, f'vành Z{Z_RIM:.0f}', font_size=9, fill=GRN))
    o.append(dim_v(va, 0, B.FOOT, 0, f'{B.FOOT:.0f}', off=-30))
    o.append(dim_v(va, B.FOOT, Z_FL, 0, f'{B.BOT:.0f}', off=-30))
    o.append(dim_v(va, Z_FL, Z_RIM, 0, f'{Z_RIM-Z_FL:.0f}', off=-30))
    o.append(dim_v(va, Z_RIM, Z_LID, 0, f'{B.T_LID:.0f}', off=-30))
    o.append(dim_v(va, 0, Z_LID, 0, f'{Z_LID:.0f}', off=-62))
    # chuoi X — dat duoi mat cat A-A, chung cho ca hai hinh chieu
    o.append(dim_h(va, 0, WH, 0, f'{WH:.0f}', off=30))
    o.append(dim_h(va, WH, WH+BAY, 0, f'{BAY:.0f}', off=30))
    o.append(dim_h(va, *X_DIV[0], 0, f'{DIV:.0f}', off=30))
    o.append(dim_h(va, *X_AC, 0, f'{ACB:.0f}', off=30))
    o.append(dim_h(va, X_DIV[1][0], X_DIV[1][1], 0, f'{DIV:.0f}', off=30))
    o.append(dim_h(va, W-WH-BAY, W-WH, 0, f'{BAY:.0f}', off=30))
    o.append(dim_h(va, W-WH, W, 0, f'{WH:.0f}', off=30))
    o.append(dim_h(va, 0, W, 0, f'{W:.0f}   THÂN', off=58))
    o.append(dim_h(va, -S['PROUD'], W+S['PROUD'], 0,
                   f'{S["X_OA"]:.1f}   PHỦ BÌ X (kể cả ống bản lề)', off=86))
    # ---------------- MAT CAT B-B (cot phai)
    vb = V(880, 330, SC)
    o.append(viewbox(866, 74, 686, 320, 'MẶT CẮT B-B — cắt dọc qua khoang khay', '', 'TL 1:2'))
    o.append(vb.rect(0, YB, 0, B.FOOT, '#efe9df', INK, MED))
    o.append(vb.rect(FB-B.BOT_TON, YB-FB+B.BOT_TON, B.FOOT, Z_FL, '#efe9df', INK, MED))
    for y0, y1 in [(0, FB), (YB-FB, YB)]:
        o.append(vb.rect(y0, y1, B.FOOT, Z_RIM, '#e6d9c4', INK, MED))
    o.append(vb.rect(0, B.WELL_D, Z_RIM-14, Z_RIM, '#f7e9e6', ACC, THIN))
    o.append(vb.rect(YB-B.WELL_D, YB, Z_RIM-14, Z_RIM, '#f7e9e6', ACC, THIN))
    for k in (0, 1):
        o.append(vb.rect(FB+B.AC_CLR, YB-FB-B.AC_CLR, Z_FL+k*B.TRAY_H,
                         Z_FL+(k+1)*B.TRAY_H, '#fbfaf8', HID, THIN))
    o.append(vb.rect(0, YB, Z_RIM, Z_LID, '#e6d9c4', INK, MED))
    o.append(vb.rect(B.RAIL+B.PAN_REV, YB-B.RAIL-B.PAN_REV, Z_LID-S['PAN_TH'], Z_LID,
                     '#d9b877', INK, THIN))
    o.append(dim_h(vb, 0, FB, 0, f'{FB:.0f}', off=28))
    o.append(dim_h(vb, FB, YB-FB, 0, f'{B.INNER_Y:.0f}', off=28))
    o.append(dim_h(vb, 0, YB, 0, f'{YB:.0f}', off=56))
    o.append(lead(*vb.P((B.WELL_D/2, Z_RIM-7)), 1010, 150,
                  f'khe luồn ngón {B.WELL_W:.0f} × sâu {B.WELL_D:.0f}', anchor='start'))
    o.append(lead(*vb.P((YB*0.62, Z_LID)), 1500, 122,
                  f'tấm Nu nâng — mặt trên ngang mặt khung'))
    # ---------------- BANG CHI TIET
    rows = [['1', f'Mắt mộng gỗ Ø{2*RK:.1f} · {B.N_KN} mắt × {B.KN_LEN:.0f} · bước {S["KN_PITCH"]:.0f} · '
             f'trục trên arris (X {PXX:.1f} , Z{Z_RIM:.0f}) · lỗ chốt Ø{KH:.2f}'],
            ['2', f'Hốc âm hai tay {GW:.0f} × sâu {GD:.0f}; khe hở vào tay {S["GRIP_APER"]:.2f} — xem BX-02'],
            ['3', f'Khe luồn ngón nhấc khay {B.WELL_W:.0f} × sâu {B.WELL_D:.0f}; X = '
             + ', '.join(f'{x:.0f}' for x in S['WELL_X'])],
            ['4', f'Hốc nam châm {B.MAG[0]+0.2:.1f} × {B.MAG[1]+0.2:.1f} × sâu {B.MAG_REC:.1f} · '
             f'{2*S["MAG_N_LEAF"]} hốc trên thân + {2*S["MAG_N_LEAF"]} đối ứng trên nắp · vị trí ±0,2'],
            ['5', f'Vách ngăn {DIV:.0f} · ngậm {B.DIV_TON:.0f} vào mặt trong vách trước/sau'],
            ['6', f'Rãnh ngậm vách trước/sau vào vách bản lề: sâu {B.JOINT_D:.0f} × rộng {FB:.0f}, '
             f'suốt chiều cao · {B.JOINT_NP} chốt draw-bore Ø{B.JOINT_PIN:.0f} mỗi góc, lệch tâm 0,4']]
    t, _ = table(866, 430, ['#', 'GHI CHÚ CHI TIẾT'], rows, 686, rh=23, fs=10, colw=[38, 648])
    o.append(t)
    notes = [f'Đáy THẢ trong rãnh sâu {B.BOT_GRV:.0f}, mộng {B.BOT_TON:.0f} → thả {S["BOT_FLOAT"]:.0f} mm mỗi phía; '
             f'chỉ dán 1 điểm ở tâm.',
             f'Rãnh ngậm ở hai đầu vách bản lề, hốc âm ở giữa — KHÔNG chồng nhau theo Y. '
             f'Vách còn {S["JOINT_LEFT"]:.0f} mm sau rãnh.',
             f'Vành thân phẳng Z{Z_RIM:.0f} suốt. Ống bản lề nhô ra {S["PROUD"]:.1f} mm mỗi bên — không hạ bậc.']
    return sheet('BX-01', 'THÂN HỘP', '1:2', 'cocobolo',
                 f'{sum(S["V"][k] for k in S["V_THAN"])/1e6*B.RHO["cocobolo"]:.2f} kg',
                 2, N_SH, ''.join(o), notes=notes)
SHEETS.append(('BX-01-than-hop', sheetBX01))

# ==========================================================================
# TO BX-02 — VACH BAN LE
# ==========================================================================
def sheetBX02():
    o = []
    SC = 4*MM                                   # 4:1
    prof = S['grip_profile'](40)
    ZCUT = Z_RIM + 7.0                          # cat ngang canh nap, ve duong gay
    v = V(180, 966, SC)
    o.append(viewbox(46, 74, 520, 966, 'MẶT CẮT VÁCH BẢN LỀ — tại một mắt mộng NẮP',
                     'cánh nắp đóng, cắt ngang ở Z' + f'{ZCUT:.0f}', 'TL 4:1'))
    # than
    wall = ([(0.0, S['GRIP_Z_TOP']), (0.0, Z_RIM - RK)]
            + [(RK*math.cos(math.radians(270 + 90*i/16)),
                Z_RIM + RK*math.sin(math.radians(270 + 90*i/16))) for i in range(17)]
            + [(WH, Z_RIM), (WH, B.FOOT), (0.0, B.FOOT), (0.0, Z_FL), (GD, Z_FL)]
            + list(prof)[::-1])
    o.append(v.rect(WH-B.BOT_GRV, WH+6, B.FOOT, Z_FL, '#efe9df', INK, MED))  # day tha trong ranh
    o.append(v.rect(-RK-1, WH+6, 0, B.FOOT, '#e2ded6', INK, THIN))           # chan dem
    o.append(v.poly([(0.0, Z_FL), (GD, Z_FL)] + list(prof)[::-1], '#ffffff', HID, THIN))
    o.append(v.poly(wall, '#e6d9c4', INK, THICK))
    o.append(v.rect(0.0, WH, Z_RIM, ZCUT, '#e6d9c4', INK, MED))             # canh nap (cat)
    o.append(v.path([(-RK-1, ZCUT), (-RK+1.5, ZCUT+1.2), (WH*0.25, ZCUT-1.2),
                     (WH*0.5, ZCUT+1.2), (WH*0.75, ZCUT-1.2), (WH, ZCUT)], INK, MED))
    o.append(v.circ((0.0, Z_RIM), RK, '#ffffff', INK, THICK))
    o.append(v.circ((0.0, Z_RIM), KH/2, '#efe9df', INK, MED))
    o.append(v.cross((0.0, Z_RIM), 16))
    o.append(v.path(list(prof), ACC, 2.0))
    o.append(centre(v, [(-RK-16, Z_RIM), (WH+10, Z_RIM)]))
    o.append(v.rect(WH-B.BOT_GRV, WH, B.FOOT, Z_FL, 'none', ACC, MED))       # ranh om day
    # kich thuoc
    o.append(dim_v(v, Z_FL, S['GRIP_Z_TOP'], 0, f'{S["GRIP_APER"]:.2f}  khe hở vào tay', off=-34))
    o.append(dim_v(v, S['GRIP_Z_TOP'], Z_RIM - RK, 0, f'{S["GRIP_LIP_MIN"]:.2f}', off=-34))
    o.append(dim_v(v, 0, Z_RIM, 0, f'{Z_RIM:.0f}  vành', off=-76))
    o.append(dim_h(v, 0, GD, Z_FL, f'{GD:.0f}  sâu hốc', off=34))
    o.append(dim_h(v, 0, WH, 0, f'{WH:.0f}  vách', off=64))
    o.append(dim_h(v, -RK, 0, Z_RIM + RK, f'{S["PROUD"]:.1f}', off=-30))
    o.append(lead(*v.P((B.GRIP_R*0.35, S['GRIP_Z_TOP']-B.GRIP_R*0.55)), 300, 600,
                  f'bo R{B.GRIP_R:.0f} ở mép ngoài trần'))
    o.append(lead(*v.P((GD*0.85, S['grip_ceil'](GD*0.85))), 300, 632,
                  f'dốc {B.GRIP_SLOPE:.0f}° lên phía trong'))
    o.append(lead(*v.P((-RK*0.7, Z_RIM+RK*0.7)), 500, 170,
                  f'ống Ø{2*RK:.1f} · lỗ chốt Ø{KH:.2f} · nhô ra {S["PROUD"]:.1f}'))
    o.append(lead(*v.P((WH-B.BOT_GRV/2, B.FOOT+B.BOT/2)), 500, 880,
                  f'rãnh ôm đáy {B.BOT_GRV:.0f} sâu × {B.BOT:.0f}; đáy thả {S["BOT_FLOAT"]:.0f} mm/phía'))
    # ---------------- KHAI TRIEN MAT NGOAI VACH
    SE = MM/2
    ve = V(600, 272, SE)
    o.append(viewbox(586, 74, 700, 268, 'KHAI TRIỂN MẶT NGOÀI VÁCH BẢN LỀ TRÁI',
                     'nhìn từ ngoài vào', 'TL 1:2'))
    o.append(ve.rect(0, B.LID_L, B.FOOT, Z_RIM, '#e6d9c4', INK, MED))
    o.append(ve.rect(GY0, GY1, Z_FL, S['GRIP_Z_TOP'], '#ffffff', ACC, MED))
    for y0, is_body in KN:
        o.append(ve.rect(y0, y0+B.KN_LEN, Z_RIM-RK, Z_RIM,
                         '#e6d9c4' if is_body else '#ffffff', INK, MED))
    for y0, y1 in [(0, FB), (B.LID_L-FB, B.LID_L)]:
        o.append(hidden(ve, [(y0, B.FOOT), (y1, B.FOOT), (y1, Z_RIM), (y0, Z_RIM), (y0, B.FOOT)]))
    o.append(dim_h(ve, GY0, GY1, B.FOOT, f'{GW:.0f}', off=26))
    o.append(dim_h(ve, 0, GY0, B.FOOT, f'{GY0:.0f}', off=26))
    o.append(dim_h(ve, 0, B.LID_L, B.FOOT, f'{B.LID_L:.0f}', off=52))
    o.append(dim_h(ve, S['KN_Y0'], S['KN_Y0']+B.KN_LEN, Z_RIM, f'{B.KN_LEN:.0f}', off=-24))
    o.append(dim_h(ve, S['KN_Y0'], S['KN_Y0']+S['KN_PITCH'], Z_RIM, f'{S["KN_PITCH"]:.0f}', off=-46))
    o.append(T(600, 332, 'mắt tô đậm = THÂN · mắt trắng = NẮP · '
               f'hõm 1/4 đĩa R{RK:.1f} ở góc trên-ngoài chỉ tại mắt NẮP',
               font_size=10, fill=DIM))
    # ---------------- BANG TOA DO TRAN HOC
    rows = [[f'{x:.0f}', f'{S["grip_ceil"](x):.2f}'] for x in range(0, int(GD)+1)]
    t, yy = table(600, 366, ['x (từ mặt ngoài)', 'Z trần (từ chuẩn A)'], rows, 260,
                  rh=18, fs=9.5, colw=[130, 130])
    o.append(T(600, 356, 'TOẠ ĐỘ TRẦN HỐC ÂM — cho lập trình CNC',
               font_size=11, font_weight='bold', fill=INK))
    o.append(t)
    o.append(T(600, yy + 18, f'Bán kính bo mép R{B.GRIP_R:.0f}, tâm ({B.GRIP_R:.1f} , {S["GRIP_CZ"]:.2f}).',
               font_size=9.5, fill=DIM))
    o.append(T(600, yy + 32, f'Tiếp điểm cung/mặt dốc tại x = {S["GRIP_XT"]:.2f}.', font_size=9.5, fill=DIM))
    o.append(T(600, yy + 46, f'Từ đó là mặt phẳng dốc {B.GRIP_SLOPE:.0f}° tới x = {GD:.0f}.',
               font_size=9.5, fill=DIM))
    # ---------------- BANG DUNG SAI
    tol = [['Đường kính ống gỗ', f'Ø{2*RK:.1f}', '±0,15', 'lộ ra ngoài — đặc tính nhìn thấy'],
           ['Lỗ chốt', f'Ø{KH:.2f}', '+0,05 / 0', f'chốt Ø{B.KN_PIN:.2f} −0,05 → khe 0,20…0,25'],
           ['Đồng trục lỗ chốt', '—', '≤ 0,15', 'giữa hai đầu chuỗi 350'],
           ['Bước mắt mộng', f'{S["KN_PITCH"]:.0f}', '±0,10', 'cộng dồn 6 bước → ±0,25'],
           ['Khe dọc trục giữa hai mắt', f'{B.KN_GAP:.0f}', '+0,3 / 0', 'chỗ cho gỗ nở theo mùa'],
           ['Thành gỗ quanh lỗ chốt', f'{S["KN_WALL_EFF"]:.1f}', 'min', 'ĐO ĐỘ TRÔI MŨI KHOAN TRƯỚC'],
           ['Khe hở vào tay', f'{S["GRIP_APER"]:.2f}', '+0,5 / 0', 'nông hơn là ngón không lọt'],
           ['Chiều sâu hốc âm', f'{GD:.0f}', '+0,5 / 0', ''],
           ['Bo mép ngoài trần', f'R{B.GRIP_R:.0f}', '±0,3', 'dao bo cạnh R8 có sẵn']]
    o.append(T(900, 356, 'DUNG SAI VÁCH BẢN LỀ', font_size=11, font_weight='bold', fill=INK))
    t2, yy2 = table(900, 366, ['KÍCH THƯỚC', 'TRỊ SỐ', 'DUNG SAI', 'LÝ DO'], tol, 640,
                    rh=20, fs=9.5, colw=[190, 90, 90, 270])
    o.append(t2)
    notes = [f'Hốc âm chỉ có ở vách TRÁI và PHẢI, đối xứng qua tâm hộp.',
             f'Trần hốc phay bằng dao bo cạnh R{B.GRIP_R:.0f} rồi vét mặt dốc {B.GRIP_SLOPE:.0f}°; '
             f'KHÔNG đánh giấy nhám làm tròn thêm.',
             f'Gỗ đặc còn trên trần {S["GRIP_LIP_MIN"]:.2f} mm — đủ, nhưng không được phay sâu hơn bảng toạ độ.']
    return sheet('BX-02', 'VÁCH BẢN LỀ · HỐC ÂM', '4:1 / 1:2', 'cocobolo',
                 f'{S["V"]["vach trai/phai"]/1e6*B.RHO["cocobolo"]/2:.2f} kg/chiếc',
                 3, N_SH, ''.join(o), notes=notes)
SHEETS.append(('BX-02-vach-ban-le', sheetBX02))

# ==========================================================================
# TO HD-01 — CANH NAP
# ==========================================================================
def sheetHD01():
    o = []
    SC = MM/2
    ST, RL, TL_ = B.STILE, B.RAIL, B.T_LID
    v = V(120, 790, SC)
    o.append(viewbox(46, 74, 470, 760, 'MẶT BẰNG MỘT CÁNH — nhìn từ trên',
                     'cánh trái; cánh phải đối xứng', 'TL 1:2'))
    o.append(v.rect(0, LW, 0, B.LID_L, '#e6d9c4', INK, THICK))
    o.append(v.rect(ST, LW-ST, RL, B.LID_L-RL, '#f6efe2', INK, MED))
    o.append(v.rect(ST+B.PAN_REV, LW-ST-B.PAN_REV, RL+B.PAN_REV, B.LID_L-RL-B.PAN_REV,
                    '#d9b877', INK, MED))
    o.append(hidden(v, [(ST-B.GRV, RL-B.GRV), (LW-ST+B.GRV, RL-B.GRV),
                        (LW-ST+B.GRV, B.LID_L-RL+B.GRV), (ST-B.GRV, B.LID_L-RL+B.GRV),
                        (ST-B.GRV, RL-B.GRV)]))
    for y0, is_body in KN:
        if is_body: continue
        o.append(v.rect(0, 2*RK, y0, y0+B.KN_LEN, '#ffffff', INK, MED))
    o.append(centre(v, [(PXX, -16), (PXX, B.LID_L+16)]))
    for xc in B.MAG_X:
        for yc in (B.MAG_Y, B.LID_L-B.MAG_Y):
            o.append(hidden(v, [(xc-B.MAG[0]/2, yc-B.MAG[1]/2), (xc+B.MAG[0]/2, yc-B.MAG[1]/2),
                               (xc+B.MAG[0]/2, yc+B.MAG[1]/2), (xc-B.MAG[0]/2, yc+B.MAG[1]/2),
                               (xc-B.MAG[0]/2, yc-B.MAG[1]/2)]))
    o.append(dim_h(v, 0, ST, 0, f'{ST:.0f}', off=28))
    o.append(dim_h(v, ST, LW-ST, 0, f'{S["OP_W"]:.2f}', off=28))
    o.append(dim_h(v, LW-ST, LW, 0, f'{ST:.0f}', off=28))
    o.append(dim_h(v, 0, LW, 0, f'{LW:.2f}', off=56))
    o.append(dim_v(v, 0, RL, 0, f'{RL:.0f}', off=-28))
    o.append(dim_v(v, RL, B.LID_L-RL, 0, f'{S["OP_L"]:.0f}', off=-28))
    o.append(dim_v(v, 0, B.LID_L, 0, f'{B.LID_L:.0f}', off=-56))
    o.append(lead(*v.P((LW*0.55, B.LID_L*0.62)), 452, 250,
                  f'tấm Nu nâng, lộ ra {S["FIELD_W"]:.2f} × {S["FIELD_L"]:.0f}'))
    o.append(lead(*v.P((ST-B.GRV/2, B.LID_L*0.28)), 452, 640,
                  f'rãnh ôm tấm {B.GRV:.0f} × {B.PAN_T:.0f}'))
    # ---------------- MAT CAT NGANG 1:1
    S1 = MM
    vc = V(600, 210, S1)
    o.append(viewbox(560, 74, 986, 230, 'MẶT CẮT NGANG CÁNH NẮP', '', 'TL 1:1'))
    o.append(vc.rect(0, LW, 0, TL_, '#e6d9c4', INK, MED))
    o.append(vc.rect(ST-B.GRV, LW-ST+B.GRV, TL_-B.S_TOP-B.PAN_T, TL_-B.S_TOP, '#d9b877', INK, MED))
    o.append(vc.rect(ST+B.PAN_REV, LW-ST-B.PAN_REV, TL_-B.S_TOP, TL_, '#d9b877', INK, MED))
    o.append(vc.rect(ST, LW-ST, 0, S['LIP_BOT'], '#ffffff', HID, THIN))
    o.append(vc.circ((PXX, TL_/2), RK, '#ffffff', INK, MED))
    o.append(dim_v(vc, 0, TL_, LW, f'{TL_:.0f}', off=26))
    o.append(dim_h(vc, 0, LW, 0, f'{LW:.2f}', off=30))
    o.append(lead(*vc.P((LW/2, S['LIP_BOT'])), 1180, 262,
                  f'khay bỏ bài — lòng lõm sâu {S["LIP_BOT"]:.1f} hình thành miễn phí'))
    # ---------------- CHI TIET MONG-RANH 4:1
    S4 = 4*MM
    vd = V(760, 610, S4)
    o.append(viewbox(560, 330, 480, 380, 'CT 1 — MỘNG–RÃNH & TẤM NÂNG', '', 'TL 4:1'))
    o.append(vd.rect(-13, 0, 0, TL_, '#e6d9c4', INK, MED))
    o.append(vd.rect(-B.GRV, 0, TL_-B.S_TOP-B.PAN_T, TL_-B.S_TOP, '#ffffff', INK, THIN))
    o.append(vd.rect(-B.TON, 9, TL_-B.S_TOP-B.PAN_T, TL_-B.S_TOP, '#d9b877', INK, MED))
    o.append(vd.rect(B.PAN_REV, 9, TL_-B.S_TOP, TL_, '#d9b877', INK, MED))
    o.append(dim_h(vd, -B.GRV, 0, TL_, f'{B.GRV:.0f}', off=-26))
    o.append(dim_h(vd, -B.TON, 0, 0, f'{B.TON:.0f}', off=26))
    o.append(dim_h(vd, 0, B.PAN_REV, TL_, f'{B.PAN_REV:.1f}', off=-52))
    o.append(dim_v(vd, TL_-B.S_TOP-B.PAN_T, TL_-B.S_TOP, 9, f'{B.PAN_T:.0f}', off=26))
    o.append(dim_v(vd, TL_-B.S_TOP, TL_, 9, f'{B.S_TOP:.0f}', off=26))
    o.append(dim_v(vd, 0, S['LIP_BOT'], -13, f'{S["LIP_BOT"]:.0f}', off=-26))
    o.append(lead(*vd.P((-B.GRV+(B.GRV-B.TON)/2, TL_-B.S_TOP-B.PAN_T/2)), 620, 690,
                  f'thả {S["PAN_FLOAT"]:.0f} mm mỗi phía — KHÔNG keo', anchor='start'))
    o.append(lead(*vd.P((B.PAN_REV/2, TL_)), 620, 360,
                  f'khe {B.PAN_REV:.1f} quanh lòng tấm', anchor='start'))
    # ---------------- BANG
    rows = [['Đố dọc × 2', f'{B.LID_L:.0f} × {ST:.0f} × {TL_:.0f}',
             f'XẺ XUYÊN TÂM, vòng năm ≥ 60° — P7'],
            ['Đố ngang × 2', f'{S["OP_W"]+2*B.TON:.1f} × {RL:.0f} × {TL_:.0f}', 'kể cả mộng hai đầu'],
            ['Tấm Nu nâng', f'{S["PAN_L"]:.0f} × {S["PAN_W"]:.2f} × {S["PAN_TH"]:.0f}',
             f'bậc {B.S_TOP:.0f} × {S["PAN_REB"]:.0f} quanh mép trên'],
            ['Rãnh ôm tấm', f'{B.GRV:.0f} sâu × {B.PAN_T:.0f} rộng', 'giữa bề dày, cách mặt trên '
             f'{B.S_TOP:.0f}'],
            ['Mộng khung', '8 mộng', 'epoxy + chốt draw-bore Ø5'],
            ['Mắt mộng bản lề', f'{S["N_KN_LID"]} mắt × {B.KN_LEN:.0f}',
             f'phay thẳng từ đố dọc, ống Ø{2*RK:.1f}'],
            ['Hốc nam châm', f'{2*len(B.MAG_X)}/cánh',
             f'{B.MAG[0]+0.2:.1f} × {B.MAG[1]+0.2:.1f} × {B.MAG_REC:.1f} ở mặt dưới']]
    o.append(T(1070, 348, 'CHI TIẾT CÁNH NẮP', font_size=11, font_weight='bold', fill=INK))
    t, yy = table(1070, 358, ['CHI TIẾT', 'KÍCH THƯỚC', 'GHI CHÚ'], rows, 480, rh=22,
                  fs=9.5, colw=[122, 158, 200])
    o.append(t)
    o.append(T(1070, yy + 26, 'GỖ NỞ — vì sao có khe quanh lòng tấm',
               font_size=11, font_weight='bold', fill=INK))
    mv = [['đã ổn định 11 %, ±{:.0f} % — TRƯỜNG HỢP THIẾT KẾ'.format(B.DMC_DES),
           f'{S["PAN_MOVE"]:.2f}',
           f'{B.PAN_REV-S["PAN_MOVE"]:.2f}', f'{B.PAN_REV+S["PAN_MOVE"]:.2f}'],
          ['xấu nhất, kể cả dung sai ±{:.2f}'.format(B.PAN_REV_TOL),
           f'{S["PAN_MOVE"]:.2f}',
           f'{B.PAN_REV-B.PAN_REV_TOL-S["PAN_MOVE"]:.2f}',
           f'{B.PAN_REV+B.PAN_REV_TOL+S["PAN_MOVE"]:.2f}'],
          ['lắp thẳng ở 9 %, +{:.0f} % — P5 CẤM'.format(B.DMC_DRY), f'{S["PAN_MOVE_DRY"]:.2f}',
           f'{B.PAN_REV-S["PAN_MOVE_DRY"]:.2f}', f'{B.PAN_REV+S["PAN_MOVE_DRY"]:.2f}']]
    t2, _ = table(1070, yy + 36, ['TRƯỜNG HỢP', 'DỊCH/PHÍA', 'KHE MIN', 'KHE MAX'], mv,
                  476, rh=20, fs=9.5, colw=[196, 96, 92, 92])
    o.append(t2)
    notes = [f'Tấm Nu THẢ trong rãnh — chỉ dán/chốt 1 điểm ở đúng tâm tấm. Dán quanh rãnh là tấm nứt.',
             f'Khe quanh lòng tấm {B.PAN_REV:.1f} ±{B.PAN_REV_TOL:.2f} chỉ đủ khi tấm ĐÃ ổn định '
             f'về 11 % MC (P5). Hàng cuối bảng bên phải là hậu quả nếu bỏ P5: khe âm, tấm ép vỡ mộng khung.',
             f'Khe ráp giữa hai cánh {B.SEAM:.1f} ±{B.SEAM_TOL:.2f} — bào CHUNG hai mép giáp nhau '
             f'sau khi lắp bản lề, không cộng hai bề rộng cánh.',
             f'Đố dọc XẺ XUYÊN TÂM (P7): khe ráp giữa {B.SEAM:.1f} tính theo hệ số {B.RAD_TAN:.2f}. '
             f'Xẻ tiếp tuyến thì khe đóng hẳn ở ΔMC {B.SEAM/(2*2*B.STILE*B.K["cocobolo ngang tho"]):.1f} %.']
    return sheet('HD-01', 'CÁNH NẮP', '1:2 / 1:1 / 4:1', 'cocobolo + Nu gõ đỏ',
                 f'{(S["V"]["khung nap"]/1e6*B.RHO["cocobolo"] + S["V"]["tam Nu"]/1e6*B.RHO["Nu go do"])/2:.2f} kg/cánh',
                 4, N_SH, ''.join(o), notes=notes)
SHEETS.append(('HD-01-canh-nap', sheetHD01))

# ==========================================================================
# TO TR-01 — KHAY QUAN
# ==========================================================================
def sheetTR01():
    o = []
    TL_, TW, TH = B.TRAY
    IL, IW, ID = B.TRAY_IN
    WALLT = (TL_ - IL)/2
    BOTT  = TH - ID
    nx, ny = int(IL//B.TILE_MAX[0]), int(IW//B.TILE_MAX[1])
    SC = MM/2
    v = V(200, 380, SC)
    o.append(viewbox(46, 74, 800, 400, 'MẶT BẰNG KHAY QUÂN',
                     f'xếp {ny} hàng × {nx} quân · cạnh 325 chạy theo Y của hộp', 'TL 1:2'))
    o.append(v.rect(0, TL_, 0, TW, '#e6d9c4', INK, THICK))
    o.append(v.rect(WALLT, TL_-WALLT, WALLT, TW-WALLT, '#fbfaf8', INK, MED))
    for j in range(ny):
        for k in range(nx):
            x = WALLT + 1 + k*(IL-2)/nx
            y = WALLT + 1 + j*(IW-2)/ny
            o.append(v.rect(x, x+B.TILE_MAX[0], y, y+B.TILE_MAX[1], '#f4efe2', HID, THIN))
    # khoet o MAT DAU khay (canh 124) — thang hang voi khe luon ngon o vach truoc/sau
    for x0, x1 in [(0, B.NOTCH_D), (TL_-B.NOTCH_D, TL_)]:
        o.append(v.rect(x0, x1, TW/2-B.WELL_W/2, TW/2+B.WELL_W/2, '#f7e9e6', ACC, MED))
    o.append(dim_h(v, 0, TL_, 0, f'{TL_:.0f}', off=52))
    o.append(dim_h(v, WALLT, TL_-WALLT, 0, f'{IL:.0f}  lòng', off=26))
    o.append(dim_v(v, 0, TW, 0, f'{TW:.0f}', off=-52))
    o.append(dim_v(v, WALLT, TW-WALLT, 0, f'{IW:.0f}', off=-26))
    o.append(dim_v(v, TW/2-B.WELL_W/2, TW/2+B.WELL_W/2, TL_, f'{B.WELL_W:.0f}', off=26))
    o.append(lead(*v.P((B.NOTCH_D/2, TW/2)), 300, 440,
                  f'khoét xuyên MẶT ĐẦU {B.WELL_W:.0f} × cao {B.NOTCH_H:.0f} × sâu {B.NOTCH_D:.0f} '
                  f'— thẳng hàng khe luồn ngón ở vách trước/sau', anchor='start'))
    # ---------------- MAT CAT 1:1
    S1 = MM
    vc = V(170, 720, S1)
    o.append(viewbox(46, 500, 800, 330, 'MẶT CẮT NGANG KHAY',
                     'hai khay chồng trong một khoang', 'TL 1:1'))
    for k in (0, 1):
        z0 = k*TH
        o.append(vc.rect(0, TW, z0, z0+BOTT, '#efe9df', INK, MED))
        o.append(vc.rect(0, WALLT, z0, z0+TH, '#e6d9c4', INK, MED))
        o.append(vc.rect(TW-WALLT, TW, z0, z0+TH, '#e6d9c4', INK, MED))
        o.append(vc.rect(WALLT, TW-WALLT, z0+BOTT, z0+BOTT+B.FELT, '#7a3b3b', INK, THIN))
        for j in range(ny):
            y = WALLT + 1 + j*(IW-2)/ny
            o.append(vc.rect(y, y+B.TILE_MAX[1], z0+BOTT+B.FELT,
                             z0+BOTT+B.FELT+B.TILE_MAX[2], '#f4efe2', HID, THIN))
    o.append(dim_v(vc, 0, TH, 0, f'{TH:.0f}', off=-26))
    o.append(dim_v(vc, 0, BOTT, 0, f'{BOTT:.0f}', off=-52))
    o.append(dim_v(vc, 0, 2*TH, TW, f'{2*TH:.0f}  hai khay', off=26))
    o.append(dim_h(vc, 0, TW, 0, f'{TW:.0f}', off=30))
    o.append(lead(*vc.P((TW*0.28, BOTT+B.FELT/2)), 700, 770, f'nỉ lót {B.FELT:.1f}'))
    o.append(lead(*vc.P((TW*0.72, TH + BOTT + B.FELT + B.TILE_MAX[2])), 700, 560,
                  f'quân {B.TILE_MAX[0]:.1f} × {B.TILE_MAX[1]:.1f} × {B.TILE_MAX[2]:.1f} (lớn nhất)'))
    # ---------------- BANG
    rows = [['Số khay', '4', f'2 khoang × 2 khay chồng'],
            ['Quân mỗi khay', f'{nx*ny}', f'{ny} hàng × {nx} quân'],
            ['Tổng quân trong khay', f'{4*nx*ny}', f'còn {B.N_TILES-4*nx*ny} quân ở rãnh Joker AC-01'],
            ['Phủ bì khay', f'{TL_:.0f} × {TW:.0f} × {TH:.0f}', 'khe 1,0 mỗi bên trong khoang'],
            ['Lòng khay', f'{IL:.0f} × {IW:.0f} × {ID:.0f}', f'vách {WALLT:.0f}, đáy {BOTT:.0f}'],
            ['Nỉ lót', f'{B.FELT:.1f}', 'dán kín đáy lòng'],
            ['Khoét mặt đầu (cạnh 124)', f'{B.WELL_W:.0f} × {B.NOTCH_H:.0f} × sâu {B.NOTCH_D:.0f}',
             f'hở {S["TILE_OPEN"]:.1f} mm bề dày quân — quân không tuột'],
            ['Khe luồn ngón', f'{S["LIFT_CHANNEL"]:.1f}', 'khoét khay + hốc vách trước/sau']]
    o.append(T(880, 92, 'CHI TIẾT KHAY QUÂN', font_size=11, font_weight='bold', fill=INK))
    t, yy = table(880, 102, ['MỤC', 'TRỊ SỐ', 'GHI CHÚ'], rows, 660, rh=22, fs=10,
                  colw=[190, 180, 290])
    o.append(t)
    notes = [f'Bốn khay giống hệt nhau, không phân trái/phải.',
             f'Mép trên vách khay bo R1; mép lòng bo R2 để lấy quân không cấn tay.',
             f'Đáy khay có thể dùng lõi ổn định + veneer để giảm {(S["V"]["khay quan"]/1e6*(B.RHO["cocobolo"]-B.RHO["loi on dinh"])):.2f} kg.']
    return sheet('TR-01', 'KHAY QUÂN', '1:2 / 1:1', 'cocobolo',
                 f'{S["V"]["khay quan"]/1e6*B.RHO["cocobolo"]/4:.2f} kg/chiếc',
                 5, N_SH, ''.join(o), notes=notes)
SHEETS.append(('TR-01-khay-quan', sheetTR01))

# ==========================================================================
# TO AC-01 — KHAY PHU KIEN
# ==========================================================================
def sheetAC01():
    o = []
    L, Wo, H = S['AC_L'], S['AC_W_OUT'], B.AC_H
    Wi = S['AC_W_IN']
    aw = B.AC_WALL
    jl = B.AC_JOKER[1]
    xs = [aw, aw+jl, aw+jl+aw, aw+jl+aw+S['AC_DICE_L'], aw+jl+aw+S['AC_DICE_L']+aw]
    SC = MM/2
    v = V(200, 300, SC)
    o.append(viewbox(46, 74, 800, 300, 'MẶT BẰNG AC-01', '', 'TL 1:2'))
    o.append(v.rect(0, L, 0, Wo, '#e6d9c4', INK, THICK))
    jy0, jy1 = (Wo - B.AC_JOKER[0])/2, (Wo + B.AC_JOKER[0])/2
    o.append(v.rect(aw, aw+jl, aw, Wo-aw, '#f6efe2', INK, MED))                 # long khoang Joker
    o.append(v.rect(aw, aw+jl, jy0, jy1, '#fbfaf8', INK, MED))                  # ranh Joker
    o.append(v.rect(xs[2], xs[2]+S['AC_DICE_L'], aw, Wo-aw, '#f6efe2', INK, MED))
    DL = B.dice_layout(S)                    # u theo chiều dài AC-01, w ngang
    for u0, u1, w0, w1 in DL['slots']:
        o.append(v.rect(xs[2]+u0, xs[2]+u1, aw+w0, aw+w1, '#e3dbcb', INK, THIN))
    for u0, u1, w0, w1 in DL['socks']:
        o.append(v.rect(xs[2]+u0, xs[2]+u1, aw+w0, aw+w1, '#cdc2ac', INK, MED))
    o.append(hidden(v, [(xs[2]+cx, aw+cy) for cx, cy in
                        [(0, 0), (S['AC_DICE_L'], 0), (S['AC_DICE_L'], S['AC_W_IN']),
                         (0, S['AC_W_IN']), (0, 0)]]))
    o.append(lead(*v.P((xs[2]+S['AC_DICE_L']/2, aw+S['AC_W_IN']/2)), 826, 96,
                  f'ổ xúc xắc — chi tiết ở AC-02', anchor='end'))
    o.append(v.rect(xs[4], L-aw, aw, Wo-aw, '#fbfaf8', INK, MED))               # hoc du phong
    for yc in (jy0, jy1):
        for xc in (aw+jl/2 - 40, aw+jl/2 + 40):
            o.append(v.circ((xc, yc), B.SCAL_D/2, '#fbfaf8', ACC, MED))
    o.append(lead(*v.P((aw+jl/2 - 40, jy1)), 826, 132,
                  f'hõm ngón Ø{B.SCAL_D:.0f} sâu {B.SCAL_DEP:.0f} — dải gỗ còn {S["SCAL_LEFT"]:.1f}',
                  anchor='end'))
    o.append(dim_h(v, 0, aw, 0, f'{aw:.0f}', off=26))
    o.append(dim_h(v, aw, aw+jl, 0, f'{jl:.0f}', off=26))
    o.append(dim_h(v, xs[2], xs[2]+S['AC_DICE_L'], 0, f'{S["AC_DICE_L"]:.0f}', off=26))
    o.append(dim_h(v, xs[4], L-aw, 0, f'{B.AC_AUX_L:.0f}', off=26))
    o.append(dim_h(v, 0, L, 0, f'{L:.0f}', off=52))
    o.append(dim_v(v, 0, Wo, 0, f'{Wo:.0f}', off=-26))
    o.append(dim_v(v, aw, Wo-aw, L, f'{Wi:.0f}', off=26))
    # ---------------- MAT CAT DOC 1:1
    S1 = MM/2
    vc = V(200, 620, S1)
    o.append(viewbox(46, 420, 800, 300, 'MẶT CẮT DỌC AC-01', '', 'TL 1:2'))
    o.append(vc.rect(0, L*0.0 + 0, 0, H, 'none', 'none', 0))
    prof = [(0, 0), (L, 0), (L, H), (0, H)]
    o.append(vc.poly(prof, '#e6d9c4', INK, MED))
    o.append(vc.rect(aw, aw+jl, H-B.AC_JOKER[2], H, '#fbfaf8', INK, MED))
    o.append(vc.rect(0, L, 0, H, 'none', INK, MED))
    o.append(vc.rect(xs[2], xs[2]+S['AC_DICE_L'], H-B.COVER_T, H, '#f6efe2', INK, MED))
    for u0, u1, w0, w1 in DL['slots']:
        if abs(w0 - S['DICE_W'][0]) > 1e-9: continue
        o.append(vc.rect(xs[2]+u0, xs[2]+u1, H-DL['slot_d'], H-B.COVER_T, '#e3dbcb', INK, THIN))
    for u0, u1, w0, w1 in DL['socks']:
        if abs(w0 - S['DICE_W'][0]) > 1e-9: continue
        o.append(vc.rect(xs[2]+u0, xs[2]+u1, H-DL['sock_d'], H-B.COVER_T, '#cdc2ac', INK, MED))
    o.append(vc.rect(xs[4], L-aw, H-B.AC_AUX_D, H, '#fbfaf8', INK, MED))
    o.append(dim_v(vc, 0, H, 0, f'{H:.0f}', off=-26))
    o.append(dim_v(vc, H-B.AC_JOKER[2], H, aw+jl/2, f'{B.AC_JOKER[2]:.1f}', off=26))
    o.append(dim_v(vc, H-B.AC_AUX_D, H, L, f'{B.AC_AUX_D:.1f}', off=26))
    o.append(lead(*vc.P((aw+jl*0.35, H-B.AC_JOKER[2]/2)), 250, 470,
                  f'rãnh Joker {B.AC_JOKER[0]:.0f} × {jl:.0f} × sâu {B.AC_JOKER[2]:.1f}',
                  anchor='start'))
    o.append(lead(*vc.P((xs[2]+S['DICE_U'][0]+B.DICE_SOCK/2, H-DL['sock_d']/2)), 700, 690,
                  f'4 ổ {B.DICE_SOCK:.0f} × {B.DICE_SOCK:.0f} sâu {DL["sock_d"]:.0f} + khe luồn '
                  f'ngón {B.DICE_SLOT:.0f} sâu {DL["slot_d"]:.0f} — AC-02'))
    o.append(lead(*vc.P(((xs[4]+L-aw)/2, H-B.AC_AUX_D/2)), 700, 712,
                  f'hốc {B.AC_AUX_L:.0f} — 4 quân dự phòng nằm 2 × 2'))
    rows = [['Phủ bì', f'{L:.0f} × {Wo:.0f} × {H:.0f}', f'khe {B.AC_CLR:.1f} mỗi đầu trong khoang {ACB:.0f}'],
            ['Lòng rộng', f'{Wi:.0f}', f'vách {aw:.0f}'],
            ['Chuỗi dài', f'{aw:.0f}+{jl:.0f}+{aw:.0f}+{S["AC_DICE_L"]:.0f}+{aw:.0f}+{B.AC_AUX_L:.0f}+{aw:.0f}',
             f'= {L:.0f}'],
            ['Rãnh Joker', f'{B.AC_JOKER[0]:.0f} × {jl:.0f} × {B.AC_JOKER[2]:.1f}', '8 quân dựng đứng'],
            ['Hõm ngón rãnh Joker', f'Ø{B.SCAL_D:.0f} sâu {B.SCAL_DEP:.0f}',
             f'2 cặp đối nhau; dải gỗ còn {S["SCAL_LEFT"]:.1f}'],
            ['Ổ xúc xắc', f'4 × {B.DICE_SOCK:.0f} × {B.DICE_SOCK:.0f} × {B.DICE_SOCK_D:.0f}',
             f'sâu đo từ SÀN đặt nắp che — xem AC-02'],
            ['Nắp che ổ xúc xắc', f'{S["COVER_L"]:.1f} × {S["COVER_W"]:.1f} × {B.COVER_T:.0f}',
             f'nắp thả kín miệng hốc, sàn sâu {B.COVER_T:.0f}'],
            ['Hốc dự phòng', f'{B.AC_AUX_L:.0f} × sâu {B.AC_AUX_D:.1f}', '4 quân 2 × 2']]
    o.append(T(880, 92, 'CHI TIẾT AC-01', font_size=11, font_weight='bold', fill=INK))
    t, _ = table(880, 102, ['MỤC', 'TRỊ SỐ', 'GHI CHÚ'], rows, 660, rh=22, fs=10,
                 colw=[190, 210, 260])
    notes = [f'AC-01 nhấc ra bằng hai hõm ngón Ø{B.SCAL_D:.0f} hai bên rãnh Joker, không có khe luồn ngón riêng.',
             f'Đáy các hốc dán nỉ {B.FELT:.1f}.',
             f'Khối đặc phay lòng — KHÔNG ghép hộp, vì vách {aw:.0f} mm ghép mộng sẽ yếu hơn phay.']
    o.append(t)
    return sheet('AC-01', 'KHAY PHỤ KIỆN', '1:2', 'cocobolo',
                 f'{S["V"]["khay phu kien"]/1e6*B.RHO["cocobolo"]:.2f} kg',
                 6, N_SH, ''.join(o), notes=notes)
SHEETS.append(('AC-01-khay-phu-kien', sheetAC01))

# ==========================================================================
# TO AC-02 — O XUC XAC VA NAP CHE
# ==========================================================================
def rr(v, x0, x1, z0, z1, r, fill, st=INK, sw=MED, n=6):
    """Chu nhat bo goc ban kinh r — goc bo LA VET DAO PHAY, khong phai trang tri."""
    pts = []
    for cx, cz, a0 in [(x1-r, z0+r, -90.0), (x1-r, z1-r, 0.0),
                       (x0+r, z1-r, 90.0), (x0+r, z0+r, 180.0)]:
        for i in range(n+1):
            a = math.radians(a0 + 90.0*i/n)
            pts.append((cx + r*math.cos(a), cz + r*math.sin(a)))
    return v.poly(pts, fill, st, sw)

def cover_outline(u0, w0):
    """Duong bao nap che dat tai (u0,w0), hai hom ngon o canh u nho."""
    L, Wc = S['COVER_L'], S['COVER_W']
    c = B.COVER_CLR/2
    pts, r = [], B.COVER_NOTCH/2
    pts.append((u0, w0))
    for wc in S['COVER_NOTCH_W']:                 # tam hom, do trong he cua HOC
        wl = wc - c                               # doi ve he cua NAP
        pts.append((u0, w0 + wl - r))
        for i in range(13):
            a = math.radians(-90.0 + 180.0*i/12)
            pts.append((u0 + r*math.cos(a), w0 + wl + r*math.sin(a)))
        pts.append((u0, w0 + wl + r))
    pts += [(u0, w0 + Wc), (u0 + L, w0 + Wc), (u0 + L, w0), (u0, w0)]
    return pts

def sheetAC02():
    o = []
    DL = B.dice_layout(S)
    ZL, ZW = S['AC_DICE_L'], S['AC_W_IN']
    ml, mw = S['DICE_MARG_L'], S['DICE_MARG_W']
    sk, rb, sl = B.DICE_SOCK, B.DICE_RIB, B.DICE_SLOT
    aw, H = B.AC_WALL, B.AC_H
    R = S['DICE_R']
    col0, col1 = S['DICE_W']
    SEC_W = col0 + sk/2                       # mat cat A-A di qua tam cot o thu nhat
    z_rec, z_slt, z_sok = H - B.COVER_T, H - DL['slot_d'], H - DL['sock_d']
    zb = S['Z_RIM'] - S['Z_FLOOR']            # vanh than, trong he toa do AC-01
    SC1, SC2, SC3 = MM, MM*2, MM*3

    # ================================================ V1  MAT BANG 2:1
    v = V(108, 586, SC2)
    o.append(viewbox(46, 74, 660, 620, 'MẶT BẰNG Ổ XÚC XẮC — nắp che tháo ra',
                     'ba cao độ phay từ vành AC-01: sàn đặt nắp · khe luồn ngón · ổ',
                     'TL 2:1'))
    o.append(v.rect(-aw, ZL+aw, -aw, ZW+aw, '#e6d9c4', INK, MED))     # vach AC-01
    o.append(v.rect(0, ZL, 0, ZW, '#f2ece1', INK, THICK))             # san dat nap che
    for u0, u1, w0, _ in DL['slots']:
        comb = (u0, u0 + sl + sk) if u0 < ZL/2 else (u1 - sl - sk, u1)
        o.append(rr(v, comb[0], comb[1], w0, w0 + sk, R, '#e3dbcb', INK, THIN))
    for u0, u1, w0, w1 in DL['socks']:
        o.append(rr(v, u0, u1, w0, w1, R, '#cdc2ac', INK, MED))
    o.append(v.path(cover_outline(B.COVER_CLR/2, B.COVER_CLR/2), ACC, MED, '8,4'))
    ch = [(0, ml), (ml, ml+sl), (ml+sl, ml+sl+sk), (ml+sl+sk, ml+sl+sk+rb),
          (ZL-ml-sl-sk, ZL-ml-sl), (ZL-ml-sl, ZL-ml), (ZL-ml, ZL)]
    for a, b in ch:
        o.append(dim_h(v, a, b, -aw, f'{b-a:.0f}', off=26))
    o.append(dim_h(v, 0, ZL, -aw, f'{ZL:.0f}  miệng hốc', off=54))
    for a, b in [(0, mw), (mw, mw+sk), (mw+sk, mw+sk+rb), (ZW-mw-sk, ZW-mw), (ZW-mw, ZW)]:
        o.append(dim_v(v, a, b, 0, f'{b-a:.1f}' if (b-a) % 1 else f'{b-a:.0f}', off=-26))
    o.append(dim_v(v, 0, ZW, ZL+aw, f'{ZW:.0f}', off=30))
    ya = v.Z(SEC_W)
    o.append(f'<path d="M {v.X(-aw)-26:.1f},{ya:.1f} L {v.X(ZL+aw)+26:.1f},{ya:.1f}" '
             f'stroke="{CEN}" stroke-width="{MED}" stroke-dasharray="14,4,3,4"/>')
    for xx, an in ((v.X(-aw)-30, 'end'), (v.X(ZL+aw)+30, 'start')):
        o.append(T(xx, ya + 4, 'A', text_anchor=an, font_size=12,
                   font_weight='bold', fill=CEN))
    for u0, u1, w0, w1 in DL['socks']:
        cx_, cy_ = v.X((u0+u1)/2), v.Z((w0+w1)/2)
        o.append(T(cx_, cy_ - 3, f'Ổ {sk:.0f} × {sk:.0f}', text_anchor='middle',
                   font_size=9.5, font_weight='bold', fill=INK))
        o.append(T(cx_, cy_ + 11, f'sâu {B.DICE_SOCK_D:.0f}  R{R:.0f}',
                   text_anchor='middle', font_size=9, fill=DIM))
    for u0, u1, w0, w1 in DL['slots']:
        o.append(f'<g transform="translate({v.X((u0+u1)/2):.1f},'
                 f'{v.Z(w0+sk/2):.1f}) rotate(-90)">'
                 + T(0, 4, 'khe luồn ngón', text_anchor='middle', font_size=9, fill=DIM)
                 + '</g>')

    # ================================================ V2  MAT CAT A-A 1:1
    vc = V(101, 985, SC1)
    o.append(viewbox(46, 714, 390, 350, 'MẶT CẮT A-A', 'qua tâm một cột ổ', 'TL 1:1'))
    seg, u = [], 0.0
    marks = sorted([(a, b, z_slt) for a, b, w0, _ in DL['slots'] if abs(w0-col0) < 1e-9]
                   + [(a, b, z_sok) for a, b, w0, _ in DL['socks'] if abs(w0-col0) < 1e-9])
    for a, b, z in marks:
        if a > u: seg.append((u, a, z_rec))
        seg.append((a, b, z)); u = b
    if u < ZL: seg.append((u, ZL, z_rec))
    prof = [(-aw, 0.0), (ZL+aw, 0.0), (ZL+aw, H), (ZL, H)]
    for a, b, z in reversed(seg):
        prof += [(b, z), (a, z)]
    prof += [(0.0, H), (-aw, H)]
    o.append(vc.poly(prof, '#e6d9c4', INK, MED))
    o.append(vc.rect(B.COVER_CLR/2, ZL - B.COVER_CLR/2, z_rec, H, '#f2ece1', INK, THICK))
    for u0, u1, w0, _ in DL['socks']:
        if abs(w0 - col0) > 1e-9: continue
        c = (u0 + u1)/2
        o.append(vc.rect(c - B.DIE/2, c + B.DIE/2, z_sok, z_sok + B.DIE,
                         '#cbd6e4', CEN, MED))
    o.append(vc.rect(-aw, ZL+aw, zb - B.FELT_PAD, zb, '#dcdcd2', HID, THIN))
    o.append(vc.path([(-aw-8, zb), (ZL+aw+8, zb)], HID, MED, '7,4'))
    o.append(dim_v(vc, 0, H, -aw, f'{H:.0f}', off=-30))
    o.append(dim_v(vc, 0, z_sok, ZL+aw, f'{S["AC_DICE_FLR"]:.0f}', off=26))
    o.append(dim_v(vc, z_sok, H, ZL, f'{DL["sock_d"]:.0f}', off=52))
    o.append(T(vc.X(ZL/2), vc.Z(zb) - 8, f'nắp hộp Z{S["Z_RIM"]:.0f} · nỉ đệm '
               f'{B.FELT_PAD:.1f}', text_anchor='middle', font_size=9, fill=HID))

    # ================================================ V3  NAP CHE 2:1
    o.append(viewbox(726, 74, 660, 560, 'NẮP CHE Ổ XÚC XẮC — 1 chiếc',
                     'cocobolo, thớ chạy theo cạnh dài', 'TL 2:1'))
    vl = V(806, 550, SC2)
    o.append(vl.poly(cover_outline(0.0, 0.0), '#e6d9c4', INK, THICK))
    o.append(dim_h(vl, 0, S['COVER_L'], 0, f'{S["COVER_L"]:.1f}', off=26))
    o.append(dim_v(vl, 0, S['COVER_W'], S['COVER_L'], f'{S["COVER_W"]:.1f}', off=28))
    nl = [wc - B.COVER_CLR/2 for wc in S['COVER_NOTCH_W']]
    for wl_ in nl:
        o.append(vl.cross((0, wl_), 4.0, ACC))
        o.append(dim_v(vl, wl_ - B.COVER_NOTCH/2, wl_ + B.COVER_NOTCH/2, 0,
                       f'Ø{B.COVER_NOTCH:.0f}', off=-26))
    o.append(dim_v(vl, nl[0] + B.COVER_NOTCH/2, nl[1] - B.COVER_NOTCH/2, 0,
                   f'{S["COVER_LIG_MID"]:.0f}', off=-26))
    o.append(dim_v(vl, nl[1] + B.COVER_NOTCH/2, S['COVER_W'], 0,
                   f'{S["COVER_LIG_END"]:.2f}', off=-26))
    o.append(dim_h(vl, 0, B.COVER_NOTCH/2, S['COVER_W'], f'{B.COVER_NOTCH/2:.0f}', off=-24))
    ax, ay2 = vl.X(S['COVER_L']*0.55), vl.Z(S['COVER_W']*0.5)
    o.append(f'<path d="M {ax:.0f},{ay2:.0f} L {ax+70:.0f},{ay2:.0f}" stroke="{DIM}" '
             f'stroke-width="{THIN}"/>' + T(ax + 76, ay2 + 4, 'chiều thớ',
                                            font_size=9.5, fill=DIM))
    ve = V(806, 612, SC2)
    o.append(ve.rect(0, S['COVER_L'], 0, B.COVER_T, '#e6d9c4', INK, MED))
    o.append(dim_v(ve, 0, B.COVER_T, S['COVER_L'], f'{B.COVER_T:.0f}', off=30))
    o.append(T(806, 628, f'CẠNH — bề dày {B.COVER_T:.0f} (0 / −0,10)',
               font_size=9.5, fill=DIM))

    # ================================================ V4  CHI TIET BAC 3:1
    u_lo, u_hi = 8.0, 26.0
    vd = V(486 - u_lo*SC3, 1210.8, SC3)
    o.append(viewbox(446, 714, 260, 350, 'CHI TIẾT — bậc khe', '', 'TL 3:1'))
    segd = [(u_lo, ml + sl, z_slt), (ml + sl, u_hi, z_sok)]
    pf = [(u_lo, 14.0), (u_hi, 14.0)]
    for a, b, z in reversed(segd):
        pf += [(b, z), (a, z)]
    o.append(vd.poly(pf, '#e6d9c4', INK, MED))
    o.append(vd.rect(u_lo, u_hi, z_rec, H, '#f2ece1', INK, THICK))
    cdie = S['DICE_U'][0] + sk/2
    o.append(vd.rect(cdie - B.DIE/2, u_hi, z_sok, z_sok + B.DIE, '#cbd6e4', CEN, MED))
    o.append(dim_v(vd, z_sok, z_slt, u_lo, f'{B.DICE_STEP:.0f}', off=-26))
    o.append(dim_v(vd, z_sok + B.DIE, z_rec, u_lo, f'{S["DIE_HEAD"]:.0f}', off=-26))
    o.append(T(vd.X((u_lo + ml + sl)/2), vd.Z(z_slt) - 8, 'sàn khe',
               text_anchor='middle', font_size=9, fill=DIM))
    o.append(T(vd.X(u_hi) - 4, vd.Z(z_sok + B.DIE/2), 'quân', text_anchor='end',
               font_size=9, fill=CEN))
    o.append(T(vd.X(u_lo), vd.Z(H) - 8, 'nắp che', font_size=9, fill=DIM))

    # ================================================ bang kich thuoc
    rows = [['Miệng hốc trên khối AC-01', f'{ZL:.0f} × {ZW:.0f}', 'suy từ chuỗi dài AC-01'],
            ['Sàn đặt nắp che', f'sâu {B.COVER_T:.0f} +0,15 / 0',
             f'phủ HẾT miệng hốc; vành đỡ {ml:.0f} hai đầu / {mw:.1f} hai bên'],
            ['Ổ xúc xắc', f'4 × {sk:.0f} × {sk:.0f} × sâu {B.DICE_SOCK_D:.0f}, góc R{R:.0f}',
             f'sâu kể từ sàn nắp; từ vành là {DL["sock_d"]:.0f}'],
            ['Khe luồn đầu ngón', f'4 × {sl:.0f} × {sk:.0f} × sâu {DL["slot_d"]:.0f}',
             f'sâu kể từ vành; bậc {B.DICE_STEP:.0f} so với sàn ổ'],
            ['Dao phay ổ', f'Ø{B.DICE_MILL:.0f} → R{R:.0f}',
             f'trần trên R{S["DICE_R_MAX"]:.2f}; dao Ø8 làm quân kênh góc'],
            ['Nắp che', f'{S["COVER_L"]:.1f} × {S["COVER_W"]:.1f} × {B.COVER_T:.0f} (0 / −0,10)',
             f'khe lắp {B.COVER_CLR:.1f} tổng; thớ theo cạnh dài'],
            ['Hõm ngón trên nắp che', f'2 × nửa tròn Ø{B.COVER_NOTCH:.0f}, khoét suốt bề dày',
             f'gỗ còn {S["COVER_LIG_MID"]:.0f} giữa, {S["COVER_LIG_END"]:.2f} hai góc'],
            ['Đáy AC-01 dưới ổ', f'{S["AC_DICE_FLR"]:.0f}',
             f'quân xúc xắc {B.DIE:.0f} — PHẢI đo lại trên lô mua (P3)']]
    o.append(T(726, 648, 'BẢNG KÍCH THƯỚC AC-02', font_size=12,
               font_weight='bold', fill=INK))
    t, _ = table(726, 656, ['MỤC', 'TRỊ SỐ (mm)', 'GHI CHÚ'], rows, 660, rh=14, fs=9,
                 colw=[170, 235, 255])
    o.append(t)
    notes = [f'Tô đậm dần theo chiều sâu: sàn đặt nắp · khe luồn ngón · ổ. Đứt đỏ = bao nắp che.',
             f'Ba cao độ phay từ MỘT lần gá; chuẩn là vành AC-01 đã bào phẳng, không phải đáy khay.',
             f'Nắp che tựa bốn cạnh vào sàn — KHÔNG hạ bậc vào thành vách nào, nên không có gờ mỏng.',
             f'Vành AC-01 Z{S["Z_FLOOR"]+H:.0f}, nắp hộp Z{S["Z_RIM"]:.0f}, nỉ đệm {B.FELT_PAD:.1f} '
             f'→ nắp che chỉ được nhô {S["COVER_PROUD"]:.1f} mm.',
             f'Nên dung sai một chiều: sàn {B.COVER_T:.0f} +0,15/0 và nắp che {B.COVER_T:.0f} 0/−0,10 '
             f'→ nắp luôn thấp hơn vành 0..0,25.',
             f'Đầu ngón {B.FING_T_TIP:.0f} lọt khe {sl:.0f}, bám {S["DIE_GRIP"]:.0f} mm sườn quân. '
             f'Quân hở trên đầu {S["DIE_HEAD"]:.0f} nên không leo nổi bậc {B.DICE_STEP:.0f}.',
             f'Thớ nắp che cùng chiều thớ AC-01. Đáy ổ và đáy khe dán nỉ {B.FELT:.1f}.']
    return sheet('AC-02', 'Ổ XÚC XẮC · NẮP CHE', '2:1 / 1:1 / 3:1', 'cocobolo',
                 f'{S["V"]["nap che o xuc xac"]/1e3*B.RHO["cocobolo"]:.0f} g (nắp che)',
                 7, N_SH, ''.join(o), notes=notes)
SHEETS.append(('AC-02-o-xuc-xac', sheetAC02))

# ==========================================================================
# TO QA-01 — DUNG SAI, KIEM, DAC TINH BAT BUOC
# ==========================================================================
def sheetQA01():
    o = []
    x0, y0 = FR[0] + 26, FR[1] + 60
    o.append(T(x0, y0 - 22, 'ĐẶC TÍNH KIỂM BẮT BUỘC — làm TRƯỚC khi cắt lô',
               font_size=15, font_weight='bold', fill=INK))
    pre = [['P1', f'Khoan thử lỗ chốt Ø{KH:.2f} sâu {B.KN_PIN_L:.0f} xuyên {B.N_KN} mắt mộng cocobolo',
            '≤ 0,10 mm độ trôi mũi khoan',
            f'thành gỗ quanh lỗ chỉ {S["KN_WALL_EFF"]:.1f} mm; trượt là nứt ống'],
           ['P2', 'Ép thử 1 mộng khung cocobolo, để 7 ngày rồi phá huỷ',
            'đường phá đi qua thớ gỗ, không đi dọc đường keo',
            'gỗ nhiều dầu — epoxy + lau acetone trong 15 phút'],
           ['P3', 'Đo tối thiểu 20 quân thuộc ĐÚNG lô mua',
            f'≤ {B.TILE_MAX[0]:.1f} × {B.TILE_MAX[1]:.1f} × {B.TILE_MAX[2]:.1f}',
            'chặn mọi thứ về khay; sai là làm lại toàn bộ khay'],
           ['P4', f'Đo lực tách 1 cặp nam châm {B.MAG[0]:.0f}×{B.MAG[1]:.0f}×{B.MAG[2]:.0f} qua lớp hoàn thiện',
            f'≥ {B.MAG_PULL*(1-B.MAG_DERATE):.0f} N mỗi cặp',
            'catalogue ghi 30 N khi tiếp xúc trực tiếp'],
           ['P5', 'Ổn định tấm Nu và mọi phôi về 11 % MC — ĐIỀU KIỆN CHẶN', '11 % ±1',
            f'khe quanh lòng tấm {B.PAN_REV:.1f} chỉ đủ NẾU P5 đạt; bỏ P5 thì cần '
            f'{S["PAN_MOVE_DRY"]:.2f} và tấm ép vỡ mộng khung'],
           ['P6', 'Đo cạnh quân xúc xắc thuộc ĐÚNG lô mua (tối thiểu 4 quân)',
            f'≤ {B.DIE:.1f} mm mỗi cạnh',
            f'ổ {B.DICE_SOCK:.0f} chỉ chừa {(B.DICE_SOCK-B.DIE)/2:.1f} mm mỗi bên; '
            f'quân lớn hơn là làm lại cả ổ lẫn nắp che — xem AC-02'],
           ['P7', 'Kiểm góc vòng năm 4 đố dọc cánh nắp — phải XẺ XUYÊN TÂM',
            '≥ 60° so với mặt đố',
            f'khe {B.SEAM:.1f} tính theo hệ số {B.RAD_TAN:.2f} (tra bảng); xẻ tiếp tuyến '
            f'thì khe đóng ở ΔMC {B.SEAM/(2*2*B.STILE*B.K["cocobolo ngang tho"]):.1f} %'],
           ['P8', f'Đo lực nén 1 miếng nỉ {B.FELT_PAD_SZ[0]:.0f}×{B.FELT_PAD_SZ[1]:.0f}×'
                  f'{B.FELT_PAD:.1f} ép xuống {B.CLR_Z:.1f} mm',
            f'≤ {S["FELT_F_PAD"]:.1f} N mỗi miếng',
            f'nỉ đẩy nắp lên, nam châm giữ xuống; {S["FELT_PAD_N"]:.0f} miếng = '
            f'{S["FELT_FORCE"]:.0f} N trên {S["MAG_TOTAL"]:.0f} N lực hút']]
    t, yy = table(x0, y0, ['#', 'PHÉP THỬ', 'TIÊU CHÍ ĐẠT', 'VÌ SAO'], pre, 1480, rh=26,
                  fs=10.5, colw=[50, 560, 350, 520])
    o.append(T(x0, yy + 34, 'DUNG SAI CHUNG', font_size=15, font_weight='bold', fill=INK))
    tol = [['Kích thước phủ bì', '±0,5', 'không lắp với gì'],
           ['Kích thước lắp ghép', '±0,15', 'mộng, rãnh, lỗ chốt'],
           ['Vị trí hốc nam châm', '±0,2', 'lệch quá thì hai cánh không đều'],
           ['Đồng phẳng vành thân', '≤ 0,2 trên 350', 'nắp đóng phải kín'],
           ['Đồng phẳng mặt nắp (tấm Nu ↔ khung)', '≤ 0,15', 'đặc tính nhìn thấy chính'],
           ['Khe ráp giữa hai cánh', f'{B.SEAM:.1f} ±{B.SEAM_TOL:.2f}',
            'bào chung hai mép SAU khi lắp bản lề — không cộng hai bề rộng cánh'],
           ['Khe quanh lòng tấm Nu', f'{B.PAN_REV:.1f} ±{B.PAN_REV_TOL:.2f}',
            f'chỗ cho gỗ nở; xấu nhất {B.PAN_REV-B.PAN_REV_TOL:.2f} so với nở {S["PAN_MOVE"]:.2f}'],
           ['Góc mở nắp', '180° +0 / −1°', 'chặn tự nhiên bằng mặt cạnh nắp'],
           ['Độ nhám bề mặt lộ ra', 'P400 trước khi hoàn thiện', '']]
    t2, yy2 = table(x0, yy + 44, ['MỤC', 'DUNG SAI', 'GHI CHÚ'], tol, 720, rh=22, fs=10,
                    colw=[330, 190, 200])
    o.append(t2)
    o.append(T(x0 + 760, yy + 34, 'THỨ TỰ LẮP', font_size=15, font_weight='bold', fill=INK))
    seq = [['1', 'Phay hốc âm + hõm mắt mộng trên vách bản lề (TRƯỚC khi ghép thân)'],
           ['2', 'Phay rãnh ngậm + rãnh ôm đáy trên vách bản lề và vách trước/sau'],
           ['3', 'Ghép thử KHÔ toàn bộ thân, kiểm vuông góc và đồng phẳng vành'],
           ['4', 'Ghép thân bằng epoxy + chốt draw-bore; đáy THẢ, không keo'],
           ['5', 'Ghép khung nắp, thả tấm Nu, chỉ chốt 1 điểm ở tâm tấm'],
           ['6', 'Đặt nắp lên thân, kẹp, khoan lỗ chốt bản lề XUYÊN cả hai (match-drill)'],
           ['7', 'Tháo, vét sạch, lắp chốt gỗ; kiểm mở 180° và đồng phẳng vành'],
           ['7b', f'Bào CHUNG hai mép giáp nhau của hai cánh xuống khe {B.SEAM:.1f} — '
                  f'khe do một lượt bào tạo ra, không do hai bề rộng cộng lại'],
           ['8', 'Phay hốc nam châm bằng dưỡng, dán nam châm, kiểm lực tách'],
           ['9', f'Hoàn thiện; dán {S["FELT_PAD_N"]:.0f} miếng nỉ {B.FELT_PAD:.1f} dưới nắp '
                  f'(RỜI, không trải kín); lắp khay']]
    t3, yy3 = table(x0 + 760, yy + 44, ['#', 'BƯỚC'], seq, 720, rh=22, fs=10, colw=[46, 674])
    o.append(t3)
    o.append(t)
    # --- bang kiem xuat xuong (co o tich)
    yq = max(yy2, yy3) + 40
    o.append(T(x0, yq - 10, 'BẢNG KIỂM XUẤT XƯỞNG — điền cho từng hộp',
               font_size=15, font_weight='bold', fill=INK))
    chk = [['Phủ bì X', f'{S["X_OA"]:.1f} ±0,5'], ['Phủ bì Y', f'{S["Y_OA"]:.0f} ±0,5'],
           ['Phủ bì Z (nắp đóng)', f'{S["Z_OA"]:.0f} ±0,5'],
           ['Khe ráp giữa hai cánh', f'{B.SEAM:.1f} ±{B.SEAM_TOL:.2f} (đo 3 điểm)'],
           ['Khe quanh lòng tấm Nu', f'{B.PAN_REV:.1f} ±{B.PAN_REV_TOL:.2f} (đo 4 cạnh × 2 cánh)'],
           ['Đồng phẳng tấm Nu ↔ khung', '≤ 0,15'],
           ['Góc mở nắp', '180° +0 / −1°'],
           ['Cánh mở nằm ngang, mặt trên bằng vành', f'Z{Z_RIM:.0f} ±0,3'],
           ['Lực tách nắp (tổng 8 cặp)',
            f'≥ {S["MAG_TOTAL"]:.0f} N (nỉ đã tiêu {S["FELT_FORCE"]:.0f} N)'],
           ['Khe hở vào tay hốc âm', f'{S["GRIP_APER"]:.2f} +0,5 / 0 (đo 2 bên)'],
           ['Khay quân vào/ra không kẹt', 'đủ 4 khay'],
           ['AC-01 nhấc ra được bằng 2 hõm ngón', 'đạt'],
           ['Đủ 152 quân', f'{4*36} trong khay + 8 rãnh Joker = 152'],
           ['Hốc dự phòng còn trống', 'chứa được 4 quân thừa'],
           ['Nắp che ổ xúc xắc so với vành AC-01', 'thấp hơn 0..0,25 — KHÔNG nhô'],
           ['Nắp đóng kín, không kênh (nỉ đã nén)', f'khe ráp giữa đều {B.SEAM:.1f} suốt 350'],
           [f'Đủ {S["FELT_PAD_N"]:.0f} miếng nỉ {B.FELT_PAD_SZ[0]:.0f}×{B.FELT_PAD_SZ[1]:.0f}, '
            f'1 miếng trên nắp che', 'đạt'],
           ['Lấy được xúc xắc bằng khe luồn ngón', 'cả 4 ổ'],
           ['Không chi tiết kim loại nào ở bản lề', 'đạt']]
    rows_q = [[c[0], c[1], '☐  đạt', '', ''] for c in chk]
    tq, _ = table(x0, yq, ['MỤC KIỂM', 'TIÊU CHÍ', 'KẾT QUẢ', 'TRỊ SỐ ĐO', 'NGƯỜI KIỂM'],
                  rows_q, 916, rh=22, fs=10, colw=[276, 250, 90, 180, 120])
    o.append(tq)
    notes = ['Mọi trị số trong bộ bản vẽ này sinh từ tools/box_spec.py. Sửa số bằng tay là sai quy trình.',
             'Bước 6 — khoan lỗ chốt bản lề khi thân và nắp đã kẹp với nhau — là điều kiện để hai cánh đồng phẳng.',
             'Không phép thử nào ở bảng trên được bỏ qua để kịp tiến độ.']
    return sheet('QA-01', 'DUNG SAI · KIỂM · LẮP', '—', '—', '—', 8, N_SH,
                 ''.join(o), notes=notes)
SHEETS.append(('QA-01-dung-sai-kiem', sheetQA01))

# ==========================================================================
# XUAT
# ==========================================================================
def main():
    os.makedirs('build/ban-ve', exist_ok=True)
    pages = []
    for name, fn in SHEETS:
        svg = fn()
        open(f'build/ban-ve/{name}.svg', 'w').write(svg)
        pages.append(svg)
        print(f'  build/ban-ve/{name}.svg')
    html = ['<!doctype html><meta charset="utf-8"><style>',
            '@page { size: 420mm 297mm; margin: 0 }',
            'html,body{margin:0;padding:0;background:#fff}',
            '.p{width:420mm;height:297mm;overflow:hidden;page-break-after:always;'
            'display:block}',
            '.p:last-child{page-break-after:auto}',
            '.p svg{width:420mm;height:297mm;display:block}',
            '</style>']
    for svg in pages:
        html.append('<div class="p">' + svg + '</div>')
    open('build/ban-ve.html', 'w').write(''.join(html))
    print(f'  build/ban-ve.html  ({len(pages)} tờ)')

if __name__ == '__main__':
    main()
