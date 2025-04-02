# API de Nómina

Esta es una API desarrollada con **FastAPI** para gestionar la nómina de empleados. Permite registrar empleados, calcular su nómina y gestionar usuarios con autenticación basada en tokens JWT.

## Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Endpoints Principales](#endpoints-principales)
- [Pruebas](#pruebas)
- [Licencia](#licencia)

---

## Características

- **Gestión de Empleados**: Registro, consulta y cálculo de nómina.
- **Autenticación**: Login de usuarios con generación de tokens JWT.
- **Cálculo de Nómina**: Incluye deducciones como salud, pensión y fondo solidario.
- **Documentación Automática**: Disponible en `/docs` (Swagger) y `/redoc` (ReDoc).

---

## Requisitos

- Python 3.10 o superior
- MySQL (o cualquier base de datos compatible con SQLAlchemy)

---

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/JoseCm8/nomina_endpoint.git
   cd nomina_backend

2. Crea un entorno virtual e instálalo:
   ```bash
   python -m venv venv
   source venv/bin/activate
   
   En Windows:
   ```bash
   venv\Scripts\activate
   pip install -r requirements.txt

4. Configura la base de datos en el archivo .env.

5. Crea las tablas en la base de datos:
   python -c "from db.database import Base, engine; Base.metadata.create_all(bind=engine)"

   o ejecutar el script: "db/schema.sql"

## Ejecución
Para iniciar el servidor de desarrollo, ejecuta:

   uvicorn main:app --reload o fastapi dev main.py

   El servidor estará disponible en http://127.0.0.1:8000.

## Endpoints Principales
   Usuarios
   POST /usuarios/login/: Inicia sesión y genera un token JWT.
   GET /usuarios/perfil/: Obtiene el perfil del usuario autenticado.

   Empleados
   POST /empleados/: Registra un nuevo empleado.
   GET /empleados/: Consulta un empleado por su DNI.

## Pruebas
   Las pruebas están implementadas con pytest. Para ejecutarlas:

1. Instala las dependencias de prueba:
   pip install pytest
2. Ejecuta las pruebas:
   pytest tests/

## Licencia
Este proyecto está licenciado bajo la MIT License.
