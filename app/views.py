from app import app, db
from flask import jsonify

from app.models import Users, Photos


@app.route('/')
def index():
    return "Hello world!", 200


@app.route('/dev/init')
def init():
    db.create_all()
    return jsonify({"message": "Init was successful."}), 200
