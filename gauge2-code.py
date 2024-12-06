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
channel_d = label.Label(
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
    anchored_position = (140, 50)
)

channel_d.text = str("AFR1")

value_d_max = 1.02
value_d_min = 0.75

value_d = label.Label(
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
    anchored_position = (110, 125)
)

unit_d = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=1,
    base_alignment=True,
    anchor_point = (0.5, 0),
    anchored_position = (150, 210)
)

#gauge_d_bkgd_width = 10

unit_d.text = str("lambda")

gauge_d_frame = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x = 200,
    y = 0,
    width = 40,
    height = 480,
    color_index = 3
    )

gauge_d_bkgd = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x = 205,
    y = 0,
    width = 30,
    height = 240,
    color_index = 2
    )

channel_e = label.Label(
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
    anchored_position = (345, 50)
)

channel_e.text = str("AFR2")

value_e_max = 1.02
value_e_min = 0.75

value_e = label.Label(
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
    anchored_position = (370, 125)
)

unit_e = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=1,
    base_alignment=True,
    anchor_point = (0.5, 0),
    anchored_position = (330, 210)
)

#gauge_e_bkgd_width = 240

unit_e.text = str("lambda")

gauge_e_frame = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x = 240,
    y = 0,
    width = 40,
    height = 480,
    color_index = 3
    )

gauge_e_bkgd = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x = 245,
    y = 0,
    width = 30,
    height = 240,
    color_index = 2
    )


lower_divider = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x = 0,
    y = 235,
    width = 480,
    height = 10,
    color_index = 3
    )

channel_f = label.Label(
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

channel_f.text = str("FuelP")

value_f_max = 400
value_f_min = 180

value_f = label.Label(
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

unit_f = label.Label(
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

unit_f.text = str("kPa")

channel_g = label.Label(
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

channel_g.text = str("OilP")

value_g_max = 300
value_g_min = 100

value_g = label.Label(
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

unit_g = label.Label(
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

unit_g.text = str("kPa")

main_group.append(lower_divider)
main_group.append(channel_d)
main_group.append(unit_d)
main_group.append(value_d)
main_group.append(gauge_d_frame)
main_group.append(gauge_d_bkgd)
main_group.append(channel_e)
main_group.append(unit_e)
main_group.append(value_e)
main_group.append(gauge_e_frame)
main_group.append(gauge_e_bkgd)
main_group.append(channel_f)
main_group.append(unit_f)
main_group.append(value_f)
main_group.append(channel_g)
main_group.append(unit_g)
main_group.append(value_g)


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
        afr1 = round((packet_int / 150) + 0.5,2)
        afr2 = round((packet_int / 150) + 0.55,2)
        fuelp = int(packet_int * 4)
        oilp = int(packet_int * 5)
        value_d.text = str(afr1)
        value_e.text = str(afr2)
        value_f.text = str(fuelp)
        value_g.text = str(oilp)
        gauge_d_bkgd.height = int((afr1/1.5) * 480)
        gauge_d_bkgd.y = int(480 - gauge_d_bkgd.height)
        gauge_e_bkgd.height = int((afr2/1.5) * 480)
        gauge_e_bkgd.y = int(480 - gauge_e_bkgd.height)

        if afr1 <= value_d_min:
            value_d.color=0x0000ff
            gauge_d_bkgd.color_index = 2
        if value_d_min < afr1 < value_d_max:
            value_d.color=0xffffff
            gauge_d_bkgd.color_index = 4
        if afr1 >= value_d_max:
            value_d.color=0xff0000
            gauge_d_bkgd.color_index = 0

        if afr2 <= value_e_min:
            value_e.color=0x0000ff
            gauge_e_bkgd.color_index = 2
        if value_e_min < afr2 < value_e_max:
            value_e.color=0xffffff
            gauge_e_bkgd.color_index = 4
        if afr2 >= value_e_max:
            value_e.color=0xff0000
            gauge_e_bkgd.color_index = 0

        if fuelp <= value_f_min:
            value_f.color=0xff0000
        if value_f_min < fuelp < value_f_max:
            value_f.color=0xffffff
        if fuelp >= value_f_max:
            value_f.color=0xff0000

        if oilp <= value_g_min:
            value_g.color=0xff0000
        if value_g_min < oilp < value_g_max:
            value_g.color=0xffffff
        if oilp >= value_g_max:
            value_g.color=0xff0000
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


