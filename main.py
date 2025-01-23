from fastapi import FastAPI
from pydantic import BaseModel 

app = FastAPI()
# test test
# http://localhost:8080/
@app.get("/")
async def root():
    return {"message": "Hello World"}

# http://localhost:8080/items/{item_id}?q={q}
@app.put("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    result = {
        "item_id": item_id,
        "name": "Test Item",
        "description": "A test description",
        "price": 10.5,
        "tax": 1.5
    }
    if q:
        result.update({"q": q})
    return result
