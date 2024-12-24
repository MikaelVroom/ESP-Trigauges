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

pointer_pal = displayio.Palette(7)
pointer_pal[0] = 0xff0000 #red
pointer_pal[1] = 0x000000 #black
pointer_pal[2] = 0x0000ff #blue
pointer_pal[3] = 0xffffff #white
pointer_pal[4] = 0x00ff00 #green
pointer_pal[5] = 0xffff00 #yellow
pointer_pal[6] = 0xffbb00 #orange

context = ssl.create_default_context()
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, context)
io = IO_HTTP(aio_username, aio_key, requests)

graphics = Graphics(Displays.ROUND21, default_bg=None, auto_refresh=True)

screen_1 = displayio.Group()
screen_2 = displayio.Group()
screen_3 = displayio.Group()

font = bitmap_font.load_font("fonts/LeagueSpartan-Bold-16.bdf", Bitmap)

def center(grid, bitmap):
    # center the image
    grid.x -= graphics.display.width // 2
    grid.y -= graphics.display.height // 2

graphics.display.root_group = screen_3

color_bitmap = displayio.Bitmap(480, 480, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
#main_group.append(bg_sprite)

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
    anchored_position = (70, 175)
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
    anchored_position = (240, 35)
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
    anchored_position = (400, 175)
)

state_a = label.Label(
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
    anchored_position = (240, 175)
)

target_a = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x = 0,
    y = 225,
    width = 15,
    height = 30,
    color_index = 5
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

channel_b = label.Label(
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
    anchored_position = (90, 270)
)

channel_b.text = str("CLT")

value_b_max = 220
value_b_min = 100
value_b = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=3,
    base_alignment=True,
    anchor_point = (0.5, 0),
    anchored_position = (90, 300)
)

unit_b = label.Label(
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
    anchored_position = (90, 360)
)

unit_b.text = str("degF")

channel_bb = label.Label(
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
    anchored_position = (240, 270)
)

channel_bb.text = str("Flex")

value_bb_max = 100
value_bb_min = 0
value_bb = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=3,
    base_alignment=True,
    anchor_point = (0.5, 0),
    anchored_position = (240, 300)
)

channel_c = label.Label(
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
    anchored_position = (390, 270)
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
    scale=3,
    base_alignment=True,
    anchor_point = (0.5, 0),
    anchored_position = (390, 300)
)

unit_c = label.Label(
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
    anchored_position = (390, 360)
)

unit_c.text = str("degF")

channel_cc = label.Label(
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
    anchored_position = (240, 380)
)

channel_cc.text = str("Fan")

value_cc_max = 100
value_cc_min = 0
value_cc = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=3,
    base_alignment=True,
    anchor_point = (0.5, 0),
    anchored_position = (240, 410)
)

screen_1.append(channel_a)
screen_1.append(unit_a)
screen_1.append(value_a)
screen_1.append(state_a)
screen_1.append(gauge_a_frame)
screen_1.append(gauge_a_bkgd)
screen_1.append(target_a)
screen_1.append(channel_b)
screen_1.append(unit_b)
screen_1.append(value_b)
screen_1.append(channel_bb)
screen_1.append(value_bb)
screen_1.append(channel_c)
screen_1.append(unit_c)
screen_1.append(value_c)
screen_1.append(channel_cc)
screen_1.append(value_cc)

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
    anchor_point=(0.5, 0),
    anchored_position=(140, 50)
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
    anchor_point=(0.5, 0),
    anchored_position=(110, 125)
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
    anchor_point=(0.5, 0),
    anchored_position=(150, 210)
)

unit_d.text = str("lambda")

gauge_d_frame = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x=200,
    y=0,
    width=40,
    height=480,
    color_index=3
    )

gauge_d_bkgd = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x=205,
    y=0,
    width=30,
    height=240,
    color_index=2
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
    anchor_point=(0.5, 0),
    anchored_position=(345, 50)
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
    anchor_point=(0.5, 0),
    anchored_position=(370, 125)
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
    anchor_point=(0.5, 0),
    anchored_position=(330, 210)
)

