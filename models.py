from pydantic import BaseModel, ConfigDict, PositiveFloat
from typing import Optional

# DATA MODEL FOR VALIDATION 
class SeashellData(BaseModel): 
    name: Optional[str] = None 
    species: Optional[str] = None  
    color: Optional[str] = None 
    weight: Optional[PositiveFloat] = None # Weight cannot be negative 
    description: Optional[str] = None 

class SeashellResponse(SeashellData):
    model_config = ConfigDict(from_attributes=True)
    id: int 