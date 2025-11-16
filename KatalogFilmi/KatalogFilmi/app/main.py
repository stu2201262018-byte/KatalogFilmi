from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from app import models, database
import os

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.SQLModel.metadata.create_all(bind=database.engine)

frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.get("/")
async def root():
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "Филмов каталог"}


@app.get("/api/movies")
def get_movies():
    with Session(database.engine) as session:
        movies = session.exec(select(models.Movie)).all()
        return movies


@app.post("/api/movies")
def add_movie(movie: models.Movie):
    with Session(database.engine) as session:
        session.add(movie)
        session.commit()
        session.refresh(movie)
        return movie


@app.put("/api/movies/{movie_id}")
def update_movie(movie_id: int, updated_movie: models.Movie):
    with Session(database.engine) as session:
        movie = session.get(models.Movie, movie_id)
        if not movie:
            return {"error": "Филмът не е намерен"}
        
        movie.title = updated_movie.title
        movie.year = updated_movie.year
        movie.genre = updated_movie.genre
        
        session.add(movie)
        session.commit()
        session.refresh(movie)
        return movie


@app.delete("/api/movies/{movie_id}")
def delete_movie(movie_id: int):
    with Session(database.engine) as session:
        movie = session.get(models.Movie, movie_id)
        if not movie:
            return {"error": "Филмът не е намерен"}
        
        session.delete(movie)
        session.commit()
        return {"message": "Филмът е изтрит"}
