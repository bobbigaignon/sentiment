import os

from requests_oauthlib import OAuth1


AUTH = OAuth1(
	client_key=os.environ['TWITTER_CLIENT_KEY'],
	client_secret=os.environ['TWITTER_CLIENT_SECRET'],
	resource_owner_key=os.environ['TWITTER_RESOURCE_OWNER_KEY'],
	resource_owner_secret=os.environ['TWITTER_RESOURCE_OWNER_SECRET'],
)
