import quart.flask_patch
import asyncio
import hypercorn.asyncio
from pyngrok import ngrok
from quart import Quart, request
from flask_sqlalchemy import SQLAlchemy
import os
from pyngrok import ngrok
from config import Config
from message_parser import Update
from telegram_bot import TelegramBot
from openai_helper import OpenAiHelper

app = Quart(__name__)
app.config.from_object(os.getenv('APP_SETTINGS'))

db = SQLAlchemy(app)

@app.route('/', methods=["GET", "POST"])
async def handle_webhook():
    update = Update(**await request.json)
    chat_id = update.message.chat.id
    # history = await app.bot.get_chat_history(chat_id)
    # print(history)
    response = app.openai_helper.get_response(update.message.text)    
    app.bot.send_message(chat_id, response)

    return "OK", 200

def run_ngrok(port=8000):
    http_tunnel = ngrok.connect(port)
    return http_tunnel.public_url

@app.before_serving
async def startup():
    app.bot = TelegramBot(Config.TELEGRAM_TOKEN)    
    ngrok.set_auth_token(os.getenv("NGROK_AUTH_TOKEN"))
    host = run_ngrok(Config.PORT)
    app.bot.set_webhook(host)
    app.openai_helper = OpenAiHelper(Config.OPENAI_TOKEN)

async def main():
    quart_cfg = hypercorn.Config()
    quart_cfg.bind = [f"127.0.0.1:{Config.PORT}"]
    await hypercorn.asyncio.serve(app, quart_cfg)

if __name__ == "__main__":
    asyncio.run(main())