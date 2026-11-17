from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Pet, Tutor
from app.schemas import PetAtualizar, PetCriar, PetSaida

router = APIRouter(prefix="/pets", tags=["Pets"])


def buscar_pet_ou_404(db: Session, pet_id: int) -> Pet:
    pet = db.get(Pet, pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return pet


def garantir_tutor(db: Session, tutor_id: int) -> None:
    if db.get(Tutor, tutor_id) is None:
        raise HTTPException(status_code=404, detail="Tutor não encontrado")


@router.post("", response_model=PetSaida, status_code=status.HTTP_201_CREATED)
def criar_pet(dados: PetCriar, db: Session = Depends(get_db)):
    garantir_tutor(db, dados.tutor_id)
    pet = Pet(**dados.model_dump())
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet


@router.get("", response_model=list[PetSaida])
def listar_pets(
    tutor_id: Optional[int] = None,
    especie: Optional[str] = None,
    db: Session = Depends(get_db),
):
    consulta = select(Pet)
    if tutor_id is not None:
        consulta = consulta.where(Pet.tutor_id == tutor_id)
    if especie:
        consulta = consulta.where(Pet.especie == especie)
    return db.scalars(consulta.order_by(Pet.nome)).all()


@router.get("/{pet_id}", response_model=PetSaida)
def buscar_pet(pet_id: int, db: Session = Depends(get_db)):
    return buscar_pet_ou_404(db, pet_id)


@router.patch("/{pet_id}", response_model=PetSaida)
def atualizar_pet(pet_id: int, dados: PetAtualizar, db: Session = Depends(get_db)):
    pet = buscar_pet_ou_404(db, pet_id)
    mudancas = dados.model_dump(exclude_unset=True)
    if "tutor_id" in mudancas:
        garantir_tutor(db, mudancas["tutor_id"])
    for campo, valor in mudancas.items():
        setattr(pet, campo, valor)
    db.commit()
    db.refresh(pet)
    return pet


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = buscar_pet_ou_404(db, pet_id)
    db.delete(pet)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)