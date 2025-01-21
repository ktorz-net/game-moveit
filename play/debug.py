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
    missions= [(1, 12), (1, 12), (8, 12)],
    tic= 10 
)
gameEngine.setMobilePosition(1, 1, 10)

# Go...
gameMaster= moveit.GameMaster( gameEngine )
player= moveit.player.ShellPlayer()
gameMaster.launch( [player], 1 )

