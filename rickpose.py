import cv2,mediapipe as mp,numpy as np,pyttsx3,time,webbrowser
pose=mp.solutions.pose.Pose()
mpd=mp.solutions.drawing_utils
eng=pyttsx3.init()
link="https://tinyurl.com/surpandrise"
def yap(text):
    eng.say(text)
    eng.runAndWait()
def ang(p1,p2,p3):
    a=np.array(p1)
    b=np.array(p2)
    c=np.array(p3)
    rads=np.arccos(np.clip(np.dot((a-b),(c-b))/(np.linalg.norm(a-b)*np.linalg.norm(c-b)),-1.0,1.0))
    return np.degrees(rads)
cam=cv2.VideoCapture(0)
sd=False
while cam.isOpened():
    ret,frame=cam.read()
    if not ret:break
    frame=cv2.flip(frame,1)
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result=pose.process(rgb)
    h,w,_=frame.shape
    if result.pose_landmarks:
        mpd.draw_landmarks(frame,result.pose_landmarks,mp.solutions.pose.POSE_CONNECTIONS)
        lm=result.pose_landmarks.landmark
        ls=[lm[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x*w,lm[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y*h]
        lh=[lm[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x*w,lm[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y*h]
        le=[lm[mp.solutions.pose.PoseLandmark.LEFT_EAR.value].x*w,lm[mp.solutions.pose.PoseLandmark.LEFT_EAR.value].y*h]
        angle=ang(le,ls,lh)
        cv2.putText(frame,f"Posture Angle:{int(angle)}deg",(10, 40),cv2.FONT_ITALIC,0.8,(0,255,255),2)
        if angle<135 and not sd:  
            sd=True
            yap("Posture check failed. Here's your penalty.")
            time.sleep(1.5)
            webbrowser.open(link)
            break
    cv2.imshow("Posture Checker",frame)
    if cv2.waitKey(1)&0xFF==27:break
cam.release()
cv2.destroyAllWindows()