from contextlib import asynccontextmanager
import uvicorn
import threading

from fastapi import FastAPI

def preprocess(x: float):
    return x + 3

models ={}


@asynccontextmanager
async def lifespan(app:FastAPI):
    # Loading thhe model
    models["answers"] = preprocess
    print("started")
    yield
    print("shutting down")
    models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def predict(x:float):
    result = models['answers'](x)
    return {"result": result}
@app.get("/print/")
def prin():
    for i in range(2000):
        print(i)

if __name__ == "__main__":
    thread1 = threading.Thread(target=prin)
    thread2 = threading.Thread(target=uvicorn.run("main:app", host="127.0.0.1", log_level="info"))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    print("hey now")