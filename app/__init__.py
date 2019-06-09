from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

app.secret_key = app.config["APP_SECRET_KEY"]

db = SQLAlchemy(app)

from app import views
