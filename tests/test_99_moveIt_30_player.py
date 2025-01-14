import os, sys, pathlib
workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

"""
Test - MoveIt Games Class
"""

import src.hacka.core as hk
import src.hacka.games.moveIt as moveIt
from src.hacka.games.moveIt.shell import PlayerShell
from src.hacka.games.moveIt.firstBot import AutonomousPlayer 

def debug( aString ):
    print("<--")
    for line in aString.split("\n") :
        print( '"'+ line + '",')
    print("-->")

def test_playerInteractive():
    game= moveIt.GameMoveIt(42)
    initPod= game.initialize()

    player= PlayerShell()
    player.wakeUp( 1, 1, initPod )

    test= [
"          ▁         ▁         ▁         ▁         ▁         ▁     ",
"       ▖▝   ▘▗   ▖▝   ▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗  ",
"     █         █         ███████████         █         █         █",
"     █         █         ███████████         █         █         █",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝  ",
"█         █         █         █         ███████████         █     ",
"█         █         █         █         ███████████         █     ",
"  ▘▗   ▖▝   ▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝   ▀▜████████▙▄   ▖▝   ▘▗  ",
"     █         ███████████         █         ███████████         █",
"     █         ███████████         █         ███████████         █",
"  ▄▟███▙▄   ▖▝▁▁▁▀▜███▛▀▁▁▁▘▗   ▄▟███▙▄   ▖▝▁▁▁▀▜███▛▀   ▘▗   ▖▝  ",
"███████████  ⎛R  ⎞  █  ⎛H  ⎞  ███████████  ⎛H  ⎞  █         █     ",
"███████████  ⎝  1⎠  █  ⎝  2⎠  ███████████  ⎝  3⎠  █         █     ",
"  ▀▜███▛▀   ▘▗▔▔▔▖▝   ▘▗▔▔▔▖▝   ▀▜███▛▀   ▘▗▔▔▔▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]

    #debug( player._board.shell() )
    for l1, l2 in zip( player._board.shell().split("\n"), test ) :
        assert( l1 == l2)

    assert( len(player._mobiles) == 3 )
    assert( str( player._mobiles[0] ) == "Robot-1[on(1, 0), dir(0), error(0.0)]" )
    assert( str( player._mobiles[1] ) == "Human-2[on(2, 0), dir(0), error(0.0)]" )
    assert( str( player._mobiles[2] ) == "Human-3[on(4, 0), dir(0), error(0.0)]" )

    assert( player._countTic == 0 )
    assert( player._countCycle == 0 )
    assert( player._score == 0 )

    player.perceive( game.playerHand(1) )

    assert( len(player._mobiles) == 3 )
    assert( str( player._mobiles[0] ) == "Robot-1[on(0, 1), dir(0), goal(0, 3)-F, error(0.0)]" )
    assert( str( player._mobiles[1] ) == "Human-2[on(5, 0), dir(0), error(0.0)]" )
    assert( str( player._mobiles[2] ) == "Human-3[on(4, 0), dir(0), error(0.0)]" )

    assert( player._countTic == 16 )
    assert( player._countCycle == 10 )
    assert( player._score == 0 )

def test_playerFirstIA():
    game= moveIt.GameMoveIt(42)
    initPod= game.initialize()

    player= AutonomousPlayer()
    player.wakeUp( 1, 1, initPod )
    player.perceive( game.playerHand(1) )

    test= [
"          ▁         ▁         ▁         ▁         ▁         ▁     ",
"       ▖▝   ▘▗   ▖▝   ▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗  ",
"     █ ⎡     ⎤ █         ███████████         █         █         █",
"     █ ⎣     ⎦1█         ███████████         █         █         █",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝  ",
"█         █         █         █         ███████████         █     ",
"█         █         █         █         ███████████         █     ",
"  ▘▗   ▖▝▁▁▁▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝   ▀▜████████▙▄   ▖▝   ▘▗  ",
"     █  ⎛R  ⎞  ███████████         █         ███████████         █",
"     █  ⎝  1⎠  ███████████         █         ███████████         █",
"  ▄▟███▙▄▔▔▔▖▝   ▀▜███▛▀   ▘▗   ▄▟███▙▄   ▖▝▁▁▁▀▜███▛▀▁▁▁▘▗   ▖▝  ",
"███████████         █         ███████████  ⎛H  ⎞  █  ⎛H  ⎞  █     ",
"███████████         █         ███████████  ⎝  3⎠  █  ⎝  2⎠  █     ",
"  ▀▜███▛▀   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗▔▔▔▖▝   ▘▗▔▔▔▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]

    debug( player._board.shell() )
    for l1, l2 in zip( player._board.shell().split("\n"), test ) :
        assert( l1 == l2)

    assert( len(player._mobiles) == 3 )
    assert( str( player._mobiles[0] ) == "Robot-1[on(0, 1), dir(0), goal(0, 3)-F, error(0.0)]" )
    assert( str( player._mobiles[1] ) == "Human-2[on(5, 0), dir(0), error(0.0)]" )
    assert( str( player._mobiles[2] ) == "Human-3[on(4, 0), dir(0), error(0.0)]" )

    assert( player._countTic == 16 )
    assert( player._countCycle == 10 )
    assert( player._score == 0 )

    assert( player.decide() == "move 1" )

    for i in range(6) :
        player.perceive( game.playerHand(1) )
        game.applyPlayerAction(1, player.decide())
        game.tic()

def test_playerFirstIA_multiRobot():
    game= moveIt.GameMoveIt(42, numberOfRobots= 3, numberOfHuman=1)
    initPod= game.initialize()

    player= AutonomousPlayer()
    player.wakeUp( 1, 1, initPod )
    player.perceive( game.playerHand(1) )

    test= [
"          ▁         ▁         ▁         ▁         ▁         ▁     ",
"       ▖▝   ▘▗   ▖▝   ▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗  ",
"     █ ⎡     ⎤ █         ███████████         █         █         █",
"     █ ⎣     ⎦1█         ███████████         █         █         █",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗   ▄▟███▙▄   ▖▝▁▁▁▘▗   ▖▝  ",
"█         █         █         █         ███████████  ⎛H  ⎞  █     ",
"█         █         █         █         ███████████  ⎝  4⎠  █     ",
"  ▘▗   ▖▝▁▁▁▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝   ▀▜████████▙▄▔▔▔▖▝   ▘▗  ",
"     █  ⎛R  ⎞  ███████████         █         ███████████         █",
"     █  ⎝  1⎠  ███████████         █         ███████████         █",
"  ▄▟███▙▄▔▔▔▖▝   ▀▜███▛▀   ▘▗   ▄▟███▙▄   ▖▝▁▁▁▀▜███▛▀▁▁▁▘▗   ▖▝  ",
"███████████ ⎡     ⎤ █ ⎡     ⎤ ███████████  ⎛R  ⎞  █  ⎛R  ⎞  █     ",
"███████████ ⎣     ⎦3█ ⎣     ⎦2███████████  ⎝  3⎠  █  ⎝  2⎠  █     ",
"  ▀▜███▛▀   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗▔▔▔▖▝   ▘▗▔▔▔▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]

    debug( game._board.shell() )
    debug( player._board.shell() )
    for l1, l2 in zip( player._board.shell().split("\n"), test ) :
        assert( l1 == l2)

    assert( len(player._mobiles) == 4 )
    assert( str( player._mobiles[0] ) == "Robot-1[on(0, 1), dir(0), goal(0, 3)-F, error(0.0)]" )
    assert( str( player._mobiles[1] ) == "Robot-2[on(5, 0), dir(0), goal(2, 0)-F, error(0.0)]" )
    assert( str( player._mobiles[2] ) == "Robot-3[on(4, 0), dir(0), goal(1, 0)-F, error(0.0)]" )
    assert( str( player._mobiles[3] ) == "Human-4[on(5, 2), dir(0), error(0.0)]" )

    assert( player._countTic == 16 )
    assert( player._countCycle == 10 )
    assert( player._score == 0 )

    assert( player.decide() == "move 1 5 6" )

    for i in range(6) :
        player.perceive( game.playerHand(1) )
        game.applyPlayerAction(1, player.decide())
        game.tic()