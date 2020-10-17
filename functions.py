#######################
#	Imports
#######################
# Files
from config import * 	# All vars that are set by user before runnning
import settings 		# All vars that are being shared across whole program

# Modules
from pynput import keyboard 	# For keyboard monitoring and control


#######################
#	Values
#######################
# Classes
Controller = keyboard.Controller() 	# To control the keyboard

# Auto-Complete Thing
AutoCompleteList = [] 	# Holds all of the possible commands when autofilling
TabChangeValue = -1 	# Tracks the position in the autofill list


#######################
#	Functions
#######################
# To remove the written command
def RemoveCommand(txt, extra):
	settings.WordSelected = False  	# No longer selecting the word
	settings.AllSelected = False 	# No longer selecting the whole text
	extra = extra or 0 				# How many extra characters are being removed (such as Prefix)

	for i in range(0, txt.count("")+extra): 				# Loops the length of the command +extra, this method (I think) better as not all editors allow words to be selected/highlighted (for quicker removal)
		settings.IgnoreKeys = settings.IgnoreKeys + 1 		# To ignore the computer's key press
		Controller.press(keyboard.Key.backspace) 			# Removes a character
		Controller.release(keyboard.Key.backspace)

# To type text out
def TypeCommand(txt, space):
	settings.WordSelected = False 						# If we're typing, these will no longer be True
	settings.AllSelected = False

	for i in txt:
		Controller.press(i) 							# Not using .type() since I needed more control per keystroke
		Controller.release(i)
		settings.IgnoreKeys = settings.IgnoreKeys + 1 	# To avoid the script typing out a registering another command, so we ignore the keypresses

	if space:
		Controller.press(keyboard.Key.space) 			# Quality of life space so can keep typing normally after a result
		Controller.release(keyboard.Key.space)

# To change what the script thinks the user has typed
def ChangeTypedCommand(newCommand):
	global TabChangeValue
	global AutoCompleteList

	settings.TypedCommand = newCommand 	# Changing what the script thinks we have typed
	settings.WordSelected = False 		# If the command is changing then this cant be true anymore
	settings.AllSelected = False		# ^
	TabChangeValue = -1 				# They are no longer looking at the same auto-fill so reset
	AutoCompleteList = [] 				# ^

# To start listening for command
def StartCommandListening():
	print("Starting Command Listen") 

	print(settings.TypedCommand)
	settings.ListenCommand = True 	# Started listening for certain keyboard events
	ChangeTypedCommand("") 			# Reseting what we think the command is so its ready for a new one

# To stop listening for command
def StopCommandListening():
	print("Stopping Command Listen")

	settings.ListenCommand = False 	# Stopping listening for certain keyboard events
	ChangeTypedCommand("") 			# Reseting what we think the command is so its ready for next time

# Check given command against table to then type
def CheckCommands(cmd):
	global Commands

	if cmd in Commands: 					# Checks for valid command
		RemoveCommand(cmd, 1) 				# Removes the user written command and prefix
		TypeCommand(Commands[cmd], True) 	# Types the command result and a space

	StopCommandListening() 					# Stops listening for command reguardless since space has been pressed

# Check for matching commands for auto-fill
def CheckMatchingCommands(cmd):
	global Commands
	global TabChangeValue
	global AutoCompleteList

	if TabChangeValue != -1: 										# If this is not -1 then we are already going through a list
		if TabChangeValue == len(AutoCompleteList): 				# Check if we are at the end of the list
			TabChangeValue = 0 										# Setting us back to the start of the list

		print("Changing to "+AutoCompleteList[TabChangeValue])
		RemoveCommand(settings.TypedCommand, 0) 					# Removes our command (not the prefix)
		settings.TypedCommand = AutoCompleteList[TabChangeValue] 	# Changing our known command to the new auto-filled one
		TypeCommand(settings.TypedCommand, False) 					# Typing out the auto-filled command

		TabChangeValue = TabChangeValue + 1 						# Increasing where we are in the auto-fill list

	else: 													# If we don't have a list going
		for k, v in Commands.items(): 						# Loop through all the config commands
			ListPosition = k.find(cmd) 						# Searching through one command to find any matching sub-strings with the user given command
			if ListPosition != -1: 							# If there is a matching sub-string anywhere in the command
				AutoCompleteList.insert(ListPosition, k) 	# Inserts the command to auto-fill list to a position based on how many characters matched 

		if len(AutoCompleteList) > 0: 						# If we had any auto-fill matches
			TabChangeValue = 0								# Put us at the start of the list
			CheckMatchingCommands("") 						# Re-run this command as to put us on the first auto-fill (quality of life)
		else: 												# If we didn't have any matches
			TabChangeValue = -1 							# Set indicatior that there is no auto-fill list