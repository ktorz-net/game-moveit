
import copy, hacka

from .map import Map

class Engine():

    def __init__( self, matrix= [[0, 0, 0],[0, -1, 0],[0, 0, 0]], numberOfPlayers=1, numberOfRobot=1, numberOfPVips=0 ):
        # Initialize Map :
        self._map= Map(numberOfPlayers)
        self._map.initializeGrid( copy.deepcopy(matrix), 0.9, 0.1 )
        # Initialize ViPs :
        size= self._map.size()
        for iVip in range(numberOfPVips) :
                self._map.popRobot( 0, size-iVip )
        # Initialize Robots :
        i= 1
        for pId in range(1, numberOfPlayers+1) :
            for iRobot in range(numberOfRobot) :
                self._map.popRobot( pId, i )
                i+=1
        # Initialize mission:
        self._missions= []
        # Initialize Artist :
        self._artist= hacka.artist.Artist().initializePNG( "shot-moveIt.png" )
        self._artist.flip()
        self._artist.fitBox( [(-0.5, -0.5), (9.5, 6.5)], 10 )#self._map.box(), 10 )
        self.marketBrush= self._artist._panel[6]
        self.marketBrush.width= 8

    # Mission :
    def addMission( self, iFrom, iTo ):
        self._missions.append( (iFrom, iTo, 10, 0, 0) )

    # Rendering :
    def render(self):
        self._artist.drawMap( self._map )
        # Market:
        self._artist.drawPolygon(
            [6.55, 6.55, 9.5, 9.5], [2.45, -0.6, -0.6, 2.45],
            self.marketBrush
        )
        self._artist._fontSize= 20
        self._artist.write( 6.6, 2.2, "Market Place:", self.marketBrush )
        self._artist._fontSize= 16
        sep= 0.0
        for mFrom, mTo, pay, iPlayer, iRobot in self._missions :
            if iPlayer == 0 :
                self._artist.write( 6.8, 1.9-sep, f"> from: {mFrom} to: {mTo} ({pay} ¢)", self.marketBrush )
            else :
                self._artist.write( 6.8, 1.9-sep, f"> from: {mFrom} to: {mTo} (---)", self.marketBrush )
            sep+= 0.24
        # Finalize:
        self._artist.flip()
