import serial
import serial.tools.list_ports
import threading
import time

class TurretSerial:
    def __init__(self, baudrate=9600):
        self.ser = None
        self.baudrate = baudrate
        self.lock = threading.Lock()
        self.port = self.find_arduino_port()
        if self.port:
            self._connect()
        else:
            print("[SERIAL] No Arduino found.")

    def find_arduino_port(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "Arduino" in port.description or "ttyACM" in port.device or "ttyUSB" in port.device:
                print(f"[SERIAL] Found candidate port: {port.device}")
                return port.device
        return None

    def _connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Give time for Arduino to reboot
            print(f"[SERIAL] Connected to Arduino on {self.port}")
        except Exception as e:
            print(f"[ERROR] Failed to open serial port {self.port}: {e}")
            self.ser = None

    def send(self, cmd):
        if not self.ser or not self.ser.is_open:
            print("[SERIAL] Not connected, attempting reconnect...")
            self.port = self.find_arduino_port()
            if self.port:
                self._connect()

        if self.ser and self.ser.is_open:
            with self.lock:
                message = (cmd + '\n').encode('utf-8')
                self.ser.write(message)
                print(f"[SERIAL] Sent: {cmd}")
        else:
            print(f"[SERIAL] Skipped sending (not connected): {cmd}")
