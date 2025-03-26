from typing import Optional
from pydantic import BaseModel


class ResidentialAreaCreate(BaseModel):
    id_residential_area: int = None
    name_residential_area: str
    city_residential_area: int
    total_houses: int
