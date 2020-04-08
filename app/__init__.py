import os

import click
from flask import Flask
from flask.cli import with_appcontext
from flask_babel import Babel, lazy_gettext
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

babel = Babel()
db = SQLAlchemy()
login_manager = LoginManager()
toolbar = DebugToolbarExtension()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        BABEL_DEFAULT_LOCALE="fr",
        BABEL_DEFAULT_TIMEZONE="Europe/Vienna",
        DATABASE=os.path.join(app.instance_path, "school-issues.sqlite3"),
        DEBUG_TB_INTERCEPT_REDIRECTS=False,
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///"
        + os.path.join(app.instance_path, "school-issues.sqlite3"),
        SQLALCHEMY_ECHO=True,  # display query params as well in toolbar Logging section (and queries to stderr)
        SQLALCHEMY_RECORD_QUERIES=True,  # display queries in toolbar SQLAlchemy section
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        USE_SESSION_FOR_NEXT=True,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.debug = True
    login_manager.login_message = lazy_gettext("Please log in to access this page.")
    login_manager.login_message_category = "error"
    login_manager.login_view = "user.login"

    babel.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    toolbar.init_app(app)

    from . import filters
    from .helpers import get_arg_or_cookie
    from .views import ip, issue, user
    from .models.orm import User

    @click.command("init-db")
    @with_appcontext
    def init_db_command():
        db.drop_all()
        db.create_all()
        User.create_admin()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def utility_processor():
        return dict(get_arg_or_cookie=get_arg_or_cookie)

    app.register_blueprint(filters.bp)
    app.register_blueprint(ip.bp)
    app.register_blueprint(issue.bp)
    app.register_blueprint(user.bp)

    app.add_url_rule("/", endpoint="index")
    app.cli.add_command(init_db_command)

    try:
        os.makedirs(app.instance_path)
    except FileExistsError:
        pass

    return app
