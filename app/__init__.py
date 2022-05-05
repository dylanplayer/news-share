from flask import Flask, redirect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment, Bundle
from dotenv import load_dotenv
from app.config import Config
import os

load_dotenv()

app = Flask(__name__)

app.config.from_object(Config)
app.secret_key = os.environ.get('SECRET')

db = SQLAlchemy(app)

assets = Environment(app)
assets.url = app.static_url_path

scss = Bundle("assets/main.scss", filters="libsass", output="css/scss-generated.css")
assets.register("scss_all", scss)

js = Bundle("assets/node_modules/jquery/dist/jquery.min.js", "assets/node_modules/@popperjs/core/dist/umd/popper.min.js", "assets/node_modules/bootstrap/dist/js/bootstrap.min.js", "assets/node_modules/bootstrap/js/dist/alert.js", filters="jsmin", output="js/generated.js")
assets.register("js_all", js)

from app.controllers.users import users
from app.controllers.main import main
from app.controllers.stories import stories
from app.controllers.comments import comments
from app.controllers.api import api

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(stories)
app.register_blueprint(comments)
app.register_blueprint(api)

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)

from app.models import User
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

with app.app_context():
  db.create_all()
