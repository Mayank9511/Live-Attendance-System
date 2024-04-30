from sklearn.neighbors import KNeighborsClassifier

import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime

from win32com.client import Dispatch

def speak(str1):
    speak=Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)


video = cv2.VideoCapture(1)
facedetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

with open('data/names.pkl', 'rb') as f:
    LABELS=pickle.load(f)
with open('data/face_data.pkl', 'rb') as f:
    FACES=pickle.load(f)

knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

imBackground = cv2.imread("bg6.png")

COL_NAMES = ['Name','Time']

while True:
    ret,frame=video.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=facedetect.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        crop_img=frame[y:y+h, x:x+w, :]
        resized_img=cv2.resize(crop_img,(50,50)).flatten().reshape(1,-1)
        output=knn.predict(resized_img)
        ts=time.time()
        date=datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp=datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")

        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255),1)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (50,50,255),2)
        cv2.rectangle(frame, (x,y-40), (x+w,y), (50,50,255),-1)
        cv2.putText(frame,str(output[0]),(x,y-15),cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),1 )
        cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),1)
        attendance=[str(output[0]),str(timestamp)]
    imBackground[162:162 + 480, 55:55 + 640] = frame 
    # imBackground[250:250 + 680, 150:150 + 760] = frame 
    cv2.imshow("Frame",imBackground)
    k=cv2.waitKey(1)
    if k==ord('t'):
        speak("Attendance Taken..")
        time.sleep(1)
        if exist:
            with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(attendance)
            csvfile.close()
        else:
            with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)
            csvfile.close()
    if k==ord('a'):
        break
video.release()
cv2.destroyAllWindows()
 
