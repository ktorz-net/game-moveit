#!env python3
import os

"""
HackaGame player interface 
"""

from ... import command as cmd
from ...core import player as pl
from . import Hexaboard, defineMobiles

def main():
    player= PlayerShell()
    player.takeASeat()

class PlayerShell( pl.AbsPlayer ):

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
        print( f'---\nwake-up player-{playerId} ({numberOfPlayers} players)')
        self.report(False)

    def perceive(self, statePod):
        # update the game state:
        self._countTic= statePod.flag(1)
        self._countCycle= statePod.flag(2)
        self._score= statePod.value(1)
        self._board.mobilesFromPod( statePod )
        self.report(True)

    def decide(self):
        #print( self.state() )
        action = input('Enter your action (move x OR pass): ')
        return action
    
    def sleep(self, result):
        print( f'---\ngame end\nresult: {result}')
    
    # Reports:
    def report(self, clear=True):
        if clear :
            os.system("clear")
        print( f"counters{(self._countTic, self._countCycle)}, score({self._score})" )
        print( self._board.shell() )
        for mobile in self._mobiles :
            print( mobile )

    def state(self):
        # Récupération des 3 robots de la scéne:
        robot, human1, human2 = tuple(self._mobiles)
        # Calcul du chemin à l'objectif:
        pathGoal= self._board.path( robot.x(), robot.y(), robot.goalx(), robot.goaly() )
        state= [ pathGoal[0], len(pathGoal) ]
        # Environment proche
        for dir in range(1, 7) :
            x, y = self._board.at_dir( robot.x(), robot.y(), dir )
            state.append( self._board.isCoordinate(x, y) and not self._board.at(x, y).isObstacle() )
        # Calcul du chemin aux humain:
        pathH1= self._board.path( robot.x(), robot.y(), human1.x(), human1.y() )
        pathH2= self._board.path( robot.x(), robot.y(), human2.x(), human2.y() )
        state+= [ pathH1[0], len(pathH1), human1.direction(), pathH2[0], len(pathH2), human2.direction() ]
        return state
    
# script
if __name__ == '__main__' :
    main()