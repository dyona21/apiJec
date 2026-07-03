from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date
from typing import Optional

# 1. A Base: O que é comum para criar e para retornar
class PessoaBase(BaseModel):
    nome: str
    cpf: str
    email: Optional[EmailStr] = None # Valida automaticamente se tem @ e .com
    data_nascimento: date
    adm: bool = False
    id_plano: Optional[int] = None

class PessoaCreate(BaseModel):
    nome: str
    cpf: str
    email: Optional[EmailStr] = None   # <- era: email: str
    senha: Optional[str] = None        # <- era: senha: str
    data_nascimento: date
    adm: bool = False
    id_plano: Optional[int] = None

# 3. Schema de Resposta: O que o Python devolve para o Angular (GET)
class PessoaResponse(PessoaBase):
    id: int # O banco que gera o ID, então ele só aparece na resposta
    
    # Isso ensina o Pydantic a ler os dados mágicos do SQLAlchemy
    model_config = ConfigDict(from_attributes=True)