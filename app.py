from flask import Flask, redirect, render_template, session, url_for
from models import Profile, db, Test, User
from api import api, limiter

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
    return render_template('profile.html', user=user, profile=user.profile)

@app.route("/results/<int:id>/")
def results(id):
    user = auth()
    if not user:
        return redirect(url_for('login'))
    test = Test.query.get(id)
    if not test:
        return '',404
    timestamp = test.timestamp.strftime('%d/%m/%Y %I:%M%p')
    return render_template('results.html', user=user, test=test, timestamp=timestamp)

