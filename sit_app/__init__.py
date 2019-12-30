import os
import click
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext

db = SQLAlchemy()
toolbar = DebugToolbarExtension()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "school-issues.sqlite3"),
        DEBUG_TB_INTERCEPT_REDIRECTS=False,
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" +
        os.path.join(app.instance_path, "school-issues.sqlite3"),
        SQLALCHEMY_ECHO=True,  # display queries to stderr
        SQLALCHEMY_RECORD_QUERIES=True,  # display queries in toolbar
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    app.debug = True
    toolbar.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @click.command("init-db")
    @with_appcontext
    def init_db_command():
        db.drop_all()
        db.create_all()

    from . import auth
    from . import filters
    from . import issue

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(filters.bp)
    app.register_blueprint(issue.bp)

    app.add_url_rule("/", endpoint="index")
    app.cli.add_command(init_db_command)

    return app
