"""
Creating security  features  for fastapi application
OAuth2.0

"""

from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel

app = FastAPI()

# DEFINE A DICTIONARY CONTAINING SAMPLE USERS

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "hashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "hashedsecret2",
        "disabled": True,
    },
}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str):
    return "hashed" + password

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
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid user credentials",
            headers={
                "something": "Bearer"
            }
        )
    return user
async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User offline"
        )
    return current_user

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400,
            detail="Incorrect Username"
        )
    user = userInDb(**user_dict)
    hashed_password = hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect userName or password"
        )
    return {
        "access_token" : user.username,
        "token_type" : "Bearer"
    }


@app.get("/users/me/")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user