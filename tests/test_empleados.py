import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import Base, get_db
from main import app

# Configuración de la base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base de datos de prueba
Base.metadata.create_all(bind=engine)

# Sobrescribir la dependencia de la base de datos
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Cliente de prueba
client = TestClient(app)

@pytest.fixture
def setup_empleado():
    """
    Configuración inicial para crear un empleado de prueba.
    """
    return {
        "nombre": "Juan Pérez",
        "dni": "12345678",
        "salario_mensual": 2000000,
        "fecha_ingreso": "2025-01-01",
        "dias_laborados": 30,
        "aux_transporte": True
    }

def test_registrar_empleado(setup_empleado):
    """
    Prueba para registrar un empleado.
    """
    response = client.post("/empleados/", json=setup_empleado)
    assert response.status_code == 200
    data = response.json()
    assert data["empleado"]["nombre"] == setup_empleado["nombre"]
    assert data["empleado"]["dni"] == setup_empleado["dni"]

def test_obtener_empleado(setup_empleado):
    """
    Prueba para consultar un empleado por ID.
    """
    # Crear un empleado primero
    response = client.post("/empleados/", json=setup_empleado)
    assert response.status_code == 200
    empleado_id = response.json()["empleado"]["id"]

    # Consultar el empleado creado
    response = client.get(f"/empleados/{empleado_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == setup_empleado["nombre"]
    assert data["dni"] == setup_empleado["dni"]