import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from middleware.jwt_middleware import JWTMiddleware
from routes.data_routes import data_router

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    ),
    Middleware(JWTMiddleware)
]

app = FastAPI(middleware=middleware)

app.include_router(data_router, prefix="/data", tags=["data"])