from sqlalchemy import Column, Integer, String, Boolean, Date, DECIMAL
from db.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)


class Empleado(Base):
    __tablename__ = "empleados"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    dni = Column(String(20), unique=True, nullable=False)
    salario_mensual = Column(DECIMAL(10, 2), nullable=False)
    fecha_ingreso = Column(Date, nullable=False)
    dias_laborados = Column(Integer, nullable=False)
    aux_transporte = Column(Boolean, nullable=False)