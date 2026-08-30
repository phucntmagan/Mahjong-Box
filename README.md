# Hộp Mahjong 152 quân — hồ sơ thiết kế

Hộp gỗ đựng bộ Mahjong 152 quân (BURLORA), tham chiếu bộ Mahjong của Hermès.
Khởi đầu là một bản review độc lập cho bản vẽ sản xuất **Rev B**; nay là hồ sơ thiết kế đang tiến hoá.

**Phủ bì đã chốt: 388.2 × 350 × 62 mm · 6.45 kg** (khay lõi ổn định) hoặc **7.08 kg** (khay cocobolo).
Ống gỗ bản lề Ø10.2 nằm **đúng trên arris**, nhô ra 5.1 mm mỗi bên — **không hạ bậc**.

## Đọc theo thứ tự này

| # | Đường dẫn | Nội dung |
|---|---|---|
| 1 | `docs/CHOT-REV-C.md` | **Bắt đầu ở đây.** Quyết định đã chốt, và những chỗ tài liệu cũ sai hoặc hết hiệu lực |
| 2 | `docs/BX-01.md` | Sheet thân hộp — chuẩn, dung sai, bản lề, hốc âm, khe luồn ngón, ổ xúc xắc |
| 3 | `docs/KHOA-NAP.md` | Khóa nắp — vì sao phải nối nắp với thân, và chặn đúng một phương |
| 4 | `docs/REVIEW-RevB.md` | Review gốc bản vẽ Rev B (hồ sơ, có banner chỉ chỗ đã đổi) |
| 5 | `docs/NAP-GO-DAC.md` | Nắp khung gỗ đặc ôm tấm Nu thả |
| 6 | `docs/DONG-HOC-BAN-LE.md` | Bản lề mắt mộng gỗ — **chỗ đặt trục quyết định đường kính ống** |
| 7 | `docs/QUAI-XACH.md` | Phương án quai A — **đã loại**, giữ làm hồ sơ |
| 8 | `docs/PROMPT-RENDER.md` | Prompt dựng ảnh 3D vật liệu thật — sinh từ đặc tả, không gõ tay |

PDF tương ứng trong `build/`. Hình trong `figs/`.

**Hình 3D:** `figs/fig12a..g` — tổng thể nắp đóng, nắp mở 180°, lòng hộp, cắt dọc giữa hộp,
vách trái (hốc âm hai tay + bản lề), cắt ngang hốc âm, và nắp che ổ xúc xắc đậy vào.
Dựng bằng `tools/render3d.py` (bộ dựng hình riêng, không thư viện ngoài); mọi toạ độ lấy từ
`box_spec` nên hình đúng từng milimét chứ không phải phác hoạ.

## Quyết định đã chốt

| | |
|---|---|
| Vật liệu | thân, khay, khung nắp: **cocobolo** ρ 1,00 · tấm nắp: **Nu gõ đỏ** thả trong rãnh |
| Nắp | khung gỗ đặc **đều 15** ôm **tấm Nu NÂNG** dày 10 (mộng 7 thả trong rãnh): mặt tấm **ngang bằng mặt khung**, khe 1.5 mm quanh lòng tấm để nở |
| Xách | **phương án C** — hai hốc âm 120 rộng × sâu **16** trong **vách trái/phải**, khe hở vào tay 22.6, xách hai tay |
| Bản lề | **mắt mộng gỗ, KHÔNG kim loại.** Trục **P = (0.0 , 47) — đúng trên arris**, ống gỗ **Ø10.2** (chốt gỗ Ø5 + thành 2.5) **nhô ra 5.1 mm mỗi bên**, **KHÔNG hạ bậc**. 7 mắt × 44, chuỗi 314, 2 chốt gỗ Ø5 × 160 mỗi cánh. Mở 180° nằm ngang phẳng bằng vành thân, vươn 188.25 |
| Xách | hốc âm **sâu 16** (đốt ngón tay lọt hẳn vào mới móc được) → vách bản lề **22** = 16 + 6. Trần hốc bo **R8** rồi dốc 10° — bề mặt 20.7 mm |
| Bề rộng | thân **378** = 22+126+6+70+6+126+22; phủ bì **388.2** kể cả ống bản lề nhô ra. Vách bản lề 22 suy ra từ hốc âm, không phải do bản lề |
| Khe ráp giữa | **1,5 ±0,3** |
| Khóa nắp | **8 cặp nam châm 20 × 5 × 5** nối nắp với thân, chặn phương Z, tự do theo X |

## Chạy

