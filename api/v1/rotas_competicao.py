from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.competicao_schemas import CompeticaoCreate, CompeticaoResponse
from services import competicao_service
from typing import List

router = APIRouter()

@router.post("/", response_model=CompeticaoResponse, status_code=201)
def registrar_competicao(competicao: CompeticaoCreate, db: Session = Depends(get_db)):
    """
    Registra um novo campeonato ou troféu conquistado.
    """
    return competicao_service.criar_competicao(db=db, competicao_data=competicao)

@router.get("/", response_model=List[CompeticaoResponse])
def listar_todas_competicoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Busca o catálogo de todas as competições (Sala de Troféus).
    """
    return competicao_service.listar_competicoes(db=db, skip=skip, limit=limit)