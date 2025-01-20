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

        #self._moveRePattern = re.compile( "^move "+ ' '.join(["[0123456]" for i in range(numberOfRobots)])+ "$" )
        #self._moveRePatShort = re.compile( "^"+ ' '.join(["[0123456]" for i in range(numberOfRobots)])+ "$" )
    
    # Game interface :
    def initialize(self):
        # Clean Up.
        #for tile in self._map.tiles() :
        #    tile.clear()
        # Initialize configuration :
        return self._engine.asPod("MoveIt")
    
    def playerHand( self, iPlayer ):
        # ping with the increasing counter
        pod= hk.Pod(
            'MoveIt', flags=[self._maxTic, self._countDownCycle],
            values= [self._score] )
        for mobileList in self.mobiles() :
            for robot in mobileList :
                pod.append( robot.asPod("Robot") )
        
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
        """
        for human in self._mobiles[self._nbRobots:] :
            x, y= human.position()
            gx, gy= human.goal()
            dir= self._map.path( x, y, gx, gy )[0]
            tx, ty= self._map.at_dir(x, y, dir)
            if self._map.at(tx, ty).mobile() :
                self._moves.append(0)
            else : 
                self._moves.append(dir)
        """

        # Extract mobiles' directions
        assert( len(self.mobiles()) == len(self._moves) )
        #multiMoves= [ [r.x(), r.y(), dir]
        #     for r, dir in zip( self.mobiles(), self._moves ) ]
        
        collisions= 0
        #collisions= self.board().multiMoveHumans( multiMoves[self._nbRobots:] )
        #collisions+= self.board().multiMoveRobots( multiMoves[:self._nbRobots] )
        
        # valide robot goals
        allOk= True
        #for robot in self.robots()[:self._nbRobots] :
        #    robot.updateGoalSatifaction()
        #    allOk= allOk and robot.isGoalSatisfied()

        if collisions > 0 :
            # Dommage
            self._score -= self._maxTic * 10 * collisions
            
        if allOk :
            # Bravo
            self._score= 0# += self._countDownTic
            #self.initializeCycle()
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
        return 0.0 #self.score()/self._nbCycle

    # Board Managment:

    # Artist rendering:
    def render(self):
        self.map.render( self._artist )
        return self
    
"""
    def setupObstacles(self):
        # initialize obstacles' positions:
        for iObst in range(self._nbObstacles) :
            options= self._map.cellsObstacleOk()
            if len(options) == 0 :
                break
            x, y= random.choice( options )
            self._map.at(x, y).setObstacle()

    def setupMobile(self):
        # initialize robot' positions:
        for robot in self._mobiles :
            x, y= random.choice( self._map.cellsEmpty() )
            robot.setPosition(x, y)
            self._map.at(x, y).attachMobile( robot )

    def initializeCycle(self):
        # initialize robot' Goals:
        goalOptions= self._map.cellsType( Cell.TYPE_FREE )
        for robot in self._mobiles :
            gx, gy= random.choice( goalOptions )
            robot.setGoal( gx, gy )
        # initialize cycle counters:
        self._countDownTic= self._maxTic
        self._countDownCycle-= 1
"""