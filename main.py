from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from models import TodoModel
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI() #create an instance of the FastAPI class

TodoModel.metadata.create_all(bind=engine) #create the database tables based on the models defined in models.py

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Todo(BaseModel): #create a Pydantic model for the todo item
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

@app.get("/todos", response_model=List[Todo]) #retrieve all todo items from the database
def get_todos(db: Session = Depends(get_db)):
    return db.query(TodoModel).all()

@app.get("/todos/{todo_id}", response_model=Todo) #retrieve a specific todo item by id
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.post("/todos", response_model=Todo) #create a new todo item in the database
def create_todo(todo: Todo, db: Session = Depends(get_db)):
    db_todo = TodoModel(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.put("/todos/{todo_id}", response_model=Todo) #update a specific todo item by id
def update_todo(todo_id: int, updated_todo: Todo, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Update attributes dynamically
    for key, value in updated_todo.model_dump().items():
        setattr(db_todo, key, value)
        
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}") #delete a specific todo item by id
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

@app.delete("/todos") #delete all todo items
def delete_all_todos(db: Session = Depends(get_db)):
    db.query(TodoModel).delete()
    db.commit()
    return {"message": "All todos deleted successfully"}