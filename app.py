from flask import Flask, jsonify, redirect, render_template, request, session, url_for
import random

app = Flask(__name__)
app.secret_key = "utype_secret"

@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route("/home/")
def home():
    if "id" not in session:
        session["id"] = random.randint(0,99999)
    return render_template('home.html', session_id = session["id"])

@app.route("/submit/", methods=["POST"])
def submit():
    data = request.json
    print(data)

    response = {'message': 'Data received successfully'}
    return jsonify(response), 200
