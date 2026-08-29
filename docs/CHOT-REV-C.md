Tài liệu này ghi lại các quyết định chốt trong phiên làm việc 29-08-2026, và — quan trọng hơn — **những chỗ
các tài liệu trước đó sai hoặc đã hết hiệu lực**. Đọc nó trước khi đọc bốn tài liệu cũ.

## Bảng chốt

| | Rev B | Chốt hiện tại | Nguồn |
|---|---|---|---|
| Phủ bì | 354 × 350 × 80 | **370 × 350 × 59** | `box_spec.py` |
| Chuỗi X | 10+126+6+70+6+126+10 | **18+126+6+70+6+126+18** | `width_options.py` |
| Phương án xách | (chưa có) | **C — hốc âm hai tay** | `handle_option_c.py` |
| Đáy hộp | 8 | **6** | `detail_features.py` |
| Tấm nắp Nu | 10 | **8** | `lid_solid_calc.py` |
| Nắp | 18 → 8 (vát) | **đều 12, không vát** | `box_spec.py` |
| Ống bản lề | không định nghĩa | **Ø12**, chốt brass Ø4 | `hinge_kinematics.py` |
| Khe ráp giữa | 0,6 | **1,5 ±0,3** | `lid_solid_calc.py` |
| Trục xoay bản lề | không định nghĩa | **P = (6 , 53)** | `hinge_kinematics.py` |
| Khóa nắp | không có | **8 cặp nam châm nắp↔thân** | `lid_latch.py` |
| Khối lượng | không tính | **5,86 / 6,48 kg** | `box_spec.py` |
| Tải thiết kế | — | **172 / 191 N** | `box_spec.py` |

## 1. Bề rộng: 370

Vách bản lề buộc phải dày 18 vì mắt mộng là ống gỗ R9 quanh lỗ Ø6,20. Vách 10 của Rev B chỉ còn 1,9 mm
thành mỗi bên. Nên chuỗi X 354 không dùng được nữa. Ba cách đóng lại:

| Vách | Khay | Ngăn | Phụ kiện | Tổng | Khối lượng | Hộp/lô | Đổi lại |
|---:|---:|---:|---:|---:|---:|---:|---|
| 18 | 126 | 6 | 70 | **370** | 7,61 kg | 2 | không đổi gì |
| 18 | 126 | 4 | 70 | 366 | 7,52 kg | 2 | vách ngăn 4 mm, mảnh 82:1 |
| 18 | 126 | 6 | 62 | 362 | 7,48 kg | 2 | mất 2 chi tiết công năng |

*(khối lượng trong bảng này tính ở cấu hình lúc so sánh — phương án A, đáy 8, tấm Nu 10)*

Hai điều làm quyết định này dễ hơn tưởng:

- **Bề rộng không lật được số hộp mỗi lô CITES.** Cả ba đều 2 hộp/lô với khay cocobolo. Đòn bẩy là khay,
  không phải bề rộng.
- **362 làm hỏng hai chi tiết công năng của AC-01**, không chỉ "phải bố trí lại": lòng AC còn 50 nên hốc 4
  quân dự phòng 2×2 cần 51,4 không nhét được, và dải gỗ bên rãnh Joker còn 11 nên hõm ngón Ø25 sâu 12 khoét
  thủng ra ngoài.

Chênh khối lượng 370 ↔ 362 chỉ 0,13 kg. Không đáng đổi.

## 2. Phương án xách: C — hốc âm hai tay

Bỏ sống khóa và quai da. Hai hốc lòng bàn tay 120 × 30 sâu 16 phay vào vách trước và vách sau.

Hốc âm nằm ở **vách trái và phải** — tức vách bản lề, dày 18, đủ nuốt hốc sâu 12 + thành sau 6 mà **không
phải nối gỗ ra ngoài**. Phủ bì không đổi.

