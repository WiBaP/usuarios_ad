from fastapi import FastAPI
from controller import usuario_ad_controller, email_controller

app = FastAPI(title="Inventário de TI (Simples)")


app.include_router(usuario_ad_controller.router)
app.include_router(email_controller.router)

@app.get("/")
def root():
    return {"message": "Inventário rodando!"}
