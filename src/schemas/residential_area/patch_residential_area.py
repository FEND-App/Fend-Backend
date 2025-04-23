from typing import Optional
from pydantic import BaseModel


class ResidentialAreaPatch(BaseModel):
    name_residential_area: Optional[str] = None
    city_residential_area: Optional[int] = None
    total_houses: Optional[int] = None
    is_active: Optional[bool] = None
