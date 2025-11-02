from fastapi import FastAPI, Query, Path
from typing import Annotated
from fastapi.responses import JSONResponse
from models import TodoItem
import uvicorn

app = FastAPI(title="Wyatt's FastAPI Demo", description="Your number one to-do app!")

todos = []
#Create routes
@app.get("/", description="A great place to make your first API Call") #Define what path we are using
def home():
    return {"Hello": "FastAPI"} #Json response

@app.get("/todos", description="Show all of the to do items we have", response_description="A list of to do items", response_model=list[TodoItem])
def get_todos(limit: Annotated[int, Query(description="The number of responses you want", ge=0)] = 20, offset: Annotated[int, Query(description="The index of the item you want to start with", ge=0)] = 0): #This is where we specify query paramaters.
    fun_offset = offset
    fun_limit = limit
    if fun_offset >= len(todos):
        return []
    if fun_offset + fun_limit >= len(todos):
        fun_limit = len(todos) - fun_offset
    return todos[fun_offset:fun_offset+fun_limit]

@app.get("/todos/complete", description="Show all of the completed to do items we have", response_description="A list of to do items", response_model=list[TodoItem])
def todos_complete(limit: Annotated[int, Query(description="The number of responses you want", ge=0)] = 20, offset: Annotated[int, Query(description="The index of the item you want to start with", ge=0)] = 0): #This is where we specify query paramaters.
    completed_todos = []
    for todo in todos:
        if todo.completed:
            completed_todos.append(todo)
    fun_offset = offset
    fun_limit = limit
    if fun_offset >= len(todos):
        return []
    if fun_offset + fun_limit >= len(todos):
        fun_limit = len(todos) - fun_offset
    return completed_todos[fun_offset:fun_offset+fun_limit]

@app.get("/todos/incomplete", description="Show all of the noncompleted to do items we have", response_description="A list of to do items", response_model=list[TodoItem])
def todos_incomplete(limit: Annotated[int, Query(description="The number of responses you want", ge=0)] = 20, offset: Annotated[int, Query(description="The index of the item you want to start with", ge=0)] = 0): #This is where we specify query paramaters.
    noncompleted_todos = []
    for todo in todos:
        if not todo.completed:
            noncompleted_todos.append(todo)
    fun_offset = offset
    fun_limit = limit
    if fun_offset >= len(todos):
        return []
    if fun_offset + fun_limit >= len(todos):
        fun_limit = len(todos) - fun_offset
    return noncompleted_todos[fun_offset:fun_offset+fun_limit]

@app.post("/todo/{text}", description="Addd a new to do item, returns the to do item you sent.", response_description="The item you just added", response_model=TodoItem) #Item is a path parameter
def add_todo(text: Annotated[str, Path(description="The text you want on the item")]):
    item = TodoItem(text=text)
    todos.append(item)
    return item

@app.delete("/todo/{index}", description="Remove a todo item at a certain index", response_model=TodoItem, response_description="The todo item you just deleted", responses={
    404 : {"description": "index not found"}
})
def remove_todo(index: Annotated[int, Path(description="The index of the todo item you want to remove", ge=0)]):
    if index >= len(todos):
        return JSONResponse(status_code=404, content="Index not found")
    removed = todos[index]
    del todos[index]
    return removed

@app.post("/complete/{index}", description="Complete the todo item at the selected index", response_model=TodoItem, response_description="The todo item you just checked", responses={
    404: {"description": "index not found"}
})
def complete_todo(index: Annotated[int, Path(description="The index of the todo item you want to complete", ge=0)]):
    if index >= len(todos):
        return JSONResponse(status_code=404, content="Index not found")
    todos[index].completed = True
    return todos[index]

@app.post("/uncomplete/{index}", description="Remove complettion of the todo item at the selected index", response_model=TodoItem, response_description="The todo item you just unchecked", responses={
    404: {"description": "index not found"}
})
def uncomplete_todo(index: Annotated[int, Path(description="The index of the todo item you want to uncomplete", ge=0)]):
    if index >= len(todos):
        return JSONResponse(status_code=404, content="Index not found")
    todos[index].completed = False
    return todos[index]

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')