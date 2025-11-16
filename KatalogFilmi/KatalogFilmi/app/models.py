from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    year: int
    genre: str

    reviews: list["Review"] = Relationship(back_populates="movie")
    movie_actors: list["MovieActorLink"] = Relationship(back_populates="movie")

class Actor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    birth_year: Optional[int] = None

    movie_actors: list["MovieActorLink"] = Relationship(back_populates="actor")

class MovieActorLink(SQLModel, table=True):
    movie_id: Optional[int] = Field(default=None, foreign_key="movie.id", primary_key=True)
    actor_id: Optional[int] = Field(default=None, foreign_key="actor.id", primary_key=True)

    movie: Optional[Movie] = Relationship(back_populates="movie_actors")
    actor: Optional[Actor] = Relationship(back_populates="movie_actors")

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    rating: int
    movie_id: Optional[int] = Field(default=None, foreign_key="movie.id")

    movie: Optional[Movie] = Relationship(back_populates="reviews")
