import os
from PIL import Image
import secrets
from flask_mail import Message
from flask import url_for, current_app
from rolwithfriends import mail
import cloudinary
import cloudinary.uploader
import cloudinary.api
from rolwithfriends.config import Config
from io import BytesIO


def save_picture(form_picture):
    buf = BytesIO()
    
    i = Image.open(form_picture)
    
    i.save(buf, 'png')
    buf.seek(0)

    image_bytes = buf.read()

    picture_uploaded = cloudinary.uploader.upload(image_bytes,
                        eager=[{"width": 200, "height": 200, "crop": "pad"}], 
                        folder = "RolWithFriends/profile_pics/")
    print("Hola mundo")
    print(picture_uploaded)
    buf.close()
    return picture_uploaded['eager'][0]['secure_url']

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request', 
                  sender='noreply@demo.com', 
                  recipients=[user.email])
    msg.body = f'''To reset your password, please follow the link:
{url_for('users.reset_token', token=token, _external=True)}
    
    If you didn't request this reset, then simply just ignore this email an no changes will be made.
    '''
    mail.send(msg)

