#!env python3
"""
HackaGame - Game - MoveIt 
"""
import sys
sys.path.insert( 1, __file__.split('gameMoveIt')[0] )

from hacka.games.moveIt import GameMoveIt
from hacka.games.moveIt.shell import PlayerShell as Player
from hacka.core.command import Command, Option

# Define a command interpreter: 2 options: host address and port:
cmd= Command(
        "start-server",
        [
            Option( "port", "p", default=1400 ),
            Option( "seed", "s", 0, "random seed (0 == no seed)" ),
            Option( "cycle", "c", 10, "number of cycles before game end" ),
            Option( "number", "n", 1, "number of games" ),
        ],
        (
            "star a server of gameMoveIt on your machine. "
            "gameMoveIt do not take ARGUMENT."
        ))
# Process the command line: 
cmd.process()
if not cmd.ready() :
    print( cmd.help() )
    exit()

game= GameMoveIt( seed= cmd.option("seed"), numberOfCycle= cmd.option("cycle") )
player= Player()
game.launch( [player], cmd.option("number") )  
