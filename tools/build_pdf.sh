#!/bin/bash
# Dung PDF tu docs/*.md. Chay: ./tools/build_pdf.sh
set -e
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
b() {  # b <md> <ten-file> <tieu de> <meta...>
  local md=$1 name=$2 title=$3; shift 3
  python3 tools/md2html.py "$md" "build/$name.html" "$title" "$@"
  $CHROME --headless --no-pdf-header-footer --disable-gpu --no-sandbox \
    --print-to-pdf="build/$name.pdf" "build/$name.html" >/dev/null 2>&1
  echo "  build/$name.pdf"
}
b docs/BX-01.md bx01 "BX-01 — Thân hộp" \
  "<b>Bộ hồ sơ:</b> Hộp Mahjong 152 quân, BURLORA · <b>Đơn vị:</b> mm" \
  "<b>Nguồn số:</b> tools/box_spec.py · <b>Hình:</b> tools/draw_bx01.py"
b docs/KHOA-NAP.md khoa-nap "Khóa nắp — nam châm nối nắp với thân" \
  "<b>Bộ hồ sơ:</b> Hộp Mahjong 152 quân, BURLORA · <b>Đơn vị:</b> mm" \
  "<b>Nguồn số:</b> tools/box_spec.py · tools/lid_latch.py · <b>Hình:</b> tools/draw_latch.py"
b docs/CHOT-REV-C.md chot-rev-c "Chốt Rev C — quyết định và hệ quả" \
  "<b>Bộ hồ sơ:</b> Hộp Mahjong 152 quân, BURLORA · <b>Đơn vị:</b> mm" \
  "<b>Nguồn số:</b> tools/box_spec.py"
