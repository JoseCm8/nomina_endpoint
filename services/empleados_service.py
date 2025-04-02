from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.models import Empleado
from db.schemas import EmpleadoSchema
from core.config import settings
from datetime import datetime

import locale
locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8') # Configurar la localización para el formato de moneda en español (Colombia)

# Función para calcular la nómina de un empleado
def calcular_nomina(empleado: Empleado) -> dict:
    salario_proporcional = (empleado.salario_mensual / 30) * empleado.dias_laborados
    aux_transporte = settings.VALOR_AUX_TRANSPORTE if empleado.aux_transporte else 0
    total_devengado = salario_proporcional + aux_transporte
    total_devengado = float(total_devengado)
    salud = total_devengado * 0.04
    pension = total_devengado * 0.04
    fondo_solidario = 0
    if(total_devengado > (settings.VALOR_SALARIO_MINIMO * 4)):
        fondo_solidario = total_devengado * 0.01 
    salario_neto = total_devengado - (salud + pension)
    fecha_actual = datetime.today().date()
    dias_trabajados = (fecha_actual - empleado.fecha_ingreso).days
    dias_vacaciones = round((dias_trabajados / 360) * 15, 2)
    prima_servicio = (total_devengado * empleado.dias_laborados) / 360

    return {
        "salario_mensual": locale.currency(empleado.salario_mensual, grouping=True),
        "salario_proporcional": locale.currency(salario_proporcional, grouping=True),
        "aux_transporte": locale.currency(aux_transporte, grouping=True),
        "total_devengado": locale.currency(total_devengado, grouping=True),
        "deducciones": {"salud": locale.currency(salud, grouping=True), "pension": locale.currency(pension, grouping=True), "fondo_solidario": locale.currency(fondo_solidario, grouping=True), "total": locale.currency(salud + pension + fondo_solidario, grouping=True)},
        "salario_neto": locale.currency(salario_neto, grouping=True),
        "vacaciones": f"{dias_vacaciones} dias",
        "prima_servicio": locale.currency(round(prima_servicio, 2), grouping=True),
    }
# Crear un nuevo empleado en la base de datos
def crear_empleado(db: Session, empleado_data: EmpleadoSchema) -> Empleado:
    nuevo_empleado = Empleado(**empleado_data.dict())

    #Validacion valor de salario vs aplica auxilio de transporte
    if (nuevo_empleado.salario_mensual > (settings.VALOR_SALARIO_MINIMO * 2) and nuevo_empleado.aux_transporte == True):
        raise HTTPException(status_code=400, detail="Revise la informacion ingresada, no puede tener auxilio de transporte")
    
    #Validacion logica dias trabajados vs fecha ingreso
    fecha_actual = datetime.today().date()
    dias_trabajados = (fecha_actual - nuevo_empleado.fecha_ingreso).days
    if(dias_trabajados < nuevo_empleado.dias_laborados):
        raise HTTPException(status_code=400, detail="Revise la informacion ingresada, no pudo haber laborado esa cantidad de dias")

    db.add(nuevo_empleado)
    db.commit()
    db.refresh(nuevo_empleado)
    return nuevo_empleado
# Consultar un empleado por su ID
def consultar_empleado(db: Session, empleado_id: str) -> Empleado:
    empleado = db.query(Empleado).filter(Empleado.dni == empleado_id).first()

    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    info_empleado = {
        "empleado": {
            "detail": "Empleado en la base de datos",
            "id": empleado.id,
            "nombre": empleado.nombre,
            "dni": empleado.dni,
            "salario_mensual": empleado.salario_mensual,
            "fecha_ingreso": empleado.fecha_ingreso,
            "dias_laborados": empleado.dias_laborados,
            "aux_transporte": empleado.aux_transporte
        },
        "nomina": calcular_nomina(empleado)
    }
    return info_empleado