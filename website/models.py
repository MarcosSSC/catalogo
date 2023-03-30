from . import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique =True)
    poster = db.Column(db.Text)
    description = db.Column(db.String(200))