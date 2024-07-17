import os


class Config:
    SECRET_KEY = os.environ.get('F_KEY')
    MONGO_URI = os.environ.get('MONGO_URI')
    RECAPTCHA_SECRET_KEY = os.environ.get("G_KEY")
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USER = os.environ.get("E_ID")
    EMAIL_PASSWORD = os.environ.get("E_KEY")
    EMAIL_RECEIVER = os.environ.get("E_ID_TO")
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    RECAPTCHA_SITE_KEY = os.environ.get('S_KEY')
