from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow())

    tests = db.relationship('Test', backref='user', lazy=True)

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def __repr__(self):
            return f'<User {self.username}>'

class Test(db.Model):
    __tablename__ = "tests"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    words = db.Column(db.Integer, nullable=False)
    chars = db.Column(db.Integer, nullable=False)
    errors = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    wpm = db.Column(db.Float, nullable=False)
    kpm = db.Column(db.Float, nullable=False)
    difficulty = db.Column(db.String(10), nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    score = db.Column(db.Float, nullable=False)
    raw = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, user_id, words, chars, errors, time, wpm, kpm, difficulty, accuracy, score, raw):
        self.user_id = user_id
        self.words = words
        self.chars = chars
        self.kpm = kpm
        self.wpm = wpm
        self.errors = errors
        self.time = time
        self.difficulty = difficulty
        self.accuracy = accuracy
        self.score = score
        self.raw = raw

    def __repr__(self):
        return f"<Record {self.id}>"
