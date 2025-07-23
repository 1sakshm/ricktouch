import cv2,dlib,time,pyttsx3,webbrowser,numpy as np
from imutils import face_utils
from scipy.spatial import distance as dist
earth=0.21
cf=3
nbl=10
link=""
eng=pyttsx3.init()
yap=lambda t: (eng.say(t), eng.runAndWait())
detect=dlib.get_frontal_face_detector()
predict=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
(ise,ie)=face_utils.FACIAL_LANDMARKS_IDXS("left_eye")
(rs,re)=face_utils.FACIAL_LANDMARKS_IDXS("right_eye")
def ear(eye):
    a=dist.euclidean(eye[1],eye[5])
    b=dist.euclidean(eye[2],eye[4])
    c=dist.euclidean(eye[0],eye[3])
    return (a+b)/(c*2.0)
cam=cv2.VideoCapture(0)
bc=0
lbt=time.time()
rickrolled=False
print("keep blinking or else....")
while True:
    ret,frame=cam.read()
    if not ret:break
    frame=cv2.flip(frame,1)
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    rects=detect(gray)
    for rect in rects:
        shape=predict(gray,rect)
        shape=face_utils.shape_to_np(shape)
        leftI=shape[ise:ie]
        rightI=shape[rs:re]
        leftE=ear(leftI)
        rightE=ear(rightI)
        eyr=(leftE+rightE)/2.0
        cv2.putText(frame,f"EAR:{eyr:2f}",(10,30),cv2.FONT_ITALIC,0.7,(255,255,0),2)
        if eyr<earth:bc+=1
        if bc>=cf:lbt=time.time()
        bc=0