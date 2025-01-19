
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
        # Initialize Mission:
        self._missions= []
        # Initialize Artist :
        self._artist= hacka.artist.Artist().initializePNG( "shot-moveIt.png" )
        self._artist.flip()
        self._artist.fitBox( [(-0.5, -0.5), (9.5, 6.5)], 10 )#self._map.box(), 10 )
        self.marketBrush= self._artist._panel[6]
        self.marketBrush.width= 8
        # Plaers: 
        self._numberOfPlayers= numberOfPlayers

    # Accessor :
    def mobilePosition(self, iPlayer, iRobot):
        return self._map.mobilePosition(iPlayer, iRobot)

    def mobile(self, iPlayer, iRobot):
        iTile= self._map.mobilePosition(iPlayer, iRobot)
        return self._map.tile(iTile).piece()

    def mission(self, iMission):
        return self._missions[iMission-1]

    def freeMissions(self):
        free= []
        i=1
        for iFrom, iTo, pay, owner in self._missions :
            if owner == 0 :
                free.append(i)
            i+= 1
        return free
    
    # Mission :
    def addMission( self, iFrom, iTo ):
        self._missions.append( (iFrom, iTo, 10, 0) )
        return len(self._missions)

    def updateMission(self, iMission, iFrom, iTo, pay, owner):
        self._missions[iMission-1]= (iFrom, iTo, pay, owner)
    
    # Move :
    def moveActions(self, iPlayer):
        return [ self._map.tile(i).piece().move()
                 for i in self._map.mobilePositions(iPlayer) ]

    def moveDestinations(self, iPlayer):
        return [ self._map.clockposition( mTile, clockDir )
                for mTile, clockDir in zip( self._map.mobilePositions(iPlayer), self.moveActions(iPlayer) ) ]

    def setMoveAction( self, iPlayer, iRobot, clockDir ):
        iTile= self._map.mobilePosition(iPlayer, iRobot)
        robot= self._map.tile(iTile).piece()
        robot.setMove(clockDir)
        return True
    
    def applyMoveActions( self ):
        reserved= []
        blocked= []
        # Move Vips:

        # Get players moves:
        moves= [[]]
        for iPlayer in range( 1, self._numberOfPlayers+1 ):
            moves.append([ [iFrom, iTo]
                for iFrom, iTo in zip( self._map.mobilePositions(iPlayer), self.moveDestinations(iPlayer) ) ])

        # Start Collision: 
        for iPlayer in range( 1, self._numberOfPlayers+1 ):
            for m in moves[iPlayer] :
                if m[0] != m[1] and self._map.tile(m[1]).count() > 0 :
                    print("Boom")
                    m[1]= m[0]

        # Reserve and block:
        for iPlayer in range( 1, self._numberOfPlayers+1 ):
            for m in moves[iPlayer] :
                if m[0] != m[1] :
                    if m[1] in reserved :
                        if m[1] not in blocked :
                            blocked.append(m[1])
                    else:
                        reserved.append(m[1])

        # Apply non-bloked moves :
        for iPlayer in range( 1, self._numberOfPlayers+1 ):
            for m in moves[iPlayer] :
                if m[1] in blocked :
                    print("Boom !!!")
                else:
                    self._map.teleport( m[0], m[1] )
        # Clean moves:
        self._map.initializeMoves()

    def missionAction(self, iPlayer, iRobot, iMission ):
        robot= self.mobile(iPlayer, iRobot)
        robotPos= self.mobilePosition(iPlayer, iRobot)
        iFrom, iTo, pay, owner= self.mission(iMission)
        # Mission start:
        if robot.mission() == 0 : 
            if robotPos == iFrom and owner == 0 :
                robot.setMission( iMission )
                self.updateMission(iMission, iFrom, iTo, pay, iPlayer)
                return True
            return False
        # Mission end:
        if robot.mission() == iMission and robotPos == iTo : 
            robot.setMission(0)
            self.updateMission(iMission, 0, iTo, pay, iPlayer)
            return True
        return False

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
        i= 1
        for mFrom, mTo, pay, iPlayer in self._missions :
            if mFrom > 0 :
                self._artist.write( 6.8, 1.9-sep, f".{i}", self.marketBrush) 
                self._artist.write( 7.2, 1.9-sep, f"- {mFrom} to: {mTo}", self.marketBrush )
                if iPlayer == 0 :
                    self._artist.write( 8.5, 1.9-sep, f"({pay} ¢)", self.marketBrush )
                else :
                    self._artist.write( 8.4, 1.9-sep, f"(Team-{iPlayer})", self.marketBrush )
                sep+= 0.24
            i+= 1
        # Finalize:
        self._artist.flip()
