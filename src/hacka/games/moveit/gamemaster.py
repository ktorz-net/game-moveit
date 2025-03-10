import random, hacka.py as hk
from .artist import Artist
#from  ... import tiled

from .gameengine import Engine

class Master( hk.AbsSequentialGame ) :

    # Initialization:
    def __init__( self, game= Engine(), randomMission= 0, seed=False, vipZones= None ):
        super().__init__( game.numberOfPlayers() )
        self._seed= seed
        # GameEngine: 
        self._engine= game
        self._gameTic= self._engine.tic()
        self._randomMission= randomMission
        # GameEngine:  
        self.computeDistances()
        self.initializeVipsBehavior()
        # Vips goal zones: 
        self._vipZones= range( 1, self.mapSize()+1 )
        if vipZones :
            self._vipZones= vipZones

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
        self._engine.reInit( self._gameTic )
        #else :
        #    pass
        #for tile in self._map.tiles() :
        #    tile.clear()
        # Initialize configuration :
        #self.computeDistances()
        self.initializeVipsBehavior()
        return self._engine.asPod("MoveIt")
    
    def playerHand( self, iPlayer ):        
        return self._engine.state()

    def applyPlayerAction( self, iPlayer, action ):
        decompo= action.split(" ")
        if 'move' in decompo or 'mission' in decompo :
            return self.applyPlayerMoveMissionAction(iPlayer, action)
        iRobot= 1
        while len(decompo) > 0 :
            act= decompo.pop(0)
            if act == 'go' :
                clockDir= int(decompo.pop(0))
                self._engine.setMoveAction(iPlayer, iRobot, clockDir)
            elif act == 'act' :
                missionId= int(decompo.pop(0))
                self._engine.missionAction(iPlayer, iRobot, missionId)
            elif act != 'pass' :
                break
            iRobot+=1

        return self.applyPlayerMoveMissionAction(iPlayer, action)

    def applyPlayerMoveMissionAction( self, iPlayer, action ):
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
        self.activateVips()
        self._engine.applyMoveActions()
    
    def isEnded( self ):
        # if the counter reach it final value
        return self._engine.tic() == 0 or self._engine.missionsList() == []

    def playerScore( self, iPlayer ):
        # All players are winners.
        return self._engine.score(iPlayer) + self._engine.tic()

    # map tools:
    def mapSize(self):
        return self._engine._map.size()
    
    def computeDistances(self):
        s= self.mapSize()
        self._distances= [ [ i for i in range(s+1) ] ]
        for i in range( 1, s+1 ) :
            dist= self.computeDistancesTo(i)
            self._distances.append( dist )

    def computeDistancesTo(self, iTile):
        gameMap= self._engine.map()
        # Initialize distances to 0:
        dists= [iTile] +  [0 for i in range( gameMap.size() )]
        # Initialize step from iTile:
        ringNodes= gameMap.neighbours(iTile)
        ringDistance= 1
        # while theire is nodes to visit
        while len(ringNodes) > 0 :
            nextNodes= []
            # Visit all step nodes:
            for node in ringNodes :
                # Update distance information
                dists[node]= ringDistance
            for node in ringNodes :
                # Search for new tile to visit:
                neighbours= gameMap.neighbours(node)
                for candidate in neighbours :
                    if dists[candidate] == 0 :
                         nextNodes.append(candidate)
            # swith to the next step.
            ringNodes= nextNodes
            ringDistance+= 1
        # Correct 0 distance:
        dists[iTile]= 0
        return dists
    
    def toward(self, iTile, iTarget):
        gameMap= self._engine.map()
        # If no need to move:
        if iTile == iTarget :
            return 0, iTile
        # Get candidates:
        clockdirs= gameMap.clockBearing(iTile)
        nextTiles= gameMap.neighbours(iTile)
        selectedDir= clockdirs[0]
        selectedNext= nextTiles[0]
        # Test all candidates:
        for clock, tile in zip( clockdirs, nextTiles ) :
            if self._distances[tile][iTarget] < self._distances[selectedNext][iTarget] :
                selectedDir= clock
                selectedNext= tile
        # Return the selected candidates:
        return selectedDir, selectedNext

    def moveOptions(self, iTile, iTarget):
        gameMap= self._engine.map()
        # If no need to move:
        if iTile == iTarget :
            return [(0, iTile)]
        # Get candidates:
        clockdirs= gameMap.clockBearing(iTile)
        nextTiles= gameMap.neighbours(iTile)
        selected= [ (clockdirs[0], nextTiles[0]) ]
        refDist= self._distances[nextTiles[0]][iTarget]
        # Test all candidates:
        for clock, tile in zip( clockdirs[1:], nextTiles[1:] ) :
            if self._distances[tile][iTarget] == refDist :
                selected.append( (clock, tile) )
            elif self._distances[tile][iTarget] < refDist :
                selected= [ (clock, tile) ]
                refDist= self._distances[tile][iTarget]
            
        # Return the selected candidates:
        return selected

    def path(self, iTile, iTarget):
        clock, tile= self.toward(iTile, iTarget)
        move= [clock]
        path= [tile]
        while tile != iTarget :
            clock, tile= self.toward(tile, iTarget)
            move.append( clock )
            path.append( tile )
        return move, path
    
    # Vips managment: 
    def initializeVipsBehavior(self):
        self._vipsGoals= [ p for p in self.vipPositions() ]

    def numberOfVips(self):
        return self._engine.numberOfMobiles(0)

    def vipPositions(self) :
        n= self.numberOfVips()
        return [ self._engine.mobilePosition(0, i) for i in range(1, n+1) ]

    def vipGoals(self) :
        return self._vipsGoals
    
    def vipMoves(self) :
        moves= []
        for p, g in zip( self.vipPositions(), self.vipGoals() ) :
            opts= self.moveOptions( p, g )
            moves.append( opts[0][0] )
        return moves
    
    def activateVips(self) :
        vipIds= range( 1, self.numberOfVips()+1 )
        for i, m in zip( vipIds, self.vipMoves() ) :
            self._engine.setMoveAction(0, i, m)
            if m == 0 :
                self._vipsGoals[i-1] = random.choice( self._vipZones )
