import shelve
from flask import Flask, request, redirect, render_template, abort
from utils.map import Map
from utils.player import Player

DEBUG = True
PLAYER_DB = None
APP = Flask(__name__)

@APP.route('/')
def index():
    return render_template('index.html')
    
@APP.route('/login', methods=['POST'])
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
        _ = map.show_map(player)
        _ = map.show_total_map(player)
        
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
    return render_template('map_items.html',
                           player=player, map=map,
                           usage='wear',
                           objs=player.getWearable())

@APP.route('/wear/<id>/<int:index>')
def wear_it(id, index):
    player, map = loadData(id)
    player.wear(index, map)
    map.update(player)
    save(player, map)
    return redirect("/map/" + player.hashID, code=303)

@APP.route('/use/<id>')
def use(id):
    player, map = loadData(id)
    return render_template('map_items.html',
                           player=player, map=map,
                           usage='use',
                           objs=player.getUsable())
    
@APP.route('/use/<id>/<int:index>')
def use_it(id, index):
    player, map = loadData(id)
    player.use(index, map)
    map.update(player)
    save(player, map)
    return redirect("/map/" + player.hashID, code=303)

@APP.route('/move/<id>/<dir>')
def move(id, dir):
    player, map = loadData(id)
    
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
        map.player_move(player, dir)
        map.update(player)
        save(player, map)
        return redirect("/map/" + player.hashID, code=303)

def save(player, map):
    PLAYER_DB['player'][player.hashID] = (player, map)

def loadData(id):
    if id in PLAYER_DB['player']:
        return PLAYER_DB['player'][id]
    else:
        abort(404)
    
if __name__ == "__main__":    
    # Main Function
    try:
        PLAYER_DB = shelve.open('storage/db.shelf', writeback=True)
        if 'player' not in PLAYER_DB:
            PLAYER_DB['player'] = {}
        APP.run(host='0.0.0.0', port='5555', debug=DEBUG)
    except Exception as e:
        print(str(e))
    finally:
        if PLAYER_DB is not None:
            PLAYER_DB.sync()
            PLAYER_DB.close()