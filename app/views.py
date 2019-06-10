import os
import uuid

from app import app, db
from flask import jsonify, render_template, request, redirect, session, url_for, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User, Photo

from .aws_helper import upload_file_to_s3, build_s3_url


# login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route("/")
def index():
    return "Hello world!", 200


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    # if a user is found, we want user can try again
    user = User.query.filter_by(email=email).first()
    if user:
        flash("Email address already exists")
        return redirect(url_for("signup"))

    # create new user with the form data
    # hash the password
    new_user = User(email=email,
                    name=name,
                    quota=20,
                    count=0,
                    password=generate_password_hash(password, method="sha256"))

    # add the new user to db
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("login"))


@app.route("/login")
def login():
    return render_template("login.html",
                           next=request.args.get("next") or url_for("index"))


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    next_url = request.form.get("next")

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # hash the supplied password and compare it to the one in db
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("login"))

    # all checks passed
    login_user(user, remember=remember)
    return redirect(next_url)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/logout")
def logout():
    logout_user()
    return "Logged out"


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/upload")
@login_required
def upload():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    """
        These attributes are available for file object
        file.filename
        file.content_type
        file.content_length
        file.mimetype
    """
    # check request.files for user_file key (the name of the file input on form)
    if "user_file" not in request.files:
        return "No user_file key in request.files"
    files = request.files.getlist("user_file")

    for file in files:
        file.filename = secure_filename(file.filename)
        is_safe, message = validate_file(file)
        if not is_safe:
            return message

        # check and update user quota
        if current_user.count >= current_user.quota:
            return "Quota exceeded, please upgrade your plan"

        # rename file
        file_uuid = str(uuid.uuid4()).upper()
        file.filename = "{}.jpg".format(file_uuid)

        # update db
        new_photo = Photo(
            uuid=file_uuid,
            user_id=current_user.id,
        )
        db.session.add(new_photo)
        current_user.count += 1
        db.session.add(current_user)
        db.session.commit()

        path = upload_file_to_s3(file, app.config["S3_BUCKET"])
        print(path)

    return "ok"


def validate_file(file):
    # check that the file exists
    if not file:
        return False, "file does not exist"

    # user sumbmitted an empty form
    if file.filename == "":
        return False, "Please select a file"

    # verify file extension
    if os.path.splitext(file.filename)[1].lower() not in [".jpg", ".jpeg"]:
        return False, "Only JPEG files are supported (file extension)"

    # verify MIME type
    if file.mimetype != "image/jpeg":
        return False, "Only JPEG files are supported (mimetype)"

    return True, ""


@app.route("/dev/init")
def init():
    db.create_all()
    return jsonify({"message": "Init was successful."}), 200
