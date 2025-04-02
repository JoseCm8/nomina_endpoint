from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definir Base para los modelos
Base = declarative_base()

#Conexion a base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()