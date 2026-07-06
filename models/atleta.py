from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base 


class Atleta(Base):
    __tablename__ = "atleta"

    id_pessoa = Column(Integer, ForeignKey("pessoa.id", ondelete="CASCADE"), primary_key=True)
    posicao = Column(String(50), nullable=False)
    foto = Column(String(255))
    partidas = Column(Integer, default=0)
    gols = Column(Integer, default=0)

    pessoa = relationship("Pessoa", back_populates="atleta")
    
