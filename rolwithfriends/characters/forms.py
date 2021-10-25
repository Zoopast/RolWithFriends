from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class CreateCharacterForm(FlaskForm):
    cName = StringField('Character name', validators=[DataRequired()])
    bgStory = TextAreaField('Character background story', validators=[DataRequired()])
    cImage = FileField('Character portrait', validators=[FileAllowed(['jpg', 'png'])])
    cAvatar = FileField('Character avatar', validators=[FileAllowed(['jpg', 'png'])])
    cRace = SelectField('Character race', validators=[DataRequired()], choices=[('human','Human'), ('dwarf','Dwarf'), ('warewolf','Warewolf'), 
                                                                                 ('undead','Undead'), ('orc','Orc'), ('fairy','fairy'),
                                                                                 ('naga','Naga'), ('dragonborn','Dragonborn')])
    cClass = SelectField('Character race', validators=[DataRequired()], choices=[('fighter','Fighter'), ('dark wizard','Dark wizard'), ('warrior','Warrior'), 
                                                                                 ('monk','Monk')])
    cHeight = IntegerField('Character height (cm)', validators=[DataRequired()])
    cWeight = IntegerField('Character weight (Kg)', validators=[DataRequired()])
    cLanguage = SelectField('Character language', validators=[DataRequired()], choices=[('spanish','Spanish')])
    submit = SubmitField('Create character')
