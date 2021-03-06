from flask import Blueprint, redirect, render_template, abort, request, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from operator import attrgetter
from app import app, db

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
  if (request.method == 'GET'):
    return(render_template('users/login.html'))
  else:
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()

    if (not user or not check_password_hash(user.password, password)):
      flash('Check email or password and try again', category='danger')
      return(redirect(url_for('users.login')))

    login_user(user, True)
    return(redirect('/'))

@users.route('/signup', methods=['GET', 'POST'])
def signup():
  if (request.method == 'GET'):
    return(render_template('users/signup.html'))
  else:
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    email = request.form.get('email')
    given_name = request.form.get('given_name')
    family_name = request.form.get('family_name')
    bio = request.form.get('bio')
    position = request.form.get('position')
    company = request.form.get('company')

    if password != confirm_password:
      flash('Passwords do not match', category='danger')
      return(render_template('users/signup.html', email=email, given_name=given_name, family_name=family_name, bio=bio, position=position, company=company))

    user = User.query.filter_by(email=email).first()

    if (user):
      flash('Email address already exists', category='danger')
      return(render_template('users/signup.html', email=email, given_name=given_name, family_name=family_name, bio=bio, position=position, company=company))

    new_user = User(
      given_name=given_name,
      family_name=family_name,
      email=email,
      password=generate_password_hash(password, method='sha256'),
      bio=bio,
      position=position,
      company=company,
    )
    
    db.session.add(new_user)
    db.session.commit()

    flash('Account created, please login.', category='success')
    return(redirect(url_for('users.login')))

@users.route('/profile/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
  user = User.query.get(id)
  if current_user.id == user.id:
    if request.method == 'GET':
      return(render_template('users/edit.html', user=user))
    else:
      user.given_name = request.form.get('given_name')
      user.family_name = request.form.get('family_name')
      user.bio = request.form.get('bio')
      user.position = request.form.get('position')
      user.company = request.form.get('company')

      db.session.add(user)
      db.session.commit()
      
      flash('Account Updated', category='success')
      return(redirect(url_for('users.show', id=id)))
  else:
    return(redirect(url_for('main.index')))

@users.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return(redirect('/'))

@users.route('/profile/<id>', methods=['GET'])
@login_required
def show(id):
  user = User.query.get(id)
  stories = sorted(user.stories, key=lambda x: len(x.ratings), reverse=True)
  return(render_template('users/show.html', user=user, stories=stories))
