from fastapi import FastAPI, Query, Path
from typing import Annotated
from decimal import Decimal
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

#  --- HW3 ---
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.get("/items/{item_id}")
async def read_items(
    item_id : Annotated[Decimal, Path(ge=1, le=1000, description="Item ID must be between 1 and 1000.")],
    q : Annotated[str | None, Query(min_length=3, max_length=50, description = "Query 'q' must be between 3 and 50 characters.")] = None,
    sort_order : Annotated[str, Query(pattern="^(asc|desc)$")] = "asc"
):
    result = {
        "item_id": item_id,
        "description": f"This is a sample item." if not q else f"This is a sample item that matches the query {q}",
        "sort_order": sort_order
    }
    
    return result

@app.put("/items/{item_id}")
async def update_items(
    item_id : Annotated[Decimal, Path(ge=1, le=1000, description="Item ID must be between 1 and 1000.")],
    item: Item = None,
    q : Annotated[str | None, Query(min_length=3, max_length=50, description = "Query 'q' must be between 3 and 50 characters.")] = None,
):
    result = {"item_id": item_id, **item.dict()}

    if q:
        result.update({"q": q})

    return result