from flask import Flask, request, jsonify
import face_recognition
import cv2
import base64
import numpy as np
import os
import datetime
import shutil
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PORT = int(os.environ.get("PORT", 5000))

@app.route("/face/check", methods=["POST"])
def check_face():
    data = request.json
    image_data = base64.b64decode(data["image"].split(",")[1])
    img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    face_locations = face_recognition.face_locations(img)
    return jsonify(hasFace=bool(face_locations))

@app.route("/register-face", methods=["POST"])
def register_face():
    data = request.json
    username = data.get("username")
    images = data.get("images")

    if not username or not images:
        return jsonify(success=False, message="요청 데이터 누락")

    user_dir = os.path.join("encodings", username)
    os.makedirs(user_dir, exist_ok=True)

    all_encodings = []

    for idx, img_base64 in enumerate(images):
        img_data = base64.b64decode(img_base64.split(",")[1])
        img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        img_path = os.path.join(user_dir, f"{timestamp}_{idx+1}.jpg")
        cv2.imwrite(img_path, img)

        face_locations = face_recognition.face_locations(img)
        encodings = face_recognition.face_encodings(img, face_locations)
        if encodings:
            all_encodings.append(encodings[0])

    if not all_encodings:
        return jsonify(success=False, message="인코딩 실패")

    enc_path = os.path.join(user_dir, f"{username}.npy")
    if os.path.exists(enc_path):
        existing = np.load(enc_path, allow_pickle=True)
        all_encodings = list(existing) + all_encodings

    np.save(enc_path, all_encodings)

    return jsonify(success=True, message="등록 완료")

@app.route("/admin/face-users", methods=["GET"])
def list_users():
    users = []
    if os.path.exists("encodings"):
        for user in os.listdir("encodings"):
            if os.path.isfile(os.path.join("encodings", user, f"{user}.npy")):
                users.append(user)
    return jsonify(users)

@app.route("/admin/delete-face/<username>", methods=["DELETE"])
def delete_user(username):
    user_dir = os.path.join("encodings", username)
    if os.path.exists(user_dir):
        shutil.rmtree(user_dir)
        return jsonify(success=True, message="삭제 완료")
    else:
        return jsonify(success=False, message="사용자 없음")

@app.route("/verify-face", methods=["POST"])
def verify_face():
    data = request.json
    image_data = base64.b64decode(data["image"].split(",")[1])
    img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)

    input_encs = face_recognition.face_encodings(img)
    if not input_encs:
        return jsonify(success=False, message="인식 실패", username=None)

    input_enc = input_encs[0]

    for user in os.listdir("encodings"):
        enc_path = os.path.join("encodings", user, f"{user}.npy")
        if os.path.exists(enc_path):
            known_encs = np.load(enc_path, allow_pickle=True)
            results = face_recognition.compare_faces(known_encs, input_enc)
            if True in results:
                return jsonify(success=True, username=user, message="로그인 성공")

    return jsonify(success=False, username=None, message="등록되지 않은 얼굴입니다")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
