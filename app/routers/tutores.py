from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Pet, Tutor
from app.schemas import PetSaida, TutorAtualizar, TutorCriar, TutorSaida

router = APIRouter(prefix="/tutores", tags=["Tutores"])


def buscar_tutor_ou_404(db: Session, tutor_id: int) -> Tutor:
    tutor = db.get(Tutor, tutor_id)
    if tutor is None:
        raise HTTPException(status_code=404, detail="Tutor não encontrado")
    return tutor


@router.post("", response_model=TutorSaida, status_code=status.HTTP_201_CREATED)
def criar_tutor(dados: TutorCriar, db: Session = Depends(get_db)):
    tutor = Tutor(**dados.model_dump())
    db.add(tutor)
    db.commit()
    db.refresh(tutor)
    return tutor


@router.get("", response_model=list[TutorSaida])
def listar_tutores(nome: Optional[str] = None, db: Session = Depends(get_db)):
    consulta = select(Tutor)
    if nome:
        consulta = consulta.where(Tutor.nome.ilike(f"%{nome}%"))
    return db.scalars(consulta.order_by(Tutor.nome)).all()


@router.get("/{tutor_id}", response_model=TutorSaida)
def buscar_tutor(tutor_id: int, db: Session = Depends(get_db)):
    return buscar_tutor_ou_404(db, tutor_id)


@router.get("/{tutor_id}/pets", response_model=list[PetSaida])
def listar_pets_do_tutor(tutor_id: int, db: Session = Depends(get_db)):
    buscar_tutor_ou_404(db, tutor_id)
    return db.scalars(select(Pet).where(Pet.tutor_id == tutor_id).order_by(Pet.nome)).all()


@router.patch("/{tutor_id}", response_model=TutorSaida)
def atualizar_tutor(tutor_id: int, dados: TutorAtualizar, db: Session = Depends(get_db)):
    tutor = buscar_tutor_ou_404(db, tutor_id)
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(tutor, campo, valor)
    db.commit()
    db.refresh(tutor)
    return tutor


@router.delete("/{tutor_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_tutor(tutor_id: int, db: Session = Depends(get_db)):
    tutor = buscar_tutor_ou_404(db, tutor_id)
    tem_pets = db.scalar(select(Pet.id).where(Pet.tutor_id == tutor_id).limit(1))
    if tem_pets is not None:
        raise HTTPException(
            status_code=409, detail="Tutor possui pets cadastrados. Exclua os pets antes."
        )
    db.delete(tutor)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)