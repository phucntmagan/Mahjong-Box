#!/bin/bash
# Xuat bo ban ve san xuat: SVG -> mot PDF nhieu trang kho A3 ngang.
# Chay: ./tools/build_drawings.sh
set -e
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
python3 tools/drawings.py
$CHROME --headless --no-pdf-header-footer --disable-gpu --no-sandbox \
  --print-to-pdf="build/BAN-VE-SAN-XUAT.pdf" build/ban-ve.html >/dev/null 2>&1
echo "  build/BAN-VE-SAN-XUAT.pdf"
# PNG tung to de xem nhanh
PY=$(command -v python3)
if ! $PY -c "import PIL" 2>/dev/null; then
  VDIR="${SCRATCH:-${TMPDIR:-/tmp}}/mahjong-figs-venv"
  [ -x "$VDIR/bin/python" ] || { $PY -m venv "$VDIR" && "$VDIR/bin/pip" -q install Pillow; }
  PY="$VDIR/bin/python"
fi
for f in build/ban-ve/*.svg; do
  n=$(basename "$f" .svg)
  printf '<!doctype html><meta charset="utf-8"><style>body{margin:0}img{display:block}</style><img src="../%s" width="1587">' "$f" > build/_d.html
  $CHROME --headless --disable-gpu --no-sandbox --screenshot="build/ban-ve/$n.png" \
    --window-size=1587,1243 --hide-scrollbars --virtual-time-budget=6000 build/_d.html >/dev/null 2>&1
  $PY -c "from PIL import Image; Image.open('build/ban-ve/$n.png').crop((0,0,1587,1123)).save('build/ban-ve/$n.png')"
  echo "  build/ban-ve/$n.png"
done
rm -f build/_d.html
