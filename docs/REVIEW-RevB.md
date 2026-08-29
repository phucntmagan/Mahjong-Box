# Review bản vẽ sản xuất — Hộp Mahjong 152 quân, Rev B

> **Trạng thái 29-08-2026.** Đây là bản review gốc của Rev B, giữ nguyên làm hồ sơ. Bốn kết luận trong đây
> đã thay đổi: §2.3 (đề xuất hốc nhấc khay không đóng được), §3.2 (mép tự do nắp không còn cần chi tiết đỡ),
> §8.1 (phần CITES đã tra lại, xem `tools/cites_check.py`), và toàn bộ chuỗi kích thước.
> Số hiện hành: **`docs/CHOT-REV-C.md`** và **`docs/BX-01.md`**.

**Tài liệu được review:** `Ban_ve_san_xuat_hop_Mahjong_152_quan_RevB.pdf` (BURLORA, 6 sheet, Rev B 24-08-2026)
**Phạm vi:** kiểm tra độc lập toàn bộ chuỗi kích thước, dung sai, sức chứa và tính khả thi chế tạo.
**Công cụ kiểm tra:** `tools/check_dimensions.py` (chạy lại được, không phụ thuộc thư viện ngoài).

**Kết luận tổng quát:** số học của Rev B **đúng toàn bộ** — 0 lỗi tính. Nhưng có **5 vấn đề hình học/công năng** đủ nghiêm trọng để phải giải quyết trước khi lập trình CNC, cộng 2 chi tiết công năng bị bỏ sót so với ảnh mẫu và 1 rủi ro độ ẩm có thể làm nắp kẹt cứng.

---

## 1. Phần đã verify — tất cả đều đúng

| # | Hạng mục | Rev B ghi | Tính lại | |
|---|---|---|---|---|
| 1 | Quân 1 × 1-7/16 × 7/16 in | 25,4 × 36,51 × 11,11 | 25,400 × 36,512 × 11,113 | ✅ |
| 2 | Chuỗi X thân hộp | 10+126+6+70+6+126+10 = 354 | 354 | ✅ |
| 3 | Chuỗi Y thân hộp | 10+330+10 = 350 | 350 | ✅ |
| 4 | Khe khay quân | 1,0 mỗi bên / 2,5 mỗi đầu | (126−124)/2 = 1,0 ; (330−325)/2 = 2,5 | ✅ |
| 5 | Khe giữa 12 cột, quân max 25,7 | ≥ 0,42 | 0,418 | ✅ |
| 6 | Khe giữa 3 hàng, quân max 36,8 | ≥ 0,80 | 0,800 | ✅ |
| 7 | Mép khay cao hơn quân max | 2,8 | 19 − 4,0 − 0,8 − 11,4 = 2,800 | ✅ |
| 8 | Lòng Joker | 4×36,8 + 3×0,4 + 2×0,8 = 150 | 150,000 | ✅ |
| 9 | Chuỗi dài AC-01 | 5+150+5+75+5+80+5 | 325 | ✅ |
| 10 | Góc vát mặt dưới nắp | 3,24° | atan(10/176,7) = 3,239° | ✅ |
| 11 | Nắp khép về phủ bì | 2×176,7 + 0,6 | 354,0 | ✅ |
| 12 | Stack dung sai nắp | ±0,8 | 2×(±0,3) + (±0,2) = ±0,8 | ✅ |
| 13 | Chiều dài mộng hoạt động | 7×44 + 6×1 = 314 | 314 | ✅ |
| 14 | Phủ bì Z tại mộng | 2+60+18 = 80 | 80 | ✅ |
| 15 | Phủ bì Z tại khe giữa | 2+70+8 = 80 | 80 | ✅ |
| 16 | Sức chứa | 4×36 + 8 = 152 | 152 | ✅ |

Chuỗi dung sai ở mục 12 đặc biệt đáng ghi nhận — hiếm bản vẽ nào ở giai đoạn này đã cộng stack.

