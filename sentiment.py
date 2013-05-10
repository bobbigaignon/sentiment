import httplib
import json

from flask import abort
from flask import render_template
import sqlalchemy

from core.app import app
from core.app import db
from models.movie import Movie
from movies import MOVIES


class InvalidSentimentException(Exception): pass


@app.route('/')
def hello():
	return 'Welcome to the movie sentiment analyzer!'


@app.route('/movie/<movie_key>')
def movie(movie_key):
	return render_template(
		'movie.html',
		movie_key=movie_key,
		movie_title=MOVIES[movie_key].title,
		movie_poster=MOVIES[movie_key].poster_uri,
	)


def compute_aggregated_sentiment(tweets):
	scoring = {
		'POS': 1,
		'NEU': 0,
		'NEG': -1,
	}
	aggregated_score = 0.0
	total = 0
	for tweet in tweets:
		score = scoring.get(tweet.sentiment, None)
		if score is None:
			raise InvalidSentimentException("%s" % tweet.sentiment)
		aggregated_score = aggregated_score + score
		total = total + 1

	if total == 0:
		return 0

	return 100 * (aggregated_score + total) / (2 * total)


@app.route('/score_movie/<movie_key>')
def score_movie(movie_key):
	try:
		print MOVIES[movie_key]
		movie = db.session.query(
			Movie,
		).filter(
			Movie.id == MOVIES[movie_key].movie_id,
		).one()
	except sqlalchemy.orm.exc.NoResultFound:
		abort(httplib.NOT_FOUND)

	db.session.rollback()

	return json.dumps(
		dict(score="%d" % compute_aggregated_sentiment(movie.tweets)),
	)
