from flask import Blueprint, redirect, render_template, abort, request, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from app.models import Comment
from app import app, db

comments = Blueprint('comments', __name__)

@comments.route('/stories/<id>/comments', methods=['POST'])
@login_required
def new(id):
  text = request.form.get('text')
  comment = Comment(text=text, user_id=current_user.id, story_id=id)
  db.session.add(comment)
  db.session.commit()
  return(redirect(url_for('stories.show', id=id)))
