import sys, pathlib

import hacka.pylib  as hacka
import hacka.artist as hartist
import hacka.tiled  as htiled

"""
Test - MoveIt Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.hacka.games.moveit as mi

def test_moveIt_board():
    # Game MoveIt:
    game= mi.GameMaster( 38 )
    matrix= [
        [00, 00, 00, -1, 00, 00, 00, 00, 00, 00],
        [00, -1, 00, 00, 00, -1, 00, -1, -1, 00],
        [00, 00, 00, -1, 00, 00, 00, -1, 00, 00],
        [00, 00, 00, -1, 00, 00, 00, 00, 00, 00],
        [00, -1, 00, 00, 00, -1, 00, -1, -1, -1],
        [00, -1, 00, -1, 00, 00, 00, -1, -1, -1],
        [00, 00, 00, 00, 00, -1, 00, -1, -1, -1]
    ]
    game.initializeBoardGrid( matrix, 0.9, 0.1 )
    game.render()

    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-board-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    game.popRobot(1, 1)
    game.popRobot(1, 25)

    game.popRobot(2, 7)
    game.popRobot(2, 44)

    game.render()
    
    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-board-02.png", mode='rb' ).read()
    assert( shotFile == refsFile )
