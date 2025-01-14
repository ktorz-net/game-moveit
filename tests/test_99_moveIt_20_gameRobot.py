import sys, pathlib, random
workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

"""
Test - MoveIt Games Class
"""

import src.hacka.core as hk
import src.hacka.games.moveIt as moveIt

def debug( aString ):
    print("<--")
    for line in aString.split("\n") :
        print( '"'+ line + '",')
    print("-->")

def test_construct():
    game= moveIt.GameMoveIt()
    
    #debug( game.board().shell() )
    test= [
"          ▁         ▁         ▁         ▁         ▁         ▁     ",
"       ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗  ",
"     █         █         █         █         █         █         █",
"     █         █         █         █         █         █         █",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝  ",
"█         █         █         █         █         █         █     ",
"█         █         █         █         █         █         █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗  ",
"     █         █         █         █         █         █         █",
"     █         █         █         █         █         █         █",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝  ",
"█         █         █         █         █         █         █     ",
"█         █         █         █         █         █         █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]

    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)

    for i, robot in zip( range(3), game.mobiles() ) :
         assert( robot.position() == ( i%6, i//6 ) )
         assert( robot.goal() == ( i%6, i//6 ) )

def test_initialize():
    game= moveIt.GameMoveIt(42, numberOfRobots=3, numberOfHuman=0, defective=False, numberOfObstacles=0)
    game.initialize()
    
    #debug( game.board().shell() )
    test= [
"          ▁         ▁         ▁         ▁         ▁         ▁     ",
"       ▖▝   ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗  ",
"     █         █         █  ⎛R  ⎞  █         █         █ ⎡     ⎤ █",
"     █         █         █  ⎝  1⎠  █         █         █ ⎣     ⎦1█",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗▔▔▔▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝  ",
"█         █         █         █         █         █         █     ",
"█         █         █         █         █         █         █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗  ",
"     █         █ ⎡     ⎤ █ ⎡     ⎤ █         █         █         █",
"     █         █ ⎣     ⎦3█ ⎣     ⎦2█         █         █         █",
"  ▖▝▁▁▁▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝  ",
"█  ⎛R  ⎞  █         █         █  ⎛R  ⎞  █         █         █     ",
"█  ⎝  3⎠  █         █         █  ⎝  2⎠  █         █         █     ",
"  ▘▗▔▔▔▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗▔▔▔▖▝   ▘▗   ▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]

    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)

def test_initialize2():
    game= moveIt.GameMoveIt(42, numberOfRobots=3, numberOfHuman=0, defective=False)
    podInit= game.initialize()
    
    #debug( game.board().shell() )
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
"███████████ ⎡     ⎤ █ ⎡     ⎤ ███████████  ⎛R  ⎞  █  ⎛R  ⎞  █     ",
"███████████ ⎣     ⎦3█ ⎣     ⎦2███████████  ⎝  3⎠  █  ⎝  2⎠  █     ",
"  ▀▜███▛▀   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗▔▔▔▖▝   ▘▗▔▔▔▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]

    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)


def test_wakeUp():
    game= moveIt.GameMoveIt(42, numberOfRobots=3, numberOfHuman=0, defective=0.3)
    podInit= game.initialize()
    
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
"███████████ ⎡     ⎤ █ ⎡     ⎤ ███████████  ⎛R  ⎞  █  ⎛R  ⎞  █     ",
"███████████ ⎣     ⎦3█ ⎣     ⎦2███████████  ⎝  3⎠  █  ⎝  2⎠  █     ",
"  ▀▜███▛▀   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗▔▔▔▖▝   ▘▗▔▔▔▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]

    #debug( game.board().shell() )
    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)

    #assert( game.mobile(1).error() == 0.1 )
    #assert( game.mobile(2).error() == 0.2 )
    #assert( game.mobile(3).error() == 0.1 )

    test= [
"MoveIt: [6, 4, 3, 3]",
"- Line:",
"  - Cell: OBSTACLE",
"  - Cell: FREE",
"  - Cell: FREE",
"  - Cell: OBSTACLE",
"  - Cell: FREE",
"  - Cell: FREE",
"- Line:",
"  - Cell: FREE",
"  - Cell: OBSTACLE",
"  - Cell: FREE",
"  - Cell: FREE",
"  - Cell: OBSTACLE",
"  - Cell: FREE",
"- Line:",
"  - Cell: FREE",
"  - Cell: FREE",
"  - Cell: FREE",
"  - Cell: FREE",
"  - Cell: OBSTACLE",
"  - Cell: FREE",
"- Line:",
"  - Cell: FREE",
"  - Cell: FREE",
"  - Cell: OBSTACLE",
"  - Cell: FREE",
"  - Cell: FREE",
"  - Cell: FREE"
]

    #debug( str(podInit) )
    for l1, l2 in zip( str(podInit).split("\n"), test ) :
        assert( l1 == l2)
    
    hand= game.playerHand(1)

    robots= [ moveIt.Mobile(i+1) for i in range( len(hand.children()) ) ] 
    for robot, pod in zip( robots, hand.children() ) :
        robot.fromPod(pod)
    
    assert( len( robots ) == 3 )
    assert( str(robots[0]) == "Robot-1[on(0, 1), dir(0), goal(0, 3)-F, error(0.0)]" )
    assert( str(robots[1]) == "Robot-2[on(5, 0), dir(0), goal(2, 0)-F, error(0.0)]" )
    assert( str(robots[2]) == "Robot-3[on(4, 0), dir(0), goal(1, 0)-F, error(0.0)]" )

    for robot in game.mobiles() :
        random.seed(1245)
        x, y = random.choice( game.board().cellsEmpty() )
        print( f"Move {robot} to {(x, y)}" )
        assert( game.board().teleportMobile( robot.x(), robot.y(), x, y ) )

    test= [
"          ▁         ▁         ▁         ▁         ▁         ▁     ",
"       ▖▝   ▘▗   ▖▝   ▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗  ",
"     █ ⎡     ⎤ █         ███████████         █         █         █",
"     █ ⎣     ⎦1█         ███████████         █         █         █",
"  ▖▝   ▘▗   ▖▝▁▁▁▘▗   ▖▝▁▁▁▀▜███▛▀▁▁▁▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝  ",
"█         █  ⎛R  ⎞  █  ⎛R  ⎞  █  ⎛R  ⎞  ███████████         █     ",
"█         █  ⎝  3⎠  █  ⎝  2⎠  █  ⎝  1⎠  ███████████         █     ",
"  ▘▗   ▖▝   ▘▗▔▔▔▄▟███▙▄▔▔▔▖▝   ▘▗▔▔▔▖▝   ▀▜████████▙▄   ▖▝   ▘▗  ",
"     █         ███████████         █         ███████████         █",
"     █         ███████████         █         ███████████         █",
"  ▄▟███▙▄   ▖▝   ▀▜███▛▀   ▘▗   ▄▟███▙▄   ▖▝   ▀▜███▛▀   ▘▗   ▖▝  ",
"███████████ ⎡     ⎤ █ ⎡     ⎤ ███████████         █         █     ",
"███████████ ⎣     ⎦3█ ⎣     ⎦2███████████         █         █     ",
"  ▀▜███▛▀   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗   ▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]
    
    #debug( game.board().shell() )
    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)

    game.board().mobilesFromPod( hand )
    
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
"███████████ ⎡     ⎤ █ ⎡     ⎤ ███████████  ⎛R  ⎞  █  ⎛R  ⎞  █     ",
"███████████ ⎣     ⎦3█ ⎣     ⎦2███████████  ⎝  3⎠  █  ⎝  2⎠  █     ",
"  ▀▜███▛▀   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗▔▔▔▖▝   ▘▗▔▔▔▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]
    

    #debug( game.board().shell() )
    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)

    #assert( str(game.mobile(1)) == "Robot-1[on(0, 1), dir(0), goal(0, 3)-F, error(0.0)]" )
    #assert( str(game.mobile(2)) == "Robot-2[on(5, 0), dir(0), goal(2, 0)-F, error(0.0)]" )
    #assert( str(game.mobile(3)) == "Robot-3[on(0, 0), dir(0), goal(3, 1)-F, error(0.0)]" )

def test_actionsOk():
    game= moveIt.GameMoveIt(42, numberOfRobots=3, numberOfHuman=0, defective=False)
    game.initialize()
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
"███████████ ⎡     ⎤ █ ⎡     ⎤ ███████████  ⎛R  ⎞  █  ⎛R  ⎞  █     ",
"███████████ ⎣     ⎦3█ ⎣     ⎦2███████████  ⎝  3⎠  █  ⎝  2⎠  █     ",
"  ▀▜███▛▀   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗▔▔▔▖▝   ▘▗▔▔▔▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]

    #debug( game.board().shell() )
    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)

    assert( game.mobile(1).direction() == 0 )
    assert( game.mobile(2).direction() == 0 )
    assert( game.mobile(3).direction() == 0 )

    game.applyPlayerAction( 1, "move 1 0 6" )
    game.tic()
    
    test= [
"          ▁         ▁         ▁         ▁         ▁         ▁     ",
"       ▖▝   ▘▗   ▖▝   ▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗  ",
"     █ ⎡     ⎤ █         ███████████         █         █         █",
"     █ ⎣     ⎦1█         ███████████         █         █         █",
"  ▖▝   ▘▗   ▖▝▁▁▁▘▗   ▖▝   ▀▜███▛▀   ▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝  ",
"█         █  ⎛R  ⎞  █         █         ███████████         █     ",
"█         █  ⎝  1⎠  █         █         ███████████         █     ",
"  ▘▗   ▖▝   ▘▗▔▔▔▄▟███▙▄   ▖▝   ▘▗   ▖▝▁▁▁▀▜████████▙▄   ▖▝   ▘▗  ",
"     █         ███████████         █  ⎛R  ⎞  ███████████         █",
"     █         ███████████         █  ⎝  3⎠  ███████████         █",
"  ▄▟███▙▄   ▖▝   ▀▜███▛▀   ▘▗   ▄▟███▙▄▔▔▔▖▝   ▀▜███▛▀▁▁▁▘▗   ▖▝  ",
"███████████ ⎡     ⎤ █ ⎡     ⎤ ███████████         █  ⎛R  ⎞  █     ",
"███████████ ⎣     ⎦3█ ⎣     ⎦2███████████         █  ⎝  2⎠  █     ",
"  ▀▜███▛▀   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗   ▖▝   ▘▗▔▔▔▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]

    debug( game.board().shell() )
    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)

    assert( game.score() == 0 )
    assert( game.mobile(1).direction() == 1 )
    assert( game.mobile(2).direction() == 0 )
    assert( game.mobile(3).direction() == 6 )
    assert( game.mobile(1).isGoalSatisfied() == False )
    assert( game.mobile(2).isGoalSatisfied() == False )
    assert( game.mobile(3).isGoalSatisfied() == False )

    game.applyPlayerAction( 1, "6 5 5" ) # short move
    game.tic()
    
    test= [
"          ▁         ▁         ▁         ▁         ▁         ▁     ",
"       ▖▝▁▁▁▘▗   ▖▝   ▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗  ",
"     █ ⎡⎛R  ⎞⎤ █         ███████████         █         █         █",
"     █ ⎣⎝  1⎠⎦1█         ███████████         █         █         █",
"  ▖▝   ▘▗▔▔▔▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝  ",
"█         █         █         █         ███████████         █     ",
"█         █         █         █         ███████████         █     ",
"  ▘▗   ▖▝   ▘▗   ▄▟███▙▄   ▖▝▁▁▁▘▗   ▖▝   ▀▜████████▙▄   ▖▝   ▘▗  ",
"     █         ███████████  ⎛R  ⎞  █         ███████████         █",
"     █         ███████████  ⎝  3⎠  █         ███████████         █",
"  ▄▟███▙▄   ▖▝   ▀▜███▛▀   ▘▗▔▔▔▄▟███▙▄   ▖▝▁▁▁▀▜███▛▀   ▘▗   ▖▝  ",
"███████████ ⎡     ⎤ █ ⎡     ⎤ ███████████  ⎛R  ⎞  █         █     ",
"███████████ ⎣     ⎦3█ ⎣     ⎦2███████████  ⎝  2⎠  █         █     ",
"  ▀▜███▛▀   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗▔▔▔▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]
    
    #debug( game.board().shell() )
    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)

    assert( game.mobile(1).isGoalSatisfied() == True )
    assert( game.score() == 0 )

    game.applyPlayerAction( 1, "move 2 6 4" )
    game.tic()

    assert( game.mobile(1).isGoalSatisfied() == True )
    assert( game.mobile(2).isGoalSatisfied() == False )
    assert( game.mobile(3).isGoalSatisfied() == False )
    assert( game.score() == 0 )

    game.applyPlayerAction( 1, "move 0 5 5" )
    game.tic()

    assert( game.mobile(1).isGoalSatisfied() == True )
    assert( game.mobile(2).isGoalSatisfied() == False )
    assert( game.mobile(3).isGoalSatisfied() == True )
    assert( game.score() == 0 )

    assert( game._countDownTic == 12 )
    assert( game._countDownCycle == 10 )

    game.applyPlayerAction( 1, "move 0 4 0" )
    game.tic()

    assert( game.mobile(1).isGoalSatisfied() == False )
    assert( game.mobile(2).isGoalSatisfied() == False )
    assert( game.mobile(3).isGoalSatisfied() == False )

    assert( game._countDownTic == 16 )
    assert( game._countDownCycle == 9 )
    assert( game.score() == 12 )

    test= [
"          ▁         ▁         ▁         ▁         ▁         ▁     ",
"       ▖▝   ▘▗   ▖▝▁▁▁▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗  ",
"     █         █  ⎛R  ⎞  ███████████         █         █         █",
"     █         █  ⎝  1⎠  ███████████         █         █         █",
"  ▖▝   ▘▗   ▖▝   ▘▗▔▔▔▖▝   ▀▜███▛▀   ▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝  ",
"█         █         █         █ ⎡     ⎤ ███████████         █     ",
"█         █         █         █ ⎣     ⎦3███████████         █     ",
"  ▘▗   ▖▝   ▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝   ▀▜████████▙▄   ▖▝   ▘▗  ",
"     █         ███████████         █         ███████████ ⎡     ⎤ █",
"     █         ███████████         █         ███████████ ⎣     ⎦1█",
"  ▄▟███▙▄   ▖▝▁▁▁▀▜███▛▀▁▁▁▘▗   ▄▟███▙▄   ▖▝   ▀▜███▛▀   ▘▗   ▖▝  ",
"███████████  ⎛R  ⎞  █  ⎛R  ⎞  ███████████         █         █     ",
"███████████  ⎝  3⎠  █  ⎝  2⎠  ███████████         █         █     ",
"  ▀▜███▛▀   ▘▗▔▔▔▖▝   ▘▗▔▔▔▖▝   ▀▜███▛▀   ▘▗   ▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]
    
    debug( game.board().shell() )
    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)