---

## 2. Năm vấn đề phải sửa

### 2.1 — Chiều cao 80 mm dư 14–24 mm khoảng rỗng; khay sẽ xóc khi vận chuyển

Dựng lại chuỗi Z (Z = 0 tại mặt bàn):

```
chân 2 + đáy 8                     → sàn trong          Z10
2 khay chồng × 19                  → đỉnh khay          Z48
vành thân tại mộng    = 2 + 60     → mặt dưới nắp       Z62   ⇒ RỖNG 14 mm
vành thân tại khe giữa= 2 + 70     → mặt dưới nắp       Z72   ⇒ RỖNG 24 mm
```

14–24 mm này **không được giao nhiệm vụ trong BOM**, không có chốt/khóa nắp (sheet 1 tự nhận đã hoãn), không có chi tiết nào ép khay xuống. Hộp bị nghiêng hoặc xóc trong vận chuyển là 152 quân + 4 xúc xắc va vào nhau và vào lớp hoàn thiện.

**Phương án A — hạ chiều cao (khuyến nghị):**

```
vành thân tại mộng     = Z48 + khe 1,0 = Z49  → thân cao 47
mặt ngoài nắp          = Z49 + 18      = Z67  → PHỦ BÌ 354 × 350 × 67
mặt dưới nắp tại khe giữa = 67 − 8     = Z59  → thân cao tại khe giữa 57
góc vát bù trên đỉnh thân = 3,239°  (khớp đúng góc nắp)
```

Giảm 13 mm chiều cao trên diện tích 354 × 350 — tiết kiệm gỗ đáng kể và tỷ lệ hộp thanh hơn.

**Phương án B — giữ 80 mm** nhưng giao nhiệm vụ rõ ràng cho 14 mm: khăn trải da lộn + 4 nút chỉ gió + sách luật, kèm chi tiết ép khay.

Lưu ý: dù chọn phương án nào, nắp hình nêm + khay đáy phẳng **luôn** sinh khoảng rỗng hình nêm. Với Rev C, khe còn lại dưới mặt nắp trên khoang khay trái là:

| X (mm từ mộng) | 10 | 50 | 90 | 136 | 177 |
|---|---|---|---|---|---|
| Mặt dưới nắp (Z) | 49,57 | 51,83 | 54,09 | 56,70 | 59,02 |
| Hở trên đỉnh khay (Z48) | 1,57 | 3,83 | 6,09 | 8,70 | 11,02 |

Phần rỗng phía trong vẫn cần đệm mềm hoặc khăn phủ.

### 2.2 — Không có sheet nào vẽ thân hộp BX-01

Bộ 6 sheet gồm GA-01, GA-02, TR-01, AC-01, HD-01, QA-01. **Chi tiết quan trọng nhất — thân hộp — chỉ tồn tại dưới dạng một chuỗi kích thước trên mặt bằng GA-02.**

Thiếu: dung sai của chính các khoang (126 / 70 / 330), mặt cắt có dung sai vách và đáy, vị trí mắt mộng so với chuẩn, vị trí chân đệm, vị trí hốc nhấc tay.

Hệ quả trực tiếp: QA-01 yêu cầu *"khe khay trong khoang 1,0 ±0,3 mỗi bên"*, nhưng riêng khay đã ±0,25 (= ±0,125 mỗi bên) — phần dung sai còn lại phải dồn hết vào khoang, mà khoang **chưa hề được dung sai hóa**. Yêu cầu này không truy nguyên được.

**Phải làm:** thêm 1 sheet BX-01, và ghi rõ khoang **126 +0,4/0**, **70 +0,4/0**, **330 +0,5/0**.

Ngoài ra QA-01 bước 3 ghi *"khóa chuẩn A/B/C"* nhưng **A/B/C chưa được định nghĩa ở bất kỳ đâu** — chỉ có "DATUM A" của mặt ngoài nắp trên HD-01.

