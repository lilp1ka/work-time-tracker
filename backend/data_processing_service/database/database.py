import asyncio

import motor.motor_asyncio
MONGO_DETAILS = "mongodb://mongo-service:27017/workInfo"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.workInfo
collection = database.get_collection("Logs")