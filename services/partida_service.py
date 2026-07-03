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
    # Adicionamos o joinedload aqui também para garantir que a partida única venha com a competição
    return db.query(Partida).options(joinedload(Partida.competicao)).filter(func.date(Partida.data_hora) == data_partida).first()

def listar_partidas(db: Session):
    """
    Lista todas as partidas trazendo o objeto 'competicao' aninhado automaticamente.
    """
    # 👇 A MÁGICA ACONTECE AQUI:
    # Removemos aquela lista enorme de colunas e o .join() manual.
    # Pedimos a Partida inteira e mandamos "carregar junto" (joinedload) a competição.
    resultados = db.query(Partida).options(joinedload(Partida.competicao)).all()
    
    return resultados

def atualizar_partida(db: Session, partida_id: int, dados_atualizados: dict):
    """
    Atualiza os dados de uma partida existente garantindo as regras de negócio.
    """
    # 1. Busca a partida no banco
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada.")

    agora = datetime.now()
    
    # 2. Pega a nova data (se o admin enviou na atualização) ou mantém a data atual
    nova_data_hora = dados_atualizados.get("data_hora", partida.data_hora)

    # Regra 3 (Status do Jogo): Garantir placar se o jogo já passou
    if nova_data_hora < agora:
        novo_gol_jec = dados_atualizados.get("gols_jec", partida.gols_jec)
        novo_gol_adv = dados_atualizados.get("gols_adversa", partida.gols_adversa)
        
        if novo_gol_jec is None or novo_gol_adv is None:
            raise HTTPException(status_code=400, detail="A partida já ocorreu! É obrigatório informar o placar final.")

    # Regra 3 (Conflito de Horário): Verificar conflito APENAS se a data estiver sendo alterada
    if "data_hora" in dados_atualizados and dados_atualizados["data_hora"] != partida.data_hora:
        conflito = db.query(Partida).filter(Partida.data_hora == dados_atualizados["data_hora"]).first()
        if conflito:
            raise HTTPException(status_code=409, detail="Já existe outra partida cadastrada para este mesmo dia e horário.")

    # 3. Se passou pelas regras, atualiza os campos
    for chave, valor in dados_atualizados.items():
        setattr(partida, chave, valor)
        
    db.commit()
    db.refresh(partida)
    
    return partida

def deletar_partida(db: Session, partida_id: int):
    # 1. Busca a partida no banco
    partida_banco = db.query(Partida).filter(Partida.id == partida_id).first()
    
    # 2. Se ela não existir, avisa o front-end
    if not partida_banco:
        raise HTTPException(status_code=404, detail="Partida não encontrada.")
    
    # 3. Se existir, deleta e confirma a transação
    db.delete(partida_banco)
    db.commit()
    
    return True