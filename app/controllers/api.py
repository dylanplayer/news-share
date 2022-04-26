from flask import Blueprint, jsonify, redirect, render_template, abort, request, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
import requests
from app.models import User
from app import app, db
from bs4 import BeautifulSoup
import json

api = Blueprint('api', __name__)

@api.route('/api/meta-data', methods=['POST'])
def get_meta_data():
  data = request.get_json()
  response = requests.get(data['url'])
  soup = BeautifulSoup(response.text, 'html.parser')
  title = soup.find('title')
  if title:
    data = {
      'title': title.text
    }
  else:
    data = {
      'title': ''
    }
  return jsonify(data)
