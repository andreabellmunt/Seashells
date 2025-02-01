from fastapi import FastAPI, Depends, HTTPException
from decimal import Decimal 
from sqlmodel import SQLModel, Field, create_engine, Session, select # uses pydantic + sqlalchemy: data validation + interaction with db

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
    """ 
    Description: Lists all the seashells found in the DB table. 
    Parameters: Session dependency. 
    Returns: list of SeashellResp objects (id is included). 
    """
    seashells = session.exec(select(Seashell)).all() # SELECT * FROM seashells
    return seashells # Validation for list of SeashellResp object type
    
@app.post("/seashells", response_model = SeashellResp)
def add_seashell(new_seashell: SeashellAdd, session: Session = Depends(get_session)):
    """ 
    Description: Add a new Seashell object in the DB.  
    Parameters: SeashellAdd object (does not contain id), Session dependency. 
    Returns: SeashellResp object saved (contains id) 
    """
    seashell = Seashell.validate(new_seashell) 
    session.add(seashell) # Add new object 
    session.commit() # Commit changes in DB
    session.refresh(seashell) # Expire (remove loaded data from mem) + refresh value of seashells 
    return seashell # Validation for SeashellResp object type 
    
@app.patch("/seashells/{seashell_id}", response_model = SeashellResp)
def edit_seashell(seashell_id: int, new_seashell: SeashellAdd, session: Session = Depends(get_session)): 
    """ 
    Description: Edits an existing Seashell object entry  in the DB
    Parameters: ID for the seashell, SeashellAdd object (does not contain id), Session dependency. 
    Returns: SeashellResp object updated (contains id) 
    """
    seashell = session.get(Seashell, seashell_id)
    if not seashell: 
        raise HTTPException(status_code = 404, detail = "Seashell not found")
    # UPDATE object 
    changes_seashell = new_seashell.model_dump(exclude_unset = True) # Only getting changed attributes
    seashell.sqlmodel_update(changes_seashell) # Updating object 
    session.add(seashell) # Add new object to DB 
    session.commit()
    session.refresh(seashell)
    return seashell # Validation for SeashellResp object type

@app.delete("/seashells/{seashell_id}", status_code = 204)
def delete_seashell(seashell_id: int, session: Session = Depends(get_session)):
    """ 
    Description: Deletes an existing Seashell object entry  in the DB
    Parameters: ID for the seashell, Session dependency. 
    Return: Status code and, if successful, OK message
    """
    seashell = session.get(Seashell, seashell_id)
    if not seashell: 
        raise HTTPException(status_code = 404, detail = "Seashell not found")
    session.delete(seashell) # Deleting object 
    session.commit() # Commit changes
    return {"Message" : f"Seashell {seashell_id} deleted"} # Successful message 