unit_e.text = str("lambda")

gauge_e_frame = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x=240,
    y=0,
    width=40,
    height=480,
    color_index=3
    )

gauge_e_bkgd = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x=245,
    y=0,
    width=30,
    height=240,
    color_index=2
    )

gauge_ee = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x=215,
    y=240,
    width=50,
    height=10,
    color_index=1
    )

lower_divider = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x=0,
    y=238,
    width=480,
    height=4,
    color_index=3
    )

channel_f = label.Label(
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
    anchored_position=(30, 260)
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
    scale=2,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(110, 260)
)

unit_f = label.Label(
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
    anchored_position=(175, 260)
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
    scale=1,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(40, 310)
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
    scale=2,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(110, 310)
)

unit_g = label.Label(
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
    anchored_position=(175, 310)
)

unit_g.text = str("kPa")

channel_gg = label.Label(
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

channel_gg.text = str("Ign")

value_gg = label.Label(
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
    anchored_position=(360, 330)
)

knock_block2 = vectorio.Rectangle(
    pixel_shader=pointer_pal,
    x=240,
    y=240,
    width=240,
    height=240,
    color_index=1
    )

screen_2.append(lower_divider)
screen_2.append(knock_block2)
screen_2.append(channel_d)
screen_2.append(unit_d)
screen_2.append(value_d)
screen_2.append(gauge_d_frame)
screen_2.append(gauge_d_bkgd)
screen_2.append(channel_e)
screen_2.append(unit_e)
screen_2.append(value_e)
screen_2.append(gauge_e_frame)
screen_2.append(gauge_e_bkgd)
screen_2.append(gauge_ee)
screen_2.append(channel_f)
screen_2.append(unit_f)
screen_2.append(value_f)
screen_2.append(channel_g)
screen_2.append(unit_g)
screen_2.append(value_g)
screen_2.append(channel_gg)
screen_2.append(value_gg)

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

channel_j.text = str("Spd")

value_j_max = 80
value_j_min = 0

value_j = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=3,
    base_alignment=True,
    anchor_point=(0, 0),
    anchored_position=(290, 100)
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
    anchored_position=(440, 155)
)

unit_j.text = str("mph")

state_jj = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=1,
    base_alignment=True,
    anchor_point=(0, 0),
    anchored_position=(380, 210)
)

state_jj.text = str("Spd")

value_jj = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=3,
    base_alignment=True,
    anchor_point=(0, 0),
    anchored_position=(290, 180)
)

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

channel_k.text = str("Throttle")

value_k = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=3,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(120, 300)
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
    anchored_position=(190, 320)
)

unit_k.text = str("TPS")

value_kk = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=3,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(120, 360)
)

unit_kk = label.Label(
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
    anchored_position=(190, 380)
)

unit_kk.text = str("APS")

state_k = label.Label(
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
    anchored_position=(160, 420)
)

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

channel_l.text = str("Launch")

value_l = label.Label(
    font=font,
    text=text,
    color=0xFFFFFF,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=3,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(360, 320)
)

state_l = label.Label(
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
    anchored_position=(320, 420)
)


value_k1_max = 0
value_k1_min = -2

#value_k1 = label.Label(
#    font=font,
#    text=text,
#    color=0xFFFFFF,
#    padding_left=2,
#    padding_right=2,
#    padding_top=2,
#    padding_bottom=2,
#    scale=4,
#    base_alignment=True,
#    anchor_point=(0.5, 0),
#    anchored_position=(360, 320)
#)

screen_3.append(lower_divider)
screen_3.append(channel_h)
screen_3.append(unit_h)
screen_3.append(value_h)
screen_3.append(gauge_i_frame)
screen_3.append(gauge_i_bkgd)
screen_3.append(channel_j)
screen_3.append(unit_j)
screen_3.append(state_jj)
screen_3.append(value_jj)
screen_3.append(value_j)
screen_3.append(channel_k)
screen_3.append(unit_k)
screen_3.append(value_k)
screen_3.append(unit_kk)
screen_3.append(value_kk)
screen_3.append(state_k)
screen_3.append(div_1)
screen_3.append(div_2)
screen_3.append(div_3)
screen_3.append(div_4)
screen_3.append(mpg_scale_1)
screen_3.append(mpg_scale_2)
screen_3.append(mpg_scale_3)
screen_3.append(channel_l)
screen_3.append(value_l)
screen_3.append(state_l)
#screen_3.append(value_k1)


