import cv2,dlib,time,pyttsx3,webbrowser
from scipy.spatial import distance as dist
from imutils import face_utils
link="https://tinyurl.com/surpandrise"
earth=0.21
cf=3
eng=pyttsx3.init()
yap=lambda text: (eng.say(text),eng.runAndWait())
detect=dlib.get_frontal_face_detector()
predict=dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
(ise,ie)=face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rs,re)=face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
def ear(eye):
    a=dist.euclidean(eye[1],eye[5])
    b=dist.euclidean(eye[2],eye[4])
    c=dist.euclidean(eye[0],eye[3])
    eyr=(a+b)/(c*2.0)
    return eyr
cam=cv2.VideoCapture(0)
bc=0
b=False
st=time.time()
print("dont blink")
while True:
    ret,frame=cam.read()
    if not ret:break
    frame=cv2.flip(frame,1)
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    rects=detect(gray,0)
    for rect in rects:
        shape=predict(gray,rect)
        shape=face_utils.shape_to_np(shape)
        leftI=shape[ise:ie]
        rightI=shape[rs:re]
        leftE=ear(leftI)
        rightE=ear(rightI)
        eyr=(leftE+rightE)/2.0
        cv2.polylines(frame,[leftI],True,(0,255,0),1)
        cv2.polylines(frame,[rightI],True,(0,255,0),1)
        cv2.putText(frame,f"EAR:{eyr:2f}",(10,30),cv2.FONT_ITALIC,0.7,(0.255,255),2)
        if eyr<earth:bc+=1
        else: 
            if bc>=cf and not b:
                b=True
                et=time.time()
                duration=round(et-st,2)
                print(f"\nyou blinked! you lasted: {duration} seconds")
                yap(f"\nyou blinked! you lasted: {duration} seconds. now get ready for your punishment")
                time.sleep(1)
                webbrowser.open(link)
            bc=0
    if b:break
    cv2.imshow("Eye Contact Challenge", frame)
    if cv2.waitKey(1)&0xFF==27:break
cam.release()
cv2.destroyAllWindows()