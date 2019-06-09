from app import app, db
from flask import jsonify, render_template, request, redirect

from app.models import Users, Photos

from .aws_helper import upload_file_to_s3


@app.route('/')
def index():
    return "Hello world!", 200


@app.route('/upload')
def upload():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    """
        These attributes are also available
        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype
    """
    # check request.files for user_file key (the name of the file input on form)
    if "user_file" not in request.files:
        return "No user_file key in request.files"

    # If the key is in the object, we save it in a variable called file.
    file = request.files["user_file"]

    # if filename is empty, it means the user sumbmitted an empty form
    if file.filename == "":
        return "Please select a file"

    # check that the file exists, and that an allowed file type and size
    if file:
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])
        return str(output)

    else:
        return redirect("/")


@app.route('/dev/init')
def init():
    db.create_all()
    return jsonify({"message": "Init was successful."}), 200
