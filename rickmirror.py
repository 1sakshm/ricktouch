import cv2,mediapipe as mp,time,pyttsx3,webbrowser
mpfm=mp.solutions.face_mesh
face_mesh=mpfm.FaceMesh(refine_landmarks=True)
mpd=mp.solutions.drawing_utils
engine=pyttsx3.init()
link="https://tinyurl.com/surpandrise"
cam=cv2.VideoCapture(0)
ls=None
lt=3
l=False
def yap(text):
    engine.say(text)
    engine.runAndWait()
def ils(landmarks):
    leftI=landmarks[33]
    rightI=landmarks[263]
    nose=landmarks[1]
    eyed=abs(leftI.x-rightI.x)
    ntc=abs((leftI.x+rightI.x)/2-nose.x)
    return ntc<eyed*0.05
while True:
    ret,frame=cam.read()
    if not ret:break
    frame=cv2.flip(frame,1)
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=face_mesh.process(rgb)
    h,w,_=frame.shape
    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            mpd.draw_landmarks(frame,landmarks,mpfm.FACEMESH_CONTOURS)
            if ils(landmarks.landmark):
                if not ls:ls=time.time()
                elif time.time()-ls>=lt and not l:
                    l=True
                    yap("You're looking pretty good today")
                    time.sleep(2)
                    yap("psych")
                    webbrowser.open(link)
            else:ls=None
    else:ls=None
    cv2.imshow("see how you look today", frame)
    if cv2.waitKey(1)&0xFF==27:break
cam.release()
cv2.destroyAllWindows()

                