#!env python3
"""
MoveIt - an HackaGame Game  
"""

import hacka.games.moveit as moveit
#from hacka.games.moveIt.shell import PlayerShell as Player
from hacka.command import Command, Option

# Configure the game:
gameEngine= moveit.GameEngine(
    matrix= [
        [00, 00, 00, 00, 00],
        [00, -1, 00, -1, 00],
        [00, 00, 00, 00, 00],
        [00, -1, 00, -1, 00],
        [00, 00, 00, 00, 00]
    ],
    numberOfPlayers=1, numberOfRobot=2,
    tic= 10 
)
gameEngine.setMobilePosition(1, 1, 10)

# Player: 

class ShellPlayer( moveit.BasicBot ):
    def __init__(self):
        super().__init__()
        self._action= "go"
    
    # Player interface :
    def wakeUp(self, playerId, numberOfPlayers, gamePod):
        super().wakeUp(playerId, numberOfPlayers, gamePod)
        self.model().render()
        print( f"Output image : ./shot-moveIt.png" )
        self._action= "go"
        print( "New game..." )
        print( "Possible Actions:" )
        print( "   - [mission robotId missionId ...] move robotId clockDirection ... or pass" )
        print( "   - pass" )
        print( "the mission part is optional and only one action per robot will be achieved" )

    def perceive(self, statePod):
        super().perceive(statePod)
        self.model().render()

    def decide(self):
        if self._action != "stop" :
            self._action = input(f'tic-{ self.model().tic() } - Enter your action: ')
        if self._action == "stop" :
            return "pass"
        return self._action

    def sleep(self, result):
        super().sleep(result)
        print( f"End on result: {result}" )

# Then Go...
gameMaster= moveit.GameMaster( gameEngine, randomMission= 4 )
player= ShellPlayer() #moveit.player.ShellPlayer()
gameMaster.launch( [player], 1 )

