"""
    DEPENDENCY INJECTION
-A design pattern in which an object/function receives its dependencies,
from an external source rather that creating them

"""

from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()

async def common_params(q:str | None = None, skip: int=0, limit: int = 100):
    return {
        'q': q, "skip": skip, "limit": limit
    }

commonQuery = Annotated[dict, Depends(common_params)]
@app.get("/items/")
async def read_items(commons: commonQuery):
    return commons

@app.get('/users/', tags=['user'])
async def fetch_user(commons: commonQuery):
    return commons