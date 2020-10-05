# Emoticon-Typer-Thing
### What is it?
A small Python script that will allow the user to type a command (e.g. "\shrug") and have it replaced with a result (e.g. "¯\\\_(ツ)\_/¯")

### How it roughly works
It listens to keys being pressed, when the prefix is pressed it will start to log all the following keys that can be used for a command, when it sees space or enter it will then lookup the command, remove the command and prefix, and enter in the result, then forget and reset

### Why did I make this?
I was bored when looking at Discord's "/shrug" command and thought it would be cool to have that in other messaging apps so took a language I somewhat knew and started messing around

### Current Features
- Decent tracking of keyboard input
  - Only accepts certain characters stored in a set
  - Reconises selecting and removing of the word or the whole text
- Removing of the original command and typing of the result
- Auto-compleating of a partial typed command
- Config file
  - Change Prefix key
  - Change Auto-compleate key
  - Change the list of commands and emoticons/results

### Dependencies
- Python 3 (untested on any other versions)
- PynPut (https://pypi.org/project/pynput/)
- Windows (only tested on Win10)
