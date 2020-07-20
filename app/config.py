import os

SQLALCHEMY_DATABASE_URI = os.environ['DB_URI']
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Will only be set to False if the environment variable is present and set to 'no'
HCG_UTILS_AUTHENTICATION_JWT_VERIFY = os.environ.get('HCG_UTILS_AUTHENTICATION_JWT_VERIFY', 'yes').lower() != 'no'
