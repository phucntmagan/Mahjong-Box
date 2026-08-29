#!/usr/bin/env python3
"""
Xac minh CITES cho hai loai go cua hop: Dalbergia retusa (cocobolo, than va
khung nap) va Afzelia xylocarpa (Nu go do, tam nap).

Chay: python3 tools/cites_check.py

CACH DOC FILE NAY
  Cot NGUON ghi ro moi dieu duoi day den tu dau va do chac den dau:
    [S1] nhieu nguon thu cap doc lap trung khop, trich nguyen van dieu khoan
    [S2] mot nguon thu cap, hoac dien giai
    [??] chua xac minh duoc
  KHONG dong nao o day duoc kiem tu cites.org. Trong moi truong chay session
  nay, cites.org / fws.gov / bada.org / legislation.gov.uk / speciesplus.net
  deu bi chan o tang proxy. Toan bo la nguon thu cap qua cong cu tim kiem.
  => Truoc khi ky hop dong mua go hoac lam thu tuc xuat, phai doi chieu voi
     ban Phu luc hien hanh tren cites.org va voi Co quan quan ly CITES VN.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B

S = B.derive()
def hr(t): print("\n" + "="*78 + "\n" + t + "\n" + "="*78)

# ============================================================== dieu da tra
FACTS = [
 ("S1", "Dalbergia", "Dalbergia spp. (tru D. nigra o Phu luc I) nam PHU LUC II,"
                     " chu giai #15. Ban hien hanh co hieu luc tu 23-02-2023."),
 ("S1", "Dalbergia", "#15 loai tru: (a) la, hoa, phan hoa, qua, hat;"
                     " (b) THANH PHAM voi khoi luong go loai duoc liet ke toi da"
                     " 10 kg moi lo hang; (c) nhac cu hoan chinh, bo phan va phu"
                     " kien nhac cu hoan chinh; (d) D. cochinchinensis theo #4;"
                     " (e) Dalbergia xuat tu Mexico theo #6."),
 ("S1", "Dalbergia", "CoP19 (2022) DA DOI muc (b) tu 'xuat khau phi thuong mai'"
                     " sang 'thanh pham'. Day la thay doi CO LOI va la ly do ban"
                     " ghi trong docs (viet theo tri nho) van dung ve con so 10 kg."),
 ("S1", "Dalbergia", "CoP20 (Samarkand, 24-11 -> 05-12-2025) KHONG sua #15."
                     " CoP20 thong qua bao cao tac dong cua mien tru Dalbergia/"
                     "Guibourtia va khang dinh mien tru (c) la hop ly."),
 ("S1", "chung",     "Sua doi Phu luc cua CoP20 co hieu luc 05-03-2026."),
 ("S1", "Dalbergia", "DIEN GIAI nguong 10 kg (phan Interpretation cua Phu luc,"
                     " va Notification to the Parties 2023/005): nguong tinh"
                     " RIENG cho tung loai duoc chu giai, va tinh tren khoi luong"
                     " go cua loai do trong TUNG MON HANG cua lo, KHONG cong don"
                     " ca lo va KHONG cong khoi luong cua cac loai khac nhau."),
 ("S1", "Afzelia",   "CoP19 dua QUAN THE CHAU PHI cua Afzelia spp. vao Phu luc II"
                     " voi chu giai #17, hieu luc 23-02-2023."),
 ("S1", "Afzelia",   "#17 = go tron, go xe, van lang, van dan va go da che bien."
                     " THANH PHAM khong nam trong pham vi #17."),
 ("S1", "Afzelia",   "CoP20 BAC hai de xuat loai Afzelia bipindensis va"
                     " Pterocarpus soyauxii chau Phi khoi Phu luc II"
                     " -> danh sach chau Phi giu nguyen."),
 ("S2", "Afzelia",   "Afzelia xylocarpa (go do, chau A) KHONG co trong Phu luc"
                     " CITES. Khong tim thay de xuat nao o CoP20 them loai"
                     " Afzelia chau A."),
 ("S2", "Viet Nam",  "A. xylocarpa thuoc NHOM IIA trong nuoc. Nen phap ly la"
                     " Nghi dinh 06/2019/ND-CP sua boi 84/2021/ND-CP; co dau hieu"
                     " danh muc hien hanh da chuyen sang Thong tu 85/2025/TT-BNNMT."),
 ("??", "Dalbergia", "Dinh nghia chinh xac cua 'thanh pham' (finished product)"
                     " trong phan Interpretation — quan trong vi no quyet dinh"
                     " hop ban le co duoc mien tru hay khong."),
 ("??", "Viet Nam",  "Thu tuc va ho so Nhom IIA cho viec MUA va van chuyen noi dia"
                     " Nu go do; va lieu Thong tu 85/2025 co doi gi khong."),
]

hr("1. DA XAC MINH DUOC GI")
print(f"  {'':4s}{'loai':11s}noi dung")
for src, tax, txt in FACTS:
    body = txt.split(' ')
    line, out = "", []
    for w in body:
        if len(line) + len(w) + 1 > 60:
            out.append(line); line = w
        else:
            line = (line + " " + w).strip()
    out.append(line)
    print(f"  [{src}] {tax:11s}{out[0]}")
    for x in out[1:]:
        print(f"  {'':4s} {'':11s}{x}")

# ============================================================== hau qua
hr("2. HAU QUA CHO HOP NAY — DALBERGIA (cocobolo)")
print(f"  Hop chot: phuong an {S['HANDLE']}, phu bi {S['W']:.0f} x {S['Y_OA']:.0f}"
      f" x {S['Z_OA']:.0f}\n")
print(f"  {'cau tao khay':16s}{'Dalbergia/hop':>15s}{'/ 10 kg':>10s}   ket qua")
for khay in ('cocobolo', 'loi on dinh'):
    d = B.dalbergia_of(S, khay)
    print(f"  {khay:16s}{d:15.2f}{d/B.CITES_LIMIT*100:9.0f} %   "
          f"{'MOI HOP deu duoi nguong' if d < B.CITES_LIMIT else 'VUOT nguong'}")
print()
print("  Hai cach doc nguong, va hai ket qua khac han nhau:")
print(f"  {'':4s}{'cach doc':34s}{'khay cocobolo':>16s}{'khay loi o.d.':>16s}")
for lbl, per_item in [("A. cong don ca lo (ban docs cu doc)", False),
                      ("B. tinh tung mon hang (dien giai)", True)]:
    row = []
    for khay in ('cocobolo', 'loi on dinh'):
        d = B.dalbergia_of(S, khay)
        row.append("khong gioi han" if per_item else f"{int(B.CITES_LIMIT//d)} hop/lo")
    print(f"  {'':4s}{lbl:34s}{row[0]:>16s}{row[1]:>16s}")
print()
print("  => Neu dien giai [S1] o muc 1 dung, thi 'so hop moi lo hang' KHONG CON")
print(f"     LA RANG BUOC. Moi hop la mot mon hang, chua {B.dalbergia_of(S,'cocobolo'):.2f} kg"
      f" cocobolo — duoi 10 kg —")
print("     nen ca lo bao nhieu hop cung duoc mien tru.")
print("  => Bang 'so hop moi lo' trong docs/QUAI-XACH.md va docs/NAP-GO-DAC.md")
print("     duoc viet theo cach doc A. Phai sua lai, va phai ghi ro do la mot")
print("     DIEN GIAI chua duoc xac nhan bang van ban goc.")
print()
print("  CANH BAO — dieu kien cua mien tru khong phai chi la khoi luong:")
print("   - Phai la THANH PHAM. Hop rap roi, hoan thien, dong goi ban le thi hop le;")
print("     gui chi tiet roi cho ben kia rap thi KHONG. Dinh nghia chinh xac chua tra duoc.")
print("   - Mien tru la mien GIAY PHEP CITES, khong mien luat go cua nuoc nhap")
print("     (EUDR o EU, Lacey Act o My deu doi ho so nguon goc rieng).")

hr("3. HAU QUA CHO HOP NAY — AFZELIA (Nu go do, tam nap)")
nu = S['V']['tam Nu']/1e6*B.RHO['Nu go do']
print(f"  Nu go do moi hop: {nu:.2f} kg (2 tam {S['PAN_W']:.1f} x {S['PAN_L']:.0f}"
      f" x {B.PAN_T:.0f})\n")
for t in ["A. xylocarpa la loai CHAU A. Chu giai CITES chi phu quan the CHAU PHI"
          " cua chi Afzelia.",
          "Ngay ca voi loai chau Phi, #17 chi phu go tron / go xe / van lang /"
          " van dan / go da che bien — mot cai hop hoan chinh khong nam trong do.",
          "=> CITES gan nhu chac chan KHONG cham toi tam nap. Hai lop bao ve,"
          " ca hai deu khong dinh."]:
    print(f"   - {t}")
print()
print("  NHUNG rang buoc that su nam o TRONG NUOC, khong o CITES:")
print("   ! Nhom IIA chi phoi viec KHAI THAC, MUA BAN va VAN CHUYEN noi dia.")
print("     Mua Nu go do phai co ho so lam san hop phap tu nguoi ban.")
print("   ! IUCN xep A. xylocarpa la Endangered. Do khong phai rang buoc phap ly,")
print("     nhung la rui ro thuong hieu neu ho so nguon goc khong sach.")

hr("4. CON PHAI TU DI HOI — danh sach cho nguoi, khong phai cho script")
for i, (who, what) in enumerate([
   ("Co quan quan ly CITES Viet Nam",
    "Ban Phu luc hien hanh sau 05-03-2026; van ban dien giai nguong 10 kg cua #15;"
    " Dalbergia retusa co dung dang o Phu luc II khong."),
   ("Co quan quan ly CITES nuoc NHAP",
    "Ho doc nguong 10 kg theo cach A hay cach B. Day la cho nguy hiem nhat:"
    " nuoc nhap co the doc chat hon nuoc xuat."),
   ("Chi cuc Kiem lam",
    "Thu tuc Nhom IIA cho A. xylocarpa; Thong tu 85/2025/TT-BNNMT co thay the"
    " danh muc cu khong."),
   ("Nguoi ban go",
    "Ho so nguon goc hop phap cho ca cocobolo lan Nu go do. Cocobolo nhap khau"
    " phai co giay phep CITES dau vao."),
   ("Luat su thuong mai / dai ly hai quan",
    "Dinh nghia 'thanh pham' ap dung cho san pham nay; va luat go cua thi truong"
    " dich (EUDR / Lacey Act)."),
], 1):
    print(f"  {i}. {who}")
    print(f"     {what}")

hr("5. TRANG THAI")
print("  Phan CITES trong docs truoc day viet theo tri nho. Sau lan tra nay:")
print("   - Con so 10 kg: DUNG.")
print("   - 'Thanh pham duoc mien tru': DUNG (CoP19 doi, truoc do chi phi thuong mai).")
print("   - 'Annotation #15 co the da doi o CoP20': KHONG DOI.")
print("   - 'Afzelia CoP18 dua quan the chau Phi vao PL II': gan dung, nhung la CoP19"
      " (2022) chu khong phai CoP18 (2019).")
print("   - '2 hop moi lo hang': CO THE SAI. Xem muc 2.")
print("\n  Muc do tin cay tong the: DU DE THIET KE TIEP, KHONG DU DE KY HOP DONG.")
