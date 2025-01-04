from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager
import uvicorn


# creating a database table
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name : str

sqlite_filename = "database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"

connext_args = {'check_same_thread': False}
engine = create_engine(sqlite_url, connect_args=connext_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()

@app.on_event("startup")
def lifespan():
    create_db_and_tables()



@app.post("/heroes/")
def create_Hero(hero: Hero, session: SessionDep):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.get("/heroes")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit : Annotated[int, Query(le=100)] = 0,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

# getting only one hero

@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)

    if not hero:
        raise HTTPException(status_code=404, detail="Hero Not found")
    return hero

# deleting a hero
@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)

    if not hero:
        raise HTTPException(status_code=404, detail="Hero Not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}

# going on i guess

# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)
