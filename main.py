from fastapi import FastAPI
from routes import health, fap_routes
from database import connect_to_db, close_db_connection
from contextlib import asynccontextmanager

# Definir el lifespan de la aplicación para manejar la conexión a la base de datos 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    await connect_to_db()
    print("✅ Conectado a la base de datos")

    yield  # Aquí FastAPI empieza a atender peticiones

    # --- Shutdown ---
    await close_db_connection()
    print("🛑 Conexión cerrada")

# Crear la instancia principal de la aplicación
app = FastAPI(
    title="API Urgencias - Módulo Base",
    description="API inicial para el módulo de urgencias del hospital",
    version="1.0.0",
    lifespan=lifespan
)

# Ruta

app.include_router(health.router)
app.include_router(fap_routes.router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)