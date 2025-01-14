import sys, pathlib
workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

"""
Test - MoveIt Games Class
"""

import src.hacka.core as hk
import src.hacka.games.moveIt as moveIt

def test_Robot():
    board= moveIt.Hexaboard(4, 3)
    assert( type( board ) is moveIt.Hexaboard  )
    assert( board.size() == (4, 3) )

    board.at(2, 1).setObstacle()
    assert( board.setMobile_at( moveIt.Mobile(12, hidenGoal=False), 1, 1) == True )
    assert( board.setMobile_at( moveIt.Mobile(1, hidenGoal=False), 1, 1) == False )
    assert( board.setMobile_at( moveIt.Mobile(1, hidenGoal=False), 2, 1) == False )

    #print( board.shell() )
    test= [
"     ▁         ▁         ▁         ▁          ",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗       ",
"█         █         █         █         █     ",
"█         █         █         █         █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗   ▄▟███▙▄   ▖▝   ▘▗  ",
"     █         █  ⎛R  ⎞  ███████████         █",
"     █         █  ⎝ 12⎠  ███████████         █",
"  ▖▝   ▘▗   ▖▝   ▘▗▔▔▔▖▝   ▀▜███▛▀   ▘▗   ▖▝  ",
"█ ⎡     ⎤1█         █         █         █     ",
"█ ⎣     ⎦2█         █         █         █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔          "]
    for l1, l2 in zip( board.shell().split("\n"), test ) :
        assert( l1 == l2 )

    r8= moveIt.Mobile(8)
    r8.setGoal(1,1)
    assert( board.setMobile_at( r8, 3, 2) == True )

    #print( board.shell() )
    test= [
"     ▁         ▁         ▁         ▁          ",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗       ",
"█         █         █         █  ⎛R  ⎞  █     ",
"█         █         █         █  ⎝  8⎠  █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗   ▄▟███▙▄▔▔▔▖▝   ▘▗  ",
"     █         █ ⎡⎛R  ⎞⎤ ███████████         █",
"     █         █ ⎣⎝ 12⎠⎦8███████████         █",
"  ▖▝   ▘▗   ▖▝   ▘▗▔▔▔▖▝   ▀▜███▛▀   ▘▗   ▖▝  ",
"█ ⎡     ⎤1█         █         █         █     ",
"█ ⎣     ⎦2█         █         █         █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔          "]
    for l1, l2 in zip( board.shell().split("\n"), test ) :
        assert( l1 == l2 )
    
    board.at(1, 1).removeMobile()

    #print( board.shell() )
    test= [
"     ▁         ▁         ▁         ▁          ",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗       ",
"█         █         █         █  ⎛R  ⎞  █     ",
"█         █         █         █  ⎝  8⎠  █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▄▟███▙▄▔▔▔▖▝   ▘▗  ",
"     █         █ ⎡     ⎤ ███████████         █",
"     █         █ ⎣     ⎦8███████████         █",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀   ▘▗   ▖▝  ",
"█         █         █         █         █     ",
"█         █         █         █         █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔          "]
    for l1, l2 in zip( board.shell().split("\n"), test ) :
        assert( l1 == l2 )

