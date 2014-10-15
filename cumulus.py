#!/usr/bin/env python3

import time
import subprocess
import urllib2
import os
import glob
import random
import re
import pifacedigitalio
import pygame
import pyaudio
import numpy
import audioop
import sys
import math
import struct

### Cumulus Semi-Smart Cloud ###
### Nick Bartley 2014 ###
			
class Cloud(object):
	def __init__(self, PIFACE):
			
		self.PIFACE = PIFACE		
		self.randomSound = 1
		self.delayTime = 201
		self.flash = 31
		self.randomChoose = 1
		self.flashTime = 1
		self.sporaticCounter = 0
		self.strikeCounter = 0

	#This is the main cloud loop		
	def run(self):
		while True:
			if self.PIFACE.input_pins[0].value == 0:
				time.sleep(3)
				sensor1 = 0
				sensor2 = 0
				sensor1 = self.PIFACE.input_pins[4].value
				sensor2 = self.PIFACE.input_pins[5].value
				if sensor1 == 0 or sensor2 == 0:
					self.strikes()
					self.storm()
					time.sleep(random.randint(3,10))
			else:
				self.soundTOlight()
	
	#This runs a set of strikes			
	def strikes(self):
		self.strikeCounter = 0
		while self.strikeCounter < random.randint(5,25):
			self.sporaticCounter = 0
			self.delayTime = random.randint(30,5000)/1000
			self.flash = random.randint(1,3)
			self.flashTime = random.randint(10,50)/1000
			self.randomChoose = random.randint(1,6)
			while self.flash > self.sporaticCounter:
				print("flash")
				self.PIFACE.output_pins[self.randomChoose].turn_on()
				time.sleep(self.flashTime)
				self.PIFACE.output_pins[self.randomChoose].turn_off()
				time.sleep(self.flashTime)
				self.sporaticCounter += 1
			time.sleep(self.delayTime)
			self.strikeCounter += 1				
	
	#This runs a storm
	def storm(self):
		#FIRST FLASH
		self.PIFACE.output_pins[1].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[2].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[3].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[4].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)			
		self.PIFACE.output_pins[5].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[6].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[3].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[1].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[2].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[5].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[6].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[4].turn_off()
		#SECOND FLASH
		self.PIFACE.output_pins[5].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[2].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[1].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[2].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[5].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[1].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		#THIRD FLASH
		self.PIFACE.output_pins[4].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[6].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[3].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[6].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[4].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[3].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		#THUNDER CLAP
		self.thunder()
		time.sleep(2)
		#FORTH FLASH
		self.PIFACE.output_pins[6].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[3].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[2].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)			
		self.PIFACE.output_pins[5].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[3].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[2].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[6].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[5].turn_off()
		time.sleep(1)
		#FIFTH FLASH
		self.PIFACE.output_pins[4].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[6].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[3].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[1].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)			
		self.PIFACE.output_pins[2].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[5].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[6].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[3].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[2].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[5].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[1].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[4].turn_off()
		#SIXTH FLASH
		self.PIFACE.output_pins[2].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[4].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[3].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[1].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)			
		self.PIFACE.output_pins[5].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[6].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[4].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[1].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[3].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[2].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[6].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[5].turn_off()
	
	def thunder(self):
		silence = self.PIFACE.input_pins[3].value
		self.randomSound = random.randint(1,4)
		pygame.mixer.init()
		if silence == 0:
			effect = pygame.mixer.Sound("/home/pi/cumulus/thunder/"+str(self.randomSound)+".wav")
			effect.play()

	def soundTOlight(self):
		chunk      = 2**11 # Change if too fast/slow, never less than 2**11
		scale      = 50    # Change if too dim/bright
		exponent   = 5     # Change if too little/too much difference between loud and quiet sounds
		samplerate = 44100
		device   = 2  
    
		p = pyaudio.PyAudio()
		stream = p.open(format = pyaudio.paInt16,
			channels = 1,
			rate = 44100,
			input = True,
			frames_per_buffer = chunk,
			input_device_index = device)
			
		while self.PIFACE.input_pins[0].value == 1:
			data  = stream.read(chunk)
			
			# Do FFT
            levels = calculate_levels(data, chunk, samplerate)
 
            # Make it look better and send to serial
			led = 0
            for level in levels:
                level = max(min(level / scale, 1.0), 0.0)
                level = level**exponent 
                level = int(level * 255)
				if level > 100:
					self.PIFACE.output_pins[led].turn_on()
				if level < 100:
					self.PIFACE.output_pins[led].turn_off()
				led += 1
		stream.close()
        p.terminate()
				
	def calculate_levels(data, chunk, samplerate):
		# Use FFT to calculate volume for each frequency
		global MAX = 0
	 
		# Convert raw sound data to Numpy array
		fmt = "%dH"%(len(data)/2)
		data2 = struct.unpack(fmt, data)
		data2 = numpy.array(data2, dtype='h')
	 
		# Apply FFT
		fourier = numpy.fft.fft(data2)
		ffty = numpy.abs(fourier[0:len(fourier)/2])/1000
		ffty1=ffty[:len(ffty)/2]
		ffty2=ffty[len(ffty)/2::]+2
		ffty2=ffty2[::-1]
		ffty=ffty1+ffty2
		ffty=numpy.log(ffty)-2
		
		fourier = list(ffty)[4:-4]
		fourier = fourier[:len(fourier)/2]
		
		size = len(fourier)
	 
		# Add up for 6 lights
		levels = [sum(fourier[i:(i+size/6)]) for i in xrange(0, size, size/6)][:6]
		
		return levels

if __name__ == "__main__":
	
	pfd = pifacedigitalio.PiFaceDigital()
	global cloud
	cloud = Cloud(pfd)
	cloud.run();