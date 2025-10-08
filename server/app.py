# server/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.db import Base, engine
from server.controllers import auth_controller, file_controller, tracker_controller

# cria as tabelas no banco automaticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(title="P2P File Share API")

# CORS – libera acesso pra interface ou testes locais
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# health check
@app.get("/health")
def health():
    return {"ok": True}

# registra as rotas dos controladores
app.include_router(auth_controller.router)
app.include_router(file_controller.router)
app.include_router(tracker_controller.router) 