
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import User
from database import db_session
import jwt
import bcrypt
import os
from flask_cors import CORS, cross_origin



app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


#sign up route 
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    user = User(name=data['name'], email=data['email'], password=hashed_password)
    db_session.add(user)
    db_session.commit()
    token = jwt.encode({'email': user.email, 'name': user.name}, "signlingo-top-secret", algorithm='HS256')
    return jsonify({'message': 'user created' , "token" : token}), 201


#login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        if bcrypt.checkpw(data['password'].encode('utf-8'), user.password):
            token = jwt.encode({'email': user.email, 'name': user.name}, "signlingo-top-secret", algorithm='HS256')
            return jsonify({'message': 'login successful', 'token': token}), 200
    return jsonify({'message': 'wrong email or password'}), 404