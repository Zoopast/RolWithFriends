from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired


class CreateRoomForm(FlaskForm):
    roomName = StringField('Room name', validators=[DataRequired()])
    numberOfPlayers = IntegerField('Number of players', validators=[DataRequired()])
    publicRoom = BooleanField('Public room')
    allowSpectators = BooleanField('Allow spectators')
    startGame = BooleanField('Start game at once')
    submit = SubmitField('Create new room')
