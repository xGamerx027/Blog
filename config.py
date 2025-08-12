import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'TekomoNakama')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db'
    UPLOAD_FOLDER = 'static/uploads'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///blog.db')
