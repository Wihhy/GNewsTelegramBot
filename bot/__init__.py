from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gnews-telebot.sqlite'
db.init_app(app)

from .views import *
from .models import *

with app.app_context():
    db.create_all()
