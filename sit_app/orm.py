from sit_app import db2


class User(db2.Model):
    id = db2.Column(db2.Integer, primary_key=True)
    username = db2.Column(db2.String(80), unique=True, nullable=False)
    password = db2.Column(db2.String(120), unique=True, nullable=False)
