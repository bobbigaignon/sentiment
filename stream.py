import httplib
import json
import requests
from requests_oauthlib import OAuth1


TWITTER_STREAM_URL = "https://stream.twitter.com/1.1/statuses/filter.json"
AUTH = OAuth1(
	'7h6O6n3KwB4VGtkE2vAnhA',
	'L98gUDKzxvz8Cw0gA6XgyZ06BAJEPDfu0t0JqYdS7Y',
	'15382735-GV1EIslrUUCIHRmdEHilFMRXBdDuyrAbRA4UtYRJL',
	'ozVuPS7QS0BBh9JpssHbVVD6skguUyslptCrKMh9E',
)

UK_BOUNDING_BOX = "-9.23,2.69,60.85,49.84"
SF_BOUNDING_BOX = "-122.75,36.8,-121.75,37.8"
NYC_BOUNDING_BOX = "-74,40,-73,41"


class StreamException(Exception): pass


def tweet_stream(track):
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


if __name__ == '__main__':
	for tweet_id, tweet_text in tweet_stream('ironman'):
		print tweet_id, tweet_text
