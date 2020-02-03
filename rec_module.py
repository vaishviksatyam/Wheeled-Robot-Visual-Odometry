#!/usr/bin/env python
# encoding: utf-8

## Module infomation ###
# Python (3.4.4)
# numpy (1.10.2)
# PyAudio (0.2.9)
# matplotlib (1.5.1)
# All 32bit edition
########################

import numpy as np
import pyaudio
import pygame
import time
from datetime import datetime, timedelta
from omxplayer.player import OMXPlayer
#import matplotlib.pyplot as plt

path ="/home/pi/Desktop/ACCENTURE_USE_CASES/new_audio/"

class SpectrumAnalyzer:
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 16000
    CHUNK =512
    START = 0
    N = 512
    frequency_got=0

    wave_x = 0
    wave_y = 0
    spec_x = 0
    spec_y = 0
    data = []

    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(format = self.FORMAT,
            channels = 1,
            rate = self.RATE,
            input = True,
            output = False,
            frames_per_buffer = self.CHUNK)
        # Main loop
        self.loop()

    def loop(self):
        try:
            end_time = datetime.now() + timedelta(seconds=60)
            while (datetime.now()< end_time) :
                self.data = self.audioinput()
                self.fft()
                if frequency_got==1000 or frequency_got==-1000:
                    #print("got it")

                    player=OMXPlayer(path+"Hi, I have detected noise levels greater than the average value of 70 to 75 db. This is indicative of Cavitation, which could harm the equipment. I have raised an incident.mp3")
                    player.set_volume(1)
                    time.sleep(5)

                    break
                #self.graphplot()
            #self.stream.stop_stream()
            #self.stream.close()

        except KeyboardInterrupt:
            self.pa.close()

        print("End...")

    def audioinput(self):
        ret = self.stream.read(self.CHUNK, exception_on_overflow = False)
        ret = np.fromstring(ret, np.float32)
        return ret

    def fft(self):
        global frequency_got
        self.wave_x = range(self.START, self.START + self.N)
        self.wave_y = self.data[self.START:self.START + self.N]
        self.spec_x = np.fft.fftfreq(self.N, d = 1.0 / self.RATE)

        #print("x ",max(self.spec_x))
        y = np.fft.fft(self.data[self.START:self.START + self.N])


        self.spec_y = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in y]
        max_of_y=self.spec_y.index(max(self.spec_y))
        frequency_got=self.spec_x [max_of_y]
        print("frequency_got: ",frequency_got)
        #print("y ",max(self.spec_y))
##        if (frequency_got>=1500 or frequency_got<=-1500):
##            print("frequency_got ", frequency_got)
##            return frequency_got
        #     time.sleep(10)
        #     pygame.mixer.init()
        #     pygame.mixer.music.load("sin@6000.wav")
        #     pygame.mixer.music.play()
        #     while pygame.mixer.music.get_busy() == True:
        #         continue
        #     print("Audio sent")


        #print("y : ", self.spec_y)

    # def graphplot(self):
    #     plt.clf()
    #     # wave
    #     plt.subplot(311)
    #     plt.plot(self.wave_x, self.wave_y)
    #     plt.axis([self.START, self.START + self.N, -0.5, 0.5])
    #     plt.xlabel("time [sample]")
    #     plt.ylabel("amplitude")
    #     #Spectrum
    #     plt.subplot(312)
    #     plt.plot(self.spec_x, self.spec_y, marker= 'o', linestyle='-')
    #     plt.axis([0, self.RATE / 2, 0, 50])
    #     plt.xlabel("frequency [Hz]")
    #     plt.ylabel("amplitude spectrum")
    #     #Pause
    #     plt.pause(0.05)
if __name__ == "__main__":
    spec = SpectrumAnalyzer()
