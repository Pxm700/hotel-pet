import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

engine_teste = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionTeste = sessionmaker(bind=engine_teste, autoflush=False, autocommit=False)


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine_teste)
    Base.metadata.create_all(bind=engine_teste)

    def get_db_teste():
        db = SessionTeste()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_db_teste
    yield TestClient(app)
    app.dependency_overrides.clear()


QUARTO = {"numero": "101", "tipo": "médio", "valor_diaria": 80}


def test_criar_quarto(client):
    resposta = client.post("/quartos", json=QUARTO)
    assert resposta.status_code == 201
    assert resposta.json()["numero"] == "101"
    assert resposta.json()["ativo"] is True


def test_numero_duplicado_retorna_409(client):
    client.post("/quartos", json=QUARTO)
    resposta = client.post("/quartos", json=QUARTO)
    assert resposta.status_code == 409


def test_valor_invalido_retorna_422(client):
    resposta = client.post("/quartos", json={**QUARTO, "valor_diaria": -5})
    assert resposta.status_code == 422


def test_buscar_inexistente_retorna_404(client):
    assert client.get("/quartos/999").status_code == 404


def test_listar_com_filtro_de_tipo(client):
    client.post("/quartos", json=QUARTO)
    client.post("/quartos", json={"numero": "201", "tipo": "grande", "valor_diaria": 120})
    resposta = client.get("/quartos", params={"tipo": "grande"})
    assert resposta.status_code == 200
    assert [q["numero"] for q in resposta.json()] == ["201"]


def test_atualizar_so_o_valor(client):
    criado = client.post("/quartos", json=QUARTO).json()
    resposta = client.patch(f"/quartos/{criado['id']}", json={"valor_diaria": 95})
    assert resposta.status_code == 200
    assert resposta.json()["valor_diaria"] == 95
    assert resposta.json()["numero"] == "101"


def test_atualizar_para_numero_existente_retorna_409(client):
    client.post("/quartos", json=QUARTO)
    outro = client.post("/quartos", json={**QUARTO, "numero": "102"}).json()
    resposta = client.patch(f"/quartos/{outro['id']}", json={"numero": "101"})
    assert resposta.status_code == 409


def test_excluir_quarto(client):
    criado = client.post("/quartos", json=QUARTO).json()
    assert client.delete(f"/quartos/{criado['id']}").status_code == 204
    assert client.get(f"/quartos/{criado['id']}").status_code == 404