# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Enable the development environment
DEBUG = True

# Define the database
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://luminauser:luminapassword@localhost:3306/luminadb'
SQLALCHEMY_TRACK_MODIFICATIONS = True
