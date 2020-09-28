#######################
#	Imports
#######################
from pynput import keyboard  							# For keyboard monitoring and control


#######################
#	Config
#######################
Prefix = "\\" 											# The character used to tell the script user is starting a command
AutoCompleteKey = "`"
Commands = { 											# the table holding all of the commands and results
	"shrug": "¯\\_(ツ)_/¯",
	"tableflip": "(╯°□°）╯︵ ┻━┻",
	"tableunflip": "┬─┬ ノ( ゜-゜ノ)",
	"lenny": "( ͡° ͜ʖ ͡°)",
	"bear": "ʕ•ᴥ•ʔ",
	"disapprove": "ಠ_ಠ",
	"creepylenny": "┬┴┬┴┤ ͜ʖ ͡°) ├┬┴┬┴",
	"fightme": "(ง'̀-'́)ง",
	"worried": "(´･_･`)",
	"personflip": "(╯°Д°)╯︵/(.□ . \\)",
	"magic": "(∩ ` -´)⊃━━☆ﾟ.*･｡ﾟ",
	"disbelief": "☉_☉",
	"gimme": "( つ ◕_◕ )つ",
	"kiss": "( ˘ ³˘)♥",
	"blank": "(゜-゜)",
	"pissed": "(/ﾟДﾟ)/",
	"pretty": "(◕‿◕✿)",
	"dance2": "♪~ ᕕ(ᐛ)ᕗ",
	"dance": "(~˘▾˘)~",
	"stab": "ᗜԅ(⇀︿⇀)ᓄ-¤]═────",
	"kick": "ヽ(#ﾟДﾟ)ﾉ┌┛(ﾉ´Д｀)ﾉ",
	"punch": "O=('-'Q)",
	"shoot": "(• ε •)",
	"wink": "◕‿↼",
	"sad": "(ﾟ∩ﾟ)",
	"myman": "(☞ﾟ∀ﾟ)☞",
	"handonhead": "(>‘o’)>",
	"HHH": "HHH",
	"rickroll": "https://www.youtube.com/watch?v=oHg5SJYRHA0",
}


#######################
#	Values
#######################
Controller = keyboard.Controller()						# To control the keyboard
ListenCommand = False 									# To know to listen for the following keys after prefix pressed
TypedCommand = ""										# The possible command being typed to check against 'commands' array 
IgnoreKeys = 0 											# Used to ignore some auto key presses cuz screw python
CommandChars = {"\\","0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","`","!","\"","$","%","^","&","*","(",")","_","+","-","=","|","[","]","{","}",";","'","#",":","@","~",",",".","/","<",">","?"} 	# Allowed characters that can be used in commands
HotKeyListen = {"ctrl_l": False, "shift": False, "left": False, "": False}
WordSelected = False
AllSelected = False
AutoCompleteList = []
TabChangeValue = -1


#######################
#	Functions
#######################
# To remove the written command
def RemoveCommand(txt, extra):
	global IgnoreKeys
	global WordSelected
	global AllSelected

	WordSelected = False
	AllSelected = False
	extra = extra or 0

	for i in range(0, txt.count("")+extra): 				# Loops the length of the command (+extra for the prefix n stuff), this method better as not all editors allow words to be selected/highlighted
		IgnoreKeys = IgnoreKeys + 1
		Controller.press(keyboard.Key.backspace) 			# Removes a character
		Controller.release(keyboard.Key.backspace)

# To type text out
def TypeCommand(txt, space):
	global IgnoreKeys
	global WordSelected
	global AllSelected

	WordSelected = False
	AllSelected = False

	for i in txt:
		Controller.press(i) 							# Not using .type() since it types after the python code leading to command possibly looping with prefix
		Controller.release(i)
		IgnoreKeys = IgnoreKeys + 1 					# ^ to help avoid by ignoring the typing of the command result

	if space:
		Controller.press(keyboard.Key.space) 				# Quality of life space so can keep typing normally
		Controller.release(keyboard.Key.space)

def ChangeTypedCommand(newCommand):
	global TypedCommand
	global WordSelected
	global AllSelected
	global TabChangeValue
	global AutoCompleteList

	TypedCommand = newCommand
	WordSelected = False
	AllSelected = False
	TabChangeValue = -1
	AutoCompleteList = []

