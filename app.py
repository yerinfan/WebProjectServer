from flask import Flask, request, jsonify
import face_recognition
import numpy as np
from PIL import Image
import io
import base64
import os

app = Flask(__name__)

# 서버 시작 시 등록된 얼굴 인코딩 불러오기
known_face_encodings = []
known_face_names = []

def load_known_faces():
    for filename in os.listdir("known_faces"):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join("known_faces", filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(os.path.splitext(filename)[0])

load_known_faces()

@app.route("/face/login", methods=["POST"])
def face_login():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    img = face_recognition.load_image_file(file)
    encodings = face_recognition.face_encodings(img)

    if not encodings:
        return jsonify({"success": False, "message": "No face found"}), 200

    user_encoding = encodings[0]
    results = face_recognition.compare_faces(known_face_encodings, user_encoding)
    matched_names = [name for match, name in zip(results, known_face_names) if match]

    if matched_names:
        return jsonify({"success": True, "user": matched_names[0]}), 200
    else:
        return jsonify({"success": False, "message": "Face not recognized"}), 200

@app.route("/")
def index():
    return "✅ Face login server is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)