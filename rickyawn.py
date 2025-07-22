import cv2,dlib,time,webbrowser
from scipy.spatial import distance as dist
from imutils import face_utils
path="shape_predictor_68_face_landmarks.dat"
link="https://tinyurl.com/surpandrise"
def mar(mouth):
    a=dist.euclidean(mouth[13],mouth[19])
    b=dist.euclidean(mouth[14],mouth[18])
    c=dist.euclidean(mouth[15],mouth[17])
    d=dist.euclidean(mouth[12],mouth[16])
    marr=(a+b+c)/(2.0*d)
    return marr
mart=0.7
yc=3
detect=dlib.get_frontal_face_detector()
predict=dlib.shape_predictor(path)
(ms,me)=face_utils.FACIAL_LANDMARKS_IDXS['mouth']
cam=cv2.VideoCapture(0)
lyt=0
while True:
    ret,frame=cam.read()
    if not ret: break
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    rects=detect(gray,0)
    for rect in rects:
        shape=predict(gray, rect)
        shape=face_utils.shape_to_np(shape)
        mouth=shape[ms:me]
        marr=mar(mouth)
        cv2.drawContours(frame,[cv2.convexHull(mouth)],-1,(0,255,0),1)
        if marr>mart and (time.time()-lyt)>yc:
            print("lmao why you yawning? you sleepy already? listen to this!")
            webbrowser.open(link)
            lyt=time.time()
        cv2.putText(frame, f"MAR:{marr:.2f}",(30,30),cv2.FONT_ITALIC,0.7,(0,0,225),2)
    cv2.imshow("yawn if you're feeling sleepy",frame)
    if cv2.waitKey(1)&0xFF==27:break
cam.release()
cv2.destroyAllWindows()



