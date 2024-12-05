import sys
import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from fastapi import FastAPI


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
]
app = FastAPI(middleware=middleware)

