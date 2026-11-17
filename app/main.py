from fastapi import FastAPI

from app import models  # noqa: F401  (garante que as tabelas sejam registradas)
from app.database import Base, engine
from app.routers import quartos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hotel Pet API", version="0.2.0")
app.include_router(quartos.router)


@app.get("/")
def raiz():
    return {"mensagem": "Hotel Pet API no ar"}