### 2.3 — Không lấy được khay ra khỏi hộp

Khay hở 1,0 mm mỗi bên và 2,5 mm mỗi đầu — không luồn được ngón tay. Hốc nhấc tay 70 × 7 nằm **trên khay**, nhưng vách khoang chắn ngay bên cạnh nên hốc đó vô dụng. AC-01 thì không có hốc nào cả, lại là chi tiết nặng nhất (cao 38).

**Phải làm:** phay **hốc lõm 70 × 10 sâu trên vành khoang của thân**, trùng vị trí hốc trên khay → mở được ~17 mm để kẹp. Bổ sung hốc tương tự cho AC-01.

Rãnh Joker cũng bị y hệt: sâu 24,5 mm mà quân chỉ hở 2,3 mm bề ngang → không nhặt được, phải lật úp cả khay. **Thêm hõm ngón bán nguyệt Ø25 × sâu 12** vào dải gỗ 15 mm bên hông rãnh (còn lại 3 mm + 5 mm vách ngoài = 8 mm gỗ, đủ bền vì hõm chỉ dài 25/150 mm).

### 2.4 — Chốt gỗ Ø6 × 322: vừa không khoan được, vừa sẽ gãy

- Độ mảnh **54 : 1** cho một thanh gỗ Ø6.
- Mũi khoan Ø6,35 dài 322 mm thực tế không có sẵn; khoan từ hai đầu thì phá yêu cầu đồng trục 0,15/322.
- Khe lỗ Ø6,35 / chốt Ø6,00 = **0,35–0,40 mm đường kính** — quá lỏng cho bản lề, cánh sẽ rơ và xệ.

**Phải làm — 2 chốt Ø6 × 160 cho mỗi cánh**, đóng từ hai đầu, gặp nhau bên trong mắt mộng số 4:

| Mắt mộng | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| Thuộc về | THÂN | NẮP | THÂN | **NẮP** | THÂN | NẮP | THÂN |
| Vị trí (mm) | 0–44 | 45–89 | 90–134 | **135–179** | 180–224 | 225–269 | 270–314 |

Chốt A: −4 → 156 (ăn 21 mm vào mắt 4). Chốt B: 318 → 158 (ăn 21 mm vào mắt 4). Khe hở giữa hai chốt 2 mm, nằm gọn trong mắt mộng → **khớp vẫn liên tục, hai chốt không va nhau**. Khoan chỉ còn 165 mm mỗi đầu (mũi tiêu chuẩn làm được), đồng trục chỉ phải giữ trong từng nửa. Số nút bịt CP-01 vẫn là 4.

Đồng thời siết khe chốt về **Ø6,20 +0,05/0** (khe 0,20–0,25 mm).

### 2.5 — Chưa giải quyết động học mở 180°

HD-01 ghi *"góc mở 180° ±2°"* nhưng **không định nghĩa cao độ trục xoay so với mặt bàn**, cũng không nói cánh mở ra thì tựa vào đâu.

Nếu trục nằm giữa bề dày nắp tại mộng (Z ≈ 71), mở 180° sẽ khiến cánh **treo lơ lửng ở Z62**: toàn bộ trọng lượng, đòn bẩy 176,7 mm, dồn lên một chốt gỗ Ø6 qua 3 mắt mộng — chỉ **132/350 mm (38 %)** chiều dài cánh có mắt mộng chịu lực.

Ảnh mẫu cho thấy hai cánh mở ra **nằm phẳng trên mặt bàn**, tức trục phải rất thấp. Bố trí hiện tại không cho ra kết quả đó.

**Đây là điểm phải chốt bằng một bản vẽ động học riêng trước mọi thứ khác** — vị trí trục quyết định lại biên dạng mộng, bề dày nắp và cả chiều cao thân.

---

## 3. Hai chi tiết công năng bị bỏ sót so với ảnh mẫu

