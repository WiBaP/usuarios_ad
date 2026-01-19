from fastapi import APIRouter
from db import ad  # db/ad.py

router = APIRouter(prefix="/usuarios-ad", tags=["Usuários AD"])

@router.post("/importar")
def importar_usuarios_ad():
    return ad.buscar_usuarios_ad()