def test_wrongAction():
    game= moveIt.GameMoveIt(42, numberOfRobots=3, numberOfHuman=0, defective=False)
    game.initialize()
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
"███████████ ⎡     ⎤ █ ⎡     ⎤ ███████████  ⎛R  ⎞  █  ⎛R  ⎞  █     ",
"███████████ ⎣     ⎦3█ ⎣     ⎦2███████████  ⎝  3⎠  █  ⎝  2⎠  █     ",
"  ▀▜███▛▀   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗▔▔▔▖▝   ▘▗▔▔▔▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]

    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)

    game.applyPlayerAction( 1, "move 0 0" )
    game.tic()
    game.applyPlayerAction( 1, "tout pourry" )
    game.tic()
    game.applyPlayerAction( 1, "mov 1 2 3" )
    game.tic()
    game.applyPlayerAction( 1, "move 1 2 8" )
    game.tic()
    game.applyPlayerAction( 1, "move 1 2 3 6" )
    game.tic()

    assert( game._countDownTic == 11 )
    assert( game._countDownCycle == 10 )
    assert( game.score() == 0 )

    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)

def test_collisionEnvironment():
    game= moveIt.GameMoveIt(42, numberOfRobots=3, numberOfHuman=0, defective=False)
    game.initialize()
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
"███████████ ⎡     ⎤ █ ⎡     ⎤ ███████████  ⎛R  ⎞  █  ⎛R  ⎞  █     ",
"███████████ ⎣     ⎦3█ ⎣     ⎦2███████████  ⎝  3⎠  █  ⎝  2⎠  █     ",
"  ▀▜███▛▀   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗▔▔▔▖▝   ▘▗▔▔▔▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]

    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)

    game.applyPlayerAction( 1, "move 2 0 0" )
    game.tic()

    assert( game._countDownTic == 15 )
    assert( game.score() == -160 )

    game.applyPlayerAction( 1, "move 2 6 5" )
    game.tic()

    assert( game._countDownTic == 14 )
    assert( game.score() == -640 )
    
    game.applyPlayerAction( 1, "move 0 4 0" )
    game.tic()

    assert( game._countDownTic == 13 )
    assert( game.score() == -800 )

    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)

