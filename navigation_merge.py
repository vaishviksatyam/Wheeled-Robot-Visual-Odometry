####################################################################### LIBRARY INITIALISATION
print("initialising libraries")
import RPi.GPIO as GPIO
from time import sleep
import numpy as np
import time
import cv2
import sys
#from face_detection import face_and_Helmet_detect
#from Inventory_Count import *
from rec_module import *
from omxplayer.player import OMXPlayer
from datetime import datetime, timedelta
print("import complete")
# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO    = 24
GPIO_BUZZER_OUTPUT = 16
RED = 11
GREEN = 12
BLUE = 13
vlaue=1

path ="/home/pi/Desktop/ACCENTURE_USE_CASES/"

######################################################################## GPIO INITIALISATION

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(GPIO_BUZZER_OUTPUT,GPIO.OUT)
GPIO.output(GPIO_BUZZER_OUTPUT, False)
GPIO.setup(37,GPIO.OUT)
GPIO.setup(35,GPIO.OUT)
GPIO.setup(31,GPIO.OUT)
GPIO.setup(32,GPIO.OUT)
GPIO.setup(RED,GPIO.OUT)
GPIO.output(RED,0)
GPIO.setup(GREEN,GPIO.OUT)
GPIO.output(GREEN,0)
GPIO.setup(BLUE,GPIO.OUT)
GPIO.output(BLUE,0)
motor_1= 38
motor_2= 40
GPIO.setup(motor_2,GPIO.OUT)
GPIO.setup(motor_1,GPIO.OUT)
pi_pwm1 = GPIO.PWM(motor_1,100)
pi_pwm2 = GPIO.PWM(motor_2,100)
pi_pwm1.start(0)
pi_pwm2.start(0)

GPIO.output(31, 1)
GPIO.output(32, 1)




######################################################################### VARIABLE INITIALISATION
base_speed=80
max_correction = 40
Navigation_status=False
counter=0
Route ="UCA"
UpdateString=[0,0,0,0,0,0]


##################################### Functions #####################################
###################################iNVENTORY COUNT###################
def object_count():
##    Down_camera.release()
##    Front_camera.release()
    GPIO.output(31, 0)
    GPIO.output(32, 1)
    time.sleep(2)
    GPIO.output(31, 0)
    GPIO.output(32, 0)
    print("Object Count Started")
    end_time = datetime.now() + timedelta(seconds=20)
    Inventory_count_object = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.2:1.0-video-index0')
##    Inventory_count_object.set(3, 480)
##    Inventory_count_object.set(4, 320)

    while datetime.now()< end_time:
        q=[0,0,0]
        _, frame = Inventory_count_object.read()
        if(frame==None):
            #time.sleep(3)
            print("frame none")
    ##        player=OMXPlayer(path+"Please find the tools required for.mp3")
    ##        player.set_volume(4)
            
            #return 0
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # hammer
        low_yellow = np.array([116, 105, 90])   ##100, 130
        high_yellow = np.array([130, 255, 255])
        red_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
        _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
        if len(contours)>0:
            q[0] = 1
        else:
            q[0] = 0

        # wrench

        low_red = np.array([70, 107, 97])   ##100, 130
        high_red = np.array([82, 131, 133])
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
            player=OMXPlayer(path+"The hammer is missing from the inventory I will raise an incident.mp3")
            player.set_volume(1)
            time.sleep(5)
            return_value=0
            Inventory_count_object.release()
            print("released")
            Inventory_count_object = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.2:1.0-video-index0')
            print("captured again")
            

        elif q[0]==1:
            print("All tools available")
            return_value=3
            player=OMXPlayer(path+"Please find the tools required for the valve repair.mp3")
            player.set_volume(1)
            time.sleep(5)
            Inventory_count_object.release()
            print("released")
            Inventory_count_object = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.2:1.0-video-index0')
            print("captured again")
        
    #Inventory_count_object.release()
    return return_value

#object_count()


################################## FACE####################
Status=0
def nothing(x):
    pass

def face_and_Helmet_detect():
    global Status
