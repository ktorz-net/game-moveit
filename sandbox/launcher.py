#!env python3
import hacka.games.moveit as moveit
from hacka.games.moveit.player import ShellPlayer
import bot, json, sys

#with open("./sandbox/config-7x10.json") as file:
with open( sys.argv[1] ) as file:
    dico= json.load(file)

# Configure the game:
gameEngine= moveit.GameEngine(
    matrix= dico['matrix'],
    tic= dico['tic'],
    numberOfPlayers= dico['numberOfPlayers'], numberOfRobots= dico['numberOfRobots'],
    numberOfPVips= dico['numberOfPVips']
)

# Then Go...
gameMaster= moveit.GameMaster( gameEngine, randomMission= dico['numberOfMissions'], vipZones= [1])
player= ShellPlayer()
#player= bot.VoidBot()
gameMaster.launch( [player, ShellPlayer()] )
