from flask import Flask,request,jsonify,render_template_string, face_recognition, numpy as np, cv2, base64, os
app=Flask(__name__)
app.secret_key='yes'
sip=""
if not os.path.exists(sip): raise FileNotFoundError(f"source image not found at {sip}")
si=face_recognition.load_image_file(sip)
se=face_recognition.face_encodings(si)
if not se: raise ValueError("no face found")
se1=se[0]