#    Down_camera.release()
#    Front_camera.release()
    Face_detection_object = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.2:1.0-video-index0')
##    Face_detection_object.set(3,640)
##    Face_detection_object.set(4,480)
    print("Face camera initialised")
    end_time = datetime.now() + timedelta(seconds=30)
    face_cascade = cv2.CascadeClassifier(path+"haarcascade_frontalface_default.xml")
##    time.sleep(7)
##    player=OMXPlayer(path+"you are authorized to enter this zone. As .mp3")
##    player.set_volume(4)
    q=[0,0]
    while (datetime.now() < end_time):
        
        _, frame = Face_detection_object.read()
        print("starting of the frame capture")
    ##        print("counter: ",count)
        #print("starting of the frame capture")
        print("frame taken")
        if(frame==None):
	    #time.sleep(5)
            #player=OMXPlayer(path+"You are not authorized to enter this zone.mp3")
            #player=OMXPlayer(path+"you are authorized to enter this zone as.mp3")
            #player.set_volume(4)
            #time.sleep(5)
            print("Frame is None")
            print("done with function from None")
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
    ##        print("helllloooo"+str(q[0])+","+str(q[1]))
        if q[1]==1 and q[0]==1:
            return_value=1
            print("Detected both face and helmet, Ending my Watch")
##            player=OMXPlayer(path+"you are authorized to enter this zone as.mp3")
##            player.set_volume(1)  
##            time.sleep(10)
##            print("helmet end")
            Face_detection_object.release()
	    print("camera released")
            Face_detection_object = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.2:1.0-video-index0')
            print("object created")

        elif q[0] == 1 and q[1]==0 :
            return_value=1
            print("Intruder_alert!")
##            player=OMXPlayer(path+"You are not PPE compliant You are not allowed in this zone, please exit immediately This will be logged as a safety incident.mp3")
##            player.set_volume(1)
##            time.sleep(1)
##            GPIO.output(31, 1)
##            GPIO.output(32, 0)
##            time.sleep(1)
##            GPIO.output(31, 0)
##            GPIO.output(32, 0)
##            time.sleep(8)
##            print("intruder end")
            Face_detection_object.release()
            Face_detection_object = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.2:1.0-video-index0')
          
        elif  q[0] == 0 :
            return_value=0
            print("person missing")
            #player=OMXPlayer(path+"Equipment Unmanned, authorized personnel please report to the area immediately.mp3")
            #player.set_volume(1)
            #time.sleep(5)
            Face_detection_object.release()
	    Face_detection_object = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.2:1.0-video-index0')
        
        #Face_detection_object.release()
    
    print(" face camera released",return_value)
    return return_value

#########################################################################
def RGB(x, y, z):
    print("inside")

    GPIO.output(RED,x)
    GPIO.output(GREEN,y)
    GPIO.output(BLUE,z)

def UpdateString_f():

    global UpdateString
    #print("from UpdateString: "+str(UpdateString))
    return str(UpdateString)

def motor1(direction):

        if(direction==0):
            #print("motor1 changed to front")

            GPIO.output(37, False)
        elif(direction==1):
            #print("motor1 changed to Back")
            GPIO.output(37, True)

def motor2(direction):

        if(direction==0):
            #print("motor2 changed to front")
            GPIO.output(35, False)
        elif(direction==1):
            #print("motor2 changed to Back")
            GPIO.output(35, True)

