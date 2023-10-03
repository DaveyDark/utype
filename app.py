from flask import Flask, redirect, render_template, session, url_for
from models import  Profile, db, Test, User
from api import api, limiter, stats, rank
import os

app = Flask(__name__)
limiter.init_app(app)
app.secret_key = "utype_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///utype.db"

db.init_app(app)

app.register_blueprint(api, url_prefix='/api')

def auth():
    if "user_id" not in session:
        return None
    user = User.query.get(session['user_id'])
    if not user:
        return None
    return user

@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route("/login/")
def login():
    if auth():
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route("/logout/")
def logout():
    if not auth():
        return redirect(url_for('login'))
    del session['user_id']
    return redirect(url_for('login'))

@app.route("/home/")
def home():
    if not auth():
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route("/leaderboard/")
def leaderboard():
    if not auth():
        return redirect(url_for('login'))
    return render_template('leaderboard.html')

@app.route("/profile/")
def user_profile():
    user = auth()
    if not user:
        return redirect(url_for('login'))
    return redirect(url_for('profile', id=user.id))

@app.route('/profile/<int:id>/')
def profile(id):
    user = auth()
    if not user:
        return redirect(url_for('login'))
    profile = Profile.query.filter_by(user_id=id).first()
    if not profile:
        return '',404
    tests = Test.query.filter_by(user_id=id).order_by(Test.timestamp.desc()).all()
    for test in tests:
        test.time= test.timestamp.strftime("%d %h %Y %I:%M%p")
    stat = stats(id)[0]
    return render_template('profile.html', user=user, profile=profile, tests=tests, stats=stat, rank=rank(id)[0], is_user=id==session['user_id'])

@app.route('/profile/<int:id>/edit')
def edit_profile(id):
    user = auth()
    directory = './static/img/avatars/'
    pics = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not user:
        return redirect(url_for('login'))
    profile = Profile.query.filter_by(user_id=id).first()
    if not profile:
        return '',404
    return render_template('edit_profile.html', pics=pics, profile=profile)

@app.route("/results/<int:id>/")
def results(id):
    user = auth()
    if not user:
        return redirect(url_for('login'))
    test = Test.query.get(id)
    if not test:
        return '',404
    timestamp = test.timestamp.strftime('%d/%m/%Y %I:%M%p')
    tester = User.query.get(test.user_id)
    if not tester:
        return '',404
    return render_template('results.html', user=user, test=test, timestamp=timestamp, username = tester.username)

