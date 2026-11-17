TUTOR = {"nome": "Maria Souza", "telefone": "11999990000", "email": "maria@exemplo.com"}


def criar_tutor(client):
    return client.post("/tutores", json=TUTOR).json()


def pet_de(tutor_id, nome="Rex"):
    return {"tutor_id": tutor_id, "nome": nome, "especie": "cachorro", "porte": "médio"}


def test_criar_tutor(client):
    resposta = client.post("/tutores", json=TUTOR)
    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "Maria Souza"


def test_tutor_com_telefone_curto_retorna_422(client):
    resposta = client.post("/tutores", json={**TUTOR, "telefone": "123"})
    assert resposta.status_code == 422


def test_buscar_tutor_inexistente_retorna_404(client):
    assert client.get("/tutores/999").status_code == 404


def test_buscar_tutor_por_nome(client):
    criar_tutor(client)
    resposta = client.get("/tutores", params={"nome": "souza"})
    assert [t["nome"] for t in resposta.json()] == ["Maria Souza"]


def test_criar_pet(client):
    tutor = criar_tutor(client)
    resposta = client.post("/pets", json=pet_de(tutor["id"]))
    assert resposta.status_code == 201
    assert resposta.json()["tutor_id"] == tutor["id"]


def test_criar_pet_com_tutor_inexistente_retorna_404(client):
    resposta = client.post("/pets", json=pet_de(999))
    assert resposta.status_code == 404


def test_porte_invalido_retorna_422(client):
    tutor = criar_tutor(client)
    resposta = client.post("/pets", json={**pet_de(tutor["id"]), "porte": "gigante"})
    assert resposta.status_code == 422


def test_listar_pets_do_tutor(client):
    tutor = criar_tutor(client)
    client.post("/pets", json=pet_de(tutor["id"], "Rex"))
    client.post("/pets", json=pet_de(tutor["id"], "Mel"))
    resposta = client.get(f"/tutores/{tutor['id']}/pets")
    assert [p["nome"] for p in resposta.json()] == ["Mel", "Rex"]


def test_nao_exclui_tutor_com_pets(client):
    tutor = criar_tutor(client)
    client.post("/pets", json=pet_de(tutor["id"]))
    assert client.delete(f"/tutores/{tutor['id']}").status_code == 409


def test_exclui_tutor_sem_pets(client):
    tutor = criar_tutor(client)
    assert client.delete(f"/tutores/{tutor['id']}").status_code == 204