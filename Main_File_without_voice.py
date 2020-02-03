#! /usr/bin/env python
import socket
import threading
import sys
from navigation_merge import *
from omxplayer.player import OMXPlayer

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(31,GPIO.OUT)
GPIO.setup(32,GPIO.OUT)

##player=OMXPlayer("The hammer is missing from the inventory.mp3")
##player.set_volume(4)
##GPIO.output(31, 1)
##GPIO.output(32, 1)
##
##time.sleep(3)
##GPIO.output(31, 0)
##GPIO.output(32, 0)


s = socket.socket()
print "Socket successfully created"
path ="/home/pi/Desktop/ACCENTURE_USE_CASES/"
port = 53

def Serial_over_WIFI():
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('192.168.0.10', port))
    print "socket binded to %s" %(port)
    s.listen(1)
    print "socket is listening"
    player=OMXPlayer(path+"I am ready.mp3")
    player.set_volume(1)
    time.sleep(2)
    Connection_Status=False
    c, addr = s.accept()
    print 'Got connection from', addr
    c.send('Thank you for connecting\n')
    player=OMXPlayer(path+"I am connected to the application.mp3")
    player.set_volume(1)
    time.sleep(3)
    #player.play()
##    GPIO.output(31, 0)
##    GPIO.output(32, 1)
##    RGB(0,0,0)

    while True:
        
        
        recv_data=(c.recv(64))

        #print('\x1b[6;30;42m'+ "Recieved data from Device: " +str(recv_data) +'\x1b[0m')
        print("Recieved data from Device: " +str(recv_data))
        if not recv_data:
            print("Disconnected with device")
            player=OMXPlayer(path+"I am disconnected from the application.mp3")
            player.set_volume(1)
            #player.play()
            time.sleep(3)
##            GPIO.output(31, 1)
##            GPIO.output(32, 0)
##            RGB(0,0,0)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            c, addr = s.accept()
            print 'Got connection from', addr
            c.send('Thank you for connecting\n')
            player=OMXPlayer(path+"I am connected to the application.mp3")
            player.set_volume(1)
            #player.play()
            time.sleep(3)
##            GPIO.output(31, 0)
##            GPIO.output(32, 1)
            
        if( "Front" in recv_data):
##                work=threading.Thread(target=walk_for_thread,args=(3,))
##                work.start()
            walk_for_thread(2)
            
        elif ("Back" in recv_data):
##                work=threading.Thread(target=turn_around_updated,args=(5,))
##                work.start()
            turn_around_updated(5)
            
        elif ("Left" in recv_data):
##                work=threading.Thread(target=turn_left_updated,args=(2,))
##                work.start()
            turn_right_updated(0.6)
            
        elif ("Right" in recv_data):
##                work=threading.Thread(target=turn_right_updated,args=(2,))
##                work.start()
            turn_left_updated(0.6)
            
        elif ("STOP" in recv_data):
##                work=threading.Thread(target=walk_stop_for_threading)
##                work.start()
            walk_stop_for_threading()
            
        elif("UpdatesPlease" in recv_data):
            update_strings=UpdateString_f()
            c.send(update_strings +"\n")

        elif("UCA" in recv_data):
##                work=threading.Thread(target=Navigation,args=("UCA",))
##                work.start()
##               Navigation("UCA")
            Navigation("UCA")

        elif("UCB" in recv_data):
##                work=threading.Thread(target=Navigation,args=("UCB",))
##                work.start()
           Navigation("UCB")

        elif("UCC" in recv_data):
##                work=threading.Thread(target=Navigation,args=("UCC",))
##                work.start()
           Navigation("UCC")

##        except:
##            sys.exit("systems Exit")
    c.close()

try:
    Serial_comm=threading.Thread(target=Serial_over_WIFI)
    Serial_comm.start()
except:
    sys.exit("system Exit")
