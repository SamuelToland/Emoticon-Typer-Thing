#######################
#	Imports
#######################
# Files
from config import *
import settings

# Modules
from pynput import keyboard  							# For keyboard monitoring and control


#######################
#	Values
#######################
# Classes
Controller = keyboard.Controller()						# To control the keyboard

# Auto-Complete Thing
AutoCompleteList = []
TabChangeValue = -1


#######################
#	Functions
#######################
# To remove the written command
def RemoveCommand(txt, extra):
	settings.WordSelected = False
	settings.AllSelected = False
	extra = extra or 0

	for i in range(0, txt.count("")+extra): 				# Loops the length of the command (+extra for the prefix n stuff), this method better as not all editors allow words to be selected/highlighted
		settings.IgnoreKeys = settings.IgnoreKeys + 1
		Controller.press(keyboard.Key.backspace) 			# Removes a character
		Controller.release(keyboard.Key.backspace)

# To type text out
def TypeCommand(txt, space):
	settings.WordSelected = False
	settings.AllSelected = False

	for i in txt:
		Controller.press(i) 							# Not using .type() since it types after the python code leading to command possibly looping with prefix
		Controller.release(i)
		settings.IgnoreKeys = settings.IgnoreKeys + 1 					# ^ to help avoid by ignoring the typing of the command result

	if space:
		Controller.press(keyboard.Key.space) 				# Quality of life space so can keep typing normally
		Controller.release(keyboard.Key.space)

def ChangeTypedCommand(newCommand):
	global TabChangeValue
	global AutoCompleteList

	settings.TypedCommand = newCommand
	settings.WordSelected = False
	settings.AllSelected = False
	TabChangeValue = -1
	AutoCompleteList = []

# To start listening for command
def StartCommandListening():
	print("Starting Command Listen")

	print(settings.TypedCommand)
	settings.ListenCommand = True 								# Telling the 'CheckKeyPress' that we are listening for a command
	ChangeTypedCommand("") 								# Reseting what we think is the command (going to be typed) is

# To stop listening for command
def StopCommandListening():
	print("Stopping Command Listen")


	settings.ListenCommand = False								# Telling the 'CheckKeyPress' that we are no longer listening for a command
	ChangeTypedCommand("") 								# Reseting what we think is the command (that was typed) is

# Check given command against table to then type
def CheckCommands(cmd):
	global Commands

	if cmd in Commands: 								# Checks for valid command
		RemoveCommand(cmd, 1) 							# Removes the user written command and prefix
		TypeCommand(Commands[cmd], True) 				# Types the command result

	StopCommandListening() 								# Stops listening for command reguardless of validity since space has been pressed

# Check for matching commands
def CheckMatchingCommands(cmd):
	global Commands
	global TabChangeValue
	global AutoCompleteList
	global Prefix

	#settings.IgnoreKeys = settings.IgnoreKeys + 1
	#Controller.press(keyboard.Key.backspace) 		# Removes the character used to start autocomplete
	#Controller.release(keyboard.Key.backspace)

	if TabChangeValue != -1:
		if TabChangeValue == len(AutoCompleteList):
			TabChangeValue = 0

		print("Changing to "+AutoCompleteList[TabChangeValue])
		RemoveCommand(settings.TypedCommand, 0)
		settings.TypedCommand = AutoCompleteList[TabChangeValue]
		TypeCommand(settings.TypedCommand, False)

		TabChangeValue = TabChangeValue + 1
	else:
		for k, v in Commands.items():
			ListPosition = k.find(cmd)
			if ListPosition != -1:
				AutoCompleteList.insert(ListPosition, k)

		if len(AutoCompleteList) > 0:
			TabChangeValue = 0
			CheckMatchingCommands("")
		else:
			TabChangeValue = -1

