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
        [00, 00, 00, -1, 00, 00, 00, 00, 00, 00],
        [00, -1, 00, 00, 00, -1, 00, -1, -1, 00],
        [00, 00, 00, -1, 00, 00, 00, -1, 00, 00],
        [00, 00, 00, -1, 00, 00, 00, 00, 00, 00],
        [00, -1, 00, 00, 00, -1, 00, -1, -1, -1],
        [00, -1, 00, -1, 00, 00, 00, -1, -1, -1],
        [00, 00, 00, 00, 00, -1, 00, -1, -1, -1]
    ],
    numberOfPlayers=2, numberOfRobot=6,
    tic= 40
)

# Then Go...
gameMaster= moveit.GameMaster( gameEngine, randomMission=8 )
player= ShellPlayer()
player2= ShellPlayer()
gameMaster.launch( [player, player2], gameEngine.numberOfPlayers() )
