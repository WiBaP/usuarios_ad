from fastapi import APIRouter
from service.senha_service import notificar_senhas, notificar_usuario

router = APIRouter(prefix="/senha", tags=["Senha"])

@router.post("/notificar")
def notificar():
    total = notificar_senhas()
    return {"emails_enviados": total}

@router.post("/notificar/{login}")
def notificar_um(login: str):
    ok = notificar_usuario(login)
    return {"sucesso": ok}
