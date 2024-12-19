import motor.motor_asyncio
import asyncio
# docker network inspect backend_backend-network - взять ип data-db  и воркает
MONGO_DETAILS = "mongodb://172.29.0.5:27017/workInfo"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.workInfo
collection = database.get_collection("Logs")

async def check_db_connection():
    try:
        await client.server_info()
        print("Успешно подключились к MongoDB.")
    except Exception as e:
        print(f"Ошибка подключения к MongoDB: {e}")

async def main():
    await check_db_connection()

if __name__ == "__main__":
    asyncio.run(main())