# print(f"My MAC address: {[hex(i) for i in wifi.radio.mac_address]}")

print(f"Connecting to {os.getenv('CIRCUITPY_WIFI_SSID')}")
wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
print(f"Connected to {os.getenv('CIRCUITPY_WIFI_SSID')}")
print(f"My IP address: {wifi.radio.ipv4_address}")

e = espnow.ESPNow()
packets = []

map_kpa = 0
map_tar = 0
boost_state = 0
boost_states = ["Off", "RPM Lock", "MAP Lock", "Open Loop", "Dome", "DB", "Stg2", "Stg3", "Clamp", "Map Lim", "Stg1", ]
boost_colors = [0xffffff, 0xffbb00, 0xffbb00, 0xffbb00, 0xffbb00, 0xffbb00, 0x00ff00, 0x00ff00, 0xffbb00, 0xffbb00, 0x00ff00]
flex_perc = 0
fan_perc = 0

iat = 0
ect = 0
mpg_avg = 0
mpg_avg_last = 1
mpg_inst = 0

lambda1 = 0
lambda2 = 0
lambda_tar = 0

fuel_kpa = 0
fuel_tar = 0
fuel_pwm = 0
oil_kpa = 0

knock_1 = 0
knock_2 = 0
knock_3 = 0
knock_4 = 0
knock_5 = 0
knock_6 = 0

ign_adv = 0
ign_adv_last = 1
tps = 0
aps = 0
idle_state = 0
idle_states = [
    "Startup", 
    "na", 
    "na", 
    "Thr Open", 
    "RPM lock", 
    "RPM tar", 
    "Dash hold", 
    "Dash Decay", 
    "Strt Decay", 
    "Off", 
    "Spd hold", 
    "na",
    "na",
    "na",
    "na",
    "na",
    "Open Loop",
    "na",
    "RPM 0",
    "na",
    "na",
    "na",
    "na",
    "na",
    "Active",
    "MAP hold",
    "ISC OR"
    ]

idle_colors = [
    0xffbb00, 
    0xffbb00, 
    0xffbb00, 
    0xffffff, 
    0xffbb00, 
    0xffbb00, 
    0xffbb00, 
    0xffbb00, 
    0xffbb00, 
    0xffffff, 
    0xffbb00, 
    0xffbb00,
    0xffbb00,
    0xffbb00,
    0xffbb00,
    0xffbb00,
    0xffbb00,
    0xffbb00,
    0xffffff,
    0xffbb00,
    0xffbb00,
    0xffbb00,
    0xffbb00,
    0xffbb00,
    0x00ff00,
    0xffbb00,
    0xffbb00
    ]

vvt_int_tar = 0
vvt_exh_tar = 0
vvt_b1_int = 0
vvt_b1_exh = 0
vvt_b2_int = 0
vvt_b2_ext = 0

vss_lf = 0
vss_rf = 0
vss_lr = 0
vss_rr = 0
vss_driven = 0
tc_status = 0

batt_v = 0
fault_count = 0

launch_rpm = 0
launch_status = 0
launch_states = ["Off", "Active", "Inactive"]
launch_colors = [0xffffff, 0x00ff00, 0xffbb00]
cruise_status = 0
cruise_states = ["Off", "Enabled", "Active", "Strt Lck", "Min RPM", "Max RPM", "CAN Er"]
cruise_colors = [0x000000, 0xffbb00, 0x00ff00, 0xffbb00, 0xffbb00, 0xffbb00, 0xffbb00]
cruise_speed = 0


print("starting listen")

while True:
    if e:
        print("Reading packet:")
        packet = e.read()
