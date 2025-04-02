from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

# Función para encriptar contraseñas
def hash_password(password: str):
    return pwd_context.hash(password)

# Función para verificar contraseñas
def verificar_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Función para crear el token JWT
def crear_token_jwt(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Función para verificar el token en las rutas protegidas
def verificar_token(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