# To start listening for command
def StartCommandListening():
	print("Starting Command Listen")

	global ListenCommand

	ListenCommand = True 								# Telling the 'CheckKeyPress' that we are listening for a command
	ChangeTypedCommand("") 								# Reseting what we think is the command (going to be typed) is

# To stop listening for command
def StopCommandListening():
	print("Stopping Command Listen")

	global ListenCommand

	ListenCommand = False								# Telling the 'CheckKeyPress' that we are no longer listening for a command
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
	global IgnoreKeys
	global TypedCommand
	global Prefix

	#IgnoreKeys = IgnoreKeys + 1
	#Controller.press(keyboard.Key.backspace) 		# Removes the character used to start autocomplete
	#Controller.release(keyboard.Key.backspace)

	if TabChangeValue != -1:
		if TabChangeValue == len(AutoCompleteList):
			TabChangeValue = 0

		print("Changing to "+AutoCompleteList[TabChangeValue])
		RemoveCommand(TypedCommand, 0)
		TypedCommand = AutoCompleteList[TabChangeValue]
		TypeCommand(TypedCommand, False)

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

# Check and listen to key presses for key characters
def CheckKeyPress(key):
	try: 												# Getting keyboard input as string to compare against 
		k = key.char
	except:
		k = key.name

	global ListenCommand
	global TypedCommand
	global IgnoreKeys
	global HotKeyListen
	global WordSelected
	global AllSelected

	if k == "page_up": 									# To stop the whole listening, for failsafe
		print("Escaping")
		return False

	elif IgnoreKeys > 0: 								# Check if we are to ignore the keypress (for when script is typing)
		print("Ignoring")
		IgnoreKeys = IgnoreKeys - 1

	elif k == Prefix and k != "ctrl_l": 				# Checking for prefix to start command listening
		if not ListenCommand:
			StartCommandListening()
		else:											# If already listening then lets restart the listen
			StopCommandListening()
			StartCommandListening()

	elif ListenCommand and (k == "space" or k == "enter") and k != "ctrl_l" and not AllSelected: 				# Checking if we are listening and if user types space indecating end of 'TypedCommand'
		print("Checking Command")		
		CheckCommands(TypedCommand)
 		
	elif ListenCommand: 								# If listening and none above, check the input as to compare it for 'TypedCommand' later
		if k == "backspace":							# If backspace then remove last char from 'TypedCommand'
			if TypedCommand == "": 						# If 'TypedCommand' is empty then user has removed the prefix so stop listening
				StopCommandListening()
			elif HotKeyListen["ctrl_l"] or WordSelected == True:
				ChangeTypedCommand("")
			elif AllSelected == True:
				StopCommandListening()
			else:
				ChangeTypedCommand(TypedCommand[:-1])

		elif k in HotKeyListen:
			HotKeyListen[k] = True
			if HotKeyListen["ctrl_l"] and HotKeyListen["shift"] and HotKeyListen["left"]:
				WordSelected = True
			elif HotKeyListen["ctrl_l"] and HotKeyListen[""]:
				AllSelected = True

		elif k == AutoCompleteKey and not (AllSelected or WordSelected):
			CheckMatchingCommands(TypedCommand)

		elif k in CommandChars and k != "ctrl_l": 						# Checking if input is in our allowed command characters as to stop utility keys (such as enter, insert, etc)
			if WordSelected == True:
				ChangeTypedCommand("" + str(k))
			elif AllSelected == True:
				StopCommandListening()
			else:
				ChangeTypedCommand(TypedCommand + str(k))

		print("Current Command: "+TypedCommand)

# Check for hot key releases
def CheckKeyRelease(key):
	try: 												# Getting keyboard input as string to compare against 
		k = key.char
	except:
		k = key.name

	global HotKeyListen
	global WordSelected
	global AllSelected

	if k == "page_up": 									# To stop the whole listening, for failsafe
		print("Escaping")
		return False

	elif k in HotKeyListen:
		HotKeyListen[k] = False

	elif (WordSelected or AllSelected) and k == "right":
		WordSelected = False
		AllSelected = False


#######################
#	Key Listener
#######################
listener = keyboard.Listener(on_press=CheckKeyPress, on_release=CheckKeyRelease) 	# Creating a keyboard listener to run 'CheckKeyPress' on keyboard input
listener.start() 										
listener.join()