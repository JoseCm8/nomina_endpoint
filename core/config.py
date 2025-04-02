from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql://root:1q2w3e4r@localhost/nomina"
    SECRET_KEY: str = "NOMINAJOSECM"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    VALOR_SALARIO_MINIMO: int = 1423500
    VALOR_AUX_TRANSPORTE: int = 200000

settings = Settings()