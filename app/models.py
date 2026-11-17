from sqlalchemy import Boolean, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Quarto(Base):
    __tablename__ = "quartos"

    id: Mapped[int] = mapped_column(primary_key=True)
    numero: Mapped[str] = mapped_column(String(10), unique=True)
    tipo: Mapped[str] = mapped_column(String(30))
    valor_diaria: Mapped[float] = mapped_column(Float)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)