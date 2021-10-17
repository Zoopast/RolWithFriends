from rolwithfriends import mongo, login_manager
from flask_login import UserMixin
from flask import current_app
from bson.objectid import ObjectId
from bson import json_util
import json
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.User.find_one({"_id": ObjectId(user_id)})
    loggedUser = User(user)
    return loggedUser

class User(UserMixin):

    def __init__(self, newUser):
        self.id = newUser['_id']
        self.username = newUser['username']
        self.email = newUser['email']
        self.image_file = newUser['image_file']
        self.password = newUser['password']
        self.role = newUser['role']

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        print("Aqui si!")
        return s.dumps({'user_id': json.loads(json_util.dumps(self.id))}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        print(token)
        s = Serializer(current_app.config['SECRET_KEY'])
        print(s)
        try:
            user_id = s.loads(token)['user_id']
            user_id_mongo = {"_id": user_id['$oid']}
        except:
            return None
        user = mongo.db.User.find_one({"_id": ObjectId(user_id_mongo['_id'])})
        return User(user)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
