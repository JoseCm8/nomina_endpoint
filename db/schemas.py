from pydantic import BaseModel
from datetime import date

class UsuarioSchema(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class EmpleadoSchema(BaseModel):
    nombre: str
    dni: str
    salario_mensual: float
    fecha_ingreso: date
    dias_laborados: int
    aux_transporte: bool

class EmpleadoFiltro(BaseModel):
    dni: str