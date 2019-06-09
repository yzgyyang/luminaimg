# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Enable the development environment
DEBUG = True

# Define the database
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://luminauser:luminapassword@localhost:3306/luminadb'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Amazon S3 config from env
S3_BUCKET = os.environ.get("S3_BUCKET")
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")
