import os #import the os module
from dotenv import load_dotenv #import the load_dotenv function from the dotenv module
from sqlalchemy import create_engine #import the create_engine function from the sqlalchemy module
from sqlalchemy.orm import sessionmaker #import the sessionmaker function from the sqlalchemy.orm module
from sqlalchemy.orm import declarative_base #import the declarative_base function from the sqlalchemy.orm module


load_dotenv() #load the environment variables from the .env file

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) #create a database engine using the DATABASE_URL environment variable
# It is a factory for creating database connections. It is used to manage the connection pool (which minimizes the cost of connecting to the database by reusing existing connections) and to execute SQL statements.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #create a session factory that will be used to create database sessions

Base = declarative_base() #create a base class for the database models to inherit from
