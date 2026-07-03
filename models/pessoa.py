from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base # Importando a fundação que criamos no passo anterior

# 1. Tabelas Base
class Pessoa(Base):
    __tablename__ = "pessoa"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    senha = Column(String(255))
    data_nascimento = Column(Date, nullable=False)
    adm = Column(Boolean, default=False)

    # Relacionamentos (Permite acessar jec.com/pessoa/1/atleta facilmente)
    atleta = relationship("Atleta", back_populates="pessoa", uselist=False)
    socio = relationship("Socio", back_populates="pessoa", uselist=False)