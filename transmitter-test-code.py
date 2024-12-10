import os
import board
import digitalio
import busio
import time
import espnow
import wifi
from canio import CAN as CAN1
from adafruit_mcp2515 import MCP2515 as CAN2
from canio import Message, RemoteTransmissionRequest

# print(f"My MAC address: {[hex(i) for i in wifi.radio.mac_address]}")

print(f"Connecting to {os.getenv('CIRCUITPY_WIFI_SSID')}")
wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
print(f"Connected to {os.getenv('CIRCUITPY_WIFI_SSID')}")
print(f"My IP address: {wifi.radio.ipv4_address}")

# Setup CAN1 via canio
can1 = CAN1(rx=board.IO6, tx=board.IO7, baudrate=500_000, auto_restart=True)

e = espnow.ESPNow()
peer = espnow.Peer(mac=b'\x74\x4D\xBD\x9D\x4D\x14')
e.peers.append(peer)

while True:
    print("CAN1: Tx Errors:", can1.transmit_error_count,
    "Rx Errors:", can1.receive_error_count,
    "state:", can1.state)
    with can1.listen(timeout=1.0) as can1_listener:
        message_count = can1_listener.in_waiting()
        if message_count:
            print("CAN1: Messages available:", message_count)
            for _i in range(message_count):
                msg = can1_listener.receive()
                if isinstance(msg, Message):
                    if hex(msg.id) == "0x3e8":
                        print("CAN1: Recieved", msg.data, "from", hex(msg.id))
                        can_message_str = msg.data
                        value_1 = round(((can_message_str[0] * 256) + can_message_str[1])/100,2)
                        value_2 = (can_message_str[2] * 256) + can_message_str[3]
                        print("Battery voltage: ", value_1)
                        print("Math block 3: ", value_2)
                if isinstance(msg, RemoteTransmissionRequest):
                    print("CAN1: RTR request length", msg.length, "from", hex(msg.id))
    time.sleep(0.1)
#    for i in range(101):
#        x = str(i)
#        e.send(x)
#        print("sending: " + x)
#        time.sleep(0.1)
#    time.sleep(0.5)
#    print("Time to count down")

#    for i in range(100):
#        x = str(100 - i)
#        e.send(x)
#        print("sending: " + x)
#        time.sleep(0.1)
#    time.sleep(0.5)

print("finished sending")
# For the ESP32-CAN-X2 the LED is on IO2
led = digitalio.DigitalInOut(board.IO2)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)
