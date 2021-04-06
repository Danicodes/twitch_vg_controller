# twitch_vg_controller [Work in progress]

Project to let chat play a game (Mortal Kombat) in IRC

-------------
vclient.py
----
Creates a client running within the bot (in WSL) that will be sending requests to the server to perform some actions 
in the game

vserver.py
----
Creates a server running in a powershell subprocess that will be handling requests from the client to perform some actions 
in the game.

vcontroller
----
Contains Controller class and Button Enums
Creates a Controller class which instantiates an Xbox 360 gamepad and saves the player name
The controller has wrapper functions to make it easy to do common actions like press and release any button
since the controller will need to update in between button presses and sometimes needs to stall to let input go through

Also allows to parse string input (which we will get from the twitch IRC chat)
```
def parse_moveset(self, moveset: str):
        for movechar in moveset:
            if movechar == 'L':
                self.move_left()
```

vplayer.py -- to delete

windowfocus.py
---
Lets you find a window by name and bring it to focus on the windows OS.
