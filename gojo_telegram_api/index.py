from telethon.sync import TelegramClient, events
from telethon.tl.types import InputPeerUser
from telethon.sessions import StringSession
from telethon import connection
import os
from dotenv import load_dotenv
import gpt
import io
import sys
import session_handler
import asyncio
load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
string_session = os.getenv("TELEGRAM_SESSION")
proxy = os.getenv("PROXY")
proxy_secret = os.getenv("PROXY_SECRET")
proxy_port = os.getenv("PROXY_PORT")

def get_messages(messages, target_messages):
   char_limit = 750
   for message in messages[::-1]:
      if message.out:
         role = "assistant"
      else:
         role = "user"
      if len(message.message) < char_limit:
         target_messages.append({"role": role, "content": message.message})

def main():
   with TelegramClient(StringSession(string_session), api_id, api_hash) as client:
      print('bot started...')
      @client.on(events.NewMessage(incoming=True))
      async def handler(event):
         messages = []
         limit = 30
         sender = await event.get_input_sender()
         get_messages(await client.get_messages(sender, limit=limit), messages)
         # get_messages(await client.get_messages(user_id, reverse=True, limit=50), messages)
         reply = gpt.get_reply(messages)
         await client.send_message(sender, reply)

      print('bot running...')
      client.run_until_disconnected()

# if not string_session:
#    string_session = asyncio.run(session_handler.get_session())
#    print(string_session)
# else:
#    main()

main()