### 3.1 — Cánh nắp trong ảnh là khay lõm có lót da

Ảnh 1 và ảnh 3 cho thấy rõ hai cánh mở ra là **khay lõm, lót da (dải vàng/cam)** — đó là khay bỏ bài / tính điểm của người chơi, và chính là thứ khiến cánh nắp có ích khi mở.

Rev B mô hình hóa cánh nắp là **nêm gỗ đặc, không có lòng lõm**. Ở mép tự do dày 8 mm thì không phay lòng được.

**Giải:** phay lòng **~100 × 330 sâu 6** chỉ trong nửa dày của cánh (vùng còn dày ≥ 12 mm, tức từ phía mộng ra 106 mm), lót da dê. Đáy lòng còn 4–8 mm.

### 3.2 — Mép tự do dày 8 mm dài 350 mm không có gì đỡ ở giữa

Khi đóng, hai cánh chìa ra 176,7 mm và gặp nhau qua khe 0,6 mm **ngay trên khoang phụ kiện rộng 70 mm — chỗ hoàn toàn rỗng**. Hai đầu cánh chỉ tì vào vách trước và vách sau, nhịp hở 330 mm. Ấn tay vào giữa nắp là hai đầu cánh võng xuống và cào vào nhau.

**Giải (một chi tiết xử lý ba vấn đề):** cho AC-01 một **sống nổi giữa chạy suốt 325 mm, rộng 12–16 mm**, cao đúng tới mặt dưới nắp tại khe giữa — **11 mm** trên vành khay nếu theo phương án hạ chiều cao ở §2.1. Sống này:

1. đỡ hai đầu cánh nắp suốt chiều dài,
2. ép khay xuống, triệt tiêu xóc,
3. làm tay nắm để rút AC-01 ra (giải luôn §2.3 cho khay này).

Bọc nỉ 0,8 mm trên đỉnh sống để nắp đóng êm và hấp thụ sai lệch.

---

## 4. Ba con số nên đổi

### 4.1 — Rãnh Joker 150 → 152; khoang phụ 80 → 78

Rãnh Joker đang dùng **triết lý khe khác hẳn** khay quân: biên 0,8 / khe 0,4, so với biên 1,0 / khe 0,75 của khay quân. Cùng một loại quân, cùng một hộp, mà hai tiêu chuẩn.

Hệ quả — nếu lô quân về +0,5 mm so với danh nghĩa:

| Trường hợp lô quân | Khe khay quân | Khe rãnh Joker (biên 1,0) |
|---|---|---|
| Danh nghĩa | 0,745 | 0,650 |
| Rev B max (+0,3) | 0,418 | 0,267 |
| Lô thực tế +0,5 | 0,200 | **−0,016 — không nhét được** |

Đổi rãnh Joker sang **152**, khoang phụ sang **78**: chuỗi vẫn khép đúng `5+152+5+75+5+78+5 = 325`, và kể cả lô +0,5 vẫn còn khe 0,651.

### 4.2 — Giao nhiệm vụ cho khoang phụ 58 × 78

Khoang phụ 58 × 80 × sâu 18,5 hiện **không có nội dung nào trong BOM** — một khoảng trống chưa được giao việc.

**Đề xuất:** 4 quân trắng dự phòng xếp 2 × 2 nằm ngang. Cần 51,4 × 73,6 mm (quân max) hoặc 51,8 × 74,0 mm (lô +0,5) — vừa khít trong 58 × 78. Sâu 11,4 ≤ 18,5. Bộ thành **156 quân**, đúng cấu hình chuẩn thị trường Mỹ.

### 4.3 — Hốc xúc xắc: 4 ổ riêng thay vì một ngăn rỗng

Hốc 58 × 75 × 18,5 để 4 viên xúc xắc chạy tự do sẽ va sứt lớp hoàn thiện và va vào quân. Làm **4 ổ 18 × 18 sâu 12 dạng 2 × 2**, mỗi ổ có hõm ngón — đúng như bố trí thấy trong ảnh 3.

