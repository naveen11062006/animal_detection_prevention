import cv2
import serial
import time
from ultralytics import YOLO

# =========================
# Arduino Serial Setup
# =========================
arduino = serial.Serial("COM3", 9600, timeout=1)  # Change COM port
time.sleep(2)

# =========================
# Load YOLO Model
# =========================
model = YOLO("yolov8n.pt")

# Animal classes YOLO detects (COCO dataset)
ANIMALS = [
    "bird", "cat", "dog", "horse", "sheep",
    "cow", "elephant", "bear", "zebra", "giraffe"
]

# =========================
# Camera Setup
# =========================
cap = cv2.VideoCapture(0)

animal_count = 0
previous_detection = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    animal_detected = False

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]

            if class_name in ANIMALS:
                animal_detected = True

                # Draw bounding box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, class_name, (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    # =========================
    # Detection Logic
    # =========================
    if animal_detected and not previous_detection:
        animal_count += 1

        if animal_count == 1:
            arduino.write(b'1')  # Low sound
            print("First Animal Detected")
        elif animal_count == 2:
            arduino.write(b'2')  # Medium sound
            print("Second Animal Detected")
        else:
            arduino.write(b'3')  # High sound
            print("Third or More Animal Detected")

    elif not animal_detected:
        arduino.write(b'0')  # No animal → stop LED & buzzer

    previous_detection = animal_detected

    cv2.imshow("Animal Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()