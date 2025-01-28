
import copy, hacka
from hacka.tiled import Float2, Shape

from .map import Map

class Mission:
    def __init__( self, start, final, reward, owner ):
        self.start= start
        self.final= final
        self.reward= reward
        self.owner= owner

    def list(self):
        return [self.start, self.final, self.reward, self.owner]
    
    def tuple(self):
        return self.start, self.final, self.reward, self.owner

class Engine():

    def __init__( self, 
                 matrix= [[0, 0, 0],[0, -1, 0],[0, 0, 0]],
                 numberOfPlayers=1, numberOfRobot=1,
                 numberOfPVips=0,
                 missions= [],
                 tic= 100 ):
        # Initialize Map :
        self._map= Map(numberOfPlayers)
        self._map.initializeGrid( copy.deepcopy(matrix), 0.9, 0.1 )
        # Initialize ViPs :
        size= self._map.size()
        for iVip in range(numberOfPVips) :
                self._map.popRobot( 0, size-iVip )
        # Initialize Robots
        iTile= 1
        for pId in range(1, numberOfPlayers+1) :
            for iRobot in range(numberOfRobot) :
                self._map.popRobot( pId, iTile )
                iTile+=1
        # Players: 
        self._scores= [ 0.0 for i in range(numberOfPlayers+1) ]
        self._numberOfPlayers= numberOfPlayers
        # Initialize Mission:
        self._missions= []
        for iFrom, iTo in missions :
            self.addMission(iFrom, iTo)
        self._tic= tic
        # Initialize Artist :
        self._artist= hacka.artist.Artist().initializePNG( "shot-moveIt.png" )
        self._artist.flip()
        self._artist.fitBox( [Float2(-0.5, -0.5), Float2(9.5, 6.5)], 10 )#self._map.box(), 10 )
        self.marketBrush= self._artist._panel[6]
        self.marketBrush.width= 8

    # Accessor :
    def map(self):
        return self._map
    
    def numberOfPlayers(self):
        return self._numberOfPlayers
    
    def numberOfMobiles(self, iPlayer=1):
        return len( self._map._mobiles[iPlayer] )
    
    def mobilePosition(self, iPlayer, iRobot):
        return self._map.mobilePosition(iPlayer, iRobot)

    def setMobilePosition(self, iPlayer, iRobot, iPosition):
        iT= self.mobilePosition(iPlayer, iRobot)
        self._map.teleport(iT, iPosition)
        return self.mobile(iPlayer, iRobot).mission()

    def mobileMission(self, iPlayer, iRobot):
        return self.mobile(iPlayer, iRobot).mission()

    def mobile(self, iPlayer, iRobot):
        iTile= self._map.mobilePosition(iPlayer, iRobot)
        return self._map.tile(iTile).piece()
    
    def isMobile(self, iPlayer, iRobot):
        return ( 0 <= iPlayer and iPlayer <= self.numberOfPlayers() 
            and 0 < iRobot and iRobot <= self.numberOfMobiles(iPlayer) )
    
    def mission(self, iMission):
        return self._missions[iMission-1]
    
    def missionsList(self):
        l= []
        i= 1
        for m in self._missions :
            if m.start > 0 :
                l.append(i)
            i+= 1
        return l
    
    def isMission(self, iMission):
        return ( 0 < iMission and iMission <= len(self._missions) )

    def missions(self):
        return self._missions

    def freeMissions(self):
        free= []
        i=1
        for m in self._missions :
            if m.owner == 0 :
                free.append(i)
            i+= 1
        return free
    
    def tic( self ):
        return self._tic
    
    def setTic( self, clixNumber ):
        self._tic= clixNumber
    
    def score(self, iPlayer):
        return self._scores[iPlayer]
    
    def filePath(self):
        self._artist._support._filePath
    
    def setFilePath(self, filePath):
        self._artist._support._filePath= filePath
    
    # Mission :
    def clearMissions(self):
        self._missions= []
        for iOwner in range(self.numberOfPlayers()+1) :
            for iRobot in range(1, self.numberOfMobiles(iOwner)+1) :
                self.mobile( iOwner, iRobot ).setMission(0)
        return self

    def addMission( self, iFrom, iTo, pay= 10 ):
        self._missions.append( Mission(iFrom, iTo, pay, 0) )
        return len(self._missions)

    def updateMission(self, iMission, iFrom, iTo, pay, owner):
        self._missions[iMission-1]= Mission(iFrom, iTo, pay, owner)
    
    # Move :
    def moveActions(self, iPlayer):
        return [ self._map.tile(i).piece().move()
                 for i in self._map.mobilePositions(iPlayer) ]

    def moveDestinations(self, iPlayer):
        return [ self._map.clockposition( mTile, clockDir )
                for mTile, clockDir in zip( self._map.mobilePositions(iPlayer), self.moveActions(iPlayer) ) ]

    def setMoveAction( self, iPlayer, iRobot, clockDir ):
        # Security:
        if not(self.isMobile(iPlayer, iRobot) and 0<= clockDir and clockDir <= 12) :
            return False
        iTile= self._map.mobilePosition(iPlayer, iRobot)
        robot= self._map.tile(iTile).piece()
        robot.setMove(clockDir)
        return True
    
    def applyMoveActions( self ):
        collision= 0
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
                    self._scores[iPlayer]+= -100
                    collision+= 1
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
                    self._scores[iPlayer]+= -100
                    collision+= 1
                else:
                    self._map.teleport( m[0], m[1] )
        # Clean moves:
        self._map.initializeMoves()
        self._tic-= 1
        return collision

    def missionAction(self, iPlayer, iRobot, iMission ):
        # Security:
        if not(self.isMobile(iPlayer, iRobot) and self.isMission(iMission) ) :
            return False
        # Localvariable:
        robot= self.mobile(iPlayer, iRobot)
        robotPos= self.mobilePosition(iPlayer, iRobot)
        iFrom, iTo, pay, owner= self.mission(iMission).tuple()
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
            self._scores[iPlayer]+= pay
            self.updateMission(iMission, 0, iTo, 0, iPlayer)
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
        for i in self.missionsList() :
            mFrom, mTo, pay, iPlayer= self.mission(i).tuple()
            self._artist.write( 6.8, 1.9-sep, f".{i}", self.marketBrush) 
            self._artist.write( 7.2, 1.9-sep, f"- {mFrom} to: {mTo}", self.marketBrush )
            if iPlayer == 0 :
                self._artist.write( 8.5, 1.9-sep, f"({pay} ¢)", self.marketBrush )
            else :
                self._artist.write( 8.4, 1.9-sep, f"(Team-{iPlayer})", self.marketBrush )
            sep+= 0.24
        # Finalize:
        self._artist.flip()

    # State and Updates:
    def state(self):
        # Engine :
        pod= hacka.Pod( "State", "", [self._tic], self._scores )
        # Missions :
        pod.append( self.stateMissions() )
        # Mobiles :
        pod.append( self.stateMobiles() )
        return pod
    
    def setOnState(self, podState):
        # Engine :
        self._tic= podState.flag(1)
        # Score :
        self._scores= podState.values()
        # Missions :
        self.setStateMissions( podState.child(1) )
        # Mobiles :
        self.setStateMobiles( podState.child(2) )
        return self
    
    def stateMissions(self):
        podMissions= hacka.Pod( "missions" )
        i= 1
        for m in self._missions :
            podMissions.append( hacka.Pod( f"{i}", flags=m.list() ) )
            i+= 1
        return podMissions
    
    def setStateMissions( self, podState ):
        self._missions= []
        for pod in podState.children() :
            self._missions.append( Mission(pod.flag(1), pod.flag(2),pod.flag(3), pod.flag(4)) )
        return self
    
    def stateMobiles(self):
        podMobiles= hacka.Pod( "mobiles" )
        for ip in range(self.numberOfPlayers()+1 ):
            for ir in range( 1, self.numberOfMobiles(ip)+1 ):
                pos= self.mobilePosition(ip, ir)
                mis= self.mobileMission(ip, ir)
                podMobiles.append( hacka.Pod( flags=[ip, ir, pos, mis] ) )
        return podMobiles
    
    def setStateMobiles( self, podState ):
        self._map.clearMobiles()
        for pod in podState.children() :
            iPlayer= pod.flag(1)
            iRobot= pod.flag(2)
            pos= pod.flag(3)
            mis= pod.flag(4)
            self._map.popRobot( iPlayer, pos, mis )
        return self
    
    # Podable :
    def asPod(self, name="MoveIt"):
        # Engine :
        pod= hacka.Pod( 
            name, "",
            [self._numberOfPlayers, self.numberOfMobiles(), self.numberOfMobiles(0), self._tic],
            self._scores )
        # Map :
        pod.append( self._map.asPod() )
        # Missions :
        podMissions= hacka.Pod( "missions" )
        i= 1
        for m in self._missions :
            podMissions.append( hacka.Pod( f"{i}", flags=m.list() ) )
            i+= 1
        pod.append( podMissions )
        return pod
    
    def fromPod(self, pod):
        # Engine :
        self._numberOfPlayers= pod.flag(1)
        numberOfRobots= pod.flag(2)
        numberOfVips= pod.flag(3)
        self._tic= pod.flag(4)
        # Score :
        self._scores= pod.values()
        # Map :
        self._map._mobiles= [ [0 for i in range(numberOfVips) ] ]
        for p in range( self.numberOfPlayers() ):
            self._map._mobiles.append( [ 0 for i in range(numberOfRobots) ] )
        self._map.fromPod( pod.child(1) )
        # Missions :
        self._missions= []
        for pod in pod.child(2).children() :
            self._missions.append( Mission(pod.flag(1), pod.flag(2),pod.flag(3), pod.flag(4)) )
        return self