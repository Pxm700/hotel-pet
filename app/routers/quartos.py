from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Quarto
from app.schemas import QuartoAtualizar, QuartoCriar, QuartoSaida

router = APIRouter(prefix="/quartos", tags=["Quartos"])


def buscar_quarto_ou_404(db: Session, quarto_id: int) -> Quarto:
    quarto = db.get(Quarto, quarto_id)
    if quarto is None:
        raise HTTPException(status_code=404, detail="Quarto não encontrado")
    return quarto


def numero_em_uso(db: Session, numero: str, ignorar_id: Optional[int] = None) -> bool:
    consulta = select(Quarto).where(Quarto.numero == numero)
    if ignorar_id is not None:
        consulta = consulta.where(Quarto.id != ignorar_id)
    return db.scalar(consulta) is not None


@router.post("", response_model=QuartoSaida, status_code=status.HTTP_201_CREATED)
def criar_quarto(dados: QuartoCriar, db: Session = Depends(get_db)):
    if numero_em_uso(db, dados.numero):
        raise HTTPException(status_code=409, detail="Já existe um quarto com esse número")
    quarto = Quarto(**dados.model_dump())
    db.add(quarto)
    db.commit()
    db.refresh(quarto)
    return quarto


@router.get("", response_model=list[QuartoSaida])
def listar_quartos(
    tipo: Optional[str] = None,
    apenas_ativos: bool = False,
    db: Session = Depends(get_db),
):
    consulta = select(Quarto)
    if tipo:
        consulta = consulta.where(Quarto.tipo == tipo)
    if apenas_ativos:
        consulta = consulta.where(Quarto.ativo.is_(True))
    return db.scalars(consulta.order_by(Quarto.numero)).all()


@router.get("/{quarto_id}", response_model=QuartoSaida)
def buscar_quarto(quarto_id: int, db: Session = Depends(get_db)):
    return buscar_quarto_ou_404(db, quarto_id)


@router.patch("/{quarto_id}", response_model=QuartoSaida)
def atualizar_quarto(quarto_id: int, dados: QuartoAtualizar, db: Session = Depends(get_db)):
    quarto = buscar_quarto_ou_404(db, quarto_id)
    mudancas = dados.model_dump(exclude_unset=True)

    novo_numero = mudancas.get("numero")
    if novo_numero and numero_em_uso(db, novo_numero, ignorar_id=quarto_id):
        raise HTTPException(status_code=409, detail="Já existe um quarto com esse número")

    for campo, valor in mudancas.items():
        setattr(quarto, campo, valor)
    db.commit()
    db.refresh(quarto)
    return quarto


@router.delete("/{quarto_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_quarto(quarto_id: int, db: Session = Depends(get_db)):
    quarto = buscar_quarto_ou_404(db, quarto_id)
    db.delete(quarto)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)