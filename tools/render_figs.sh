#!/bin/bash
# Render SVG -> PNG. Cua so phai CAO HON SVG roi crop, neu khong Chromium cat mat day.
set -e
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
VENV=/tmp/claude-0/-home-user-Mahjong-Box/c895b263-5c9c-5e62-8a1f-70bdc49db222/scratchpad/venv/bin/python
for f in figs/*.svg; do
  n=$(basename "$f" .svg)
  W=$(grep -o 'width="[0-9]*"' "$f" | head -1 | grep -o '[0-9]*')
  H=$(grep -o 'height="[0-9]*"' "$f" | head -1 | grep -o '[0-9]*')
  printf '<!doctype html><meta charset="utf-8"><style>body{margin:0}img{display:block}</style><img src="../%s" width="%s">' "$f" "$W" > build/_r.html
  $CHROME --headless --disable-gpu --no-sandbox --screenshot="figs/$n.png" \
    --window-size=$W,$((H+120)) --hide-scrollbars --virtual-time-budget=6000 build/_r.html >/dev/null 2>&1
  $VENV -c "from PIL import Image; Image.open('figs/$n.png').crop((0,0,$W,$H)).save('figs/$n.png')"
  echo "  $n.png  ${W}x${H}"
done
rm -f build/_r.html
