#!/usr/bin/env python3
"""
Sinh PROMPT dung de yeu cau mot cong cu tao anh dung anh 3D "vat lieu that"
cua hop. Chay: python3 tools/render_prompt.py > docs/PROMPT-RENDER.md

Vi sao la SCRIPT chu khong phai mot file md go tay: prompt nay mo ta hinh hoc
bang so. Neu dac ta doi ma prompt khong doi thi prompt tro thanh mot loi noi
doi ve chinh san pham. Moi tri so duoi day lay tu box_spec.derive().
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box_spec as B

S = B.derive()
DL = B.dice_layout(S)
M_CORE = B.mass_of(S, 'loi on dinh')[2]
KN_BARREL = 2*S['R_KN']
N_TRAY = 2*B.N_STACK
TILES_PER_TRAY = B.N_TILES // 4 - 2          # 36 quan moi khay (8 con lai o ranh Joker)

print(f'''# Prompt dựng ảnh 3D vật liệu thật

Sinh bởi `tools/render_prompt.py` từ `tools/box_spec.py`. **Không sửa số bằng tay** —
chạy lại script sau mỗi lần đặc tả đổi.

Cách dùng: dán khối **A** trước (một lần, để công cụ nắm vật thể), rồi dán từng khối
**B1…B5** cho từng góc nhìn. Nếu công cụ nhận ảnh, **đính kèm `figs/fig12a-tong-the-nap-dong.png`
làm tham chiếu hình học** và nói rõ: *hình đó đúng hình học nhưng sai vật liệu; giữ hình,
thay vật liệu*. Đó là cách rẻ nhất để nó không tự bịa tỉ lệ.

Prompt viết bằng tiếng Anh vì mọi mô hình dựng ảnh đều ăn tiếng Anh chắc tay hơn.

---

## A · Khối mô tả vật thể (dán một lần)

```
A hand-made solid-wood Mahjong case for {B.N_TILES} tiles, in the spirit of a Hermès
game box: quiet, no ornament, all of the interest in the wood itself.

OVERALL
{S["X_OA"]:.1f} x {S["Y_OA"]:.0f} x {S["Z_OA"]:.0f} mm (W x D x H), about {M_CORE:.1f} kg. The body is
{S["W"]:.0f} wide; the only thing that breaks the rectangular envelope is the row of
wooden hinge barrels, which stand {S["PROUD"]:.1f} mm proud on each side edge.

MATERIALS — this is the whole point of the picture, get the wood right
- Body, trays, lid frames, hinge knuckles and pins: COCOBOLO (Dalbergia retusa).
  Deep orange-red through burgundy to chocolate brown, with irregular near-black
  streaks that wander across the board. Very dense, oily, fine-pored, almost no
  visible open grain. Hand-planed and polished to a SATIN sheen with strong
  chatoyance — the light travels in the fibre when the surface turns. Never a
  plastic or lacquered gloss. Colour and figure differ from part to part, as real
  boards do. Grain runs lengthwise on every component.
- The two lid panels: AFZELIA XYLOCARPA BURL (Vietnamese "nu go do").
  Warm golden amber to honey brown, a dense cluster of small burl eyes and
  swirling figure, no straight grain anywhere. Clearly LIGHTER and more golden
  than the cocobolo frame around it — that contrast is the design.
- Finish: hand-rubbed oil then wax. Satin, open pore, no film build.
  Exposed edges eased R0.5, not chamfered, not moulded.
- Corners: the front and back walls are housed into the side walls, so from the
  outside each side wall runs unbroken past the corner and the joint reads as one
  fine vertical line. No mitre, no exposed end grain, NO DOVETAILS, no finger
  joints, no visible pins or splines on the outside.

LID — two leaves, each {S["LW"]:.2f} x {B.LID_L:.0f} x {B.T_LID:.0f} mm
- Solid cocobolo frame: stiles {B.STILE:.0f} wide, rails {B.RAIL:.0f} wide, square corners.
- A raised burl panel {S["PAN_W"]:.1f} x {S["PAN_L"]:.0f} sits in the frame with its field
  FLUSH with the frame face — the top of the case is one continuous plane.
  A {B.PAN_REV:.1f} mm reveal gap runs all round the panel field and reads as a fine
  shadow line. The panel is not glued; it floats.
- The two leaves meet along the centre with a {B.SEAM:.1f} mm seam running front to back.
  No cover strip over the seam, no lock, no catch, no handle, nothing on the top.

HINGE — ALL WOOD, this is a hard constraint
- {B.N_KN} knuckles per side, each {B.KN_LEN:.0f} mm long at {S["KN_PITCH"]:.0f} pitch, total run
  {S["KN_RUN"]:.0f} mm centred on the {B.LID_L:.0f} mm edge.
- Each knuckle is a turned wooden barrel of diameter {KN_BARREL:.1f} mm whose axis lies
  exactly on the outer top arris of the case. So the side edge reads as a row of
  {B.N_KN} short wooden barrels, half-buried in the edge, standing {S["PROUD"]:.1f} mm proud.
- Two wooden pins of diameter {B.KN_PIN:.0f} mm and {B.KN_PIN_L:.0f} mm long run hidden along the
  hinge axis on each side.
- NO brass, NO steel, NO piano hinge, NO screws, NO visible fastener of any kind.

TWO-HAND GRIP POCKETS — there is no handle
- One pocket cut into each side wall, centred on the depth: {B.GRIP_W:.0f} mm long,
  {B.GRIP_D:.0f} mm deep into the {S["WALL_HINGE"]:.0f} mm wall, opening {S["GRIP_APER"]:.1f} mm tall,
  its floor level with the inside floor of the case.
- Its ceiling is not flat: a generous R{B.GRIP_R:.0f} bullnose at the outer lip, then a
  {B.GRIP_SLOPE:.0f} degree slope upward and inward. Fingers hook this bullnose.
- Above each pocket a {S["GRIP_LEDGE"]:.1f} mm band of solid wood carries the load.

FEET: {B.FOOT:.0f} mm dark pads, inset from the edges, barely noticed.

INTERIOR — only when the shot shows it
- Two bays, each holding two stacked trays: {N_TRAY} cocobolo trays
  {B.TRAY[0]:.0f} x {B.TRAY[1]:.0f} x {B.TRAY_H:.0f}, each with {TILES_PER_TRAY} tiles standing on edge,
  wells felt-lined in a deep oxblood red.
- {B.N_TILES} tiles {B.TILE_MAX[0]:.1f} x {B.TILE_MAX[1]:.1f} x {B.TILE_MAX[2]:.1f}, warm bone white,
  faces up, carved and coloured in the traditional way.
- Centre bay: one accessory tray {S["AC_L"]:.0f} x {S["AC_W_OUT"]:.0f} x {B.AC_H:.0f} carrying a
  Joker groove {B.AC_JOKER[0]:.0f} x {B.AC_JOKER[1]:.0f}, four dice sockets {B.DICE_SOCK:.0f} x {B.DICE_SOCK:.0f}
  under a flush drop-in cocobolo cover {S["COVER_L"]:.1f} x {S["COVER_W"]:.1f} x {B.COVER_T:.0f} with two
  half-round finger notches of diameter {B.COVER_NOTCH:.0f}, and a spare-tile well.
- The inside face of each lid leaf is a shallow tray — that is where discards go.

MUST NOT APPEAR
metal hinge of any kind, piano hinge, brass barrel hinge, screws, nails, hasp,
lock, latch, clasp, handle, carrying strap, turned legs, high-gloss or lacquered
or plastic surface, veneer seams, book-matched figure on the frame parts, printed
or repeating grain, moulded or chamfered edge profiles, engraving, inlay, logo,
branding, drawer pulls, a third leaf, a hinge on the front edge.

PHOTOGRAPHY
Studio product photograph. One large soft key from upper left at about 40 degrees
elevation, gentle fill on the right, one soft rim light to catch the polished
arris and the hinge barrels. Neutral warm-grey seamless or a fine matte stone
slab, no props, no styling. 50-85 mm equivalent, f/8 so the whole case is sharp,
slight vignette. Colour accurate, no heavy grade, no teal-orange.
Photoreal photograph — not a CAD render, no wireframe, no shading facets, no
tessellation grid, no measurement lines.
```

---

## B1 · Tổng thể, nắp đóng

```
Three-quarter view of the closed case from the front left, camera about 25 degrees
above the top plane. Show the whole top (both leaves, the {B.SEAM:.1f} mm centre seam, both
burl panels flush in their frames), the front wall, and the left side wall with the
row of {B.N_KN} wooden hinge barrels along its top arris and the grip pocket reading as a
dark horizontal slot below them. The case sits closed on a neutral surface.
```

## B2 · Nắp mở phẳng 180°

```
The case opened flat on a table, seen from about 45 degrees above and slightly to
the front. Both leaves lie fully open at 180 degrees, one to the left and one to the
right, their top faces up and level with the rim of the body, so the whole thing
reads as three panels at the same height, about {S["X_OA"] + 2*S["LW"]:.0f} mm wide overall.
The body between them is full of tiles. The wooden hinge barrels are visible along
both joints, still the only thing at those edges.
```

## B3 · Lòng hộp, tháo nắp

```
The body alone, lid removed, three-quarter view from above. Two bays of ivory tiles
standing on edge in cocobolo trays, and the accessory tray down the middle with the
Joker groove, the flush dice cover in place, and the spare-tile well. Warm raking
light so the tile faces catch a highlight and the tray walls show cocobolo figure.
```

## B4 · Cận cảnh vách bên: bản lề mộng gỗ + hốc âm

```
Macro of one side wall, camera low and close, raking light from the left. In frame:
the row of {B.N_KN} turned wooden hinge barrels of diameter {KN_BARREL:.1f} mm along the top arris,
each {B.KN_LEN:.0f} mm long with a {B.KN_GAP:.0f} mm gap to the next, and below them the grip pocket —
opening {S["GRIP_APER"]:.1f} mm tall, its outer lip a soft R{B.GRIP_R:.0f} bullnose, the inside of the
pocket falling into shadow. Show that every part of the hinge is wood: end grain on
the barrels, the same cocobolo figure running through them. No metal anywhere.
```

## B5 · Bàn tay xách hai bên

```
The closed case being carried, one hand hooked into the grip pocket on each side,
fingers curled over the R{B.GRIP_R:.0f} bullnose inside the pocket, the case level. Hands only,
neutral skin, no cuffs or jewellery, plain background. This shot exists to show that
the case has no handle and none is needed.
```

---

## Kiểm ảnh nó trả về

Sáu điều dưới đây là chỗ mọi công cụ dựng ảnh sai. Nhìn đúng sáu chỗ này trước khi
nhận ảnh:

| # | Nhìn cái gì | Đúng là |
|---|---|---|
| 1 | Bản lề | {B.N_KN} ống **gỗ** trên sống cạnh. Thấy đồng, thép, bản lề lá, ốc vít → loại |
| 2 | Mặt nắp | Tấm nu **ngang bằng** mặt khung, chỉ có khe {B.PAN_REV:.1f} chạy quanh. Thấy tấm thụt xuống hay nổi lên → loại |
| 3 | Khe ráp giữa | Một khe {B.SEAM:.1f} chạy suốt trước–sau, **không** có nẹp che, không khoá |
| 4 | Vách bên | Một rãnh ngang dài {B.GRIP_W:.0f}, cao {S["GRIP_APER"]:.1f}. Thấy quai xách → loại |
| 5 | Vật liệu | Khung đỏ sẫm vân đen (cocobolo) **tương phản rõ** với tấm nu vàng mật. Cùng một màu → loại |
| 6 | Bề mặt | Satin, sâu, ánh vân chuyển theo góc. Bóng gương như sơn PU → loại |

Nếu sai chỗ nào, đừng viết lại cả prompt — dán đúng dòng tương ứng ở bảng trên kèm
câu *"fix only this, keep everything else"*.

## Chỗ prompt này cố ý không nói

- **Nam châm khoá nắp** ({2*S["MAG_N_LEAF"]} cặp {B.MAG[0]:.0f} x {B.MAG[1]:.0f} x {B.MAG[2]:.0f}) nằm âm trong vành thân và
  mặt trong nắp, phủ gỗ, **không nhìn thấy** — nói ra chỉ khiến công cụ vẽ thêm chi
  tiết kim loại không có thật.
- **Dung sai, mộng, chốt draw-bore, chuỗi kích thước bên trong**: không thuộc về một
  tấm ảnh. Chúng ở `build/BAN-VE-SAN-XUAT.pdf`.
- **Màu gỗ chính xác**: cocobolo và nu gõ đỏ biến thiên rất rộng giữa các tấm. Prompt
  cố tình mô tả dải màu chứ không đưa mã màu — ép một mã màu ra ảnh gỗ giả.
''')
