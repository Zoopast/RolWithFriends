from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired
from rolwithfriends import mongo
from flask_login import current_user


class FindRoom(FlaskForm):
    roomId = IntegerField('Room number', validators=[DataRequired()])
    findRoom = SubmitField('Find room')

    