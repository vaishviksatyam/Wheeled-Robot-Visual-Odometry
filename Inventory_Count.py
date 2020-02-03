import cv2
import numpy as np
import time
from datetime import datetime, timedelta
from omxplayer.player import OMXPlayer

def object_count():
    print("Object Count Started")
    end_time = datetime.now() + timedelta(seconds=10)
    Inventory_count_object = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.2:1.0-video-index0')
##    Inventory_count_object.set(3, 480)
##    Inventory_count_object.set(4, 320)

    #while datetime.now()< end_time:
    q=[0,0,0]
    _, frame = Inventory_count_object.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # hammer
    low_yellow = np.array([110, 50, 50])   ##100, 130
    high_yellow = np.array([130, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
    _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    if len(contours)>0:
        q[0] = 1
    else:
        q[0] = 0

    # wrench

    low_red = np.array([170, 120, 70])   ##100, 130
    high_red = np.array([180, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    if len(contours)>0:
        q[1] = 1
    else:
        q[1] = 0


    low_green = np.array([25, 100, 120])   ##100, 130
    high_green = np.array([30, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_green, high_green)
    _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    if len(contours)>0:
        q[2] = 1
    else:
        q[2] = 0

    print("q ", q)
##    cv2.imshow("Frame", frame)
##
##    key = cv2.waitKey(1)
##    if key == 27:
##        break
    if q[0]==0:
        print("first one missing")
        player=OMXPlayer("the_hammer_is_missing_from_the_inventory.mp3")
        return_value=0

    else:
	print("All tools available")
        return_value=3
        player=OMXPlayer("please_find_the_tools_required_for_the.mp3")

    return return_value

#object_count()
