import re, hacka.pylib as hk
from hacka.artist import Artist
import hacka.tiled as htiled

from .mobile import Mobile

class GameMaster( hk.AbsSequentialGame ) :

    # Initialization:
    def __init__( self, seed=False, numberOfPlayers=1, numberOfRobots=2 ) :
        super().__init__( numberOfPlayers )
        self._seed= seed
        self._board= htiled.Board()
        self._robots= [ Mobile(i+1) for i in range(numberOfPlayers*numberOfRobots) ]
        self._nbRobots= numberOfRobots
        self._moves= []
        self._maxTic= 100
        self._countDownCycle= 100
        self._score= [0 for p in range(numberOfPlayers) ]
        self._moveRePattern = re.compile( "^move "+ ' '.join(["[0123456]" for i in range(numberOfRobots)])+ "$" )
        self._moveRePatShort = re.compile( "^"+ ' '.join(["[0123456]" for i in range(numberOfRobots)])+ "$" )
        
        # Artist:
        self._artist= Artist().initializePNG( "shot-moveIt.png" )

    # accessor:
    def board(self): 
        return self._board

    def score(self):
        return self._score

    def robots(self):
        return self._robots

    # Construction:
    def initializeBoardGrid(self, matrix, size, separetion):
        self._board.initializeSquares( matrix, size, separetion )
        self._board.connectAllCondition(
            lambda tileFrom, tileTo : tileFrom.centerDistance( tileTo ) < 1.2
        )
        self._artist.fitBox( self._board.box(), 10 )
        return self

    def popRobot(self, playerId, tileId ):
        robot= htiled.Piece( f"R{playerId}{0}", playerId , (0, 0), 0.7 )
        robot._envs= [ (x+0.08, y+0.08) for x, y in robot._envs ]
        self._board.tile(tileId).addPiece( robot )

    # Game interface :
    def initialize(self):
        # clean Up.
        for tile in self._board.tiles() :
            tile.clear()
        
        pod= self._board.asPod("MoveIt")
        return pod
    
    def playerHand( self, iPlayer ):
        # ping with the increasing counter
        pod= hk.Pod(
            'MoveIt', flags=[self._maxTic, self._countDownCycle],
            values= [self._score] )
        for robot in self._robots :
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
            dir= self._board.path( x, y, gx, gy )[0]
            tx, ty= self._board.at_dir(x, y, dir)
            if self._board.at(tx, ty).mobile() :
                self._moves.append(0)
            else : 
                self._moves.append(dir)
        """

        # Extract mobiles' directions
        assert( len(self.robots()) == len(self._moves) )
        multiMoves= [ [r.x(), r.y(), dir]
             for r, dir in zip( self.robots(), self._moves ) ]
        
        collisions= 0
        #collisions= self.board().multiMoveHumans( multiMoves[self._nbRobots:] )
        #collisions+= self.board().multiMoveRobots( multiMoves[:self._nbRobots] )
        
        # valide robot goals
        allOk= True
        for robot in self.robots()[:self._nbRobots] :
            robot.updateGoalSatifaction()
            allOk= allOk and robot.isGoalSatisfied()

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
        # Board:
        self._artist.drawBoard( self._board )
        # Market:
        self._artist.drawPolygon(
            [6.55, 6.55, 9.5, 9.5], [2.45, -0.6, -0.6, 2.45],
            self._artist._panel[6]
        )
        # Finalize:
        self._artist.flip()
        return self
    
"""
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