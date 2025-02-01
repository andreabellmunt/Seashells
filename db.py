from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Float 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() # Base for the data model in DB

# DEFINING TABLE seashells 
class Seashell(Base): # DB model     
    __tablename__ = "seashells"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    species = Column(String)
    color = Column(String)
    weight = Column(Float)
    description = Column(String)

# HANDLING THE CONNECTION TO DB 
db_file = "seashells.db"
db_url = f"sqlite:///{db_file}" # required url format 
engine = create_engine(db_url)# object handling comm with DB 
session = sessionmaker(engine) # DB session 

def create_db():
    """
    Creates DB with table 'seashells' if it does NOT exist yet. 
    """
    Base.metadata.create_all(engine)

def get_db_session(): 
    """
    Generates a new session dependency (each request uses a session). 
    """
    db_session = session() # new DB session 
    try: 
        yield db_session 
    finally: 
        db_session.close() # close session once done with request 
        