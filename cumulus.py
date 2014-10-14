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
from vlcclient import VLCClient

### Cumulus Semi-Smart Cloud ###
### Nick Bartley 2014 ###

#General Control Variables
SHUTDOWN_CMD = "sudo shutdown now"
REBOOT_CMD = "sudo shutdown -r now"
	
def run_cmd(cmd):
	return subprocess.check_output(cmd, shell=True).decode('utf-8')

def shutdown():
	run_cmd(SHUTDOWN_CMD)

def reboot():
	run_cmd(REBOOT_CMD)
			
class Cloud(object):
	#def __init__(self, PIFACE, VLC):
	def __init__(self, PIFACE):
		
		#self.current_option_index = initial_option
		
		self.PIFACE = PIFACE
		#self.VLC = VLC
		
		self.randomSound = 1
		self.delayTime = 201
		self.flash = 31
		self.randomChoose = 1
		self.flashTime = 1
		self.sporaticCounter = 0
		self.strikeCounter = 0

	#This is the main cloud loop		
	def run(self):
		print("running")
		while True:
			print("In Loop")
			time.sleep(3)
			sensor1 = 0
			sensor2 = 0
			sensor1 = self.PIFACE.input_pins[1].value
			sensor2 = self.PIFACE.input_pins[2].value
			if sensor1 == 0 and sensor2 == 0:
				#DO NOTHING
				print("NO MOTION")
			else:
				self.strikes()
				self.storm()
				print("MOTION")[1]
				time.sleep(3,10)
	
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
		print("storm")
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
	
	def thunder(self):
		silence = self.PIFACE.input_pins[3].value
		self.randomSound = random.randint(1,8)
		pygame.mixer.init()
		if silence == 0:
			#self.VLC.connect()
			#seld.VLC.clear()
			#self.VLC.add("cumulus/thunder/"+self.randomSound+".wav")
			#self.VLC.disconnect()
			effect = pygame.mixer.Sound("thunder/"+str(self.randomSound)+".wav")
			effect.play()
		
if __name__ == "__main__":
	
	#PLAYER_PROCESS = subprocess.Popen(["/usr/bin/vlc", "-I", "dummy", "--volume", "150", "--intf", "telnet", "--lua-config", "telnet={host='0.0.0.0:4212'}"])
	
	pfd = pifacedigitalio.PiFaceDigital()
	
	#vlc = VLCClient("127.0.0.1",4212,"admin",1)
	
	global cloud
	
	#cloud = Cloud(pfd, vlc)
	cloud = Cloud(pfd)
	cloud.run();