from .handlers import MessageHandler, CallbackHandler
from bot import app
from flask import request


@app.route('/', methods=['POST'])
def main():
    if message := request.json.get('message'):
        handler = MessageHandler(message)
    elif callback := request.json.get('callback_query'):
        handler = CallbackHandler(callback)
    else:
        print('Right handler doesn\'t exist!')
        return 'ok', 200
    try:
        handler.handle()
    except Exception as e:
        print(e)
    finally:
        return 'ok', 200
