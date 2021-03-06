from flask import Blueprint, redirect, render_template, abort, request, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User, Story
from app import app, db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
@login_required
def index():
  stories = sorted(Story.query.all(), key=lambda x: len(x.ratings), reverse=True)
  return(render_template('stories/index.html', current_user=current_user, stories=stories))
