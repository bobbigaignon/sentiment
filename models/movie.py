import datetime
from core.app import db


class Movie(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(120), nullable=False)


class Tweet(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)

	time_created = db.Column(db.DateTime, default=datetime.datetime.now)
	tweet_id = db.Column(db.String(120), nullable=False)
	sentiment = db.Column(db.Enum('POS', 'NEG', 'NEU', name='sentiment'), nullable=False)
	movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
	movie = db.relationship(Movie, backref=db.backref('tweets'))
