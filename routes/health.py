from fastapi import APIRouter, HTTPException
from database import query

router = APIRouter(prefix="/health")

@router.get("/")
async def health_check_db():
    """Verifica la conexión a la base de datos."""
    try:
        result = await query("SELECT 1", one=True)
        if result and result[0] == 1:
            return {"status": "ok", "message": "Conexión a la base de datos exitosa"}
        else:
            raise HTTPException(status_code=500, detail="Error inesperado en la base de datos")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar a la base de datos: {e}")
