from app import db
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    total_score = db.Column(db.Integer, default=0)
    difficulty_level = db.Column(db.Integer, default=1)

# class Word(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     word = db.Column(db.String(50), nullable=False)
#     focus_sound = db.Column(db.String(20), nullable=False)
#     difficulty_level = db.Column(db.Integer, nullable=False)

from app import db

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(255), nullable=False)
    focus_sound = db.Column(db.String(50), nullable=False)
    difficulty_level = db.Column(db.Integer, nullable=False)


class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())



from app import db

class Score(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    total_score = db.Column(db.Integer, default=0, nullable=False)

