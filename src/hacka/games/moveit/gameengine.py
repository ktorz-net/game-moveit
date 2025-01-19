
import copy, hacka

from .map import Map

class Engine():

    def __init__( self, matrix= [[0, 0, 0],[0, -1, 0],[0, 0, 0]] ):
        self._map= Map()
        self._map.initializeGrid( copy.deepcopy(matrix), 0.9, 0.1 )
        self._artist= hacka.artist.Artist().initializePNG( "shot-moveIt.png" )
        self._artist.flip()
        self._artist.fitBox( [(-0.5, -0.5), (9.5, 6.5)], 10 )#self._map.box(), 10 )

    # Rendering :
    def render(self):
        self._artist.drawMap( self._map )
        # Market:
        self._artist.drawPolygon(
            [6.55, 6.55, 9.5, 9.5], [2.45, -0.6, -0.6, 2.45],
            self._artist._panel[6]
        )
        # Finalize:
        self._artist.flip()