```
python3 tools/box_spec.py          # đặc tả đã chốt: hình học, khối lượng, tải, tự kiểm
python3 tools/break_selfcheck.py   # PHÁ THỬ lưới tự kiểm: mỗi điều kiện phải nổ được
python3 tools/render_prompt.py > docs/PROMPT-RENDER.md   # prompt dựng ảnh vật liệu thật
python3 tools/width_options.py     # so sánh ba phương án bề rộng
python3 tools/handle_option_c.py   # phương án xách C, so với A
python3 tools/hinge_kinematics.py  # trục xoay ở đâu, quét va chạm, mặt chặn 180°
python3 tools/hinge_concealed.py   # bản lề chìm hẳn có được không (không) và vì sao
python3 tools/lid_solid_calc.py    # nắp gỗ đặc: giãn nở, khe ráp giữa, lip rãnh ôm tấm
python3 tools/detail_features.py   # nhấc khay, hõm Joker, đỡ mép nắp, ổ xúc xắc + nắp che
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
python3 tools/render3d.py      # sinh figs/fig12a..g (hình 3D)
python3 tools/draw_hinge.py    # sinh figs/fig8
python3 tools/draw_concealed.py # sinh figs/fig13 (bản lề chìm)
python3 tools/draw_grip.py     # sinh figs/fig14 (trần hốc âm)
python3 tools/draw_lid.py      # sinh figs/fig6, fig7
python3 tools/draw_handle.py   # sinh figs/fig1..fig5
./tools/render_figs.sh         # SVG -> PNG (cửa sổ chụp cao hơn SVG rồi crop)
./tools/build_pdf.sh           # docs/*.md -> build/*.html -> build/*.pdf
./tools/build_drawings.sh      # BỘ BẢN VẼ SẢN XUẤT -> build/BAN-VE-SAN-XUAT.pdf (8 tờ A3)
```

## Bộ bản vẽ sản xuất

`build/BAN-VE-SAN-XUAT.pdf` — 8 tờ A3 ngang, có khung tên, sinh từ `tools/drawings.py`.

| Tờ | Nội dung | Tỉ lệ |
|---|---|---|
| 00 | Danh mục · bảng kê phôi · quy ước chung | — |
| BX-01 | Thân hộp — mặt bằng, mặt cắt A-A, B-B | 1:2 |
| BX-02 | Vách bản lề — hốc âm, mắt mộng, **bảng toạ độ trần cho CNC** | 4:1 / 1:2 |
| HD-01 | Cánh nắp — khung + tấm Nu nâng | 1:2 / 1:1 / 4:1 |
| TR-01 | Khay quân (4 chiếc) | 1:2 / 1:1 |
| AC-01 | Khay phụ kiện | 1:2 |
| AC-02 | Ổ xúc xắc và nắp che — **ba cao độ**, khe luồn ngón, dao phay | 2:1 / 1:1 / 3:1 |
| QA-01 | Dung sai, đặc tính kiểm bắt buộc, thứ tự lắp, bảng kiểm xuất xưởng | — |

Mối ghép góc thân được chốt trong vòng này (trước đó **không tài liệu nào định nghĩa**):
vách trước/sau **ngậm 5 mm** vào rãnh trên mặt trong vách bản lề + 2 chốt
draw-bore Ø5 mỗi góc; đáy **thả** trong rãnh sâu 6, mộng 4.

`tools/md2html.py` dùng chung CSS với `build/review.html` nên PDF mới và cũ đồng bộ định dạng.

## Rủi ro lớn nhất còn lại

1. **Mộng khung cocobolo.** 8 mộng, gỗ nhiều dầu. Bắt buộc epoxy + lau acetone trong vòng 15 phút kể từ khi
   phay xong má mộng + chốt draw-bore Ø5. Phải ép thử một mộng mẫu, để 7 ngày rồi phá huỷ.
2. **CITES.** Phần pháp lý đã tra lại nhưng cites.org bị chặn trong môi trường chạy, nên toàn bộ là nguồn thứ
   cấp. Đủ để thiết kế tiếp, không đủ để ký hợp đồng.
3. **Lô quân cờ.** Phải đo tối thiểu 20 quân thuộc đúng lô mua trước khi chốt lòng khay.
4. **Va chạm giữa các chi tiết thiết kế rời rạc.** Bản dựng 3D đã bắt được hai vụ mà không script nào
   phát hiện — nam châm nằm trong khe luồn ngón, và khe luồn ngón cộng hốc âm ăn thủng vách trước.
   `box_spec.selfcheck()` nay kiểm chéo, nhưng nguyên tắc là: **dựng hình trước khi lập trình CNC.**
