# Thiết kế quai xách — Hộp Mahjong 152 quân

> **Trạng thái 29-08-2026. Phương án A trong tài liệu này ĐÃ BỊ LOẠI**, thay bằng phương án C (hốc âm hai tay).
> Giữ lại làm hồ sơ vì nó là cơ sở của các trị số vẫn còn hiệu lực: vát nắp 18 → 12 và khe ráp giữa (1,5 lúc đó; nay 0.7 — xem CHOT-REV-C.md mục Rev C3b).
> Bảng khối lượng và bảng "số hộp mỗi lô" trong đây đều đã lỗi thời — xem **`docs/CHOT-REV-C.md`**.
> So sánh A ↔ C: `tools/handle_option_c.py`.

> Bản đầy đủ có hình: **`build/Thiet-ke-quai-xach-Mahjong.pdf`** (7 trang).
> Hình rời: `figs/fig1..fig5`. Tính toán: `tools/handle_calc.py`. Dựng hình: `tools/draw_handle.py`.

## Ý chính

**Quai và khóa nắp là cùng một bài toán.** Hộp mở bằng hai cánh nắp xoay ra hai bên; nhấc hộp
lên mà không có gì giữ thì hai cánh bung. Nên chi tiết nào làm quai cũng buộc phải làm khóa.

Đề xuất giải cả hai bằng **một chi tiết**: sống khóa cocobolo 362 × 44 × 20 nằm dọc khe ráp
giữa, đè lên cả hai cánh, mang quai da ở giữa, giữ xuống hai trụ vách bằng hai chốt xoay gỗ
1/4 vòng. Chi tiết này cũng đỡ mép tự do của nắp — vấn đề §3.2 còn treo trong review Rev B.
**Một chi tiết, ba việc.**

## Khối lượng — con số quyết định

Cấu hình chốt: thân, khay, khung nắp, sống khóa = **cocobolo** (ρ 1,00); tấm nắp = **Nu gõ đỏ**;
quai = **da bò**. Nguồn sự thật: `tools/box_spec.py`.

| Cấu tạo khay | Gỗ | + Quân | TỔNG |
|---|---:|---:|---:|
| Khay cocobolo | 5,05 | 2,43 | **7,48 kg** |
| Khay lõi ổn định | 4,43 | 2,43 | **6,86 kg** |

7,5 kg một tay là nặng — hơn chiếc cặp laptop đầy. **Đòn bẩy duy nhất còn lại là khay**
(chênh 0,62 kg); 2,43 kg quân cờ là cố định.

Tải thiết kế: **P = 220 N** (7,48 kg × hệ số động 3), 110 N mỗi điểm neo.
Kiểm chứng: treo **30 kg / 60 s** + **5.000 chu kỳ** nhấc–đặt.

## Vì sao quai phải nằm giữa nóc

Trọng tâm ở X 177, Y 175. Vật treo tự xoay đến khi trọng tâm rơi thẳng dưới điểm treo.
Quai trên vách trước lệch 175 mm → hộp treo dọc, nắp thành hai tấm đứng, xúc xắc rời ổ.

Mặt trên chỉ có bốn chỗ neo được:

| Vị trí | |
|---|---|
| Vách trái/phải | ✗ 314/350 mm đã là mặt mộng bản lề |
| **Vách trước/sau** | ✓ liền khối với đáy |
| Hai vách ngăn | ✓ nhưng chỉ cách nhau 76 mm — quá hẹp để nắm |
| Cánh nắp | ✗ xoay tự do, sẽ bung |

→ Hai điểm neo tại **đỉnh vách trước và sau, X 177**, cách nhau 342 mm. Đó là hình dạng sống khóa.

## Ba phương án

| | A · Sống + quai da | B · Bail gỗ gập | C · Hốc âm hai tay |
|---|---|---|---|
| Giải luôn khóa nắp | ✓ | ✓ | ✗ |
| Đỡ mép tự do nắp | ✓ | ✓ | ✗ |
| Phủ bì | 354 × 362 × 83 | 354 × 362 × 99 | 354 × 350 × 67 |
| Chi tiết chuyển động | 2 | 4 | 0 |
| Kim loại | không | không | không |
| Da | có | không | không |
| Tay xách | một tay · 7,48 kg | một tay · 7,48 kg | hai tay · 3,74 kg/tay |
| Rủi ro chế tạo | trung bình | cao | thấp |

