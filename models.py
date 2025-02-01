from pydantic import BaseModel, PositiveFloat

# DATA MODEL FOR VALIDATION 
class SeashellData(BaseModel): 
    name: str 
    species: str | None 
    color: str | None 
    weight: PositiveFloat | None  # Weight cannot be negative 
    addDescription: str | None

