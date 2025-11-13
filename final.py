import os
from djitellopy import Tello
import cv2
import mediapipe as mp
import threading
from time import sleep
import time
from ultralytics import YOLO
import KeyPressModule as kp

# 初始化按鍵模組
kp.init()

# 初始化 Tello 無人機
me = Tello()
me.connect()
print("現存電池容量: ", me.get_battery())
me.streamon()

# 使用者模式選擇
print('請輸入控制模式，鍵盤為1，自動為0:')
mode = int(input())
if mode == 0:
    print('請輸入來回次數: ')
    run = int(input())
    print('請輸入來回速度(輸入0則設為預設10): ')
    speed = int(input())
    if speed == 0:
        speed = 10
    print('請輸入來回距離(輸入0則設為預設50): ')
    distance = int(input())
    if distance == 0:
        distance = 10


# 初始化 MediaPipe 和 YOLO 模組
mp_pose = mp.solutions.pose
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
model = YOLO('yolov8n.pt')
target_class = 67

# 全域變數
running = True
pause = False
wrong = False  # 0 是轉頭，1 是手機
warning_turn_path = 'warning_turn.png'
warning_phone_path = 'warning_phone.png'
frame_counter = 0
detection_interval = 3  # 每 3 幀執行一次 YOLO 偵測
results = []  # 初始化結果變數，避免未定義問題

# 確保存檔目錄存在
screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

# 無人機控制執行緒
def drone_control():
    global running


    duration = distance / abs(speed)

    me.takeoff()
    me.send_rc_control(0, 0, 20, 0)
    for i in range(run):
        print(f"第 {i + 1} 次飛行")
        me.send_rc_control(speed, 0, 0, 0)
        sleep(duration)
        me.send_rc_control(-speed, 0, 0, 0)
        sleep(duration)
        me.send_rc_control(0, 0, 0, 0)
        sleep(1)

    print("飛行完成")
    me.land()
    running = False

# 鍵盤控制執行緒
def keyboard_control():
    global running
    while running:
        vals = kp.getKey("LEFT"), kp.getKey("RIGHT"), kp.getKey("UP"), kp.getKey("DOWN"), kp.getKey("w"), kp.getKey(
            "s"), kp.getKey("a"), kp.getKey("d"), kp.getKey("q"), kp.getKey("e")

        lr, fb, up, yv = 0, 0, 0, 0
        speed = 50
        if vals[0]:
            lr = -speed
        elif vals[1]:
            lr = speed

        if vals[2]:
            fb = speed
        elif vals[3]:
            fb = -speed

        if vals[4]:
            up = speed
        elif vals[5]:
            up = -speed

        if vals[6]:
            yv = -speed
        elif vals[7]:
            yv = speed

        if vals[8]:
            me.land()
            running = False
            break

        if vals[9]:
            me.takeoff()

        me.send_rc_control(lr, fb, up, yv)
        sleep(0.05)

# 顯示警告視窗執行緒
def warning_window():
    global pause, wrong
    warning_img = cv2.imread(warning_phone_path if wrong else warning_turn_path)
    if warning_img is None:
        print("警告圖片不存在，跳過顯示！")
        pause = False
        return

    start_time = time.time()
    while pause:
        cv2.imshow('Warning', warning_img)
        if time.time() - start_time > 1:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyWindow('Warning')
    pause = False

# 儲存截圖
def save_screenshot(frame, event_type):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(screenshot_dir, f"{event_type}_{timestamp}.png")
    cv2.imwrite(filename, frame)
    print(f"已儲存截圖: {filename}")

# 啟動控制執行緒
if mode == 0:
    control_thread = threading.Thread(target=drone_control)
elif mode == 1:
    control_thread = threading.Thread(target=keyboard_control)

control_thread.start()

# 主程式
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
        mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
    while running:
        frame = me.get_frame_read().frame
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        pose_results = pose.process(frame_rgb)
        face_results = face_mesh.process(frame_rgb)

        frame_counter += 1
        if frame_counter % detection_interval == 0:
            results = model(frame, stream=True)

        detected_phone = False
        detected_head_turn = False

        # 手機檢測
        for r in results:
            for box in r.boxes:
                if int(box.cls) == target_class:
                    detected_phone = True
                    wrong = True
                    print("偵測到手機")
                    save_screenshot(frame, "phone")

        # 頭部轉動檢測
        if pose_results.pose_landmarks and face_results.multi_face_landmarks:
            landmarks = pose_results.pose_landmarks.landmark
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

            shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
            nose_x = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x
            if abs(nose_x - shoulder_center_x) > 0.03:
                detected_head_turn = True
                wrong = False
                print("偵測到轉頭")
                save_screenshot(frame, "head_turn")

         # 繪製關鍵點
        if pose_results.pose_landmarks:
             mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        if face_results.multi_face_landmarks:
            for face_landmark in face_results.multi_face_landmarks:
                mp_drawing.draw_landmarks(frame, face_landmark, mp_face_mesh.FACEMESH_CONTOURS)

        # 顯示警告視窗
        if detected_phone or detected_head_turn:
            if not pause:
                pause = True
                warning_thread = threading.Thread(target=warning_window)
                warning_thread.start()

        cv2.imshow('Drone View', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
            break

# 清理資源
me.streamoff()
me.end()
cv2.destroyAllWindows()
