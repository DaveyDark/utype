from flask import Blueprint, request, jsonify, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import db, User, Test, Profile
from sqlalchemy import func
import bcrypt

api = Blueprint('api', __name__)

limiter = Limiter(
    key_func=lambda: get_remote_address(),
)

@api.route('/login/', methods=['POST'])
@limiter.limit('5 per minute')
def login():
    if 'username' not in request.form or 'password' not in request.form:
        return 'Bad Request', 400
    user = User.query.filter_by(username=request.form['username']).first()
    if not user or not bcrypt.checkpw(request.form['password'].encode('utf-8'), user.password):
        return 'Incorrect username or password', 401
    session['user_id'] = user.id
    return '',200

@api.route('/register/', methods=['POST'])
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
    profile = Profile(user.id)
    db.session.add(profile)
    db.session.commit()
    session['user_id'] = user.id
    return 'User Created',201

@api.route("/submit/", methods=["POST"])
def submit():
    if not 'user_id' in session:
        return '', 401
    data = request.json
    if not data:
        return '',400
    test = Test(user_id=session['user_id'], words=data['words'], chars=data['chars'], errors=data['errors'], time=data['time'], wpm=data['wpm'], kpm=data['kpm'], difficulty=data['difficulty'], accuracy=data['accuracy'], score=data['score'], raw=data['raw'])
    db.session.add(test)
    db.session.commit()
    return {'id': test.id}, 200

@api.route("/stats/<int:id>/", methods=["GET"])
def stats(id):
    user = User.query.get(id)
    if not user:
        return 'User doesn\'t exist',400
    test_count = len(user.tests)
    total_wpm = 0
    total_score = 0
    total_accuracy = 0
    highest_score = 0
    highest_wpm = 0
    if test_count == 0:
        stats = {
            'average_wpm': 0,
            'average_score': 0,
            'average_accuracy': 0,
            'highest_score': 0,
            'highest_wpm': 0,
            'tests': 0,
            }
        return jsonify(stats),200
    for test in user.tests:
        total_wpm += test.wpm
        total_score += test.score
        total_accuracy += test.accuracy
        highest_score = max(highest_score,test.score)
        highest_wpm = max(highest_wpm,test.wpm)
    stats = {
        'average_wpm': total_wpm/test_count,
        'average_score': total_score/test_count,
        'average_accuracy': total_accuracy/test_count,
        'highest_score': highest_score,
        'highest_wpm': highest_wpm,
        'tests': test_count,
        }
    return jsonify(stats),200

@api.route("/graphs/<int:id>/", methods=["GET"])
def graph(id):
    user = User.query.get(id)
    if not user:
        return 'User doesn\'t exist',400
    latest_tests = Test.query.filter_by(user=user).order_by(Test.timestamp.desc()).limit(10).all()
    tests = []
    for test in latest_tests:
        timestamp = test.timestamp.strftime("%Y/%m/%d") 
        tests.append({'wpm': round(test.wpm,1), 'score': round(test.score,1), 'accuracy': round(test.accuracy,1), 'timestamp': timestamp})
    return jsonify(tests),200

@api.route("/ranks/", methods=["GET"])
def ranks():
    users = User.query.all()
    user_scores = []

    for user in users:
        highest_score = db.session.query(db.func.max(Test.score)).filter(Test.user_id == user.id).scalar()
        if not highest_score:
            highest_score = 0
        user_scores.append([user.id, highest_score])

    # Sort the list of users by their highest score in descending order
    sorted_users = sorted(user_scores, key=lambda x: x[1], reverse=True)

    return jsonify(sorted_users),200
@api.route("/rank/<int:id>/", methods=["GET"])
def rank(id):
    user = User.query.get(id)
    if not user:
        return 'User doesn\'t exist',400
    rankings = ranks()[0].json;    
    if not rankings:
        return '',500
    i = 0
    for rank in rankings:
        i += 1
        if rank[0] == id:
            break
    return jsonify(i), 200
