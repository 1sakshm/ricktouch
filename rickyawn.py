import cv2
import dlib
import time
import webbrowser
from scipy.spatial import distance as dist
from imutils import face_utils

# Path to dlib's pre-trained facial landmark detector
PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
LINK = "https://tinyurl.com/surpandrise"  # Change to your desired link

def mouth_aspect_ratio(mouth):
    # compute the euclidean distances between the vertical mouth landmarks
    A = dist.euclidean(mouth[13], mouth[19])  # 51, 59
    B = dist.euclidean(mouth[14], mouth[18])  # 52, 58
    C = dist.euclidean(mouth[15], mouth[17])  # 53, 57
    # compute the euclidean distance between the horizontal mouth landmarks
    D = dist.euclidean(mouth[12], mouth[16])  # 49, 55
    mar = (A + B + C) / (2.0 * D)
    return mar

MAR_THRESH = 0.7  # You may need to adjust this threshold
YAWN_COOLDOWN = 3  # seconds

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)

(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

cap = cv2.VideoCapture(0)
last_yawn_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        mouth = shape[mStart:mEnd]
        mar = mouth_aspect_ratio(mouth)

        # Draw mouth contour
        cv2.drawContours(frame, [cv2.convexHull(mouth)], -1, (0, 255, 0), 1)

        # Yawn detection
        if mar > MAR_THRESH and (time.time() - last_yawn_time) > YAWN_COOLDOWN:
            print("Yawn detected! Opening link...")
            webbrowser.open(LINK)
            last_yawn_time = time.time()

        # Optionally, display MAR value
        cv2.putText(frame, f"MAR: {mar:.2f}", (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Yawn Detector", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
