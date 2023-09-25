from flask import Flask, redirect, render_template, session, url_for
from models import db
from api import api, limiter

app = Flask(__name__)
limiter.init_app(app)
app.secret_key = "utype_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///utype.db"

db.init_app(app)

app.register_blueprint(api, url_prefix='/api')

@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route("/login/")
def login():
    if "user_id" in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route("/logout/")
def logout():
    if 'user_id' in session:
        del session['user_id']
    return redirect(url_for('login'))

@app.route("/home/")
def home():
    if "user_id" not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route("/results/")
def results():
    if "user_id" not in session:
        return redirect(url_for('login'))
    return render_template('results.html')

