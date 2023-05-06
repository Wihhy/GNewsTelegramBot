import json
import os
import requests
from dotenv import load_dotenv
from bot import db
from .settings import *
from .models import User, Settings
from .services import GNews

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
GNEWS_URL = f'https://gnews.io/api/v4/top-headlines?apikey={os.getenv("GNEWS_API_KEY")}27&category=general&lang=uk'


class FromUser:

    def __init__(self, **kwargs):
        self.first_name = kwargs.get('first_name')
        self.id = kwargs.get('id')
        self.is_bot = kwargs.get('is_bot')
        self.language_code = kwargs.get('language_code')
        self.last_name = kwargs.get('last_name')
        self.username = kwargs.get('username')


class TelegramHandler:
    from_user = None
    message_text = None

    def send_message(self, text: str):
        data = {
            'chat_id': self.from_user.id,
            'text': text
        }
        requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=data)

    def send_inline_markup_message(self, markup, text: str):
        data = {
            'chat_id': self.from_user.id,
            'text': text,
            'reply_markup': {'inline_keyboard': markup}
        }
        requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=data)

    def send_reply_markup_message(self, keyboard, text: str):
        data = {
            'chat_id': self.from_user.id,
            'text': text,
            'reply_markup': {
                'keyboard': keyboard,
                'resize_keyboard': True
            }
        }
        requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=data)


class MessageHandler(TelegramHandler):

    def __init__(self, user_data):
        self.message_text = user_data.get('text')
        self.from_user = FromUser(**user_data.get('from'))

    def handle(self):
        match self.message_text.lower():
            case '/start':
                if not User.query.get(self.from_user.id):
                    user = User(
                        first_name=self.from_user.first_name,
                        chat_id=self.from_user.id,
                        is_bot=self.from_user.is_bot if self.from_user.is_bot else False,
                        last_name=self.from_user.last_name if self.from_user.last_name else '',
                        username=self.from_user.username if self.from_user.username else ''
                    )
                    user_settings = Settings(
                        id=self.from_user.id
                    )
                    db.session.add(user)
                    db.session.add(user_settings)
                    db.session.commit()
                self.send_reply_markup_message(text=GREETING,
                                               keyboard=NEWS_SETTINGS_REPLY_MARKUP)
            case 'налаштування':
                self.send_inline_markup_message(
                    markup=SETTINGS_CHOOSE_INLINE_MARKUP,
                    text='Що саме будемо налаштовувати?')
            case 'новини':
                self.send_inline_markup_message(
                    markup=HEADLINES_SEARCH_INLINE_MARKUP,
                    text='Пошук новин чи топові заголовки?'
                )


class CallbackHandler(TelegramHandler):

    def __init__(self, data):
        self.from_user = FromUser(**data.get('from'))
        self.callback_data = data.get('data')

    def handle(self):
        match self.callback_data.split():
            case 'choose_country', code:
                self.send_inline_markup_message(
                    markup=COUNTRY_CHOOSE_INLINE_MARKUP,
                    text='Оберіть із переліку доступних країн:')
            case 'set_country_code', country, code:

                user_settings = User.query.get(self.from_user.id)
                user_settings.settings.country = code
                db.session.commit()
                self.send_message(text=f'Успішно! Країну пошуку змінено! Тепер це: {country.capitalize()}!')

            case 'choose_language', code:
                self.send_inline_markup_message(
                    markup=LANGUAGE_CHOOSE_INLINE_MARKUP,
                    text='Оберіть із переліку доступних мов:')

            case 'set_language_code', language, code:

                user_settings = User.query.get(self.from_user.id)
                user_settings.settings.language_code = code
                db.session.commit()
                self.send_message(text=f'Успішно! Мову пошуку змінено! Тепер це {language.capitalize()}!')

            case 'news', 'headlines':
                self.send_inline_markup_message(
                    markup=CATEGORY_CHOOSE_INLINE_MARKUP,
                    text='Оберіть одну із категорій:'
                )

            case 'headlines_category', category:
                gnews = GNews(user_chat_id=self.from_user.id, category=category)
                self.send_message(str(gnews.get_headlines()))


