from fastapi import FastAPI, Depends, HTTPException
from models import SeashellData, SeashellResponse  # data model for validation
from db import get_db_session, create_db, Seashell
from sqlalchemy.orm import Session

app = FastAPI()


@app.on_event("startup")
def starting_app():
    """
    Calls create_db(), which ensures table 'seashells' exists 
    """
    create_db()


@app.get("/seashells", status_code=200, response_model=list[SeashellResponse])
def list_seashells(session: Session = Depends(get_db_session)):
    seashells = session.query(Seashell).all()  # SELECT * FROM seashells
    return [SeashellResponse.model_validate(seashell) for seashell in seashells]  # Validation for list of SeashellResponse object type


@app.post("/seashells", status_code=201, response_model=SeashellResponse)
def add_seashell(seashell: SeashellData, session: Session = Depends(get_db_session)):
    new_seashell = Seashell(**seashell.model_dump())  # creates Seashell object
    session.add(new_seashell)  # Add new object
    session.commit()  # Commit changes in DB
    # Expire (remove loaded data from mem) + refresh value of seashells
    session.refresh(new_seashell)
    return SeashellResponse.model_validate(new_seashell)


@app.patch("/seashells/{seashell_id}", status_code=200, response_model=SeashellResponse)
def edit_seashell(seashell_id: int, new_seashell: SeashellData, session: Session = Depends(get_db_session)):
    seashell = session.query(Seashell).filter(
        Seashell.id == seashell_id).first()
    if not seashell:
        raise HTTPException(status_code=404, detail="Seashell not found")
    # UPDATE object
    changes_seashell = new_seashell.model_dump(
        exclude_unset=True)  # Only getting changed attributes
    for key, val in changes_seashell.items():  # for each attribute changed
        setattr(seashell, key, val)
    session.commit()
    session.refresh(seashell)
    return SeashellResponse.model_validate(seashell)


@app.delete("/seashells/{seashell_id}", status_code=204)
def delete_seashell(seashell_id: int, session: Session = Depends(get_db_session)):
    seashell = session.query(Seashell).filter(
        Seashell.id == seashell_id).first()
    if not seashell:
        raise HTTPException(status_code=404, detail="Seashell not found")
    session.delete(seashell)  # Deleting object
    session.commit()  # Commit changes
    return {"Message": f"Seashell {seashell_id} deleted"}  # Successful message
