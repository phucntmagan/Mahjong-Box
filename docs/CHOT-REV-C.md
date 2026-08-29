Tài liệu này ghi lại các quyết định chốt trong phiên làm việc 29-08-2026, và — quan trọng hơn — **những chỗ
các tài liệu trước đó sai hoặc đã hết hiệu lực**. Đọc nó trước khi đọc bốn tài liệu cũ.

## Bảng chốt

| | Rev B | Chốt hiện tại | Nguồn |
|---|---|---|---|
| Phủ bì | 354 × 350 × 80 | **382,2 × 350 × 62** (thân 370) | `box_spec.py` |
| Chuỗi X | 10+126+6+70+6+126+10 | **18+126+6+70+6+126+18** | `width_options.py` |
| Phương án xách | (chưa có) | **C — hốc âm hai tay** | `handle_option_c.py` |
| Đáy hộp | 8 | **6** | `detail_features.py` |
| Tấm nắp Nu | 10 | **7** | `lid_solid_calc.py` |
| Nắp | 18 → 8 (vát) | **đều 15, không vát** | `box_spec.py` |
| **Trục xoay bản lề** | không định nghĩa | **P = (0 , 47) — trên arris** | `hinge_kinematics.py` |
| **Bản lề** | mắt mộng gỗ + chốt Ø6 | **mắt mộng gỗ + chốt gỗ Ø6** (không đổi) | `hinge_kinematics.py` |
| Ống gỗ | Ø18 | **Ø12,2**, nhô ra 6,1 mỗi bên | `hinge_kinematics.py` |
| Khe ráp giữa | 0,6 | **1,5 ±0,3** | `lid_solid_calc.py` |
| Khóa nắp | không có | **8 cặp nam châm nắp↔thân** | `lid_latch.py` |
| Khối lượng | không tính | **6,17 / 6,78 kg** | `box_spec.py` |
| Tải thiết kế | — | **181 / 200 N** | `box_spec.py` |

## 1. Bề rộng: 370

Vách bản lề buộc phải dày 18 — lúc quyết định là vì ống gỗ R9, nay là vì **hốc âm hai tay** (sâu 12 +
thành sau 6). Lý do đổi nhưng con số không đổi, nên chuỗi X 354 của Rev B vẫn không dùng được. Ba cách
đóng lại:

| Vách | Khay | Ngăn | Phụ kiện | Tổng | Khối lượng | Hộp/lô | Đổi lại |
|---:|---:|---:|---:|---:|---:|---:|---|
| 18 | 126 | 6 | 70 | **370** | 6,78 kg | 2 | không đổi gì |
| 18 | 126 | 4 | 70 | 366 | 6,71 kg | 2 | vách ngăn 4 mm, mảnh 82:1 |
| 18 | 126 | 6 | 62 | 362 | 6,66 kg | 2 | mất 2 chi tiết công năng |

*(khối lượng khay cocobolo ở cấu hình hiện hành; chạy `python3 tools/width_options.py` để đối chiếu)*

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
| Phủ bì | 370 × 362 × 78 | **370 × 350 × 62** |
| Thể tích bao | 10,45 L | **8,03 L** |
| Khối lượng (khay cocobolo) | 7,19 kg | **6,78 kg** |
| Khối lượng (khay lõi ổn định) | 6,59 kg | **6,17 kg** |
| Số tay | một | hai |
| Tải mỗi tay | 71 N | **34 N** |
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

## 6. Ba lỗi của bản trước

1. **Góc vát nắp.** Bản trước ghi 1,945°, tính bằng `atan(6/176,7)` — chia cho cả bề rộng cánh, trong khi
   đoạn vát thật ngắn hơn. Ở bề rộng 370 góc đúng là 2,067°. **Nay không còn ý nghĩa: nắp đều 15, không vát.**
2. **Khối lượng ở bề rộng 370.** Đoạn ước lượng bằng tay ở cuối `hinge_kinematics.py` cộng cả phần vách dày
   thêm lẫn phần vách trước/sau dài thêm, đếm trùng. Con số 7,75 kg sai; tính lại bằng `derive()` cho 7,60 kg.
3. **"Ống phải bằng nửa bề dày nắp" — đúng, nhưng là hệ quả của một giả thiết chưa ai đặt câu hỏi.**
   Xem mục 7 dưới.

## 7. Ba lần sửa sau khi dựng hình 3D và đối chiếu ảnh mẫu

**(a) Hốc âm chuyển từ vách trước/sau sang vách trái/phải.** Lý do gốc: ba chi tiết (hốc âm, khe luồn ngón,
nam châm) tranh nhau vách 10 mm. Kéo theo: phủ bì Y về lại 350, khoang phụ kiện lấy lại được khe luồn ngón,
và cách nhấc AC-01 bằng kẹp hai dải gỗ qua hõm ngón rãnh Joker — vốn xấu — bị bỏ.

**(b) Ống bản lề Ø18 → Ø12** (bước trung gian, nay đã bỏ). Lập luận khi đó: ống phải tiếp tuyến cả vành thân
lẫn mặt trên nắp, nên R = nửa bề dày nắp; muốn ống thanh hơn thì phải làm nắp mỏng hơn.

![Tổng thể nắp đóng: mắt mộng gỗ Ø12,2 chạy dọc cạnh trái, không một chi tiết kim loại.](figs/fig12a-tong-the-nap-dong.png)

**(c) Bỏ ống gỗ Ø15: đưa trục xoay ra arris.** Đây là thay đổi lớn nhất của phiên này, và nó bắt đầu từ
một câu hỏi: *bản lề trong ảnh gần như vô hình, mà nắp vẫn dày — sao họ làm được?*

