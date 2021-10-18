from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from rolwithfriends import mongo
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=5, max=20) ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', 
                                      validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign up')

    def validate_username(self, username):
        isTaken = mongo.db.User.find_one({"username": username.data})

        if isTaken:
            raise ValidationError('That username is already taken, please choose a different one')

    def validate_email(self, email):
        isTaken = mongo.db.User.find_one({"email": email.data})

        if isTaken:
            raise ValidationError('That email is already taken, please choose a different one')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=5, max=20) ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            isTaken = mongo.db.User.find_one({"username": username.data})
            if isTaken:
                raise ValidationError('That username is already taken, please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            isTaken = mongo.db.User.find_one({"email": email.data})
            if isTaken:
                raise ValidationError('That email is already taken, please choose a different one')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request password reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', 
                                      validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')