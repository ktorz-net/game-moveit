#!env python3
"""
HackaGame player interface 
"""

from ...core import player as pl
from . import Hexaboard, defineMobiles

def log( aStr ):
    #print( aStr )
    pass

def main():
    player= AutonomousPlayer()
    result= player.takeASeat()
    print( f"Average: {sum(result)/len(result)}" )

class AutonomousPlayer( pl.AbsPlayer ):

    def __init__(self):
        super().__init__()
        self._board= Hexaboard()
        self._mobiles= []
        self._id= 0
    
    # Player interface :
    def wakeUp(self, playerId, numberOfPlayers, gamePod):
        # Initialize from gamePod:
        self._id= playerId
        assert( gamePod.family() == 'MoveIt')
        self._board.fromPod( gamePod )
        nbRobots, nbMobiles= gamePod.flag(3), gamePod.flag(4)
        self._mobiles= defineMobiles( nbRobots, nbMobiles )
        self._board.setupMobiles( self._mobiles )

        # Initialize state variable:
        self._countTic= 0
        self._countCycle= 0
        self._score= 0

        # Reports:
        log( f'---\nwake-up player-{playerId} ({numberOfPlayers} players)')
        
    def perceive(self, statePod):
        # update the game state:
        self._countTic= statePod.flag(1)
        self._countCycle= statePod.flag(2)
        self._score= statePod.value(1)
        self._board.mobilesFromPod( statePod )
    
    def decide(self):
        action= "move"
        for r in self._mobiles :
            if r.isRobot() :
                path= self._board.path( r.x(), r.y(), r.goalx(), r.goaly() )
                dir= path[0]
                action+= " " + str(dir)
        return action
    
    def sleep(self, result):
        log( f'---\ngame end on result: {result}' )

# script
if __name__ == '__main__' :
    main()