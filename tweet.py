from app import db


class Tweet(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	time_created = db.Column(db.DateTime)
	tweet_id = db.Column(db.String(120))
	sentiment = db.Column(db.Enum('POS', 'NEG', 'NEU'))
