#!/usr/bin/env python3

import time
import subprocess
import urllib2
import os
import glob
import threading
import pifacecad
import re
import pifacedigitalio
from vlcclient import VLCClient

### Cumulus Semi-Smart Cloud ###
### Nick Bartley 2014 ###

# GLOBALS

#General Control Variables
GET_TEMP_CMD = "/opt/vc/bin/vcgencmd measure_temp"
TOTAL_MEM_CMD = "free | grep 'Mem' | awk '{print $2}'"
USED_MEM_CMD = "free | grep '\-\/+' | awk '{print $3}'"
SHUTDOWN_CMD = "sudo shutdown now"
REBOOT_CMD = "sudo shutdown -r now"
	
def run_cmd(cmd):
	return subprocess.check_output(cmd, shell=True).decode('utf-8')

def shutdown():
	run_cmd(SHUTDOWN_CMD)

def reboot():
	run_cmd(REBOOT_CMD)
			
class Cloud(object):
	def __init__(self, PIFACE, VLC):
		
		#self.current_option_index = initial_option
		
		self.PIFACE = PIFACE
		self.VLC = VLC
		randomSound = 1;
		chooseWAV = (randomSound);
		delayTime = 201;
		flash = 31;
		randomChoose = 1;
		chooseLED = (randomChoose);
		flashTime = 1;
		self.sporaticCounter = 0;
		self.strikeCounter = 0;

	#This is the main cloud loop		
	def run(self):
		time.sleep(3000)
		sensor1 = 0
		sensor2 = 0
		sensor1 = PIFACE.input_pins[1].value
		sensor2 = PIFACE.input_pins[2].value
		silence = PIFACE.input_pins[3].value
		if sensor1 == 0 and sensor2 == 0:
			#DO NOTHING
		else:
			
		
		

		
		
		
		
		
		

	@property
	def get_menu_mode(self):
		"""Returns the menu mode True or False."""
		return self.menu_mode
		
	@property
	def get_current_option_index(self):
		"""Returns the currentl option."""
		return self.current_option_index
		
	@property
	def current_option(self):
		"""Returns the current mode of operation."""
		return OPTIONS[self.current_option_index]
		
	@property
	def highlighted_option(self):
		"""Returns the highlighted mode of operation."""
		return OPTIONS[self.highlighted_option_index]

	@property
	def get_highlighted_option_index(self):
		"""Returns the currently highlighted option."""
		return self.highlighted_option_index
	
	@property
	def get_current_sting(self):
		"""Returns the current sting number."""
		return self.last_sting
	
	def set_menu_mode(self, mode=True):
		self.menu_mode = mode
	
	def menu_left(self):
		if self.menu_mode == True:
			highlighted_option = self.highlighted_option_index
			highlighted_option = highlighted_option - 1
			if highlighted_option < 0:
				highlighted_option = (self.number_of_options-1)
			self.highlighted_option_index = highlighted_option
			return highlighted_option
	
	def menu_right(self):
		if self.menu_mode == True:
			highlighted_option = self.highlighted_option_index
			highlighted_option = highlighted_option + 1
			if highlighted_option > (self.number_of_options-1):
				highlighted_option = 0
			self.highlighted_option_index = highlighted_option
			return highlighted_option
	
	def menu_load(self):
		if self.current_option['type'] <> "Folder":
			self.stop()
		self.current_option_index = self.highlighted_option_index
		self.load_player()
		self.menu_mode = False

	def play(self):
		if self.current_option['type'] <> "Info":
			self.VLC.connect()
			if self.current_option['type'] == "Folder":
				self.VLC.randomon()
				self.VLC.next()
			self.VLC.play()
			self.VLC.disconnect()
		
	def stop(self):
		if self.current_option['type']  == "Sting":
			self.load_player()
		self.VLC.connect()
		self.VLC.stop()
		self.VLC.disconnect()
	
	def load_player(self):
		
		option_type = self.current_option['type']
		option_name = self.current_option['name']
		option_address = self.current_option['source']

		self.VLC.connect()

		if option_type == "Stream":
			player_source = option_address
			self.VLC.clear()
			self.VLC.enqueue(player_source)
			self.VLC.loopoff()
		if option_type == "Folder":
			player_source = option_address
			self.VLC.clear()
			self.VLC.enqueue(player_source)
			self.VLC.loopon()
			self.VLC.randomon()
		if option_type == "File":
			player_source = option_address
			self.VLC.clear()
			self.VLC.enqueue(player_source)
			self.VLC.loopoff()
		if option_type == "Help":
			player_source = option_address
			self.VLC.clear()
			self.VLC.enqueue(player_source)
			self.VLC.loopon()
		if option_type == "Sting":
			sting = str(self.last_sting+1)
			option_name = "Sting: "+sting
			sting_counter = len(glob.glob1(option_address,"*.mp3"))-1
			self.last_sting = self.last_sting+1
			if self.last_sting > sting_counter:
				self.last_sting = 0
			player_source = option_address+sting+".mp3"
			self.VLC.clear()
			self.VLC.enqueue(option_address+sting+".mp3")
			self.VLC.loopoff()
			self.VLC.randomoff()
		
		self.VLC.disconnect()
		return option_name
		
