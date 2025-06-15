import qrcode
import face_recognition
import os
from PIL import Image

def generate_qr(data):
    img = qrcode.make(data)
    path = "static/event_qr.png"
    img.save(path)
    return path

def match_faces(user_image_path, folder_path):
    matches = []
    user_img = face_recognition.load_image_file(user_image_path)
    user_enc = face_recognition.face_encodings(user_img)[0]

    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        img = face_recognition.load_image_file(img_path)
        encs = face_recognition.face_encodings(img)
        for face_encoding in encs:
            results = face_recognition.compare_faces([user_enc], face_encoding)
            if results[0]:
                matches.append(f"/static/uploaded_photos/{filename}")
    return matches
