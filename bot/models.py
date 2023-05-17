from bot import db


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language_code = db.Column(db.String, default='uk')
    country = db.Column(db.String, default='ua')


class User(db.Model):
    chat_id = db.Column(db.Integer, db.ForeignKey('settings.id'), primary_key=True, nullable=False)
    settings = db.relationship('Settings', backref='user')
    first_name = db.Column(db.String, nullable=False)
    is_bot = db.Column(db.Boolean)
    last_name = db.Column(db.String)
    username = db.Column(db.String)
    is_searching = db.Column(db.Boolean, default=False)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_chat_id = db.Column(db.Integer, db.ForeignKey('user.chat_id'), nullable=False)
    user = db.relationship('User', backref='articles')
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    image_url = db.Column(db.String, nullable=False)
    article_url = db.Column(db.String, nullable=False)
