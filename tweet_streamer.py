import argparse
import httplib
import json
import time

import requests

from core.app import db
from models import movie
from movies import MOVIES
from auth import AUTH


TWITTER_STREAM_URL = "https://stream.twitter.com/1.1/statuses/filter.json"
SENTIMENT_ANALYZER_URL = "http://text-processing.com/api/sentiment/"
THROTTLER_SLEEP_TIME = 2


class StreamException(Exception): pass
class InvalidSentimentLabelException(Exception): pass


def tweet_stream(track):
	"""Stream Twitter's public API for tweets matching a topic of interest."""
	payload = {
		'track': track,
	}
	res = requests.post(TWITTER_STREAM_URL, stream=True, auth=AUTH, data=payload)

	if res.status_code != httplib.OK:
		raise StreamException("(%s) %s" % (res.status_code, res.reason))

	for tweet in res.iter_lines():
		if tweet is not None:
			tweet = json.loads(tweet)
			if  tweet.get('lang') == 'en':
				yield tweet['id'], tweet['text']
		# Will hit the rate limits of various service this app depends on if all tweets
		# are processed. Put the worker to sleep for a short while to throttle Twitter's
		# stream.
		time.sleep(THROTTLER_SLEEP_TIME)
	else:
		raise StreamException("Stream ended unexpectedly")

def compute_sentiment(phrase):
	"""Analyze a tweet for its sentiment."""
	payload = {
		'text': phrase,
	}
	res = requests.post(SENTIMENT_ANALYZER_URL, data=payload)
	sentiment = res.json()['label']
	if sentiment == u"neg":
		return 'NEG'
	elif sentiment == u"neutral":
		return 'NEU'
	elif sentiment == u"pos":
		return 'POS'
	else:
		raise InvalidSentimentLabelException("%s" % sentiment)


def parse_tweets(title):
	"""Parse live tweets for a given movie and store them into the DB. The
	stored object will contain the sentiment associated to the tweet."""
	movie_meta = MOVIES[title]
	for tweet_id, tweet_text in tweet_stream(movie_meta.track_term):
		print "Processing %d" % tweet_id
		new_tweet = movie.Tweet(
			tweet_id=tweet_id,
			sentiment=compute_sentiment(tweet_text),
			movie_id=movie_meta.movie_id,
		)

		print "New tweet! %s (%d)" % (new_tweet.sentiment, new_tweet.movie_id)

		db.session.add(new_tweet)
		db.session.commit()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='Streem twitter for movie sentiment.',
	)
	parser.add_argument(
		'title',
		metavar='TITLE',
		type=str,
		help='A movie title.',
	)
	args = parser.parse_args()

	parse_tweets(args.title)