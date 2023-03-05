from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class Item(BaseModel):
    item_id: int
    task: str
    complete: bool


app = FastAPI()

# data is hard-coded for now, rather than implementing DB with ORM
# if I were to implement a db, I wouuld search a specific list by user_id
# (or user_id and list_id once implementing multiple to-do lists)

todoList = [{"item_id": 1, "task": "get the server working", "complete": True},
            {"item_id": 2,"task": "get the posting and updating working", "complete": True},
            {"item_id": 3, "task": "get deleting working, then set up the db.", "complete": False},
            {"item_id": 4, "task": "remove hard-coded data, and use database", "complete": False}]

# helper function to find index of list item, would move such item into a folder of helper methods in production


def findIndex(key, value):
    for i, dic in enumerate(todoList):
        if dic[key] == value:
            return i
    return -1


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/tasks")
async def root():
    return {"todoList": todoList}


@app.get("/tasks/{item_id}")
async def get_item_by_id(item_id: int):
    itemIdx = findIndex("item_id", item_id)
    return {"item": todoList[itemIdx]}


@app.post("/tasks")
async def post_item_to_list(item: Item):
    item_dict = item.dict()
    todoList.append(item_dict)
    return {"todoList": todoList}


@app.put("/tasks/{item_id}")
async def update_item_in_list(item_id: int, item: Item):
    itemIdx = findIndex("item_id", item_id)
    if itemIdx != -1:
        todoList[itemIdx] = item.dict()
        return {"todoList": todoList, "message": "successfully Updated!"}
    else:
        return {"message": "Error: Item Not Found"}


@app.delete("/tasks")
async def delete_list():
    todoList.clear()
    return {"todoList": todoList, "message": "successfully Deleted!"}


@app.delete("/tasks/{item_id}")
async def delete_item_in_list(item_id: int):
    itemIdx = findIndex("item_id", item_id)
    if itemIdx != -1:
        todoList.pop(itemIdx)
        return {"todoList": todoList, "message": "successfully Deleted!"}
    else:
        return {"message": "Error: Item Not Found"}
