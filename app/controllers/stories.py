from flask import Blueprint, redirect, render_template, abort, request, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from app.models import Story
from app import app, db
from urllib.parse import urlparse

stories = Blueprint('stories', __name__)

@stories.route('/new', methods=['GET', 'POST'])
@login_required
def new_story():
  if (request.method == 'GET'):
    return(render_template('stories/new.html', current_user=current_user))
  else:
    url = request.form.get('url')
    title = request.form.get('title')
    text = request.form.get('text')
    source = urlparse(url).hostname
    user = current_user

    new_story = Story(url=url, title=title, text=text, source=source, user=user)

    db.session.add(new_story)
    db.session.commit()
    return(redirect(f'/stories/{new_story.id}'))

@stories.route('/stories/<id>', methods=['GET', 'POST'])
@login_required
def story(id):
  story = Story.query.filter_by(id=id).first()
  return(render_template('stories/show.html', story=story, current_user=current_user))

@stories.route('/stories/<id>/vote', methods=['GET', 'POST'])
@login_required
def vote(id):
  story = Story.query.filter_by(id=id).first()
  if current_user in story.ratings:
    story.ratings.remove(current_user)
  else:
    story.ratings.append(current_user)
  
  db.session.add(story)
  db.session.commit()
  
  return(redirect(request.referrer))
