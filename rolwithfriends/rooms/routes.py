from flask import render_template, Blueprint, url_for, redirect, flash
from flask_login import login_required
from rolwithfriends import mongo
from rolwithfriends.rooms.forms import CreateRoomForm
from flask_login import current_user
import random


rooms = Blueprint('rooms', __name__)

@rooms.route("/room/<int:roomId>",  methods=['GET', 'POST'])
@login_required
def room(roomId):
    roomId = mongo.db.Rooms.find_one({"roomId": roomId})
    print("Hola mundo")
    if roomId:
        print("Adios mundo!")
        if roomId['isActive'] == True and roomId["gm"] != current_user.id:
            return render_template("rooms/room.html", room = roomId)
        elif roomId['isActive'] == False and roomId["gm"] == current_user.id:
            return render_template("rooms/room.html", room = roomId)
        elif roomId['isActive'] == True and roomId["gm"] == current_user.id:
            return render_template("rooms/room.html", room = roomId)
        else:
            flash('There was a problem joining the game, please try again later', 'warning')
            return redirect(url_for("main.home"))            
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
                                             "players": [], "characters": [], "gm": current_user.id, "isActive": createRoomForm.startGame.data})
        flash('Room created!', 'success')
        return redirect(url_for('rooms.room', roomId= roomId))


    return render_template("rooms/createroom.html", form = createRoomForm)
