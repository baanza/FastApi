from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import SQLModel, Session, create_engine, select, Field

class HeroBase(SQLModel):
    name : str = Field(index=True)
    age: int | None = Field(default=None, index=True)

class Hero(HeroBase, table = True):
    id: int | None = Field(default=None, index=True)
    secret_name : str

class HeroPublic(HeroBase):
    id: int

class Herocreate(HeroBase):
    secret_name: str

class HeroUpdate(HeroBase):
    name: str | None = None
    age : int | None = None
    secret_name : str | None = None

db_name = "trial.db"
db_url = f"sqlite:///{db_name}"

conn_args = {"Check_same_thread": False}
engine = create_engine()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
def get_session():
    with Session(engine) as session:
        yield session

sessionDependence = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_tables()

@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero:Herocreate, session: sessionDependence):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