def test_move():
    board= moveIt.Hexaboard(4, 3)
    assert( type( board ) is moveIt.Hexaboard  )
    assert( board.size() == (4, 3) )

    board.at(3, 1).setObstacle()
    board.setMobile_at( moveIt.Mobile(1, hidenGoal= False), 1, 1 )
    
    #print( board.shell() )
    test= [
"     ▁         ▁         ▁         ▁          ",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗       ",
"█         █         █         █         █     ",
"█         █         █         █         █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗   ▖▝   ▘▗   ▄▟███▙▄  ",
"     █         █  ⎛R  ⎞  █         ███████████",
"     █         █  ⎝  1⎠  █         ███████████",
"  ▖▝   ▘▗   ▖▝   ▘▗▔▔▔▖▝   ▘▗   ▖▝   ▀▜███▛▀  ",
"█ ⎡     ⎤ █         █         █         █     ",
"█ ⎣     ⎦1█         █         █         █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔          "]
    for l1, l2 in zip( board.shell().split("\n"), test ) :
        assert( l1 == l2 )

    dirs= []
    for i in range(7):
        dirs.append( board.at_dir( 0, 0, i ) )
    assert( dirs == [(0, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 0), (-1, 1)] )

    dirs= []
    for i in range(7):
        dirs.append( board.at_dir( 3, 2, i ) )
    assert( dirs == [(3, 2), (3, 3), (4, 2), (3, 1), (2, 1), (2, 2), (2, 3)] )

    dirs= []
    for i in range(7):
        dirs.append( board.at_dir( 1, 1, i ) )
    assert( dirs == [(1, 1), (2, 2), (2, 1), (2, 0), (1, 0), (0, 1), (1, 2)] )

    assert( board.at_dir(1, 1, 4) == (1, 0) )

    assert( board.movesFrom(1, 1) == [0, 1, 2, 3, 4, 5, 6] )
    assert( board.at_dir(1, 1, 4) == (1, 0) )
    assert( board.moveMobileAt_dir(1, 1, 4) == True )
    assert( board.movesFrom(1, 0) == [0, 1, 2, 5, 6] )
    assert( board.moveMobileAt_dir(1, 0, 5) == True )
    assert( board.movesFrom(0, 0) == [0, 1, 2] )

    #print( board.shell() )
    test= [
"     ▁         ▁         ▁         ▁          ",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗       ",
"█         █         █         █         █     ",
"█         █         █         █         █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▄▟███▙▄  ",
"     █         █         █         ███████████",
"     █         █         █         ███████████",
"  ▖▝▁▁▁▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀  ",
"█ ⎡⎛R  ⎞⎤ █         █         █         █     ",
"█ ⎣⎝  1⎠⎦1█         █         █         █     ",
"  ▘▗▔▔▔▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔          "]
    for l1, l2 in zip( board.shell().split("\n"), test ) :
        assert( l1 == l2 )

    assert( board.moveMobileAt_dir(0, 0, 0) == True )
    assert( board.moveMobileAt_dir(0, 0, 5) == False )
    assert( board.moveMobileAt_dir(1, 1, 5) == False )

    robot= board.at(0, 0).removeMobile()
    board.setMobile_at(robot, 3, 2)

    #print( board.shell() )
    test= [
"     ▁         ▁         ▁         ▁          ",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗       ",
"█         █         █         █  ⎛R  ⎞  █     ",
"█         █         █         █  ⎝  1⎠  █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗▔▔▔▄▟███▙▄  ",
"     █         █         █         ███████████",
"     █         █         █         ███████████",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▀▜███▛▀  ",
"█ ⎡     ⎤ █         █         █         █     ",
"█ ⎣     ⎦1█         █         █         █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔          "]
    for l1, l2 in zip( board.shell().split("\n"), test ) :
        assert( l1 == l2 )

    assert( board.at_dir(3, 2, 3) == (3, 1) )
    assert( board.at(3, 1).isObstacle() )
    assert( board.movesFrom(3, 2) == [0, 4, 5] )

