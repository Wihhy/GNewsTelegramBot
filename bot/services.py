from pprint import pprint

from .models import User
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
        res = requests.get(url=self.g_news_url)
        data = res.json()
        pprint(data)
        articles = data.get('articles')
        total_articles = data.get('totalArticles')

        for article in articles:
            print(article.get('content'))
        return data.get('articles')[0].get('description')