*(Bản đầu đặt hốc âm ở vách trước/sau dày 10 và kết luận C phải nới Y 350 → 374. Kết luận đó sai vì chọn
nhầm vách: vách trước/sau còn phải mang cả ba khe luồn ngón nhấc khay lẫn tám nam châm khóa nắp — ba chi
tiết tranh nhau một bộ phận dày 10 mm.)*

| | A · sống khóa + quai da | C · hốc âm hai tay |
|---|---|---|
| Phủ bì | 370 × 362 × 75 | **370 × 350 × 59** |
| Thể tích bao | 10,05 L | **7,64 L** |
| Số tay | một | hai |
| Tải mỗi tay | 67 N | **32 N** |
| Chi tiết chuyển động | 2 chốt xoay | **0** |
| Chi tiết mòn | lỗ chốt + da | **không có** |
| Vật liệu ngoài gỗ | da bò bridle | **không** |
| Giải khóa nắp | có | **KHÔNG** |

**Hai điều C để lại:**

1. **Khóa nắp — ĐÃ GIẢI** (29-08-2026, sau khi bỏ ràng buộc "không kim loại"). 8 cặp nam châm nối nắp
   với thân. Xem `docs/KHOA-NAP.md`. Điểm cốt lõi: khóa **không được** nối cánh với cánh — hai cánh cùng
   mở thì hai mép khe nâng bằng nhau và chỉ tách nhau, nên chốt trượt ngang tuột ra sau khi khe đã vênh
   31 mm; và giãn nở theo mùa 1,09 mm buộc mọi khóa cánh–cánh phải có từng ấy rơ, tự nó đã cho 11 mm vênh.
2. **Ec-gô-nô-mi trần hốc.** C chia đôi tải nhưng *tăng* áp lực cục bộ: quai da có 3000 mm² bề mặt nắm, hốc
   âm chỉ có 960 mm² đầu ngón. Nếu trần hốc phẳng và mép sắc thì lực dồn hết về mép trước. Bắt buộc: trần hốc
   dốc vào trong ~10°, mép ngoài bo tròn R ≥ 8.

## 3. Đáy 6 và tấm Nu 8

Hai đòn bẩy giảm cân, nhưng cái thứ hai hoá ra sửa một lỗi tiềm ẩn.

**Đáy 8 → 6.** Kiểm uốn dưới 2 khay đầy trong một khoang: 0,127 MPa, hệ số 864×, võng 0,005 mm giữa nhịp
126. Đáy 6 thừa sức. Ràng buộc thật là rãnh ôm đáy — mộng 4 trong vách 10 để lại 3 mm mỗi bên.

**Tấm Nu 10 → 8.** Khung nắp vát, nên chỗ mỏng nhất của nó là mép trong đố dọc cạnh khe giữa, chỉ còn
13,23 mm. Rãnh ôm tấm ăn vào đó: lip trên 3 + rãnh + lip dưới.

| Dày tấm | Lip trên | Rãnh | Lip dưới | |
|---:|---:|---:|---:|---|
| 10 | 3,0 | 10 | **0,23** | không phay được |
| 9 | 3,0 | 9 | 1,23 | không phay được |
| **8** | 3,0 | 8 | **2,23** | đạt |

Bản trước chốt tấm 10 — đó là một lỗi tiềm ẩn, không phải chỉ là chuyện nặng nhẹ. Kèm theo: rãnh rộng đúng
bằng dày tấm nên **cạnh tấm không bị phay bậc**, tốt cho Nu vì một bậc 1,5 mm trên cạnh gỗ thớ xoắn loạn là
chỗ nứt.

## 4. Bốn chi tiết công năng

Xem `docs/BX-01.md` để có kích thước đầy đủ. Tóm tắt cái gì đổi so với review:

