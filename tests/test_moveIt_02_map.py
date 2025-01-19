import sys, copy, pathlib

import hacka.pylib  as hacka
import hacka.artist as hartist
import hacka.tiled  as htiled

"""
Test - MoveIt Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.hacka.games.moveit as mi

refMatrix= [
    [00, 00, 00, -1, 00, 00, 00, 00, 00, 00],
    [00, -1, 00, 00, 00, -1, 00, -1, -1, 00],
    [00, 00, 00, -1, 00, 00, 00, -1, 00, 00],
    [00, 00, 00, -1, 00, 00, 00, 00, 00, 00],
    [00, -1, 00, 00, 00, -1, 00, -1, -1, -1],
    [00, -1, 00, -1, 00, 00, 00, -1, -1, -1],
    [00, 00, 00, 00, 00, -1, 00, -1, -1, -1]
]

"""
    [ 1,  2,  3,   ,  4,  5,  6,  7,  8,  9],
    [10,   , 11, 12, 13,   , 14,   ,   , 15],
    [16, 17, 18,   , 19, 20, 21,   , 22, 23],
    [24, 25, 26,   , 27, 28, 29, 30, 31, 32],
    [33,   , 34, 35, 36,   , 37,   ,   ,   ],
    [38,   , 39,   , 40, 41, 42,   ,   ,   ],
    [43, 44, 45, 46, 47,   , 48,   ,   ,   ]
"""

def test_moveIt_board():
    # Game MoveIt:
    map= mi.Map(numberOfPlayers=2)
    map.initializeGrid( copy.deepcopy( refMatrix ), 0.9, 0.1 )
    artist= hartist.Artist().initializePNG( "shot-moveIt.png" )
    artist.fitBox( map.box(), 10 )

    map.render( artist )

    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-board-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    assert map.popRobot(1, 1)
    assert map.popRobot(1, 25)

    assert map.popRobot(2, 7)
    assert map.popRobot(2, 44)

    map.render( artist )
    
    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-board-02.png", mode='rb' ).read()
    assert( shotFile == refsFile )

def test_moveIt_neibors():
    # Game MoveIt:
    map= mi.Map( numberOfPlayers=2 )
    map.initializeGrid( copy.deepcopy( refMatrix ), 0.9, 0.1 )

    assert map.neighbours(11) == [3, 11, 12, 18]
    assert map.directions(11) == [(0.0, 1.0), (0.0, 0.0), (1.0, 0.0), (0.0, -1.0)]
    assert map.clockBearing(11) == [12, 0, 3, 6]
    assert map.completeClock(11) == [11,
                             11, 11, 12, 11, 11, 18,
                             11, 11, 11, 11, 11,  3 ]
    assert map.clockposition(11, 0) == 11
    assert map.clockposition(11, 12) == 3
    assert map.clockposition(11, 6) == 18
    assert map.clockposition(11, 3) == 12
    assert map.clockposition(11, 9) == 11

def test_moveIt_robots():
    # Game MoveIt:
    map= mi.Map( numberOfPlayers=2 )
    map.initializeGrid( copy.deepcopy(refMatrix), 0.9, 0.1 )

    assert str(map.popRobot(1, 1)) == 'R-1: [1, 1]'
    assert str(map.popRobot(1, 25)) == 'R-2: [1, 2]'

    assert str(map.popRobot(2, 7)) == 'R-1: [2, 1]'
    assert str(map.popRobot(2, 44)) == 'R-2: [2, 2]'

    assert map.popRobot(3, 33) == False
    assert map.popRobot(1, 7) == False

    assert map.robots(1) == [1, 25]
    assert map.robots(2) == [7, 44]

    assert map.vips() == []

    assert map.move( 11, 12 ) == False
    assert map.move( 1, 6 ) == 10

    assert map.robots(1) == [10, 25]
    assert map.robots(2) == [7, 44]

    assert str( map.tile(10).piece() ) == 'R-1: [1, 1]'

    assert map.clockBearing(44) == [9, 0, 3]

    assert map.move( 44, 12 ) == False
    assert map.move( 44, 3 ) == 45
    assert map.move( 45, 12 ) == 39
    assert map.move( 39,  0 ) == 39
    assert map.move( 39,  3 ) == False
    
    artist= hartist.Artist().initializePNG( "shot-moveIt.png" )
    artist.fitBox( map.box(), 10 )
    
    map.render( artist )

    shotFile= open( "shot-moveIt.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-map-03.png", mode='rb' ).read()
    assert( shotFile == refsFile )

"""
    [ 1,  2,  3,   ,  4,  5,  6,  7,  8,  9],
    [10,   , 11, 12, 13,   , 14,   ,   , 15],
    [16, 17, 18,   , 19, 20, 21,   , 22, 23],
    [24, 25, 26,   , 27, 28, 29, 30, 31, 32],
    [33,   , 34, 35, 36,   , 37,   ,   ,   ],
    [38,   , 39,   , 40, 41, 42,   ,   ,   ],
    [43, 44, 45, 46, 47,   , 48,   ,   ,   ]
"""