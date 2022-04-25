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
