import asyncio
import requests
import time
from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from dotenv import load_dotenv
import os

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv("PHONE_NUMBER")
verification_url = os.getenv("VERIFICATION_URL")

def get_verification_code():
    verification_code = ''
    while len(verification_code) != 5:
        try:
            verification_code = requests.get(verification_url).content.decode()
        except:
            print('not yet')
            
        time.sleep(30)

    return verification_code

async def get_session():
    print('getting session string...')
    client = TelegramClient(StringSession(''), api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        verification_code = get_verification_code()
        await client.sign_in(phone_number, verification_code)
    
    await client.disconnect()
    return client.session.save()
