#!env python3
"""
MoveIt - an HackaGame Game  
"""

import hacka.games.moveit as moveit
#from hacka.games.moveIt.shell import PlayerShell as Player
from hacka.command import Command, Option

# Define a command interpreter: 2 options: host address and port:
cmd= Command(
        "start-server",
        [
            Option( "port", "p", default=1400 ),
            Option( "seed", "s", 0, "random seed (0 == random seed)" ),
            Option( "cycle", "c", 10, "number of cycles before game end" ),
            Option( "number", "n", 1, "number of games" ),
        ],
        (
            "star a server of MoveIt on your machine. "
            "MoveIt do not take ARGUMENT."
        ))

# Process the command line: 
cmd.process()
if not cmd.ready() :
    print( cmd.help() )
    exit()

game= moveit.GameMaster(
    seed= cmd.option("seed"),
    numberOfCycle= cmd.option("cycle")
)
player= moveit.ShellPlayer()

game.launch( [player], cmd.option("number") )  
