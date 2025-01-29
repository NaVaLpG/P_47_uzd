from pydantic import BaseModel
import datetime


class CarScheme(BaseModel):
    id: int
    brand: str
    model: str
    model: str
    color: str
    year: int
    price: float
    age: int

    class Config:
        from_attributes = True
