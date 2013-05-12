from core.app import db

from models.movie import Tweet


if __name__ == '__main__':
	db.session.query(Tweet).delete()
	db.session.commit()
