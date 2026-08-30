#!/usr/bin/env python3
"""
PHA THU LUOI TU KIEM.

Mot tu kiem khong bao giu duoc gi neu no khong the noi. Ho so nay da hai lan
viet phai cai luoi khong bao gio no:
  - Rev C1: dieu kien viet la REBATE_D > GRIP_D (6,1 > 16) — vinh vien sai, nen
    loi ha bac an mat tran hoc am lot qua;
  - va mot lan cong be day hai chi tiet nam o hai vi tri khac nhau roi ket luan
    thung vach.

Script nay lam nguoc lai: voi MOI dieu kien trong box_spec.selfcheck() ma ta
quan tam, no doi mot hang so cho hong DUNG cho do, roi doi hoi loi tuong ung
PHAI xuat hien. Neu doi hang so ma luoi van im, tuc dieu kien do la trang tri.

Chay: python3 tools/break_selfcheck.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B

# (nhan, {hang so: tri so hong}, chuoi PHAI xuat hien trong danh sach loi)
CASES = [
 # --- o xuc xac va nap che (to AC-02)
 ("truong o khong lot mieng hoc",   {'DICE_SOCK': 30.0},    "khong lot mieng hoc"),
 ("vanh do nap che qua hep",        {'DICE_SLOT': 15.0},    "vanh do nap che"),
 ("o nong hon xuc xac",             {'DICE_SOCK_D': 16.5},  "ho tren dau xuc xac"),
 ("dao phay qua to, kenh goc o",    {'DICE_MILL': 8.0},     "kenh goc o"),
 ("khe luon ngon hep hon dau ngon", {'DICE_SLOT': 11.0},    "khe luon ngon canh o rong"),
 ("xuc xac tut sang khe",           {'DIE': 12.0},          "tut sang khe"),
 ("xuc xac truot len bac",          {'DICE_STEP': 1.0},     "truot len bac"),
 ("ngon khong bam duoc suon",       {'DICE_STEP': 12.0},    "suon xuc xac"),
 ("day AC-01 duoi o qua mong",      {'AC_H': 26.0},         "day AC-01 duoi o xuc xac"),
 ("nap che khong tha vao duoc",     {'COVER_CLR': 0.0},     "khong tha vao duoc"),
 ("khe lap nho hon go no",          {'COVER_CLR': 0.2},     "khe lap nap che"),
 ("ni dem khong cham khay",        {'FELT_PAD': 0.9},      "khong ep duoc gi"),
 ("ni bi nen chai",                {'FELT_PAD': 1.3, 'CLR_Z': 0.8}, "chai va mat tinh dan hoi"),
 ("dem ni trai qua rong, nap khong dong", {'FELT_PAD_SZ': (40.0, 40.0)}, "nap khong dong duoc"),
 ("qua it mieng dem, khay van xoc", {'FELT_PAD_SZ': (6.0, 6.0)}, "khay van xoc duoc"),
 ("khong mieng ni nao tren nap che", {'FELT_PAD_Y': (115.0, 300.0)}, "nap che khong co gi giu"),
 ("mieng ni vat qua khe rap giua", {'FELT_PAD_X': (85.0, 189.0, 293.0)}, "vat qua khe rap giua"),
 ("dung sai cho nap che nho len",  {'COVER_T_TOL_HI': 0.1}, "nap NHO LEN"),
 ("hom ngon khong voi toi khe",     {'COVER_NOTCH': 12.0},  "voi qua vanh do"),
 ("hom ngon thoc vao o xuc xac",    {'COVER_NOTCH': 34.0},  "thoc qua khe luon ngon"),
 ("hom ngon rong hon khe",          {'COVER_NOTCH': 20.0},  "rong hon khe luon ngon"),
 ("canh nap che canh hom qua mong", {'COVER_NOTCH': 21.0},  "canh hom ngon"),
 # --- khe nhin thay tren mat nap (siet 30-08-2026)
 ("khe long tam duoi he so an toan", {'PAN_REV': 0.7},   "khe quanh long tam"),
 ("bo P5 thi ve kho song lai",      {'MC_STABILISED': False}, "lap o do am xuong"),
 ("khe rap giua dong o 5 %",        {'SEAM': 0.5},        "khe rap giua con"),
 ("do doc xe tiep tuyen thay vi xuyen tam",
                                    {'STILE_GRAIN': 'tiep tuyen'}, "khe rap giua con"),
 ("do doc mong, het go giua ranh va ong", {'STILE': 18.0}, "go dac giua ranh om tam"),
 ("khe long tam 0,8 khong song noi dung sai", {'PAN_REV': 0.8}, "truong hop xau"),
 ("dung sai khe long tam qua rong", {'PAN_REV_TOL': 0.25}, "truong hop xau"),
 ("dung sai khe rap giua qua rong", {'SEAM_TOL': 0.25},   "khe rap giua o truong hop xau"),
 ("lop hoan thien day (son phu)",  {'FINISH_T': 0.3},     "truong hop xau"),
 # --- vai dieu kien cu, de chung minh cai khung nay khong tu bia ra ket qua
 ("thanh go quanh lo chot",         {'KN_WALL': 1.5},       "thanh go quanh lo chot"),
 ("bo mep tran hoc am qua nho",     {'GRIP_R': 2.0},        "bo mep tran qua nho"),
 ("mong day rut khoi ranh",         {'BOT_TON': 2.5},       "ngam"),
]

def run(patch):
    old = {k: getattr(B, k) for k in patch}
    try:
        for k, v in patch.items():
            setattr(B, k, v)
        return B.selfcheck(B.derive())
    finally:
        for k, v in old.items():
            setattr(B, k, v)

print("=" * 78)
print("PHA THU LUOI TU KIEM — moi hang loi PHAI no")
print("=" * 78)
base = B.selfcheck(B.derive())
print(f"  Dac ta nguyen ven: {'DAT' if not base else 'LOI — ' + str(base)}")
if base:
    raise SystemExit(1)
print()
bad = 0
for label, patch, want in CASES:
    errs = run(patch)
    hit = [x for x in errs if want in x]
    ok = bool(hit)
    if not ok:
        bad += 1
    ptxt = ", ".join(f"{k}={v}" for k, v in patch.items())
    print(f"  [{'NO ' if ok else 'IM '}] {label:34s} {ptxt:22s}")
    if ok:
        print(f"         -> {hit[0]}")
    else:
        print(f"         -> KHONG NO. Loi thu duoc: {errs if errs else '(khong co)'}")
print()
print(f"  {len(CASES) - bad}/{len(CASES)} dieu kien no dung cho. "
      + ("Luoi that." if not bad else "CO DIEU KIEN TRANG TRI."))
raise SystemExit(1 if bad else 0)
