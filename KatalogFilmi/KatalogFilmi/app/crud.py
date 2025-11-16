from sqlmodel import Session, select
from .models import Movie, Actor, Review, MovieActorLink


# ----- ФИЛМИ -----
def get_movies(session: Session):
    return session.exec(select(Movie)).all()


def get_movie(session: Session, movie_id: int):
    return session.get(Movie, movie_id)


def create_movie(session: Session, movie: Movie):
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie


def update_movie(session: Session, movie_id: int, updated_data: dict):
    movie = session.get(Movie, movie_id)
    if not movie:
        return None
    for key, value in updated_data.items():
        setattr(movie, key, value)
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie


def delete_movie(session: Session, movie_id: int):
    movie = session.get(Movie, movie_id)
    if not movie:
        return None
    session.delete(movie)
    session.commit()
    return movie


# ----- АКТЬОРИ -----
def get_actors(session: Session):
    return session.exec(select(Actor)).all()


def get_actor(session: Session, actor_id: int):
    return session.get(Actor, actor_id)


def create_actor(session: Session, actor: Actor):
    session.add(actor)
    session.commit()
    session.refresh(actor)
    return actor


def delete_actor(session: Session, actor_id: int):
    actor = session.get(Actor, actor_id)
    if not actor:
        return None
    session.delete(actor)
    session.commit()
    return actor


# ----- РЕВЮТА -----
def get_reviews(session: Session, movie_id: int):
    statement = select(Review).where(Review.movie_id == movie_id)
    return session.exec(statement).all()


def create_review(session: Session, review: Review):
    session.add(review)
    session.commit()
    session.refresh(review)
    return review


def delete_review(session: Session, review_id: int):
    review = session.get(Review, review_id)
    if not review:
        return None
    session.delete(review)
    session.commit()
    return review


# ----- ВРЪЗКИ ФИЛМИ - АКТЬОРИ -----
def link_actor_to_movie(session: Session, movie_id: int, actor_id: int):
    link = MovieActorLink(movie_id=movie_id, actor_id=actor_id)
    session.add(link)
    session.commit()
    return link


def get_movie_actors(session: Session, movie_id: int):
    statement = select(Actor).join(MovieActorLink).where(MovieActorLink.movie_id == movie_id)
    return session.exec(statement).all()
