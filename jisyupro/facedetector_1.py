import cv2
import os
import numpy as np
from PIL import Image
from django.contrib.staticfiles.storage  import staticfiles_storage

# face_cascade_path = staticfiles_storage.url('/jisyupro/haarcascade_frontalface_default.xml')
# face_cascade_path = staticfiles_storage.url('a.xml')
face_cascade_path ='media/jisyupro/cascade.xml'
# face_cascade_path ='http://localhost:8000/static/jisyupro/haarcascade_frontalface_default.xml'
# face_cascade_path ='media/jisyupro/b.xml'

def save_clipped_face(img_name,upload_file):
    image_path = "images/" + img_name + ".png"
    # print(type(upload_file))
    img = np.asarray(Image.open(upload_file))
    if img.ndim == 2:  # モノクロ
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
    gray_clipped = gray[y:y+h,x:x+w]
    gray_clipped = scale_to_width(gray_clipped,640)
    cv2.imwrite("media/" + image_path,gray_clipped)
    return image_path

def scale_to_width(img, width):
    h, w = img.shape[:2]
    height = round(h * (width / w))
    dst = cv2.resize(img, dsize=(width, height))
    return dst

def main():
    img_path = "sample_face3.png"
    a = clip_face(img_path)
    cv2.imshow("gray",a)
    cv2.waitKey(0)
    print(a)

if __name__=="__main__":
    main()
