from pydantic import BaseModel
from typing import List

class Patient(BaseModel):
    age: int
    weight: float
    conditions: List[str]
    allergies: List[str]
