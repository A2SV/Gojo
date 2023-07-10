from telethon.sync import TelegramClient, events
import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')


with TelegramClient('Rediet_Demisse', api_id, api_hash) as client:
   client.send_message('me', 'Hello, myself!')

   @client.on(events.NewMessage(pattern='(?i).*Hello'))
   async def handler(event):
      await event.reply('Hey!')

   client.run_until_disconnected()
