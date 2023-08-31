from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from pyngrok import ngrok
from config import Config
from message_parser import Update
from telegram_bot import TelegramBot
from flask import request
from openai_helper import OpenAiHelper

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS'))

db = SQLAlchemy(app)

@app.route('/', methods=["GET", "POST"])
def handle_webhook():
    update = Update(**request.json)
    chat_id = update.message.chat.id

    response = app.openai_helper.get_response(update.message.text)
    app.bot.send_message(chat_id, response)

    return "OK", 200

def run_ngrok(port=8000):
    http_tunnel = ngrok.connect(port)
    return http_tunnel.public_url

app.bot = TelegramBot(Config.TELEGRAM_TOKEN)
host = run_ngrok(Config.PORT)
app.bot.set_webhook(host)
app.openai_helper = OpenAiHelper(Config.OPENAI_TOKEN)

def main():
    app.run(port=Config.PORT, debug=True, use_reloader=False)

if __name__ == "__main__":
    main()