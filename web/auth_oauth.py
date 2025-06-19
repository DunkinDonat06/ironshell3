from fastapi_users.authentication import OAuth2PasswordBearerWithCookie
from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase
from .models import User
from .db import get_user_db

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="auth/jwt/login")

fastapi_users = FastAPIUsers(
    get_user_db,
    [oauth2_scheme],
    User,
)

# В main.py или web.py
from fastapi import FastAPI
from .auth_oauth import fastapi_users

app = FastAPI()
app.include_router(fastapi_users.get_auth_router(oauth2_scheme), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(), prefix="/auth", tags=["auth"])