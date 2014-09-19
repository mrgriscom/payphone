#!/usr/bin/env python
from time import sleep

import RPi.GPIO as GPIO
import os
import pygame

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

buttonDown = False
onHook = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN) # on hook trigger
GPIO.setup(17, GPIO.IN) # button pressed trigger 
GPIO.setup(18, GPIO.IN) # outA
GPIO.setup(23, GPIO.IN) # outB
GPIO.setup(24, GPIO.IN) # outC
GPIO.setup(25, GPIO.IN) # outD

GPIO.setup(27, GPIO.IN) # coin in 1

sound0 = pygame.mixer.Sound('/home/pi/audio/DTMF-0.wav')
sound1 = pygame.mixer.Sound('/home/pi/audio/DTMF-1.wav')
sound2 = pygame.mixer.Sound('/home/pi/audio/DTMF-2.wav')
sound3 = pygame.mixer.Sound('/home/pi/audio/DTMF-3.wav')
sound4 = pygame.mixer.Sound('/home/pi/audio/DTMF-4.wav')
sound5 = pygame.mixer.Sound('/home/pi/audio/DTMF-5.wav')
sound6 = pygame.mixer.Sound('/home/pi/audio/DTMF-6.wav')
sound7 = pygame.mixer.Sound('/home/pi/audio/DTMF-7.wav')
sound8 = pygame.mixer.Sound('/home/pi/audio/DTMF-8.wav')
sound9 = pygame.mixer.Sound('/home/pi/audio/DTMF-9.wav')
soundStar = pygame.mixer.Sound('/home/pi/audio/DTMF-star.wav')
soundPound = pygame.mixer.Sound('/home/pi/audio/DTMF-pound.wav')
soundDialTone = pygame.mixer.Sound('/home/pi/audio/dialtone.wav')

menu1 = pygame.mixer.Sound('/home/pi/audio/project1.wav')
menu2 = pygame.mixer.Sound('/home/pi/audio/project2.wav')
menu3 = pygame.mixer.Sound('/home/pi/audio/project3.wav')
menu4 = pygame.mixer.Sound('/home/pi/audio/project4.wav')
menu5 = pygame.mixer.Sound('/home/pi/audio/history.wav')
menu = pygame.mixer.Sound('/home/pi/audio/menu.wav')
menuShort = pygame.mixer.Sound('/home/pi/audio/menuShort.wav')

def stopSound():
	pygame.mixer.stop()

def stopSomeSounds(): 
	sound0.stop()
	sound1.stop()
	sound2.stop()
	sound3.stop()
	sound4.stop()
	sound5.stop()
	sound6.stop()
	sound7.stop()
	sound8.stop()
	sound9.stop()
	soundStar.stop()
	soundPound.stop()

def playSelection(keyNum): 
	if(keyNum == "0"):
		menuShort.play()
	elif(keyNum == "1"): 
		menu1.play()
	elif(keyNum == "2"): 
		menu2.play()
	elif(keyNum == "3"): 
		menu3.play()
	elif(keyNum == "4"): 
		menu4.play()
	elif(keyNum == "5"): 
		menu5.play()


def playKey(keyNum): 
	if(keyNum == "0"):
		stopSound()
		sound0.play()
	elif(keyNum == "1"): 
		stopSound()
		sound1.play()
	elif(keyNum == "2"): 
		stopSound()
		sound2.play()
	elif(keyNum == "3"): 
		stopSound()
		sound3.play()
	elif(keyNum == "4"): 
		stopSound()
		sound4.play()
	elif(keyNum == "5"): 
		stopSound()
		sound5.play()
	elif(keyNum == "6"): 
		sound6.play()
	elif(keyNum == "7"): 
		sound7.play()
	elif(keyNum == "8"): 
		sound8.play()
	elif(keyNum == "9"): 
		sound9.play()
	elif(keyNum == "*"): 
		soundStar.play()
	elif(keyNum == "#"): 
		soundPound.play()

# Maps binary output to a button number. 

def keyPress(outA, outB, outC, outD): 
	if(outA == 1 and outB == 0 and outC == 0 and outD == 0): 
		return "2" 
	elif(outA == 0 and outB == 0 and outC == 0 and outD == 0): 
		return "1" 
	elif(outA == 0 and outB == 1 and outC == 0 and outD == 0): 
		return "3" 
	elif(outA == 1 and outB == 0 and outC == 1 and outD == 0): 
		return "5"
	elif(outA == 0 and outB == 0 and outC == 1 and outD == 0): 
		return "4"
	elif(outA == 0 and outB == 1 and outC == 1 and outD == 0): 
		return "6"
	elif(outA == 1 and outB == 0 and outC == 0 and outD == 1): 
		return "8" 
	elif(outA == 0 and outB == 0 and outC == 0 and outD == 1): 
		return "7" 
	elif(outA == 0 and outB == 1 and outC == 0 and outD == 1): 
		return "9" 
	elif(outA == 1 and outB == 0 and outC == 1 and outD == 1): 
		return "0"
	elif(outA == 0 and outB == 0 and outC == 1 and outD == 1): 
		return "*"
	elif(outA == 0 and outB == 1 and outC == 1 and outD == 1): 
		return "#"
	else:
		return "F"

while True:

	# Main loop. 
    	# Trigger for input(4) goes low (false) when activated. 
    	# Check to see if we are moving from being on the hook to off the hook... 
    
	if(GPIO.input(4) == True and onHook == False): 
		print("on hook")
		onHook = True # moving to on state 
		stopSound() # stop all sounds 
		buttonDown = False # just in case someone puts phone down while pressing button... 

	elif(GPIO.input(4) == False and onHook == True): 
		print("off hook")
        	menu.play(loops=999)
		onHook = False
       
	elif(onHook == False):
		
        	# If phone is picked up, handle button presses 

		if(GPIO.input(17) == True and buttonDown == False): 
        
        		# Button pressed. 
            		# To test, print out formatted binary from 74C922 chip. 

			currentKey = keyPress(GPIO.input(18), GPIO.input(23), GPIO.input(24), GPIO.input(25))
			playKey(currentKey)
			buttonDown = True 
#			print str(GPIO.input(18)) + " " + str(GPIO.input(23)) + " " + str(GPIO.input(24)) + " " + str(GPIO.input(25))
#			print "button pressed: " + currentKey

	        # otherwise, if button released, print that and set state. 
        	# if neither of these is true, the handle is up and no buttons are pressed, so do nothing. 

		elif(GPIO.input(17) == False and buttonDown == True):

			# Button released - stop all DTMF sounds, reset buttonDown

			stopSound()
			currentKey = keyPress(GPIO.input(18), GPIO.input(23), GPIO.input(24), GPIO.input(25))
			playSelection(currentKey)
			print("button released: " + currentKey) 
			buttonDown = False

		elif(pygame.mixer.get_busy() == False): 

			menuShort.play()
            
    	# Sleep for 100 ms then repeat. 
	
	# print keyPress(GPIO.input(18), GPIO.input(23), GPIO.input(24), GPIO.input(25))
	# print str(GPIO.input(18)) + " " + str(GPIO.input(23)) + " " + str(GPIO.input(24)) + " " + str(GPIO.input(25))
	sleep(0.025);
