from flask import Flask
import ZODB, ZODB.FileStorage
from utils.map import Map
from utils.player import Player

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5555')