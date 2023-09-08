import requests
from config import Config
from models import Message
from sqlalchemy import desc

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.bot_api_url = f"{Config.TELEGRAM_API}/bot{self.token}"

    def set_webhook(self, host):
        host = host.replace("http:", "https:")
        set_webhook_url = f"{self.bot_api_url}/setWebhook?url={host}"
        response = requests.get(set_webhook_url)
        response.raise_for_status()

    def send_message(self, chat_id, message):
        send_message_url = f"{self.bot_api_url}/sendMessage"
        response = requests.post(send_message_url, json={"chat_id": chat_id,
                                                          "text": message})
        response.raise_for_status()

    def get_chat_history(self, chat_id, limit=30):
        history = Message.query.filter(Message.chat_id == chat_id).order_by(desc(Message.timestamp)).limit(limit).all()
        for i in range(len(history)):
            if history[i].from_bot:
                role = 'assistant'
            else:
                role = 'user'

            history[i] = {"role": role, "content": str(history[i])}
        
        return history[::-1]