from bot import db


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language_code = db.Column(db.String, default='uk')
    country = db.Column(db.String, default='ua')


class User(db.Model):
    chat_id = db.Column(db.Integer, db.ForeignKey('settings.id'), primary_key=True, nullable=False)
    settings = db.relationship('Settings')
    first_name = db.Column(db.String, nullable=False)
    is_bot = db.Column(db.Boolean)
    last_name = db.Column(db.String)
    username = db.Column(db.String)



