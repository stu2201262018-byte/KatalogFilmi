from sqlmodel import SQLModel, create_engine, Session

# Използваме SQLite база данни (файл movies.db в основната директория)
DATABASE_URL = "sqlite:///./movies.db"

# Създаваме SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Функция за създаване на таблиците (ако не съществуват)
def init_db():
    SQLModel.metadata.create_all(engine)

# Функция, която връща сесия към базата
def get_session():
    with Session(engine) as session:
        yield session

# Поддържаме съвместимост с кода, който използва SessionLocal
SessionLocal = Session
