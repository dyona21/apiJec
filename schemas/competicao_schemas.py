from pydantic import BaseModel, ConfigDict
from typing import Optional

class CompeticaoBase(BaseModel):
    nome_competicao: str
    ano: int
    foto: Optional[str] = None
    descricao: Optional[str] = None

class CompeticaoCreate(CompeticaoBase):
    pass

class CompeticaoResponse(CompeticaoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)