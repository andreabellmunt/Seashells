from fastapi import FastAPI, Depends
from decimal import Decimal 
from sqlmodel import SQLModel, Field, create_engine, Session # uses pydantic + sqlalchemy: data validation + interaction with db


""" 
    DEFINING THE DATA MODELS
"""
class SeashellBase(SQLModel): # Base data model to generate others
    name: str | None 
    species: str | None 
    color: str | None
    weight:  Decimal = Field(max_digits=5, decimal_places=3) 
    addDescription: str | None 

class Seashell(SeashellBase, table = True): # DB model 
    id: int | None = Field(primary_key = True) # DB generates id
    
class SeashellAdd(SeashellBase): # Request model (we do NOT ask for id)
    pass # exactly the same as base

class SeashellResp(SeashellBase): # Response model 
    id: int # for responses, sharing the id 


"""
    MANAGING THE DB CONNECTION: 
    - DB: SQLite (uses one file)
    - Name of the file DB: seashells.db
    - Need to have Session to interact with DB and track changes 
"""

db_file = "seashells.db"
db_url = f"sqlite:///{db_file}" # required url format 
engine = create_engine(db_url)# object handling comm with DB 

def generate_table(): 
    """ 
    Generates table in DB if NOT existing yet 
    """
    SQLModel.metadata.create_all(engine)

def get_session(): 
    """
    Generates a new session dependency (each request uses a session)
    """
    with Session(engine) as session: 
        yield session 

"""
    API FUNCTIONS 
"""
app = FastAPI()

@app.on_event("startup")
def start_DB():
    """
    Calls generate_table() function, which creates or 
    ensures the table 'seashells' exists in the DB
    """
    generate_table()
    
@app.get("/seashells", response_model = list[SeashellResp]) 
def list_seashells(session: Session = Depends(get_session)):
    return 
    
@app.post("/seashells")
async def add_seashell():
