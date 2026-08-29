# Động học bản lề — mắt mộng gỗ, trục ở arris

> Bản đầy đủ có hình: **`build/dong-hoc-ban-le.pdf`**.
> Hình: `figs/fig8-dong-hoc-ban-le`. Tính toán: `tools/hinge_kinematics.py`.
> Mọi con số trong tài liệu này do script sinh ra. Chạy lại để đối chiếu.

## Ràng buộc vật liệu — không phải biến

Bản lề làm bằng **mắt mộng gỗ, không dùng kim loại**. Đây là quyết định đã chốt từ đầu và không nằm
trong phạm vi thương lượng của tài liệu này. (Kim loại chỉ được chấp nhận cho **khóa nắp** — xem
`docs/KHOA-NAP.md`.)

Cái duy nhất còn là biến là **chỗ đặt trục** — và chính chỗ đó ép đường kính ống gỗ, chứ không phải
ngược lại.

## Bản trước lập luận thế nào, và sai ở đâu

> *"Ống phải tiếp tuyến cả vành thân (để mắt mộng bên thân mọc lên được từ vách) lẫn mặt trên nắp
> (để cánh mở 180° nằm phẳng đúng cao độ vành) → R = nửa bề dày nắp."*

Câu đó **đúng, nhưng chỉ đúng bên trong một giả thiết chưa hề được đặt câu hỏi**: rằng trục nằm ở
**giữa bề dày nắp**. Ràng buộc hình học thật sự chỉ có một — trong cả hành trình 0–180°, vật liệu
cánh nắp không được cắt vào vật liệu thân hộp. Vị trí trục là **biến**, không phải dữ kiện.

Hệ quả của giả thiết đó: muốn ống mảnh hơn thì **chỉ còn cách làm nắp mỏng hơn**. Đó là lý do bản
trước phải đi Ø18 (nắp 18) → Ø15 (nắp 15) — và vẫn còn to.

## Đặt trục ở đâu thì phải bỏ đi bao nhiêu

`hinge_kinematics.py` §1 không lập luận bằng lời. Nó bo tròn đầu cánh nắp thành mũi tròn bán kính R
quanh trục, quét cánh 0→180° từng nửa độ, và tìm **R nhỏ nhất còn quay lọt**:

| đặt trục ở | toạ độ | R mũi phải bo |
|---|---:|---:|
| giữa bề dày nắp (bản gốc) | (7,5 , 54,5) | **7,52 mm** |
| lùi vào 4 mm từ mặt ngoài | (4,0 , 54,5) | 7,53 mm |
| lùi vào 2 mm từ mặt ngoài | (2,0 , 54,5) | 7,55 mm |
| **trên mặt ngoài, giữa bề dày nắp** | (0,0 , 54,5) | **0,00 mm** |
| **trên mặt ngoài, ở arris** | **(0,0 , 47,0)** | **0,00 mm** |

R tụt về 0 **đúng khi px = 0**, tức khi trục nằm **trên mặt phẳng ngoài** của thân. Lý do hình học:
mặt đầu cánh nắp *chính là* mặt phẳng x = 0; trục nằm trên nó thì cả mặt đầu là một **tia xuất phát
từ trục**, quay bao nhiêu cũng chỉ trượt trên chính nó, không bao giờ đâm vào thân.

Trục lùi vào trong bao nhiêu thì mặt đầu quét thành cung, và phải bo tròn đúng bấy nhiêu. Ở giữa bề
dày nắp: R = 7,5 = 15/2 = **nửa bề dày nắp**. Không phải trùng hợp — mũi tròn buộc phải tiếp tuyến cả
mặt trên lẫn mặt dưới nắp, mà hai mặt đó cách nhau đúng bề dày nắp.

> **Quy tắc rút ra:** trục cắm sâu vào trong vật liệu bao nhiêu thì phải bỏ đi bấy nhiêu.
> Đó là lý do bản lề trong ảnh tham chiếu gần như vô hình trong khi nắp vẫn dày: **họ không đặt trục
> vào giữa bề dày nắp.**

## Chỉ có đúng hai họ nghiệm

