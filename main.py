from flask import Flask
import ZODB, ZODB.FileStorage
from utils.map import Map
from utils.player import Player

app = Flask(__name__)
debug = True

if __name__ == "__main__":
    if debug:
        print('Loading debug map...')
        map = Map(1)
        player = Player('Test')
        map.gen_level()
        map.gen_tiles_level()
        map.set_player(player)
        showMap = map.show_map(player)
        level = map.show_total_map(player)

        with open('camera.debug', 'w') as f:
            for row in showMap:
                f.write(row + '\n')

        with open('total.debug', 'w') as f:
            for row in level:
                f.write(row + '\n')
        print('End loading debug map...')
    app.run(host='0.0.0.0', port='5555')