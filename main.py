from fastapi import FastAPI
from routes import empleados, usuarios

app = FastAPI(
    title="API de Nómina",
    description="Esta API permite calcular la nómina de empleados.",
    version="1.0.0",
    contact={
        "name": "Jose Carrillo",
        "email": "jose.cm08@hotmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    documentacion="http://127.0.0.1:8000/redoc"
)

# Incluir rutas
app.include_router(usuarios.router)
app.include_router(empleados.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
