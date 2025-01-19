"""
MoveIt - an HackaGame game 
"""

from . import map, gameengine, gamemaster

Map= map.Map
GameEngine= gameengine.Engine
GameMaster= gamemaster.GameMaster


"""
MoveIt - an HackaGame game 
import sys, random, re

Hexaboard= board.Hexaboard
Cell= board.Cell
Mobile= mobile.Mobile

















import sys, random, re

import hacka.pylib as hk
from . import board, mobile

import sys, random, re

Hexaboard= board.Hexaboard
Cell= board.Cell
Mobile= mobile.Mobile

def defineMobiles( nbRobots, nbMobiles ):
    mobiles= [ Mobile(i+1) for i in range(nbMobiles) ]
    for m in mobiles[nbRobots:] :
        m.setHuman()
    return mobiles

class GameMaster( hk.AbsSequentialGame ) :

    # Initialization:
    def __init__( self, seed=False, sizeLine=6, sizeHeight=4,
                 numberOfRobots=1, numberOfHuman=2,
                 numberOfObstacles=6, defective=False,
                 numberOfCycle= 10, maximunTics= 16) :
        super().__init__( numberOfPlayers=1 )
        self._seed= seed
        self._board= Hexaboard( sizeLine, sizeHeight )
        self._mobiles= [ Mobile( i+1, i%sizeLine, i//sizeLine) for i in range(numberOfRobots+numberOfHuman)]
        self._nbObstacles= numberOfObstacles
        self._nbCycle= numberOfCycle
        self._countDownCycle= numberOfCycle+1
        self._maxTic= maximunTics
        self._countDownTic= 0
        self._moveRePattern = re.compile( "^move "+ ' '.join(["[0123456]" for i in range(numberOfRobots)])+ "$" )
        self._moveRePatShort = re.compile( "^"+ ' '.join(["[0123456]" for i in range(numberOfRobots)])+ "$" )
        if defective :
            for robot in self._mobiles :
                if random.random() < defective :
                    robot.setError( random.choice([
                        0.1, 0.1, 0.1, 0.1,
                        0.2, 0.2, 0.2,
                        0.3 ]) )
        self._nbRobots= numberOfRobots
        for i in range(numberOfHuman) :
            h= self.mobile(numberOfRobots+1+i)
            h.setHuman()
            h.setError(0.15)
        self._moves= []

    # Accessor: 
    def mobiles(self):
        return self._mobiles
    
    def mobile(self, i): 
        return self._mobiles[i-1]

    def board(self): 
        return self._board

    def score(self):
        return self._score

    # Game interface :
    def initialize(self):
        # clean Up.
        self._board.clear()

        # initialize board.
        seed= (int)(random.random()*32000)
        if self._seed :
            random.seed( self._seed )
        self._score= 0
        self.setupObstacles()
        self.setupMobile()
        self._countDownCycle= self._nbCycle+1

        # initialize cycle.
        self.initializeCycle()
        
        # initialize board.
        pod= self._board.asPod("MoveIt")
        pod.setFlags( pod.flags()+[ self._nbRobots, len(self._mobiles) ] )

        # debug :
        #print( self.board().shell() )
        #for m in self.mobiles() :
        #    print( m )
        random.seed( seed )
        return pod
    
    def playerHand( self, iPlayer ):
        # ping with the increasing counter
        pod= hk.Pod(
            'MoveIt', flags=[self._maxTic, self._countDownCycle],
            values= [self._score] )
        for robot in self._mobiles :
            if robot.number() <= self._nbRobots :
                pod.append( robot.asPod("Robot") )
            else :
                pod.append( robot.asPod("Human") )
        return pod

    def applyPlayerAction( self, iPlayer, action ):
        # Sleep action:
        if action == "pass" :
            self._moves= action
            return True
        
        # Extract robot directions :
        if self._moveRePatShort.match( action ) :
            action= "move "+ action
        elif not self._moveRePattern.match( action ) :
             action= "move "+" ".join( [ '0' for r in range(self._nbRobots) ] )

        robotActions= [int(a) for a in action.split(" ")[1:] ]
        if len(robotActions) != self._nbRobots :
             robotActions= [0 for r in self._mobiles]
        
        self._moves+= robotActions
        return True
    
    def tic( self ):
        # Sleep: 
        if self._moves == "pass" :
            self.initializeCycle()
            self._moves= [ 0 for i in range(self._nbRobots) ]
        
        # Generate Human moves
        for human in self._mobiles[self._nbRobots:] :
            x, y= human.position()
            gx, gy= human.goal()
            dir= self._board.path( x, y, gx, gy )[0]
            tx, ty= self._board.at_dir(x, y, dir)
            if self._board.at(tx, ty).mobile() :
                self._moves.append(0)
            else : 
                self._moves.append(dir)

        # Extract mobiles' directions
        assert( len(self.mobiles()) == len(self._moves) )
        multiMoves= [ [r.x(), r.y(), dir]
             for r, dir in zip( self.mobiles(), self._moves ) ]
        
        collisions= self.board().multiMoveHumans( multiMoves[self._nbRobots:] )
        collisions+= self.board().multiMoveRobots( multiMoves[:self._nbRobots] )
        
        # valide robot goals
        allOk= True
        for robot in self.mobiles()[:self._nbRobots] :
            robot.updateGoalSatifaction()
            allOk= allOk and robot.isGoalSatisfied()

        if collisions > 0 :
            # Dommage
            self._score -= self._maxTic * 10 * collisions
            
        if allOk :
            # Bravo
            self._score += self._countDownTic
            self.initializeCycle()
        elif self._countDownTic == 0 :
            # Too late
            self.initializeCycle()
        else :
            # step on the counter
            self._countDownTic-= 1

        # turn initialization
        self._moves= []

    def isEnded( self ):
        # if the counter reach it final value
        return self._countDownCycle == 0

    def playerScore( self, iPlayer ):
        # All players are winners.
        return self.score()/self._nbCycle

    # Board Managment:
    def setupObstacles(self):
        # initialize obstacles' positions:
        for iObst in range(self._nbObstacles) :
            options= self._board.cellsObstacleOk()
            if len(options) == 0 :
                break
            x, y= random.choice( options )
            self._board.at(x, y).setObstacle()

    def setupMobile(self):
        # initialize robot' positions:
        for robot in self._mobiles :
            x, y= random.choice( self._board.cellsEmpty() )
            robot.setPosition(x, y)
            self._board.at(x, y).attachMobile( robot )

    def initializeCycle(self):
        # initialize robot' Goals:
        goalOptions= self._board.cellsType( Cell.TYPE_FREE )
        for robot in self._mobiles :
            gx, gy= random.choice( goalOptions )
            robot.setGoal( gx, gy )
        # initialize cycle counters:
        self._countDownTic= self._maxTic
        self._countDownCycle-= 1
"""
