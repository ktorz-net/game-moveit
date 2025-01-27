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

## Squelette de joueur:

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

Dans la mesure ou `FirstBot` définie les méthodes appropriées avec les parramétres cohérents, une instance de `FirstBot` pourra jouer dans un jeu _HackaGames_. Naturellement, dans l'état, le résultat sera null.

```sh
python3 launch.py
```

Le `gameConfiguration` de la méthode `wakeUp` défini le plateau de jeu.
Les cellules et comment elles sont connecté les unes au autre. 
Au passage on a dés le `wakeUp`, la position des robots et le 'Market Place' avec les missions diponible.

Ensuite, la méthode `perceive` avec cont parramétre `state` ne va renseigner que sur l'avancé du jeux. Le positionnement des robots surle plateau et l'avancé des missions.

Cependant il n'est pas utile de rentre dans le détail des object `gameConfiguration` et `state`. 
Il est possible de charger un modéle du jeu, avec la class `GameEngine` du package python `moveIt`.
Il sera alors possible de carger la caonfiguration du jeu et de mettre à jour son état simplement:

```python
from hacka.games.moveit import GameEngine

...

def wakeUp(self, playerId, numberOfPlayers, gameConfiguration ):
    self._model= GameEngine()
    self._model.fromPod(gameConfiguration)  # Load the model from gameConfiguration
    self._model.render()                    # Draw the game image in shot-moveIt.png

def perceive(self, state ):
    self._model.setOnState(state)           # Update the model sate
```

Then model will be querry throught its methods (look at [inspect](https://docs.python.org/3/library/inspect.html) python package for instance). 

## _MoveIt_ model (GameEngine class):

Let take a look at `GameEngine` accessor methods:

```python
    def numberOfPlayers(self):
```

Return the number of players.


```python
    def numberOfRobots(self, iPlayer=1):
```

Return the number of robots owned by the player identifiate as `iPlayer`.

```python
    def mobile(self, iPlayer, iRobot):
```

Return the `iRobot`th robot as a `Mobile` instance of the player `iPlayer`. 
A `Mobile` as several well named methods:  `owner()` (should be equal to `iPlayer`), `identifier()` (should be equal to `iRobot`) and `mission()` the identifier of the current robot mission.

```python
    def mobilePosition(self, iPlayer, iRobot):
```

return the position (tile identifier) of the `iRobot`th robot of the player `iPlayer`.

```python
    def missions(self):
```

return all missions tuples.

```python
    def mission(self, iMission):
```

Return the tuple describing the `iMission`th mission (tile from, tile to, payment, allocation to player)

```python
    def missionsList(self):
```

return the list of active missions identifiers.


```python
    def freeMissions(self):
```

Return the list of mission identifier not allocated to any players.


```python
    def tic( self ):
```

Return the counter on game turn.


```python
    def score(self, iPlayer):
```

Return the score of the `iPlayer` player.
