"""
Test - MoveIt Hexagonal-cells' board Class
"""
import sys

sys.path.insert( 1, __file__.split('gameMoveIt')[0] )
from ... import core as hk

import random

class Cell:
    TYPE_FREE= 0
    TYPE_OBSTACLE= 1

    # Construction:
    def __init__(self):
        self._type= Cell.TYPE_FREE
        self._mobile= False

    def setFree(self):
        self._type= Cell.TYPE_FREE

    def setObstacle(self):
        self._type= Cell.TYPE_OBSTACLE

    def attachMobile(self, aMobile):
        if self._type == Cell.TYPE_FREE and not self._mobile :
            self._mobile= aMobile
            return True
        return False

    def removeMobile(self):
        r= self._mobile
        self._mobile= False
        return r
        
    # Accessors: 
    def type(self):
        return self._type

    def mobile(self):
        return self._mobile

    def isObstacle(self):
        return self.type() == Cell.TYPE_OBSTACLE
    
    def isAvailable(self):
        return not ( self.isObstacle() or bool(self._mobile) )

class Hexaboard(hk.PodInterface):
    DIRECTIONS= [ [(0, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 0), (-1, 1)],
                    [ (0, 0), (1, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (0, 1)] ]

    # Construction:
    def __init__(self, sizeLine= 8, numberLine= 6):
        self.reset( sizeLine, numberLine )

    def reset(self, sizeLine, numberLine):
        self._sizeLine= sizeLine
        self._nbLine= numberLine
        self._lines= [[ Cell() for i in range(self._sizeLine) ] for j in range(self._nbLine) ]

    # Pod interface:
    def asPod(self, family="Board"):
        pod= hk.Pod( family, "", [ self._sizeLine, self._nbLine ] )
        cellType= [ "FREE", "OBSTACLE" ]
        for line in self._lines :
            podLine= hk.Pod( "Line" )
            for cell in line :
                podLine.append( hk.Pod( "Cell", cellType[cell.type()] ) )
            pod.append( podLine )

        return pod
    
    def fromPod(self, aPod):
        self.reset( aPod.flag(1), aPod.flag(2) )
        iLine= 0
        for podLine in aPod.children() :
            iCell= 0
            for podCell in podLine.children() :
                if podCell.status() == "OBSTACLE" :
                    self.at(iCell, iLine).setObstacle()
                iCell+= 1
            iLine+= 1
        return self
    
    def copy(self):
        newOne= Hexaboard().fromPod( self.asPod() )
        for y in range( self._nbLine ) :
            for x in range( self._sizeLine ) :
                if self.at(x, y).mobile() :
                    newOne.setMobile_at( 
                        self.at(x, y).mobile().copy(), x, y)
        return newOne

    # Accessors: 
    def size(self):
        return (self._sizeLine, self._nbLine)

    def at(self, x, y):
        return self._lines[y][x]
    
    def at_dir(self, x, y, i):
        dx, dy= Hexaboard.DIRECTIONS[ y%2 ][i]
        return x+dx, y+dy

    def movesFrom(self, x, y):
        dirs= []
        for i in range(7) :
            targetX, targetY= self.at_dir( x, y, i )
            if self.isCoordinate( targetX, targetY ) and not self.at( targetX, targetY ).isObstacle() :
                dirs.append( i )
        return dirs

    def isCoordinate(self, x, y):
        return 0 <= x and x < self._sizeLine and 0 <= y and y < self._nbLine 

    def cellsType(self, aType ):
        options= []
        for y in range( self._nbLine ) :
            for x in range( self._sizeLine ) :
                if self.at(x, y).type() == aType :
                    options.append( (x, y) )
        return options
    
    def cellsEmpty( self ):
        options= []
        for y in range( self._nbLine ) :
            for x in range( self._sizeLine ) :
                if self.at(x, y).type() == Cell.TYPE_FREE and not self.at(x, y).mobile() :
                    options.append( (x, y) )
        return options
    
    def isObstacleOkAt(self, x, y):
        neighbours= self.movesFrom(x, y)
        if self.at(x, y).type() == Cell.TYPE_OBSTACLE :
            return False
        if neighbours == [0] :
            return True
        
        cuts= 0
        if neighbours[1] != 1 or neighbours[-1] != 6 :
            cuts= 1
        for i in range(1, len(neighbours)-1) :
            if neighbours[i]+1 != neighbours[i+1] :
               cuts+= 1
        return cuts < 2
    
    def cellsObstacleOk( self ):
        options= []
        for y in range( self._nbLine ) :
            for x in range( self._sizeLine ) :
                if self.isObstacleOkAt(x, y) :
                    options.append( (x, y) )
        return options
    
    def mobiles(self):
        nonordonedMobiles= []
        for y in range( self._nbLine ) :
            for x in range( self._sizeLine ) :
                if self.at(x, y).mobile() :
                    nonordonedMobiles.append( self.at(x, y).mobile() )
        mobiles= [ False for m in nonordonedMobiles ]
        for m in nonordonedMobiles :
            mobiles[ m.number()-1 ]= m
        return mobiles    

    # Clear: free all cells:
    def clear(self):
        for y in range( self._nbLine ) :
            for x in range( self._sizeLine ) :
                self.at(x, y).setFree()
                self.at(x, y).removeMobile()
                
    # Mobile Manipulation:
    def mobilesFromPod( self, pod ):
        mobiles= []
        # Search the robots:
        for y in range( self._nbLine ) :
            for x in range( self._sizeLine ) :
                robot= self.at(x, y).mobile()
                if robot :
                    robot.fromPod( pod.child( robot.number() ) )
                    self.at(x, y).removeMobile()
                    mobiles.append(robot)
        
        # Install the robots:
        for m in mobiles :
            self.at( m.x(), m.y()).attachMobile( m )
        return mobiles

    def setupMobiles(self, mobiles):
        options= self.cellsEmpty()
        # initialize robot' positions:
        i= 0
        for m in mobiles :
            x, y= options[i]
            m.setPosition(x, y)
            self.at(x, y).attachMobile( m )
            i+= 1

    def setMobile_at(self, robot, x, y):
        if self.at(x, y ).attachMobile( robot ) :
            robot.setPosition(x, y)
            return True
        return False
    
    def teleportMobile(self, x, y, tx, ty):
        robot= self.at( x, y ).mobile()
        if robot and (x, y) == (tx, ty) :
            return True
        if robot and self.isCoordinate( tx, ty ) and self.at( tx, ty ).isAvailable() :
            self.at(tx, ty).attachMobile( robot )
            robot= self.at( x, y ).removeMobile()
            robot.setPosition(tx, ty)
            return True
        return False
    
    def moveMobileAt_dir(self, x, y, dir):
        robot= self.at( x, y ).mobile()
        if robot : 
            robot.setDirection(0)
            if dir != 0 and random.random() < robot.error() :
                dir= random.choice( self.movesFrom(x, y) )
            targetX, targetY= self.at_dir( x, y, dir )
            if self.teleportMobile(x, y, targetX, targetY):
                robot.setDirection( dir )
                return True
        return False

    def multiMoveHumans(self, moves):
        nbCollision= 0
        reserved= []
        for m in moves :
            tx, ty= self.at_dir( m[0], m[1], m[2] )
            if (tx, ty) in reserved :
                m[2]= 0
            else :
                reserved.append( (tx, ty) )
        for m in moves :
            if not self.moveMobileAt_dir( m[0], m[1], m[2] ) :
                nbCollision+= 1
        return nbCollision

    def multiMoveRobots(self, moves):
        nbCollision= 0
        reserved= {}
        # Reserve:
        for m in moves :
            tx, ty= self.at_dir( m[0], m[1], m[2] )
            if (tx, ty) in reserved :
                reserved[(tx, ty)]+= 1
            else :
                reserved[(tx, ty)]= 1
        # Execute:
        for m in moves :
            tx, ty= self.at_dir( m[0], m[1], m[2] )
            if reserved[(tx, ty)] == 1 or m[2] == 0 :
                if not self.moveMobileAt_dir( m[0], m[1], m[2] ) :
                    nbCollision+= 1
            else:
                nbCollision+= 1
        return nbCollision
    
    def path(self, x1, y1, x2, y2):
        if ( (x1, y1) == (x2, y2) ) :
            return [0]
        tested= [ (x1, y1) ]
        pathes= [ [] ]
        while len( pathes ) > 0 :
            path= pathes.pop(0)
            px, py= x1, y1
            for dir in path :
                px, py= self.at_dir( px, py, dir )
            for dir in self.movesFrom(px, py)[1:] :
                x, y = self.at_dir( px, py, dir )
                if (x, y) == (x2, y2) :
                    return path+[dir]
                elif (x, y) not in tested :
                    pathes.append( path+[dir] )
                    tested.append( (x, y) )
        return [0] 


    # Print:
    def shell_coord(self, ix, iy):
        if iy%2 == 0 :
            return ix*10+5, iy*3+3
        return ix*10+10, iy*3+3
        
    def shell_freeCell(self, b, ix, iy):
        x, y= self.shell_coord(ix, iy)
        b[y+1][x-3],b[y+1][x-2], b[y+1][x+2], b[y+1][x+3]= "▖","▝","▘","▗"
        b[y][x-5], b[y][x+5]= "█", "█"
        b[y-1][x-5], b[y-1][x+5]= "█", "█"
        b[y-2][x-3],b[y-2][x-2], b[y-2][x+2], b[y-2][x+3]= "▘","▗","▖","▝"
        robot= self.at(ix, iy).mobile()
        if robot :
            b[y+1][x-1], b[y+1][x], b[y+1][x+1]= '▁', '▁', '▁'
            b[y][x-2], b[y][x-1], b[y][x+2]=     "⎛", "R", "⎞"
            b[y-1][x-2], b[y-1][x], b[y-1][x+2]= "⎝", " ", "⎠"
            b[y-2][x-1], b[y-2][x], b[y-2][x+1]= '▔', '▔', '▔'
            if robot.isHuman() :
                b[y][x-1]= "H"
            
            num= str(robot.number())
            l= len(num)
            for i in range(l):
                    b[y-1][x-l+i+2]= num[i]
            
            if not robot.isGoalHiden() :
                xg, yg= robot.goal()
                xg, yg= self.shell_coord( xg, yg )
                b[yg][xg-3], b[yg][xg+3]= '⎡', '⎤'
                b[yg-1][xg-3], b[yg-1][xg+3]= '⎣', '⎦'
                for i in range(l):
                    b[yg+l-i-2][xg+4]= num[i]

        return x, y
    
    def shell_obsCell(self, b, ix, iy):
        y, x= iy*3+3, ix*10+10
        if iy%2 == 0 :
            x = ix*10+5
        b[y+1][x-3],b[y+1][x-2], b[y+1][x+2], b[y+1][x+3]= "▄","▟","▙","▄"
        
        for l, c in [(y-2, x-3), (y-2, x+3) ]:
            if b[l][c] in ["▟","▙"] :
                b[l][c]= "█"
            else :
                b[l][c]= "▀"
        
        if b[y-2][x-2] == "▄" :
            b[y-2][x-2]= "█"
        else :
            b[y-2][x-2]= "▜"
        
        if b[y-2][x+2] == "▄" :
            b[y-2][x+2]= "█"
        else :
            b[y-2][x+2]= "▛"
        
        fill= [ (y-2, c) for c in range( x-1, x+2, 1 ) ]
        fill+= [ (y-1, c) for c in range( x-5, x+6, 1 ) ]
        fill+= [ (y, c) for c in range( x-5, x+6, 1 ) ]
        fill+= [ (y+1, c) for c in range( x-1, x+2, 1 ) ]
        for l, c in fill :
            b[l][c]= "█"
        return x, y

    def shell(self): 
        # Initialize the char buffer
        bufSize= 6 + self._sizeLine*10
        buffer= [ [ " " for c in range( bufSize ) ] for l in range( 3 + self._nbLine*3 ) ]
        
        iPlus= 0
        if self._nbLine %2 == 0 :
            iPlus= 5
        for i in range(5, bufSize-5, 10 ) :
            buffer[0][i]= "▔"
            buffer[-1][i+iPlus]= "▁"
        
        # Draw the grid
        obsCell= []
        for iL in range(self._nbLine) :
            for iC in range(self._sizeLine) :
                if self.at( iC, iL ).type() == Cell.TYPE_OBSTACLE :
                    obsCell.append( [iC, iL] )
                else:
                    self.shell_freeCell( buffer, iC, iL )

        for c in obsCell:
            self.shell_obsCell( buffer, c[0], c[1] )

        # Fill the cells
        # Send it
        return "\n".join( [ "".join( line ) for line in reversed(buffer) ] )