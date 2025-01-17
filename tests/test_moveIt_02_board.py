import sys, pathlib
workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

"""
Test - MoveIt Games Class
"""

import hacka.pylib  as hk
import hacka.artist as hka
import hacka.board  as hkb

import src.hacka.games.moveit as mi

def test_moveIt_board():
    # Game MoveIt:
    game= mi.GameMaster( 38 )
    game.initializeBoardGrid( [
        [00, 00, 00, -1, 00, 00, 00, 00],
        [00, -1, 00, 00, 00, -1, 00, 00],
        [00, 00, 00, -1, 00, 00, 00, 00],
        [00, 00, 00, -1, 00, 00, 00, 00],
        [-1, -1, 00, 00, 00, -1, -1, -1]],
        0.9, 0.1
    )
    game.render()

    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-board-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

