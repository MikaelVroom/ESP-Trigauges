import os
import board
import digitalio
import time
import espnow
import wifi

print(f"My MAC address: {[hex(i) for i in wifi.radio.mac_address]}")

print(f"Connecting to {os.getenv('CIRCUITPY_WIFI_SSID')}")
wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
print(f"Connected to {os.getenv('CIRCUITPY_WIFI_SSID')}")
print(f"My IP address: {wifi.radio.ipv4_address}")

e = espnow.ESPNow()
peer = espnow.Peer(mac=b'\x74\x4D\xBD\x9D\x4D\x14')
e.peers.append(peer)

while True:
#e.send("Starting...")
    for i in range(100):
        x = str(i)
        e.send(x)
        print("sending: " + x)
        time.sleep(0.05)
    time.sleep(0.5)
    print("Time to count down")

    for i in range(100):
        x = str(100 - i)
        e.send(x)
        print("sending: " + x)
        time.sleep(0.05)
    time.sleep(0.5)    
#e.send(b'end')

print("finished sending")
# For the ESP32-CAN-X2 the LED is on IO2
led = digitalio.DigitalInOut(board.IO2)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)


