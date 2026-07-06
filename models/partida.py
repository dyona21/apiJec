from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base 

class Partida(Base):
    __tablename__ = "partida"

    id = Column(Integer, primary_key=True, index=True)
    adversario = Column(String(100), nullable=False)
    data_hora = Column(DateTime, nullable=False) 
    local = Column(String(150), nullable=False)
    gols_jec = Column(Integer, default=0)
    gols_adversa = Column(Integer, default=0)
    descricao = Column(Text)
    link_dos_lances = Column(String(255), nullable=True)
    id_competicao = Column(Integer, ForeignKey("competicao.id", ondelete="CASCADE"), nullable=False)

    competicao = relationship("Competicao", back_populates="partidas")