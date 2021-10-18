from flask import render_template, Blueprint, url_for
from flask_login import login_required
from rolwithfriends import mongo

rooms = Blueprint('rooms', __name__)

@rooms.route("/room",  methods=['GET', 'POST'])
@login_required
def room():
    return render_template("rooms/room.html")

