import json

CURRENT_WEBHOOK_URL = 'https://f902-178-74-212-109.ngrok-free.app'  # TODO DELETE

TG_BASE_URL = 'https://api.telegram.org/bot'

GREETING = 'Привіт! Я Корисний бот, Ви можете використовувати як кнопки для зручного використання,' \
           ' так і просто написати мені що саме хочете робити! У налаштуваннях Ви можете змінити' \
           'краіну, а також мову пошуку.'

NEWS_SETTINGS_REPLY_MARKUP = [[
    {
        'text': 'Новини',
    },
    {
        'text': 'Налаштування'
    }
]]

HEADLINES_SEARCH_INLINE_MARKUP = [
    [
        {'text': 'Пошук', 'callback_data': json.dumps({'route': 'news',
                                                       'act': 'search'})},
        {'text': 'Топові заголовки', 'callback_data': json.dumps({'route': 'choose_category'})}
    ]
]

SETTINGS_CHOOSE_INLINE_MARKUP = [
    [
        {'text': 'Країна пошуку', 'callback_data': json.dumps({'route': 'settings',
                                                               'act': 'choose_country'})},
        {'text': 'Мова пошуку', 'callback_data': json.dumps({'route': 'settings',
                                                             'act': 'choose_language'})}
    ]
]

COUNTRY_CHOOSE_INLINE_MARKUP = [
    [
        {'text': 'Канада', 'callback_data': json.dumps({'route': 'settings',
                                                        'act': 'setcountry',
                                                        'country_code': 'ca'})},
        {'text': 'США', 'callback_data': json.dumps({'route': 'settings',
                                                     'act': 'setcountry',
                                                     'country_code': 'us'})}
    ],
    [
        {'text': 'Великобританія', 'callback_data': json.dumps({'route': 'settings',
                                                                'act': 'setcountry',
                                                                'country_code': 'gb'})},
        {'text': 'Німеччина', 'callback_data': json.dumps({'route': 'settings',
                                                           'act': 'setcountry',
                                                           'country_code': 'de'})}
    ],
    [{'text': 'Україна', 'callback_data': json.dumps({'route': 'settings',
                                                      'act': 'setcountry',
                                                      'country_code': 'ua'})}]
]

LANGUAGE_CHOOSE_INLINE_MARKUP = [
    [
        {'text': 'Українська', 'callback_data': json.dumps({'route': 'settings',
                                                            'act': 'setlang',
                                                            'language_code': 'uk'})}
    ],
    [
        {'text': 'Англійська', 'callback_data': json.dumps({'route': 'settings',
                                                            'act': 'setlang',
                                                            'language_code': 'en'})}
    ],
    [{'text': 'Німецька', 'callback_data': json.dumps({'route': 'settings',
                                                       'act': 'setlang',
                                                       'language_code': 'de'})}]
]

CATEGORY_CHOOSE_INLINE_MARKUP = [
    [
        {
            'text': 'Світ', 'callback_data': json.dumps({'route': 'headlines',
                                                         'category': 'world'})
        },
        {
            'text': 'Нація', 'callback_data': json.dumps({'route': 'headlines',
                                                          'category': 'nation'})
        }
    ],
    [
        {
            'text': 'Бізнес', 'callback_data': json.dumps({'route': 'headlines',
                                                           'category': 'business'})
        },
        {
            'text': 'Технології', 'callback_data': json.dumps({'route': 'headlines',
                                                               'category': 'technology'})
        }
    ],
    [
        {
            'text': 'Розваги', 'callback_data': json.dumps({'route': 'headlines',
                                                            'category': 'entertainment'})
        },
        {
            'text': 'Спорт', 'callback_data': json.dumps({'route': 'headlines',
                                                          'category': 'sports'})
        }
    ],
    [
        {
            'text': 'Наука', 'callback_data': json.dumps({'route': 'headlines',
                                                          'category': 'science'})
        },
        {
            'text': 'Здоровʼя', 'callback_data': json.dumps({'route': 'headlines',
                                                             'category': 'health'})
        }
    ],
    [
        {
            'text': 'Загальна', 'callback_data': json.dumps({'route': 'headlines',
                                                             'category': 'general'})
        }
    ]
]

COUNTRY_DICT = {
    'ca': 'Канада',
    'de': 'Німеччина',
    'ua': 'Україна',
    'us': 'США',
    'gb': 'Великобританія'
}

LANGUAGE_DICT = {
    'uk': 'Українська',
    'de': 'Німецька',
    'en': 'Англійська'
}
