from sqlalchemy import Column, Integer, String, Boolean #import the Column, Integer, and String classes from the sqlalchemy module
from database import Base #import the Base class from the database module

class TodoModel(Base): #create a TodoModel class that inherits from the Base class
    __tablename__ = "todo_db" #set the name of the database table to "todos"

    id = Column(Integer, primary_key=True, index=True) #create an id column that is an integer, is the primary key, and is indexed
    title = Column(String(255), index=True) #create a title column that is a string with a maximum length of 255 characters and is indexed
    description = Column(String(255), index=True, nullable=True) #create a description column that is a string with a maximum length of 255 characters and is indexed
    completed = Column(Boolean, default=False) #create a completed column that is a boolean and has a default value of False
