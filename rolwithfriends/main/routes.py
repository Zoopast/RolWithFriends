from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import login_required
from rolwithfriends.main.forms import FindRoom
from rolwithfriends import mongo

main = Blueprint('main', __name__)

def get_data(data):
     data['_id'] = str(data['_id'])
     return data

@main.route("/home", methods=['GET', 'POST'])
@main.route("/", methods=['GET', 'POST'])
def home():
    roomNumber = FindRoom()
    if  roomNumber.is_submitted():
         findRoom = mongo.db.Rooms.find_one({"roomNumber": int(roomNumber.roomId.data)})
         if findRoom:
              return redirect(url_for('rooms.room'))
         else:
              flash('Room number does not exist!', 'warning')
    assets = [get_data(i) for i in mongo.db.Weapons.find()]
    return render_template('home.html', weapons = assets, form = roomNumber)

