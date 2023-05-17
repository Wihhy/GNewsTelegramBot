import json
import os
import requests
from dotenv import load_dotenv
from flask_paginate import Pagination
from bot import db
from .settings import *
from .models import User, Settings, Article
from .services import GNews

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')


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

    def send_photo_and_inline_markup(self, photo_url: str, markup):
        data = {
            'chat_id': self.from_user.id,
            'photo': photo_url,
            'reply_markup': {'inline_keyboard': markup}
        }
        requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendPhoto', json=data)


class MessageHandler(TelegramHandler):

    def __init__(self, user_data):
        self.message_text = user_data.get('text')
        self.from_user = FromUser(**user_data.get('from'))
        self.user_in_db = User.query.get(self.from_user.id)

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
        if self.user_in_db.is_searching is True:
            self.user_in_db.is_searching = False
            db.session.commit()
            gnews = GNews(user_chat_id=self.from_user.id, q=self.message_text)
            gnews.get_news()
            first_art = Article.query.filter(Article.user_chat_id == int(self.from_user.id)).first()
            markup = [[{
                'text': 'Детальніше',
                'callback_data': json.dumps({'article_id': str(first_art.id)})
            }],
                [{
                    'text': 'Наступна',
                    'callback_data': json.dumps({'route': 'headlines', 'page': 2})
                }]]

            self.send_message(text=first_art.title)
            self.send_photo_and_inline_markup(photo_url=first_art.image_url, markup=markup)


class CallbackHandler(TelegramHandler):

    def __init__(self, data):
        self.from_user = FromUser(**data.get('from'))
        self.callback_data = json.loads(data.get('data'))

    def handle(self):
        match self.callback_data:
            # SETTINGS
            case {'route': 'settings'}:
                match self.callback_data:
                    case {'act': 'choose_country'}:
                        self.send_inline_markup_message(
                            markup=COUNTRY_CHOOSE_INLINE_MARKUP,
                            text='Оберіть із переліку доступних країн:')

                    case {'act': 'choose_language'}:
                        self.send_inline_markup_message(
                            markup=LANGUAGE_CHOOSE_INLINE_MARKUP,
                            text='Оберіть із переліку доступних мов:')

                    case {'act': 'setcountry'}:
                        country_code = self.callback_data.get('country_code')
                        country_name = COUNTRY_DICT.get(country_code)
                        user_settings = User.query.get(self.from_user.id)
                        user_settings.settings.country = country_code
                        db.session.commit()
                        self.send_message(text=f'Успішно! Країну пошуку змінено! Тепер це: {country_name}!')

                    case {'act': 'setlang'}:
                        language_code = self.callback_data.get('language_code')
                        language_name = LANGUAGE_DICT.get(language_code)
                        user_settings = User.query.get(self.from_user.id)
                        user_settings.settings.language_code = language_code
                        db.session.commit()
                        self.send_message(text=f'Успішно! Мову пошуку змінено! Тепер це {language_name}!')

            # NEWS
            case {'route': 'choose_category'}:
                print(type(self.callback_data))
                self.send_inline_markup_message(
                    markup=CATEGORY_CHOOSE_INLINE_MARKUP,
                    text='Оберіть одну із категорій:'
                )

            case {'route': 'search'}:
                self.send_message(
                    text='Введіть текст для пошуку:'
                )
                user = User.query.get(self.from_user.id)
                user.is_searching = True
                db.session.commit()

            case {'route': 'headlines'}:
                if 'category' in self.callback_data:
                    category = self.callback_data.get('category')
                    gnews = GNews(user_chat_id=self.from_user.id, category=category)
                    gnews.get_news()

                news_list = Article.query.filter(Article.user_chat_id == int(self.from_user.id)).all()

                if news_list:
                    if 'page' in self.callback_data:
                        page = int(self.callback_data['page'])
                    else:
                        page = 1

                    news_on_page = news_list[page - 1: page]
                    news_buttons = []
                    for art in news_on_page:
                        news_buttons.append([{
                            'text': 'Детальніше',
                            'callback_data': json.dumps({'article_id': str(art.id)})
                        }])
                        photo_url = art.image_url
                        self.send_message(text=art.title)

                    pagination = Pagination(page=page, total=len(news_list), per_page=1,
                                            record_name='articles')
                    markup = news_buttons
                    if pagination.has_next:
                        markup.append([{
                            'text': 'Наступна',
                            'callback_data': json.dumps({'route': 'headlines', 'page': page + 1})
                        }])
                    if page > 1:
                        markup.append([{
                            'text': 'На першу',
                            'callback_data': json.dumps({'route': 'headlines'})
                        }])
                    self.send_photo_and_inline_markup(photo_url=photo_url, markup=markup)

            case {'article_id': article_id}:
                article = Article.query.filter(Article.id == article_id).first()
                description = article.description
                markup = [[{'text': 'Стаття повністю',
                            'url': article.article_url}]]
                self.send_inline_markup_message(text=description, markup=markup)


