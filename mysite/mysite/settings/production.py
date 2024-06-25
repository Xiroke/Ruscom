from .base import *
from config import (SECRET_KEY, ALLOWED_HOSTS) 

DEBUG = bool(os.environ.get("DEBUG", default=0))
SECRET_KEY = SECRET_KEY
ALLOWED_HOSTS = ALLOWED_HOSTS

try:
    from .local import *
except ImportError:
    pass
