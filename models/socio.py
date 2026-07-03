from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base # Importando a fundação que criamos no passo anterior
from pydantic import BaseModel

class Socio(Base):
    __tablename__ = "socio"

    id_pessoa = Column(Integer, ForeignKey("pessoa.id", ondelete="CASCADE"), primary_key=True)
    id_plano = Column(Integer, ForeignKey("plano_socio.id", ondelete="RESTRICT"), nullable=False)

    pessoa = relationship("Pessoa", back_populates="socio")
    plano = relationship("PlanoSocio", back_populates="socios")

