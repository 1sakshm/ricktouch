from flask import Flask,request,jsonify,render_template_string
import face_recognition, numpy as np, cv2, base64, os
app=Flask(__name__)
app.secret_key='yes'
sip="C:\\Users\\Saksham\\ricktouch\\source.jpg"
if not os.path.exists(sip): raise FileNotFoundError(f"source image not found at {sip}")
si=face_recognition.load_image_file(sip)
se=face_recognition.face_encodings(si)
if not se: raise ValueError("no face found")
se1=se[0]
html='''
<!DOCTYPE html>
<html>
<head>
    <title>verify your FACE</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            min-height: 100vh;
            margin: 0;
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
            display: flex;
            align-items: center;
            justify-content: center;}
        .container {
            background: #fff;
            border-radius: 18px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.18);
            padding: 2.5rem 2rem 2rem 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            max-width: 400px;
            width: 100%;}
        h1 {
            margin-bottom: 1.5rem;
            color: #2d3a4b;
            font-weight: 700;
            letter-spacing: 1px;
            text-align: center;
            font-family: 'Poppins', 'Segoe UI', Arial, sans-serif;
            font-size: 1.6rem;
            line-height: 1.3;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;}
        video {
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(44, 62, 80, 0.12);
            margin-bottom: 1.2rem;
            width: 320px;
            height: 240px;
            background: #222;}
        button {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            margin-bottom: 1.2rem;
            transition: background 0.2s, transform 0.2s;
            box-shadow: 0 2px 8px rgba(44, 62, 80, 0.08);}
        button:hover {
            background: linear-gradient(90deg, #5a67d8 0%, #6b47b6 100%);
            transform: translateY(-2px) scale(1.03);}
        {   font-size: 1.1rem;
            font-weight: 500;
            color: #444;
            min-height: 1.5em;
            text-align: center;
            margin-top: 0.5rem;}
    </style>
</head>
<body>
    <div class="container">
        <h1>scan your face to find out if you are ready for a surprise</h1>
        <video id="face" autoplay></video><br>
        <button id="verification button">Verify Your Face</button>
        <p id="result"></p>
    </div>
    <script>
        const video=document.getElementById("face"),button=document.getElementById("verification button"),result=document.getElementById("result");
        navigator.mediaDevices.getUserMedia({video:true})
            .then(stream => { video.srcObject = stream; })
            .catch(err => {result.textContent = "Camera error: " + err.name + " - " + err.message;
                result.style.color = "#e74c3c";});
        button.onclick = function() {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            const dataURL = canvas.toDataURL('image/png');
            fetch('/verify',{method:'POST',headers:{'Content-Type':'application/json'},body: JSON.stringify({image: dataURL})})
            .then(res => res.json())
            .then(data => {
                if(data.match){result.textContent = "✅ Face matched. Welcome!";
                    result.style.color = "#2ecc40";
                    setTimeout(function() {window.location.href = "https://tinyurl.com/surpandrise"; // <-- your URL}, 1000);} 
                else {result.textContent = data.error || "❌ Face not recognized.";
                    result.style.color = "#e74c3c";}});};
    </script>
</body>
</html>
'''
@app.route('/',methods=['GET'])
def auth_index():
    return render_template_string(html)
@app.route('/verify',methods=['POST'])
def verify():
    data=request.json
    imgd=data['image'].split(',')[1]
    imgb=base64.b64decode(imgd)
    nparr=np.frombuffer(imgb,np.uint8)
    img=cv2.imdecode(nparr,cv2.IMREAD_COLOR)
    try:
        fe=face_recognition.face_encodings(img)
        if not fe: return jsonify({'match':False, 'error':'no face detected boy'})
        match=face_recognition.compare_faces([se1],fe[0])[0]
        return jsonify({'match':bool(match)})
    except Exception as e: return jsonify({'match':False, 'error':str(e)})
if __name__=='__main__':
    app.run(debug=True)