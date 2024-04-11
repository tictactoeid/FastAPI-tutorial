from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from pydantic import BaseModel, Field, HttpUrl

from enum import Enum
from typing import Union, List, Annotated, Set, Any

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None,
        title="The description of the item",
        max_length=300
    )
    price: float = Field(
        gt=0,
        description="The price must be greater than zero"
    )
    tax: float | None = None
    tags: Set[str] = set()
    images: List[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: List[Item]



class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    elif model_name is ModelName.lenet:
        return {"model_name": model_name, "message": "LeCNN all the images"}
    else:
        return {"model_name": model_name, "message": "Have some residuals"}


# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item


@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item, query: str | None = None):
#     result = {"item_id": item_id, **item.dict()}
#     if query:
#         result.update({"query": query})
#     return result

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results


@app.get("/items/")
async def read_items(q: List[str] | None = Query(default=["foo", "bar"], max_length=50)):
    query_items = {"q": q}
    return query_items


@app.get("/items/{item_id}")
async def read_items(
        item_id: int = Path(title="The ID of the item to get", gt=0, le=1000),
        q: str | None = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    return images


@app.get("/items/cookie/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}


@app.get("/items/header/")
async def read_items(user_agent: str | None = Header(default=None)):
    return {"User-Agent": user_agent}


@app.get("/items/token/")
async def read_items(x_token: Union[List[str], None] = Header(default=None)):
    return {"X-Token values": x_token}