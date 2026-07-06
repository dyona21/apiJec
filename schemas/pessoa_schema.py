from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date
from typing import Optional

class PessoaBase(BaseModel):
    nome: str
    cpf: str
    email: Optional[EmailStr] = None 
    data_nascimento: date
    adm: bool = False
    id_plano: Optional[int] = None

class PessoaCreate(BaseModel):
    nome: str
    cpf: str
    email: Optional[EmailStr] = None   
    senha: Optional[str] = None        
    data_nascimento: date
    adm: bool = False
    id_plano: Optional[int] = None

class PessoaResponse(PessoaBase):
    id: int 
    
    
    model_config = ConfigDict(from_attributes=True)