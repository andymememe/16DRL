import shelve
from flask import Flask
from utils.map import Map
from utils.player import Player

APP = Flask(__name__)
DEBUG = True
PLAYER_DB = None

if __name__ == "__main__":
    if DEBUG:
        print('Loading debug map...')
        map = Map(1)
        player = Player('Test')
        map.reset(player)
        showMap = map.show_map(player)
        level = map.show_total_map(player)

        with open('camera.debug', 'w') as f:
            for row in showMap:
                for col in row:
                    f.write(col)
                f.write('\n')

        with open('total.debug', 'w') as f:
            for row in level:
                for col in row:
                    f.write(col)
                f.write('\n')
        print('End loading debug map...')
    
    # Main Function
    try:
        PLAYER_DB = shelve.open('storage/db.shelf', writeback=True)
        if 'player' not in PLAYER_DB:
            PLAYER_DB['player'] = {}
        APP.run(host='0.0.0.0', port='5555')
    except Exception as e:
        print(str(e))
    finally:
        if PLAYER_DB is not None:
            PLAYER_DB.sync()
            PLAYER_DB.close()