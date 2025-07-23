import cv2
import numpy as np
import mediapipe as mp
import time
import pyttsx3
import webbrowser
import os

engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

rick_img_path = 'img.png'
rick_face = cv2.imread(rick_img_path, cv2.IMREAD_UNCHANGED)
if rick_face is None:
    raise FileNotFoundError("Please add a transparent Rick Astley face image as 'rick_astley_face.png'.")

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)
start_time = None
rickrolled = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks and not rickrolled:
        landmarks = results.multi_face_landmarks[0].landmark
        left_eye = landmarks[33]
        right_eye = landmarks[263]
        nose = landmarks[1]

        eye_dist = np.linalg.norm(np.array([left_eye.x - right_eye.x, left_eye.y - right_eye.y]))
        face_width = int(eye_dist * w * 2.2)
        face_height = int(face_width * rick_face.shape[0] / rick_face.shape[1])

        cx = int(nose.x * w)
        cy = int(nose.y * h)

        x1 = cx - face_width // 2
        y1 = cy - face_height // 2
        x2 = x1 + face_width
        y2 = y1 + face_height

        resized_rick = cv2.resize(rick_face, (face_width, face_height))
        b, g, r, a = cv2.split(resized_rick)
        overlay = cv2.merge((b, g, r))
        mask = cv2.merge((a, a, a))

        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        roi = frame[y1:y2, x1:x2]

        if roi.shape[:2] == mask[0:roi.shape[0], 0:roi.shape[1]].shape[:2]:
            masked_bg = cv2.bitwise_and(roi, cv2.bitwise_not(mask[0:roi.shape[0], 0:roi.shape[1]]))
            masked_fg = cv2.bitwise_and(overlay[0:roi.shape[0], 0:roi.shape[1]], mask[0:roi.shape[0], 0:roi.shape[1]])
            frame[y1:y2, x1:x2] = cv2.add(masked_bg, masked_fg)

        if start_time is None:
            start_time = time.time()
        elif time.time() - start_time > 4:
            speak("You have become the Rick.")
            time.sleep(10)
            webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            rickrolled = True

    cv2.imshow("Rick Face Swap", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
