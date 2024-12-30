from fastapi import FastAPI
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fakedb = {}
app = FastAPI()

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None

@app.put('/items/{item_id}')
async def updateshit(item_id: str, item: Item):
    jsoned_data = jsonable_encoder(item)
    fakedb[id] = jsoned_data
    print(fakedb)