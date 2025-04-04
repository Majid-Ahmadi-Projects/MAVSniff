import socket
import threading
from pymavlink import mavutil

# Ports
QGC_PORT = 14560
SITL_PORT = 14551
BUFFER_SIZE = 4096

# Sockets
qgc_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
qgc_sock.bind(('127.0.0.1', QGC_PORT))

sitl_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sitl_sock.bind(('127.0.0.1', SITL_PORT))

# MAVLink decoder (for QGC messages)
mav = mavutil.mavlink.MAVLink(None)

# These will be dynamically learned
qgc_addr = None
sitl_addr = None

def qgc_to_sitl():
    global sitl_addr, qgc_addr
    while True:
        data, addr = qgc_sock.recvfrom(BUFFER_SIZE)
        qgc_addr = addr  # track QGC sender

        if sitl_addr:
            sitl_sock.sendto(data, sitl_addr)

        # Feed raw bytes directly into MAVLink parser
        for byte in data:
            try:
                if isinstance(byte, int):  # Python 3
                    msg = mav.parse_char(bytes([byte]))
                else:  # Python 2 compatibility or fallback
                    msg = mav.parse_char(byte)
                if msg:
                    msg_type = msg.get_type()
                    msg_dict = msg.to_dict()
                    if msg_type not in ["HEARTBEAT", "REQUEST_DATA_STREAM"]:
                        print(f"\n[QGC → SITL] MAVLink message received:")
                        print(f"  Type: {msg_type}")
                        print(f"  Fields: {msg.to_dict()}")
            except Exception as e:
                print(f"Decode error: {e}")

def sitl_to_qgc():
    global sitl_addr, qgc_addr
    while True:
        data, addr = sitl_sock.recvfrom(BUFFER_SIZE)
        sitl_addr = addr  # Save the latest SITL sender
        if qgc_addr:
            qgc_sock.sendto(data, qgc_addr)
        #print(f"[SITL → QGC] {len(data)} bytes")

threading.Thread(target=qgc_to_sitl, daemon=True).start()
threading.Thread(target=sitl_to_qgc, daemon=True).start()

print("MAVLink forwarder running (2-port mode). Press Ctrl+C to stop.")

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Forwarder stopped.")