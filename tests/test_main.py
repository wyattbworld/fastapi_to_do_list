'''
Note: The name of htis file MUST start with test_
'''
from fastapi.testclient import TestClient
from main import app, todos
from models import TodoItem
from fastapi.encoders import jsonable_encoder
import pytest

client = TestClient(app)

'''
This fixture ensures we get a clean copy of the todo list every time we run the test.
All tests should be independent.
'''
@pytest.fixture(autouse=True)
def reset_todos():
    todos.clear()

'''
Test that our root function is working
'''
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "FastAPI"}

'''
Test that we can get an empty to do list
'''
def test_get_todos_empty():
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []

'''
Tests adding and then removing a todo item.
'''
def test_add_and_remove_todo_item():
    response = client.post("/todo/apple")
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(TodoItem(text="apple"))
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == [jsonable_encoder(TodoItem(text="apple"))]
    response = client.delete("/todo/0")
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(TodoItem(text="apple"))
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []

'''
Test that we can get a todo list in the right order
'''
def test_get_todos():
    response = client.post("/todo/apple")
    response = client.post("/todo/banana")
    response = client.post("/todo/coconut")
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == [jsonable_encoder(TodoItem(text="apple")), jsonable_encoder(TodoItem(text="banana")), jsonable_encoder(TodoItem(text="coconut"))]

'''
Test that we can get a todo list with a small limit
'''
def test_get_todos_limit():
    response = client.post("/todo/apple")
    response = client.post("/todo/banana")
    response = client.post("/todo/coconut")
    response = client.get("/todos?limit=2")
    assert response.status_code == 200
    assert response.json() == [jsonable_encoder(TodoItem(text="apple")), jsonable_encoder(TodoItem(text="banana"))]

'''
Test that we can get a todo list with an offset
'''
def test_get_todos_offset():
    response = client.post("/todo/apple")
    response = client.post("/todo/banana")
    response = client.post("/todo/coconut")
    response = client.get("/todos?offset=1")
    assert response.status_code == 200
    assert response.json() == [jsonable_encoder(TodoItem(text="banana")), jsonable_encoder(TodoItem(text="coconut"))]

'''
Test that we can get a todo list with an offset and limit 
'''
def test_get_todos_offset_and_limit():
    response = client.post("/todo/apple")
    response = client.post("/todo/banana")
    response = client.post("/todo/coconut")
    response = client.get("/todos?offset=1&limit=1")
    assert response.status_code == 200
    assert response.json() == [jsonable_encoder(TodoItem(text="banana"))]

'''
Test that we can get a todo list with a limit greater than the to do size
'''
def test_get_todos_limit_greater_than_todo_size():
    response = client.post("/todo/apple")
    response = client.post("/todo/banana")
    response = client.post("/todo/coconut")
    response = client.get("/todos?limit=4")
    assert response.status_code == 200
    assert response.json() == [jsonable_encoder(TodoItem(text="apple")), jsonable_encoder(TodoItem(text="banana")), jsonable_encoder(TodoItem(text="coconut"))]

'''
Test that we can get a todo list with an offset greater than the to do size
'''
def test_get_todos_offset_greater_than_todo_size():
    response = client.post("/todo/apple")
    response = client.post("/todo/banana")
    response = client.post("/todo/coconut")
    response = client.get("/todos?offset=4")
    assert response.status_code == 200
    assert response.json() == []

'''
Test that when we get a to do list with a negative offset, it throws a 404.
'''
def test_get_todos_negative_offset():
    response = client.post("/todo/apple")
    response = client.post("/todo/banana")
    response = client.post("/todo/coconut")
    response = client.get("/todos?offset=-4")
    assert response.status_code == 422
    assert response.json() == {
    "detail": [
            {
                "type": "greater_than_equal",
                "loc": [
                    "query",
                    "offset"
                ],
                "msg": "Input should be greater than or equal to 0",
                "input": "-4",
                "ctx": {
                    "ge": 0
                }
            }
        ]
    }

