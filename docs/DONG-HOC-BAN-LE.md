# Động học bản lề — giải điểm treo §2.5

> Bản đầy đủ có hình: **`build/Dong-hoc-ban-le-Mahjong.pdf`**.
> Hình: `figs/fig8-dong-hoc-ban-le`. Tính toán: `tools/hinge_kinematics.py`.

## Kết luận

**Trục xoay P = (9 , 58)** — suy ra từ ràng buộc, không phải chọn.

Ống gỗ bán kính 9 phải tiếp tuyến cả mặt trên (Z67) lẫn mặt dưới (Z49) của nắp. Điều đó ép tâm ống
vào đúng một điểm: giữa bề dày nắp, cách mặt ngoài thân đúng một bán kính. Hết bậc tự do.

## Cánh mở ra nằm ở đâu

| Điểm | Đóng X | Đóng Z | Mở 180° X | Z |
|---|---:|---:|---:|---:|
| Mép mộng, mặt trên | 18,0 | 67,0 | 0,0 | 49,0 |
| Mép mộng, mặt dưới | 18,0 | 49,0 | 0,0 | 67,0 |
| Mép khe giữa, mặt trên | 176,7 | 67,0 | −158,7 | 49,0 |
| Mép khe giữa, mặt dưới | 176,7 | 55,0 | −158,7 | 61,0 |
| Đáy sống khóa | 154,7 | 83,0 | −136,7 | 33,0 |

Cánh mở ra **nằm ngang, mặt dưới phẳng tại Z49** — đúng cao độ vành thân. Vươn ra **158,7 mm**.
Mặt trên dốc từ Z67 xuống Z61 = **1,94° nghiêng về phía người chơi**, đúng thứ cần cho khay bỏ bài,
có được miễn phí từ chính cái vát nắp 18→12.

## Sống khóa chứng minh cánh không thể nằm xuống bàn

Mở hết, sống khóa chúc xuống Z33 — hở mặt bàn 33 mm, đạt. Nhưng nếu hạ trục để cánh nằm hẳn xuống
bàn (cần Pz = 33,5), sống khóa **đâm xuống dưới mặt bàn 16 mm**.

Chính chi tiết sống khóa loại bỏ toàn bộ họ nghiệm "cánh nằm phẳng trên bàn". Trục cao là bắt buộc.

## Quét 0–180°

1° một bước, 11 điểm biên + đáy sống khóa, kiểm với vách thân / đáy hộp / khay / mặt bàn:
**không va chạm ở bất kỳ góc nào**. Khoảng cách nhỏ nhất tới mặt bàn 33 mm.

## Vấn đề mới: không có mặt chặn 180° tự nhiên

Ở 180° không bề mặt nào của cánh gặp bề mặt nào của thân. Khớp chốt không chịu được mô men quanh
chính trục nó → cánh quay tiếp và rớt xuống nếu không chặn.

**Giải:** phay một mặt phẳng trên ống gỗ của cả hai bên — chặn nằm trong lòng mộng, hoàn toàn khuất.

| Trường hợp tải | Mô men | Lực chặn | Ứng suất |
|---|---:|---:|---:|
| Chỉ trọng lượng cánh (0,83 kg) | 0,72 N·m | 120 N | 0,11 MPa |
| + 2 kg quân bỏ trên khay | 2,45 N·m | 409 N | 0,39 MPa |
| + người chơi tỳ 5 kg mép ngoài | 8,94 N·m | 1491 N | **1,41 MPa** |

Mặt chặn 8 × 44 × 3 mắt mộng = 1056 mm², bán kính 6. Nén ngang thớ cocobolo ~14 MPa → **hệ số 10×**.

## Độ võng đầu cánh

Khe chốt 0,25 trong ống dài 44 → góc rơ 5,68 mrad → **võng 0,95 mm** ở mút 168 mm.
Sụt mặt chặn dưới 5 kg chỉ 0,004 mm.

**Đặc tính kiểm mới:** võng đầu cánh mở ≤ 1,5 mm dưới tải 5 kg tại mép ngoài. Muốn chặt hơn thì
siết khe chốt — toàn bộ độ rơ nằm ở đó, không phải ở tiết diện.

