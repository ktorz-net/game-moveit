#!env python3
"""
MoveIt - an HackaGame Game  
"""

import hacka.games.moveit as moveit
from hacka.games.moveit.player import ShellPlayer
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
    missions= [(6, 21), (7, 12), (11, 2), (18, 8)],
    tic= 100
)

# Then Go...
gameMaster= moveit.GameMaster( gameEngine )
player= ShellPlayer()
gameMaster.launch( [player], 1 )

