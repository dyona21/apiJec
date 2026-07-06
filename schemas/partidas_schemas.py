from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class PartidaBase(BaseModel):
    adversario: str
    data_hora: datetime 
    local: str
    gols_jec: int = 0
    gols_adversa: int = 0
    descricao: Optional[str] = None
    link_dos_lances: Optional[str] = None

class CompeticaoResponse(BaseModel):
    id: int
    nomeCompeticao: str = Field(validation_alias="nome_competicao")
    
    model_config = ConfigDict(from_attributes=True) 

class PartidaCreate(BaseModel):
    adversario: str
    data_hora: datetime
    local: str
    id_competicao: int
    gols_jec: Optional[int] = 0
    gols_adversa: Optional[int] = 0
    descricao: Optional[str] = None
    link_dos_lances: Optional[str] = None #

class PartidaResponse(PartidaBase):
    id: int
    id_competicao: int
    
    competicao: CompeticaoResponse

    model_config = ConfigDict(from_attributes=True)