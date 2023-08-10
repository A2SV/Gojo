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
         print("new message")
         await client.send_read_acknowledge(event.chat_id)
         get_messages(await client.get_messages(sender, limit=limit), messages)

         post_prompt = "\n\nHow likely is it, on a scale of 0 to 9 (only integers), that a Gojo virtual assistant may respond with the above sentences related to the context information? Please reply with the rating number only."
         reply = gpt.get_reply(messages)
         reply_rating = gpt.get_reply([{"role": "user", "content": reply+post_prompt}])
         if not reply_rating.isdigit() or int(reply_rating[0]) < 5:
            reply = "This is beyond my scope"
            
         await client.send_message(sender, reply)

      print('bot running...')
      client.run_until_disconnected()

# if not string_session:
#    string_session = asyncio.run(session_handler.get_session())
#    print(string_session)
# else:
#    main()

main()