| # | Review Rev B nói | Kết quả |
|---|---|---|
| Nhấc khay §2.3 | hốc lõm 70 × 10 trên vành khoang, "mở được ~17 mm để kẹp" | **không đóng được** — không có chỗ nào quanh khay lọt ngón tay, và cả hai bên đối diện đều bị chắn. Thay bằng khe luồn ngón 12,5 mm + mỏ móc sâu 5 ở hai đầu khoang |
| Hõm ngón Joker §2.3 | Ø25 sâu 12 vào dải 15 mm | **đúng**, giữ nguyên. Còn 3 mm gỗ + 5 mm vách, hệ số 65× |
| Đỡ mép nắp §3.2 | cần sống nổi giữa trên AC-01 | **không còn cần**. Nêu ra khi mép dày 8 (võng 1,98 mm); ở 12 thì võng 0,59 mm, hệ số 22× |
| Nắp trượt ổ xúc xắc | "phải có nắp trượt" | **trượt không làm được** — cần 51 mm hành trình, chỗ trống 22 mm. Thay bằng nắp thả 64 × 51 × 4 |

Việc bỏ sống nổi còn giải luôn một xung đột chưa ai để ý: sống nổi phải nằm ở khe ráp giữa X = 185 và rộng
16, còn rãnh Joker cũng nằm giữa AC-01 và rộng 28. Lòng AC-01 chỉ có 58, nên không thể vừa chừa 16 mm giữa
vừa đặt rãnh Joker. Một trong hai phải đi, và số học cho thấy sống nổi là cái đi.

## 5. CITES — phần viết theo trí nhớ đã được tra lại

Chi tiết và mức tin cậy từng dòng ở `tools/cites_check.py`.

| Điều tài liệu cũ viết | Kết quả tra |
|---|---|
| Ngưỡng 10 kg | **đúng** |
| Thành phẩm được miễn trừ | **đúng** — CoP19 (2022) đổi mục (b) của chú giải #15 từ "xuất khẩu phi thương mại" sang "thành phẩm". Trước CoP19 thì một lô hàng thương mại không được miễn trừ dù nhẹ tới đâu |
| "#15 có thể đã đổi ở CoP20" | **không đổi**. CoP20 (Samarkand, 24-11 → 05-12-2025) thông qua báo cáo tác động và giữ nguyên #15. Sửa đổi Phụ lục của CoP20 có hiệu lực 05-03-2026 |
| "Afzelia vào Phụ lục II ở CoP18" | thực ra **CoP19**, và chỉ **quần thể châu Phi**, chú giải #17 (gỗ tròn / xẻ / ván lạng / ván dán / gỗ đã chế biến — **không** phủ thành phẩm). *A. xylocarpa* là loài châu Á, không có trong Phụ lục |
| "2 hộp mỗi lô hàng" | **có thể sai** — xem dưới |

**Chỗ có thể sai.** Diễn giải chính thức của ngưỡng 10 kg là tính **riêng từng loài** và **riêng từng món
hàng** trong lô, không cộng dồn cả lô. Mỗi hộp chứa 3,88 kg cocobolo (khay cocobolo) hoặc 2,42 kg (khay lõi
ổn định), đều dưới 10 kg. Nếu đọc như vậy thì **số hộp mỗi lô không còn là ràng buộc**, và bảng "số hộp mỗi
lô" trong `QUAI-XACH.md` và `NAP-GO-DAC.md` phải sửa.

> **Cảnh báo về độ tin cậy.** Trong môi trường chạy phiên này, cites.org, fws.gov, bada.org,
> legislation.gov.uk và speciesplus.net đều bị chặn ở tầng proxy. Toàn bộ phần trên là **nguồn thứ cấp qua
> công cụ tìm kiếm**, không có dòng nào được đối chiếu với văn bản gốc. Đủ để thiết kế tiếp, **không đủ để ký
> hợp đồng**. Năm chỗ phải tự đi hỏi liệt kê ở `tools/cites_check.py` mục 4 — trong đó nguy hiểm nhất là cơ
> quan quản lý CITES của **nước nhập**, vì họ có thể đọc ngưỡng chặt hơn nước xuất.

