# 🎯 Autonomous IR Turret Face Tracking
## Designed for Crunchlabs Hack Pack IR Turret (by Mark Rober) 
### Using Raspberry Pi Zero 2 W + Camera Module 3 

A mobile-friendly, Flask-powered web app to control the Crunchlabs IR Turret using a Raspberry Pi Zero 2 W. Features include face tracking, a full-screen live video stream, and remote control, using serial communication with the turret's Arduino.

---

## Hardware Requirements

- Crunchlabs IR Turret (by Mark Rober)
- Raspberry Pi Zero 2 W (+ min 16gb SD Card)
- Camera Module 3 (v3 Wide version)

---

## 🚀 Features

- 📷 Live MJPEG video stream from Pi Camera Module 3
- 🤖 Face detection overlays (OpenCV)
- 🎯 Manual D-Pad + FIRE controls (mobile UI)
- 🧠 Auto-tracking and auto-firing modes
- 🎯 Tap-to-calibrate custom target zone
- 🔌 Serial communication to Arduino turret (via USB)

---

## ⚙️ Setup Instructions (Raspberry Pi Zero 2 W + Pi Camera 3)

### Arduino Code

Go to https://ide.crunchlabs.com/editor/8718988640487 or get the Arduino IDE (https://www.arduino.cc/en/software/) and we need to add some code to the sketch.

Add this inside your existing loop() and outside the if (IrReceiver.decode()) block, so both IR and serial input can be handled independently.

```bash
// Check for serial input from Raspberry Pi
if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n'); // Read full command line
    cmd.trim(); // Remove whitespace or newlines

    if (cmd == "UP") {
        upMove(1);
    } else if (cmd == "DOWN") {
        downMove(1);
    } else if (cmd == "LEFT") {
        leftMove(1);
    } else if (cmd == "RIGHT") {
        rightMove(1);
    } else if (cmd == "FIRE") {
        fire();
    } else if (cmd == "FIREALL") {
        fireAll();
    } else if (cmd == "YES") {
        shakeHeadYes(3);
    } else if (cmd == "NO") {
        shakeHeadNo(3);
    } else {
        Serial.print("Unknown command: ");
        Serial.println(cmd);
    }
}
```


### 1. Flash Raspberry Pi OS (Bookworm or later)
- Use **Raspberry Pi Imager**:
  - Choose: Raspberry Pi OS Lite (64-bit)
  - Enable: SSH, set hostname to `ir-turret.local`
  - Set username to `pi` and create a password
  - Configure Wi-Fi

---

### 2. SSH into Your Pi

```bash
ssh pi@ir-turret.local
```

---

### 3. Update the System

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

---

### 4. Install Required Dependencies

```bash
sudo apt install -y \
  git python3-flask python3-serial \
  python3-picamera2 python3-libcamera libatlas-base-dev \
  libjpeg-dev libopenjp2-7 libopenexr-dev \
  libavcodec-dev libavformat-dev libswscale-dev \
  libgstreamer1.0-dev libglib2.0-dev v4l-utils
```

Then install full OpenCV (for face detection):

```bash
sudo apt remove python3-opencv -y
pip3 install opencv-python --break-system-packages
```
Then install pyserial (may already be satisfied)

```bash
pip3 install pyserial --break-system-packages
```

---

### 5. Test the Camera

```bash
libcamera-hello
```

---

### 6. Clone This Project

```bash
cd ~
git clone https://github.com/martyn-johnson/ir_turret.git
cd ir_turret
```

---

### 7. Connect the Arduino (Crunchlabs IR Turret)

Plug the Arduino in via USB and check:

```bash
ls /dev/ttyACM*   # or /dev/ttyUSB*
```

---

### 8. (Optional) Auto-Start Flask App on Boot

```bash
sudo nano /etc/systemd/system/turret.service
```

Paste the following:

```ini
[Unit]
Description=IR Turret Flask App
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/ir_turret
ExecStart=/usr/bin/python3 /home/pi/ir_turret/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then enable and start the service:

```bash
sudo systemctl daemon-reexec
sudo systemctl enable turret.service
sudo systemctl start turret.service
```

To restart the service after editing Python files:

```bash
sudo systemctl restart turret.service
```

---

### 9. Open the Web Interface

From any device on your network:

```
http://ir-turret.local:5000/
```

---

## 🛠️ Development Notes

- All camera processing and face detection runs directly on the Pi
- Web UI is built mobile-first (touch-friendly layout)
- System Python is used (not virtualenv) for compatibility with `picamera2` and `libcamera`

---

## 📦 GitHub Repo

Project code is hosted here:  
🔗 [https://github.com/martyn-johnson/ir_turret](https://github.com/martyn-johnson/ir_turret)

Youtube

🔗 [https://www.youtube.com/@atexj](https://www.youtube.com/@atexj)