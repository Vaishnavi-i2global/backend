from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

client = AsyncIOMotorClient(os.getenv('DATABASE_URL'))
db = client.notes_app_test

