import sys
from . import local

import hacka.pylib  as hacka

"""
Test - MoveIt Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.hacka.games.moveit as mi

def test_gamemaster_method():
    game= mi.GameEngine()
    master= mi.GameMaster( game )

    assert( type( master.initialize().asPod() ) is hacka.Pod  )
    assert( type( master.playerHand(1).asPod() ) is hacka.Pod )
    assert( master.applyPlayerAction( 1, "move 1 0" )  )
    master.tic()
    assert( not master.isEnded() )
    
    assert( master.playerScore(1) == 0.0 )

def test_gamemaster_live_cycle():
    game= mi.GameEngine( tic= 10 )
    master= mi.GameMaster( game )

    assert master.initialize()

    t= 10
    while t > 0 :
        assert not master.isEnded()
        assert game.tic() == t
        master.tic()
        t-= 1

    assert( master.isEnded() )
    
def test_gamemaster_moves():
    game= mi.GameEngine( tic= 10, missions= [(4, 5), (7, 8)] )
    master= mi.GameMaster( game )

    game.render()
    local.sleep()

    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-04.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    assert game._map.mobilePositions(1) == [1]

    # Turn 1
    master.initialize()
    master.playerHand(1)
    master.applyPlayerAction( 1, "move 1 6" )
    master.tic()

    assert game.mobilePosition(1, 1) == 4
    assert game.mobileMission(1, 1) == 0
    
    # Turn 2
    master.playerHand(1)
    master.applyPlayerAction( 1, "mission 1 1" )
    master.tic()

    assert game.mobilePosition(1, 1) == 4
    assert game.mobileMission(1, 1) == 1
    
    # Turn 3-6
    moves= [12, 3, 3, 6]
    for m in moves :
        master.playerHand(1)
        master.applyPlayerAction( 1, f"move 1 {m}" )
        master.tic()

    assert game.mobilePosition(1, 1) == 5
    assert game.mobileMission(1, 1) == 1
    assert game.score(1) == 0.0

    # Turn 7
    master.playerHand(1)
    master.applyPlayerAction( 1, "mission 1 1 move 1 12" )
    master.tic()

    assert game.mobilePosition(1, 1) == 5
    assert game.mobileMission(1, 1) == 0
    assert game.score(1) == 10.0
