from app import app, db
from flask import jsonify, render_template, request, redirect, session, url_for, flash
from flask_login import LoginManager, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User, Photo

from .aws_helper import upload_file_to_s3


# login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route('/')
def index():
    return "Hello world!", 200


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # if a user is found, we want user can try again
    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email address already exists')
        return redirect(url_for('signup'))

    # create new user with the form data
    # hash the password
    new_user = User(email=email,
                    name=name,
                    quota=20,
                    count=0,
                    is_activated=0,
                    password=generate_password_hash(password, method='sha256'))

    # add the new user to db
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("login"))


@app.route('/login')
def login():
    return render_template("login.html",
                           next=request.args.get("next") or url_for("index"))


@app.route('/login', methods=['POST'])
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
    return redirect(next_url)


@app.route('/profile')
def profile():
    return render_template("profile.html")


@app.route('/upload')
@login_required
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