**Khuyến nghị A.** Chọn B nếu khách đòi không dùng da (giá: +16 mm chiều cao, thêm 2 khớp mòn).
Ở 7,5 kg, **C không còn là phương án dự phòng mà là lựa chọn nghiêm túc**: 3,74 kg mỗi tay.

## Kiểm bền phương án A

| Bộ phận | Tính | Cho phép | Hệ số |
|---|---|---:|---:|
| Sống — uốn tại hốc quai | 11,2 MPa | 110 (MOR) | 10× |
| Sống — võng giữa nhịp | 0,87 mm | 1,14 (L/300) | đạt |
| Chốt — cắt qua lưỡi | 0,86 MPa | ~14 | 16× |
| Chốt — ép mặt gỗ | 0,69 MPa | ~10 | 14× |
| Da — kéo | 0,92 MPa | ~20 | 22× |
| Đường chỉ khóa, 8 mũi | 220 N | 720 N | 3,3× |

Hai cảnh báo không nằm trong bảng:

1. **Điểm yếu thật là mòn, không phải bền tức thời.** Sau 5.000 chu kỳ lỗ chốt gỗ sẽ ô-van hóa.
   Lót ổ bằng gỗ cực cứng (grenadille/lignum) hoặc sừng, bôi sáp vi tinh thể.
2. **Đừng để dây da dẹt trần làm phần nắm.** Dây 30 × 8 cạnh vuông mang 7 kg sẽ cắt vào tay sau
   ~30 giây. Phần nắm giữa 120 mm phải bọc quanh lõi tròn Ø20–22.

## Tác động dây chuyền

| # | Thay đổi | Hệ quả |
|---|---|---|
| 1 | Vách trước/sau 10 → 20 tại băng X 155–199 | +6 ngoài, +4 trong. Phủ bì Y = **362** |
| 2 | AC-01: 325 → **317** | 5+152+5+65+5+80+5 = 317 |
| 3 | Vát nắp 18 → 8 đổi thành **18 → 12** | góc 1,945°; phay được rãnh âm 4; hết cạnh dao 8 mm |
| 4 | Hốc R8,5 đầu mỗi cánh tại Y 4 / Y 346 | ghép thành lỗ Ø17 cho chốt |
| 5 | Ổ xúc xắc phải có **nắp trượt** | xách là xúc xắc rời ổ |
| 6 | Phủ bì 354 × 350 × 67 → **354 × 362 × 83** | +16 cao, +12 sâu |
| 7 | QA: treo 29 kg/60 s, 5.000 chu kỳ | thay cho mục "20 chu kỳ" hiện chỉ áp cho bản lề |

## Ngưỡng miễn trừ CITES — số hộp mỗi lô hàng

Khung nắp cocobolo đẩy lượng gỗ *Dalbergia* mỗi hộp lên cao:

| Cấu tạo khay | Dalbergia / hộp | 3 hộp | Tối đa mỗi lô |
|---|---:|---:|---:|
| Khay cocobolo | 4,40 kg | 13,19 | **2 hộp** |
| Khay lõi ổn định | 2,92 kg | 8,75 | **3 hộp** |

Theo ngưỡng miễn trừ 10 kg của annotation #15 — phải xác minh bản hiện hành.
Đây là **lý do thương mại** để chọn khay lõi ổn định, độc lập với lý do khối lượng.

## Cần chốt trước khi vẽ chi tiết

1. Khay cocobolo (7,48 kg) hay lõi ổn định (6,86 kg)? → quyết định A/B hay C, và số hộp mỗi lô CITES
2. Có dùng da không? → A hay B
3. Chấp nhận phủ bì 83 mm và hai trụ nhô 6 mm? → nếu không thì chỉ còn C
4. **Động học bản lề (review Rev B §2.5) đã chốt chưa?**

Mục 4 là điều kiện tiên quyết: chừng nào chưa chốt trục xoay bản lề thì chưa vẽ được chi tiết
đầu cánh, mà sống khóa lại kẹp đúng vào đầu cánh.
