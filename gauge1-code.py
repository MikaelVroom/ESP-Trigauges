#v2
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
channel_a = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=2,
    base_alignment=True,
    anchor_point = (0.5, 0),
    anchored_position = (80, 150)
)

channel_a.text = str("MAP")

value_a_max = 220
value_a_min = 15
value_a = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=7,
    base_alignment=True,
    anchor_point = (0.5, 0),
    anchored_position = (240, 50)
)

unit_a = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=2,
    base_alignment=True,
    anchor_point = (0.5, 0),
    anchored_position = (390, 150)
)

gauge_a_bkgd_width = 240

unit_a.text = str("kPa")

gauge_a_frame = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x = 0,
    y = 220,
    width = 470,
    height = 40,
    color_index = 3
    )

gauge_a_bkgd = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x = 0,
    y = 225,
    width = 240,
    height = 30,
    color_index = 2
    )

lower_divider = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x = 235,
    y = 240,
    width = 10,
    height = 240,
    color_index = 3
    )

channel_b = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=2,
    base_alignment=True,
    anchor_point = (0.5, 0),
    anchored_position = (120, 270)
)

channel_b.text = str("CLT")

value_b_max = 195
value_b_min = 100
value_b = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=4,
    base_alignment=True,
    anchor_point = (0.5, 0),
    anchored_position = (120, 320)
)

unit_b = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=2,
    base_alignment=True,
    anchor_point = (0.5, 0),
    anchored_position = (160, 400)
)

unit_b.text = str("degF")

channel_c = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=2,
    base_alignment=True,
    anchor_point = (0.5, 0),
    anchored_position = (360, 270)
)

channel_c.text = str("IAT")

value_c_max = 120
value_c_min = 0
value_c = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=4,
    base_alignment=True,
    anchor_point = (0.5, 0),
    anchored_position = (360, 320)
)

unit_c = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=2,
    base_alignment=True,
    anchor_point = (0.5, 0),
    anchored_position = (320, 400)
)

unit_c.text = str("degF")

main_group.append(channel_a)
main_group.append(unit_a)
main_group.append(value_a)
main_group.append(gauge_a_frame)
main_group.append(lower_divider)
main_group.append(gauge_a_bkgd)
main_group.append(channel_b)
main_group.append(unit_b)
main_group.append(value_b)
main_group.append(channel_c)
main_group.append(unit_c)
main_group.append(value_c)


#print(f"My MAC address: {[hex(i) for i in wifi.radio.mac_address]}")

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
        #print("Decoded: " + packet_decoded)
        packet_float = float(packet_decoded)
        #print("Str: " + str(packet_float))
        packet_int = int(packet_float)
        print("Int: " + str(packet_int))
        map_val = int(packet_int * 2.4)
        clt = int(packet_int * 2.2)
        iat = int(packet_int * 1.6)
        value_a.text = str(map_val)
        value_b.text = str(clt)
        value_c.text = str(iat)
        gauge_a_bkgd.width = int((packet_int/100) * 480)
        if map_val <= value_a_min:
            value_a.color=0x0000ff
            gauge_a_bkgd.color_index = 2
        if value_a_min < map_val < value_a_max:
            value_a.color=0xffffff
            gauge_a_bkgd.color_index = 4
        if map_val >= value_a_max:
            value_a.color=0xff0000
            gauge_a_bkgd.color_index = 0
        if clt <= value_b_min:
            value_b.color=0x0000ff
        if value_b_min < clt < value_b_max:
            value_b.color=0xffffff
        if clt >= value_b_max:
            value_b.color=0xff0000
        if iat <= value_c_min:
            value_c.color=0x0000ff
        if value_c_min < iat < value_c_max:
            value_c.color=0xffffff
        if iat >= value_c_max:
            value_c.color=0xff0000
print("packets:", f"length={len(packets)}")
for packet in packets:
    print(packet)


#while True:
#    for i in range(0, 101):
#        example_gauge.level = i
#        example_gauge_2.level = i
#        example_gauge_3.level = i/2
#        if i <= 75:
#            example_gauge.foreground_color = 0x00ff00
#            example_gauge_2.foreground_color = 0x00fd00
#            example_gauge_3.foreground_color = 0x00fd50
#        if i > 75:
#            example_gauge.foreground_color = 0xff0000
#            example_gauge_2.foreground_color = 0xfffd00
#            example_gauge_3.foreground_color = 0xfffd50
#        text_area.text = str(i)
#        time.sleep(0.001)




