from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def read_root():
    print("Запрос пришёл на /")
    return {"message": "Hello, FastAPI!"}


# Определим модель данных для POST-запроса
class Item(BaseModel):
    name: str
    description: str = None  # Поле необязательное
    price: float
    tax: float = None  # Поле необязательное


@app.post("/")
async def create_item(item: Item):
    print(f"Получены данные: {item}")
    return {"message": "Item created", "item": item}
