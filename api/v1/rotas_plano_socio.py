from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.planoSocio_schema import PlanoSocioCreate, PlanoSocioResponse
from services import plano_socio_service

router = APIRouter()

@router.post("/", response_model=PlanoSocioResponse, status_code=201)
def criar_plano(plano: PlanoSocioCreate, db: Session = Depends(get_db)):
    """
    Cadastra um novo tipo de plano de sócio-torcedor no catálogo.
    """
    return plano_socio_service.criar_plano(db=db, plano_data=plano)

@router.get("/{plano_id}", response_model=PlanoSocioResponse)
def buscar_plano(plano_id: int, db: Session = Depends(get_db)):
    """
    Busca os detalhes de um plano de sócio-torcedor específico pelo seu ID.
    """
    plano_encontrado = plano_socio_service.buscar_plano_por_id(db=db, plano_id=plano_id)
    
    if not plano_encontrado:
        raise HTTPException(status_code=404, detail="Plano não encontrado no banco de dados.")
        
    return plano_encontrado