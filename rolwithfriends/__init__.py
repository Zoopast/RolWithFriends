from flask import Flask
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_mail import Mail
from rolwithfriends.config import Config
from flask_socketio import SocketIO
import cloudinary
import os

mongo = PyMongo()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
cloudinary.config(cloud_name = Config.CLOUDINARY_CLOUD_NAME, 
                  api_key = Config.CLOUDINARY_API_KEY, api_secret = Config.CLOUDINARY_API_SECRET, secure = True)
mail = Mail()







def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app, tls=True, tlsAllowInvalidCertificates=True)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)



    from rolwithfriends.users.routes import users
    from rolwithfriends.main.routes import main
    from rolwithfriends.errors.handlers import errors
    from rolwithfriends.assets.routes import assets 
    from rolwithfriends.rooms.routes import rooms
    from rolwithfriends.characters.routes import characters

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(assets)
    app.register_blueprint(rooms)
    app.register_blueprint(characters)
    socketio.init_app(app)

    return app