import random, hacka.py as hk
from hacka.artist import Artist
import hacka.tiled as htiled

from .gameengine import Engine

class Master( hk.AbsSequentialGame ) :

    # Initialization:
    def __init__( self, game= Engine(), randomMission= 0, seed=False, ):
        super().__init__( game.numberOfPlayers() )
        self._seed= seed
        # GameEngine: 
        self._engine= game
        self._gameTic= self._engine.tic()
        self._randomMission= randomMission

    def addRandomMission(self):
        bound= self._engine._map.size()+1
        iFrom= random.randrange(1, bound)
        iTo= random.randrange(1, bound)
        pay= 10+random.randrange(bound)
        self._engine.addMission( iFrom, iTo, pay )
        return iFrom, iTo, pay

    # Game interface :
    def initialize(self):
        if self._randomMission > 0 :
        # Clean Up.
            self._engine.clearMissions()
            for iOwner in range(self.numberOfPlayers+1) :
                for iMob in range( 1, self._engine.numberOfMobiles(iOwner)+1 ) :
                    self._engine.mobile(iOwner, iMob).setMission(0)
        # Set missions at random:
            for i in range( self._randomMission ) :
                self.addRandomMission()
        #for tile in self._map.tiles() :
        #    tile.clear()
        # Initialize configuration :
        return self._engine.asPod("MoveIt")
    
    def playerHand( self, iPlayer ):        
        return self._engine.state()

    def applyPlayerAction( self, iPlayer, action ):
        # Separate moves and missions actions:
        moveActions= action.split("move")
        missionActions= moveActions[0].split("mission")
        burnedRobot= []
        # If there is some mission actions:
        if len(missionActions) > 1 :
            orders= []
            # get move indexes :
            for strX in missionActions[1].split(" ") :
                if strX.isdigit() :
                    orders.append( int(strX) )
            # Apply moves :
            for iRobot, missionId in zip( orders[0::2], orders[1::2] ) :
                self._engine.missionAction(iPlayer, iRobot, missionId)
                burnedRobot.append(iRobot)
        # If there is some move actions:
        if len(moveActions) > 1 :
            orders= []
            # get move indexes :
            for strX in moveActions[1].split(" ") :
                if strX.isdigit() :
                    orders.append( int(strX) )
            # Apply moves :
            for iRobot, clockDir in zip( orders[0::2], orders[1::2] ) :
                if iRobot not in burnedRobot :
                    self._engine.setMoveAction(iPlayer, iRobot, clockDir)
        return True
    
    def tic( self ):
        self._engine.applyMoveActions()
    
    def isEnded( self ):
        # if the counter reach it final value
        return self._engine.tic() == 0 or self._engine.missionsList() == []

    def playerScore( self, iPlayer ):
        # All players are winners.
        return self._engine.score(iPlayer)
