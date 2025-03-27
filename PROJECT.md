

# Project Specification  
## Autonomous Pi Zero 2 W Face Tracking, Web UI, and Calibrated Targeting for Crunchlabs Hack Pack IR Turret

---

## Project Overview

Build a mobile-friendly, web-controlled, face-tracking IR turret system using a Raspberry Pi Zero 2 W and a Crunchlabs Hack Pack IR turret. The Pi will handle camera streaming, face detection, calibration, and turret control through serial communication with the IR Turret's Arduino.

---

## System Components

### Hardware
- **Raspberry Pi Zero 2 W**
- **Pi Camera Module 3** – mounted on the turret
- **Hack Pack IR Turret with Arduino** (from Crunchlabs by Mark Rober)
  - Yaw (rotation): Servo on pin 10
  - Pitch (tilt): Servo on pin 11
  - Roll/Firing: Servo on pin 12

---

## System Architecture

```
User Device (Phone/Tablet/Desktop)
        ⬌ Flask Web UI (Pi Zero)
              ⬇
       OpenCV + Camera Feed
              ⬇
      Target Logic + Face Detection
              ⬇
      Serial Commands to Arduino
              ⬇
      Arduino Executes Servo/Firing
```

---

## User Interface (Mobile-Friendly Web UI)

### Live Video Feed
- MJPEG stream from Pi camera
- Face detection overlays (bounding boxes round detected faces)
- Crosshair or indicator for current callibrated target zone (centre of video feed by default)

### Controls (Overlaid on Stream)
- D-Pad (↑ ↓ ← →) (Bottom left of feed)
- Large **FIRE** button (Bottom right of feed)
- Two checkbox toggles (Bottom centre of feed):
  1. **Track Faces** – Auto room scanning + Enables face detection + turret centering
  2. **Auto Fire** – Fires when a face is in the target zone

### Calibration Mode
- **“Calibrate” button** (Bottom centre of feed)
- Puts UI into calibration mode:
  1. User fires at a fixed object (test target).
  2. User taps/clicks where the dart hit on the video feed.
  3. That point becomes the new **target zone**.
- UI shows updated crosshair overlay at calibrated **target zone**.

---

## Turret Behavior Modes
Face detection is always turned on and highlighted in the feed with a bounding box

### Manual Mode (default)
- User manually moves and fires turret using D-Pad and FIRE button.

### Track Faces Mode
- Room scanning - Pi alternates between `LEFT` and `RIGHT` commands at set intervals to simulate room scanning.
- Face detection + tracking is active.
- Turret stops scanning and centers face in the **target zone**.
- If no face is seen for N seconds, scanning resumes.

### Auto Fire Mode
- When a face is detected and aligned within a small threshold of the **calibrated target zone**, turret fires.
- Auto Fire paused for 5 seconds

---

## Command Set (Pi → Arduino via Serial)

| Command | Description              |
|---------|--------------------------|
| `LEFT`  | Rotate yaw left          |
| `RIGHT` | Rotate yaw right         |
| `STOP`  | Stop yaw rotation        |
| `UP`    | Tilt pitch up            |
| `DOWN`  | Tilt pitch down          |
| `FIRE`  | Fire single dart         |

> Commands are sent via serial (USB connection) from Pi to Arduino. Arduino already handles them as per the Hack Pack existing sketch.

---

## Calibration System

### Purpose:
Align camera field of view with actual dart trajectory by manually defining a custom **target zone**.

### Default Target Zone:
- Center of the video frame (`x = 320`, `y = 240` for 640x480)

### Calibration Flow:
1. User presses **Calibrate** in UI.
2. Fires a dart.
3. Taps/clicks on video feed where dart hit.
4. System saves the click position as `target_x, target_y`.
5. Future face tracking attempts to center faces in this region.

---

## Backend Tech Stack

- Python 3
- Flask
- OpenCV
- PySerial
- HTML/CSS/JavaScript (Bootstrap for mobile responsiveness)
- jQuery AJAX for control input (simple polling)

---

## Software Flow Summary

1. **Startup**:
   - Pi initializes camera stream and face detection
   - Arduino connected via USB and ready for commands

2. **User opens UI**:
   - Live stream begins
   - Can manually control turret or enable automation

3. **Tracking Mode**:
   - Pi detects face using OpenCV
   - Calculates distance of face from `target_x, target_y`
   - If not centered → sends YAW/PITCH commands
   - If centered and Auto Fire is ON → sends `FIRE`

4. **Calibration Mode**:
   - Saves a new `target_x`, `target_y` based on user click

---

## Future Features (v2+)
- **Face recognition** (known faces database, define friendly faces)
- **Prioritized target selection** (e.g. largest or closest)
- **Fire rate / burst control**
- **Remote control** from outside local network
- **Game modes**, scoring, etc.
- **Motion tracking** or auto-record when face appears
- **Prediction** position prediction for fast moving targets

---

## Deliverables
- Complete Setup instruction for fresh Raspberry Pi Zero 2 W with Camera Module
- Flask app (`app.py`) with routes:
  - `/` → Web UI
  - `/video_feed` → MJPEG stream
  - `/command/<cmd>` → Turret control
  - `/calibrate` → POST route to save new target zone
- HTML/JS front-end:
  - Mobile-first layout
  - Fullscreen video feed
  - Live video with overlay buttons and checkbox toggles
  - Clickable calibration logic
- Python OpenCV logic:
  - Face detection
  - Frame overlays (bounding boxes + crosshair)
  - Tracking + firing behavior
- Serial communication class (for clean Arduino command handling)
