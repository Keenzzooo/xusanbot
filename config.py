import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("8771059479:AAFx_4ySlEpqMtt2ZJXYS5gZGHzWkoO4FLo", "")
DATABASE_PATH = os.getenv("DATABASE_PATH", "users.db")