#        packets.append(packet)
        print(packet.msg)
        contents = packet.msg

        if contents[55] == 1:
            graphics.display.root_group = screen_1
        if contents[55] == 2:
            graphics.display.root_group = screen_2
        if contents[55] == 3:
            graphics.display.root_group = screen_3

        print(f"8: {contents[8]} 9: {contents[9]} 10: {contents[10]} 11: {contents[11]}")
        print(f"Batt V: {batt_v}")

################### Decode the ESP-now message into variables

        map_kpa = int(((contents[0] * 256) + contents[1])/100)
        map_tar = int(((contents[2] * 256) + contents[3])/100)
        target_a.x = int((map_tar/400) * 480)

        boost_state = contents[4]
        state_a.text = boost_states[boost_state]
        state_a.color = boost_colors[boost_state]

        flex_perc = contents[5]
        fan_perc = contents[6]

        iat = int(((((contents[7] * 256) + contents[8])-5000)/100)*9/5 + 32)
        ect = int(((((contents[9] * 256) + contents[10])-5000)/100)*9/5 + 32)
        mpg_avg = round(((contents[11] * 256) + contents[12])/100,1)
        mpg_inst = (contents[13]/4)


        lambda1 = round(((contents[14] * 256) + contents[15])/1000,3)
        lambda2 = round(((contents[16] * 256) + contents[17])/1000,3)
        lambda_tar = round(((contents[18] * 256) + contents[19])/1000,3)
        fault_count = contents[20]

        fuel_kpa = round(((contents[21] * 256) + contents[22])/100,0)
        fuel_tar = round(((contents[23] * 256) + contents[24])/100,0)
        fuel_pwm = contents[25]
        oil_kpa = round(((contents[26] * 256) + contents[27])/100,0)

        knock_1 = round(((contents[28])/10)-15,1)
        knock_2 = round(((contents[29])/10)-15,1)
        knock_3 = round(((contents[30])/10)-15,1)
        knock_4 = round(((contents[31])/10)-15,1)
        knock_5 = round(((contents[32])/10)-15,1)
        knock_6 = round(((contents[33])/10)-15,1)

        ign_adv = int(((contents[35] * 256) + contents[36])/100)
        tps = int(((contents[37] * 256) + contents[38])/100)
        idle_state = contents[39]
        aps = int(((contents[40] * 256) + contents[41])/100)

        vvt_int_tar = round((contents[42])/3,0)
        vvt_exh_tar = round((contents[43])/3,0)
        vvt_b1_int = round((contents[44])/3,1)
        vvt_b1_exh = round((contents[45])/3,1)
        vvt_b2_int = round((contents[46])/3,1)
        vvt_b2_ext = round((contents[47])/3,1)
        tc_status = (contents[48])

        vss_lf = (contents[49])
        vss_rf = (contents[50])
        vss_lr = (contents[51])
        vss_rr = (contents[52])
        vss_driven = int((((contents[53] * 256) + contents[54])/100)*0.6213)

        screen_number = contents[55]

        launch_rpm = int(((contents[56] * 256) + contents[57])/100)
        launch_status = contents[58]
        cruise_status = contents[59]
        cruise_speed = contents[60]
        batt_v = round((contents[61] * 256 + (contents[62]))/100,1)

################## Start writing values to gauges

######## Screen 1
        value_a.text = str(map_kpa)
        value_b.text = str(ect)
        value_c.text = str(iat)
        value_cc.text = str(f"{fan_perc}%")
        gauge_a_bkgd.width = int((map_kpa/400) * 480)
        if map_kpa <= value_a_min:
            value_a.color=0x0000ff
            gauge_a_bkgd.color_index = 2
        if value_a_min < map_kpa < value_a_max:
            value_a.color=0xffffff
            gauge_a_bkgd.color_index = 4
        if map_kpa >= value_a_max:
            value_a.color=0xff0000
            gauge_a_bkgd.color_index = 0
        if ect <= value_b_min:
            value_b.color=0x0000ff
        if value_b_min < ect < value_b_max:
            value_b.color=0xffffff
        if ect >= value_b_max:
            value_b.color=0xff0000
        if iat <= value_c_min:
            value_c.color=0x0000ff
        if value_c_min < iat < value_c_max:
            value_c.color=0xffffff
        if iat >= value_c_max:
            value_c.color=0xff0000

