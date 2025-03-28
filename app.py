from flask import Flask, render_template, Response, request, jsonify
from picamera2 import Picamera2
from turret_serial import TurretSerial
import cv2
import threading
import serial.tools.list_ports

app = Flask(__name__)

# Start camera at high resolution (wide format for Camera Module 3 Wide)
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(
    main={"size": (1280, 720)},  # widescreen 16:9 ratio
    controls={"AfMode": 1}       # Auto focus mode
))
picam2.start()

# Apply improved default controls
picam2.set_controls({
    "AwbEnable": True,
    "AeEnable": True,
    "Brightness": 0.2,
    "Contrast": 1.3,
    "Saturation": 0.8,
    "Sharpness": 1.0,
    "AfMode": 1  # continuous autofocus
})

# Initialize serial communication with Arduino
turret = TurretSerial('/dev/ttyACM0')  # Adjust if you're using a different port

# Face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Globals
target_x, target_y = 640, 360  # center of 1280x720
auto_track = False
auto_fire = False
latest_command = None
lock = threading.Lock()

def generate_frames():
    global target_x, target_y

    while True:
        frame = picam2.capture_array()
        # Ensure correct color conversion: RGB → BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.resize(frame, (1280, 720))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.drawMarker(frame, (target_x, target_y), (0, 0, 255), cv2.MARKER_CROSS, 30, 2)

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/command/<cmd>', methods=['GET'])
def send_command(cmd):
    global latest_command
    with lock:
        latest_command = cmd
        print(f"[COMMAND] Sent to Arduino: {cmd}")
        turret.send(cmd)
    return jsonify(success=True, command=cmd)

@app.route('/calibrate', methods=['POST'])
def calibrate():
    global target_x, target_y
    data = request.get_json()
    target_x = int(data.get('x', 640))
    target_y = int(data.get('y', 360))
    print(f"[CALIBRATION] Target set to: ({target_x}, {target_y})")
    return jsonify(success=True, x=target_x, y=target_y)

@app.route('/settings', methods=['POST'])
def update_settings():
    global auto_track, auto_fire
    data = request.get_json()
    auto_track = data.get('track', False)
    auto_fire = data.get('auto_fire', False)
    print(f"[SETTINGS] Track: {auto_track}, Auto Fire: {auto_fire}")

    # Apply additional camera settings
    try:
        settings = {
            "Brightness": float(data.get("brightness", 0.2)),
            "Contrast": float(data.get("contrast", 1.3)),
            "Saturation": float(data.get("saturation", 0.8)),
            "Sharpness": float(data.get("sharpness", 1.0)),
            "AnalogueGain": float(data.get("gain", 1.0)),
        }

        print(f"[CAMERA] Applying settings: {settings}")
        picam2.set_controls(settings)
    except Exception as e:
        print(f"[ERROR] Failed to set camera settings: {e}")

    return jsonify(success=True)

@app.route('/serial_ports', methods=['GET'])
def list_serial_ports():
    ports = [port.device for port in serial.tools.list_ports.comports()]
    return jsonify(ports=ports)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)