from .base import *

DEBUG = bool(os.environ.get("DEBUG", default=0))

try:
    from .local import *
except ImportError:
    pass
