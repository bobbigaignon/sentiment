import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask('Sentiment')

app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['HEROKU_POSTGRESQL_BRONZE_URL']
db = SQLAlchemy(app)

