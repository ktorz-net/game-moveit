import sys
from . import local

"""
Test - MoveIt Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.hacka.games.moveit as mi
from src.hacka.games.moveit import player

def test_players_basic():
    game= mi.GameEngine(
        numberOfRobot= 2,
        missions= [(4, 5), (7, 8)],
    )

    master= mi.GameMaster( game )
    bot= player.BasicBot()
    bot.wakeUp( 1, 2, master.initialize() )
    
    assert bot.model().numberOfRobots() == 2

    bot.perceive( master.playerHand(1) )
    assert bot.decide() == "pass"

    assert bot.model().asPod().dump() == game.asPod().dump()

    bot.model().render()
    local.sleep()


def test_players_basic():
    game= mi.GameEngine(
        missions= [(4, 5), (7, 8)],
    )
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