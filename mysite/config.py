from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = os.getenv('DEBUG')
SECRET_KEY = str(os.getenv('SECRET_KEY')) #why did't this work without str()? Write me please
ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS')]

POSTGRESQL_ENGINE = os.getenv('POSTGRESQL_ENGINE')
POSTGRESQL_NAME = os.getenv('POSTGRESQL_NAME')
POSTGRESQL_USER = os.getenv('POSTGRESQL_USER')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