def play_button(event):
	global player
	global display
	player.set_menu_mode(False)
	player.menu_mode = False
	if player.get_highlighted_option_index <> player.get_current_option_index:
		player.menu_load()
	player.play()
	if player.current_option['type'] <> "Sting":
		display.update_display_line_one(player.current_option['name'])
	else:
		sting = str(player.get_current_sting)
		option_name = "Sting: "+sting
		display.update_display_line_one(option_name)
	display_thread = threading.Thread(target=display.start_playing_info)
	display_thread.start()
	
def stop_button(event):
	global player
	global display
	player.stop()
	if player.current_option['type'] == "Sting":
		sting = str(player.get_current_sting)
		option_name = "Sting: "+sting
		display.update_display_line_one(option_name)
	display.stop_playing_info()

def menu_button(event):
	global player
	global display
	
	player.set_menu_mode(True)
	display.stop_playing_info()
	display.update_display_line_one("Mode:")
	display.update_display_line_two(player.highlighted_option['name'])
	
def left_button(event):
	global player
	global display
	player.menu_left()
	display.update_display_line_one("Mode:")
	display.update_display_line_two(player.highlighted_option['name'])
	
def right_button(event):
	global player
	global display
	player.menu_right()
	display.update_display_line_one("Mode:")
	display.update_display_line_two(player.highlighted_option['name'])

def select_button(event):
	global player
	global display
	display.stop_playing_info()
	if player.get_menu_mode:
		if player.highlighted_option['type'] <> "Info":	
			display.stop_playing_info()
			if player.highlighted_option['name'] <> player.current_option['name']:
				player.menu_load()
			else:
				display_thread = threading.Thread(target=display.start_playing_info)
				display_thread.start()
			if player.current_option['type'] <> "Sting":	
				display.update_display_line_one(player.current_option['name'])
			else:
				sting = str(player.get_current_sting)
				option_name = "Sting: "+sting
				display.update_display_line_one(option_name)
			display.update_display_line_two(" ")
		else:
			if player.highlighted_option['name'] == "Net Info":
				net_info()
			if player.highlighted_option['name'] == "Sys Info":
				display.sys_info()
	else:
		player.set_menu_mode(True)
		display.stop_playing_info()
		display.update_display_line_one("Mode:")
		display.update_display_line_two(player.highlighted_option['name'])
		
if __name__ == "__main__":
	
	PLAYER_PROCESS = subprocess.Popen(["/usr/bin/vlc", "-I", "dummy", "--volume", "150", "--intf", "telnet", "--lua-config", "telnet={host='0.0.0.0:4212'}"])
	
	pfd = pifacedigitalio.PiFaceDigital()
	
	vlc = VLCClient("127.0.0.1",4212,"admin",1)
	
	global cloud
	
	cloud = Cloud(pfd, vlc)
	cloud.run();
	player.set_menu_mode(True)
	
	#LISTENER = pifacecad.SwitchEventListener(chip=cad)
	
	#LISTENER.register(0, pifacecad.IODIR_FALLING_EDGE, play_button)
	#LISTENER.register(1, pifacecad.IODIR_FALLING_EDGE, stop_button)
	#LISTENER.register(2, pifacecad.IODIR_FALLING_EDGE, left_button)
	#LISTENER.register(3, pifacecad.IODIR_FALLING_EDGE, right_button)
	#LISTENER.register(4, pifacecad.IODIR_FALLING_EDGE, select_button)
	#LISTENER.activate()