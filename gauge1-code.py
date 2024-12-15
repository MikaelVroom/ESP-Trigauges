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

gauge_1 = displayio.Group()
gauge_2 = displayio.Group()
gauge_3 = displayio.Group()

font = bitmap_font.load_font("fonts/LeagueSpartan-Bold-16.bdf", Bitmap)

def center(grid, bitmap):
    # center the image
    grid.x -= graphics.display.width // 2
    grid.y -= graphics.display.height // 2

graphics.display.root_group = gauge_3

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

value_aa = label.Label(
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
    anchored_position = (240, 170)
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

gauge_1.append(channel_a)
gauge_1.append(unit_a)
gauge_1.append(value_a)
gauge_1.append(value_aa)
gauge_1.append(gauge_a_frame)
gauge_1.append(lower_divider)
gauge_1.append(gauge_a_bkgd)
gauge_1.append(channel_b)
gauge_1.append(unit_b)
gauge_1.append(value_b)
gauge_1.append(channel_c)
gauge_1.append(unit_c)
gauge_1.append(value_c)

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
    scale=2,
    base_alignment=True,
    anchor_point=(0.5, 0),
    anchored_position=(120, 270)
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
    anchor_point=(0.5, 0),
    anchored_position=(120, 320)
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
    anchor_point=(0.5, 0),
    anchored_position=(160, 400)
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
    anchor_point=(0.5, 0),
    anchored_position=(360, 270)
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
    anchor_point=(0.5, 0),
    anchored_position=(360, 320)
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
    anchor_point=(0.5, 0),
    anchored_position=(320, 400)
)

unit_g.text = str("kPa")

gauge_2.append(lower_divider)
gauge_2.append(channel_d)
gauge_2.append(unit_d)
gauge_2.append(value_d)
gauge_2.append(gauge_d_frame)
gauge_2.append(gauge_d_bkgd)
gauge_2.append(channel_e)
gauge_2.append(unit_e)
gauge_2.append(value_e)
gauge_2.append(gauge_e_frame)
gauge_2.append(gauge_e_bkgd)
gauge_2.append(channel_f)
gauge_2.append(unit_f)
gauge_2.append(value_f)
gauge_2.append(channel_g)
gauge_2.append(unit_g)
gauge_2.append(value_g)


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

gauge_3.append(knock_block)
gauge_3.append(lower_divider)
gauge_3.append(channel_h)
gauge_3.append(unit_h)
gauge_3.append(value_h)
gauge_3.append(gauge_i_frame)
gauge_3.append(gauge_i_bkgd)
gauge_3.append(channel_j)
gauge_3.append(unit_j)
gauge_3.append(value_j)
gauge_3.append(channel_k)
gauge_3.append(unit_k)
gauge_3.append(value_k)
gauge_3.append(div_1)
gauge_3.append(div_2)
gauge_3.append(div_3)
gauge_3.append(div_4)
gauge_3.append(mpg_scale_1)
gauge_3.append(mpg_scale_2)
gauge_3.append(mpg_scale_3)
gauge_3.append(channel_l)
gauge_3.append(value_k1)


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
idle_state = 0

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
batt_v = 0
fault_count = 0


print("starting listen")

while True:
    if e:
        print("Reading packet:")
        packet = e.read()
#        packets.append(packet)
        print(packet.msg)
        contents = packet.msg

        if contents[55] == 1:
            graphics.display.root_group = gauge_1
        if contents[55] == 2:
            graphics.display.root_group = gauge_2
        if contents[55] == 3:
            graphics.display.root_group = gauge_3

        batt_v = ((contents[40] * 256 + (contents[41]))/100)
        print(f"8: {contents[8]} 9: {contents[9]} 10: {contents[10]} 11: {contents[11]}")
        print(f"Batt V: {batt_v}")

        map_kpa = int(((contents[0] * 256) + contents[1])/25)
        map_tar = int(((contents[2] * 256) + contents[3])/100)
        boost_state = contents[4]
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

        knock_1 = round((contents[28])/10,1)
        knock_2 = round((contents[29])/10,1)
        knock_3 = round((contents[30])/10,1)
        knock_4 = round((contents[31])/10,1)
        knock_5 = round((contents[32])/10,1)
        knock_6 = round((contents[33])/10,1)

        ign_adv = round(((contents[35] * 256) + contents[36])/100,0)
        tps = round(((contents[37] * 256) + contents[38])/100,1)
        idle_state = contents[39]
        tps = round(((contents[40] * 256) + contents[41])/100,1)

        vvt_int_tar = round((contents[42])/3,0)
        vvt_exh_tar = round((contents[43])/3,0)
        vvt_b1_int = round((contents[44])/3,1)
        vvt_b1_exh = round((contents[45])/3,1)
        vvt_b2_int = round((contents[46])/3,1)
        vvt_b2_ext = round((contents[47])/3,1)

        vss_lf = (contents[49])
        vss_rf = (contents[50])
        vss_lr = (contents[51])
        vss_rr = (contents[52])
        vss_driven = round(((contents[53] * 256) + contents[54])/100,1)

        screen_number = contents[55]

        value_a.text = str(map_kpa)
        value_aa.text = str(map_tar)
        value_b.text = str(ect)
        value_c.text = str(iat)
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

        value_d.text = str(lambda1)
        value_e.text = str(lambda2)
        value_f.text = str(int(fuel_kpa))
        value_g.text = str(int(oil_kpa))
        gauge_d_bkgd.height = int((lambda1/2) * 480)
        gauge_d_bkgd.y = int(480 - gauge_d_bkgd.height)
        gauge_e_bkgd.height = int((lambda2/2) * 480)
        gauge_e_bkgd.y = int(480 - gauge_e_bkgd.height)

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

        knock_levels = [knock_1,knock_2,knock_3,knock_4,knock_5,knock_6]
        max_knock = max(knock_levels)
#        if mpg_avg != mpg_avg_last:
        value_h.text = str(mpg_avg)
#            mpg_avg_last = mpg_avg
        if ign_adv != ign_adv_last:
            value_j.text = str(ign_adv)
            ign_adv_last = ign_adv
        value_k.text = str(flex_perc)
        gauge_i_bkgd.height = int((mpg_inst/40) * 480)
        gauge_i_bkgd.y = int(480 - gauge_i_bkgd.height)
        value_k1.text = str(max_knock)

        if max_knock <= value_k1_min:
            knock_block.color_index = 0
        if max_knock > value_k1_min:
            knock_block.color_index = 1

print("packets:", f"length={len(packets)}")
for packet in packets:
    print(packet)
