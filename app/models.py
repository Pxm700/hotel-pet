from sqlalchemy import Boolean, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Quarto(Base):
    __tablename__ = "quartos"

    id: Mapped[int] = mapped_column(primary_key=True)
    numero: Mapped[str] = mapped_column(String(10), unique=True)
    tipo: Mapped[str] = mapped_column(String(30))
    valor_diaria: Mapped[float] = mapped_column(Float)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)


class Tutor(Base):
    __tablename__ = "tutores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    telefone: Mapped[str] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(120), nullable=True)


class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(primary_key=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey("tutores.id"))
    nome: Mapped[str] = mapped_column(String(60))
    especie: Mapped[str] = mapped_column(String(30))
    raca: Mapped[str | None] = mapped_column(String(60), nullable=True)
    porte: Mapped[str | None] = mapped_column(String(20), nullable=True)
    observacoes: Mapped[str | None] = mapped_column(String(300), nullable=True)