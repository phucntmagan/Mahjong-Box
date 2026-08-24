# Phương án nắp gỗ đặc — khung gỗ đỏ ôm tấm Nu

> Bản đầy đủ có hình: **`build/Nap-go-dac-Mahjong.pdf`**.
> Hình: `figs/fig6-khung-tam-tha`, `figs/fig7-ket-ban-le`. Tính toán: `tools/lid_solid_calc.py`.

## Kết luận

Nắp gỗ đặc làm được — **nhưng không phải bằng một tấm Nu nguyên khối.**

Mặt mộng bản lề nằm dọc cạnh 350 của cánh nắp. Nu không có hướng thớ nên nở đều mọi phương;
ở **ΔMC 4,1 %** — đúng bằng chênh lệch xưởng (9 %) ↔ mùa nồm (13 %) — khe dọc trục 1,0 mm giữa
các mắt mộng đóng hoàn toàn và **bản lề kẹt cứng**.

Lời giải: **khung gỗ đặc thẳng thớ ôm tấm Nu thả trong rãnh** — đúng thứ trong ảnh mẫu.

## Khe mộng còn lại theo ΔMC (mm)

| Cấu tạo cánh nắp | Hệ số | 2 % | 3 % | 4 % | 5 % |
|---|---:|---:|---:|---:|---:|
| Tấm Nu ĐẶC | 0,22 % | 0,51 | 0,26 | 0,01 | **−0,23** |
| Khung gỗ đặc (dọc thớ) | 0,01 % | 0,98 | 0,97 | 0,96 | 0,94 |
| Lõi ổn định + veneer | 0,05 % | 0,89 | 0,83 | 0,78 | 0,72 |

Khe đóng khi vật liệu giãn ε = 1,0/112 = 0,893 %. Nu đặc: ngưỡng ΔMC 4,1 %. Khung gỗ đặc: 89 %.

Vấn đề thứ hai không tính được bằng số: mắt mộng là ống gỗ thành 5,8 mm quanh lỗ Ø6,2, dài 44.
Nu thớ xoắn loạn, hay có lõi vỏ và lỗ rỗng → có thể tách, và **không có trị số cho phép ổn định**
để thiết kế theo.

## Cấu tạo

| Chi tiết | Kích thước | Ghi chú |
|---|---|---|
| Đố dọc cạnh mộng | 34 × 350 × 18 | gõ đỏ đặc, thớ dọc 350; mang mặt mộng và lỗ Ø6,2 |
| Đố dọc cạnh khe giữa | 34 × 350 × 12 | mang rãnh âm 4 × 21,7 cho sống khóa |
| Đố ngang trước/sau | 30 × 108,7 | |
| Lòng khung | 108,7 × 290 | |
| Tấm Nu | 120,7 × 302 × 10 | mộng 6 vào rãnh sâu 9 → **thả 3 mm mỗi phía** |
| Khe ráp giữa | 0,6 → **1,5 ±0,3** | sống khóa 44 phủ kín nên không lộ |

Chỉ hai thanh đố nằm trong chuỗi kích thước bề rộng: 176,7 = 34 + 108,7 (THẢ) + 34.
Tấm Nu nở vào khoảng trống 3 mm trong rãnh, không đẩy vào khe ráp giữa.

Chuyển vị tấm Nu cần nuốt ở ΔMC 5 %: 0,66 mm (bề rộng), 1,66 mm (chiều dài) — chỗ trống 3,0 mm.

**Chỉ chốt hoặc dán tấm ở đúng một điểm giữa tấm.** Dán quanh rãnh là tấm nứt.

## Khay bỏ bài hình thành miễn phí

Khung dày 18 → 12, tấm Nu dày đều 10 phẳng mặt trên → mặt dưới tấm cao hơn mặt dưới khung
**8 mm tại cạnh mộng, 2 mm tại khe giữa**. Lòng lõm 108,7 × 290 đó chính là khay bỏ bài.

Giải luôn: §3.1 review Rev B (cánh nắp cần lòng lõm) và vấn đề "không phay được lòng ở mép 8 mm".

## Khối lượng

| Cấu tạo | Gỗ | + Quân | TỔNG |
|---|---:|---:|---:|
| Thân + khay cocobolo \| nắp gõ đỏ đặc | 4,94 | 2,43 | **7,37 kg** |
| Thân cocobolo, khay lõi ổn định \| nắp gõ đỏ đặc | 4,17 | 2,43 | **6,60 kg** |
| Thân + khay cocobolo \| nắp lõi ổn định + veneer Nu | 4,49 | 2,43 | 6,92 kg |

Tải thiết kế **217 N** so với 215 N bước trước. **Toàn bộ tính toán quai, sống khóa, chốt xoay
vẫn đủ — không phải tính lại.**

## Tấm Nu — mua và xử lý

Cần 2 tấm đã lạng **121 × 302 × 12** (bào xuống 10), lạng liên tiếp để book-match.
Khối Nu thô tối thiểu ~161 × 342 × 40.

| | |
|---|---|
| Ổn định hoá | ngâm nhựa chân không **trước** khi gia công tinh |
| Mắt / lõi vỏ | trám epoxy **trước** khi chà tinh |
| Chiều dày | 10 mm là điểm cân |
| Dán tấm | chỉ chốt 1 điểm ở đúng tâm |
| Hoàn thiện | bít lỗ (grain filler) rồi mới phủ |

## Không đổi

Sống khóa 44 × 20, chốt xoay Ø16, quai — giữ nguyên. Sống bắt vào **đố dọc cạnh khe giữa**
(gỗ đặc), không bao giờ vào tấm Nu thả. Vát nắp 18 → 12. Phủ bì 354 × 362 × 83.

## Pháp lý

Gõ đỏ = *Afzelia xylocarpa*, IUCN **Endangered**. CoP18 (2019) đưa *Afzelia* spp. **quần thể
châu Phi** vào Phụ lục II CITES. Loài châu Á và quy định **Nhóm IIA** trong nước là hai chuyện
khác nhau và có thể đã thay đổi — phần này viết theo trí nhớ, **bắt buộc xác minh** với Cơ quan
quản lý CITES Việt Nam và Chi cục Kiểm lâm trước khi mua.

Cộng với cocobolo (*Dalbergia*, Phụ lục II) — hộp này nay có **hai loài** cần giấy tờ.

## Thay đổi so với bản trước

| # | Thay đổi | Lý do |
|---|---|---|
| 1 | Cánh nắp: tấm liền → **khung + tấm thả** | Nu đặc kẹt bản lề ở ΔMC 4,1 % |
| 2 | Khe ráp giữa 0,6 → **1,5 ±0,3** | chuyển vị hai đố ở ΔMC 5 % là 1,02 mm |
| 3 | Bỏ nguyên công phay lòng lõm cánh nắp | khung–tấm tự sinh ra khay bỏ bài |
| 4 | Thêm nguyên công ổn định hoá tấm Nu | chống nứt, chống hút hoàn thiện không đều |
| 5 | BOM thêm: 2 tấm Nu, epoxy trám, grain filler | |
| 6 | Hồ sơ CITES: thêm *Afzelia* | trước chỉ có *Dalbergia* |
