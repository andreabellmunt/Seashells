from fastapi import FastAPI, Depends, HTTPException
from models import SeashellData # data model for validation 
from db import get_db_session, create_db, Seashell 
from sqlalchemy.orm import Session

app = FastAPI()

@app.on_event("startup")
def starting_app(): 
    """
    Calls create_db(), which ensures table 'seashells' exists 
    """
    create_db()
    
@app.get("/seashells", status_code = 200) 
def list_seashells(session: Session = Depends(get_db_session)):
    seashells = session.query(Seashell).all() # SELECT * FROM seashells
    return seashells # Validation for list of SeashellResp object type
    
@app.post("/seashells", status_code = 201)
def add_seashell(seashell: SeashellData, session: Session = Depends(get_db_session)):
    new_seashell = Seashell(**seashell.dict()) # creates Seashell object 
    session.add(new_seashell) # Add new object 
    session.commit() # Commit changes in DB
    session.refresh(new_seashell) # Expire (remove loaded data from mem) + refresh value of seashells 
    return seashell 
    
@app.patch("/seashells/{seashell_id}", status_code = 200)
def edit_seashell(seashell_id: int, new_seashell: SeashellData, session: Session = Depends(get_db_session)): 
    seashell = session.query(Seashell).filter(Seashell.id == seashell_id).first() 
    if not seashell: 
        raise HTTPException(status_code = 404, detail = "Seashell not found")
    # UPDATE object 
    changes_seashell = new_seashell.dict(exclude_unset = True) # Only getting changed attributes
    for key, val in changes_seashell.items(): # for each attribute changed
        setattr(seashell, key, val)
    session.commit()
    session.refresh(seashell)
    return seashell 

@app.delete("/seashells/{seashell_id}", status_code = 204)
def delete_seashell(seashell_id: int, session: Session = Depends(get_db_session)):
    seashell = session.query(Seashell).filter(Seashell.id == seashell_id).first() 
    if not seashell: 
        raise HTTPException(status_code = 404, detail = "Seashell not found")
    session.delete(seashell) # Deleting object 
    session.commit() # Commit changes
    return {"Message" : f"Seashell {seashell_id} deleted"} # Successful message 