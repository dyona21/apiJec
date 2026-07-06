from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.atleta import Atleta
from models.pessoa import Pessoa
from schemas.atleta_schemas import AtletaCreate

def criar_atleta(db: Session, atleta_data: AtletaCreate):
    if atleta_data.partidas < 0:
        raise HTTPException(status_code=400, detail="O número de partidas não pode ser negativo.")

    atleta_existente = db.query(Atleta).filter(Atleta.id_pessoa == atleta_data.id_pessoa).first()
    if atleta_existente:
        raise HTTPException(status_code=409, detail="Este usuário já está cadastrado como atleta do elenco.")

    novo_atleta = Atleta(
        id_pessoa=atleta_data.id_pessoa,
        posicao=atleta_data.posicao,
        foto=atleta_data.foto,
        partidas=atleta_data.partidas,
        gols=atleta_data.gols
    )
    
    db.add(novo_atleta)
    db.commit()
    db.refresh(novo_atleta)
    return novo_atleta

def listar_atletas_completos(db: Session):
    resultados = db.query(
        Atleta.id_pessoa,
        Pessoa.nome,
        Atleta.posicao,
        Atleta.foto,
        Atleta.partidas,
        Atleta.gols,
        Pessoa.data_nascimento
        
    ).join(Pessoa, Atleta.id_pessoa == Pessoa.id).all()
    
    return resultados


def listar_atletas(db: Session, skip: int = 0, limit: int = 100):
    """
    Retorna a lista de todos os atletas do elenco atual (com paginação).
    """
    return db.query(Atleta).offset(skip).limit(limit).all()

def atualizar_atleta(db: Session, id_pessoa: int, dados_atualizados: dict):
    """
    Atualiza as estatísticas ou informações de um atleta (ex: adicionar uma nova partida jogada).
    """
    atleta = db.query(Atleta).filter(Atleta.id_pessoa == id_pessoa).first()
    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado no elenco.")

    if "partidas" in dados_atualizados and dados_atualizados["partidas"] < 0:
        raise HTTPException(status_code=400, detail="O número de partidas não pode ser negativo.")

    for chave, valor in dados_atualizados.items():
        setattr(atleta, chave, valor)

    db.commit()
    db.refresh(atleta)
    return atleta

def deletar_atleta(db: Session, id_pessoa: int):
    """
    Remove o atleta do elenco (deleta da tabela atleta, mas mantém na tabela pessoa).
    """
    atleta = db.query(Atleta).filter(Atleta.id_pessoa == id_pessoa).first()
    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado no elenco.")

    db.delete(atleta)
    db.commit()
    return {"mensagem": "Atleta removido do elenco com sucesso."}