# 🧠 DroneExamMonitor
### AI-Powered Drone System for Exam Cheating Detection

---

## 📘 Project Overview
**DroneExamMonitor** is an AI-based drone monitoring system designed to detect suspicious behaviors (such as head turning or hand gestures) during exams.  
By integrating **YOLO object detection**, **MediaPipe pose tracking**, and **Tello drone control**, this project enables autonomous surveillance and real-time alerts for potential cheating activities.

---

## 🚀 Key Features
- 🎯 **YOLOv8-based Object Detection** – Detects students, invigilators, and exam-related objects in real time.  
- 🧍 **MediaPipe Pose Estimation** – Tracks body movements and head rotation to identify unusual behavior.  
- ✈️ **Tello Drone Integration** – Allows the drone to patrol and record exam rooms automatically.  
- ⚠️ **Real-time Warning System** – Displays visual or sound alerts when abnormal motion is detected.  
- 💾 **Customizable Dataset** – Supports retraining with your own exam environment data.  

---

## 🧩 System Architecture
```
+-------------------+
|   Drone Camera    |
+-------------------+
          ↓
+-------------------+
|   YOLOv8 Model    |  → Object Detection (Student / Referee / etc.)
+-------------------+
          ↓
+-------------------+
|  MediaPipe Pose   |  → Detect Head Turns / Suspicious Gestures
+-------------------+
          ↓
+-------------------+
|  Alert Module     |  → Display warning images / sounds
+-------------------+
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Minhuinoga/ExamDroneDetection.git
cd ExamDroneDetection
```

### 2️⃣ Create Virtual Environment
```bash
conda create -n drone python=3.8
conda activate drone
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
*(You can also manually install the main libraries below)*  
```bash
pip install torch torchvision opencv-python mediapipe numpy djitellopy ultralytics
```

---

## 🎮 How to Use

### 🧠 Run YOLO + Drone Detection
```bash
python final.py
```

### 🕹️ Keyboard Control (Manual Mode)
```bash
python Keyboard_Control1.py
```

### 🤖 Automated Detection Mode
```bash
python keyboard_Auto.py
```

When the drone detects suspicious behavior, a warning image (e.g., `warning_turn.png`, `warning_phone.png`) will appear on screen.

---

## 🧰 Files Description
| File | Description |
|------|--------------|
| `final.py` | Main program integrating YOLO + MediaPipe + Drone |
| `KeyPressModule.py` | Keyboard input module for controlling drone |
| `Keyboard_Control1.py`, `Keyboard_Control2.py` | Manual control programs |
| `keyboard_Auto.py` | Autonomous mode for detection and alert |
| `yolov8n.pt` | YOLOv8 model weights |
| `warning_*.png` | Warning icons displayed during alerts |

---

## ⚠️ Notes
- Ensure your **Ryze Tello** drone is connected via Wi-Fi before starting.  
- Avoid running from a **OneDrive** folder (may cause file-lock issues).  
- Large model files (>100MB) should use **Git LFS**.  
- Works best in indoor, well-lit environments.

---

## 🧑‍💻 Author
**Minhuinoga**  
📍 Developed as part of an intelligent surveillance research project.  
🚀 Built with Python, YOLOv8, and Tello SDK.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
