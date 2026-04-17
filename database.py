from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URL, DB_NAME

client = AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]

users_collection = db["users"]
tasks_collection = db["tasks"]
sessions_collection = db["sessions"]