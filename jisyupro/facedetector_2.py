import cv2
import numpy as np
from PIL import Image
import os
from .models import FaceImage

def getImagesAndLabels():
    faceSamples = []
    ids = []
    faces = FaceImage.objects.all()

    for face in faces:
        face_numpy = np.array(Image.open(face.image),dtype=np.uint8)
        id = face.person.pk

        faceSamples.append(face_numpy)
        ids.append(id)

    return faceSamples,ids

def train_faces():
    print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces,ids = getImagesAndLabels()
    recognizer.train(faces, np.array(ids))

    # Save the model into trainer/trainer.yml
    recognizer.write('media/jisyupro/trainer.yml') # recognizer.save() worked on Mac, but not on Pi

    # Print the numer of faces trained and end program
    print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
