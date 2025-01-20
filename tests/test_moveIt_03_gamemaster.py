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
    game= mi.GameEngine()
    master= mi.GameMaster( game )

    assert( type( master.initialize().asPod() ) is hacka.Pod  )
    assert( type( master.playerHand(1).asPod() ) is hacka.Pod )
    assert( master.applyPlayerAction( 1, "move 0" )  )
    master.tic()
    assert( not master.isEnded() )
    
    assert( master.playerScore(1) == 0.0 )
