from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_pymongo import PyMongo

mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = 'auth'
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address,
                  default_limits=["200 per day", "50 per hour"])


