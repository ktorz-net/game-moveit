import sys
from . import local

import hacka.pylib  as hacka

"""
Test - MoveIt Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.hacka.games.moveit as mi

def test_gameMethod():
    game= mi.GameMaster( 38 )

    assert( type( game.initialize().asPod() ) is hacka.Pod  )
    assert( type( game.playerHand(1).asPod() ) is hacka.Pod )
    assert( game.applyPlayerAction( 1, "move 0" )  )
    game.tic()
    assert( not game.isEnded() )
    assert( game.playerScore(1) == 0.0 )
