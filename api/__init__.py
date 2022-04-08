__version__ = '0.1.0'

from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/')
def greet():
    return {"msg": "Jai shree ram 🙏 "}    

@app.route('/room', methods = ['POST'])
def createRoomDetails():
    pass

@app.route('/room/<roomId>')
def getRoomDetails():
    pass

@app.route('/room/<roomId>', methods = ['PATCH'])
def updateRoomDetails():
    pass

@app.route('/room/<roomId>', methods = ['DELETE'])
def deleteRoomDetails():
    pass

@app.route('/room')
def listAllRooms():
    pass