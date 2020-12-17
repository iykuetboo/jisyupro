import cv2
import numpy as np
import os
from .models import Member
from PIL import Image

face_cascade_path ='media/jisyupro/cascade.xml'

def recognize_face(upload_file):

	recognizer = cv2.face.LBPHFaceRecognizer_create()
	recognizer.read('media/jisyupro/trainer.yml')

	img = np.asarray(Image.open(upload_file))
	if img.ndim == 2:
	# print("monotone")
		pass
	elif img.shape[2] == 3:  # カラー
		# print("RGB")
		img = img[:, :, ::-1]
	elif img.shape[2] == 4:  # 透過
		# print("RGBA")
		img = img[:, :, [2, 1, 0, 3]]
	face_detector = cv2.CascadeClassifier(face_cascade_path)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_detector.detectMultiScale(gray, 1.3, 5)
	if len(faces)==0:
		return None

	x,y,w,h = faces[0]

	id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
	# cv2.rectangle(img, (x,y), (x+w,y+h), 255, 3)

    # Check if confidence is less them 100 ==> "0" is perfect match
	if confidence < 100:
		id = Member.objects.get(pk=id).name
		confidence = "  {0}%".format(round(100 - confidence))
	else:
		id = "unknown"
		confidence = "  {0}%".format(round(100 - confidence))

	return [id,confidence,img]
