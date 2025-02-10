# Frequent Asked Question

## Update _HackaGames_ and _MoveIt_

Using git and pip : 

```sh
git -C hackagames pull
git -C game-moveit pull
pip install ./hackagames
pip install ./game-moveit
```

## Make launcher _'configurable'_.

You can easely load and dumps structured data between python and files.
Json offer an simple an elegent solution to exange dictionaries, for instance.

From the _json_ side (`config-7x10.json`): 

```json
{
    "matrix": [
        [ 0,  0, -1,  0, -1,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0, -1,  0],
        [ 0,  0, -1, -1, -1, -1,  0,  0, -1,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0, -1,  0, -1, -1,  0,  0, -1, -1, -1],
        [ 0, -1,  0, -1, -1,  0,  0, -1, -1, -1],
        [ 0,  0,  0,  0,  0,  0,  0, -1, -1, -1]
    ],
    "tic": 50
}
```

On the python side: 

```python
import json

with open("./config-7x10.json") as file:
    dico= json.load(file)

# Configure the game:
gameEngine= moveit.GameEngine(
    matrix= dico['matrix'],
    tic= dico['tic'],
    numberOfPlayers=1, numberOfRobot=1,
    numberOfPVips= 1
)
```

Or: `open(sys.argv[1])` if you want to set the configuration file on the command line.
