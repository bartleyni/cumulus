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
import alsaaudio as aa
import numpy as np
from struct import unpack
import audioop

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
		firstRun = 1
		while True:
			pygame.mixer.init()
			if self.PIFACE.input_pins[0].value == 1 or firstRun == 1:
				
				self.alloff()
				time.sleep(1)
				sensor1 = 0
				sensor2 = 0
				sensor1 = self.PIFACE.input_pins[4].value
				sensor2 = self.PIFACE.input_pins[5].value
				if sensor1 == 0 or sensor2 == 0 or firstRun == 1:
					firstRun = 0
					#subprocess.check_output("sudo pulseaudio -k", shell=False).decode('utf-8')
					#self.BTVolSet(30000)
					self.strikes()
					#self.BTVolSet(10000)
					self.storm()
					time.sleep(random.randint(3,10))
					#self.BTVolSet(65500)
			else:
				#self.soundTOlight()
				#self.list_devices()
				self.audio_playback()
				time.sleep(1)
	
	def alloff(self):
		for i in range (0,8):
			self.PIFACE.output_pins[i].turn_off()
	
	def BTVolSet(self, volume):
		return subprocess.call("pacmd set-sink-volume 1 "+str(volume), shell=True)
	
	#This runs a set of strikes	
	def strikes(self):
		self.strikeCounter = 0
		while self.strikeCounter < random.randint(5,25):
			self.sporaticCounter = 0
			self.delayTime = random.randint(30,5000)/1000
			self.flash = random.randint(1,3)
			self.flashTime = random.randint(10,50)/1000
			self.randomChoose = random.randint(1,8)
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
		self.PIFACE.output_pins[8].turn_on()
		time.sleep(random.randrange(5,50,5)/1000)
		self.PIFACE.output_pins[7].turn_on()
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
		self.PIFACE.output_pins[7].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[8].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		#THUNDER CLAP
		self.thunder()
		time.sleep(2)
		#FORTH FLASH
		self.PIFACE.output_pins[6].turn_on()
		time.sleep(random.randrange(5,80,5)/1000)
		self.PIFACE.output_pins[8].turn_on()
		time.sleep(random.randrange(5,80,5)/1000)
		self.PIFACE.output_pins[3].turn_on()
		time.sleep(random.randrange(5,80,5)/1000)
		self.PIFACE.output_pins[2].turn_on()
		time.sleep(random.randrange(5,80,5)/1000)			
		self.PIFACE.output_pins[5].turn_on()
		time.sleep(random.randrange(5,80,5)/1000)
		self.PIFACE.output_pins[7].turn_on()
		time.sleep(random.randrange(5,80,5)/1000)
		self.PIFACE.output_pins[3].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[2].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[7].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[8].turn_off()
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
		time.sleep(random.randrange(5,80,5)/1000)
		self.PIFACE.output_pins[8].turn_on()
		time.sleep(random.randrange(5,80,5)/1000)
		self.PIFACE.output_pins[4].turn_on()
		time.sleep(random.randrange(5,80,5)/1000)
		self.PIFACE.output_pins[3].turn_on()
		time.sleep(random.randrange(5,80,5)/1000)
		self.PIFACE.output_pins[1].turn_on()
		time.sleep(random.randrange(5,80,5)/1000)			
		self.PIFACE.output_pins[5].turn_on()
		time.sleep(random.randrange(5,80,5)/1000)
		self.PIFACE.output_pins[7].turn_on()
		time.sleep(random.randrange(5,80,5)/1000)
		self.PIFACE.output_pins[6].turn_on()
		time.sleep(random.randrange(5,80,5)/1000)
		self.PIFACE.output_pins[4].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[1].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[3].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[7].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[8].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[2].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[6].turn_off()
		time.sleep(random.randrange(20,100,10)/1000)
		self.PIFACE.output_pins[5].turn_off()
	
	def thunder(self):
		silence = self.PIFACE.input_pins[3].value
		self.randomSound = random.randint(1,4)
		#pygame.mixer.init()
		if silence == 0:
			effect = pygame.mixer.Sound("/home/pi/cumulus/thunder/"+str(self.randomSound)+".wav")
			effect.play()
		#pygame.mixer.quit()

	def audio_playback(self):
		# Set up audio
		sample_rate = 44100
		no_channels = 1
		chunk = 512 # Use a multiple of 8
		#data_in = aa.PCM(aa.PCM_CAPTURE, aa.PCM_ASYNC)
		data_in = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL)
		data_in.setchannels(no_channels)
		data_in.setrate(sample_rate)
		data_in.setformat(aa.PCM_FORMAT_S16_LE)
		data_in.setperiodsize(chunk)
		
		while self.PIFACE.input_pins[0].value == 0:
			# Read data from device   
			l,data = data_in.read()
			data_in.pause(1) # Pause capture whilst RPi processes data
			if l:
				# catch frame error
				try:
					matrix=self.calculate_levels(data, chunk, sample_rate)
					for i in range (0,8):
						#Set_Column((1<<matrix[i])-1,0xFF^(1<<i))
						self.Set_Led((1<<matrix[i])-1,i)								

				except audioop.error, e:
					if e.message !="not a whole number of frames":
						raise e
			time.sleep(0.001)
			data_in.pause(0) # Resume capture
			
	def calculate_levels(self, data, chunk, sample_rate):
	   
		matrix    = [0,0,0,0,0,0,0,0]
		power     = []
		weighting = [2,4,8,8,16,32,64,128] # Change these according to taste
		
		# Convert raw data to numpy array
		data = unpack("%dh"%(len(data)/2),data)
		data = np.array(data, dtype='h')
		# Apply FFT - real data so rfft used
		fourier=np.fft.rfft(data)
		# Remove last element in array to make it the same size as chunk
		fourier=np.delete(fourier,len(fourier)-1)
		# Find amplitude
		#power = np.log10(np.abs(fourier))**2
		# Find average 'amplitude' for specific frequency ranges in Hz
		power = np.abs(fourier)   
		matrix[0]= int(np.mean(power[self.piff(0)    :self.piff(156):1]))
		matrix[1]= int(np.mean(power[self.piff(156)  :self.piff(313):1]))
		matrix[2]= int(np.mean(power[self.piff(313)  :self.piff(625):1]))
		matrix[3]= int(np.mean(power[self.piff(625)  :self.piff(1250):1]))
		matrix[4]= int(np.mean(power[self.piff(1250) :self.piff(2500):1]))
		matrix[5]= int(np.mean(power[self.piff(2500) :self.piff(5000):1]))
		matrix[6]= int(np.mean(power[self.piff(5000) :self.piff(10000):1]))
		matrix[7]= int(np.mean(power[self.piff(10000):self.piff(20000):1]))
		# Tidy up column values for the LED matrix
		matrix=np.divide(np.multiply(matrix,weighting),1000000)
		# Set floor at 0 and ceiling at 8 for LED matrix
		matrix=matrix.clip(0,8) 	   
		#print(matrix)
		# Araange array into 6 rows for the 6 LEDs
		#power = np.reshape(power,(6,chunk/6))
		#matrix= np.int_(np.average(power,axis=1)/4)
		return matrix

	def Set_Led(self, col, row):
		if col > 0xC8:
			self.PIFACE.output_pins[row].turn_on()
		else:
			self.PIFACE.output_pins[row].turn_off()

	# Return power array index corresponding to a particular frequency
	def piff(self, val):
		return int(2*512*val/44100)
		
if __name__ == "__main__":
	
	pfd = pifacedigitalio.PiFaceDigital()
	global cloud
	cloud = Cloud(pfd)
	cloud.run();