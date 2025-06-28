from flask import Flask, request, jsonify
import mediapipe as mp
import cv2
import numpy as np
import base64
import os
import datetime
import shutil
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

mp_face_detection = mp.solutions.face_detection
face_detector = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

ENCODING_DIR = "encodings"
os.makedirs(ENCODING_DIR, exist_ok=True)

def decode_image(image_base64):
    image_data = base64.b64decode(image_base64.split(',')[1])
    np_arr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

def detect_face(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = face_detector.process(img_rgb)
    return result.detections

@app.route("/face/check", methods=["POST"])
def check_face():
    data = request.json
    img = decode_image(data["image"])
    detections = detect_face(img)
    return jsonify(hasFace=bool(detections))

@app.route("/register-face", methods=["POST"])
def register_face():
    data = request.json
    username = data.get("username")
    images = data.get("images")

    if not username or not images:
        return jsonify(success=False, message="요청 데이터 누락")

    user_dir = os.path.join(ENCODING_DIR, username)
    os.makedirs(user_dir, exist_ok=True)

    saved = 0
    for idx, img_base64 in enumerate(images):
        img = decode_image(img_base64)
        detections = detect_face(img)

        if detections:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(user_dir, f"{ts}_{idx+1}.jpg")
            cv2.imwrite(path, img)
            saved += 1

    if saved == 0:
        return jsonify(success=False, message="얼굴이 감지되지 않아 저장되지 않았습니다.")
    
    return jsonify(success=True, message=f"{saved}장 저장 완료")

@app.route("/admin/face-users", methods=["GET"])
def list_users():
    users = [u for u in os.listdir(ENCODING_DIR) if os.path.isdir(os.path.join(ENCODING_DIR, u))]
    return jsonify(users)

@app.route("/admin/delete-face/<username>", methods=["DELETE"])
def delete_user(username):
    user_dir = os.path.join(ENCODING_DIR, username)
    if os.path.exists(user_dir):
        shutil.rmtree(user_dir)
        return jsonify(success=True, message="삭제 완료")
    return jsonify(success=False, message="사용자 없음")

@app.route("/")
def health_check():
    return "Mediapipe 기반 얼굴 등록 서버 정상 동작 중"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
