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

led = digitalio.DigitalInOut(board.IO2)
led.direction = digitalio.Direction.OUTPUT

# Setup CAN1 via canio
can_bus = CAN1(rx=board.IO6, tx=board.IO7, baudrate=500_000, auto_restart=True)

e = espnow.ESPNow()
peer = espnow.Peer(mac=b'\x74\x4D\xBD\x9D\x4D\x14')
e.peers.append(peer)

# Constants
FRAME_COUNT = 8  # Total frames expected
FRAME_DATA_SIZE = 7  # Bytes of data per frame excluding sequence byte
TIMEOUT = 5  # Timeout in seconds to wait for all frames
send_time_delay = 0.0
last_send_time = 0.0

# Buffer to store received frames
frames = [None] * FRAME_COUNT
received = [False] * FRAME_COUNT

def collect_frames(timeout=TIMEOUT):
    """Collect frames from the CAN bus."""
    global frames, received
    frames = [None] * FRAME_COUNT  # Reset frames
    received = [False] * FRAME_COUNT  # Reset received status
    start_time = time.monotonic()
    while not all(received) and (time.monotonic() - start_time < timeout):
        with can_bus.listen(timeout=5.0) as can1_listener:
#        message_count = can1_listener.in_waiting()
            if can1_listener.in_waiting():
                message = can1_listener.receive()
                if hex(message.id) == "0x3e8":
                    data = list(message.data)
#                    print(f"First byte: {data[0]}")
                    frame_number = data[0]  # Extract frame number
#                    print(f"Frame number: {frame_number}")
            # Validate frame number and store the data
                    if 0 <= frame_number < FRAME_COUNT:
                        frames[frame_number] = data[1:]  # Store bytes 1-7
                        received[frame_number] = True
#                        print(f"Received frame {frame_number}: {data}")
    
    if not all(received):
        print("Timeout: Not all frames received!")
        return False
    return True

def reconstruct_message():
    """Reconstruct the full message from received frames."""
    if not all(received):
        raise ValueError("Cannot reconstruct message; some frames are missing.")
    
    message = bytearray()
    for frame_data in frames:
        message.extend(frame_data)
    return message

def send_message(message):
    """Send the message using ESP-Now."""
    try:
        e.send(message)
        print("Message sent successfully!")
    except Exception as error:
        print(f"Failed to send message: {error}")

# Main loop
while True:
    led.value = True
    print("Waiting for CAN frames...")
    if collect_frames():
        try:
            full_message = reconstruct_message()
            print(f"Reconstructed message: {full_message.hex()}")
#            print(f"Length: {len(full_message)}")
            if len(full_message) > 250:
                print("Message too large for ESP-Now, splitting...")
                for i in range(0, len(full_message), 250):
                    chunk = full_message[i:i + 250]
                    send_message(chunk)
                    time.sleep(0.01)  # Avoid congestion
            else:
                send_message(full_message)
                send_time_delay = time.monotonic() - last_send_time
                print(f"Send delay: {send_time_delay}")
                last_send_time = time.monotonic()
        except ValueError as error:
            print(error)
    time.sleep(1)


#while True:
#    print("CAN1: Tx Errors:", can1.transmit_error_count,
#    "Rx Errors:", can1.receive_error_count,
#    "state:", can1.state)
#    with can1.listen(timeout=1.0) as can1_listener:
#        message_count = can1_listener.in_waiting()
#        if message_count:
#            print("CAN1: Messages available:", message_count)
#            for _i in range(message_count):
#                msg = can1_listener.receive()
#                if isinstance(msg, Message):
#                    print("CAN1: Recieved", msg.data, "from", hex(msg.id))
#                    if hex(msg.id) == "0x3e8":
#                        print("CAN1: Recieved", msg.data, "from", hex(msg.id))
#                        can_message_str = msg.data
#                
#                if isinstance(msg, RemoteTransmissionRequest):
#                    print("CAN1: RTR request length", msg.length, "from", hex(msg.id))
#    time.sleep(0.001)
#    for i in range(101):
#        x = str(i)
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
