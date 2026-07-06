from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.partidas_schemas import PartidaCreate, PartidaResponse
from services import partida_service
from typing import List
from datetime import date
from fastapi import HTTPException
from fastapi import status
from models.partida import Partida

router = APIRouter()

@router.post("/", response_model=PartidaResponse, status_code=201)
def agendar_partida(partida: PartidaCreate, db: Session = Depends(get_db)):
    """
    Agenda um novo jogo ou registra o resultado de um jogo passado.
    """
    return partida_service.criar_partida(db=db, partida_data=partida)

@router.get("/", response_model=List[PartidaResponse])
def listar_todas_partidas(db: Session = Depends(get_db)):
    return partida_service.listar_partidas(db=db)

@router.put("/{partida_id}")
def atualizar_partida(partida_id: int, partida_atualizada: PartidaCreate, db: Session = Depends(get_db)):
    
    partida_banco = db.query(Partida).filter(Partida.id == partida_id).first()
    
    if not partida_banco:
        raise HTTPException(status_code=404, detail="Partida não encontrada.")
    
    partida_banco.adversario = partida_atualizada.adversario
    partida_banco.data_hora = partida_atualizada.data_hora
    partida_banco.local = partida_atualizada.local
    partida_banco.id_competicao = partida_atualizada.id_competicao
    partida_banco.gols_jec = partida_atualizada.gols_jec
    partida_banco.gols_adversa = partida_atualizada.gols_adversa
    partida_banco.descricao = partida_atualizada.descricao
    partida_banco.link_dos_lances = partida_atualizada.link_dos_lances
    
    db.commit()
    db.refresh(partida_banco)
    return partida_banco

@router.get("/data/{data_partida}", response_model=PartidaResponse)
def buscar_partida_dia(data_partida: date, db: Session = Depends(get_db)):
    """
    Retorna a partida agendada para uma data específica (Formato: YYYY-MM-DD).
    """
    partida = partida_service.buscar_partida_por_data(db=db, data_partida=data_partida)
    
    if not partida:
        raise HTTPException(status_code=404, detail="Nenhuma partida do JEC/Krona encontrada para esta data.")
        
    return partida

@router.delete("/{partida_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_partida(partida_id: int, db: Session = Depends(get_db)):
    """
    Exclui uma partida do sistema.
    """
    partida_service.deletar_partida(db=db, partida_id=partida_id)
    return None
