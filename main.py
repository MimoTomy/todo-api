from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware  # allows browser requests
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base, Todo

# creates all tables in the database on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

# this fixes CORS — allows the browser to talk to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # accept requests from any origin
    allow_methods=["*"],   # accept GET, POST, DELETE etc
    allow_headers=["*"],   # accept any headers
)

# GET /todos — fetch all todos from the database
@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

# POST /todos — add a new todo to the database
@app.post("/todos")
def add_todo(item: dict, db: Session = Depends(get_db)):
    todo = Todo(task=item["task"])  # create a new Todo object
    db.add(todo)                    # add it to the session
    db.commit()                     # save to database
    db.refresh(todo)                # refresh to get the new id
    return todo

# DELETE /todos/{id} — delete a todo by its id
@app.delete("/todos/{id}")
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()  # find the todo
    db.delete(todo)   # delete it
    db.commit()       # save the change
    return {"message": "Todo deleted!"}