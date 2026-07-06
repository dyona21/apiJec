from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from models.competicao import Competicao
from schemas.competicao_schemas import CompeticaoCreate

def criar_competicao(db: Session, competicao_data: CompeticaoCreate):
    ano_atual = datetime.now().year

    if competicao_data.ano > ano_atual:
        raise HTTPException(status_code=400, detail=f"O ano da competição não pode ser superior ao ano atual ({ano_atual}).")

    if not competicao_data.foto or competicao_data.foto.strip() == "":
        raise HTTPException(status_code=400, detail="O link da imagem/foto do troféu é obrigatório para manter o layout do site consistente.")

    nova_competicao = Competicao(
        nome_competicao=competicao_data.nome_competicao,
        ano=competicao_data.ano,
        foto=competicao_data.foto,
        descricao=competicao_data.descricao
    )
    
    db.add(nova_competicao)
    db.commit()
    db.refresh(nova_competicao)
    return nova_competicao

def listar_competicoes(db: Session, skip: int = 0, limit: int = 100):
    """
    Retorna uma lista de todas as competições e troféus cadastrados, com suporte a paginação.
    """
    return db.query(Competicao).offset(skip).limit(limit).all()