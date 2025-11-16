from .database import SessionLocal

# Тази функция се използва за достъп до базата данни
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
