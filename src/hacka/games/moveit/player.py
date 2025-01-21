import time
from hacka import AbsPlayer
from .gameengine import Engine


class BasicBot( AbsPlayer ):

    # Constructor:
    def __init__(self):
        super().__init__()
        self._model= Engine()
        self._id= 0
        self._sumResult= 0.0
        self._countResult= 0

    # Accessor:
    def model(self):
        return self._model
    
    def playerId(self):
        return self._id
    
    def averageResult(self):
        return (self._sumResult/self._countResult)

    # Construction
    def resetResult(self):
        self._sumResult= 0.0
        self._countResult= 0
        return self

    # Player interface :
    def wakeUp(self, playerId, numberOfPlayers, gamePod):
        # Initialize from gamePod:
        self._model.fromPod(gamePod)
        self._id= playerId

    def perceive(self, statePod):
        # update the game state:
        self._model.setOnState(statePod)

    def decide(self):
        return "pass"
    
    def sleep(self, result):
        self._sumResult+= result
        self._countResult+= 1

class ShellPlayer( BasicBot ):
    def __init__(self):
        super().__init__()
        self._action= "go"
    
    # Player interface :
    def wakeUp(self, playerId, numberOfPlayers, gamePod):
        super().wakeUp(playerId, numberOfPlayers, gamePod)
        self.model().render()
        print( f"Output image : ./{self.model().filePath()}" )
        self._action= "go"

    def perceive(self, statePod):
        super().perceive(statePod)
        self.model().render()

    def decide(self):
        if self._action != "stop" :
            self._action = input('Enter your action ([mission r m] move r c OR pass): ')
        if self._action == "stop" :
            return "pass"
        return self._action
