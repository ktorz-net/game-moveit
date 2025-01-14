import sys, pathlib
workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

"""
Test - MoveIt Games Class
"""

import src.hacka.core as hk
import src.hacka.games.moveIt as moveIt

def test_robotAsPod():
    board= moveIt.Hexaboard(4, 3)
    board.at(2, 1).setObstacle()

    board.setMobile_at( moveIt.Mobile(1, hidenGoal=False), 1, 1)
    board.setMobile_at( moveIt.Mobile(2, hidenGoal=False), 3, 2)
    board.at( 3, 2 ).mobile().setGoal(1,1)

    print( board.shell() )
    test= [
"     ▁         ▁         ▁         ▁          ",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗       ",
"█         █         █         █  ⎛R  ⎞  █     ",
"█         █         █         █  ⎝  2⎠  █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗   ▄▟███▙▄▔▔▔▖▝   ▘▗  ",
"     █         █ ⎡⎛R  ⎞⎤ ███████████         █",
"     █         █ ⎣⎝  1⎠⎦2███████████         █",
"  ▖▝   ▘▗   ▖▝   ▘▗▔▔▔▖▝   ▀▜███▛▀   ▘▗   ▖▝  ",
"█ ⎡     ⎤ █         █         █         █     ",
"█ ⎣     ⎦1█         █         █         █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔          "]
    for l1, l2 in zip( board.shell().split("\n"), test ) :
        assert( l1 == l2 )
    
    assert( str(board.at( 1, 1 ).mobile().asPod()) == "Mobile: 1 [1, 1, 0, 0, 0, 0]" )
    assert( str(board.at( 3, 2 ).mobile().asPod()) == "Mobile: 2 [3, 2, 0, 1, 1, 0]" )

    assert( str(board.at( 3, 2 ).mobile().asPod()) == "Mobile: 2 [3, 2, 0, 1, 1, 0]" )

def test_RobotFromPod():
    r12= moveIt.Mobile(12, 3, 4)
    r12.setGoal(2, 7)

    assert( str(r12) == "Robot-12[on(3, 4), dir(0), goal(2, 7)-F, error(0.0)]" )
    assert( str(r12.asPod()) == "Mobile: 12 [3, 4, 0, 2, 7, 0]" )
    r12.fromPod( hk.Pod( "Robot", "21", [1, 9, 4, 5, 8, 1] ) )
    assert( str(r12.asPod()) == "Mobile: 21 [1, 9, 4, 5, 8, 1]" )

    r12.setError(0.1)
    assert( str(r12) == "Robot-21[on(1, 9), dir(4), goal(5, 8)-T, error(0.1)]" )
    r12.fromPod( hk.Pod( "Robot", "12", [3, 4, 0, 2, 7, 0] ) )
    assert( str(r12) == "Robot-12[on(3, 4), dir(0), goal(2, 7)-F, error(0.1)]" )

def test_boardAsPod():
    board= moveIt.Hexaboard(4, 3)
    board.at(2, 1).setObstacle()

    board.setMobile_at( moveIt.Mobile(1, hidenGoal=False), 1, 1)
    board.setMobile_at( moveIt.Mobile(2, hidenGoal=False), 3, 2)
    board.at( 3, 2 ).mobile().setGoal(1, 1)

    print( board.shell() )
    test= [
"     ▁         ▁         ▁         ▁          ",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗       ",
"█         █         █         █  ⎛R  ⎞  █     ",
"█         █         █         █  ⎝  2⎠  █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗   ▄▟███▙▄▔▔▔▖▝   ▘▗  ",
"     █         █ ⎡⎛R  ⎞⎤ ███████████         █",
"     █         █ ⎣⎝  1⎠⎦2███████████         █",
"  ▖▝   ▘▗   ▖▝   ▘▗▔▔▔▖▝   ▀▜███▛▀   ▘▗   ▖▝  ",
"█ ⎡     ⎤ █         █         █         █     ",
"█ ⎣     ⎦1█         █         █         █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔          "]
    
    for l1, l2 in zip( board.shell().split("\n"), test ) :
        assert( l1 == l2 )

    print( board.asPod() )
    test= [
"Board: [4, 3]",
"- Line:",
"  - Cell: FREE",
"  - Cell: FREE",
"  - Cell: FREE",
"  - Cell: FREE",
"- Line:",
"  - Cell: FREE",
"  - Cell: FREE",
"  - Cell: OBSTACLE",
"  - Cell: FREE",
"- Line:",
"  - Cell: FREE",
"  - Cell: FREE",
"  - Cell: FREE",
"  - Cell: FREE" ]

    for l1, l2 in zip( str(board.asPod()).split("\n"), test ) :
        assert( l1 == l2 )


def test_boardFromPod():
    board= moveIt.Hexaboard()

    pod= hk.Pod( "Board", "", [3, 2] )
    podLine= hk.Pod( "Line" )
    podLine.append( hk.Pod( "Cell", "FREE" ) )
    podLine.append( hk.Pod( "Cell", "OBSTACLE" ) )
    podLine.append( hk.Pod( "Cell", "FREE" ) )
    pod.append(podLine)
    podLine= hk.Pod( "Line" )
    podLine.append( hk.Pod( "Cell", "FREE" ) )
    podLine.append( hk.Pod( "Cell", "FREE" ) )
    podLine.append( hk.Pod( "Cell", "OBSTACLE" ) )
    pod.append(podLine)

    board.fromPod( pod )

    print( board.shell() )
    test= [
"          ▁         ▁         ▁     ",
"       ▖▝   ▘▗   ▖▝   ▘▗   ▄▟███▙▄  ",
"     █         █         ███████████",
"     █         █         ███████████",
"  ▖▝   ▘▗   ▄▟███▙▄   ▖▝   ▀▜███▛▀  ",
"█         ███████████         █     ",
"█         ███████████         █     ",
"  ▘▗   ▖▝   ▀▜███▛▀   ▘▗   ▖▝       ",
"     ▔         ▔         ▔          "]
    
    for l1, l2 in zip( board.shell().split("\n"), test ) :
        assert( l1 == l2 )
