
CURRENT_WEBHOOK_URL = 'https://f902-178-74-212-109.ngrok-free.app'  ###

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
        {'text': 'Пошук', 'callback_data': 'news search'},
        {'text': 'Топові заголовки', 'callback_data': 'news headlines'}
    ]
]

SETTINGS_CHOOSE_INLINE_MARKUP = [
    [
        {'text': 'Країна пошуку', 'callback_data': 'choose_country 0 '},
        {'text': 'Мова пошуку', 'callback_data': 'choose_language 0'}
    ]
]

COUNTRY_CHOOSE_INLINE_MARKUP = [
    [
        {'text': 'Канада', 'callback_data': 'set_country_code Канада ca'},
        {'text': 'США', 'callback_data': 'set_country_code США us'}
    ],
    [
        {'text': 'Великобританія', 'callback_data': 'set_country_code Великобританія gb'},
        {'text': 'Німеччина', 'callback_data': 'set_country_code Німеччина de'}
    ],
    [{'text': 'Україна', 'callback_data': 'set_country_code Україна ua'}]
]

LANGUAGE_CHOOSE_INLINE_MARKUP = [
    [
        {'text': 'Українська', 'callback_data': 'set_language_code Українська uk'}
    ],
    [
        {'text': 'Англійська', 'callback_data': 'set_language_code Англійська en'}
    ],
    [{'text': 'Німецька', 'callback_data': 'set_language_code Німецька de'}]
]

CATEGORY_CHOOSE_INLINE_MARKUP = [
    [
        {
            'text': 'Світ', 'callback_data': 'headlines_category world'
        },
        {
            'text': 'Нація', 'callback_data': 'headlines_category nation'
        }
    ],
    [
        {
            'text': 'Бізнес', 'callback_data': 'headlines_category business'
        },
        {
            'text': 'Технології', 'callback_data': 'headlines_category technology'
        }
    ],
    [
        {
            'text': 'Розваги', 'callback_data': 'headlines_category entertainment'
        },
        {
            'text': 'Спорт', 'callback_data': 'headlines_category sports'
        }
    ],
    [
        {
            'text': 'Наука', 'callback_data': 'headlines_category science'
        },
        {
            'text': 'Здоровʼя', 'callback_data': 'headlines_category health'
        }
    ],
    [
        {
            'text': 'Загальна', 'callback_data': 'headlines_category general'
        }
    ]
]
