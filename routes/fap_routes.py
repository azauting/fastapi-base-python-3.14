from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from services.fap_service import get_fap_list

router = APIRouter(prefix="/fap", tags=["FAP"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def fap_list(request: Request):
    # Página completa
    faps = await get_fap_list(limit=10)
    return templates.TemplateResponse(
        "fap_list.html", {"request": request, "faps": faps}
    )


@router.get("/table", response_class=HTMLResponse)
async def fap_table(request: Request, estado: str | None = None, page: int = 1):
    limit = 5
    offset = (page - 1) * limit
    faps = await get_fap_list(limit=limit, offset=offset, estado=estado)
    return templates.TemplateResponse(
        "fap_table.html", {"request": request, "faps": faps}
    )