| | HỌ A · trục TRONG nắp | HỌ B · trục ở arris |
|---|---:|---:|
| Trục xoay | (7,5 , 54,5) | **(0,0 , 47,0)** |
| Đường kính ống gỗ | Ø15,0 | **Ø12,2** |
| Ống bị ép bởi | **bề dày nắp** | chốt + thành gỗ |
| Nhô ra ngoài mỗi bên | 0,0 mm | **6,1 mm** |
| Phủ bì X | **370,0** | 382,2 |
| Thành gỗ quanh lỗ chốt | 4,40 mm | 3,00 mm |
| Chặn 180° | phải **PHAY** mặt chặn | **tự nhiên** |
| Diện tích chặn | — | **3 335 mm²** |
| Cánh mở nằm ở | Z47…62 | Z32…47 |
| So với vành thân | cao hơn vành 15 | **phẳng bằng vành** |
| Khối lượng (khay lõi ổn định) | 6,10 kg | 6,17 kg |

**Đã chọn: HỌ B.** Đổi `B.HG_MODE` trong `tools/box_spec.py` rồi chạy lại là ra họ kia — mọi trị số
khác tự suy lại theo.

**Cái giá của họ B, nói thẳng:** ống gỗ nhô ra 6,1 mm mỗi bên, nên **phủ bì X đi từ 370 lên 382,2**.
Lòng hộp, khay, chuỗi kích thước X của thân đều **không đổi** — chỉ có một đường gờ tròn Ø12,2 chạy
dọc hai cạnh bản lề. Đổi lại: ống mảnh hơn 1,23 lần, cánh nắp giữ được cạnh vuông sắc, và có mặt chặn
180° thật.

Trong họ B, mọi điểm trên mặt phẳng x = 0 từ Z47 đến Z62 đều cho R mũi = 0. Chọn **đúng arris**
(Z47) vì chỉ ở đó, khi mở 180° mặt cạnh nắp mới áp thẳng vào mặt ngoài vách — có mặt chặn tự nhiên —
và cánh mở mới nằm phẳng bằng vành thân.

![Hành trình 0→180° và hai họ nghiệm: trục trong vật liệu ép ống Ø15, trục trên mặt phẳng ngoài cho ống Ø12,2.](figs/fig8-dong-hoc-ban-le.png)

## Cánh mở ra nằm ở đâu

| Điểm | Đóng X | Đóng Z | Mở 180° X | Mở 180° Z |
|---|---:|---:|---:|---:|
| mép bản lề, mặt dưới | 0,0 | 47,0 | 0,0 | 47,0 |
| mép bản lề, mặt trên | 0,0 | 62,0 | −0,0 | 32,0 |
| mép khe giữa, mặt dưới | 184,2 | 47,0 | −184,2 | 47,0 |
| mép khe giữa, mặt trên | 184,2 | 62,0 | −184,2 | 32,0 |

Cánh mở nằm **ngang**, mặt trên phẳng tại **Z47 — đúng cao độ vành thân**, vươn ra 184,25 mm. Mặt đó
chính là lòng lõm ôm tấm Nu khi đóng, tức **khay bỏ bài sâu 5,0 mm**.

## Chặn 180° — tự nhiên, không phải phay thêm

Ở 180°, mặt cạnh bản lề của nắp áp **đúng** vào mặt ngoài vách thân — cả hai đều là mặt phẳng x = 0.

- trong đoạn mộng (314 mm) ống gỗ ăn mất 6,1 nên chặn cao **8,90**
- ngoài đoạn mộng (36 mm) cánh nắp còn vuông nên chặn cao cả **15**
- tổng diện tích chặn **3 335 mm²**

| trường hợp tải | M (N·m) | F (N) | MPa | hệ số |
|---|---:|---:|---:|---:|
| chỉ trọng lượng cánh | 0,59 | 100 | 0,030 | 466× |
| + 2 kg quân bỏ trên khay | 2,40 | 405 | 0,121 | 115× |
| + người chơi tỳ 5 kg ở mép ngoài | 9,63 | 1 623 | 0,487 | **29×** |

Họ A phải phay một mặt chặn phẳng nằm trong lòng mắt mộng, hệ số 10×. Họ B chặn bằng cả mặt cạnh nắp
áp vào cả mặt vách, **không gia công gì thêm**.

## Quét 0–180° — kiểm va chạm

Quét 1° một bước, 9 điểm biên trên cánh. **Không va chạm ở bất kỳ góc nào.** Điểm thấp nhất Z = 32,0
(= vành thân trừ bề dày nắp — đúng vị trí cánh mở).

