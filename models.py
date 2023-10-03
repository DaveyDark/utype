from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    
    profile = db.relationship('Profile', backref='user', uselist=False)
    
    tests = db.relationship('Test', backref='user')

    def __init__(self, username, password):
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
    timestamp = db.Column(db.DateTime)

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
        self.timestamp =datetime.now()

    def __repr__(self):
        return f"<Record {self.id}>"

class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    bio = db.Column(db.String(255))
    country = db.Column(db.String(25))
    pfp = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    def __init__(self, user_id):
        self.name = ""
        self.bio = ""
        self.country = "India🇮🇳"
        self.pfp = "/static/img/avatars/01.png"
        self.user_id = user_id
