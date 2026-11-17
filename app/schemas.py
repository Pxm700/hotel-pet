from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

Porte = Literal["pequeno", "médio", "grande"]


# ---------- Quartos ----------
class QuartoCriar(BaseModel):
    numero: str = Field(min_length=1, max_length=10)
    tipo: str = Field(min_length=1, max_length=30)
    valor_diaria: float = Field(gt=0)


class QuartoAtualizar(BaseModel):
    numero: Optional[str] = Field(default=None, min_length=1, max_length=10)
    tipo: Optional[str] = Field(default=None, min_length=1, max_length=30)
    valor_diaria: Optional[float] = Field(default=None, gt=0)
    ativo: Optional[bool] = None


class QuartoSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    numero: str
    tipo: str
    valor_diaria: float
    ativo: bool


# ---------- Tutores ----------
class TutorCriar(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    telefone: str = Field(min_length=8, max_length=20)
    email: Optional[str] = Field(default=None, max_length=120)


class TutorAtualizar(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=2, max_length=100)
    telefone: Optional[str] = Field(default=None, min_length=8, max_length=20)
    email: Optional[str] = Field(default=None, max_length=120)


class TutorSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    telefone: str
    email: Optional[str]


# ---------- Pets ----------
class PetCriar(BaseModel):
    tutor_id: int
    nome: str = Field(min_length=1, max_length=60)
    especie: str = Field(min_length=1, max_length=30)
    raca: Optional[str] = Field(default=None, max_length=60)
    porte: Optional[Porte] = None
    observacoes: Optional[str] = Field(default=None, max_length=300)


class PetAtualizar(BaseModel):
    tutor_id: Optional[int] = None
    nome: Optional[str] = Field(default=None, min_length=1, max_length=60)
    especie: Optional[str] = Field(default=None, min_length=1, max_length=30)
    raca: Optional[str] = Field(default=None, max_length=60)
    porte: Optional[Porte] = None
    observacoes: Optional[str] = Field(default=None, max_length=300)


class PetSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tutor_id: int
    nome: str
    especie: str
    raca: Optional[str]
    porte: Optional[str]
    observacoes: Optional[str]