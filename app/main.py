from fastapi import FastAPI

from app import models  # noqa: F401
from app.database import Base, engine
from app.routers import pets, quartos, tutores

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hotel Pet API", version="0.3.0")
app.include_router(quartos.router)
app.include_router(tutores.router)
app.include_router(pets.router)


@app.get("/")
def raiz():
    return {"mensagem": "Hotel Pet API no ar"}