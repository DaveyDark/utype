from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from models import db
from api import api

app = Flask(__name__)
app.secret_key = "utype_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///utype.db"

db.init_app(app)

app.register_blueprint(api, url_prefix='/api')

@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route("/login/")
def login():
    return render_template('login.html')

@app.route("/home/")
def home():
    if "id" not in session:
        return redirect(url_for('login'))
    return render_template('home.html', session_id = session["id"])

@app.route("/submit/", methods=["POST"])
def submit():
    data = request.json
    print(data)

    response = {'message': 'Data received successfully'}
    return jsonify(response), 200