---

## 5. Rủi ro độ ẩm — chỗ nguy hiểm nhất của cả bộ bản vẽ

QA-01 ghi *"độ ẩm 8–10 %"* mà **không nói khí hậu đích**. 8–10 % EMC tương ứng ~40–50 % RH (phòng điều hòa / ôn đới). Môi trường Việt Nam không điều hòa là 12–14 % EMC.

Giãn nở tiếp tuyến gỗ cứng ≈ 0,20 % trên mỗi 1 % thay đổi MC:

| Kích thước | ΔMC 2 % | ΔMC 3 % | ΔMC 5 % |
|---|---|---|---|
| Một cánh nắp ngang thớ, 176,7 | 0,71 | **1,06** | 1,77 |
| Thân ngang 350 | 1,40 | 2,10 | 3,50 |
| Khoang khay rộng 126 | 0,50 | 0,76 | 1,26 |
| Lòng khay rộng 114 | 0,46 | 0,68 | 1,14 |

**Với ΔMC = 3 %, hai cánh nắp nở về phía khe giữa tổng cộng 2 × 1,06 = 2,12 mm — trong khi khe chỉ có 0,6 mm. Nắp sẽ kẹt cứng, hoặc tự cạy bung mộng.**

Ghi chú *"khuyến nghị panel floating hoặc veneer trên lõi ổn định"* ở QA-01 phải chuyển từ **khuyến nghị** thành **yêu cầu bắt buộc** — hoặc đó, hoặc mở khe giữa lên ≥ 2,5 mm (xấu về thẩm mỹ).

Cùng lý do: mép 8 mm dài 350 mm bằng gỗ đặc chắc chắn cong vênh. Yêu cầu phẳng **0,50/300** trên một nêm gỗ đặc vát tới 8 mm là **không đạt được**; trên lõi ổn định + veneer thì đạt.

**Ngoài ra:** chốt định vị độ ẩm phải ghi theo **thị trường đích**, không phải theo xưởng. Nếu bán nội địa Việt Nam không điều hòa, làm ở 8 % là sai chiều — mọi khe sẽ đóng lại.

---

## 6. Dung sai nắp: nên chuyển sang dung sai quan hệ

Stack ±0,8 tính đúng, nhưng **thân cũng là 354 ±0,8**. Trường hợp xấu: thân 354,8 và nắp 353,2 → lệch 1,6 mm, viền nắp thụt vào **0,8 mm mỗi bên** — nhìn thấy rõ trên một sản phẩm cao cấp.

**Phải làm:** dung sai hóa **quan hệ**, không phải hai trị tuyệt đối độc lập. Ghi *"đồng mép nắp–thân ±0,3, lắp theo thân thực tế"* và đưa cánh nắp vào công đoạn **match-fit** cuối chuyền (cắt theo thân đã hoàn thiện), thay vì gia công độc lập theo cote.

---

## 7. Thiếu trong BOM và QA

| Thiếu | Ghi chú |
|---|---|
| Nỉ | 5 miếng (4 khay quân + AC-01), không có dòng nào trong BOM |
| Da lót cánh nắp | Xem §3.1 |
| **Loại hoàn thiện** | QA-01 chỉ ghi chà tới P320 rồi nói *"không để sơn làm giảm khe"* — sơn gì? Dầu? Shellac? PU? |
| Xúc xắc | Có hốc chứa nhưng không có dòng BOM |
| Nút chỉ gió / đánh dấu nhà cái | Không có |
| Định nghĩa chuẩn A/B/C | QA-01 bước 3 tham chiếu nhưng chưa định nghĩa |
| Khóa / chốt đóng nắp | Sheet 1 tự nhận đã hoãn — nhưng ràng buộc "không kim loại" khiến đây là bài toán khó, cần giải sớm |

