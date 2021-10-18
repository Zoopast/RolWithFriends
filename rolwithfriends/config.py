import os

class Config:
    SECRET_KEY = os.environ["APP_SECRET_KEY"]
    MONGO_URI = os.environ["MONGO_URI"]
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ["MAIL_USERNAME"]
    MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
    CLOUDINARY_CLOUD_NAME = os.environ["CLOUDINARY_CLOUD_NAME"]
    CLOUDINARY_API_KEY= os.environ["CLOUDINARY_API_KEY"]
    CLOUDINARY_API_SECRET= os.environ["CLOUDINARY_API_SECRET"]