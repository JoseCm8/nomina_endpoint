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
def setup_usuario():
    """
    Configuración inicial para crear un usuario de prueba.
    """
    return {
        "username": "testuser",
        "password": "testpassword"
    }

def test_registrar_usuario(setup_usuario):
    """
    Prueba para registrar un usuario.
    """
    response = client.post("/usuarios/registro", json=setup_usuario)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == setup_usuario["username"]

def test_login_usuario(setup_usuario):
    """
    Prueba para autenticar un usuario.
    """
    # Registrar el usuario primero
    response = client.post("/usuarios/registro", json=setup_usuario)
    assert response.status_code == 200

    # Intentar iniciar sesión con las credenciales correctas
    login_data = {
        "username": setup_usuario["username"],
        "password": setup_usuario["password"]
    }
    response = client.post("/usuarios/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_usuario_incorrecto(setup_usuario):
    """
    Prueba para autenticar un usuario con credenciales incorrectas.
    """
    # Registrar el usuario primero
    response = client.post("/usuarios/registro", json=setup_usuario)
    assert response.status_code == 200

    # Intentar iniciar sesión con una contraseña incorrecta
    login_data = {
        "username": setup_usuario["username"],
        "password": "wrongpassword"
    }
    response = client.post("/usuarios/login", data=login_data)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Credenciales incorrectas"