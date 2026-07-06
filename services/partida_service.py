from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from datetime import datetime, date
from sqlalchemy import func

from models.competicao import Competicao
from models.partida import Partida
from schemas.partidas_schemas import PartidaCreate

def criar_partida(db: Session, partida_data: PartidaCreate):
    agora = datetime.now()

    if partida_data.data_hora < agora:
        if partida_data.gols_jec is None or partida_data.gols_adversa is None:
            raise HTTPException(status_code=400, detail="A partida já ocorreu! É obrigatório informar o placar final.")

    conflito = db.query(Partida).filter(Partida.data_hora == partida_data.data_hora).first()
    if conflito:
        raise HTTPException(status_code=409, detail="Já existe uma partida cadastrada para este mesmo dia e horário.")

    nova_partida = Partida(
        adversario=partida_data.adversario,
        data_hora=partida_data.data_hora,
        local=partida_data.local,
        gols_jec=partida_data.gols_jec,
        gols_adversa=partida_data.gols_adversa,
        descricao=partida_data.descricao,
        id_competicao=partida_data.id_competicao, 
        link_dos_lances=partida_data.link_dos_lances
    )
    
    db.add(nova_partida)
    db.commit()
    db.refresh(nova_partida)
    return nova_partida

def buscar_partida_por_data(db: Session, data_partida: date):
    """
    Busca uma partida ignorando o horário, comparando apenas Ano-Mês-Dia.
    """
    return db.query(Partida).options(joinedload(Partida.competicao)).filter(func.date(Partida.data_hora) == data_partida).first()

def listar_partidas(db: Session):
    """
    Lista todas as partidas trazendo o objeto 'competicao' aninhado automaticamente.
    """
    resultados = db.query(Partida).options(joinedload(Partida.competicao)).all()
    
    return resultados

def atualizar_partida(db: Session, partida_id: int, dados_atualizados: dict):
    """
    Atualiza os dados de uma partida existente garantindo as regras de negócio.
    """
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada.")

    agora = datetime.now()
    
    nova_data_hora = dados_atualizados.get("data_hora", partida.data_hora)

    if nova_data_hora < agora:
        novo_gol_jec = dados_atualizados.get("gols_jec", partida.gols_jec)
        novo_gol_adv = dados_atualizados.get("gols_adversa", partida.gols_adversa)
        
        if novo_gol_jec is None or novo_gol_adv is None:
            raise HTTPException(status_code=400, detail="A partida já ocorreu! É obrigatório informar o placar final.")

    if "data_hora" in dados_atualizados and dados_atualizados["data_hora"] != partida.data_hora:
        conflito = db.query(Partida).filter(Partida.data_hora == dados_atualizados["data_hora"]).first()
        if conflito:
            raise HTTPException(status_code=409, detail="Já existe outra partida cadastrada para este mesmo dia e horário.")

    for chave, valor in dados_atualizados.items():
        setattr(partida, chave, valor)
        
    db.commit()
    db.refresh(partida)
    
    return partida

def deletar_partida(db: Session, partida_id: int):
    partida_banco = db.query(Partida).filter(Partida.id == partida_id).first()
    
    if not partida_banco:
        raise HTTPException(status_code=404, detail="Partida não encontrada.")
    
    db.delete(partida_banco)
    db.commit()
    
    return True