from flask import Blueprint, request, jsonify, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import db, User, Test
import bcrypt

api = Blueprint('api', __name__)

limiter = Limiter(
    key_func=lambda: get_remote_address(),
)

@api.route('/login', methods=['POST'])
@limiter.limit('5 per minute')
def login():
    if 'username' not in request.form or 'password' not in request.form:
        return 'Bad Request', 400
    user = User.query.filter_by(username=request.form['username']).first()
    if not user or not bcrypt.checkpw(request.form['password'].encode('utf-8'), user.password):
        return 'Incorrect username or password', 401
    session['user_id'] = user.id
    return '',200

@api.route('/register', methods=['POST'])
def register():
    if 'username' not in request.form or 'password' not in request.form:
        return 'Bad Request', 400
    user = User.query.filter_by(username=request.form['username']).first()
    if user:
        return 'User already exists', 409
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), salt)
    user = User(username=request.form['username'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return 'User Created',201

@api.route("/submit/", methods=["POST"])
def submit():
    if not 'user_id' in session:
        return '', 401
    data = request.json
    print(data)
    test = Test(user_id=session['user_id'], words=data['words'], chars=data['chars'], errors=data['errors'], time=data['time'], wpm=data['wpm'], kpm=data['kpm'], difficulty=data['difficulty'])
    db.session.add(test)
    db.session.commit()
    print(data)

    return '', 200
