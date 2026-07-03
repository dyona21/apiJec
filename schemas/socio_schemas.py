from pydantic import BaseModel, ConfigDict

class SocioBase(BaseModel):
    id_plano: int

class SocioCreate(SocioBase):
    id_pessoa: int 

from pydantic import BaseModel

class LoginSocio(BaseModel):
    cpf: str
    senha: str

class AlterarPlanoSocio(BaseModel):
    id_plano: int

class SocioResponse(SocioBase):
    id_pessoa: int

    model_config = ConfigDict(from_attributes=True)