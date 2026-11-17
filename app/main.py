from fastapi import FastAPI

app = FastAPI(title="Hotel Pet API", version="0.1.0")


@app.get("/")
def raiz():
    return {"mensagem": "Hotel Pet API no ar"}