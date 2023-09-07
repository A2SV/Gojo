from pyngrok import ngrok
from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from pyngrok import ngrok
from config import Config
from message_parser import Update
from telegram_bot import TelegramBot
import openai_helper as openAiHelper
from models import *
import time

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS'))
db.init_app(app)

migrate = Migrate(app, db)

@app.route('/', methods=["GET", "POST"])
def handle_webhook():
    req = request.json
    update = Update(**req)
    chat_id = update.message.chat.id
    history = app.bot.get_chat_history(chat_id)
    user_message = update.message.text
    message = Message(chat_id, user_message, False, req['message']['date'])
    db.session.add(message)

    history.append({"role": "user", "content": user_message})
    response = openAiHelper.get_reply(history)   

    message = Message(chat_id, response, True, int(time.time()))
    app.bot.send_message(chat_id, response)
    
    db.session.add(message)
    db.session.commit()
    return "OK", 200

def run_ngrok(port=8000):
    http_tunnel = ngrok.connect(port)
    return http_tunnel.public_url

app.bot = TelegramBot(Config.TELEGRAM_TOKEN)    
ngrok.set_auth_token(os.getenv("NGROK_AUTH_TOKEN"))
host = run_ngrok(Config.PORT)
app.bot.set_webhook(host)

def main():
    app.run(port=Config.PORT, debug=True)

if __name__ == "__main__":
    main()