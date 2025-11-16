from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import date

# ----------------------
# User schemas
# ----------------------
class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr] = None

class UserRead(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

# ----------------------
# Actor schemas
# ----------------------
class ActorCreate(BaseModel):
    name: str
    birthdate: Optional[date] = None

class ActorRead(BaseModel):
    id: int
    name: str
    birthdate: Optional[date] = None

    class Config:
        orm_mode = True

class ActorUpdate(BaseModel):
    name: Optional[str] = None
    birthdate: Optional[date] = None

# ----------------------
# Movie schemas
# ----------------------
class MovieCreate(BaseModel):
    title: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    genre: Optional[str] = None

class MovieRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    genre: Optional[str] = None

    class Config:
        orm_mode = True

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    release_year: Optional[int] = None
    genre: Optional[str] = None

# ----------------------
# Review schemas
# ----------------------
class ReviewCreate(BaseModel):
    rating: Optional[conint(ge=1, le=10)] = None
    text: Optional[str] = None
    user_id: int

class ReviewRead(BaseModel):
    id: int
    rating: Optional[int] = None
    text: Optional[str] = None
    user_id: int
    movie_id: int

    class Config:
        orm_mode = True

class ReviewUpdate(BaseModel):
    rating: Optional[conint(ge=1, le=10)] = None
    text: Optional[str] = None
