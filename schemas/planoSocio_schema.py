from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, Text

class PlanoSocioBase(BaseModel):
    nome_plano: str
    valor: Decimal
    vantagens: Optional[str] = None
    beneficio: Optional[str] = None
    forma_pagamento: Optional[str] = None

class PlanoSocioCreate(PlanoSocioBase):
    pass # Para criar, os dados da Base já são suficientes

class PlanoSocioResponse(PlanoSocioBase):
    id: int # O ID gerado pelo banco retorna aqui

    model_config = ConfigDict(from_attributes=True)