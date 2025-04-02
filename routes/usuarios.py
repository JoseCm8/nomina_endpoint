from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Usuario
from db.schemas import UsuarioSchema, Token
from auth import verificar_password, crear_token_jwt, hash_password, verificar_token

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

# Endpoint para login y generación de JWT
@router.post("/login/", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.username == form_data.username).first()
    if not usuario or not verificar_password(form_data.password, usuario.password):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    token = crear_token_jwt({"sub": usuario.username})
    return {"access_token": token, "token_type": "bearer"}

# Endpoint para validar el token y obtener información del usuario
@router.get("/perfil/")
def perfil(usuario: str = Depends(verificar_token)):
    return {"usuario": usuario}
