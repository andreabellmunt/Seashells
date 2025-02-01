from pydantic import BaseModel, ConfigDict, PositiveFloat

# DATA MODEL FOR VALIDATION 
class SeashellData(BaseModel): 
    name: str 
    species: str | None 
    color: str | None 
    weight: PositiveFloat | None  # Weight cannot be negative 
    description: str | None

class SeashellResponse(SeashellData):
    model_config = ConfigDict(from_attributes=True)
    id: int 