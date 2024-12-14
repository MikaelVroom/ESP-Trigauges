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

map_kpa = 0
map_tar = 0
boost_state = 0
flex_perc = 0
fan_perc = 0

iat = 0
ect = 0
mpg_avg = 0
mpg_avg_last = 0
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
ign_adv_last = 0
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

        batt_v = ((contents[40] * 256 + (contents[41]))/100)
        print(f"5: {contents[5]}")
        print(f"Batt V: {batt_v}")
  
        map_kpa = round(((contents[0] * 256) + contents[1])/100,0)
        map_tar = round(((contents[2] * 256) + contents[3])/100,0)
        boost_state = contents[4]
        flex_perc = contents[5]
        fan_perc = contents[6]
                        
        iat = round(((contents[8] * 256) + contents[9])/100,0)
        ect = round(((contents[10] * 256) + contents[11])/100,0)
        mpg_avg = round(((contents[12] * 256) + contents[13])/100,0)
        mpg_inst = contents[14]


        lambda1 = round(((contents[15] * 256) + contents[16])/1000,3)
        lambda2 = round(((contents[17] * 256) + contents[18])/1000,3)
        lambda_tar = round(((contents[19] * 256) + contents[20])/1000,3)
        fault_count = contents[21]

        fuel_kpa = round(((contents[22] * 256) + contents[23])/100,0)
        fuel_tar = round(((contents[24] * 256) + contents[25])/100,0)
        fuel_pwm = contents[26]
        oil_kpa = round(((contents[27] * 256) + contents[28])/100,0)

        knock_1 = round((contents[29])/10,1)
        knock_2 = round((contents[30])/10,1)
        knock_3 = round((contents[31])/10,1)
        knock_4 = round((contents[32])/10,1)
        knock_5 = round((contents[33])/10,1)
        knock_6 = round((contents[34])/10,1)

        ign_adv = round(((contents[33] * 256) + contents[34])/100,0)
        tps = round(((contents[35] * 256) + contents[36])/100,1)
        idle_state = contents[37]
        tps = round(((contents[38] * 256) + contents[39])/100,1)

        vvt_int_tar = round((contents[40])/3,0)
        vvt_exh_tar = round((contents[41])/3,0)
        vvt_b1_int = round((contents[42])/3,1)
        vvt_b1_exh = round((contents[43])/3,1)
        vvt_b2_int = round((contents[44])/3,1)
        vvt_b2_ext = round((contents[45])/3,1)

        vss_lf = (contents[1])
        vss_rf = (contents[2])
        vss_lr = (contents[3])
        vss_rr = (contents[4])
        vss_driven = round(((contents[5] * 256) + contents[6])/100,1)

        knock_levels = [knock_1,knock_2,knock_3,knock_4,knock_5,knock_6]
        max_knock = max(knock_levels)
        if mpg_avg != mpg_avg_last:
            value_h.text = str(mpgavg)
            mpg_avg_last = mpg_avg
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
