from fastapi import FastAPI, Query, Path, Body, Cookie, Form, File, UploadFile, HTTPException
from typing import Annotated
from decimal import Decimal
from pydantic import BaseModel, Field
from datetime import datetime, time, timedelta
from uuid import UUID

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
    item_id: Annotated[Decimal, Path(ge=1, le=1000, description="Item ID must be between 1 and 1000.")],
    q: Annotated[str | None, Query(min_length=3, max_length=50, description = "Query 'q' must be between 3 and 50 characters.")] = None,
    sort_order: Annotated[str, Query(pattern="^(asc|desc)$")] = "asc"
):
    result = {
        "item_id": item_id,
        "description": f"This is a sample item." if not q else f"This is a sample item that matches the query {q}",
        "sort_order": sort_order
    }
    
    return result

@app.put("/items/{item_id}")
async def update_items(
    item_id: Annotated[Decimal, Path(ge=1, le=1000, description="Item ID must be between 1 and 1000.")],
    item: Item = None,
    q: Annotated[str | None, Query(min_length=3, max_length=50, description = "Query 'q' must be between 3 and 50 characters.")] = None,
):
    result = {"item_id": item_id, **item.dict()}

    if q:
        result.update({"q": q})

    return result

#  --- HW4 ---
class Item_with_field(BaseModel):
    name: str
    description: str | None = Field(default=None, title="The description of the item")
    price: float = Field(gt = 0., title="The price of the item")
    tax: float | None = Field(default=None, title="The tax of the item")

@app.post("/items/filter/")
async def filter_items(
    price_min: Annotated[int, Query(description = "Minimum price of the item")],
    price_max: Annotated[int, Query(description = "Maximum price of the item")],
    tax_included: Annotated[bool, Query(description = "Boolean indicating whether tax is included in the price")],
    tags: Annotated[list[str], Query(description="List of tags to filter items")]
):
    result = {
        "price_range": [price_min, price_max],
        "tax_included": tax_included,
        "tags": tags,
        "message": "This is a filtered list of items based on the provided criteria."
    }
    
    return result

@app.post("/items/create_with_fields/")
async def add_items(
    item: Annotated[Item_with_field, Body()],
    importance: Annotated[int, Body()]
):
    return {"item": item, "importance": importance}

@app.post("/offers/")
async def add_offer(
    name: Annotated[str, Body()],
    discount: Annotated[float, Body()],
    items: Annotated[list[Item_with_field], Body()]
):
    result = {
        "offer_name": name,
        "discount": discount,
        "items": items
    }

    return result

@app.post("/users/")
async def add_offer(
    username: Annotated[str, Body()],
    email: Annotated[str, Body()],
    full_name: Annotated[str, Body()]
):
    result = {
        "username": username,
        "email": email,
        "full_name": full_name
    }
    
    return result

@app.post("/items/extra_data_types/")
async def extra_datatype(
    start_time: Annotated[datetime, Body()],
    end_time: Annotated[time, Body()],
    repeat_every: Annotated[timedelta, Body()],
    process_id: Annotated[UUID, Body()]
):
    result = {
        "message": "This is an item with extra data types.",
        "start_time": start_time,
        "end_time": end_time,
        "repeat_every": repeat_every,
        "process_id": process_id
    }

    return result

@app.get("/items/cookies/")
async def read_from_cookies(
    session_id: Annotated[str | None, Cookie(description = "Session ID from the client's cookies")] = None
):
    return {"session_id": session_id, "message": "This is the session ID obtained from the cookies."}

#  --- HW5 ---
@app.post("/items/form_and_file")
async def add_item_with_form_and_file(
    name: Annotated[str, Form()],
    price: Annotated[float, Form()],
    description: Annotated[str | None, Form()] = None,
    tax: Annotated[float | None, Form()] = None,
    file: UploadFile = File(...)
):
    if price < 0:
        raise HTTPException(status_code=400, detail="Price cannot be negative")
    
    return {
        "name": name,
        "description": description,
        "price": price,
        "tax": tax,
        "filename": file.filename,
        "message": "This is an item created using form data and a file."
    }