import os
import click
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext

db2 = SQLAlchemy()
toolbar = DebugToolbarExtension()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "school-issues.sqlite3"),
        SQLALCHEMY_DATABASE_URI="sqlite:///"
        + os.path.join(app.instance_path, "school-issues.sqlite3"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # SQLALCHEMY_RECORD_QUERIES=True, # True by default if FLASK_DEBUG=True
        # SQLALCHEMY_ECHO=True, # queries displayed to stderr if True
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

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    @click.command("init-db2")
    @with_appcontext
    def init_db2_command():
        db2.drop_all()
        db2.create_all()

    from . import auth
    from . import issue
    from . import db

    db.init_app(app)

    db2.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(issue.bp)
    app.add_url_rule("/", endpoint="index")
    app.cli.add_command(init_db2_command)

    return app
