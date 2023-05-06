from pprint import pprint
from .handlers import MessageHandler, CallbackHandler
from bot import app
from flask import request
import requests
from .settings import *


@app.route('/', methods=['POST'])
def main():
    pprint(request.json)  ##########
    if message := request.json.get('message'):
        handler = MessageHandler(message)
    elif callback := request.json.get('callback_query'):
        handler = CallbackHandler(callback)
    handler.handle()
    return 'ok', 200


@app.get('/h')
def hui():
    return '<h1>ТИ ХУЙ</h1>'
