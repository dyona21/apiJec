from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base # Importando a fundação que criamos no passo anterior
from typing import Optional

class PlanoSocio(Base):
    __tablename__ = "plano_socio"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, index=True)
    nome_plano = Column(String(50), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    vantagens = Column(Text)
    beneficio = Column(Text)
    forma_pagamento = Column(String)

    socios = relationship("Socio", back_populates="plano")