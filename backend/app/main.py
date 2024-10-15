from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {1: "52 нахуй + 52 нахуй + 52 нахуй"}
