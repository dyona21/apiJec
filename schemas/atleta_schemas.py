from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class AtletaBase(BaseModel):
    posicao: str
    foto: Optional[str] = None
    partidas: int = 0
    gols: int = 0 

class AtletaComNomeResponse(BaseModel):
    id_pessoa: int
    nome: str     
    posicao: str
    foto: str | None = None
    partidas: int
    gols: int
    data_nascimento: date
    model_config = ConfigDict(from_attributes=True)

class Config:
        from_attributes = True

class AtletaCreate(AtletaBase):
    # Para criar um atleta, precisamos saber qual é o ID da Pessoa dele
    id_pessoa: int 

class AtletaResponse(AtletaBase):
    id_pessoa: int
    
    model_config = ConfigDict(from_attributes=True)

class AtletaUpdate(BaseModel):
    posicao: Optional[str] = None
    foto: Optional[str] = None
    partidas: Optional[int] = None
    gols: Optional[int] = None