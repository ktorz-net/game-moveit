"""
MoveIt - an HackaGame game 
"""

from . import tiled, artist
from . import mobile, map, gameengine, gamemaster, player

# TiledLand:
Artist= artist.Artist

# Game Component:
Mobile= mobile.Mobile
Map= map.Map

# Hackagame Game:
GameEngine= gameengine.Engine
GameMaster= gamemaster.Master

# Players
BasicBot= player.BasicBot
BlindBot= player.BlindBot
ShellPlayer= player.ShellPlayer
