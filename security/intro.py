"""
Creating security  features  for fastapi application
OAuth2.0

"""

from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel

app = FastAPI()

# DEFINE A DICTIONARY CONTAINING SAMPLE USERS

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: str | None = None
    full_name : str | None = None
    disabled : bool | None = None

class userInDb(User):
    hashed_password : str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return userInDb(**user_dict)

def decode_token(token):
    return User(
        username= token + "decoded", email="heyhi@gmail.com", full_name="Hey Hi"
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    return user

@app.get("/users/me/")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user