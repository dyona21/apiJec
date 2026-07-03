from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.atleta_schemas import AtletaCreate, AtletaResponse, AtletaUpdate
from services import atleta_service
from typing import List
from fastapi import HTTPException
from schemas.atleta_schemas import AtletaComNomeResponse

router = APIRouter()

# ... (seu código do @router.post já existente) ...

# @router.get("/", response_model=List[AtletaResponse])
# def listar_elenco(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     """
#     Busca a lista de todos os atletas que compõem o elenco atual.
#     """
#     return atleta_service.listar_atletas(db=db, skip=skip, limit=limit)

# O response_model aqui é o que exige que o 'nome' venha na resposta
@router.get("/", response_model=List[AtletaComNomeResponse])
def listar_atletas_completos(db: Session = Depends(get_db)):
    # Chama o service que faz o JOIN
    return atleta_service.listar_atletas_completos(db=db)

@router.put("/{id_pessoa}", response_model=AtletaResponse)
def atualizar_dados_atleta(id_pessoa: int, atleta_atualizado:  AtletaUpdate, db: Session = Depends(get_db)):
    """
    Edita as informações de um atleta (como atualizar a foto ou o número de partidas).
    """
    dados = atleta_atualizado.model_dump(exclude_unset=True)
    return atleta_service.atualizar_atleta(db=db, id_pessoa=id_pessoa, dados_atualizados=dados)

@router.delete("/{id_pessoa}", status_code=204)
def remover_atleta_elenco(id_pessoa: int, db: Session = Depends(get_db)):
    """
    Remove um jogador do elenco oficial.
    """
    atleta_service.deletar_atleta(db=db, id_pessoa=id_pessoa)
    return None


@router.post("/", response_model=AtletaResponse, status_code=201)
def cadastrar_atleta(atleta: AtletaCreate, db: Session = Depends(get_db)):
    """
    Adiciona uma pessoa existente ao elenco de atletas.
    """
    return atleta_service.criar_atleta(db=db, atleta_data=atleta)