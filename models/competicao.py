from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base 

class Competicao(Base):
    __tablename__ = "competicao"

    id = Column(Integer, primary_key=True, index=True)
    nome_competicao = Column(String(100), nullable=False)
    ano = Column(Integer, nullable=False)
    foto = Column(String(255))
    descricao = Column(Text)

    partidas = relationship("Partida", back_populates="competicao")