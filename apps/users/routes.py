from multiprocessing.sharedctypes import Value
from unittest import result
from flask import Blueprint, request, render_template

from extensions import db
from models.user import User

app = Blueprint('users', __name__, template_folder='templates')

baseurl = '/users'


@app.route(f'{baseurl}', methods=['GET'])
def index():
    try:
        users = User.query.all()
        result = []
        for user in users:
            result.append(user.as_dict())

        return {
            'success': True,
            'data': result
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@app.route(f'{baseurl}_view', methods=['GET'])
def view():
    try:
        users = User.query.all()
        result = []
        for user in users:
            result.append(user.as_dict())

        return render_template('index.html', users=result)
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@app.route(f'{baseurl}/<username>', methods=['GET'])
def read(username):
    try:
        if username == None:
            raise ValueError('Missing username')

        user = User.query.filter_by(username=username).first()
        if user == None:
            raise ValueError("User not found")

        result = user.as_dict()

        return {
            'success': True,
            'data': result
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@app.route(f'{baseurl}', methods=['POST'])
def create():
    try:
        body = request.get_json()

        if not 'username' in body or not 'password' in body:
            raise ValueError('Missing username or password')

        username = body['username']
        password = body['password']

        if not 'phone' in body:
            phone = 0

        user = User.query.filter_by(username=username).first()
        if not user == None:
            raise ValueError("No such username")

        user = User(username=username, password=password, phone=phone)
        db.session.add(user)
        db.session.commit()
        result = user.as_dict()

        return {
            'success': True,
            'data': result
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@app.route(f'{baseurl}', methods=['PUT'])
def update():
    try:
        body = request.get_json()
        args = request.args
        username = args.get('username')
        phone = body.get('phone')

        if username == None or phone == None:
            raise ValueError("Missing username or phone")

        user = User.query.filter_by(username=username).first()
        if user == None:
            raise ValueError("No such username")

        user.phone = phone
        db.session.commit()
        result = user.as_dict()

        return {
            'success': True,
            'data': result
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@app.route(f'{baseurl}', methods=['DELETE'])
def delete():
    try:
        username = request.args.get('username')

        if username == None:
            raise ValueError("Missing username")

        user = User.query.filter_by(username=username).first()
        if user == None:
            raise ValueError("No such username")

        db.session.delete(user)
        db.session.commit()
        result = user.as_dict()

        return {
            'success': True,
            'data': result
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
