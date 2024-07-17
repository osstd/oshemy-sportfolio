from flask import Flask, redirect, url_for, flash
from config import Config
from extensions import mongo, login_manager, csrf, limiter
from routes.auth import auth_bp
from routes.main import main_bp
from routes.slides import slides_bp
from routes.users import users_bp
from models.models import User
from models.transactions import get_by_id, DatabaseError
from components import render_header, render_footer
from logging_cofig import setup_logging


logger = setup_logging()


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)

    register_extensions(flask_app)
    ping_mongo()
    register_blueprints(flask_app)
    register_context_processors(flask_app)

    return flask_app


@login_manager.user_loader
def load_user(user_id):
    try:
        user = get_by_id("portfoliopage", "portfolio_users", user_id)
        if user:
            return User(user["_id"], user["username"])
        return None
    except DatabaseError as e:
        flash(f"An error occurred retrieving user record:{e}", "error")
        return redirect(url_for("auth.auth"))


def register_extensions(flask_app):
    mongo.init_app(flask_app)
    login_manager.init_app(flask_app)
    csrf.init_app(flask_app)
    limiter.init_app(flask_app)


def register_blueprints(flask_app):
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(main_bp)
    flask_app.register_blueprint(slides_bp)
    flask_app.register_blueprint(users_bp)


def inject_header():
    def get_header(active_page, subcategory=None):
        return render_header(active_page, subcategory)

    return dict(get_header=get_header)


def inject_footer():
    return dict(render_footer=render_footer)


def register_context_processors(flask_app):
    flask_app.context_processor(inject_header)
    flask_app.context_processor(inject_footer)


def ping_mongo():
    try:
        mongo.cx.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
    except Exception as e:
        logger.info(f"Failed to connect to MongoDB: {e}")


app = create_app()

if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
