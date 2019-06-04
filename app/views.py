from app import app
from flask import jsonify


@app.route('/')
def index():
    return "Hello world!", 200
