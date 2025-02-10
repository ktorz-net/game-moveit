import sys
from . import local

"""
Test - MoveIt Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import hacka.py as hk
import src.hacka.games.moveit as mi
from src.hacka.games.moveit import player

def test_vips_basic():
    game= mi.GameEngine(
        numberOfRobot= 2,
        missions= [(4, 5), (7, 8)],
        numberOfPVips= 1
    )
    assert game.numberOfMobiles(0) == 1
    assert game.mobilePosition(0, 1) == 8

def test_vips_basic():
    game= mi.GameEngine(
        matrix= [
            [00, 00, 00], #  1  2  3
            [00, 00, -1], #  4  5 
            [00, 00, 00], #  6  7  8
            [00, -1, 00]  #  9    10
        ],
        numberOfRobot= 2,
        missions= [(4, 5), (7, 8)],
        numberOfPVips= 2
    )
    assert game.numberOfMobiles(0) == 2
    assert game.mobilePosition(0, 1) == 10
    assert game.mobilePosition(0, 2) ==  9

    master= mi.GameMaster(game)

    assert master.numberOfVips() == 2
    assert master.vipPositions() == [10, 9]

    assert master.vipGoals() == [10, 9]
    assert master.vipMoves() == [0, 0]

    master.activateVips()
    assert master._engine.moveActions(0) == [0, 0]

    assert len( master.vipGoals() ) == 2
    for g in master.vipGoals() :
        assert g > 0
        assert g <= master.mapSize()
    
    master._vipsGoals= [7, 4]
    assert master.vipGoals() == [7, 4]
    assert master.vipMoves() == [12, 12]

    master.activateVips()
    assert master._engine.moveActions(0) == [12, 12]


def test_vips_basic():
    game= mi.GameEngine(
        matrix= [
            [00, 00, 00], #  1  2  3
            [00, 00, -1], #  4  5 
            [00, 00, 00], #  6  7  8
            [00, -1, 00]  #  9    10
        ],
        numberOfRobot= 2,
        missions= [(4, 5), (7, 8)],
        numberOfPVips= 2
    )

    master= mi.GameMaster(game)
    master._vipsGoals= [7, 4]

    assert master.vipPositions() == [10, 9]
    assert master.vipGoals() == [7, 4]

    master.tic()
    assert master.vipPositions() == [8, 6]

    master.tic()
    assert master.vipPositions() == [7, 4]
    
    master.tic()
    assert master.vipPositions() == [7, 4]