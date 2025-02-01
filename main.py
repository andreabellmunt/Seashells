from fastapi import FastAPI
from mongoengine import connect, disconnect, Document, StringField, IntField
from enum import Enum 
from pydantic import BaseModel # offers data validation 

app = FastAPI()

""" 
    DEFINING DATA CLASSES
"""
# DB attributes
class Seashell(Document):
    id = IntField(required = True)
    name = StringField()
    species = StringField()
    color = StringField()
    size = StringField()
    addDescription = StringField()

# Type for class SeashellData
class SizeEnum(str, Enum):
    S = 'S' #small
    M = 'M' #medium
    L = 'L' #large 

# Data model managing input data (same structure as DB)
class SeashellData(BaseModel):
    id: int
    name: str | None
    species: str | None
    color: str | None 
    size: SizeEnum | None # Possible values: 'S', 'M', or 'L'
    addDescription: str | None # Additional description 


"""
    MANAGING THE DB CONNECTION: 
    - Name of the DB: seashells-db
    - Connect and disconnect based on app state 
"""

@app.on_event("startup")
async def connect_DB():
    connect("seashells-db") # default host and port are localhost 27017 
    
@app.on_event("shutdown")
async def disconnect_DB(): 
    disconnect("seashells-db")

"""
    API FUNCTIONS 
"""
@app.get("/seashells") 
async def list_seashells():
    return 
    
@app.post("/seashells")
async def add_seashell(seashells: SeashellData):
    
    
        

    

    
    