## Hệ quả bắt buộc: vách bản lề 10 → 18

Ống R9 nghĩa là mắt mộng bên **thân** cũng phải dày 18. Vách 10 mm thì lỗ Ø6,2 chỉ còn **1,9 mm**
thành mỗi bên — không dùng được.

| Vách | Khay | Ngăn | Phụ kiện | TỔNG | |
|---:|---:|---:|---:|---:|---|
| 10 | 126 | 6 | 70 | **354** | hiện tại — không dùng được |
| 18 | 126 | 6 | 70 | **370** | **khuyến nghị** — không động bố trí lòng hộp |
| 18 | 126 | 4 | 70 | 366 | vách ngăn mỏng còn 4 |
| 18 | 126 | 6 | 62 | 362 | AC-01 còn 60/50 — phải bố trí lại ổ xúc xắc và hốc quân dự phòng |

**370 × 350** gần vuông, tỷ lệ đẹp hơn 354 × 350. Cánh nắp 184,2 mỗi bên, sống khóa X 163…207.

## Ngưỡng CITES tụt xuống 1 hộp mỗi lô

Ở bề rộng 370 với khay cocobolo, lượng *Dalbergia* mỗi hộp lên **5,13 kg** — hai hộp là 10,26 kg,
vượt ngưỡng miễn trừ 10 kg. Ở 354 vẫn còn 2 hộp.

Muốn giữ 2 hộp ở bề rộng 370: chuyển khay sang lõi ổn định (3,50 kg/hộp) hoặc dùng cocobolo nhẹ hơn.

## Khối lượng — lần thứ ba đi lên

| Mốc | Khối lượng | Tải TK |
|---|---:|---:|
| Bản đầu (ước, thiếu sống khóa) | 7,30 kg | 215 N |
| Chốt khung cocobolo + tính cả sống khóa | 7,92 kg | 233 N |
| Vách bản lề 18, hộp 370 | **8,22 kg** | 242 N |

Kiểm lại ở 242 N: sống uốn 12,3 MPa (hệ số 9×), võng 0,96 mm < 1,14, chốt xoay 0,95 MPa,
chỉ khâu hệ số 3,0×. **Vẫn đạt hết — không phải sửa kích thước nào.**

Nhưng đây là lần thứ ba khối lượng đi lên. Ở 8,2 kg, xách một tay làm được 1–2 phút chứ không hơn.
Hai đòn bẩy duy nhất còn lại: khay lõi ổn định (−0,77 kg) và phương án C (hốc âm hai tay).

## Chốt trị số cho HD-01

| | |
|---|---|
| Trục xoay | X = 9 từ mặt ngoài vách, Z = 58 từ mặt bàn |
| Bán kính ống gỗ | R9, tiếp tuyến mặt trên và mặt dưới nắp |
| Dày vách bản lề | **18** (từ 10) — thành quanh lỗ 5,9 mm |
| Lỗ chốt | Ø6,20 +0,05/0 · chốt Ø6,00 −0,05 |
| Mặt chặn 180° | phay phẳng rộng 8, bán kính 6, hai bên, khuất trong mộng |
| Góc mở | 180° +0/−2° |
| Vị trí cánh khi mở | nằm ngang, mặt dưới Z49, vươn ra 159 |
| Độ võng cho phép | ≤ 1,5 mm tại mép ngoài dưới tải 5 kg |
| Phủ bì mới | **370 × 350 × 83** |

## Còn lại phải làm

| # | Việc | Trạng thái |
|---|---|---|
| 1 | Chốt bề rộng hộp: 370 / 366 / 362 | **chờ quyết định — chặn mọi thứ phía sau** |
| 2 | Cập nhật `box_spec.py` theo bề rộng đã chốt | sau (1) |
| 3 | Vẽ sheet BX-01 thân hộp (§2.2) | **vẫn chưa có** |
| 4 | Hốc nhấc tay + hõm ngón rãnh Joker (§2.3) | chưa vẽ chi tiết |
| 5 | Nắp trượt ổ xúc xắc | chưa vẽ chi tiết |
| 6 | Xác minh CITES: *Dalbergia* + *Afzelia* | việc của bên mua |
