from typing import Union
from fastapi import FastAPI, HTTPException, status
from database import engine, Base, ToDo
from sqlalchemy.orm import Session

from fastapi_versioning import version, VersionedFastAPI

Base.metadata.create_all(engine)
import shemas

app = FastAPI()

@app.get("/")
def read_root():
    return "TODO app"

@app.post("/add", status_code=status.HTTP_201_CREATED)
@version(1)
def add_todo(todo: shemas.ToDo):
    """
        API call for adding a TODO item
    """
    session = Session(bind=engine, expire_on_commit= False)
    todoDB = ToDo(task = todo.task)
    session.add(todoDB)
    session.commit()
    id = todoDB.id
    session.close()
    return f"Created new TODO item with id {id}"

@app.delete("/change/{id}")
@version(1)
def change_todo(id: int):
    return "Create todo item with id {id}"

@app.delete("/change/{id}")
@version(2)
def change_todo(id: int, task:str):
    session = Session(bind=engine, expire_on_commit=False)
    todo = session.query(ToDo).get(id)
    if todo:
        #update
        todo.task = task
        session.commit()
    session.close()
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {id} does not exists!")
    return todo

@app.delete("/delete/{id}")
@version(1)
def delete_todo(id: int):
    return "Delete todo item with id {id}"

@app.delete("/delete/{id}")
@version(2)
def delete_todo(id: int):
    session = Session(bind=engine, expire_on_commit=False)
    todo = session.query(ToDo).get(id)
    if todo:
        #delete
        session.delete(todo)
        session.commit()
        session.close()
    else:
        session.close()
        raise HTTPException(status_code=404, detail=f"Todo with id {id} does not exists!")
    return "Delete todo item with id {id}"

@app.put("/update/{id}")
@version(1)
def update_todo():
    return "Update TODO"

@app.get("/get/{id}")
@version(1)
def get_todo():
    return "get TODO"

@app.get("/get/{id}")
@version(2)
def read_todo(id: int):
    session = Session(bind=engine, expire_on_commit= False)
    todo = session.query(ToDo).get(id)
    session.close()
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {id} does not exists!")
    return todo

@app.get("/list")
@version(1)
def get_all_todos():
    return "All todos"

@app.get("/list")
@version(2)
def get_all_todos():
    session = Session(bind=engine, expire_on_commit= False)
    todo_all = session.query(ToDo).all()
    session.close()
    return todo_all

app = VersionedFastAPI(app, version_format="{major}", prefix_format="/v{major}")