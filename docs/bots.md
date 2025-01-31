# First Autonomous Player (Bot)

_MoveIt_ est basé sur _HackaGames_. 
Se référer à cette solution pour la philosophie du moteur de jeu, et des échanges entre le Maître de jeu et les joueurs.

- Documentation de HackaGames : [ktorz-net.github.io/hackagames/](https://ktorz-net.github.io/hackagames/)


Pour lancer son premier Bot sur _MoveIt_ il faut alors éditer un script de lancement comme suit (`launch.py` par exmple).

```python
import hacka.games.moveit as moveit
import playground

# Configure the game:
gameEngine= moveit.GameEngine()

# Then Go...
gameMaster= moveit.GameMaster( gameEngine, randomMission=2 )
player= playground.FirstBot()
gameMaster.launch( [player], gameEngine.numberOfPlayers() )
```

Cela supose naturellement d'avoir une class `FirstBot` dans un fichier `playground.py`, à côté de votre lanceur.

## Blanc Bot Player

_MoveIt_ se structure comme tout jeu _HackaGames_ avec un cycle global: `wakeUp` en début de partie et `sleep` en fin de partie, et un cycle rapide de tour de jeu avec `perceive` et `decide`.

```python
class FirstBot():
    # Player interface :
    def wakeUp(self, playerId, numberOfPlayers, gameConfiguration ):
        pass
    
    def perceive(self, state ):
        pass
    
    def decide(self):
        return "pass"
    
    def sleep(self, result):
        print( f"end on : {result}" )
```

Dans la mesure où `FirstBot` définit les méthodes appropriées avec les paramètres cohérents, une instance de `FirstBot` pourra jouer dans un jeu _HackaGames_. Naturellement, dans l'état, le résultat sera nul.

```sh
python3 launch.py
```

Le `gameConfiguration` de la méthode `wakeUp` définit le plateau de jeu.
Les cellules et comment elles sont connectées les unes aux autres. 
Au passage on a dés le `wakeUp`, la position des robots et le 'Market Place' avec les missions disponibles.

Ensuite, la méthode `perceive` avec comme paramètre `state` ne va renseigner que sur l'avancée du jeu. Le positionnement des robots sur le plateau et l'avancée des missions.

Cependant il n'est pas utile de rentre dans le détail des objets `gameConfiguration` et `state`. 
Il est possible de charger un modèle du jeu, avec la class `GameEngine` du package python `moveIt`.
Il sera alors possible de charger la configuration du jeu et de mettre à jour son état simplement:

```python
from hacka.games.moveit import GameEngine

...

def wakeUp(self, playerId, numberOfPlayers, gameConfiguration ):
    self._id= playerId
    self._model= GameEngine()
    self._model.fromPod(gameConfiguration)  # Load the model from gameConfiguration
    self._model.render()                    # Draw the game image in shot-moveIt.png

def perceive(self, state ):
    self._model.setOnState(state)           # Update the model sate
```

Then model will be queried through its methods (look at [inspect](https://docs.python.org/3/library/inspect.html) python package for instance). 


## _MoveIt_ Classes

_MoveIt_ game is mainly based on *3* classe: 

- `GameEngine`: it manages the game elements and the game rules.
- `Map`: based on `Hackapy::tiled.Map`, it represents the environment as a graph of interconnected tiles.
- `Mobile`: the mobile objects on the `Map` (Robots, and Vips).
- `Mission`: the mission objects with `start` and `final` positions plus `reward` and `owner` information.

### `GameEngine` Class's methods:

- **`numberOfPlayers()`** - Return the number of players.
- **`numberOfMobiles(iPlayer=1)`** - Return the number of robots owned by the player identifiate as `iPlayer` or vips, if `iPlayer=0`.
- **`mobile(iPlayer, iRobot)`** - Return the `iRobot`th robot as a `Mobile` instance of the player `iPlayer`. 
- **`mobilePosition(iPlayer, iRobot)`** - Return the position (tile identifier) of the `iRobot`th robot of the player `iPlayer`.
- **`missions()`** - Return all missions tuples.
- **`mission(iMission)`** - Return an object describing the `iMission`th mission (Mission has 4 integer attributes: the `start` tile id, the `final` tile id, the expected `reward` by terminating the mission and the mission `owner` id ($0$ if the mission is free).
- **`missionsList()`** - Return the list of active missions identifiers.
- **`freeMissions()`** - Return the list of mission identifier not allocated to any players.
- **`tic()`** - Return the counter on game turn.
- **`score(iPlayer):`** - Return the score of the `iPlayer` player.
- **`map()`** - Return the gameEngine map.


### `Map` Class's methods:

To notice that _MoveIt_ `Map` inherits from _HackaGames_ `Map`, with tile management and drawing handled at the parent level.

- **`size()`** - Return the number of tiles on the map.
- **`neighbours(iTile)`** - Return the tile's identifiers of connected tiles to the `iTile`th tile.
- **`clockBearing(iTile)`** - Retrun the list of possible movement for a mobile on the `iTile`th tile.
- **`clockposition(iTile, clockDir)`** - Return the identifier of reached tile by moving toward the `clockDir` direction from the `iTile`th tile.


### `Mobile` Class's methods:

- **`owner(self)`** - Retrun the owner identifier, the player number or $0$ if it is a Vip.
- **`identifier(self)`** - Return identifier in the owner's mobile lists (starting from $1$).
- **`mission(self)`** - Return the mission the mobile is in charge and $0$ if it does not have any.


## A simple first Bot Player

The idea is to create a robot, moving at random and activating a mission action if available.

but before to go, set your `launcher.py` with a very simple configuration : 

```python
gameEngine= moveit.GameEngine(
    matrix= [ [00, 00, 00],
              [00, 00, -1],
              [00, 00, 00] ],
    numberOfPlayers=1, numberOfRobot=1, tic= 20,
    missions= [(4, 3), (2, 5), (5, 7)]
)
```

### Moving at random:

The first part is quite simple. 
It requires to read robot position, to get possible movements and to choose one randomly.
According to the _MoveIT_ _API_, an informative implementation of `decide` method will lookalike: 

```python
    def decide(self):
        msg= f'tic-{ self._model.tic() } | score { self._model.score(self._id) }'
        r1Position= self._model.mobilePosition(self._id, 1)
        dirs= self._model.map().clockBearing(r1Position)
        msg+= f' | postion {r1Position} and actions {dirs}'
        self._move= random.choice(dirs)
        msg+= f' > move {self._move}'
        print( msg )
        return f"move 1 {self._move}"
```

To notice that, removing $0$ from the possible directions will allow the robot to move/explore more.

It is also possible to add sleeping and rendering in the perception method to visualize the robot behavior.

```python
    def perceive(self, gameState ):
        self._model.setOnState(gameState)
        self._model.render()
        time.sleep(0.2)
```

### Activating a mission action:

It becomes trickier a litlebit. It requires to compare the position of the robot with all possible missions.
It is tricky ? so create a specific method.
Always prefer to create new method compared to any other solution...

So let get possible mission identifiers starting at a given position:

```python
    def missionOn(self, iTile):
        i= 1
        l= []
        for m in self._model.missions() :
            if m.start == iTile :
                l.append(i)
            i+= 1
        return l
```

From that point we can start a mission if the robot does not have one (`self._model.mobile(1, 1).mission() == 0`) and if it is on a tile matching a mission start (`len( self.missionOn( robotPosition ) ) > 0`).

We also need to activate mission action when the robot reach the final point of the mission :

```python
        robot1Position= self._model.mobilePosition(self._id, 1)
        robot1Mission= self._model.mobile(1, 1).mission()
        if robot1Position == self._model.mission( robot1Mission ).final :
```

At this point our first bot should move randomly, and activate missions each time it is possible.


### Going further: Multi-Robots...

The proposed _FirstBot_ only handle one robot associated to the player. 
In case of multi-robot control, the _FirstBot_ should repeat the decision process over all robots by aggregating _'mission'_ and _'move'_ orders.

Then with multiple robots moving on a same environment, the AI should avoid collision.
A robot cannot target a position currently taken by another robot and tow robot cannot move on the same tile.
