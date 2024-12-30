from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException, Cookie

app = FastAPI()

async def cookie_fetcher(cookie: Annotated[str, Cookie()]):
    if cookie == "trial":
        raise HTTPException(status_code=418, detail="stop trying")
    return cookie

async def HeaderFetcher(key: Annotated[str, Header()]):
    return key


@app.get('/users/', dependencies=[Depends(cookie_fetcher), Depends(HeaderFetcher)])
async def main():
    return {
        "depends": "On two functions"
    }