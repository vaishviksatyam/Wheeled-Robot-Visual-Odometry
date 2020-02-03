import cv2
import numpy as np
from omxplayer.player import OMXPlayer
import time
from datetime import datetime, timedelta
print("Face detection import")

Status=0
def nothing(x):
    pass

def face_and_Helmet_detect():
    global Status
    Face_detection_object = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.2:1.0-video-index0')
##    Face_detection_object.set(3,640)
##    Face_detection_object.set(4,480)
    print("Face camera initialised")
    end_time = datetime.now() + timedelta(seconds=30)
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    
    while (datetime.now() < end_time):

	#print("starting of the frame capture")
        q=[0,0]
        try:
            _, frame = Face_detection_object.read()
        except:
            if(frame==None):
                print("Frame is None")
                return 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 2)
        if len(faces)>0:
            q[0] = 1
        else:
            q[0] = 0
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        low_yellow = np.array([25, 100, 120])
        high_yellow = np.array([30, 255, 255])
        red_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
        _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
	print("processing done")
        if len(contours)>0:
            q[1] = 1
        else:
            q[1] = 0

        if q[0] == 1:
            return_value=1
            print("Intruder_alert!")
            #player=OMXPlayer("intruder_alert.mp3")
            Status=1

        if q[1]==1 and q[0]==1:
            return_value=2
            #player=OMXPlayer("you_are_authorized_to_enter_this_zone.mp3")
            print("Detected both face and helmet, Ending my Watch")
            
        if  q[0] == 0:
            return_value=0
            print("person missing")
    print("done with fucntion")
    Face_detection_object.release()
    return return_value

face_and_Helmet_detect()
