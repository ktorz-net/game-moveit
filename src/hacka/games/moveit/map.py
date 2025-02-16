
from .mobile import Mobile
from . import tiled

class Map( tiled.Map ):
    def __init__(self, numberOfPlayers= 1):
        super().__init__()
        self._mobiles= [ [] for i in range( numberOfPlayers+1 ) ]
        self._collects= [ [] for i in range( numberOfPlayers+1 ) ]

    # Accessor: 
    def vips(self):
        return self._mobiles[0]
    
    def mobilePositions(self, playerId):
        return self._mobiles[playerId]

    def mobilePosition(self, playerId, iRobot):
        return self._mobiles[playerId][iRobot-1]

    # Construction:
    def initializeGrid(self, matrix, size, separetion):
        self.initializeSquares( matrix, size, separetion )
        self.connectAllCondition(
            lambda tileFrom, tileTo :  tileFrom.centerDistance( tileTo ) < 1.2
        )
        for shape in self.shapes() :
            shape.round(2)
        
        return self
    
    def clearMobiles(self):
        for mobileList in self._mobiles :
            for pos in mobileList :
                self.tile(pos).clear()
        self._mobiles= [ [] for i in range( len(self._mobiles) ) ]
    
    def popRobot(self, playerId, tileId, mission=0 ):
        # Safety
        if playerId >= len(self._mobiles) or self.tile(tileId).count() > 0 :
            return False
        # Popping
        robotId= len( self._mobiles[playerId] )+1
        robot= Mobile( playerId, robotId, mission)
        self.addPiece( robot, tileId, 10+playerId )
        self._mobiles[playerId].append(tileId)
        return robot

    def initializeMoves(self):
        for mobilePositions in self._mobiles :
            for i in mobilePositions :
                for piece in self.tile(i).pieces():
                    piece.setMove(0)

    # Graph:
    def neighbours(self, iTile) :
        return self.tile(iTile).adjacencies()
    
    def directions(self, iTile) : 
        cx, cy= self.tile(iTile).center().tuple()
        neibor= self.neighbours(iTile)
        positions= [ self.tile(i).center().tuple() for i in neibor ]
        return [ (x-cx, y-cy) for x, y in positions ]
    
    def clockBearing(self, iTile):
        clock= [
            [ 0,  9,  0],
            [ 6,  0, 12],
            [ 0,  3,  0]
        ]
        positions= [ (int(round(x, 0)), int(round(y, 0))) for x, y in self.directions(iTile) ]
        return [ clock[1+x][1+y] for x, y in positions ]

    def completeClock(self, iTile):
        clock= [ iTile for i in range(13) ]
        for it, ic in zip( self.neighbours(iTile), self.clockBearing(iTile) ) :
            clock[ic]= it
        return clock

    def clockposition(self, iTile, clockDir):
        return self.completeClock(iTile)[clockDir]
    
    # Moving:
    def move(self, iFrom, clockDir):
        if self.tile(iFrom).count() > 0 and clockDir == 0 :
            return iFrom
        iTo= self.clockposition( iFrom, clockDir ) 
        return self.teleport(iFrom, iTo)

    def teleport( self, iFrom, iTo ):
        if self.tile(iFrom).count() == 0 or self.tile(iTo).count() :
            return False
        # move:
        mobile= self.tile(iFrom).piece()
        self.tile(iFrom).clear()
        self.tile(iTo).append(mobile, 10+mobile.owner())
        # update knoledge:
        owner= mobile.owner()
        self._mobiles[owner][ mobile.identifier()-1 ]= iTo
        return iTo
    
    def fromPod(self, aPod):
        super().fromPod(aPod)
        # Update cros knoldge:
        for t in range( 1, self.size()+1 ):
            for p in range( len( self.tile(t)._pieces ) ) :
                iPlayer= self.tile(t)._pieces[p].flag(1)
                iRobot= self.tile(t)._pieces[p].flag(2)
                self._mobiles[iPlayer][iRobot-1]= t