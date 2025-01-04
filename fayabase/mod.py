from sqlmodel import SQLModel, select, create_engine,  Session, Field

engine = create_engine("sqlite:///server.db", connect_args={"check_same_thread": False})

# SQLModel.metadata.create_all(engine)

class Album(SQLModel, table = True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    artistName : str = Field(index=True)
    runtime: str = Field()
    song_list: str = Field()

def serach_artist(artist: str):
    with Session(engine) as session:
        statement = select(Album).where(Album.artistName == artist)
        results = session.exec(statement)
        for album in results:
            print(album.name)