def test_collisionRobot1():
    game= moveIt.GameMoveIt(42, numberOfRobots=3, numberOfHuman=0, defective=False)
    game.initialize()
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
"███████████ ⎡     ⎤ █ ⎡     ⎤ ███████████  ⎛R  ⎞  █  ⎛R  ⎞  █     ",
"███████████ ⎣     ⎦3█ ⎣     ⎦2███████████  ⎝  3⎠  █  ⎝  2⎠  █     ",
"  ▀▜███▛▀   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗▔▔▔▖▝   ▘▗▔▔▔▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]

    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)

    assert( game.score() == 0 )
    game.applyPlayerAction( 1, "move 0 5 0" )
    game.tic()
    assert( game.score() == -160 )

    game.applyPlayerAction( 1, "move 0 5 2" )
    game.tic()
    assert( game.score() == -480 )

    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)

    game.applyPlayerAction( 1, "move 0 5 6" )
    game.tic()
    assert( game.score() == -640 )

    test= [
"          ▁         ▁         ▁         ▁         ▁         ▁     ",
"       ▖▝   ▘▗   ▖▝   ▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗  ",
"     █ ⎡     ⎤ █         ███████████         █         █         █",
"     █ ⎣     ⎦1█         ███████████         █         █         █",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝  ",
"█         █         █         █         ███████████         █     ",
"█         █         █         █         ███████████         █     ",
"  ▘▗   ▖▝▁▁▁▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝▁▁▁▀▜████████▙▄   ▖▝   ▘▗  ",
"     █  ⎛R  ⎞  ███████████         █  ⎛R  ⎞  ███████████         █",
"     █  ⎝  1⎠  ███████████         █  ⎝  3⎠  ███████████         █",
"  ▄▟███▙▄▔▔▔▖▝   ▀▜███▛▀   ▘▗   ▄▟███▙▄▔▔▔▖▝   ▀▜███▛▀▁▁▁▘▗   ▖▝  ",
"███████████ ⎡     ⎤ █ ⎡     ⎤ ███████████         █  ⎛R  ⎞  █     ",
"███████████ ⎣     ⎦3█ ⎣     ⎦2███████████         █  ⎝  2⎠  █     ",
"  ▀▜███▛▀   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗   ▖▝   ▘▗▔▔▔▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]

    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)

