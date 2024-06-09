from .base import *
from config import (SECRET_KEY, ALLOWED_HOSTS) 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG", default=0))

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: define the correct hosts in production!



EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
