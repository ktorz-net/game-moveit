import hacka.pylib as hk
import hacka.tiled as htiled

class Map( htiled.Map ):
    def __init__(self, numberOfPlayers= 1):
        super().__init__()
        self._mobiles= [ [] for i in range( numberOfPlayers+1 ) ]
        self._collects= [ [] for i in range( numberOfPlayers+1 ) ]

    # Accessor: 
    def vips(self):
        return self._mobiles[0]
    
    def robots(self, playerId):
        return self._mobiles[playerId]

    # Construction:
    def initializeGrid(self, matrix, size, separetion):
        self.initializeSquares( matrix, size, separetion )
        self.connectAllCondition(
            lambda tileFrom, tileTo :  tileFrom.centerDistance( tileTo ) < 1.2
        )
        return self

    def popRobot(self, playerId, tileId ):
        # Safety
        if playerId >= len(self._mobiles) or self.tile(tileId).count() > 0 :
            return False
        # Popping
        robotId= len( self._mobiles[playerId] )+1
        robot= hk.Pod( f"R-{robotId}", flags=[playerId] )
        self.addPiece( robot, tileId, 10+playerId )
        self._mobiles[playerId].append(tileId)
        return robot
    
    # Graph:
    def neighbours(self, iTile) :
        return self.tile(iTile).adjacencies()
    
    def directions(self, iTile) : 
        cx, cy= self.tile(iTile).center()
        neibor= self.neighbours(iTile)
        positions= [ self.tile(i).center() for i in neibor ]
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

    def clock(self, iTile, clock):
        return self.completeClock(iTile)[clock]
    
    # Artist rendering:
    def render(self, artist):
        artist.drawMap( self )
        # Market:
        artist.drawPolygon(
            [6.55, 6.55, 9.5, 9.5], [2.45, -0.6, -0.6, 2.45],
            artist._panel[6]
        )
        # Finalize:
        artist.flip()