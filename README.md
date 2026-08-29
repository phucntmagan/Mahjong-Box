# Hộp Mahjong 152 quân — hồ sơ thiết kế

Hộp gỗ đựng bộ Mahjong 152 quân (BURLORA), tham chiếu bộ Mahjong của Hermès.
Khởi đầu là một bản review độc lập cho bản vẽ sản xuất **Rev B**; nay là hồ sơ thiết kế đang tiến hoá.

**Phủ bì đã chốt: 370 × 374 × 65 mm · 6,25 kg** (khay lõi ổn định) hoặc **6,86 kg** (khay cocobolo).

## Đọc theo thứ tự này

| # | Đường dẫn | Nội dung |
|---|---|---|
| 1 | `docs/CHOT-REV-C.md` | **Bắt đầu ở đây.** Quyết định đã chốt, và những chỗ tài liệu cũ sai hoặc hết hiệu lực |
| 2 | `docs/BX-01.md` | Sheet thân hộp — chuẩn, dung sai, bản lề, hốc âm, khe luồn ngón, ổ xúc xắc |
| 3 | `docs/KHOA-NAP.md` | Khóa nắp — vì sao phải nối nắp với thân, và chặn đúng một phương |
| 4 | `docs/REVIEW-RevB.md` | Review gốc bản vẽ Rev B (hồ sơ, có banner chỉ chỗ đã đổi) |
| 5 | `docs/NAP-GO-DAC.md` | Nắp khung gỗ đặc ôm tấm Nu thả |
| 6 | `docs/DONG-HOC-BAN-LE.md` | Động học bản lề — suy trục xoay từ ràng buộc |
| 7 | `docs/QUAI-XACH.md` | Phương án quai A — **đã loại**, giữ làm hồ sơ |

PDF tương ứng trong `build/`. Hình trong `figs/`.

## Quyết định đã chốt

| | |
|---|---|
| Vật liệu | thân, khay, khung nắp: **cocobolo** ρ 1,00 · tấm nắp: **Nu gõ đỏ** thả trong rãnh |
| Nắp | khung gỗ đặc ôm tấm Nu thả — tấm liền sẽ kẹt bản lề ở ΔMC 4,1 % |
| Xách | **phương án C** — hai hốc âm 120 × 30 sâu 16, xách hai tay |
| Bản lề | trục **P = (9 , 56)**, ống gỗ R9 tiếp tuyến hai mặt nắp; mở 180° nằm ngang, vươn 166,25 |
| Bề rộng | **370** — vách bản lề buộc phải 18 để chứa ống gỗ R9 |
| Khe ráp giữa | **1,5 ±0,3** |
| Khóa nắp | **8 cặp nam châm 25 × 5 × 4** nối nắp với thân, chặn phương Z, tự do theo X |

## Chạy

```
python3 tools/box_spec.py          # đặc tả đã chốt: hình học, khối lượng, tải, tự kiểm
python3 tools/width_options.py     # so sánh ba phương án bề rộng
python3 tools/handle_option_c.py   # phương án xách C, so với A
python3 tools/hinge_kinematics.py  # trục xoay, quét va chạm, mặt chặn
python3 tools/lid_solid_calc.py    # nắp gỗ đặc: giãn nở, kẹt mộng, lip rãnh ôm tấm
python3 tools/detail_features.py   # nhấc khay, hõm Joker, đỡ mép nắp, nắp che xúc xắc
python3 tools/lid_latch.py         # khóa nắp: động học, độ ẩm, tải, nam châm vs brass
python3 tools/cites_check.py       # CITES: điều đã tra được và mức tin cậy từng dòng
python3 tools/check_dimensions.py  # kiểm bản vẽ Rev B + đối chiếu với đặc tả hiện hành
python3 tools/handle_calc.py       # phương án quai A (đã loại, giữ làm hồ sơ)
```

Không phụ thuộc thư viện ngoài. Thoát mã 0 nếu không có lỗi số học.

`tools/box_spec.py` là **nguồn sự thật duy nhất** cho vật liệu, hình học, khối lượng và tải.
Mọi script khác import từ đó; không script nào được viết lại một con số hình học.
Toàn bộ hình học sinh từ chuỗi kích thước qua `derive()`, và `selfcheck()` chặn các tổ hợp không dựng được.

## Dựng lại hình và PDF

```
python3 tools/draw_bx01.py     # sinh figs/fig9, fig10
python3 tools/draw_latch.py    # sinh figs/fig11
python3 tools/draw_hinge.py    # sinh figs/fig8
python3 tools/draw_lid.py      # sinh figs/fig6, fig7
python3 tools/draw_handle.py   # sinh figs/fig1..fig5
./tools/render_figs.sh         # SVG -> PNG (cửa sổ chụp cao hơn SVG rồi crop)
./tools/build_pdf.sh           # docs/*.md -> build/*.html -> build/*.pdf
```

`tools/md2html.py` dùng chung CSS với `build/review.html` nên PDF mới và cũ đồng bộ định dạng.

## Rủi ro lớn nhất còn lại

1. **Mộng khung cocobolo.** 8 mộng, gỗ nhiều dầu. Bắt buộc epoxy + lau acetone trong vòng 15 phút kể từ khi
   phay xong má mộng + chốt draw-bore Ø5. Phải ép thử một mộng mẫu, để 7 ngày rồi phá huỷ.
2. **CITES.** Phần pháp lý đã tra lại nhưng cites.org bị chặn trong môi trường chạy, nên toàn bộ là nguồn thứ
   cấp. Đủ để thiết kế tiếp, không đủ để ký hợp đồng.
3. **Lô quân cờ.** Phải đo tối thiểu 20 quân thuộc đúng lô mua trước khi chốt lòng khay.