**Lưu ý riêng cho cocobolo:** gỗ nhiều dầu, **bắt buộc lau acetone hoặc cồn ngay trước khi phủ**, nếu không lớp hoàn thiện sẽ không bám. Bụi cocobolo là chất gây mẫn cảm da và hô hấp mạnh — cần ghi cảnh báo bảo hộ cho xưởng lên bản vẽ.

---

## 8. Hai điểm ngoài kỹ thuật nhưng ảnh hưởng trực tiếp

### 8.1 — CITES

Cocobolo (*Dalbergia retusa*) và gỗ trắc (*Dalbergia* spp.) đều thuộc **Phụ lục II CITES** — toàn bộ chi *Dalbergia* đã bị liệt kê từ CoP17 (2017). Annotation #15 sau CoP19 có miễn trừ cho **thành phẩm với khối lượng gỗ loài liệt kê ≤ 10 kg mỗi lô hàng**. Hộp này ước tính ~3–4 kg gỗ, nên **2 hộp một lô đã vượt ngưỡng miễn trừ**.

Nếu có xuất khẩu, cần giấy phép CITES.

> ⚠️ Phần này viết theo trí nhớ và **annotation #15 có thể đã thay đổi tại CoP20**. Bắt buộc kiểm tra bản hiện hành với Cơ quan quản lý CITES Việt Nam trước khi chốt vật liệu — đây là rủi ro pháp lý, không phải rủi ro kỹ thuật.

### 8.2 — Rack không vào được hộp

Sheet 1 đã tự ghi *"chưa tính khoang rack 18,5–19 inch"*. Nói rõ hơn: rack Mahjong Mỹ dài 14–19 inch **không bao giờ vào được hộp 354 mm (13,9 inch)** — đây không phải chuyện hoãn lại mà là bất khả thi ở kích thước hiện tại.

Hoặc bán rack rời, hoặc định vị sản phẩm là bộ kiểu Trung/Nhật (không dùng rack). Cần quyết định vì nó ảnh hưởng tới cách mô tả sản phẩm.

---

## 9. Thứ tự xử lý đề nghị cho Rev C

| # | Việc | Chặn cái gì |
|---|---|---|
| 1 | Chốt động học bản lề (§2.5) | Quyết định lại biên dạng mộng, bề dày nắp, chiều cao thân |
| 2 | Chốt chiều cao: 67 hay giữ 80 (§2.1) | Toàn bộ chuỗi Z, chiều cao sống giữa AC-01 |
| 3 | Chốt cấu tạo nắp: veneer/lõi ổn định (§5) + lòng lõm lót da (§3.1) | Cấu tạo cánh, khe giữa, yêu cầu phẳng |
| 4 | Vẽ sheet BX-01 + dung sai khoang (§2.2) | Lập trình CNC |
| 5 | Hốc nhấc tay trên thân + hõm ngón rãnh Joker (§2.3) | Lập trình CNC |
| 6 | 2 chốt × 160, lỗ Ø6,20 (§2.4) | Gá khoan |
| 7 | Rãnh Joker 152 / khoang phụ 78 / ổ xúc xắc (§4) | Lập trình CNC |
| 8 | Chuyển sang dung sai quan hệ + match-fit nắp (§6) | Quy trình chuyền |
| 9 | Bổ sung BOM, định nghĩa chuẩn A/B/C, chốt hoàn thiện (§7) | Duyệt mẫu vàng |
| 10 | Xác minh CITES (§8.1) | Chốt vật liệu |

**Điểm khóa của Rev B vẫn giữ nguyên giá trị và phải làm trước tất cả:** đo tối thiểu 20 quân thuộc đúng lô mua, lấy trị lớn nhất theo 3 trục. Nếu lô vượt 25,7 × 36,8 × 11,4 mm thì phải hiệu chỉnh lòng khay — và như §4.1 chỉ ra, rãnh Joker là chỗ hỏng đầu tiên.
