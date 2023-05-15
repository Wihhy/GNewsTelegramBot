from pprint import pprint
from bot import db
from .models import User, Article
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GNEWS_BASE_URL = f'https://gnews.io/api/v4/top-headlines?apikey={os.getenv("GNEWS_API_KEY")}'


class GNews:
    def __init__(self, user_chat_id: int, category: str):
        self.user = User.query.get(user_chat_id)
        self.category = category
        self.g_news_url = f'{GNEWS_BASE_URL}&category={self.category}&country={self.user.settings.country}' \
                          f'&lang={self.user.settings.language_code}'

    def get_headlines(self):
        old_articles = Article.query.filter_by(user_chat_id=self.user.chat_id).all()
        for article in old_articles:
            db.session.delete(article)
        db.session.commit()
        res = requests.get(url=self.g_news_url)
        data = res.json()
        pprint(data)
        articles = data.get('articles')
        news = []
        for art in articles:
            new = Article(
                user_chat_id=self.user.chat_id,
                title=art.get('title'),
                description=art.get('description'),
                image_url= art.get('image'),
                article_url=art.get('url')
            )
            news.append(new)
        db.session.bulk_save_objects(news)
        db.session.commit()


