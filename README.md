# Hộp Mahjong 152 quân — hồ sơ review thiết kế

Review kỹ thuật độc lập cho bản vẽ sản xuất **Rev B** (BURLORA, 6 sheet, 24-08-2026):
hộp gỗ đựng bộ Mahjong 152 quân, 4 khay 3 × 12, khay phụ kiện trung tâm,
nắp hai cánh vát với mộng gỗ và chốt xoay giấu kín.

## Nội dung

| Đường dẫn | Nội dung |
|---|---|
| `docs/REVIEW-RevB.md` | Báo cáo review đầy đủ |
| `build/Review-Mahjong-152-RevB.pdf` | Bản PDF A3→A4 để in / gửi xưởng (6 trang, có hình mặt cắt và sơ đồ mộng) |
| `build/review.html` | Nguồn HTML của bản PDF |
| `tools/check_dimensions.py` | Kiểm tra lại toàn bộ chuỗi kích thước, chạy độc lập |
| `docs/QUAI-XACH.md` | Thiết kế quai xách (sống khóa + quai da) |
| `build/Thiet-ke-quai-xach-Mahjong.pdf` | Bản PDF thiết kế quai, 7 trang, 5 hình |
| `figs/*.svg` · `figs/*.png` | Hình vẽ thiết kế quai |
| `tools/handle_calc.py` | Tính khối lượng, tải, kiểm bền quai |
| `tools/draw_handle.py` · `tools/render_figs.sh` | Sinh và render hình vẽ |
| `docs/NAP-GO-DAC.md` | Phương án nắp gỗ đặc (khung gỗ đỏ + tấm Nu thả) |
| `build/Nap-go-dac-Mahjong.pdf` | Bản PDF phương án nắp gỗ đặc |
| `tools/lid_solid_calc.py` · `tools/draw_lid.py` | Tính và vẽ phương án nắp gỗ đặc |
| `tools/box_spec.py` | **Đặc tả vật liệu và hình học đã chốt** — nguồn sự thật cho khối lượng và tải |

## Kết quả

Số học của Rev B **đúng toàn bộ** — 0 lỗi trên 16 phép kiểm.
Nhưng có 5 vấn đề hình học/công năng phải giải quyết trước khi lập trình CNC:

1. Chiều cao 80 mm dư 14–24 mm khoảng rỗng, không có chi tiết ép khay → khay xóc khi vận chuyển
2. Không có sheet nào vẽ thân hộp BX-01; khoang 126/70/330 chưa được dung sai hóa
3. Không lấy được khay ra (hở 1,0 mm mỗi bên, không luồn được ngón tay)
4. Chốt gỗ Ø6 × 322 không khoan được và sẽ gãy → tách thành 2 chốt × 160
5. Chưa giải quyết động học mở 180° — cánh sẽ treo lơ lửng trên một chốt gỗ Ø6

Cộng 2 chi tiết công năng bị bỏ sót so với ảnh mẫu và 1 rủi ro độ ẩm
(khe ráp giữa 0,6 mm không hấp thụ nổi giãn nở 2,12 mm của nắp gỗ đặc).

## Chạy kiểm tra

```
python3 tools/check_dimensions.py     # chuỗi kích thước hộp
python3 tools/handle_calc.py          # khối lượng, tải, kiểm bền quai
python3 tools/box_spec.py             # đặc tả đã chốt: khối lượng, tải, Dalbergia/hộp
python3 tools/lid_solid_calc.py       # nắp gỗ đặc: giãn nở, kẹt mộng, khối lượng
python3 tools/draw_handle.py          # sinh figs/*.svg
python3 tools/draw_lid.py             # sinh figs/fig6, fig7
./tools/render_figs.sh                # SVG -> PNG
```

Không phụ thuộc thư viện ngoài. Thoát mã 0 nếu không có lỗi số học.

## Dựng lại PDF

```
chrome --headless --no-pdf-header-footer \
  --print-to-pdf=build/Review-Mahjong-152-RevB.pdf build/review.html
```