######## Screen 2

        value_d.text = str(lambda1)
        value_e.text = str(lambda2)
        value_f.text = str(int(fuel_kpa))
        value_g.text = str(int(oil_kpa))
        lambda1_level = (lambda1 - 0.5) / (1.5-0.5)
        lambda1_level = max(0, lambda1_level)
        gauge_d_bkgd.height = int((lambda1_level) * 480)
        gauge_d_bkgd.y = int(480 - gauge_d_bkgd.height)
        lambda2_level = (lambda2 - 0.5) / (1.5-0.5)
        lambda2_level = max(0, lambda2_level)
        gauge_e_bkgd.height = int((lambda2_level) * 480)
        gauge_e_bkgd.y = int(480 - gauge_e_bkgd.height)
        gauge_ee.y = int(480-((lambda_tar-0.5) * 480))

        if lambda1 <= value_d_min:
            value_d.color = 0x0000ff
            gauge_d_bkgd.color_index = 2
        if value_d_min < lambda1 < value_d_max:
            value_d.color = 0xffffff
            gauge_d_bkgd.color_index = 4
        if lambda1 >= value_d_max:
            value_d.color = 0xff0000
            gauge_d_bkgd.color_index = 0

        if lambda2 <= value_e_min:
            value_e.color = 0x0000ff
            gauge_e_bkgd.color_index = 2
        if value_e_min < lambda2 < value_e_max:
            value_e.color = 0xffffff
            gauge_e_bkgd.color_index = 4
        if lambda2 >= value_e_max:
            value_e.color = 0xff0000
            gauge_e_bkgd.color_index = 0

        if fuel_kpa <= value_f_min:
            value_f.color = 0xff0000
        if value_f_min < fuel_kpa < value_f_max:
            value_f.color = 0xffffff
        if fuel_kpa >= value_f_max:
            value_f.color = 0xff0000

        if oil_kpa <= value_g_min:
            value_g.color = 0xff0000
        if value_g_min < oil_kpa < value_g_max:
            value_g.color = 0xffffff
        if oil_kpa >= value_g_max:
            value_g.color = 0xff0000
        value_gg.text = str(ign_adv)
        knock_levels = [knock_1,knock_2,knock_3,knock_4,knock_5,knock_6]
        max_knock = max(knock_levels)
#        value_k1.text = str(max_knock)

        value_h.text = str(mpg_avg)

        value_j.text = str(vss_driven)
        if cruise_status == 0:
            value_j.anchored_position = (290, 125)
            value_j.scale = 4
        if cruise_status > 0:
            value_j.anchored_position = (290, 100)
            value_j.scale = 3
        value_jj.text = str(cruise_speed)
        value_jj.color = cruise_colors[cruise_status]
        state_jj.text = cruise_states[cruise_status]
        state_jj.color = cruise_colors[cruise_status]

        value_k.text = str(tps)
        value_kk.text = str(aps)
        state_k.text = idle_states[idle_state]
        state_k.color = idle_colors[idle_state]
        
        value_l.text = str(launch_rpm)
        value_l.color = launch_colors[launch_status]
        state_l.text = launch_states[launch_status]
        state_l.color = launch_colors[launch_status]
        
        value_bb.text = str(f"{flex_perc}%")
        gauge_i_bkgd.height = int((mpg_inst/40) * 480)
        gauge_i_bkgd.y = int(480 - gauge_i_bkgd.height)


        
        
        if max_knock <= value_k1_min:
            knock_block.color_index = 0
            knock_block2.color_index = 0
        if max_knock > value_k1_min:
            knock_block.color_index = 1
            knock_block2.color_index = 1

print("packets:", f"length={len(packets)}")
for packet in packets:
    print(packet)