def camera():
    global times
    global frame2

    _, frame = Down_camera.read()
    frame=frame[110:210,0:]
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # red color
    low_red = np.array([102, 109, 20])
    high_red = np.array([112, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    mean_value = red_mask.mean()
    print("mean_value", mean_value)

    if mean_value>=50:
        #print("1")
        times=1
        #print("got it")
    else:
        #print("0")
        times=0
        #print(" didn't got it")
    #cv2.imshow("Frame", red_mask)
   # cv2.imshow("Frame", frame)

def Navigation(r):
    
    global Navigation_status
    global counter
    counter=0
    global x_medium

    if r=="UCA":
        UpdateString[0]=1
        p_uc1()
    if r=="UCB":
        UpdateString[0]=2
        p_uc2()
    elif r=="UCC":
        UpdateString[0]=3
        p_uc1()
    elif r=="UCD":
        UpdateString[0]=3
        p_uc1()
    elif r=="V":
        just_walk_updated(1)

    Navigation_status=False
    while(Navigation_status==False):
        #print("into MAIN navigation program")
        _, frame = Front_camera.read()
	#print(frame.shape[0])
        #print(" Front camera read complete")
        frame=frame[200:300,0:640]
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
        # red color
        low_red = np.array([25, 100, 120])   ##100, 130
        high_red = np.array([30, 255, 255])
        red_mask = cv2.inRange(hsv_frame, low_red, high_red)
        _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
	#print("marker segregation")
        if len(contours)==0:
            print(" Not able to see the marker ")
            UpdateString[4] = 1
            #RGB(1,1,1)
            pi_pwm1.ChangeDutyCycle(0)
            pi_pwm2.ChangeDutyCycle(0)
            GPIO.output(31, 0)
            GPIO.output(32, 0)
            #GPIO.output(GPIO_BUZZER_OUTPUT, True)
        else:
            #print("len(contours)=>0")
            GPIO.output(GPIO_BUZZER_OUTPUT, False)
            GPIO.output(31, 1)
            GPIO.output(32, 1)

            RGB(0,0,0)
            #print("II")
            #GPIO.output(GPIO_BUZZER_OUTPUT, False)

            for cnt in contours:
                (x, y, w, h) = cv2.boundingRect(cnt)

                x_medium = int(( x + (w / 2)))
                if(x_medium>500):
                    x_medium=500
                elif (x_medium<=20):
                    x_medium=20
                break

            if (x_medium<frame.shape[1]/2):


                motor1(0)
                motor2(0)
                correction=map_imu( x_medium ,    frame.shape[1]/2-130,    frame.shape[1]/2,  max_correction, 0)
                #print("first: ","x_medium: ",x_medium)
                #print("  correction ", correction)
                final_speed_for_motor1=base_speed-correction
                final_speed_for_motor2=base_speed

                if(final_speed_for_motor1>100):
                    final_speed_for_motor1=100
                elif(final_speed_for_motor1<0):
                    final_speed_for_motor1=0


                if(final_speed_for_motor2>100):
                    final_speed_for_motor2=100
                elif(final_speed_for_motor2<0):
                    final_speed_for_motor2=0

                pi_pwm1.ChangeDutyCycle(final_speed_for_motor1)
                pi_pwm2.ChangeDutyCycle(final_speed_for_motor2)

            elif (x_medium>=frame.shape[1]/2):
                motor1(0)
                motor2(0)

                correction=map_imu( x_medium ,  frame.shape[1]/2+130,    frame.shape[1]/2, max_correction,0)

                #print("second: ","x_medium: ",x_medium)
                #print("  correction ", correction)
                final_speed_for_motor1=base_speed
                final_speed_for_motor2=base_speed-correction

                if(final_speed_for_motor1>100):
                    final_speed_for_motor1=100
                elif(final_speed_for_motor1<0):
                    final_speed_for_motor1=0


                if(final_speed_for_motor2>100):
                    final_speed_for_motor2=100
                elif(final_speed_for_motor2<0):
                    final_speed_for_motor2=0

                pi_pwm1.ChangeDutyCycle(final_speed_for_motor1)
                pi_pwm2.ChangeDutyCycle(final_speed_for_motor2)
            #print " marker: ", str(x_medium)+" Motor1: "+ str(final_speed_for_motor1)+" Motor2: "+str(final_speed_for_motor2)+" Correction: "+str(correction)
            marker_count(r)
    print(" UC has completed")

#################################################################################
def UpdateString_function():
    global UpdateString
    return UpdateString
def turn_left(t):
    print("turning_left for "+str(t)+" seconds")
    motor1(1)
    motor2(0)
    pi_pwm1.ChangeDutyCycle(30)
    pi_pwm2.ChangeDutyCycle(30)
    time.sleep(t)
    pi_pwm1.ChangeDutyCycle(0)
    pi_pwm2.ChangeDutyCycle(0)

def turn_right(t):
    print("turning_right for "+str(t)+" seconds")
    motor1(0)
    motor2(1)
    pi_pwm1.ChangeDutyCycle(30)
    pi_pwm2.ChangeDutyCycle(30)
    time.sleep(t)
    pi_pwm1.ChangeDutyCycle(0)
    pi_pwm2.ChangeDutyCycle(0)
    
def turn_right_updated(t):
    print("turning_right for "+str(t)+" seconds")
    motor1(0)
    motor2(1)
    for i in range(0,30):  
        pi_pwm1.ChangeDutyCycle(i)
        pi_pwm2.ChangeDutyCycle(i*1.14)
        time.sleep(0.04)
    
    pi_pwm1.ChangeDutyCycle(30)
    pi_pwm2.ChangeDutyCycle(30)
    time.sleep(t)
    for i in range(30,0,-1):  
        pi_pwm1.ChangeDutyCycle(i)
        pi_pwm2.ChangeDutyCycle(i*1.14)
        time.sleep(0.04)
    
def turn_left_updated(t):
    motor1(1)
    motor2(0)
    for i in range(0,30):  
        pi_pwm1.ChangeDutyCycle(i)
        pi_pwm2.ChangeDutyCycle(i*1.14)
        time.sleep(0.04)
    
    pi_pwm1.ChangeDutyCycle(30)
    pi_pwm2.ChangeDutyCycle(30)
    time.sleep(t)
    for i in range(30,0,-1):  
        pi_pwm1.ChangeDutyCycle(i)
        pi_pwm2.ChangeDutyCycle(i*1.14)
        time.sleep(0.04)
        
def turn_around(t):
    print("turning_around for "+str(t)+ " seconds")
    motor1(0)
    motor2(1)
    pi_pwm1.ChangeDutyCycle(30)
    pi_pwm2.ChangeDutyCycle(30)
    time.sleep(t)
    pi_pwm1.ChangeDutyCycle(0)
    pi_pwm2.ChangeDutyCycle(0)
    
def turn_around_updated(t):
    print("turning_around for "+str(t)+ " seconds")
    motor1(0)
    motor2(1)
    for i in range(0,30):  
        pi_pwm1.ChangeDutyCycle(i)
        pi_pwm2.ChangeDutyCycle(i*1.14)
        time.sleep(0.04)
    pi_pwm1.ChangeDutyCycle(30)
    pi_pwm2.ChangeDutyCycle(30)
    time.sleep(t)
    for i in range(30,0,-1):  
        pi_pwm1.ChangeDutyCycle(i)
        pi_pwm2.ChangeDutyCycle(i*1.14)
        time.sleep(0.04)
    


def Front(t):
    print("walking_front for "+str(t)+" seconds")
    motor1(0)
    motor2(0)
    pi_pwm1.ChangeDutyCycle(30)
    pi_pwm2.ChangeDutyCycle(30)
    time.sleep(t)
    pi_pwm1.ChangeDutyCycle(0)
    pi_pwm2.ChangeDutyCycle(0)

def map_imu(imu_ang, in_min, in_max, out_min, out_max):
    correction=(imu_ang - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return int(correction)

def walk_stop():
    print("Robot stopped")
    pi_pwm1.ChangeDutyCycle(0)
    pi_pwm2.ChangeDutyCycle(0)
    time.sleep(1)

def walk_stop_em():
    global Navigation_status
    
##    Down_camera.release()
##    Front_camera.release()
    print("Emergency stopped")
    Navigation_status=True
    pi_pwm1.ChangeDutyCycle(0)
    pi_pwm2.ChangeDutyCycle(0)
    time.sleep(1)

def just_walk(t):
    motor1(0)
    motor2(0)
    print("Just walking for "+str(t)+" Seconds")
    pi_pwm1.ChangeDutyCycle(50)
    pi_pwm2.ChangeDutyCycle(57.5)
    time.sleep(t)
    
def walk_stop_updated():
    motor1(0)
    motor2(0)
    print("Robot stopped")
    for i in range(50,0,-1):
        pi_pwm1.ChangeDutyCycle(i)
        pi_pwm2.ChangeDutyCycle(i*1.14)
        time.sleep(0.04)
    time.sleep(1)
def walk_for_thread(t):
    motor1(0)
    motor2(0)
    print("Just walking for "+str(t)+" Seconds")
    for i in range(0,50):
        pi_pwm1.ChangeDutyCycle(i)
        pi_pwm2.ChangeDutyCycle(i*1.14)
        time.sleep(0.04)
    pi_pwm1.ChangeDutyCycle(50)
    pi_pwm2.ChangeDutyCycle(57)
    time.sleep(t)
    for i in range(50,0,-1):
        pi_pwm1.ChangeDutyCycle(i)
        pi_pwm2.ChangeDutyCycle(i*1.14)
        time.sleep(0.04)

def walk_stop_for_threading():
    motor1(0)
    motor2(0)
    Navigation_status=True
    print("Robot stopped")
    walk_stop_updated()
##    pi_pwm1.ChangeDutyCycle(0)
##    pi_pwm2.ChangeDutyCycle(0)
    time.sleep(5)
    
def just_walk_updated(t):
    motor1(0)
    motor2(0)
    print("Just walking for "+str(t)+" Seconds")
    for i in range(0,50):
        pi_pwm1.ChangeDutyCycle(i)
        pi_pwm2.ChangeDutyCycle(i*1.14)
        time.sleep(0.04)
    pi_pwm1.ChangeDutyCycle(54)
    pi_pwm2.ChangeDutyCycle(56)
    time.sleep(t)
    
def walk_back(t):
    motor1(1)
    motor2(1)
    print("Just walking for "+str(t)+" Seconds")
    for i in range(0,50):
        pi_pwm1.ChangeDutyCycle(i*1.14)
        pi_pwm2.ChangeDutyCycle(i)
        time.sleep(0.04)
    pi_pwm1.ChangeDutyCycle(57)
    pi_pwm2.ChangeDutyCycle(50)
    time.sleep(t)
    for i in range(50,0,-1):
        pi_pwm1.ChangeDutyCycle(i*1.14)
        pi_pwm2.ChangeDutyCycle(i)
        time.sleep(0.04)

def walk_back_updated(t):
    motor1(1)
    motor2(1)
    print("Just walking for "+str(t)+" Seconds")
    pi_pwm1.ChangeDutyCycle(56)
    pi_pwm2.ChangeDutyCycle(54)
    time.sleep(t)

def UCB_Inventory_Count():
    object_count()

def p_uc1():
    UpdateString[1]= 1
    just_walk_updated(0.4)
    walk_stop_updated()
    turn_left_updated(1.3)
    #walk_stop_updated()
    #just_walk(12)
    just_walk_updated(7.5)
    walk_stop_updated()
    turn_right_updated(1.5)
    just_walk_updated(0.2)
    #walk_stop_updated(
    UpdateString[1]= 2
    #turn_right(1.1)


def uc1_p_end():
    #just_walk_updated(1)
##    turn_left_updated(1.7)
##    just_walk_updated(8)
##    walk_stop_updated()
##    turn_left_updated(2.1)
##    walk_back(5.8)
    
    turn_left_updated(1.7)
    just_walk_updated(8)
    walk_stop_updated()
    turn_left_updated(2.1)
    walk_back(5.8)
    
def p_uc2():
    just_walk_updated(0.4)
    walk_stop_updated()
    turn_left_updated(1.125)
    just_walk_updated(7.4)

def p_uc22():
    UpdateString[1]= 1
    just_walk_updated(0.15)
    walk_stop_updated()
    turn_left_updated(0.7)
    #walk_stop_updated()
    #just_walk(12)
    just_walk_updated(6)
    #turn_left_updated(0.5)
##    just_walk_updated(4)
##    walk_stop_updated()
##    turn_left_updated(1.1)
##    just_walk_updated(4.5)
    
    UpdateString[1]= 2

def uc2_p_end():
    just_walk_updated(0.8)
    turn_right_updated(2)
    just_walk_updated(3)
    turn_around_updated(5)


def motor_calibration():
    print("Checking both motors at 100% Speed in forward direction")
    motor1(0)
    motor2(0)
    pi_pwm1.start(100)
    pi_pwm2.start(100)
    #time.sleep(5);
def route(r):
    global Front_camera
    global Down_camera
    global UpdateString
    global counter
    global value
    print("Entering Route")
    
    if(r=="V"):
        if (counter==1):
            walk_stop_updated()
            
            turn_left_updated(3)
            
            just_walk_updated(1)
            
        elif(counter==2):
            walk_stop_updated()
            turn_right_updated(2)
            walk_stop_em()
            GPIO.output(31, 0)
            GPIO.output(32, 1)
            time.sleep(5)
            GPIO.output(31, 1)
            GPIO.output(32, 1)
    
    elif(r=="U"):
        UpdateString[0]=1
        if (counter==1):
            #pass
            sys.exit()
##            UpdateString[1]=3
##            walk_stop()
##	    print("before release")
## 	    Down_camera.release()
##	    Front_camera.release()
##            print("after release")
##            #player=OMXPlayer(path+"equipment_unmanned.mp3")
##            face_and_Helmet_detect()
##            
##            #SpectrumAnalyzer()
##            
##            Front_camera = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.3:1.0-video-index0')
##            _, Front_frame= Front_camera.read()
##            if(Front_frame==None):
##                print("Front camera issue")
##                sys.exit("exiting due to cameraaaaa")
##                
##            Down_camera =  cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.1.2:1.0-video-index0')
##            _, Down_frame = Down_camera.read()
##            if(Down_frame==None):
##                print("Down camera issue")
##                sys.exit("exiting due to camerrraaaaaaaaaaaaaaa")
##                
##            
##                
##            just_walk(1)
                
        elif (counter==2):
            UpdateString[1]=3
            walk_stop_updated()
            Down_camera.release()
	    Front_camera.release()
            spec = SpectrumAnalyzer()
            Front_camera = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.3:1.0-video-index0')
            _, Front_frame= Front_camera.read()
            if(Front_frame==None):
                print("Front camera issue")
                sys.exit("exiting due to cameraaaaa")
                
            Down_camera =  cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.1.2:1.0-video-index0')
            _, Down_frame = Down_camera.read()
            if(Down_frame==None):
                print("Down camera issue")
                sys.exit("exiting due to camerrraaaaaaaaaaaaaaa")
            just_walk(1)
            
        elif (counter==3):
            UpdateString[1]=3
            walk_stop_updated()
            Down_camera.release()
	    Front_camera.release()
            print("starting Invetory")
            UCB_Inventory_Count()
            Front_camera = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.3:1.0-video-index0')
            _, Front_frame= Front_camera.read()
            if(Front_frame==None):
                print("Front camera issue")
                sys.exit("exiting due to cameraaaaa")
                
            Down_camera =  cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.1.2:1.0-video-index0')
            _, Down_frame = Down_camera.read()
            if(Down_frame==None):
                print("Down camera issue")
                sys.exit("exiting due to camerrraaaaaaaaaaaaaaa")
            just_walk(1)
            turn_around_updated(5.5)
            walk_stop_em()
            
    elif(r=="UCA"):
        UpdateString[0]=1
        if (counter==1):
            just_walk(2.5)
            #pass
            #just_walk_updated(1)
            
        elif(counter==2):
            UpdateString[1]=3
            walk_stop_updated()
	    print("before release")
 	    Down_camera.release()
	    Front_camera.release()
            print("after release")
            face_and_Helmet_detect()
            Front_camera = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.3:1.0-video-index0')
            _, Front_frame= Front_camera.read()
            if(Front_frame==None):
                print("Front camera issue")
                sys.exit("exiting due to front camera")
                
            Down_camera =  cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.1.2:1.0-video-index0')
            _, Down_frame = Down_camera.read()
            if(Down_frame==None):
                print("Down camera issue")
                sys.exit("exiting due to down camera")
            turn_around_updated(4.3)
            UpdateString[1]=4
            just_walk_updated(2)

        elif (counter==3):
            UpdateString[1]=5
            walk_stop_updated()
            #just_walk_updated(1)
            turn_left_updated(1.2)
            just_walk_updated(0.2)
        elif (counter==4):
            walk_stop_updated()
            #uc2_p_end()
##        elif (counter==4):
##            turn_left(4.2)
##            walk_back_updated(5)
##            walk_stop_updated()
            #walk_stop_updated()
            just_walk_updated(0.3)
            walk_stop_updated()
            turn_left_updated(2.4)
            walk_back_updated(5.3)
            walk_stop_em()

    elif(r=="UCB"):
        UpdateString[0]=2
        
##        if(counter==1):
##            pass
##            time.sleep(1)
        
        if (counter==1):
            UpdateString[1]=3
            walk_stop_updated()
            Down_camera.release()
	    Front_camera.release()
	    UCB_Inventory_Count()
            #SpectrumAnalyzer()
            Front_camera = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.3:1.0-video-index0')
            _, Front_frame= Front_camera.read()
            if(Front_frame==None):
                print("Front camera issue")
                sys.exit("exiting due to cameraaaaa")
                
            Down_camera =  cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.1.2:1.0-video-index0')
            _, Down_frame = Down_camera.read()
            if(Down_frame==None):
                print("Down camera issue")
                sys.exit("exiting due to camerrraaaaaaaaaaaaaaa")
            turn_around_updated(4.5)
            UpdateString[1]=4
            time.sleep(5)
            turn_left_updated(2.1)
            #just_walk_updated(2)
            
        elif(counter==31):
##            walk_stop_updated()
##            just_walk_updated(0.5)
##            walk_stop_updated()
            for i in range(50,0,-1):
                pi_pwm1.ChangeDutyCycle(i)
                pi_pwm2.ChangeDutyCycle(i*1.14)
                time.sleep(0.15)
            time.sleep(1)
            Down_camera.release()
	    Front_camera.release()
            print("after release")
            value=face_and_Helmet_detect()
            
            Front_camera = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.3:1.0-video-index0')
            _, Front_frame= Front_camera.read()
            if(Front_frame==None):
                print("Front camera issue")
                sys.exit("exiting due to front camera")
                
            Down_camera =  cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.1.2:1.0-video-index0')
            _, Down_frame = Down_camera.read()
            if(Down_frame==None):
                print("Down camera issue")
                sys.exit("exiting due to down camera")
            turn_left_updated(2.1)
	    #just_walk_updated(1)
	    
	elif(counter==2):
            walk_stop_updated()
            turn_right_updated(2)
            just_walk_updated(1)
            
        elif(counter==3):
            walk_stop_updated()
            just_walk_updated(0.5)
            walk_stop_updated()
            turn_right_updated(1.9)
            just_walk_updated(1)
            
        elif(counter==4):
            UpdateString[1]=5
            walk_stop_updated()
            #just_walk_updated(1)
            turn_left_updated(1.2)
            just_walk_updated(0.2)
            
##            just_walk(1)
##            turn_left_updated(1.2)
##            just_walk_updated(0.5)
            
            
            

        elif (counter==5):
            walk_stop_updated()
            #uc2_p_end()
##        elif (counter==4):
##            turn_left(4.2)
##            walk_back_updated(5)
##            walk_stop_updated()
            #walk_stop_updated()
            just_walk_updated(0.3)
            walk_stop_updated()
            turn_left_updated(2.4)
            walk_back_updated(5.3)
            
            walk_stop_em()
##            UpdateString[1]=5
##            walk_stop_updated()
##            just_walk_updated(0.7)
##            turn_left_updated(2.8)
##            walk_back_updated(6.5)
##            walk_stop_em()

    elif(r=="UCC"):
        UpdateString[0]=3
        
        if(counter==1):
            just_walk(1.5)

        elif (counter==2):
            UpdateString[1]=3
            walk_stop_updated()
            Down_camera.release()
	    Front_camera.release()
            print("Valve frequency")
            time.sleep(3)
            SpectrumAnalyzer()
            time.sleep(5)
            Front_camera = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.3:1.0-video-index0')
            _, Front_frame= Front_camera.read()
            if(Front_frame==None):
                print("Front camera issue")
                sys.exit("exiting due to cameraaaaa")
                
            Down_camera =  cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.1.2:1.0-video-index0')
            _, Down_frame = Down_camera.read()
            if(Down_frame==None):
                print("Down camera issue")
                sys.exit("exiting due to camerrraaaaaaaaaaaaaaa")
            turn_around_updated(4.5)
            UpdateString[1]=4
            #turn_right(4)
            just_walk(2)

        elif (counter==3):
            UpdateString[1]=5
            walk_stop_updated()
            #just_walk_updated(1)
            turn_left_updated(1.2)
            just_walk_updated(0.2)
            
        elif (counter==4):
            walk_stop_updated()
            #uc2_p_end()
##        elif (counter==4):
##            turn_left(4.2)
##            walk_back_updated(5)
##            walk_stop_updated()
            #walk_stop_updated()
            just_walk_updated(0.1)
            walk_stop_updated()
            turn_left_updated(2.4)
            walk_back_updated(5.3)
            walk_stop_em()
            
        
            
    elif(r=="UCD"):
        UpdateString[0]=3
        
        if(counter==1):
            just_walk(1.5)
            
        elif (counter==2):
            turn_left_updated(1.1)
            just_walk_updated(2)

        elif (counter==3):
            UpdateString[1]=3
            walk_stop_updated()
            Down_camera.release()
	    Front_camera.release()
            print("starting Invetory")
            #SpectrumAnalyzer()
            Front_camera = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.3:1.0-video-index0')
            _, Front_frame= Front_camera.read()
            if(Front_frame==None):
                print("Front camera issue")
                sys.exit("exiting due to cameraaaaa")
                
            Down_camera =  cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.1.2:1.0-video-index0')
            _, Down_frame = Down_camera.read()
            if(Down_frame==None):
                print("Down camera issue")
                sys.exit("exiting due to camerrraaaaaaaaaaaaaaa")
            turn_around_updated(4.5)
            UpdateString[1]=4
            #turn_right(4)
            just_walk(2)

        elif (counter==4):
            turn_right(1.1)
            just_walk_updated(2)
            
        elif(counter==5):
            
            walk_stop_updated()
            UpdateString[1]=5
            uc1_p_end()
            walk_stop_em()

        

def marker_count(r):
    global counter
    #global Route
    camera()
    while(times==1):
        print("Mark detected")

        camera()
        if(times==0):
            counter =counter+1
            print("Marker number, ",counter," found !!")
            route(r)


#just_walk_updated(5)
#p_uc1()
##################################################################### MAIN CODE
Front_camera = cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.3:1.0-video-index0')
_, Front_frame= Front_camera.read()
if(Front_frame==None):
    print("Front camera issue")
    sys.exit("exiting due to cameraaaaa")
    
Down_camera =  cv2.VideoCapture('/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.1.2:1.0-video-index0')
_, Down_frame = Down_camera.read()
if(Down_frame==None):
    print("Down camera issue")
    sys.exit("exiting due to camerrraaaaaaaaaaaaaaa")



x_medium = 320
print("Camera Initialised")


#object_count()


#face_and_Helmet_detect()
#SpectrumAnalyzer()
#face_and_Helmet_detect()
#p_uc2()
#Navigation("UCA")
##object_count()
#walk_back(6)
#uc1_p_end()
#UCB_Inventory_Count()

#turn_around_updated(15)
    
        
##
