from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class HouseFeaturesSchema(BaseModel):
    id: int
    area: int
    year: int
    garage: int
    total_basement: int
    bath: int
    overall_quality: int
    neighborhood: str
    price: int

    class Config:
        orm_mode = True
