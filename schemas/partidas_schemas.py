from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

# 1. Molde Base (Apenas as colunas reais que existem na tabela Partida)
class PartidaBase(BaseModel):
    adversario: str
    data_hora: datetime # Valida o momento exato do jogo
    local: str
    gols_jec: int = 0
    gols_adversa: int = 0
    descricao: Optional[str] = None
    link_dos_lances: Optional[str] = None
    # A propriedade 'competicao_nome' foi removida daqui, pois não é mais uma coluna solta!

# 2. Molde da Competição (O objeto que vai ficar dentro da partida)
class CompeticaoResponse(BaseModel):
    id: int
    nomeCompeticao: str = Field(validation_alias="nome_competicao")
    
    # Atualizado para o padrão do Pydantic V2
    model_config = ConfigDict(from_attributes=True) 

# 3. Molde de Criação (Usado no POST)
class PartidaCreate(BaseModel):
    adversario: str
    data_hora: datetime
    local: str
    id_competicao: int
    gols_jec: Optional[int] = 0
    gols_adversa: Optional[int] = 0
    descricao: Optional[str] = None
    link_dos_lances: Optional[str] = None #

# 4. Molde de Resposta (Usado no GET - O que vai para o Angular)
class PartidaResponse(PartidaBase):
    id: int
    id_competicao: int
    
    # 👇 A MÁGICA: O Pydantic agora sabe que deve empacotar a competição aqui dentro!
    competicao: CompeticaoResponse

    model_config = ConfigDict(from_attributes=True)