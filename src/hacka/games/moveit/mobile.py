"""
Test - MoveIt Robot Class
"""

import hacka.py as hk

class Mobile(hk.Pod):
    FLAG_OWNER= 1
    FLAG_ID   = 2
    FLAG_MISSION = 3

    def __init__( self, owner=0, identif=0, mission= 0):
        name= f"R-{identif}"
        if owner == 0 :
            name= f"Vip{identif}"
        super().__init__( name, flags=[owner, identif, mission] )
        self._clockMove= 0

    # Accessor: 
    def owner(self):
        return self.flag( Mobile.FLAG_OWNER )
    
    def identifier(self):
        return self.flag( Mobile.FLAG_ID )
    
    def mission(self):
        return self.flag( Mobile.FLAG_MISSION )
    
    def setMission(self, iMission):
        self.setFlag( Mobile.FLAG_MISSION, iMission )

    def move(self):
        return self._clockMove

    def setMove(self, clockDir):
        self._clockMove= clockDir

class OldMobile(hk.PodInterface):
    TYPE_ROBOT= 0
    TYPE_HUMAN= 1
    
    #Construction: 
    def __init__(self, number, x=0, y=0, type= TYPE_ROBOT, hidenGoal= True):
        self._num= number
        self._x= x
        self._y= y
        self._dir= 0
        self._goalHiden= hidenGoal
        self._goalx= x
        self._goaly= y
        self._goalOk= False
        self._error= 0.0
        self._type= type
    
    # Pod interface:
    def asPod(self, family="Mobile"):
        if self._type == Mobile.TYPE_ROBOT :
            return hk.Pod( family, str(self._num),
                [self._x, self._y, self._dir,
                 self._goalx, self._goaly, int(self._goalOk)] )
        
        return hk.Pod( family, str(self._num),
            [self._x, self._y, self._dir] )
                
    def fromPod(self, aPod):
        self._num= int(aPod.status())
        self._x= aPod.flag(1)
        self._y= aPod.flag(2)
        self._dir= aPod.flag(3)
        if self._type == Mobile.TYPE_ROBOT :
            self._goalx= aPod.flag(4)
            self._goaly= aPod.flag(5)
            self._goalOk= bool(aPod.flag(6))
            self._goalHiden=False

    def copy(self):
        newOne= Mobile( self.number(), self.x(), self.y(), self.type() )
        newOne.setError( self.error() )
        newOne.setGoal( self.goalx(), self.goaly() )
        return newOne

    # Accessor: 
    def number(self): 
        return self._num
    
    def x(self):
        return self._x
    
    def y(self):
        return self._y

    def position(self):
        return self._x, self._y
    
    def direction(self):
        return self._dir

    def goal(self):
        return self._goalx, self._goaly
    
    def goalx(self):
        return self._goalx
    
    def goaly(self):
        return self._goaly

    def isGoalHiden(self):
        return self._goalHiden
    
    def isGoalSatisfied(self):
        return self._goalOk

    def error(self):
        return self._error
    
    def isRobot(self):
        return self._type == Mobile.TYPE_ROBOT
    
    def isHuman(self):
        return self._type == Mobile.TYPE_HUMAN
    
    def type(self):
        return self._type
    
    # Modifier
    def setPosition(self, x, y):
        self._x= x
        self._y= y
    
    def setDirection(self, dir):
        self._dir= dir
    
    def setGoal(self, x, y):
        self._goalx= x
        self._goaly= y
        self._goalOk= False
        self._goalHiden= False

    def updateGoalSatifaction(self):
        self._goalOk= self._goalOk or ( self.position() == self.goal() )
        return self._goalOk
        
    def setError(self, aValue):
        assert( -0.1 < aValue and aValue <= 1.1 )
        self._error= aValue
    
    def setRobot(self):
        self._type= Mobile.TYPE_ROBOT

    def setHuman(self):
        self._type= Mobile.TYPE_HUMAN

    # str
    def __str__(self):
        s= "Robot"
        if self.isHuman() :
            s= "Human"
        s+= f"-{self._num}[on({self._x}, {self._y}), dir({self._dir}), "
        if not self.isGoalHiden() :
            s+= f"goal({self._goalx}, {self._goaly})-{ str(self._goalOk)[0]}, "
        s+= f"error({self._error})]"
        return s