Lập luận (b) **đúng, nhưng chỉ đúng bên trong một giả thiết chưa hề được đặt câu hỏi**: rằng trục xoay
nằm ở giữa bề dày nắp. Giả thiết đó là **thẩm mỹ** — để cánh mở nằm đúng dải cao độ của nắp lúc đóng —
chứ không phải hình học. Ràng buộc thật sự chỉ có một: cánh không được cắt vào thân trong cả hành trình.

`hinge_kinematics.py` §1 nay quét bài toán bằng số, không bằng lời:

| đặt trục ở | toạ độ | R mũi phải bo | ống gỗ | nhô ra | chặn 180° |
|---|---:|---:|---:|---:|---|
| giữa bề dày nắp | (7,5 , 54,5) | 7,52 | Ø15,0 | 0 | phải PHAY |
| lùi vào 2 mm | (2,0 , 54,5) | 7,55 | Ø15,1 | 0 | phải PHAY |
| **trên mặt ngoài, ở arris** | **(0 , 47)** | **0,00** | **Ø12,2** | 6,1 | **tự nhiên** |

R tụt về 0 **đúng khi trục nằm trên mặt phẳng ngoài của thân**: mặt đầu cánh nắp *chính là* mặt phẳng
x = 0, nên trục nằm trên nó thì cả mặt đầu là một tia xuất phát từ trục. **Quy tắc: trục cắm sâu vào
vật liệu bao nhiêu thì phải bỏ đi bấy nhiêu** — và ở giữa bề dày nắp, con số đó đúng bằng nửa bề dày nắp.

Đưa trục ra arris thì đường kính ống hết bị bề dày nắp ép, và được định lại theo **độ bền thành gỗ quanh
lỗ chốt**: Ø12,2 = chốt gỗ Ø6 + thành 3,0 mỗi bên. Mảnh hơn 1,23 lần. Kèm theo: mặt chặn 180° trở thành
**tự nhiên** (mặt cạnh nắp áp vào mặt vách, 3 335 mm², hệ số 29× dưới người tỳ 5 kg) thay cho mặt phay
10× trong lòng mộng, và cánh mở nằm **phẳng bằng vành thân** thay vì cao hơn 15 mm.

**Cái giá, nói thẳng:** tâm ống nằm trên mặt ngoài vách nên nửa ống nhô ra **6,1 mm mỗi bên** — phủ bì X
đi từ 370 lên **382,2**. Lòng hộp, khay và chuỗi X của thân không đổi.

Vì bề dày nắp hết bị ràng buộc, nó được chọn lại theo công năng: **15 mm**, cho khay bỏ bài sâu **5,0 mm**
(thay vì 3,5) và tấm Nu **7 mm** (lip rãnh phay được).

### Một lần đi chệch phải ghi lại

Trong phiên này tao đã có lúc **thay mắt mộng gỗ bằng bản lề lá brass** và đẩy nó vào cả đặc tả lẫn tài
liệu. Đó là **sai quy trình, không phải sai kỹ thuật**: brass chỉ được chấp nhận cho **khóa nắp**, còn
bản lề mộng gỗ là ràng buộc vật liệu đã chốt từ đầu và không ai cho phép đổi. Đã hoàn nguyên toàn bộ.

Cái giữ lại được từ nhánh sai đó là **hình học**, không phải vật liệu: chỗ đặt trục ở arris đúng cho cả
mộng gỗ lẫn bản lề kim loại — nó chỉ nói rằng bán kính quét bằng 0, còn cái gì lấp vào chỗ trục thì tuỳ.

![Nắp mở 180°: hai cánh nằm ngang, mặt trên phẳng đúng cao độ vành thân Z47.](figs/fig12b-nap-mo-180.png)

## 8. Còn lại

| # | Việc | Trạng thái |
|---|---|---|
| 1 | Khóa nắp | **đã giải** — `docs/KHOA-NAP.md`. Còn lại: đo lực tách trên mẫu thật |
| 2 | Ec-gô-nô-mi trần hốc âm: dốc 10°, bo R8 | đã ghi đặc tính, chưa vẽ chi tiết |
| 3 | Sheet nắp và sheet khay theo số mới | chưa vẽ |
| 4 | Xác minh CITES bằng văn bản gốc | việc của bên mua |
| 5 | Đo tối thiểu 20 quân thuộc đúng lô mua | chưa làm — chặn mọi thứ về khay |
| 6 | Ép thử 1 mộng khung cocobolo, để 7 ngày rồi phá huỷ | chưa làm |
| 7 | Khoan thử lỗ chốt Ø6,20 sâu 160 xuyên 7 mắt mộng cocobolo, đo độ trôi | chưa làm |

Mục 5 và 6 là hai rủi ro thi công lớn nhất. Mộng khung cocobolo: 8 mộng, gỗ nhiều dầu, bắt buộc epoxy + lau
acetone trong vòng 15 phút kể từ khi phay xong má mộng + chốt draw-bore Ø5. Đường phá của mẫu thử phải đi
qua thớ gỗ, không được đi dọc đường keo.

Mục 7 mới là rủi ro chế tạo lớn thứ ba: thành gỗ quanh lỗ chốt chỉ **3,0 mm**, và mũi khoan trôi
0,1–0,2 mm trên 160 mm là bình thường trên gỗ nhiều dầu. Nếu độ trôi đo được lớn hơn, phải tăng
`KN_WALL` trong `box_spec.py` — đổi nó thì đường kính ống, độ nhô ra, phủ bì X, chiều cao mặt chặn 180°
và thể tích gỗ tự cập nhật theo.
