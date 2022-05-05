from app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  family_name = db.Column(db.String(255), nullable=False)
  given_name = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(255), nullable=False, unique=True)
  password = db.Column(db.String(255), nullable=False)
  bio = db.Column(db.Text, nullable=True)
  position = db.Column(db.String(255), nullable=False)
  company = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime, server_default=db.func.now())
  updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
  stories = db.relationship('Story', back_populates='user')
  rated_stories = db.relationship('Story', secondary='ratings', back_populates='ratings')
  comments = db.relationship('Comment', back_populates='user')

class Story(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.Text, nullable=False)
  title = db.Column(db.String(255), nullable=False)
  text = db.Column(db.Text)
  source = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime, server_default=db.func.now())
  updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  user = db.relationship('User', back_populates='stories')
  ratings = db.relationship('User', secondary='ratings', back_populates='rated_stories')
  comments = db.relationship('Comment', back_populates='story')

class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.Text)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  user = db.relationship('User', back_populates='comments')
  story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
  story = db.relationship('Story', back_populates='comments')
  created_at = db.Column(db.DateTime, server_default=db.func.now())
  updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

ratings = db.Table('ratings',
  db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
  db.Column('story_id', db.Integer, db.ForeignKey('story.id'), primary_key=True),
)
