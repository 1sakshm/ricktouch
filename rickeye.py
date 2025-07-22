import cv2,dlib,time,webbrowser
from scipy.spatial import distance as dist
from imutils import face_utils
path="shape_predictor_68_face_landmarks.dat"
link="https://tinyurl.com/surpandrise"
def ear(eye):
    a=dist.euclidean(eye[1],eye[5])
    b=dist.euclidean(eye[2],eye[4])
    c=dist.euclidean(eye[0],eye[3])
    eyr=(a+b)/(2.0*c)
    return eyr
earth=0.21
earcf=3
detect=dlib.get_frontal_face_detector()
predict=dlib.shape_predictor(path)
(ist,ie)=face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rs,re)=face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
cap=cv2.VideoCapture(0)
bc=0
bt=[]
while True:
    ret,frame=cap.read()
    if not ret: break
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    rects=detect(gray,0)
    for rect in rects:
        shape=predict(gray,rect)
        shape=face_utils.shape_to_np(shape)
        leftI=shape[ist:ie]
        rightI=shape[rs:re]
        leftE=ear(leftI)
        rightE=ear(rightI)
        eyr=(leftE+rightE)/2.0
        leftH=cv2.convexHull(leftI)
        rightH=cv2.convexHull(rightI)
        cv2.drawContours(frame,[leftH],-1,(0,255,0),1)
        cv2.drawContours(frame,[rightH],-1,(0,255,0),1)
        if eyr<earth:
            bt.append(time.time())
            if len(bt)>1 and bt[-1]-bt[-2]<0.2:bt.pop()
        else:
            if len(bt)>=2 and bt[-1]-bt[-2]<2:
                print("haha u blinked twice")
                webbrowser.open(link)
                bt=[]
                time.sleep(2)
    cv2.imshow("blink twice pls",frame)
    if cv2.waitKey(1)&0xFF==27:break
cap.release()
cv2.destroyAllWindows()
