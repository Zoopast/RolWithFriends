from flask import render_template
from flask import Blueprint
from flask_login import login_required
from rolwithfriends import mongo
main = Blueprint('main', __name__)

def get_data(data):
     data['_id'] = str(data['_id'])
     return data

@main.route("/")
@main.route("/home")
def home():
    assets = [get_data(i) for i in mongo.db.Weapons.find()]
    return render_template('home.html', weapons = assets)

