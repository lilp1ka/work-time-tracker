import sys
import os

from fastapi import FastAPI
from .routes import auth_router, email_router, users_router, token_router, change_router
from fastapi.middleware.cors import CORSMiddleware
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(email_router, prefix="/email", tags=["email"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(token_router, prefix="/token", tags=["token"])
app.include_router(change_router, prefix="/change", tags=["change"])