'''
Test that when we get a to do list with a negative offset, it throws a 404.
'''
def test_get_todos_negative_limit():
    response = client.post("/todo/apple")
    response = client.post("/todo/banana")
    response = client.post("/todo/coconut")
    response = client.get("/todos?limit=-10")
    assert response.status_code == 422
    assert response.json() == {
    "detail": [
            {
                "type": "greater_than_equal",
                "loc": [
                    "query",
                    "limit"
                ],
                "msg": "Input should be greater than or equal to 0",
                "input": "-10",
                "ctx": {
                    "ge": 0
                }
            }
        ]
    }
'''
Tests what happens if a limit is zero.
'''
def test_get_zero_limit_offset():
    response = client.post("/todo/apple")
    response = client.post("/todo/banana")
    response = client.post("/todo/coconut")
    response = client.get("/todos?limit=0")
    assert response.status_code == 200
    assert response.json() == []

'''
Test what happens if an offset is zero
'''
def test_get_zero_offset_offset():
    response = client.post("/todo/apple")
    response = client.post("/todo/banana")
    response = client.post("/todo/coconut")
    response = client.get("/todos?offset=0")
    assert response.status_code == 200
    assert response.json() == [jsonable_encoder(TodoItem(text="apple")), jsonable_encoder(TodoItem(text="banana")), jsonable_encoder(TodoItem(text="coconut"))]

'''
Test completing a task
'''
def test_complete():
    response = client.post("/todo/apple")
    response = client.post("complete/0")
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(TodoItem(text="apple", completed=True))
    response = client.get("/todos/complete")
    assert response.status_code == 200
    assert response.json() == [jsonable_encoder(TodoItem(text="apple", completed=True))]

'''
Test completing a task twice
'''
def test_double_complete():
    response = client.post("/todo/apple")
    response = client.post("/complete/0")
    response = client.post("/complete/0")
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(TodoItem(text="apple", completed=True))
    response = client.get("/todos/complete")
    assert response.status_code == 200
    assert response.json() == [jsonable_encoder(TodoItem(text="apple", completed=True))]

'''
Test uncompleting a task
'''
def test_uncomplete():
    response = client.post("/todo/apple")
    response = client.post("/complete/0")
    response = client.post("/uncomplete/0")
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(TodoItem(text="apple"))
    response = client.get("/todos/incomplete")
    assert response.status_code == 200
    assert response.json() == [jsonable_encoder(TodoItem(text="apple"))]

'''
Test a get complete query with no reponses.
'''
def test_empty_complete():
    response = client.post("/todo/apple")
    response = client.get("/todos/complete")
    assert response.status_code == 200
    assert response.json() == []

'''
Test completing a task that doesn't exist
'''
def test_complete_ooindex():
    response = client.post("/complete/0")
    assert response.status_code == 404
    assert response.json() == "Index not found"
    response = client.post("/uncomplete/0")
    assert response.status_code == 404
    assert response.json() == "Index not found"

'''
Test completing a negative index
'''
def test_complete_negative_index():
    response = client.post("/complete/-1")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than_equal",
                "loc": [
                    "path",
                    "index"
                ],
                "msg": "Input should be greater than or equal to 0",
                "input": "-1",
                "ctx": {
                    "ge": 0
                }
            }
        ]
    }

    response = client.post("/uncomplete/-3")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than_equal",
                "loc": [
                    "path",
                    "index"
                ],
                "msg": "Input should be greater than or equal to 0",
                "input": "-3",
                "ctx": {
                    "ge": 0
                }
            }
        ]
    }

def test_negative_index():
    response = client.delete("/todo/-2")
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than_equal",
                "loc": [
                    "path",
                    "index"
                ],
                "msg": "Input should be greater than or equal to 0",
                "input": "-2",
                "ctx": {
                    "ge": 0
                }
            }
        ]
    }

def test_ooindex():
    response = client.delete("/todo/0")
    assert response.status_code == 404
    assert response.json() == "Index not found"