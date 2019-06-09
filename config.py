# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Enable the development environment
DEBUG = True

# DB config from env
DB_USER = os.environ.get("DB_USER", "luminauser")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "luminapassword")
DB_URI = os.environ.get("DB_URI", "localhost:3306")
DB_NAME = os.environ.get("DB_NAME", "luminadb")

# Define the database
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{db_user}:{db_password}@{db_uri}/{db_name}'.format(
    db_user=DB_USER,
    db_password=DB_PASSWORD,
    db_uri=DB_URI,
    db_name=DB_NAME,
)
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Amazon S3 config from env
S3_BUCKET = os.environ.get("S3_BUCKET")
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")

# Flask app secret key
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY', 'dev')
