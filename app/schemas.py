from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


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