def test_collisionRobot2():
    game= moveIt.GameMoveIt(42, numberOfRobots=3, numberOfHuman=0, defective=False)
    game.initialize()

    game.applyPlayerAction( 1, "move 1 0 6" )
    game.tic()
    game.applyPlayerAction( 1, "move 2 0 0" )
    game.tic()

    test= [
"          ▁         ▁         ▁         ▁         ▁         ▁     ",
"       ▖▝   ▘▗   ▖▝   ▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗  ",
"     █ ⎡     ⎤ █         ███████████         █         █         █",
"     █ ⎣     ⎦1█         ███████████         █         █         █",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▀▜███▛▀   ▘▗   ▄▟███▙▄   ▖▝   ▘▗   ▖▝  ",
"█         █         █  ⎛R  ⎞  █         ███████████         █     ",
"█         █         █  ⎝  1⎠  █         ███████████         █     ",
"  ▘▗   ▖▝   ▘▗   ▄▟███▙▄▔▔▔▖▝   ▘▗   ▖▝▁▁▁▀▜████████▙▄   ▖▝   ▘▗  ",
"     █         ███████████         █  ⎛R  ⎞  ███████████         █",
"     █         ███████████         █  ⎝  3⎠  ███████████         █",
"  ▄▟███▙▄   ▖▝   ▀▜███▛▀   ▘▗   ▄▟███▙▄▔▔▔▖▝   ▀▜███▛▀▁▁▁▘▗   ▖▝  ",
"███████████ ⎡     ⎤ █ ⎡     ⎤ ███████████         █  ⎛R  ⎞  █     ",
"███████████ ⎣     ⎦3█ ⎣     ⎦2███████████         █  ⎝  2⎠  █     ",
"  ▀▜███▛▀   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗   ▖▝   ▘▗▔▔▔▖▝       ",
"     ▔         ▔         ▔         ▔         ▔         ▔          "]

    #debug( game.board().shell() )
    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)

    game.applyPlayerAction( 1, "move 2 0 6" )
    game.tic()

    assert( game.score() == -320 )

    debug( game.board().shell() )
    for l1, l2 in zip( game.board().shell().split("\n"), test ) :
        assert( l1 == l2)
