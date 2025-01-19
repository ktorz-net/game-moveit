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
    

def test_gameengine_initLarge():
    game= mi.GameEngine( matrix, 2, 3, 1 )

    game.render()
    local.sleep()
    
    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-02.png", mode='rb' ).read()
    assert( shotFile == refsFile )

def test_gameengine_mission():
    game= mi.GameEngine()

    game.render()
    local.sleep()
    
    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    game.addMission( 4, 5 )
    game.addMission( 7, 8 )

    game.render()
    local.sleep()
    
    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-03.png", mode='rb' ).read()
    assert( shotFile == refsFile )
