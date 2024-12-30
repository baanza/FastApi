from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum

app = FastAPI()

class Tags(Enum):
    person = 'people'
    items = 'items'

class Item(BaseModel):
    name: str
    description: str | None= None
    price: float
    tax : float | None= None
    tags : set[str] = set()
   

class Person(BaseModel):
    username: str
    password: str= Field('pass123')
    gender : str = Literal['male', 'female']


@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED, tags=[Tags.items])
async def create_item(item: Item):
    return item

@app.post("/people/", response_model=Person, tags= [Tags.person])
async def create_user(person: Person):
    return person

@app.post("/items/{tax}", response_model=Item, tags=[Tags.items])
async def get_specific_item(item: Item, tax: float):
    if tax > item.tax:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT)
    return Item