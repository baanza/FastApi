from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

items = {
    'foo': 'foo init..',
    'dat': 'shit'
}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    print(item_id in items)
    if item_id not in items:
        raise HTTPException(status_code=404, detail='sijui kenye kinaendelea')
    return {
        'item': items[item_id]
    }

#creating  custom errors
class MyException(Exception):
    def __init__(self, name:str):
        self.name = name

@app.exception_handler(MyException)
async def MyExceptionHandler(request: Request, exc:MyException):
    return JSONResponse(
        status_code = 418,
        content = {
            'detail': f"info {exc.name}"
        }
    )

@app.get('/send/{need}')
async def getInfo(need: str):
    if need not in items:
        raise MyException(name=need)
    return {
        'item': items[need]
    }