import os
import ssl
import wifi
import socketpool
import adafruit_requests
import board
import displayio
import vectorio
from displayio import Bitmap
from adafruit_io.adafruit_io import IO_HTTP
import keypad
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_qualia.graphics import Graphics, Displays
import espnow

key = keypad.Keys((board.A0,), value_when_pressed=False, pull=True)

aio_username = os.getenv('ADAFRUIT_AIO_USERNAME')
aio_key = os.getenv('ADAFRUIT_AIO_KEY')

pointer_pal = displayio.Palette(5)
pointer_pal[0] = 0xff0000
pointer_pal[1] = 0x000000
pointer_pal[2] = 0x0000ff
pointer_pal[3] = 0xffffff
pointer_pal[4] = 0x00ff00

context = ssl.create_default_context()
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, context)
io = IO_HTTP(aio_username, aio_key, requests)

graphics = Graphics(Displays.ROUND21, default_bg=None, auto_refresh=True)

main_group = displayio.Group()

font = bitmap_font.load_font("fonts/LeagueSpartan-Bold-16.bdf", Bitmap)

def center(grid, bitmap):
    # center the image
    grid.x -= graphics.display.width // 2
    grid.y -= graphics.display.height // 2

graphics.display.root_group = main_group

color_bitmap = displayio.Bitmap(480, 480, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
main_group.append(bg_sprite)

text = str("ini")

channel_h = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=2,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(140, 50)
)

channel_h.text = str("MPG")

value_h_max = 40
value_h_min = 0

value_h = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=4,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(110, 125)
)

unit_h = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=1,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(150, 210)
)

unit_h.text = str("avg")

gauge_i_frame = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x=215,
    y=0,
    width=50,
    height=480,
    color_index=3
    )

gauge_i_bkgd = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x=225,
    y=0,
    width=30,
    height=240,
    color_index=2
    )

lower_divider = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x=0,
    y=238,
    width=480,
    height=4,
    color_index=3
    )

div_1 = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x=215,
    y=418,
    width=50,
    height=4,
    color_index=3
    )

div_2 = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x=215,
    y=298,
    width=50,
    height=4,
    color_index=3
    )

div_3 = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x=215,
    y=178,
    width=50,
    height=4,
    color_index=3
    )

div_4 = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x=215,
    y=58,
    width=50,
    height=4,
    color_index=3
    )

knock_block = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x=240,
    y=240,
    width=240,
    height=240,
    color_index=1
    )

channel_j = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=2,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(345, 50)
)

channel_j.text = str("Ign")

value_j_max = 80
value_j_min = -20

value_j = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=4,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(370, 125)
)

unit_j = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=1,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(330, 210)
)

unit_j.text = str("deg BTDC")

channel_k = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=2,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(120, 260)
)

channel_k.text = str("Flex")

value_k_max = 100
value_k_min = 0

value_k = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=4,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(120, 320)
)

unit_k = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=1,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(150, 400)
)

unit_k.text = str("% ethanol")

mpg_scale_1 = label.Label(
    font=font,
    text="10",
    color=0x000000,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=1,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(240, 360)
)

mpg_scale_2 = label.Label(
    font=font,
    text="20",
    color=0x000000,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=1,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(240, 240)
)

mpg_scale_3 = label.Label(
    font=font,
    text= "30",
    color=0x000000,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=1,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(240, 120)
)

channel_l = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=2,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(360, 260)
)

channel_l.text = str("Knock")

value_k1_max = 0
value_k1_min = -2

value_k1 = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=4,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(360, 320)
)

main_group.append(knock_block)
main_group.append(lower_divider)
main_group.append(channel_h)
main_group.append(unit_h)
main_group.append(value_h)
main_group.append(gauge_i_frame)
main_group.append(gauge_i_bkgd)
main_group.append(channel_j)
main_group.append(unit_j)
main_group.append(value_j)
main_group.append(channel_k)
main_group.append(unit_k)
main_group.append(value_k)
main_group.append(div_1)
main_group.append(div_2)
main_group.append(div_3)
main_group.append(div_4)
main_group.append(mpg_scale_1)
main_group.append(mpg_scale_2)
main_group.append(mpg_scale_3)
main_group.append(channel_l)
main_group.append(value_k1)


# print(f"My MAC address: {[hex(i) for i in wifi.radio.mac_address]}")

print(f"Connecting to {os.getenv('CIRCUITPY_WIFI_SSID')}")
wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
print(f"Connected to {os.getenv('CIRCUITPY_WIFI_SSID')}")
print(f"My IP address: {wifi.radio.ipv4_address}")

e = espnow.ESPNow()
packets = []

print("starting listen")

while True:
    if e:
        print("Reading packet:")
        packet = e.read()
#        packets.append(packet)
        print(packet.msg)
        if packet.msg == b'end':
            break
        contents = packet.msg
        packet_decoded = contents.decode('utf-8')
#        print("Decoded: " + packet_decoded)
        packet_float = float(packet_decoded)
#        print("Str: " + str(packet_float))
        packet_int = int(packet_float)
        print("Int: " + str(packet_int))
        mpgavg = round((packet_int / 10.1) + 15, 1)
        mpginst = (packet_int / 2.5)
        ign = round((packet_int / 2.51) - 10, 1)
        flex = packet_int
        k1 = round((packet_int / 25) - 4, 1)
        k2 = round((packet_int / 25.1) - 4, 1)
        k3 = round((packet_int / 25.2) - 4, 1)
        k4 = round((packet_int / 25.3) - 4, 1)
        k5 = round((packet_int / 25.4) - 4, 1)
        k6 = round((packet_int / 25.5) - 4, 1)
        knock_levels = [k1,k2,k3,k4,k5,k6]
        max_knock = max(knock_levels)
        value_h.text = str(mpgavg)
        value_j.text = str(ign)
        value_k.text = str(flex)
        gauge_i_bkgd.height = int((mpginst/40) * 480)
        gauge_i_bkgd.y = int(480 - gauge_i_bkgd.height)
        value_k1.text = str(max_knock)

        if max_knock <= value_k1_min:
            knock_block.color_index = 0
        if max_knock > value_k1_min:
            knock_block.color_index = 1
print("packets:", f"length={len(packets)}")
for packet in packets:
    print(packet)