## Mắt mộng gỗ

| | |
|---|---|
| Kiểu | mắt mộng gỗ liền khối với thân và với nắp — **không một chi tiết kim loại** |
| Số mắt mộng | **7** mỗi cánh: 4 thuộc THÂN, 3 thuộc NẮP (lẻ nên hai đầu thuộc thân) |
| Kích thước | dài 44, bước 45, khe dọc trục 1,0, chuỗi **314** |
| Đặt theo Y | 18,0 … 332,0 trên cánh dài 350 |
| Ống gỗ | **Ø12,2** quanh trục (0 , 47) |
| Chốt | gỗ cocobolo thẳng thớ **Ø6 × 160**, 2 chốt mỗi cánh, gặp nhau ở mắt mộng giữa |
| Lỗ chốt | Ø6,20 (+0,20 khe) |
| Thành gỗ quanh lỗ | **3,00 mm** |

Tải: trọng lượng một cánh 0,66 kg = 6,5 N chia cho 3 mắt mộng NẮP → 2,2 N mỗi mắt. (Mô men khi mở
180° do **mặt chặn** nhận, không phải chốt.)

| kiểm | ứng suất | cho phép | hệ số |
|---|---:|---:|---:|
| cắt chốt gỗ (2 mặt cắt) | 0,038 MPa | 13 MPa | 342× |
| ép mặt lỗ chốt | 0,008 MPa | 14 MPa | 1 718× |
| xé dọc thành gỗ quanh lỗ | 0,008 MPa | 7 MPa | 859× |

**Độ bền không phải ràng buộc** — hệ số hàng trăm đến hàng nghìn lần. Cái quyết định 3,0 mm thành gỗ
là **chế tạo**: phải khoan một lỗ Ø6,20 sâu 160 mm xuyên 7 mắt mộng xen kẽ, trên gỗ nhiều dầu. Mũi
khoan trôi 0,1–0,2 mm trên 160 là bình thường; thành 3,0 mm nuốt được độ trôi đó mà không nứt ra
ngoài. Dưới 2,5 mm thì không.

**Đặc tính kiểm:** khoan bằng khoan cần hoặc khoan từng mắt mộng rồi ráp thử; sai lệch đồng trục giữa
hai đầu ≤ 0,15 mm. Chạy thử 500 chu kỳ mở–đóng.

## Độ võng đầu cánh khi mở

Cánh mở là dầm console dài 184 mm, ngàm dọc mặt chặn 180°. Người chơi tỳ 5 kg ở mép ngoài, tải trải
đều trên 100 mm bề rộng:

- võng đầu cánh **0,28 mm** · uốn 2,4 MPa (MOR 110) → hệ số **46×**
- cộng rơ của chốt trong lỗ (0,20) → tổng **~0,48 mm**

**Đặc tính kiểm:** võng đầu cánh mở ≤ 1,5 mm dưới tải 5 kg tại mép ngoài.

## Chốt lại cho HD-01

| | |
|---|---|
| Vật liệu bản lề | **MỘNG GỖ liền khối — không một chi tiết kim loại nào** |
| Họ nghiệm | B — trục trên mặt phẳng ngoài, ở arris |
| Trục xoay | X = 0,0 · Z = 47,0 |
| Suy ra từ | R mũi = 0 chỉ khi trục nằm trên mặt phẳng ngoài |
| Ống gỗ | **Ø12,2** — định bởi chốt Ø6 + thành gỗ 3,0, **KHÔNG** bởi bề dày nắp |
| Nhô ra ngoài | 6,1 mm mỗi bên → phủ bì X **382,2** |
| Mắt mộng | 7 × 44, bước 45, chuỗi 314, đặt giữa cánh |
| Chốt | gỗ Ø6 × 160, 2 chốt mỗi cánh |
| Chặn 180° | mặt cạnh nắp áp vào mặt ngoài vách — tự nhiên, 3 335 mm² |
| Góc mở | 180° +0/−1° |
| Vị trí cánh khi mở | nằm ngang, mặt trên Z47 (= vành thân), vươn ra 184 |
| Bề dày nắp | **15 đều, không vát** — bề dày nắp KHÔNG còn định ống gỗ |
| Phủ bì | **382,2 × 350 × 62** |
| Khối lượng | **6,17 kg** (khay lõi ổn định) / **6,78 kg** (khay cocobolo) |
