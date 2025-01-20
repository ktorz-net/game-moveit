import re, hacka.pylib as hk
from hacka.artist import Artist
import hacka.tiled as htiled

from .gameengine import Engine

class Master( hk.AbsSequentialGame ) :

    # Initialization:
    def __init__( self, game= Engine(), seed=False):
        super().__init__( game.numberOfPlayers() )
        self._seed= seed
        # GameEngine: 
        self._engine= game
        self._gameTic= self._engine.tic()

    # Game interface :
    def initialize(self):
        # Clean Up.
        #for tile in self._map.tiles() :
        #    tile.clear()
        # Initialize configuration :
        return self._engine.asPod("MoveIt")
    
    def playerHand( self, iPlayer ):        
        return self._engine.state()

    def applyPlayerAction( self, iPlayer, action ):
        return True
    
    def tic( self ):
        self._engine.applyMoveActions()
    
    def isEnded( self ):
        # if the counter reach it final value
        return self._engine.tic() == 0

    def playerScore( self, iPlayer ):
        # All players are winners.
        return self._engine.score(iPlayer)
