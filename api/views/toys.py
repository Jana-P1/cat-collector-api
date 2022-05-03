from distutils.log import log
import json
from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.toy import Toy

toys = Blueprint('toys', 'toys')

# Creates toys
@toys.route('/', methods=["POST"])
@login_required
def create():
  data = request.get_json()
  profile = read_token(request)
  data["profile_id"] = profile['id']

  toy = Toy(**data)
  db.session.add(toy)
  db.session.commit()
  return jsonify(toy.serialize()), 201

# Shows all toys
@toys.route('/', methods=["GET"])
def index():
  toys = Toy.query.all()
  return jsonify([toy.serialize() for toy in toys]), 201

# Shows a toy
@toys.route('/<id>', methods=["GET"])
def show(id):
  toy = Toy.query.filter_by(id=id).first()
  return jsonify(toy.serialize()), 200

# Updates a toy
@toys.route('/<id>', methods=["PUT"])
@login_required
def update(id): 
  data = request.get_json()
  profile = read_token(request)
  toy = Toy.query.filter_by(id=id).first()

  if toy.profile_id != profile['id']:
    return 'Forbidden', 403
  
  for key in data:
    setattr(toy, key, data[key])
  
  db.session.commit()
  return jsonify(toy.serialize()), 200







