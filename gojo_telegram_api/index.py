from telethon.sync import TelegramClient, events
from telethon.tl.types import InputPeerUser
import os
from dotenv import load_dotenv
import gpt
load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

def get_messages(messages, target_messages):
   for message in messages[::-1]:
      if message.out:
         role = "assistant"
      else:
         role = "user"
      target_messages.append({"role": role, "content": message.message})


with TelegramClient('gojo_rent', api_id, api_hash) as client:
   print('bot started...')

   @client.on(events.NewMessage(incoming=True))
   async def handler(event):
      # print(event)
      messages = []
      limit = 10
      sender = await event.get_input_sender()
      get_messages(await client.get_messages(sender, limit=limit), messages)
      # get_messages(await client.get_messages(user_id, reverse=True, limit=50), messages)
      print(messages)
      reply = gpt.get_reply(messages)
      print(reply)
      await client.send_message(sender, reply)

   print('bot running...')
   client.run_until_disconnected()