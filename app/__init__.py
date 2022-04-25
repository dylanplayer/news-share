from flask import Flask, redirect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app.config import Config
import os

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get('SECRET')

db = SQLAlchemy(app)

from app.controllers.users import users
from app.controllers.main import main

app.register_blueprint(users)
app.register_blueprint(main)

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)

from app.models import User
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

with app.app_context():
  db.create_all()
