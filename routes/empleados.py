from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.schemas import EmpleadoSchema, EmpleadoFiltro
from db.models import Empleado
from services.empleados_service import crear_empleado, calcular_nomina, consultar_empleado

router = APIRouter(prefix="/empleados", tags=["Empleados"])

@router.post("/")
def registrar_empleado(empleado: EmpleadoSchema, db: Session = Depends(get_db)):
    """
    Crear un empleado.
    """
    try:
        nuevo_empleado = crear_empleado(db, empleado)
        nomina = calcular_nomina(nuevo_empleado)
        return {"empleado": nuevo_empleado, "nomina": nomina}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/")
def obtener_empleado(empleado_id: EmpleadoFiltro, db: Session = Depends(get_db)):
    """
    Consulta un empleado por su ID.
    """
    try:
        info_empleado = consultar_empleado(db, empleado_id.dni)
        return info_empleado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))