def test_multi():
    board= moveIt.Hexaboard(4, 3)
    assert( type( board ) is moveIt.Hexaboard  )
    assert( board.size() == (4, 3) )

    board.at(3, 1).setObstacle()
    board.setMobile_at( moveIt.Mobile(1), 1, 1 )
    board.at(1, 1).mobile().setGoal(0, 0)
    board.setMobile_at( moveIt.Mobile(2), 2, 2 )
    board.at(2, 2).mobile().setGoal(3, 0)
    
    test= [
"     ▁         ▁         ▁         ▁          ",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗   ▖▝   ▘▗       ",
"█         █         █  ⎛R  ⎞  █         █     ",
"█         █         █  ⎝  2⎠  █         █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗▔▔▔▖▝   ▘▗   ▄▟███▙▄  ",
"     █         █  ⎛R  ⎞  █         ███████████",
"     █         █  ⎝  1⎠  █         ███████████",
"  ▖▝   ▘▗   ▖▝   ▘▗▔▔▔▖▝   ▘▗   ▖▝   ▀▜███▛▀  ",
"█ ⎡     ⎤ █         █         █ ⎡     ⎤ █     ",
"█ ⎣     ⎦1█         █         █ ⎣     ⎦2█     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔          "]
    print( board.shell() )
    for l1, l2 in zip( board.shell().split("\n"), test ) :
        assert( l1 == l2 )

    options= board.cellsEmpty()
    assert( options == [(0, 0), (1, 0), (2, 0), (3, 0),
                         (0, 1), (2, 1),
                          (0, 2), (1, 2), (3, 2) ] )

    assert( board.movesFrom(1, 1) == [0, 1, 2, 3, 4, 5, 6] )
    assert( board.movesFrom(2, 2) == [0, 2, 3, 4, 5] )

    assert( board.moveMobileAt_dir(1, 1, 1) == False )
    assert( board.moveMobileAt_dir(2, 2, 3) == True )

    assert( board.moveMobileAt_dir(1, 1, 1) == True )
    assert( board.moveMobileAt_dir(2, 1, 6) == False )

    
    #print( board.shell() )
    test= [
"     ▁         ▁         ▁         ▁          ",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗   ▖▝   ▘▗       ",
"█         █         █  ⎛R  ⎞  █         █     ",
"█         █         █  ⎝  1⎠  █         █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗▔▔▔▖▝▁▁▁▘▗   ▄▟███▙▄  ",
"     █         █         █  ⎛R  ⎞  ███████████",
"     █         █         █  ⎝  2⎠  ███████████",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗▔▔▔▖▝   ▀▜███▛▀  ",
"█ ⎡     ⎤ █         █         █ ⎡     ⎤ █     ",
"█ ⎣     ⎦1█         █         █ ⎣     ⎦2█     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔          "]
    for l1, l2 in zip( board.shell().split("\n"), test ) :
        assert( l1 == l2 )
    
    assert( board.multiMoveRobots( [[2, 2, 4], [2, 1, 1]] ) == 0 )

    #print( board.shell() )
    test= [
"     ▁         ▁         ▁         ▁          ",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗       ",
"█         █         █         █  ⎛R  ⎞  █     ",
"█         █         █         █  ⎝  2⎠  █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗   ▖▝   ▘▗▔▔▔▄▟███▙▄  ",
"     █         █  ⎛R  ⎞  █         ███████████",
"     █         █  ⎝  1⎠  █         ███████████",
"  ▖▝   ▘▗   ▖▝   ▘▗▔▔▔▖▝   ▘▗   ▖▝   ▀▜███▛▀  ",
"█ ⎡     ⎤ █         █         █ ⎡     ⎤ █     ",
"█ ⎣     ⎦1█         █         █ ⎣     ⎦2█     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔          "]
    for l1, l2 in zip( board.shell().split("\n"), test ) :
        assert( l1 == l2 )

    assert( board.multiMoveRobots( [[1, 1, 1], [3, 2, 5]] ) == 2 )

    print( board.shell() )
    test= [
"     ▁         ▁         ▁         ▁          ",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗       ",
"█         █         █         █  ⎛R  ⎞  █     ",
"█         █         █         █  ⎝  2⎠  █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗   ▖▝   ▘▗▔▔▔▄▟███▙▄  ",
"     █         █  ⎛R  ⎞  █         ███████████",
"     █         █  ⎝  1⎠  █         ███████████",
"  ▖▝   ▘▗   ▖▝   ▘▗▔▔▔▖▝   ▘▗   ▖▝   ▀▜███▛▀  ",
"█ ⎡     ⎤ █         █         █ ⎡     ⎤ █     ",
"█ ⎣     ⎦1█         █         █ ⎣     ⎦2█     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔          "]
    for l1, l2 in zip( board.shell().split("\n"), test ) :
        assert( l1 == l2 )

def test_error():
    board= moveIt.Hexaboard(4, 3)
    assert( type( board ) is moveIt.Hexaboard  )
    assert( board.size() == (4, 3) )

    board.at(3, 1).setObstacle()
    r1= moveIt.Mobile(1)
    board.setMobile_at(r1, 1, 1)

    assert( str(r1) == "Robot-1[on(1, 1), dir(0), error(0.0)]" )
    
    #print( board.shell() )
    test= [
"     ▁         ▁         ▁         ▁          ",
"  ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗       ",
"█         █         █         █         █     ",
"█         █         █         █         █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝▁▁▁▘▗   ▖▝   ▘▗   ▄▟███▙▄  ",
"     █         █  ⎛R  ⎞  █         ███████████",
"     █         █  ⎝  1⎠  █         ███████████",
"  ▖▝   ▘▗   ▖▝   ▘▗▔▔▔▖▝   ▘▗   ▖▝   ▀▜███▛▀  ",
"█         █         █         █         █     ",
"█         █         █         █         █     ",
"  ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝   ▘▗   ▖▝       ",
"     ▔         ▔         ▔         ▔          "]
    for l1, l2 in zip( board.shell().split("\n"), test ) :
        assert( l1 == l2 )
    
    r1.setError(0.2)
    reach= {}
    for i in range(10000) :
        x, y= r1.position()
        board.teleportMobile(x, y, 1, 1)
        board.moveMobileAt_dir(1, 1, 4)
        coord= r1.position()
        coord= coord[0]*100+coord[1]
        if coord not in reach :
            reach[coord]= 0
        reach[coord]+= 1
    
    print(reach)
    assert( len(reach) == 7 )
    for g in reach :
        if g == 100 :
            assert( round(reach[g]/10000, 1) == 0.8 )
        else :
            assert( 230 < reach[g] and reach[g] < 350 )
