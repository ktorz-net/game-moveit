import sys
from . import local

import hacka.pylib as hacka

"""
Test - MoveIt Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.hacka.games.moveit as mi

matrix= [
    [00, 00, 00, -1, 00, 00, 00, 00, 00, 00],
    [00, -1, 00, 00, 00, -1, 00, -1, -1, 00],
    [00, 00, 00, -1, 00, 00, 00, -1, 00, 00],
    [00, 00, 00, -1, 00, 00, 00, 00, 00, 00],
    [00, -1, 00, 00, 00, -1, 00, -1, -1, -1],
    [00, -1, 00, -1, 00, 00, 00, -1, -1, -1],
    [00, 00, 00, 00, 00, -1, 00, -1, -1, -1]
]

def test_gameengine_init():
    game= mi.GameEngine()

    game.render()
    local.sleep()
    
    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    assert game._map.tile(1).adjacencies() == [1, 2, 4]
    assert game._map.tile(2).adjacencies() == [1, 2, 3]
    assert game._map.tile(8).adjacencies() == [5, 7, 8]
    

def test_gameengine_initLarge():
    game= mi.GameEngine( matrix, 2, 3, 1 )

    game.render()
    local.sleep()
    
    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-02.png", mode='rb' ).read()
    assert( shotFile == refsFile )

def test_gameengine_move():
    game= mi.GameEngine()

    game.render()
    local.sleep()
    
    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    assert game.moveActions( 1 ) == [0]
    assert game.setMoveAction( 1, 1, 6 )
    assert game.moveActions( 1 ) == [6]

    assert game._map.mobilePositions(1) == [1]

    game.applyMoveActions()

    assert game._map.mobilePositions(1) == [4]

    game.render()
    local.sleep()
    
    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-03.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    assert game.moveActions(1) == [0]
    assert game.setMoveAction( 1, 1, 3 )
    assert game.moveActions(1) == [3]

    game.applyMoveActions()

    assert game._map.mobilePositions(1) == [4]

    game.render()
    
    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-03.png", mode='rb' ).read()
    assert( shotFile == refsFile )

def test_gameengine_mission():
    game= mi.GameEngine()

    game.render()
    local.sleep()
    
    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    assert game.freeMissions() == []
    
    assert game.addMission( 4, 5 ) == 1
    assert game.addMission( 7, 8 ) == 2

    assert game.freeMissions() == [1, 2]

    assert game.mission(1) == (4, 5, 10, 0)
    assert game.mission(2) == (7, 8, 10, 0)

    game.render()
    local.sleep()
    
    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-04.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    assert game.missionAction(1, 1, 1) == False

    assert game.mobile(1, 1).mission() == 0

    game.setMoveAction( 1, 1, 6 )
    game.applyMoveActions()

    assert game.missionAction(1, 1, 1) == True

    assert game.mobile(1, 1).mission() == 1

    assert game.freeMissions() == [2]

    game.render()
    local.sleep()

    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-05.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    game.setMoveAction( 1, 1, 6 )
    game.applyMoveActions()

    game.setMoveAction( 1, 1, 3 )
    game.applyMoveActions()

    assert game.mobilePosition(1, 1) == 7

    assert game.missionAction(1, 1, 1) == False
    assert game.missionAction(1, 1, 2) == False

    game.setMoveAction( 1, 1, 3 )
    game.applyMoveActions()

    assert game.mobilePosition(1, 1) == 8

    game.setMoveAction( 1, 1, 12 )
    game.applyMoveActions()

    assert game.mobilePosition(1, 1) == 5
    assert game.mobile(1, 1).mission() == 1
    assert game.missionAction(1, 1, 1) == True
    assert game.missionAction(1, 1, 2) == False

    assert game.mobile(1, 1).mission() == 0
    assert game.freeMissions() == [2]

    game.render()
    local.sleep()

    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-06.png", mode='rb' ).read()
    assert( shotFile == refsFile )
