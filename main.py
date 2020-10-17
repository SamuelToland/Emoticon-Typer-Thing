#######################
#	Imports
#######################
# Files
from config import *  		# All vars that are set by user before runnning
from functions import * 	# All our functions
import settings 			# All vars that are being shared across whole program

# Modules
from pynput import keyboard 	# For keyboard monitoring and control

#######################
#	Values
####################### 
# Key Press Checks
CommandChars = {"\\","0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","`","!","\"","$","%","^","&","*","(",")","_","+","-","=","|","[","]","{","}",";","'","#",":","@","~",",",".","/","<",">","?"} 	# Allowed characters that can be used in commands
HotKeyListen = {"ctrl_l": False, "shift": False, "left": False, "": False} 	# For tracking cetain key-combinations to do with deleting characters/words


#######################
#	Functions
#######################
# Check and listen to key presses for important characters
def CheckKeyPress(key):
	# Setting key's name
	try:            	# Getting keyboard input as string to easier compare against 
		k = key.char 	
	except:
		k = key.name

	# Vars
	global HotKeyListen

	# Statements
	if k == FailSafeKey: 	# Failsafe to stop the whole keyboard.Listener incase of errors
		print("Escaping")
		return False

	elif settings.IgnoreKeys > 0: 	# Check if we are to ignore the keypress (for when script is typing)
		print("Ignoring")
		settings.IgnoreKeys = settings.IgnoreKeys - 1

	elif k == Prefix and k != "ctrl_l": 	# Checking for prefix to start command listening 
		if not settings.ListenCommand:
			StartCommandListening()
		else:								# If already listening then lets restart the listen
			StopCommandListening()
			StartCommandListening()

	elif settings.ListenCommand and (k == "space" or k == "enter") and k != "ctrl_l" and not settings.AllSelected: 	# Checking if we are listening and if user types space indecating end of 'settings.TypedCommand'
		print("Checking Command")		
		CheckCommands(settings.TypedCommand)
 		
	elif settings.ListenCommand: 											# If listening and none above, check the input as to compare it for 'settings.TypedCommand' later
		if k == "backspace":
			if settings.TypedCommand == "": 								# If 'settings.TypedCommand' is empty then user is removing the prefix so stop listening
				StopCommandListening()
			elif HotKeyListen["ctrl_l"] or settings.WordSelected == True:	# If holding control key or they have the word selected, then they are removing the whole word
				ChangeTypedCommand("")
			elif settings.AllSelected == True: 								# If all of the text is selected then they're removing all of it, stop listening since no more prefix
				StopCommandListening()
			else:
				ChangeTypedCommand(settings.TypedCommand[:-1]) 				# They're removing the end character

		elif k in HotKeyListen:
			HotKeyListen[k] = True 															# Tracking what keys are being held
			if HotKeyListen["ctrl_l"] and HotKeyListen["shift"] and HotKeyListen["left"]:	# They're selecting the whole word
				settings.WordSelected = True
			elif HotKeyListen["ctrl_l"] and HotKeyListen[""]: 						# They're selecting everything in the text box
				settings.AllSelected = True

		elif k == AutoCompleteKey and not (settings.AllSelected or settings.WordSelected): 	# They're autocompleating the command (if they havent got it selected subsiquently removing the word)
			CheckMatchingCommands(settings.TypedCommand)

		elif k in CommandChars and k != "ctrl_l": 					# Checking if input is in our allowed command characters as to stop utility keys (such as enter, insert, save, etc)
			if settings.WordSelected == True:						# They're replacing their command with a character
				ChangeTypedCommand("" + str(k))
			elif settings.AllSelected == True: 						# They're replacing their whole text with a character so no more prefix (stop listening)
				StopCommandListening()
			else: 									  				# They're adding a char to the command
				ChangeTypedCommand(settings.TypedCommand + str(k))

		print("Current Command: "+settings.TypedCommand)

# Check key releases to monitor "hot-key" presses
def CheckKeyRelease(key):
	try: 				# Getting keyboard input as string to easier compare against 
		k = key.char
	except:
		k = key.name

	global HotKeyListen

	if k == FailSafeKey: 		# Failsafe to stop the whole keyboard.Listener incase of errors
		print("Escaping")
		return False

	elif k in HotKeyListen: 	# Tracking what keys are no longer held
		HotKeyListen[k] = False 	

	elif (settings.WordSelected or settings.AllSelected) and k == "right": 	# They're de-selecting the word or text
		settings.WordSelected = False
		settings.AllSelected = False


#######################
# Main	
#######################
# Key Listener
listener = keyboard.Listener(on_press=CheckKeyPress, on_release=CheckKeyRelease) 	# Creating a keyboard listener that will allow us to watch for key presses
listener.start() 										
listener.join()