Về *Afzelia*: CITES gần như chắc chắn không chạm tới tấm nắp — hai lớp bảo vệ (loài châu Á không được liệt
kê; và ngay cả loài châu Phi thì #17 không phủ thành phẩm), cả hai đều không dính. Ràng buộc thật nằm ở
**Nhóm IIA trong nước**, chi phối việc khai thác, mua bán và vận chuyển nội địa. Nền pháp lý là Nghị định
06/2019 sửa bởi 84/2021; có dấu hiệu danh mục hiện hành đã chuyển sang Thông tư 85/2025/TT-BNNMT — **phải
xác nhận**.

## 6. Hai lỗi số của bản trước

1. **Góc vát nắp.** Bản trước ghi 1,945°, tính bằng `atan(6/176,7)` — chia cho cả bề rộng cánh. Nhưng đoạn
   vát thật chỉ chạy từ X = 18 (mép trong ống gỗ) ra tới mép khe giữa. Ở bề rộng 370 thì đoạn đó là 166,25 và
   góc đúng là **2,067°**.
2. **Khối lượng ở bề rộng 370.** Đoạn ước lượng bằng tay ở cuối `hinge_kinematics.py` cộng cả phần vách dày
   thêm lẫn phần vách trước/sau dài thêm, đếm trùng. Con số 7,75 kg sai; tính lại bằng `derive()` cho 7,60 kg.

## 7. Hai lần sửa sau khi dựng hình 3D

Bản dựng 3D và ảnh mẫu thật buộc phải sửa hai chỗ, và cả hai đều kéo theo hệ quả tốt:

**Hốc âm chuyển từ vách trước/sau sang vách trái/phải.** Lý do gốc là ba chi tiết tranh nhau vách 10 mm.
Kéo theo: phủ bì Y về lại 350, khoang phụ kiện lấy lại được khe luồn ngón, và cách nhấc AC-01 bằng kẹp hai
dải gỗ qua hõm ngón rãnh Joker — vốn xấu — bị bỏ.

**Ống bản lề Ø18 → Ø12.** Ống phải tiếp tuyến cả vành thân lẫn mặt trên nắp, nên R = nửa bề dày nắp. Muốn
ống thanh hơn thì phải làm nắp mỏng hơn: nắp **đều 12** thay cho vát 18 → 12. Ống Ø18 chiếm 27,7 % chiều
cao hộp, Ø12 chiếm 20,3 %. Chốt đổi từ gỗ Ø6 sang **brass Ø4** vì thành ống chỉ còn 3,9 mm.

Giá phải trả: khay bỏ bài trên mặt dưới nắp từ 7 mm xuống 3,5 mm, và tấm Nu từ 8 xuống 6 mm.

Phần thưởng ngoài dự tính: **5,86 kg** — lần đầu xuống dưới ngưỡng 6 kg. Riêng việc làm nắp mỏng lấy đi
0,62 kg, và đó là hệ quả phụ của một thay đổi thẩm mỹ.

## 8. Còn lại

| # | Việc | Trạng thái |
|---|---|---|
| 1 | Khóa nắp | **đã giải** — `docs/KHOA-NAP.md`. Còn lại: đo lực tách trên mẫu thật |
| 2 | Ec-gô-nô-mi trần hốc âm: dốc 10°, bo R8 | đã ghi đặc tính, chưa vẽ chi tiết |
| 3 | Sheet nắp và sheet khay theo số mới | chưa vẽ |
| 4 | Xác minh CITES bằng văn bản gốc | việc của bên mua |
| 5 | Đo tối thiểu 20 quân thuộc đúng lô mua | chưa làm — chặn mọi thứ về khay |
| 6 | Ép thử 1 mộng khung cocobolo, để 7 ngày rồi phá huỷ | chưa làm |

Mục 5 và 6 là hai rủi ro thi công lớn nhất. Mộng khung cocobolo: 8 mộng, gỗ nhiều dầu, bắt buộc epoxy + lau
acetone trong vòng 15 phút kể từ khi phay xong má mộng + chốt draw-bore Ø5. Đường phá của mẫu thử phải đi
qua thớ gỗ, không được đi dọc đường keo.
