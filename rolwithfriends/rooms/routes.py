from flask import render_template, Blueprint, url_for, redirect, flash
from flask_login import login_required
from rolwithfriends import mongo
from rolwithfriends.rooms.forms import CreateRoomForm
from flask_login import current_user
from flask_socketio import SocketIO, send
from rolwithfriends import socketio
import random

rooms = Blueprint('rooms', __name__)

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)


@rooms.route("/room/<int:roomId>",  methods=['GET', 'POST'])
@login_required

def room(roomId):
    roomId = mongo.db.Rooms.find_one({"roomId": roomId})
    if roomId:
        isInGame = False

        for character in roomId["characters"]:
            if character["owner"] == current_user.id:
                isInGame = True

        if isInGame:

            characters = []
            for character in roomId["characters"]:
                fChar = mongo.db.Characters.find_one({"_id": character["character"]})
                characters.append(fChar)

            if roomId['isActive'] == True and roomId["gm"] != current_user.id:
                return render_template("rooms/room.html", room = roomId, characters = characters)
            elif roomId['isActive'] == False and roomId["gm"] == current_user.id:
                return render_template("rooms/room.html", room = roomId, characters = characters)
            elif roomId['isActive'] == True and roomId["gm"] == current_user.id:
                return render_template("rooms/room.html", room = roomId, characters = characters)
            else:
                flash('There was a problem joining the game, please try again later', 'warning')
                return redirect(url_for("main.home"))            
        else:
            return redirect(url_for('characters.create_character', roomId = roomId["roomId"]))
    else:
        flash('No room with that number', 'warning')
        return redirect(url_for("main.home"))


@rooms.route("/createroom",  methods=['GET', 'POST'])
@login_required
def createroom():
    createRoomForm = CreateRoomForm()

    if createRoomForm.is_submitted():
        roomAvailable = False
        
        while roomAvailable == False:
            roomId = random.randint(0, 99) + 1
            searchRoomId = mongo.db.Rooms.find_one({"roomId": roomId})

            if not searchRoomId:
                roomAvailable = True

        newRoom = mongo.db.Rooms.insert_one({"roomId": roomId, "roomName": createRoomForm.roomName.data, "numberOfPlayers": int(createRoomForm.numberOfPlayers.data),
                                             "isPublic": createRoomForm.publicRoom.data, "allowSpectators": createRoomForm.allowSpectators.data,
                                             "log": [],
                                             "players": [], "characters": [], "gm": current_user.id, "isActive": createRoomForm.startGame.data})
        if newRoom:
            flash('Room created!', 'success')
            return redirect(url_for('rooms.room', roomId= roomId))
        else:
            flash('Something went wrong creating the room, please try again later', 'warning')
            return redirect(url_for('main.home'))

    return render_template("rooms/createroom.html", form = createRoomForm)
