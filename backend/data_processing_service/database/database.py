from motor.motor_asyncio import AsyncIOMotorClient

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

mongodb = MongoDB()

def connect_to_mongo():
    mongodb.client = AsyncIOMotorClient("mongodb://mongo-service:27017")
    mongodb.db = mongodb.client.data_db
    print("Connected to MongoDB")

def close_mongo_connection():
    mongodb.client.close()
    print("Closed connection to MongoDB")