import cv2
import numpy as np
def nothing(x):
    pass
cap = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.2:1.0-video-index0')
cap1 = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.3:1.0-video-index0')
cap2 = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.1.2:1.0-video-index0')
##cap.set(3, 480)
##cap.set(4, 320)
##cap1.set(3, 480)
##cap1.set(4, 320)
##cap2.set(3, 480)
##cap2.set(4, 320)
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 102, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 109, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 20, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 112, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)
while True:
    #_, frame = cap.read()
    #_, frame1 = cap.read()
    #frame1=frame1[110:210,0:]
    #frame1 = frame1[200:300, 0:640]
    _, frame1 = cap2.read()
    frame1=frame1[110:210,0:]
    #frame=frame1[160:220,0:480]
    #_, frame3 = cap2.read()
    hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    lower_thresh = np.array([l_h, l_s, l_v])
    upper_thresh = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower_thresh, upper_thresh)
    mean_value = mask.mean()
    print("mean_value : ", mean_value)
    result = cv2.bitwise_and(frame1, frame1, mask=mask)
    #cv2.imshow("0", frame)
    cv2.imshow("1", frame1)
    #cv2.imshow("2", frame2)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cap1.release()
cap2.release()
cv2.destroyAllWindows()
 