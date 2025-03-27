# Autonomous IR Turret with Face Tracking (Pi Zero 2 W + Camera Module 3) for Crunchlabs Hack Pack IR Turret by Mark Rober

A mobile-friendly, Flask-powered web app to control and calibrate an autonomous infrared turret powered by a Raspberry Pi Zero 2 W and the Crunchlabs Hack Pack IR Turret. It supports face tracking, a live video stream from the Pi Camera Module 3, and serial communication with the turret's Arduino controller.

---

## 🚀 Features

- Live MJPEG video stream from Pi Camera Module 3
- Face detection overlays
- Manual turret controls (via web UI)
- Auto-tracking and auto-firing modes
- Calibration system for accurate targeting
- Communicates with Arduino turret via USB serial

---

## 🔧 Updated Setup Instructions

### 1. Flash Raspberry Pi OS (Bookworm or later)
- Use Raspberry Pi Imager to install Raspberry Pi OS Lite (64-bit)
- Enable SSH, Wi-Fi, and set hostname (e.g., `ir-turret.local`)
- Set username to pi and set a password (important)

### 2. SSH into Pi

```bash
ssh pi@ir-turret.local
```

### 3. Update & Upgrade

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### 4. Install Required System Packages
```bash
sudo apt install -y \
  git python3-flask python3-serial \
  python3-picamera2 python3-libcamera libatlas-base-dev \
  libjpeg-dev libopenjp2-7 libopenexr-dev \
  libavcodec-dev libavformat-dev libswscale-dev \
  libgstreamer1.0-dev libglib2.0-dev v4l-utils
```

Then install full OpenCV using pip (needed for face detection):

```bash
sudo apt remove python3-opencv -y
pip3 install opencv-python --break-system-packages
```

### 5. Test Camera

```bash
libcamera-hello
```

### 6. Set Up Project Directory

```bash
cd ~
mkdir ir_turret
cd ir_turret
```

### 7. Connect Arduino

Plug the Arduino via USB and check:

```bash
ls /dev/ttyACM*   # or /dev/ttyUSB*
```


## ✅ You're Ready to Start Coding!

Create `app.py` and `templates/index.html`, and begin building your turret logic!

### Access the App

Open in browser:

```
http://ir-turret.local:5000/
```


### Optional: Auto-start Flask App

```bash
sudo nano /etc/systemd/system/turret.service
```

Paste and edit:

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

Enable it:

```bash
sudo systemctl daemon-reexec
sudo systemctl enable turret.service
```

If you edit the python code in app.ph you will need to restart the service:

```bash
sudo systemctl restart turret.service
```