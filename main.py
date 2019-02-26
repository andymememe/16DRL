import shelve
from flask import Flask, request, redirect, render_template, abort
from utils.map import Map
from utils.player import Player

APP = Flask(__name__)
DEBUG = True
PLAYER_DB = None

@APP.route('/')
def index():
    return render_template('index.html')
    
@APP.route('/login')
def login():
    id = request.values['_id']
    if id.startswith('16DRL_'):
        if id not in PLAYER_DB['player']:
            abort(404)
    else:
        # Init Map
        map = Map(13)
        player = Player(id)
        map.reset(player)
        showMap = map.show_map(player)
        level = map.show_total_map(player)
        
        # Save Map
        save(player, map)
        id = player.hashID
    return redirect("/map/" + id, code=303)

@APP.route('/map/<id>')
def map(id):
    player, map = loadData(id)
    return render_template('map_base.html', player=player, map=map)

@APP.route('/wear/<id>')
def wear(id):
    player, map = loadData(id)
    return render_template('map_wear.html', player=player, map=map)

@APP.route('/wear/<id>/<int:index>')
def wear_it(id, index):
    player, map = loadData(id)
    player.wear(index)
    map.update(player)
    save(player, map)
    return redirect("/map/" + player.hashID, code=303)

@APP.route('/use/<id>')
def use(id):
    player, map = loadData(id)
    return render_template('map_use.html', player=player, map=map)
    
@APP.route('/use/<id>/<int:index>')
def use_it(id, index):
    player, map = loadData(id)
    player.use(index)
    map.update(player)
    save(player, map)
    return redirect("/map/" + player.hashID, code=303)

@APP.route('/move/<id>/<dir>')
def move(id, dir):
    player, map = loadData(id)
    map.player_move(player, dir)
    map.update(player)
    save(player, map)
    
    if player.finished:
        if player.hp == 0:
            map.logs.append('You died!')
            return render_template('map_finished.html',
                                   player=player, map=map, message='Game Over')
        else:
            map.logs.append('You win!')
            return render_template('map_finished.html',
                                   player=player, map=map, message='You Win')
    else:
        return redirect("/map/" + player.hashID, code=303)

def save(player, map):
    PLAYER_DB['player'][player.hashID] = (player, map)

def loadData(id):
    if id in PLAYER_DB['player']:
        return PLAYER_DB['player'][id]
    else:
        abort(404)
    
if __name__ == "__main__":
    # Debug
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