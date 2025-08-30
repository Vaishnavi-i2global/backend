from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os

client = AsyncIOMotorClient(os.getenv('DATABASE_URL'))
db = client.notes_app_test

