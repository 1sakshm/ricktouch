import cv2, mediapipe as mp, time, webbrowser as wb
mph=mp.solutions.hands
mpd=mp.solutions.drawing_utils
hands=mph.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
def touch(landmarks, imgw, imgh, threshold=40):
    x1,y1=int(landmarks[4].x*imgw), int(landmarks[4].y*imgh)
    x2,y2=int(landmarks[12].x*imgw), int(landmarks[12].y*imgh)
    dist=((x2-x1)**2+(y2-y1)**2)**0.5
    return dist < threshold, (x1,y1), (x2,y2)
cam=cv2.VideoCapture(0)
triggered=False
ltt=0
cool=10
while True:
    ret, frame=cam.read()
    if not ret: break
    frame=cv2.flip(frame,1)
    rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results=hands.process(rgb)
    imgh,imgw,_=frame.shape
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mpd.draw_landmarks(frame,hand_landmarks,mph.HAND_CONNECTIONS)
            tou,p1,p2=touch(hand_landmarks.landmark,imgw,imgh)
            cv2.circle(frame,p1,12,(0,255,0) if tou else (0,0,255), -1)
            cv2.circle(frame,p2,12,(0,255,0) if tou else (0,0,255), -1)
            if tou and not triggered and (time.time()-ltt>cool):
                wb.open('https://tinyurl.com/surpandrise')
                triggered=True
                ltt=time.time()
            if not tou: triggered=False
        cv2.putText(frame, "touch thumb & middle finger for a surprise", (10,30), cv2.FONT_ITALIC,0.8,(50,50,200),2)
        cv2.imshow('surprise!!!',frame)
        if cv2.waitKey(1) & 0xFF == 27: break
cam.release()
cv2.destroyAllWindows()


