from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def read_root():
    return {52: "52"}


class Item(BaseModel):
    name: str
    description: str = None  # Поле необязательное
    price: float
    tax: float = None  # Поле необязательное


@app.post("/")
async def create_item(item: Item):
    print(f"Получены данные: {item}")
    return {"message": "Item created", "item": item}
