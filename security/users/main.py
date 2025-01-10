from fastapi import FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse
from schemas import userOut, UserAuth
from utils import get_hashed_password
from uuid import uuid4

app = FastAPI()

@app.post("/signup", summary="Create new user", response_model=userOut)
async def create_user(data: UserAuth):
